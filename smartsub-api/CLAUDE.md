# CLAUDE.md - SmartSub API Backend

Documentation pour Claude Code sur l'architecture et le fonctionnement du backend FastAPI de Smart Subtitles.

## Vue d'ensemble

Le backend FastAPI traite les sous-titres en fusionnant intelligemment les pistes de langue cible (PT) et langue native (FR) selon le niveau de vocabulaire de l'utilisateur.

**Flow principal:**
```
Client HTTP → FastAPI Endpoint → Subtitle Fusion Engine → OpenAI/DeepL Translation → Processed Subtitles
```

## Architecture des fichiers

### Fichiers principaux

#### `main.py` (240+ lignes)
- **Rôle:** Point d'entrée FastAPI avec sécurité et rate limiting
- **Endpoints:**
  - `POST /fuse-subtitles` - Fusion de sous-titres avec traduction inline
  - `POST /proxy-railway` - Proxy pour Railway API
- **Sécurité:**
  - Rate limiting in-memory (10 req/min par IP)
  - Validation de taille de fichier (5MB max)
  - CORS restreint aux domaines Netflix
  - Gestion d'API keys serveur-side

#### `src/subtitle_fusion.py` (900+ lignes)
- **Rôle:** Moteur principal de fusion de sous-titres
- **Classe:** `SubtitleFusionEngine`
- **Méthode principale:** `fuse_subtitles(target_subs, native_subs, lang, native_lang, top_n, ...)`

**Algorithme de fusion:**
1. **Analyse vocabulaire** - Détermine quels mots sont connus via frequency lists
2. **Décision par sous-titre:**
   - Tous les mots connus → Garder sous-titre PT
   - 1 mot inconnu → Traduction inline `mot (translation)`
   - 2+ mots inconnus → Remplacer par sous-titre FR
3. **Synchronisation temporelle** - Bidirectionnelle avec calcul d'overlap
4. **Batch translation** - Collecte tous les mots à traduire, puis traduction parallèle

**Changements récents (Janvier 2025):**
- ✅ Suppression de la déduplication du cache pour éviter la perte de sous-titres
- ✅ Traduction contextuelle parfaite avec clés uniques `word_INDEX`
- ✅ Filtre "avalanche" - Compare FR avec PT précédent pour éviter double affichage
- ❌ **BUG ACTUEL:** Système de clés uniques cause échec de 33% des traductions (voir section Bugs)

#### `src/openai_translator.py` (390+ lignes)
- **Rôle:** Traduction contextuelle via OpenAI GPT-4.1 Nano ou Google Gemini
- **Classe:** `OpenAITranslator`
- **Méthodes clés:**
  - `translate_batch_with_context()` - Traduction synchrone d'un batch
  - `translate_batch_parallel()` - Traduction parallèle avec semaphore (8 requêtes simultanées)

**Architecture:**
- **Structured Outputs** - Schema Pydantic pour JSON garanti
- **Context-aware** - Chaque mot reçoit le texte du sous-titre comme contexte
- **Parallel execution** - Chunks de 18 mots, max 8 requêtes concurrentes
- **Cache in-memory** - Évite les traductions répétées

**Structured Output Schema:**
```python
class WordTranslation(BaseModel):
    word: str          # Le mot à traduire
    translation: str   # La traduction
```

#### `src/frequency_loader.py`
- **Rôle:** Chargement des listes de fréquence de mots au démarrage
- **Fonction:** `load_frequency_list(lang)` - Charge top 800 mots par langue
- **Langues supportées:** EN, FR, PT, ES
- **Usage:** Détermine si un mot est "connu" (dans top N)

#### `src/lemmatizer.py`
- **Rôle:** Lemmatisation intelligente des mots
- **Fonction principale:** `smart_lemmatize_line(text, lang)`
- **Logique:**
  - Top 200 mots les plus fréquents → **Pas de lemmatisation** (évite bugs comme "uma" → "umar")
  - Autres mots → Lemmatisation via `simplemma`

#### `src/srt_parser.py`
- **Rôle:** Parsing et génération de fichiers SRT
- **Fonctions:**
  - `parse_srt(srt_content)` - Parse SRT en objets `Subtitle`
  - `generate_srt(subtitles)` - Génère SRT depuis objets
  - `normalize_words(text)` - Normalise texte (expand contractions, lowercase, filtre)

#### `src/deepl_api.py`
- **Rôle:** Fallback translation sans contexte via DeepL
- **Usage:** Seulement si OpenAI échoue
- **Limitation:** Pas de contexte subtitle, juste traduction de mot

## Data Flow détaillé

### 1. Collection des mots à traduire

**Code actuel (develop branch):**
```python
# subtitle_fusion.py lignes 526-629
subtitles_to_translate = []  # Liste de tuples (word, subtitle)

for current_target_sub in target_subs:
    # Analyse des mots inconnus
    if len(unknown_words) == 1:
        # Trouve le mot original via token mappings
        original_word = mapping.original_word  # Ex: "tensão]", "delegada", "motor."

        # Collecte le tuple (PAS de déduplication)
        subtitles_to_translate.append((original_word, current_target_sub))
```

**Problème:** `original_word` contient la ponctuation attachée:
- `"tensão]"` (crochet du markup SRT `[música de tensão]`)
- `"delegada"` (pas de ponctuation)
- `"motor."` (point de fin de phrase)

### 2. Construction des clés uniques

**Code actuel (develop branch):**
```python
# subtitle_fusion.py lignes 829-838
word_contexts = {}
words_to_translate = []

for idx, (word, subtitle) in enumerate(subtitles_to_translate):
    unique_key = f"{word}_{idx}"  # Ex: "tensão]_126", "delegada_132"
    word_contexts[unique_key] = strip_html(subtitle.text)
    words_to_translate.append(unique_key)
```

**Envoyé à OpenAI:**
- `words_to_translate = ["tensão]_126", "motor._127", "delegada_132", ...]`
- `word_contexts = {"tensão]_126": "música de tensão", "motor._127": "som do motor", ...}`

### 3. Traduction OpenAI

**Prompt généré:**
```
TASK: Translate 18 Portuguese words to French.

WORD CONTEXTS (each word with its subtitle):
- "tensão]_126" appears in: "música de tensão"
- "motor._127" appears in: "som do motor"
- "delegada_132" appears in: "Eu sou a delegada Lavelle."
...

TRANSLATION RULES:
1. Use the subtitle context to understand how the word is used
2. Provide natural translations as a native speaker would say
3. Keep translations concise (1-3 words maximum)
...
```

**Structured Output attendu:**
```json
{
  "translations": [
    {"word": "tensão]_126", "translation": "tension"},
    {"word": "motor._127", "translation": "moteur"},
    ...
  ]
}
```

**Problème:** OpenAI peut "nettoyer" le champ `word`:
- Retourne `{"word": "tensão]", "translation": "tension"}` (sans `_126`)
- Ou `{"word": "tensão", "translation": "tension"}` (sans crochet ni index)
- Ou `{"word": "motor", "translation": "moteur"}` (sans point ni index)

### 4. Application des traductions

**Code actuel:**
```python
# subtitle_fusion.py lignes 882-908
for idx, (original_word, subtitle) in enumerate(subtitles_to_translate):
    unique_key = f"{original_word}_{idx}"  # Ex: "tensão]_126"
    translation = translations.get(unique_key)  # Cherche clé exacte

    if translation:
        # Applique la traduction ✅
        new_text = pattern.sub(f"{original_word} ({translation})", subtitle.text)
    else:
        # Pas de traduction trouvée ❌
        logger.warning(f"⚠️  No translation for '{original_word}' in subtitle {subtitle.index}")
```

**Résultat:** Si OpenAI retourne `"tensão]"` au lieu de `"tensão]_126"`:
- `translations = {"tensão]": "tension", ...}`
- `translations.get("tensão]_126")` → `None`
- Warning: `"⚠️  No translation for 'tensão]' in subtitle 1"`

## Bugs connus

### Bug #1: 33% des traductions échouent (ACTUEL - Janvier 2025)

**Symptôme:** Logs Railway montrent `✅ OpenAI parallel translation successful! Translated 232 subtitles` mais ensuite beaucoup de `⚠️  No translation for 'tensão]' in subtitle 1 - keeping original`

**Statistiques:**
- Envoyé: 348 mots (19 chunks × 18 + 1 chunk × 6)
- Retourné: 232 traductions
- **Échoué: 116 traductions (33%)**

**Exemples d'échecs:**
```
✅ Mots traduits: 'aumenta]' → 'augmente' (subtitle 403)
✅ Mots traduits: 'desconectadas!' → 'déconnectées' (subtitle 401)
❌ Pas de traduction: 'tensão]' (subtitle 1, 8, 36, 60, 77, ...)
❌ Pas de traduction: 'delegada' (subtitle 11)
❌ Pas de traduction: 'relatório,' (subtitle 132)
```

**Cause racine:**
1. **Clés uniques avec index** - On envoie `"tensão]_126"` à OpenAI
2. **OpenAI normalise** - Il retourne `{"word": "tensão]", "translation": "tension"}` (sans l'index!)
3. **Mismatch de clés** - On cherche `translations["tensão]_126"]` → `None`

**Pourquoi certains marchent et d'autres pas?**
OpenAI est **inconsistant** dans sa normalisation:
- Parfois il garde la clé exacte: `"aumenta]_403"` → ✅
- Parfois il enlève l'index: `"tensão]"` (au lieu de `"tensão]_126"`) → ❌
- Parfois il nettoie aussi la ponctuation: `"tensão"` (au lieu de `"tensão]_126"`) → ❌

**Code concerné:**
- `subtitle_fusion.py:834-838` - Construction des clés uniques
- `openai_translator.py:184-193` - Parsing de la réponse OpenAI
- `subtitle_fusion.py:884-908` - Application des traductions avec `translations.get(unique_key)`

**Logs de debug ajoutés (à vérifier):**
```python
# openai_translator.py:186-188
logger.info(f"   [OPENAI] 🔍 DEBUG: OpenAI returned {len(parsed_data.translations)} translations")
logger.info(f"   [OPENAI] 🔍 DEBUG: First 5 translations: {[(item.word, item.translation) for item in parsed_data.translations[:5]]}")
```

**Ancien code (avant changements):**
```python
# Pas de clés uniques, juste le mot avec ponctuation
if original_word not in unknown_words_to_translate:
    unknown_words_to_translate.append(original_word)  # Ex: "tensão]"

# Envoi à OpenAI
word_contexts["tensão]"] = "música de tensão"

# Réception
translations = {"tensão]": "tension"}  # OpenAI retourne la même clé
translations.get("tensão]")  # ✅ Match!
```

### Bug #2: Subtitle Loss (RÉSOLU - Janvier 2025)

**Symptôme:** Sous-titres avec même mot inconnu disparaissaient (seul le dernier était gardé)

**Cause:** Déduplication via dict `word_to_subtitle_mapping[word] = subtitle` écrasait les précédents

**Solution:** Suppression de la déduplication, utilisation de liste de tuples

### Bug #3: Double affichage PT+FR (RÉSOLU - Janvier 2025)

**Symptôme:** PT 633 et FR 629+630 affichés simultanément

**Cause:** FR 629 correspondait mieux à PT 632, mais était groupé avec PT 633

**Solution:** Filtre "avalanche" - Exclure FR qui overlap mieux avec PT précédent

## Fonctionnalités clés

### 1. Token Mapping System
- **Rôle:** Préserve l'alignement entre mots originaux et lemmatisés
- **Classe:** `TokenMapping` (dataclass)
- **Champs:** `original_word`, `normalized_word`, `lemmatized_word`, `is_filtered`, `original_index`
- **Usage:** Résout le problème d'alignement quand certains mots sont filtrés

### 2. Smart Lemmatization
- **Top 200 mots:** Pas de lemmatisation (évite "uma" → "umar")
- **Autres mots:** Lemmatisation via simplemma
- **Pourquoi:** Les outils NLP portugais ont des bugs sur les mots fonctionnels

### 3. Avalanche Prevention
- **Problème:** Un sous-titre FR peut mieux matcher le PT précédent que le PT actuel
- **Solution:** Comparer overlap avec PT précédent, exclure si meilleur match
- **Code:** `subtitle_fusion.py:658-692`

### 4. Parallel Translation
- **Chunks:** 18 mots par requête OpenAI
- **Concurrency:** 8 requêtes simultanées (38% du rate limit OpenAI de 500 RPM)
- **Performance:** 7.80s → 3.95s (-49%), traitement total 10.03s → 6.87s (-32%)

## Configuration

### Environment Variables
```bash
DEEPL_API_KEY=xxx          # DeepL API key (fallback)
OPENAI_API_KEY=xxx         # OpenAI API key (primary)
API_KEY=xxx                # Auth key pour endpoints
MAX_FILE_SIZE=5242880      # 5MB
```

### Startup
```bash
cd smartsub-api/
source venv/bin/activate
python main.py
```

### Testing
```bash
# Test complet de l'API
python test_fuse_subtitles_endpoint.py

# Tests unitaires
python -m pytest tests/ -v
```

## Performance

### Métriques typiques (épisode 40 min)
- **Traduction:** ~350 mots, 20 chunks, 8.37s
- **Tokens:** ~12,000 input + ~4,000 output
- **Coût:** ~$0.004 par épisode
- **Taux de remplacement:** ~72% des sous-titres traités

## Notes importantes

1. **Ne jamais utiliser `npm run build` directement** - Toujours spécifier staging ou production
2. **Railway auto-deploy** - Branch `develop` → staging, branch `main` → production
3. **Logs Railway** - Limite 500 logs/sec, risque de truncation si trop de debug
4. **Cache OpenAI** - In-memory, perdu au redémarrage, pas de persistence
5. **Rate limiting** - In-memory, par IP, pas partagé entre instances Railway

## TODO / Investigations en cours

- [ ] **PRIORITÉ 1:** Résoudre le bug des 33% de traductions échouées
  - Option A: Faire matcher les clés de manière plus flexible (fuzzy matching)
  - Option B: Demander à OpenAI de garder les clés exactes dans le prompt
  - Option C: Post-processing pour mapper les réponses d'OpenAI aux clés originales

- [ ] Vérifier si le problème de ponctuation existe aussi (`.`, `,`, `!`, `?`)

- [ ] Améliorer le tokenization dans `create_alignment_mapping()` pour séparer ponctuation

- [ ] Analyser les logs Railway pour comprendre le pattern exact de normalisation d'OpenAI

## Références

- **MASTER_DOC.md** - Documentation complète du projet (720+ lignes)
- **CLAUDE.md** (racine) - Documentation extension Chrome
- **Railway Production:** `smartsub-api-production.up.railway.app`
- **Railway Staging:** `smartsub-api-staging.up.railway.app`
