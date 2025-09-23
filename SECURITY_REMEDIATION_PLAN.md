## Security Remediation Plan

### 🔴 Critiques (bloquants ou à traiter en premier)
- [x] PostMessage non sécurisé (content/page scripts): utiliser `window.location.origin`, valider `event.origin` et `event.source === window`, schéma strict du payload.
- [x] Permission manquante dans `manifest.json`: ajouter `"tabs"` (usage de `chrome.tabs`).
- [x] API ouverte par omission: exiger `API_KEY` en production; unifier `RAILWAY_API_KEY`/`API_KEY` → une seule clé côté middleware et proxy.

### 🟡 Modérées (à planifier juste après)
- [x] Proxy: ne plus transmettre la clé en query string; passer par un header `X-API-Key`.
- Uploads: valider la taille en streaming (ne pas se fier à `UploadFile.size`/filename), vérifier encodage/texte et gérer `UnicodeDecodeError`.
- Erreurs API: ne pas exposer `str(e)` côté client; logs serveurs + message générique 500.
- JSON monkey‑patch global: limiter la portée (cibler `fetch` des endpoints Netflix) ou restaurer rapidement `JSON` si nécessaire.
- CORS: conserver restriction Netflix; documenter l’ajustement futur si client → `chrome-extension://`.

### 🟢 Mineures (durcissement/maintenance)
- DOM injection: remplacer `innerHTML` par rendu sûr (texte + mapping i/u/b) ou sanitisation stricte.
- Logs verbeux: réduire les logs en build production (extension + backend).
- Dépendances: retirer `supabase` de `requirements.txt` (non utilisée) et `node` de `/package.json` (inutile).

### Notes d’exécution
- Priorité: traiter d’abord les points critiques (Chrome Web Store + exposition API), puis modérés, puis mineurs.
- Tests: valider extension (build prod) et API (staging → prod) après chaque groupe de correctifs.

