# PostHog Setup Guide - Subly Landing Funnel Analytics

Ce guide explique comment PostHog est configuré et comment l'utiliser pour analyser votre tunnel de conversion landing.

## ✅ Installation (Complète)

PostHog est installé et configuré avec:
- ✅ `posthog-js` installé
- ✅ `PostHogProvider` créé avec session replay et masking de données sensibles
- ✅ Variables d'environnement configurées
- ✅ Auto-pageview tracking activé (defaults: '2025-11-30')

## 📊 Funnel Landing Principal (20 étapes)

Votre tunnel landing se compose de **2 parties** :

### **Partie 1: Discovery (7 étapes)**

Les utilisateurs découvrent comment fonctionne Subly:

1. `/landing` - Hero page (point d'entrée)
2. `/landing/intro` - Introduction au concept
3. `/landing/magic` - Explication de la "magie"
4. `/landing/known-words` - Concept des mots connus
5. `/landing/explanation-4` - Explication 4
6. `/landing/explanation-5` - Explication 5
7. `/landing/comparison` - Comparaison finale

### **Partie 2: Setup (13 étapes)**

Configuration et paiement:

8. `/landing/setup/vocab-intro` - Introduction au test de vocabulaire
9. `/landing/setup/target-language` - Sélection langue cible
10. `/landing/setup/explanation-1` - Explication 1
11. `/landing/setup/explanation-2` - Explication 2
12. `/landing/setup/vocab-test` - **Test de vocabulaire** (étape clé)
13. `/landing/setup/analyzing` - Analyse des résultats
14. `/landing/setup/results` - Affichage du niveau
15. `/landing/setup/finish-cta` - CTA pour continuer
16. `/landing/setup/native-language` - Sélection langue native
17. `/landing/setup/auth` - **Authentification Google** (étape clé)
18. `/landing/setup/post-auth` - Post-authentification
19. `/landing/setup/pricing` - **Page de paiement Stripe** 💰 (étape critique)
20. `/landing/setup/complete` - **Conversion finale** 🎉

## 🎯 Créer le funnel dans PostHog Dashboard

### 1. Accéder aux funnels

1. Allez sur https://app.posthog.com/project/107396/insights
2. Cliquez sur **"New insight"** → **"Funnel"**

### 2. Configurer le funnel "Landing Complet" (20 étapes)

Pour chaque étape, ajoutez un événement **Pageview** :

**Comment ajouter une étape** :
- Cliquez sur **"+ Add funnel step"**
- Sélectionnez **"Pageview"**
- Ajoutez un filtre : **"Current URL"** → **"contains"** → `/landing`

**Liste des 20 étapes à configurer** :
```
1. Pageview → Current URL contains "/landing" (exact, pas /landing/)
2. Pageview → Current URL contains "/landing/intro"
3. Pageview → Current URL contains "/landing/magic"
4. Pageview → Current URL contains "/landing/known-words"
5. Pageview → Current URL contains "/landing/explanation-4"
6. Pageview → Current URL contains "/landing/explanation-5"
7. Pageview → Current URL contains "/landing/comparison"
8. Pageview → Current URL contains "/landing/setup/vocab-intro"
9. Pageview → Current URL contains "/landing/setup/target-language"
10. Pageview → Current URL contains "/landing/setup/explanation-1"
11. Pageview → Current URL contains "/landing/setup/explanation-2"
12. Pageview → Current URL contains "/landing/setup/vocab-test"
13. Pageview → Current URL contains "/landing/setup/analyzing"
14. Pageview → Current URL contains "/landing/setup/results"
15. Pageview → Current URL contains "/landing/setup/finish-cta"
16. Pageview → Current URL contains "/landing/setup/native-language"
17. Pageview → Current URL contains "/landing/setup/auth"
18. Pageview → Current URL contains "/landing/setup/post-auth"
19. Pageview → Current URL contains "/landing/setup/pricing"
20. Pageview → Current URL contains "/landing/setup/complete"
```

### 3. Configuration du funnel

- **Conversion window** : 7 jours (temps maximum pour compléter le funnel)
- **Breakdown by** : Device type, Browser, ou User properties (langue cible)
- **Name** : "Landing Funnel - Complet (20 étapes)"

### 4. Sauvegarder

Cliquez sur **"Save insight"** → Donnez un nom descriptif

## 🔍 Funnels complémentaires recommandés

### Funnel "Partie 1 - Discovery" (7 étapes)

Pour analyser spécifiquement la phase de découverte :
- Étapes 1 à 7 (de `/landing` à `/landing/comparison`)
- **Objectif** : Mesurer combien d'utilisateurs arrivent au setup

### Funnel "Partie 2 - Setup + Conversion" (13 étapes)

Pour analyser la phase de configuration et paiement :
- Étapes 8 à 20 (de `/landing/setup/vocab-intro` à `/landing/setup/complete`)
- **Objectif** : Mesurer le taux de conversion après la découverte

### Funnel "Micro-conversion Paiement" (3 étapes critiques)

Focus sur la conversion finale :
```
1. Pageview → /landing/setup/auth (Google OAuth)
2. Pageview → /landing/setup/pricing (Page paiement)
3. Pageview → /landing/setup/complete (Conversion!)
```
- **Objectif** : Identifier les frictions sur le paiement Stripe

## 🎥 Session Replay - Analyser les drop-offs

### Comment utiliser les replays

1. **Dashboard PostHog** → **Session Replay** → **Recordings**
2. **Filtrer par drop-off** :
   - Cliquez sur votre funnel
   - Cliquez sur un segment avec fort drop-off (ex: étape 19 → 20)
   - Cliquez sur **"View recordings"**

### Analyses recommandées

**Questions à se poser en regardant les replays** :

**Drop-off étape 12 (vocab-test)** :
- Les users abandonnent-ils pendant le test ?
- Combien de temps passent-ils sur la page ?
- Cliquent-ils sur "Retour" ?

**Drop-off étape 17 (auth)** :
- Est-ce que le bouton Google OAuth est visible ?
- Y a-t-il des erreurs dans la console ?
- Les users hésitent-ils avant de cliquer ?

**Drop-off étape 19 → 20 (pricing → complete)** :
- Les users cliquent-ils sur "Subscribe" ?
- Reviennent-ils après avoir quitté Stripe Checkout ?
- Y a-t-il des erreurs réseau ?

### Métriques à surveiller dans les replays

Pour chaque étape critique, observez :
- ✅ **Temps passé** sur la page
- ✅ **Clics effectués** (sur quel élément en premier ?)
- ✅ **Scroll behavior** (lisent-ils tout le contenu ?)
- ✅ **Erreurs JavaScript** (console logs)
- ✅ **Hésitations** (mouvements de souris erratiques)

## 🔒 Sécurité et Privacy

### Données automatiquement maskées

Le `PostHogProvider` masque :
- ✅ **Tous les inputs** (emails, mots de passe, formulaires)
- ✅ **Éléments avec `data-sensitive`**
- ✅ **Iframes Stripe Checkout** (pas enregistré)

### Données sécurisées exposées

- ✅ **`NEXT_PUBLIC_POSTHOG_KEY`** - Clé publique par design (comme `NEXT_PUBLIC_SUPABASE_ANON_KEY`)
- ✅ **`NEXT_PUBLIC_POSTHOG_HOST`** - URL publique

Ces clés sont **CONÇUES** pour être exposées côté client. PostHog gère la sécurité via rate limiting et RLS sur leur backend.

## 📈 Métriques clés à suivre

### Taux de conversion global

- **Landing → Complete** : (Users à l'étape 20 / Users à l'étape 1) × 100
- **Target** : >5% (benchmark e-commerce/SaaS)

### Drop-offs critiques à surveiller

1. **Étape 1 → 2** : Les users cliquent-ils sur "Discover how it works" ?
2. **Étape 12 (vocab-test)** : Abandons pendant le test
3. **Étape 17 (auth)** : Friction sur Google OAuth
4. **Étape 19 → 20 (pricing → complete)** : Conversion paiement Stripe

### Temps moyen par étape

PostHog calcule automatiquement le **temps passé** sur chaque page. Identifiez les pages où les users passent trop de temps (confusion ?) ou trop peu (pas assez engageant ?).

## 🚀 Déploiement Vercel

### Variables d'environnement à ajouter

**Pour Staging** (`staging-subly-extension.vercel.app`) :
1. Vercel Dashboard → Projet → Settings → Environment Variables
2. Environnement **Preview** :
   ```
   NEXT_PUBLIC_POSTHOG_KEY=phc_KDT8LPdCMBCmCrN70dYu4FU3I1YbEco3bbCdv3fMdlw
   NEXT_PUBLIC_POSTHOG_HOST=https://eu.i.posthog.com
   ```

**Pour Production** (`subly-extension.vercel.app`) :
1. Environnement **Production** :
   ```
   NEXT_PUBLIC_POSTHOG_KEY=phc_KDT8LPdCMBCmCrN70dYu4FU3I1YbEco3bbCdv3fMdlw
   NEXT_PUBLIC_POSTHOG_HOST=https://eu.i.posthog.com
   ```

**Note** : Même projet PostHog pour les deux environnements. Vous pouvez filtrer par `NEXT_PUBLIC_APP_URL` dans PostHog si besoin de séparer staging/production.

### Redéployer

Après avoir ajouté les variables :
```bash
# Vercel Dashboard: Deployments → Redeploy
# Ou via Vercel CLI:
vercel --prod   # Production
vercel          # Staging
```

## 🔧 Debugging

### PostHog ne charge pas

Vérifiez :
1. **Variables d'environnement** : Présentes dans Vercel et `.env.local`
2. **Console browser** (localhost) : "PostHog loaded successfully"
3. **Network tab** : Requêtes vers `eu.i.posthog.com`

### Replays ne s'enregistrent pas

1. **PostHog Dashboard** → Settings → Project → Recordings
2. Vérifiez que **"Record user sessions"** est activé
3. Effacez le cache et attendez 1-2 minutes (ingestion delay)

### Événements manquants

PostHog a un délai d'ingestion de ~30 secondes à 2 minutes. Si après 5 minutes rien n'apparaît :
- Vérifiez la console (erreurs réseau ?)
- Testez en navigation privée (extensions browser ?)

## ✅ Checklist de setup

- [x] PostHog installé et configuré
- [x] Variables d'environnement ajoutées à `.env.local`
- [x] Session replay activé avec masking
- [ ] Créer le funnel "Landing Complet (20 étapes)" dans PostHog
- [ ] Créer les funnels complémentaires (Discovery, Setup, Micro-conversion)
- [ ] Ajouter variables d'environnement à Vercel (staging + production)
- [ ] Redéployer staging et production
- [ ] Tester : Compléter le tunnel landing et vérifier les événements dans PostHog
- [ ] Analyser les premiers drop-offs avec session replay

## 📚 Ressources

- **Votre dashboard** : https://app.posthog.com/project/107396
- **Session replays** : https://app.posthog.com/project/107396/replay/recent
- **Funnels** : https://app.posthog.com/project/107396/insights
- **Documentation** : https://posthog.com/docs/libraries/next-js

---

**Prochaine étape** : Créer le funnel "Landing Complet (20 étapes)" dans PostHog Dashboard ! 🚀
