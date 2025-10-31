# MIGRATION NEXT.JS - PLAN D'ACTION

**Date de création :** 31 octobre 2025
**Statut :** Phase 2B - Migration technique Vite → Next.js 15
**Objectif :** Migrer webapp de Vite vers Next.js pour intégrer backend Stripe

---

## 🎯 Contexte et objectif

### Pourquoi migrer vers Next.js ?
- **Besoin backend** pour Stripe (checkout, webhooks, portal)
- **Next.js = Frontend + Backend** dans même codebase (pas 2 backends séparés)
- **Pattern standard** SaaS 2025 (recommandé par Stripe)
- **Future-proof** pour analytics, admin dashboard

### Ce qui NE CHANGE PAS
- ✅ Supabase schema (tables, RLS) - **0 modification**
- ✅ Chrome extension (TypeScript, popup) - **0 modification pendant migration**
- ✅ FastAPI backend (subtitle processing) - **0 modification**

### Ce qui change
- Structure fichiers : `webapp/src/pages/` → `webapp-next/app/`
- Auth Supabase : package `@supabase/ssr` + 2 clients (browser/server)
- Routing : React Router → File-based routing Next.js
- Env vars : `VITE_*` → `NEXT_PUBLIC_*`

---

## ⏱️ Durée estimée

**Total : 12-16 heures (2 jours)**
- **Jour 1** : Setup + Migration Frontend (8-10h)
- **Jour 2** : Stripe Integration (4-6h)

---

## ✅ PRÉ-REQUIS (AVANT DE COMMENCER)

- [x] **Backup Supabase** (Dashboard → Database → Backups → Create) - **SKIPPED** (pas nécessaire, 0 changement DB)
- [x] **Git commit clean state** (`git status` doit être propre)
- [x] **Noter les env vars actuelles** (copier `.env.local` de webapp/)
- [x] **2 comptes Google test** disponibles pour tester RLS
- [x] **Stripe test keys** notées (de la session précédente)

**🚨 IMPORTANT : Ne pas commencer sans avoir fait le backup Supabase !**

---

## 📅 JOUR 1 - SETUP & MIGRATION FRONTEND (8-10h)

---

### ⚡ Phase 1 : Initialisation Next.js (1h) ✅ **COMPLÉTÉ**

**Objectif :** Créer projet Next.js 15 avec App Router

- [x] Créer nouveau projet Next.js dans `webapp-next/`
- [x] Sélectionner : TypeScript + Tailwind CSS + App Router + src/ directory
- [x] Vérifier que le projet compile et démarre
- [x] Configurer `.gitignore` (node_modules, .next, .env.local)

**✅ TEST INTERMÉDIAIRE #1 (2 min)** ✅ **RÉUSSI**
- [x] `npm run dev` fonctionne
- [x] Page http://localhost:3000 s'affiche
- [x] Pas d'erreurs dans la console

---

### 🎨 Phase 2 : Setup Shadcn UI (30 min) ✅ **COMPLÉTÉ**

**Objectif :** Installer et configurer Shadcn UI + composants

- [x] Initialiser Shadcn UI dans le projet
- [x] Installer composants utilisés : Button, Card, Select, RadioGroup, Label, Alert
- [x] Vérifier que `components/ui/` est créé avec les bons fichiers
- [x] Copier le fichier `globals.css` de l'ancien projet (si styles custom) - **Pas nécessaire** (Tailwind v4 déjà configuré)

**✅ TEST INTERMÉDIAIRE #2 (2 min)** ✅ **RÉUSSI**
- [x] `components/ui/button.tsx` existe
- [x] Projet compile toujours (`npm run dev`)
- [x] Pas d'erreurs TypeScript

---

### 🔐 Phase 3 : Configuration Supabase (1-2h) ✅ **COMPLÉTÉ**

**Objectif :** Setup auth Supabase avec pattern Next.js (cookies)

- [x] Installer package `@supabase/ssr` (remplace `@supabase/supabase-js`)
- [x] Créer fichier `lib/supabase/client.ts` (browser client)
- [x] Créer fichier `lib/supabase/server.ts` (server client)
- [x] Créer fichier `middleware.ts` (session refresh)
- [x] Copier les env vars : `NEXT_PUBLIC_SUPABASE_URL` et `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [x] Créer fichier `.env.local` avec les variables

**✅ TEST INTERMÉDIAIRE #3 (5 min)** ✅ **RÉUSSI**
- [x] Importer `createClient()` dans une page test
- [x] Appeler `supabase.from('user_settings').select('*')` dans une page
- [x] Vérifier dans les logs que la connexion Supabase fonctionne (même si erreur auth, c'est OK)
- [ ] Pas d'erreur "Invalid Supabase URL"

---

### 🧩 Phase 4 : Migration Composants (2-3h) ✅ **COMPLÉTÉ**

**Objectif :** Copier composants React de Vite vers Next.js

- [x] Créer dossier `components/` dans webapp-next/
- [x] Copier `PricingCard.tsx` depuis webapp/src/components/
- [x] Copier `ManageSubscriptionButton.tsx`
- [x] Copier tous les autres composants custom (hors Shadcn UI) - `utils/mockups.ts` copié
- [x] Ajouter `'use client'` en haut des composants qui utilisent :
  - `useState`, `useEffect`, `useContext`
  - Event handlers (`onClick`, `onChange`, etc.)
  - Browser APIs (`window`, `localStorage`, etc.)
- [x] Fixer les imports : `@/components/ui/button` → vérifier que ça marche
- [x] Supprimer imports inutiles (React Router, etc.)

**✅ TEST INTERMÉDIAIRE #4 (5 min)** ✅ **RÉUSSI**
- [x] Tous les fichiers compilent (`npm run build`)
- [x] Pas d'erreurs TypeScript dans les composants (erreur chrome résolue avec @types/chrome)
- [x] Pas d'erreur "You're importing a component that needs useState..."

**💡 ASTUCE :** Si erreur "useState", ajouter `'use client'` en première ligne du fichier

---

### 📄 Phase 5 : Migration Pages - Partie 1 (2h) ✅ **COMPLÉTÉ (9/9 pages)**

**Objectif :** Migrer les pages d'onboarding (approche incrémentale)

**Étape 5.1 : Page Welcome** ✅ **COMPLÉTÉ**
- [x] Créer `app/welcome/page.tsx`
- [x] Copier le code de `webapp/src/pages/Welcome.tsx`
- [x] Ajouter `'use client'` en haut du fichier
- [x] Fixer imports Supabase (`lib/supabase/client` au lieu de l'ancien)
- [x] Remplacer `useNavigate()` par `useRouter()` de `next/navigation`

**✅ TEST INTERMÉDIAIRE #5 (3 min)** ✅ **RÉUSSI**
- [x] Page `/welcome` s'affiche dans le browser
- [x] Bouton "Create account" visible
- [x] Pas d'erreurs console (404 image mineure non-bloquante)

**Étape 5.2 : Pages Onboarding** ✅ **COMPLÉTÉ**
- [x] Créer `app/onboarding/languages/page.tsx`
- [x] Créer `app/onboarding/vocab-test/page.tsx`
- [x] Créer `app/onboarding/results/page.tsx`
- [x] Créer `app/onboarding/pricing/page.tsx`
- [x] Créer `app/onboarding/pin-extension/page.tsx`
- [x] Créer `app/onboarding/complete/page.tsx`
- [x] Pour chaque page : copier code + ajouter `'use client'` + fixer imports

**✅ TEST INTERMÉDIAIRE #6 (5 min)** ✅ **RÉUSSI**
- [x] Naviguer manuellement vers chaque URL (`/onboarding/languages`, etc.)
- [x] Vérifier que toutes les pages s'affichent - Build réussi avec 11 routes
- [x] Pas d'erreurs 404 ou compilation - TypeScript OK

**Étape 5.3 : Autres pages** ✅ **COMPLÉTÉ**
- [x] Créer `app/subscribe/page.tsx`
- [x] Créer `app/welcome-back/page.tsx`
- [x] Copier code + fixer imports

**✅ TEST INTERMÉDIAIRE #7 (2 min)** ✅ **RÉUSSI**
- [x] Pages `/subscribe` et `/welcome-back` s'affichent
- [x] Projet compile toujours - Build production réussi

---

### 🔗 Phase 6 : Configuration Auth Context (1h) ✅ **COMPLÉTÉ**

**Objectif :** Migrer AuthContext pour gérer session utilisateur

- [x] Créer `contexts/AuthContext.tsx` (si pas déjà fait)
- [x] Copier logique d'auth depuis Vite (Google OAuth)
- [x] Utiliser le client Supabase browser (`lib/supabase/client`)
- [x] Ajouter `'use client'` en haut du fichier
- [x] Wrapper `<AuthProvider>` dans `app/layout.tsx` via `ClientProviders`
- [x] Installer sonner pour toasts
- [x] Créer `lib/syncExtension.ts` pour sync Chrome extension
- [x] Créer `components/ClientProviders.tsx` wrapper

**✅ TEST INTERMÉDIAIRE #8 (3 min)** ✅ **RÉUSSI**
- [x] Vérifier que `useAuth()` est accessible depuis n'importe quelle page
- [x] Pas d'erreur "useAuth must be used within AuthProvider"
- [x] Build réussit après installation de @types/chrome

---

### 🧪 Phase 7 : Tests Auth End-to-End (1-2h)

**Objectif :** Valider que le flow d'authentification complet fonctionne

**Test 7.1 : Google OAuth**
- [ ] Aller sur `/welcome`
- [ ] Cliquer "Create account with Google"
- [ ] Compléter OAuth dans popup
- [ ] Vérifier redirect vers `/onboarding/languages`
- [ ] Vérifier dans console : `user` object existe

**✅ RÉSULTAT ATTENDU :** User créé dans Supabase `auth.users`, redirect fonctionne

**Test 7.2 : Onboarding complet**
- [ ] Compléter `/onboarding/languages` (sélectionner PT-BR + French)
- [ ] Compléter `/onboarding/vocab-test` (sélectionner 2000 words)
- [ ] Vérifier que `/onboarding/results` affiche "2000 words"
- [ ] Continuer vers `/onboarding/pricing`
- [ ] Vérifier que pricing card s'affiche (mockup OK pour l'instant)
- [ ] Continuer jusqu'à `/onboarding/complete`

**✅ RÉSULTAT ATTENDU :**
- [ ] Données sauvegardées dans Supabase (`user_settings` + `vocab_levels`)
- [ ] Vérifier dans Supabase Dashboard → Table Editor

**Test 7.3 : Session persistence**
- [ ] Rafraîchir la page (F5) sur `/onboarding/complete`
- [ ] Vérifier que user reste connecté (pas de redirect vers `/welcome`)

**✅ RÉSULTAT ATTENDU :** Session persiste (cookies HTTP-only fonctionnent)

**Test 7.4 : RLS Isolation (avec 2 comptes)**
- [ ] User A : Compléter onboarding → PT-BR 2000
- [ ] User B : Compléter onboarding → PT-BR 1000
- [ ] User A : Vérifier qu'il ne voit QUE ses données (2000, pas 1000)
- [ ] Vérifier dans Supabase Dashboard : 2 lignes distinctes dans `vocab_levels`

**✅ RÉSULTAT ATTENDU :** Chaque user voit uniquement ses propres données

**🎉 FIN JOUR 1 - Frontend migration complète et testée**

---

## 📅 JOUR 2 - STRIPE INTEGRATION (4-6h)

---

### 💳 Phase 8 : API Routes Stripe (3-4h)

**Objectif :** Créer 3 endpoints backend pour Stripe

**Étape 8.1 : Route Checkout**
- [ ] Créer fichier `app/api/stripe/checkout/route.ts`
- [ ] Installer package `stripe` via npm
- [ ] Implémenter `POST` handler : créer session Stripe avec trial 14 jours
- [ ] Récupérer `userId` depuis body, créer customer + subscription
- [ ] Retourner `{ url: session.url }` pour redirect

**✅ TEST INTERMÉDIAIRE #9 (5 min)**
- [ ] Tester avec cURL ou Postman :
  ```bash
  curl -X POST http://localhost:3000/api/stripe/checkout \
    -H "Content-Type: application/json" \
    -d '{"userId":"test-uuid","email":"test@test.com"}'
  ```
- [ ] Vérifier réponse JSON avec `url` Stripe
- [ ] Pas d'erreur 500

**Étape 8.2 : Route Portal**
- [ ] Créer fichier `app/api/stripe/portal/route.ts`
- [ ] Implémenter `POST` handler : créer session portal
- [ ] Récupérer `customer_id` depuis Supabase `subscriptions` table
- [ ] Retourner `{ url: portalSession.url }`

**✅ TEST INTERMÉDIAIRE #10 (5 min)**
- [ ] Tester avec cURL (similaire à checkout)
- [ ] Vérifier que l'URL portal Stripe est retournée

**Étape 8.3 : Route Webhook**
- [ ] Créer fichier `app/api/stripe/webhook/route.ts`
- [ ] Vérifier signature webhook avec `STRIPE_WEBHOOK_SECRET`
- [ ] Gérer 3 events :
  - `checkout.session.completed` → INSERT dans `subscriptions`
  - `customer.subscription.updated` → UPDATE `status`
  - `customer.subscription.deleted` → UPDATE `status = 'canceled'`
- [ ] Utiliser Supabase server client (`lib/supabase/server`)

**✅ TEST INTERMÉDIAIRE #11 (10 min avec Stripe CLI)**
- [ ] Installer Stripe CLI (`brew install stripe/stripe-cli/stripe`)
- [ ] `stripe login`
- [ ] `stripe listen --forward-to localhost:3000/api/stripe/webhook`
- [ ] `stripe trigger checkout.session.completed`
- [ ] Vérifier logs : webhook reçu + ligne créée dans Supabase `subscriptions`

---

### 🎨 Phase 9 : Frontend Billing (1h)

**Objectif :** Remplacer mockups par vraies API calls

**Étape 9.1 : PricingCard**
- [ ] Ouvrir `components/PricingCard.tsx`
- [ ] Remplacer `simulateStripeCheckout()` par appel à `/api/stripe/checkout`
- [ ] Utiliser `fetch()` pour POST, récupérer `url`, faire `window.location.href = url`

**Étape 9.2 : ManageSubscriptionButton**
- [ ] Ouvrir `components/ManageSubscriptionButton.tsx`
- [ ] Remplacer `simulateStripePortal()` par appel à `/api/stripe/portal`
- [ ] Ouvrir URL dans nouvel onglet (`window.open(url, '_blank')`)

**✅ TEST INTERMÉDIAIRE #12 (10 min)**
- [ ] Sur `/onboarding/pricing`, cliquer "Start Free Trial"
- [ ] Vérifier redirect vers Stripe Checkout (vrai formulaire Stripe)
- [ ] Utiliser carte test `4242 4242 4242 4242` + date future + n'importe quel CVC
- [ ] Compléter paiement
- [ ] Vérifier redirect vers `/onboarding/pin-extension` (success_url)

**✅ RÉSULTAT ATTENDU :**
- [ ] Ligne créée dans Supabase `subscriptions` (status = 'trialing')
- [ ] Webhook reçu et traité

---

### 🔌 Phase 10 : Extension Update (1h)

**Objectif :** Faire pointer l'extension vers Next.js au lieu de Vite

**Étape 10.1 : URLs**
- [ ] Ouvrir `extension/src/background.ts`
- [ ] Changer `WEBAPP_URL` : `http://localhost:3000` (port Next.js)
- [ ] Ouvrir `extension/manifest.json`
- [ ] Modifier `externally_connectable.matches` :
  ```json
  "matches": [
    "http://localhost:3000/*",
    "https://staging-subly-extension.vercel.app/*",
    "https://subly-extension.vercel.app/*"
  ]
  ```

**Étape 10.2 : Rebuild**
- [ ] Dans `extension/` : `npm run build:staging`
- [ ] Recharger extension dans Chrome (Extensions → Reload)

**✅ TEST INTERMÉDIAIRE #13 (5 min)**
- [ ] Ouvrir extension popup
- [ ] Cliquer bouton qui devrait ouvrir webapp
- [ ] Vérifier que Next.js webapp s'ouvre (localhost:3000)
- [ ] Pas d'erreur "externally_connectable" dans console

**Étape 10.3 : Message Passing**
- [ ] Compléter onboarding dans webapp Next.js
- [ ] Vérifier que tokens sont envoyés à extension (console logs)
- [ ] Ouvrir extension popup
- [ ] Vérifier que settings sont affichés (target_lang, vocab_level)

**✅ TEST INTERMÉDIAIRE #14 (5 min)**
- [ ] Extension lit user_settings depuis Supabase
- [ ] Vocab level affiché = celui du test onboarding
- [ ] Pas d'erreur "user not authenticated"

---

### 🎯 Phase 11 : Tests End-to-End Complets (1h)

**Objectif :** Valider le flow complet avec Stripe + Extension

**Test E2E #1 : Signup → Trial → Extension**
- [ ] User : Créer nouveau compte Google (ou utiliser incognito)
- [ ] Compléter onboarding complet jusqu'à checkout Stripe
- [ ] Payer avec carte test, vérifier redirect
- [ ] Ouvrir extension popup
- [ ] Vérifier que settings sont bien synchronisés

**Test E2E #2 : Manage Subscription**
- [ ] Cliquer "Manage Subscription" dans webapp
- [ ] Vérifier que Stripe Portal s'ouvre
- [ ] Simuler annulation (ou juste consulter)
- [ ] Vérifier que webhook est reçu (si annulation testée)

**Test E2E #3 : RLS + Multi-device**
- [ ] User A : Se connecter sur Chrome
- [ ] User B : Se connecter sur Chrome incognito
- [ ] Vérifier que chaque user voit UNIQUEMENT ses données

**✅ RÉSULTATS ATTENDUS :**
- [ ] Aucune erreur durant les 3 flows
- [ ] Données correctement isolées (RLS)
- [ ] Webhooks Stripe reçus et traités
- [ ] Extension synchronisée avec webapp

**🎉 FIN JOUR 2 - Stripe intégration complète**

---

## 🧹 NETTOYAGE POST-MIGRATION (30 min)

**Objectif :** Supprimer Vite une fois Next.js validé en production

**🚨 ATTENTION : Faire ces étapes SEULEMENT après déploiement production Next.js réussi**

- [ ] Tester staging Next.js pendant 24-48h (pas de bugs critiques)
- [ ] Déployer Next.js en production (`git push origin main`)
- [ ] Vérifier que production fonctionne (auth, billing, extension)
- [ ] **BACKUP webapp/ Vite** (zip ou git tag) avant suppression
- [ ] Supprimer dossier `webapp/` (ancien Vite)
- [ ] Renommer `webapp-next/` → `webapp/` (optionnel)
- [ ] Mettre à jour `.gitignore` si nécessaire
- [ ] Commit : `git commit -m "chore: Remove old Vite webapp after Next.js migration"`

---

## 🚨 TROUBLESHOOTING - Problèmes fréquents

### Erreur : "You're importing a component that needs useState"
**Solution :** Ajouter `'use client'` en première ligne du fichier

### Erreur : "Invalid Supabase URL"
**Solution :** Vérifier `.env.local`, variable doit commencer par `NEXT_PUBLIC_`

### Erreur : Auth redirect ne fonctionne pas
**Solution :** Vérifier Supabase Dashboard → Auth → URL Configuration
- Ajouter `http://localhost:3000/*` dans redirect URLs

### Erreur : Extension ne reçoit pas les tokens
**Solution :** Vérifier `manifest.json` `externally_connectable` contient `localhost:3000`

### Erreur : Stripe webhook non reçu
**Solution :** Utiliser Stripe CLI en local (`stripe listen --forward-to ...`)

---

## 📝 CODE REFERENCE

### 1. Supabase Client (Browser)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### 2. Supabase Client (Server)

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options })
        },
      },
    }
  )
}
```

### 3. Middleware (Session Refresh)

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  await supabase.auth.getUser()

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### 4. Stripe Checkout API Route

```typescript
// app/api/stripe/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
})

export async function POST(req: NextRequest) {
  try {
    const { userId, email } = await req.json()

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      customer_email: email,
      line_items: [
        {
          price: process.env.STRIPE_PRICE_ID, // $1/month
          quantity: 1,
        },
      ],
      subscription_data: {
        trial_period_days: 14,
        metadata: { user_id: userId },
      },
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pin-extension`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pricing`,
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('Stripe checkout error:', error)
    return NextResponse.json(
      { error: 'Failed to create checkout session' },
      { status: 500 }
    )
  }
}
```

### 5. Stripe Portal API Route

```typescript
// app/api/stripe/portal/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createClient } from '@/lib/supabase/server'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
})

export async function POST(req: NextRequest) {
  try {
    const { userId } = await req.json()
    const supabase = createClient()

    // Get customer ID from Supabase
    const { data: subscription, error } = await supabase
      .from('subscriptions')
      .select('stripe_customer_id')
      .eq('user_id', userId)
      .single()

    if (error || !subscription) {
      return NextResponse.json(
        { error: 'No subscription found' },
        { status: 404 }
      )
    }

    // Create portal session
    const session = await stripe.billingPortal.sessions.create({
      customer: subscription.stripe_customer_id,
      return_url: `${process.env.NEXT_PUBLIC_APP_URL}/welcome-back`,
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('Stripe portal error:', error)
    return NextResponse.json(
      { error: 'Failed to create portal session' },
      { status: 500 }
    )
  }
}
```

### 6. Stripe Webhook Handler

```typescript
// app/api/stripe/webhook/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createClient } from '@/lib/supabase/server'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
})

export async function POST(req: NextRequest) {
  const body = await req.text()
  const signature = req.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    )
  }

  const supabase = createClient()

  // Handle events
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      const userId = session.metadata?.user_id

      if (userId) {
        await supabase.from('subscriptions').insert({
          user_id: userId,
          stripe_customer_id: session.customer as string,
          stripe_subscription_id: session.subscription as string,
          status: 'trialing',
        })
      }
      break
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription

      await supabase
        .from('subscriptions')
        .update({ status: subscription.status })
        .eq('stripe_subscription_id', subscription.id)
      break
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription

      await supabase
        .from('subscriptions')
        .update({ status: 'canceled' })
        .eq('stripe_subscription_id', subscription.id)
      break
    }
  }

  return NextResponse.json({ received: true })
}
```

### 7. Environment Variables (.env.local)

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx

# Stripe (test mode)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID=price_xxx

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 8. Navigation (Next.js vs React Router)

```typescript
// AVANT (Vite - React Router)
import { useNavigate } from 'react-router-dom'
const navigate = useNavigate()
navigate('/onboarding/languages')

// APRÈS (Next.js)
import { useRouter } from 'next/navigation'
const router = useRouter()
router.push('/onboarding/languages')
```

### 9. Example Page with 'use client'

```typescript
// app/welcome/page.tsx
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/button'

export default function WelcomePage() {
  const [loading, setLoading] = useState(false)
  const supabase = createClient()

  const handleSignIn = async () => {
    setLoading(true)
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/onboarding/languages`,
      },
    })
  }

  return (
    <div>
      <h1>Welcome</h1>
      <Button onClick={handleSignIn} disabled={loading}>
        Continue with Google
      </Button>
    </div>
  )
}
```

---

## ✅ CHECKLIST FINALE AVANT DÉPLOIEMENT PRODUCTION

- [ ] Tous les tests E2E passent (auth, billing, extension)
- [ ] Staging Next.js testé pendant 24-48h sans bugs critiques
- [ ] Env vars configurées dans Vercel (Preview + Production)
- [ ] Stripe webhook configuré pour production URL
- [ ] Extension `manifest.json` inclut production URL
- [ ] RLS testé avec 2 comptes Google (isolation données)
- [ ] Backup Supabase créé
- [ ] Git tag créé : `git tag nextjs-migration-complete`

**Déploiement production :**
```bash
git checkout main
git merge develop
git push origin main
# Vercel déploie automatiquement
```

---

**Dernière mise à jour :** 31 octobre 2025
**Prochaine étape après migration :** Phase 2C - Production deployment & monitoring
