# ARCHITECTURE SMART SUBTITLES

**Date:** January 30, 2025
**Status:** Phase 2B - Migration vers Next.js en cours

---

## 🎯 Vue d'ensemble

Smart Subtitles est une plateforme d'apprentissage de langues qui adapte les sous-titres Netflix selon le niveau de vocabulaire de l'utilisateur.

**4 composants principaux :**
1. **Chrome Extension** - Injection de sous-titres sur Netflix
2. **Next.js Webapp** - Onboarding, auth, billing, gestion compte
3. **FastAPI Backend** - Traitement algorithmique des sous-titres
4. **Supabase** - Base de données et authentification

---

## 📊 Architecture Système (APRÈS migration Next.js)

```
┌─────────────────────────────────────────────────────────────────┐
│                          UTILISATEUR                             │
│  - Regarde Netflix avec extension Chrome                         │
│  - Configure compte sur webapp                                   │
│  - Gère abonnement via Stripe                                    │
└─────────────────────────────────────────────────────────────────┘
                                 ↓ ↑
        ┌────────────────────────┴─────────────────────────┐
        ↓                                                   ↓
┌──────────────────────┐                    ┌──────────────────────────┐
│  CHROME EXTENSION    │                    │   NEXT.JS WEBAPP         │
│  (Netflix Page)      │                    │   (Vercel)               │
│                      │                    │                          │
│  ┌─────────────────┐│                    │  FRONTEND                │
│  │ Content Script  ││                    │  ├─ /welcome             │
│  │ Page Script     ││                    │  ├─ /onboarding/*        │
│  │ Popup UI        ││                    │  ├─ /subscribe           │
│  └─────────────────┘│                    │  └─ /welcome-back        │
│                      │                    │                          │
│  Fonctions:          │                    │  BACKEND (API Routes)    │
│  • Intercepte        │                    │  ├─ /api/stripe/checkout │
│    Netflix API       │                    │  ├─ /api/stripe/portal   │
│  • Injecte           │                    │  └─ /api/stripe/webhook  │
│    sous-titres       │                    │                          │
│  • Vérifie           │                    │  Fonctions:              │
│    abonnement        │                    │  • Google OAuth          │
│                      │                    │  • Gestion billing       │
│                      │◄───Message Passing─┤  • Sync settings         │
└──────────────────────┘                    └──────────────────────────┘
         ↓                                              ↓
         │                                              │
         │                                              │
         ↓                                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                          SUPABASE                                 │
│  (Base de données PostgreSQL + Auth)                             │
│                                                                   │
│  Tables:                                                          │
│  ├─ auth.users              (Utilisateurs Google OAuth)          │
│  ├─ user_settings           (Langue cible, native)               │
│  ├─ vocab_levels            (Niveau vocabulaire par langue)      │
│  ├─ subscriptions           (Statut abonnement Stripe)           │
│  └─ known_words             (Mots connus - Phase 3)              │
│                                                                   │
│  RLS Policies: Chaque user voit UNIQUEMENT ses données           │
└──────────────────────────────────────────────────────────────────┘
         ↑                                              ↑
         │                                              │
         └────────────────┬─────────────────────────────┘
                          ↓
         ┌──────────────────────────────┐
         │   FASTAPI BACKEND            │
         │   (Railway)                  │
         │                              │
         │   Endpoint:                  │
         │   POST /fuse-subtitles       │
         │                              │
         │   Fonctions:                 │
         │   • Fusion sous-titres       │
         │   • Sélection vocabulaire    │
         │   • Traduction inline        │
         │   • Lemmatisation            │
         └──────────────────────────────┘
                          ↑
                          │
                          ↓
         ┌──────────────────────────────┐
         │   SERVICES EXTERNES          │
         │                              │
         │   • Stripe (Paiements)       │
         │   • OpenAI (Traductions)     │
         │   • DeepL (Traductions)      │
         └──────────────────────────────┘
```

---

## 🔄 Flux de données principaux

### 1. Flux d'Onboarding (Nouveau utilisateur)

```
Utilisateur
   │
   └─► Next.js Webapp /welcome
          │ (Clique "Sign in with Google")
          │
          └─► Supabase Auth (Google OAuth)
                 │
                 ├─► Crée user dans auth.users
                 │
                 └─► Redirect /onboarding/languages
                        │
                        ├─► Sélectionne langues
                        ├─► Passe vocab test
                        ├─► Sauvegarde dans Supabase
                        │   (user_settings + vocab_levels)
                        │
                        └─► /onboarding/pricing
                               │
                               └─► Checkout Stripe (trial 14j)
                                      │
                                      └─► Webhook → Supabase subscriptions
                                             │
                                             └─► Onboarding complet ✅
```

---

### 2. Flux de Traitement Sous-titres (Sur Netflix)

```
Utilisateur sur Netflix (épisode chargé)
   │
   └─► Extension: Page Script intercepte JSON.parse()
          │
          ├─► Capture réponse API Netflix
          │   (timedtexttracks - sous-titres)
          │
          └─► Content Script reçoit données
                 │
                 ├─► Vérifie abonnement (chrome.storage.local)
                 │   • Si non abonné → Ouvre /subscribe
                 │   • Si abonné → Continue
                 │
                 ├─► Utilisateur clique "Process Subtitles" dans popup
                 │
                 └─► Envoie à FastAPI backend:
                        │  - Sous-titres langue cible (PT/FR)
                        │  - Sous-titres langue native (EN/etc)
                        │  - Niveau vocabulaire utilisateur
                        │
                        └─► FastAPI /fuse-subtitles
                               │
                               ├─► Algorithme fusion:
                               │   • Mot connu → Garde langue cible
                               │   • Mot inconnu → Traduction inline OU native
                               │   • Lemmatisation, alignement temporel
                               │
                               └─► Retourne sous-titres fusionnés (SRT)
                                      │
                                      └─► Extension injecte dans Netflix
                                             │
                                             └─► Utilisateur voit sous-titres adaptés ✅
```

---

### 3. Flux de Gestion Abonnement

```
Utilisateur clique "Manage Subscription"
   │
   └─► Next.js Webapp (bouton sur /complete ou /welcome-back)
          │
          └─► POST /api/stripe/portal
                 │
                 ├─► Next.js backend crée session Stripe Portal
                 │   (avec customer_id depuis Supabase)
                 │
                 └─► Redirect vers Stripe Customer Portal
                        │
                        ├─► Utilisateur annule/modifie
                        │
                        └─► Stripe envoie webhook
                               │
                               └─► POST /api/stripe/webhook
                                      │
                                      ├─► Vérifie signature webhook
                                      ├─► Met à jour Supabase subscriptions
                                      │   (status, current_period_end, etc.)
                                      │
                                      └─► Extension sync automatique
                                             │
                                             └─► Bloque traitement si expiré ✅
```

---

## 🔐 Flux d'Authentification (Webapp ↔ Extension)

```
Webapp (Next.js)
   │
   ├─► Supabase Auth: Google OAuth
   │      │
   │      └─► Obtient access_token + refresh_token
   │             │
   │             └─► Stocke dans localStorage (webapp)
   │                    │
   │                    └─► Message Passing vers Extension
   │                           │
   │                           │  chrome.runtime.sendMessage(
   │                           │    extensionId,
   │                           │    { access_token, refresh_token }
   │                           │  )
   │                           │
   │                           ↓
Extension (Chrome)
   │
   └─► chrome.runtime.onMessageExternal
          │
          ├─► Valide sender.origin (sécurité)
          │
          ├─► Appelle supabase.auth.setSession(tokens)
          │
          └─► Stocke dans chrome.storage.local
                 │
                 └─► Extension maintenant authentifiée ✅
```

**Pourquoi Message Passing ?**
- Webapp et Extension = 2 domaines différents (https://webapp vs chrome-extension://)
- Sessions localStorage pas partagées
- Solution standard pour Firebase, Auth0, Supabase extensions

---

## 🏗️ Composants détaillés

### Next.js Webapp (Vercel)

**Rôle :** Interface utilisateur + Backend billing

**Structure :**
```
webapp-next/
  app/
    layout.tsx              # Layout racine
    welcome/page.tsx        # Google OAuth entry
    onboarding/
      languages/page.tsx    # Sélection langues
      vocab-test/page.tsx   # Test vocabulaire
      results/page.tsx      # Résultats niveau
      pricing/page.tsx      # Offre trial 14j
      pin-extension/page.tsx
      complete/page.tsx
    subscribe/page.tsx      # Abonnement expiré
    welcome-back/page.tsx   # Returning users
    api/
      stripe/
        checkout/route.ts   # POST - Crée session Stripe
        portal/route.ts     # POST - Ouvre portal client
        webhook/route.ts    # POST - Reçoit events Stripe
  components/
    PricingCard.tsx
    ManageSubscriptionButton.tsx
  lib/
    supabase.ts             # Client Supabase
```

**Technologies :**
- React 19
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Shadcn UI
- Supabase client

**Déploiement :**
- Staging: `staging-subly-extension.vercel.app`
- Production: `subly-extension.vercel.app`

---

### Chrome Extension

**Rôle :** Injection sous-titres sur Netflix

**Architecture 3-scripts :**
1. **Page Script** - Intercepte Netflix API (JSON.parse hijacking)
2. **Content Script** - Coordonne messages, injecte sous-titres
3. **Popup** - UI settings (langues, niveau vocab)

**Technologies :**
- TypeScript
- Webpack
- Chrome Extension Manifest V3
- Supabase client

**Builds :**
- Staging: `npm run build:staging` → pointe vers staging API
- Production: `npm run build:production` → pointe vers production API

---

### FastAPI Backend (Railway)

**Rôle :** Algorithme traitement sous-titres

**Endpoint principal :**
- `POST /fuse-subtitles`
  - Input: SRT langue cible + SRT langue native + niveau vocab
  - Output: SRT fusionné adapté au niveau

**Algorithme :**
1. Parse SRT (langue cible + native)
2. Lemmatisation mots (simplemma)
3. Vérification fréquence (word frequency lists)
4. Décision par mot :
   - Connu → Garde langue cible
   - Inconnu → Traduction inline (OpenAI/DeepL) OU remplacement natif
5. Alignement temporel bidirectionnel
6. Export SRT final

**Technologies :**
- Python 3.11
- FastAPI
- simplemma (lemmatisation)
- OpenAI API (traductions)
- DeepL API (traductions fallback)

**Déploiement :**
- Railway (auto-deploy depuis GitHub `develop`/`main`)

---

### Supabase

**Rôle :** Base de données + Auth

**Tables principales :**

1. **auth.users** (géré par Supabase)
   - Google OAuth users
   - UUID, email, metadata

2. **user_settings**
   - Préférences utilisateur
   - Langue cible, langue native

3. **vocab_levels**
   - Niveau vocabulaire par langue
   - Multi-langue support (PT, FR, etc.)

4. **subscriptions**
   - Statut abonnement Stripe
   - customer_id, subscription_id, status, current_period_end

5. **known_words** (Phase 3)
   - Mots marqués connus/inconnus par utilisateur
   - Accès direct depuis webapp/extension (RLS)

**Sécurité :**
- Row Level Security (RLS) sur toutes les tables
- Policies : `auth.uid() = user_id`
- Chaque user voit UNIQUEMENT ses données

---

## 🔒 Sécurité

### Principes clés

**1. Secrets jamais exposés côté client :**
- ✅ Stripe Secret Key → Next.js API routes (backend)
- ✅ Webhook Secret → Next.js API routes
- ❌ JAMAIS dans extension ou webapp frontend

**2. Stripe Publishable Key (OK côté client) :**
- Utilisé pour redirection Checkout
- Pas de risque sécurité

**3. Supabase Anon Key (OK côté client) :**
- Protégé par RLS policies
- Aucune requête possible sans auth + RLS validation

**4. Webhook signature verification :**
- TOUJOURS vérifier signature Stripe
- Évite requêtes frauduleuses

**5. HTTPS obligatoire :**
- Vercel force HTTPS
- Railway force HTTPS
- Pas de données sensibles en HTTP

---

## 📈 Scalabilité

### Architecture actuelle (Monolithe modulaire)

**Avantages :**
- Simple à déployer
- Une seule codebase (Next.js)
- Pas de complexité microservices

**Limites (théoriques, pas actuelles) :**
- Scaling horizontal si traffic énorme
- Couplage frontend-backend billing

### Migration future possible

**Si vraiment nécessaire (>10k users actifs) :**
```
Next.js Webapp
   ↓
Split en:
   ├─ Next.js Frontend (pages)
   ├─ Node.js Billing Service (API Stripe)
   └─ Admin Dashboard (séparé)
```

**Mais YAGNI (You Aren't Gonna Need It) :**
- Next.js scale jusqu'à millions de users
- Vercel serverless auto-scale
- FastAPI déjà séparé (subtitle processing)
- **Pas besoin de microservices maintenant**

---

## 🎯 Pourquoi cette architecture ?

### Next.js Monolith

**Avantages :**
- ✅ Frontend + Backend billing dans 1 codebase
- ✅ Pas de CORS entre webapp et API
- ✅ Auth simple (même domaine)
- ✅ Hot reload frontend + backend
- ✅ Pattern standard SaaS 2025
- ✅ Scalable jusqu'à millions users

**Alternative rejetée (FastAPI billing) :**
- ❌ 2 backends = complexité x2
- ❌ CORS configuration
- ❌ Auth sharing compliqué
- ❌ Déploiements x2

### FastAPI externe (subtitle processing)

**Pourquoi séparé ?**
- ✅ Algorithme Python déjà écrit/testé
- ✅ Pas besoin de réécrire en TypeScript
- ✅ Peut scale indépendamment si besoin
- ✅ Next.js l'appelle comme API externe (simple)

**Futur possible :**
- Migrer en Next.js API route (optionnel)
- Ou garder séparé (fonctionne bien)

### Supabase (vs backend custom)

**Avantages :**
- ✅ PostgreSQL managed
- ✅ Auth Google OAuth intégré
- ✅ RLS policies = sécurité automatique
- ✅ Real-time si besoin (Phase 4)
- ✅ Pas de serveur DB à maintenir

**Alternative rejetée (backend custom) :**
- ❌ Gérer PostgreSQL soi-même
- ❌ Écrire logique auth manuellement
- ❌ Sécurité plus risquée
- ❌ Maintenance overhead

---

## 📝 Décisions architecturales clés

### 1. Webapp externe vs Extension pages
- **Choix :** Webapp externe (Next.js sur Vercel)
- **Raison :** Multi-device sync, auth backend, billing management
- **Pattern :** Language Reactor, Grammarly, Loom

### 2. Next.js vs Vite
- **Choix :** Next.js (migration Phase 2B)
- **Raison :** Backend intégré pour Stripe, pattern SaaS standard
- **Consensus :** ChatGPT + Claude + Senior Dev

### 3. Monolith vs Microservices
- **Choix :** Monolith modulaire (Next.js)
- **Raison :** KISS principe, scalable suffisamment, pas de complexité prématurée
- **Future :** Split si vraiment nécessaire (>10k users)

### 4. Supabase RLS vs Backend custom (known_words)
- **Choix :** Supabase RLS (Phase 3)
- **Raison :** CRUD simple, sécurité DB-level, pas besoin backend
- **Pattern :** Standard pour apps multi-tenant

---

## 🚀 Architecture finale cible

```
┌──────────────────────────────────────────────────────┐
│             UTILISATEUR FINAL                         │
│  - Extension Chrome sur Netflix                       │
│  - Webapp pour onboarding/billing                     │
└──────────────────────────────────────────────────────┘
                         ↓ ↑
        ┌────────────────┴────────────────┐
        ↓                                  ↓
┌─────────────────┐          ┌────────────────────────┐
│ Chrome Extension│          │   Next.js Monolith     │
│   (Netflix UI)  │◄────────►│   (Vercel)             │
└─────────────────┘  Sync    │   • Pages (frontend)   │
        ↓                     │   • API routes (backend)│
        │                     └────────────────────────┘
        │                                  ↓ ↑
        │                     ┌────────────┴────────────┐
        │                     ↓                         ↓
        ↓              ┌──────────────┐      ┌──────────────┐
┌──────────────┐      │   Supabase   │      │    Stripe    │
│ FastAPI      │      │   (DB+Auth)  │      │  (Payments)  │
│ (Subtitles)  │      └──────────────┘      └──────────────┘
└──────────────┘

Simple, scalable, maintenable. ✅
```

---

**Dernière mise à jour :** January 30, 2025
**Prochaine révision :** Après Phase 2B (migration Next.js complète)
