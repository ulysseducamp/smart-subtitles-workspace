# CLAUDE.md - SmartSub API Backend

Documentation pour Claude Code sur l'architecture et le fonctionnement du backend FastAPI de Smart Subtitles.

## Vue d'ensemble

Le backend FastAPI traite les sous-titres en fusionnant intelligemment les pistes de langue cible (PT) et langue native (FR) selon le niveau de vocabulaire de l'utilisateur.

**Status:** ✅ PRODUCTION LIVE (Phase 2C/3 complete - Nov 2025)

**Architecture système:**
- **Webapp**: Next.js 15 (`webapp-next/`) pour auth + billing (Supabase + Stripe) - LIVE
- **API Backend**: FastAPI (ce repo) pour traitement de sous-titres uniquement - LIVE
- **Extension**: Chrome Web Store (submitted) - intègre webapp + API

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

#### `src/subtitle_fusion.py` (~1100 lignes)
- **Rôle:** Moteur principal de fusion de sous-titres
- **Classe:** `SubtitleFusionEngine`
- **Méthode principale:** `fuse_subtitles(target_subs, native_subs, known_words, full_frequency_list, lang, ...)`

**Algorithme de fusion:**
1. **Analyse vocabulaire** - `_analyze_subtitle_words()` détection 2-phase (capitalization → lemmatization → frequency check)
2. **Décision par sous-titre:**
   - Tous les mots connus → Garder sous-titre PT
   - 1 mot inconnu → Traduction inline via `apply_translation()` (regex + word boundaries)
   - 2+ mots inconnus → Remplacer par sous-titre FR
3. **Synchronisation temporelle** - Bidirectionnelle avec calcul d'overlap
4. **Batch translation** - Collecte tous les mots à traduire, puis traduction parallèle

**Changements récents:**
- ✅ **Nov 2025 - Architecture Refactor:** Suppression TokenMapping, ajout `apply_translation()` + `_analyze_subtitle_words()`, distinction `known_words` vs `full_frequency_list`, regex word boundaries (fix bug "et" dans "Antoinette")
- ✅ Jan 2025: Suppression déduplication cache, traduction contextuelle parfaite, filtre "avalanche", native fallback system

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
- **Fonctions clés:**
  - `get_top_n_words(lang, n)` - Top N mots (niveau utilisateur)
  - `get_full_list(lang)` - Liste complète (détection noms propres)
- **Langues supportées:** EN, FR, PT, ES (EN maintenu pour backend mais retiré de l'UI frontend)
- **Usage:** Distinction `known_words` (top N) vs `full_frequency_list` (tous mots) pour détecter mots rares vs noms propres

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

### Bug #1: "et" traduit dans "Antoinette" (RÉSOLU - Novembre 2025)

**Symptôme:** "Marie-Antoinette" split en 2 mots → "et" traduit inside → "Antoin**et (and)**te"

**Cause:** TokenMapping index alignment + split hyphenated words

**Solution (Architecture Refactor):** Regex avec word boundaries `\b` + mots pré-normalisés
- `apply_translation()`: Pattern `\b + word + \b` empêche match partiel
- Mots déjà normalisés (lowercase, no punctuation) avant traduction
- Regex gère ponctuation automatiquement: "mange," → "mange (eats),"

**Résultats:** Bug 100% résolu, architecture simplifiée (-98 lignes code mort)

**Code:** `subtitle_fusion.py:18-59` - `apply_translation()` function

### Bug #2: Collision de dict avec même mot nettoyé (NON PRIORITAIRE - Janvier 2025)

**Symptôme:** Même mot apparaît plusieurs fois dans un batch → Dict écrase les traductions précédentes (ex: "banco" dans "Banco do Brasil" vs "sentei no banco")

**Impact:** ~0.5-1% des batches, traduction contextuelle incorrecte pour 1-2 mots par épisode affecté

**Statut:** Documenté, non résolu. Workaround acceptable pour l'impact mineur.

**Solution recommandée (pour implémentation future):**
- Clé composite : `f"{clean_word}|||{context[:20]}"` comme clé dict
- Garde la robustesse du système Dict word-based
- Risque : OpenAI pourrait nettoyer le séparateur (testable)
- Estimation : ~20 lignes, 1h dev+test

**Code concerné:**
- `subtitle_fusion.py:863-876` - Préparation OpenAI avec `word_cleaning_map`
- `subtitle_fusion.py:921-941` - Application des traductions avec `translations.get(clean_word)`

### Bug #2: Subtitle Loss (RÉSOLU - Janvier 2025)

**Symptôme:** Sous-titres avec même mot inconnu disparaissaient (seul le dernier était gardé)

**Cause:** Déduplication via dict `word_to_subtitle_mapping[word] = subtitle` écrasait les précédents

**Solution:** Suppression de la déduplication, utilisation de liste de tuples

### Bug #3: Double affichage PT+FR (RÉSOLU - Janvier 2025)

**Symptôme:** PT 633 et FR 629+630 affichés simultanément

**Cause:** FR 629 correspondait mieux à PT 632, mais était groupé avec PT 633

**Solution:** Filtre "avalanche" - Exclure FR qui overlap mieux avec PT précédent

## Fonctionnalités clés

### 1. Word Analysis & Proper Noun Detection (Architecture Nov 2025)
- **Fonction:** `_analyze_subtitle_words(text, lang, known_words, full_frequency_list)`
- **Détection 2-phase:**
  1. **Phase capitalization:** Mark words as `confirmed_proper` (mid-sentence caps), `potential_proper` (sentence start), `normal`
  2. **Phase lemmatization + frequency:** Potential → lemmatize → check if in `known_words` (common), `full_frequency_list` (rare word to translate), or neither (proper noun)
- **Returns:** `normalized_words`, `lemmatized_words`, `word_statuses`, `proper_nouns`, `unknown_words`
- **Code:** `subtitle_fusion.py:169-283`

### 2. Translation Application (Architecture Nov 2025)
- **Fonction:** `apply_translation(subtitle_text, word, translation)`
- **Approche:** Regex avec word boundaries `\b + escaped_word + \b` + flag `IGNORECASE`
- **Avantages:** Matche toutes occurrences, préserve casse originale, évite match partiel ("et" pas dans "Antoinette")
- **Code:** `subtitle_fusion.py:18-59`

### 3. Smart Lemmatization
- **Top 200 mots:** Pas de lemmatisation (évite "uma" → "umar")
- **Autres mots:** Lemmatisation via simplemma
- **Pourquoi:** Les outils NLP portugais ont des bugs sur les mots fonctionnels

### 4. Avalanche Prevention
- **Problème:** Un sous-titre FR peut mieux matcher le PT précédent que le PT actuel
- **Solution:** Comparer overlap avec PT précédent, exclure si meilleur match
- **Code:** `subtitle_fusion.py:658-692`

### 5. Native Fallback System
- **Déclenchement:** Quand traduction inline échoue (mot absent du dict OpenAI)
- **Fonctions:** `_find_best_native_match()`, `_apply_native_fallback()`
- **Logique:** Réutilise synchronisation temporelle pour trouver sous-titre natif correspondant
- **Stats:** `fallbackCount` tracking dans logs (~0% actuellement, GPT-4.1 Nano très fiable)
- **Code:** `subtitle_fusion.py:405-543, 1113-1139`

### 6. Parallel Translation
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

- [x] ~~Résoudre traductions échouées~~ - RÉSOLU: Dict-based matching + native fallback
- [x] ~~Bug "et" dans "Antoinette"~~ - RÉSOLU: Architecture refactor Nov 2025, regex word boundaries
- [x] ~~Améliorer tokenization~~ - OBSOLÈTE: TokenMapping supprimé, remplacé par architecture simplifiée

## Références

- **WORD_ALIGNMENT_ARCHITECTURE.md** - Décisions architecture refactor Nov 2025 (word processing, proper nouns detection)
- **MASTER_DOC.md** - Documentation complète du projet (720+ lignes)
- **CLAUDE.md** (racine) - Documentation extension Chrome
- **Railway Production:** `smartsub-api-production.up.railway.app`
- **Railway Staging:** `smartsub-api-staging.up.railway.app`
