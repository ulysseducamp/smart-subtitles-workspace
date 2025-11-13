# Onboarding Flow - Subly Extension

**Date:** January 2025
**Last Updated:** January 13, 2025
**Status:** ✅ Phase 3 (A+B+C) COMPLÉTÉE - Staging Deployment Production-Ready
**Pricing:** $9/year subscription + 3-day free trial
**Auth Strategy:** Delayed auth (after vocab test) for higher conversion
**Email Reminder:** Non (pas de mention dans l'UI)
**Architecture:** Hybrid approach (structured but simple - no over-engineering)

---

## 🏗️ Architecture Decision: Hybrid Approach

### What We Keep SIMPLE (KISS)
✅ **No sessionStorage** - Users can restart if they refresh (rare case)
✅ **No clearOnboardingData()** - YAGNI (not used anywhere)
✅ **Simple Context** - Just React state, no persistence logic

### What We Structure NOW
✅ **Separate components** (ProgressBar, BackButton, FeedbackBanner, ImagePlaceholder)
- Reason: Ultra-simple (10-15 lines each), but keeps layout readable
- Benefit: Easy to maintain as project grows in Phase 2/3
- Cost: Only 10 extra minutes vs inline

### Why Hybrid?
- **Avoid over-engineering:** No premature abstractions (sessionStorage, complex state)
- **Future-proof:** Components ready for reuse without refactoring later
- **Maintainable:** Layout stays <100 lines even with Phase 2/3 additions
- **Standard:** Follows Next.js/Shadcn UI patterns

**Total Code:** 6 files, ~130 lines (vs 1 file with 300+ lines in 2 months)

---

## 📋 Implementation Plan (Incremental Testing Strategy)

**Philosophy:** Test early, test often. Build → Test → Fix → Continue.

### Phase 1A: Setup + First Test (30 min) ✅ COMPLÉTÉ
- [x] Créer `OnboardingContext.tsx` (simple state, no persistence)
- [x] Créer `OnboardingLayout.tsx` (progress + back + footer inline)
- [x] Créer 2 pages minimales pour test:
  - [x] `/welcome` - Juste titre + bouton "Start"
  - [x] `/onboarding/explanation-1` - Juste titre + bouton "Ok"
- [x] **🧪 TEST #1 (npm run dev):**
  - [x] ✓ Pages s'affichent sans erreur
  - [x] ✓ Progress bar visible (0% sur /welcome, 5% sur explanation-1)
  - [x] ✓ Back button fonctionne (retour vers /welcome)
  - [x] ✓ Footer visible en bas de page
  - [x] ✓ Navigation entre les 2 pages fonctionne
  - [x] **Si erreurs:** Debug avant de continuer
  - [x] **Si OK:** Continuer Phase 1B

### Phase 1B: Écrans 1-5 + Test (1h) ✅ COMPLÉTÉ
- [x] Créer `ImagePlaceholder.tsx` (réutilisable)
- [x] Compléter vraies pages 1-5 avec contenu:
  - [x] `/welcome` - Contenu complet + lien "Already have account"
  - [x] `/onboarding/explanation-1` - Image placeholder + texte
  - [x] `/onboarding/explanation-2` - Known words example
  - [x] `/onboarding/explanation-3` - One unknown word example
  - [x] `/onboarding/explanation-4` - Multiple unknown words example
- [x] **🧪 TEST #2 (npm run dev):**
  - [x] ✓ Navigation fonctionne (Welcome → Explanation 1-4)
  - [x] ✓ Progress bar avance (0% → 5% → 10% → 15% → 20%)
  - [x] ✓ Back button fonctionne sur tous les écrans
  - [x] ✓ Placeholders images s'affichent avec descriptions
  - [x] ✓ Footer présent sur tous les écrans
  - [x] ✓ Pas d'erreurs console
  - [x] **Si erreurs:** Debug avant de continuer
  - [x] **Si OK:** Continuer Phase 1C

### Phase 1C: Écrans 6-10 + Test (1h) ✅ COMPLÉTÉ
- [x] Créer écrans 6-10:
  - [x] `/onboarding/comparison` - Graph placeholder + texte
  - [x] `/onboarding/target-language` - Radio buttons (FR / PT-BR)
  - [x] `/onboarding/native-language` - Radio buttons (13 langues)
  - [x] `/onboarding/vocab-test-intro` - Texte explicatif
  - [x] `/onboarding/vocab-test-explanation` - Texte explicatif
- [x] **🧪 TEST #3 (npm run dev):**
  - [x] ✓ Navigation fonctionne (écrans 1-10 complets)
  - [x] ✓ Progress bar avance correctement (25% → 45%)
  - [x] ✓ Radio buttons fonctionnent (target + native language)
  - [x] ✓ Context stocke targetLang et nativeLang (check React DevTools)
  - [x] ✓ Bouton "Continue" disabled si aucune sélection
  - [x] ✓ Bouton "Continue" enabled après sélection
  - [x] **Si erreurs:** Debug avant de continuer
  - [x] **Si OK:** Continuer Phase 1D

### Phase 1D: Écrans 11-16 + Test (1h30) ✅ COMPLÉTÉ
- [x] Créer vocab test + results:
  - [x] `/onboarding/vocab-test` - Logique test avec 2 boutons
  - [x] Loading animation (3s) après click "I don't know"
  - [x] `/onboarding/results` - Display niveau (emoji 🎉 fixe, pas conditionnel)
  - [x] `/onboarding/vocab-benefits` - Texte bénéfices
- [x] **🧪 TEST #4 (npm run dev):**
  - [x] ✓ Vocab test affiche mots corrects (FR ou PT selon targetLang)
  - [x] ✓ Bouton "I know all" → niveau suivant
  - [x] ✓ Bouton "I don't know" → loading 3s → results
  - [x] ✓ Niveau affiché correctement sur /results
  - [x] ✓ Context stocke vocabLevel (check React DevTools)
  - [x] ✓ Progress bar avance (régularisée ~7% par écran)
  - [x] **Si erreurs:** Debug avant de continuer
  - [x] **Si OK:** Continuer Phase 1E

### Phase 1E: Écrans 17-20 + Test (1h) ✅ COMPLÉTÉ
- [x] Créer auth + pricing + complete:
  - [x] `/onboarding/auth` - Bouton Google (logo coloré SVG)
  - [x] `/onboarding/pricing-intro` - Teaser pricing
  - [x] `/onboarding/pricing-details` - Timeline 2 étapes
  - [x] `/onboarding/complete` - Success screen + screenshot placeholder
- [x] **🧪 TEST #5 (npm run dev):**
  - [x] ✓ Navigation complète 1-20 fonctionne
  - [x] ✓ Progress bar à 95% sur /auth puis cachée sur pricing/complete
  - [x] ✓ Aucun bug visuel sur les 20 écrans
  - [x] ✓ Timeline pricing s'affiche correctement (2 étapes)
  - [x] ✓ Tous les placeholders images présents
  - [x] **Si erreurs:** Debug avant de continuer
  - [x] **Si OK:** Continuer Phase 1F

### Phase 1F: Polish + Test Final (30 min) ✅ COMPLÉTÉ
- [x] Polish UI completed:
  - [x] Google logo coloré dans bouton auth
  - [x] Progress bar régularisée (~7% increments)
  - [x] Progress bar cachée sur pricing/complete
  - [x] Pricing text corrigé ($9/year)
- [x] Vérifications finales:
  - [x] Responsive mobile non nécessaire (extension desktop only)
  - [x] Vérifier responsive desktop (width: 1920px)
  - [x] Vérifier tous les 6 placeholders images ont descriptions claires
  - [x] Vérifier progress bar + back button sur TOUS les écrans
  - [x] Vérifier footer email présent partout
- [x] **🧪 TEST FINAL (toi + moi):**
  - [x] ✓ L'utilisateur teste le flow complet
  - [x] ✓ UX validée
  - [x] ✓ Prêt pour Phase 2 (backend)

**PHASE 1 COMPLÉTÉE ✅** - Tous les 20 écrans frontend créés et testés (Janvier 2025)

**Estimation totale Phase 1:** 5-6 heures avec tests incrémentaux

### Phase 2: Backend Integration ✅ COMPLÉTÉE (Janvier 2025)

**Status:** ✅ COMPLÉTÉE (January 12, 2025)
**Durée réelle:** ~3h (avec debug Stripe keys + investigation)
**Pricing:** $9/year + 3-day trial (changement depuis $1/month 14j)

**Approche:** Tests incrémentaux à chaque étape (KISS principle)

**Blocages résolus:**
- ❌ Stripe "No such price" → ✅ Clés TEST/LIVE mismatch (compte Stripe différent)
- ❌ Webhooks non testés en localhost → ✅ Normal, test en staging requis

---

#### 📦 **Étape 1: Setup Stripe (15 min)** ✅ COMPLÉTÉ

**Contexte:**
- Routes API Stripe existent déjà ✅ (`/api/stripe/checkout`, `/api/stripe/webhook`, `/api/stripe/portal`)
- Ancien price: $1/month + 14 jours trial
- Nouveau price: $9/year + 3 jours trial
- **Stripe prices sont IMMUTABLES** → Impossible de modifier monthly→yearly
- **Solution:** Ajouter nouveau price sur produit existant (pas nouveau produit)

**Actions:**

- [x] **Toi (Dashboard Stripe):**
  1. Aller sur https://dashboard.stripe.com/test/products
  2. Trouver produit existant "Subly Premium"
  3. Click "+ Add another price" (pas "Create product"!)
  4. Configurer:
     - Pricing model: **Recurring**
     - Price: **$9.00**
     - Billing period: **Yearly**
  5. Click "Save"
  6. **Copier le `price_id`** (format: `price_1SScLTCpd12v3sCmb1baxznb`)

- [x] **Moi (Code):**
  - [x] Update `.env.local` avec nouveau `STRIPE_PRICE_ID=price_1SScLTCpd12v3sCmb1baxznb`
  - [x] Redémarrer serveur Next.js

- [x] **Test #1:**
  - [x] Vérifier Stripe Dashboard: price créé en mode TEST
  - [x] Vérifier console que nouveau price_id est chargé
  - [x] ✅ PASSÉ → Étape 2

**Note:** Les 3 subscriptions test existantes ($1/month) resteront inchangées. Pas grave, ce sont des comptes test.

---

#### 🔧 **Étape 2: Modifier Code Stripe (10 min)** ✅ COMPLÉTÉ

**Fichier:** `webapp-next/src/app/api/stripe/checkout/route.ts`

**Modifications:**

- [x] Ligne 20: `trial_period_days: 14` → `trial_period_days: 3`
- [x] Ligne 24: `success_url: ${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pin-extension` → `/onboarding/complete`
- [x] Ligne 25: `cancel_url: ${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pricing` → `/onboarding/pricing-details`

**Code après modification:**
```typescript
subscription_data: {
  trial_period_days: 3,  // ← Changé de 14 à 3
  metadata: { user_id: userId },
},
success_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/complete`,  // ← Changé
cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pricing-details`,  // ← Changé
```

- [x] **Test #2:**
  - [x] Redémarrer serveur (`Ctrl+C` puis `npm run dev`)
  - [x] Vérifier aucune erreur TypeScript dans console
  - [x] ✅ PASSÉ → Étape 3

---

#### 🔗 **Étape 3: Brancher Pricing Details (15 min)** ✅ COMPLÉTÉ

**Fichier:** `webapp-next/src/app/onboarding/pricing-details/page.tsx`

**Problème actuel:** Bouton "Start Trial" redirige juste vers `/complete` (mock Phase 1)

**Solution:** Copier logique `handleCheckout()` de `/onboarding/pricing` (lignes 14-39)

**Modifications:**

- [x] Importer dépendances:
  ```typescript
  import { useAuth } from '@/contexts/AuthContext'
  import { useState } from 'react'
  ```

- [x] Ajouter state + fonction:
  ```typescript
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!user) return

    setLoading(true)
    try {
      const response = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user.id,
          email: user.email,
        }),
      })

      const { url } = await response.json()

      if (url) {
        window.location.href = url  // Redirect to Stripe Checkout
      }
    } catch (error) {
      console.error('Checkout error:', error)
      alert('Failed to start checkout. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  ```

- [x] Remplacer onClick du bouton:
  ```typescript
  // Avant:
  onClick={() => router.push('/onboarding/complete')}

  // Après:
  onClick={handleCheckout}
  disabled={loading || !user}
  ```

- [x] **Test #3 (CRITICAL):**
  1. [x] Naviguer http://localhost:3000/onboarding/pricing-details
  2. [x] Click "Start My 3-Day Free Trial"
  3. [x] ✅ Redirect vers Stripe Checkout OK (mauvaises clés initialement, corrigé)
  4. [x] ✅ Trial = **3 days** vérifié
  5. [x] ✅ Prix = **$9.00/year** vérifié
  6. [x] Paiement test effectué avec succès (carte `4242...`)
  7. [x] ✅ PASSÉ → Étape 4

---

#### 🔐 **Étape 4: Google OAuth + Supabase Sync + sessionStorage (30 min)** ✅ COMPLÉTÉ

**Problème Critique:**
- OAuth **recharge la page** après authentification (sécurité Google)
- React Context (mémoire temporaire) est **effacée** au reload
- **Résultat:** User perd données vocab test (targetLang, nativeLang, vocabLevel) 💥

**Solution: sessionStorage + Auto-sync**
- sessionStorage = "Coffre-fort" navigateur qui **survit aux reloads**
- Sync automatique: Chaque changement Context → Sauvegarde sessionStorage
- Après auth: Récupère sessionStorage → Sauvegarde Supabase → Clean

**Avantages:**
- ✅ User peut refresh n'importe où → Données restaurées
- ✅ Robuste contre fermeture onglet accidentelle
- ✅ Excellente UX (pas de perte de données)

**Fichiers à modifier:** 3

---

**Fichier 1:** `webapp-next/src/contexts/OnboardingContext.tsx`

**Modifications:**

- [x] Ajouter restauration depuis sessionStorage au mount:
  ```typescript
  // Au mount: Restaurer depuis sessionStorage si existe
  useEffect(() => {
    const saved = sessionStorage.getItem('onboarding_data')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        if (data.targetLang) setTargetLang(data.targetLang)
        if (data.nativeLang) setNativeLang(data.nativeLang)
        if (data.vocabLevel) setVocabLevel(data.vocabLevel)
        console.log('✅ Restored from sessionStorage:', data)
      } catch (e) {
        console.error('Failed to restore sessionStorage:', e)
      }
    }
  }, [])
  ```

- [x] Ajouter sync automatique à chaque changement:
  ```typescript
  // À chaque changement: Sauvegarder dans sessionStorage
  useEffect(() => {
    if (targetLang || nativeLang || vocabLevel) {
      const data = { targetLang, nativeLang, vocabLevel }
      sessionStorage.setItem('onboarding_data', JSON.stringify(data))
      console.log('💾 Saved to sessionStorage:', data)
    }
  }, [targetLang, nativeLang, vocabLevel])
  ```

---

**Fichier 2:** `webapp-next/src/app/auth/callback/route.ts`

**Modification:**

- [x] Changer redirect pour nouveau flow (ligne 49):
  ```typescript
  // AVANT (ancien flow):
  return NextResponse.redirect(`${origin}/onboarding/languages`)

  // APRÈS (nouveau flow 20 écrans):
  return NextResponse.redirect(`${origin}/onboarding/pricing-intro`)
  ```

**Contexte:** Dans le nouveau flow, auth est écran 17, pricing-intro est écran 18 (suite logique)

---

**Fichier 3:** `webapp-next/src/app/onboarding/pricing-intro/page.tsx`

**Modifications:**

- [x] Ajouter imports:
  ```typescript
  import { useAuth } from '@/contexts/AuthContext'
  import { useOnboarding } from '@/contexts/OnboardingContext'
  import { createClient } from '@/lib/supabase/client'
  import { useEffect, useState } from 'react'
  ```

- [x] Ajouter logique sauvegarde Supabase:
  ```typescript
  const { user } = useAuth()
  const { targetLang, nativeLang, vocabLevel } = useOnboarding()
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const saveToSupabase = async () => {
      // Attendre que user soit disponible + données Context chargées
      if (!user || !targetLang || !nativeLang || !vocabLevel || saved) return

      console.log('💾 Saving to Supabase...', { targetLang, nativeLang, vocabLevel })

      const supabase = createClient()

      try {
        // 1. Sauvegarder user_settings
        await supabase.from('user_settings').upsert({
          user_id: user.id,
          target_lang: targetLang,
          native_lang: nativeLang,
        })

        // 2. Sauvegarder vocab_levels
        await supabase.from('vocab_levels').upsert({
          user_id: user.id,
          language: targetLang,
          level: vocabLevel,
          tested_at: new Date().toISOString(),
        })

        // 3. Clean sessionStorage (plus besoin)
        sessionStorage.removeItem('onboarding_data')
        console.log('✅ Saved to Supabase + cleaned sessionStorage')
        setSaved(true)
      } catch (error) {
        console.error('❌ Failed to save to Supabase:', error)
      }
    }

    saveToSupabase()
  }, [user, targetLang, nativeLang, vocabLevel, saved])
  ```

---

**Test #4:**

- [x] **Test A: Flow normal sans refresh**
  1. [x] Naviguer http://localhost:3000/welcome
  2. [x] Compléter flow jusqu'à `/onboarding/auth`
  3. [x] Ouvrir DevTools Console (vérifier logs sessionStorage)
  4. [x] Click "Connect with Google"
  5. [x] ✅ Popup Google OAuth OK
  6. [x] Choisir compte Google
  7. [x] ✅ Redirect vers `/onboarding/pricing-intro` OK
  8. [x] ✅ Console: "💾 Saving to Supabase..." + "✅ Saved" confirmé
  9. [x] **Vérifier Supabase** (via MCP): Données user_settings + vocab_levels vérifiées
  10. [x] ✅ PASSÉ - Données présentes dans les 2 tables

- [x] **Test B: sessionStorage fonctionne** (vérifié via console logs)
  1. [x] sessionStorage sauvegarde après chaque sélection (target/native/vocab)
  2. [x] ✅ Logs "💾 Saved to sessionStorage" confirmés dans console
  3. [x] ✅ Données restaurées après OAuth reload
  4. [x] ✅ PASSÉ - Robustesse validée

- [x] **Test C: Test complet effectué**
  1. [x] Flow complet testé (Welcome → Complete)
  2. [x] OAuth Google fonctionnel
  3. [x] Supabase sync OK
  4. [x] ✅ PASSÉ → Étape 5

**Note webhook:** Le webhook existant (`/api/stripe/webhook/route.ts`) gère déjà `subscriptions` table ✅

---

#### 🧪 **Étape 5: Test Flow Complet End-to-End (20 min)** ✅ COMPLÉTÉ

**Objectif:** Valider flow complet avec stripe checkout en localhost

**Test A: Premier compte (nouveau user):**

- [x] 1. Ouvrir fenêtre incognito
- [x] 2. http://localhost:3000/welcome
- [x] 3. Click "Start"
- [x] 4. Naviguer tout le flow (explanations, languages, vocab test)
- [x] 5. `/onboarding/auth` → Google OAuth (ulysse.tutos@gmail.com)
- [x] 6. `/onboarding/pricing-intro` → Click "Try for $0.00"
- [x] 7. `/onboarding/pricing-details` → Click "Start My 3-Day Free Trial"
- [x] 8. Stripe Checkout → Entrer carte test `4242 4242 4242 4242`
- [x] 9. ✅ Redirect vers `/onboarding/complete` OK
- [x] 10. **Webhook:** Non testé en localhost (normal, Stripe ne peut pas atteindre localhost)
- [x] 11. **Vérifier Supabase (via MCP):** user_settings + vocab_levels vérifiés ✅
- [x] ✅ PASSÉ - Flow complet fonctionnel

**Test B: Webhook & subscription (à tester en staging/production):**

- [x] Localhost: Webhooks impossibles (Stripe ne peut pas atteindre localhost:3000)
- [x] Solution: Test webhooks lors du déploiement Vercel staging
- [x] Code webhook vérifié (déjà existant et fonctionnel depuis Phase 1B)
- [x] ✅ Déploiement staging requis pour test complet subscription

**Note:** Stripe keys TEST configurées, tout fonctionne en local sauf webhooks (attendu).

---

#### 📝 **Étape 6: Update Documentation (10 min)** ✅ COMPLÉTÉ

**Fichiers à mettre à jour:**

- [x] `/CLAUDE.md` (root):
  - [x] Stripe section: $1/month 14j → $9/year 3j ✅
  - [x] Update status Phase 2 → ✅ COMPLETED

- [x] `/webapp-next/CLAUDE.md`:
  - [x] Stripe Integration section: update pricing ✅
  - [x] Update environment variables example ✅

- [x] `/ONBOARDING_FLOW.md`:
  - [x] Checker toutes les checkboxes Phase 2 ✅
  - [x] Update "Last Updated" date ✅ (January 12, 2025)

- [x] **Test #6:**
  - [x] Relire les 3 fichiers ✅
  - [x] Vérifier cohérence (même prix partout) ✅
  - [x] ✅ Phase 2 100% COMPLÉTÉE 🎉

---

**Estimation Totale:** 1h30-2h
**Next:** Phase 3 (Polish & Extension Integration)

### Phase 3: Polish & Extension Integration

#### A. Images visuelles ✅ COMPLÉTÉ (January 12, 2025)
- [x] **Intégrer image 1:** `S+N=wand.png` dans `/onboarding/explanation-1`
- [x] **Intégrer images 2-4:** Before/after images dans `/onboarding/explanation-2,3,4`
  - [x] `known_words-before.png` + `known_words-after.png`
  - [x] `one_unknown-before.png` + `one_unknown-after.png`
  - [x] `multiple_unknown-before.png` + `multiple_unknown-after.png`
  - [x] Images réduites à `max-w-md` (~500px)
  - [x] Layout aligné à gauche pour meilleure lisibilité
- [x] **Intégrer image 5:** `graph_comparison.png` dans `/onboarding/comparison`
- [x] **Intégrer image 6:** `extension_popup.png` dans `/onboarding/complete`
- [x] **Test visuel:** Toutes les images affichées correctement ✅

#### B. Extension Integration ✅ COMPLÉTÉ (January 13, 2025)
- [x] Ajouter bouton "Manage Subscription" dans `Popup.tsx`
- [x] Lier bouton → `/api/stripe/portal` → ouvre Customer Portal
- [x] Tester flow: Install extension → Onboarding → Paiement → Popup fonctionne

#### C. Déploiement Staging ✅ COMPLÉTÉ (January 13, 2025)
- [x] Deploy sur Vercel staging (branch `develop`)
- [x] Configurer Stripe webhook staging (endpoint créé avec secret)
- [x] Corriger variables d'environnement Stripe (clés TEST, price ID, webhook secret)
- [x] Test end-to-end sur staging (paiement réussi, client créé, subscription Supabase OK)
- [x] **✅ Test final Phase 3:** Flow complet production-ready

---

## 🎨 Flow Utilisateur Complet (20 écrans)

### Écran 1: Welcome
**Route:** `/welcome`
**Progress:** 0%
**Back button:** Non visible (premier écran)

**Contenu:**
- Titre: "Welcome to Subly, the extension beloved by reddit users 🤖"
- Sous-titre: "To use subly, you first need to complete a few steps"
- Bouton principal: "Start" (noir)
- Lien en dessous: "Already have an account? login with google" (underlined)

**Comportement:**
- Click "Start" → `/onboarding/explanation-1`
- Click "login with google" → Auth Google → redirect `/welcome-back` (page existante)

**Notes techniques:**
- Pas d'auth sur cet écran (auth retardée à écran 17)
- Footer feedback présent

---

### Écran 2: Subly's Magic
**Route:** `/onboarding/explanation-1`
**Progress:** 5%
**Back button:** Visible (retour `/welcome`)

**Contenu:**
- Titre: "Subly's magic"
- **Image visuelle (placeholder Phase 1):**
  - Formule: `[S logo] + [N logo] = [wand icon ✨]`
  - Description pour placeholder: Logo Subly carré noir (S) + symbole plus + Logo Netflix rouge (N) + symbole égal + icône baguette magique
- Texte: "When watching Netflix, based on your level, Subly choose if a subtitle should be displayed in your target language or in your native language"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/explanation-2`

**Notes techniques:**
- Placeholder image avec annotation claire
- Image réelle fournie Phase 3

---

### Écran 3: Known Words Example
**Route:** `/onboarding/explanation-2`
**Progress:** 10%
**Back button:** Visible

**Contenu:**
- Titre: "If a subtitle contains only words that you know"
- **Exemple visuel (image ou CSS):**
  - Texte français: "Je le souhaite vraiment"
  - Annotations sous chaque mot: "known | known | known" (couleur verte)
  - Flèche vers bas (↓)
  - Cadre noir: "Je le souhaite vraiment"
- Texte explicatif: "→ Subly displays it in your target language"
- Sous-texte: "(Since you know all the necessary words to understand it)"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/explanation-3`

**Notes techniques:**
- Phase 1: Image placeholder avec description
- Phase 3: Image fournie par l'utilisateur

---

### Écran 4: One Unknown Word Example
**Route:** `/onboarding/explanation-3`
**Progress:** 15%
**Back button:** Visible

**Contenu:**
- Titre: "If a subtitle contains exactly one word that you don't know"
- **Exemple visuel:**
  - Texte français: "Je le souhaite vraiment"
  - Annotations: "known | known | unknown" (vraiment en rouge)
  - Flèche vers bas (↓)
  - Cadre noir: "Je le souhaite vraiment (really)"
- Texte explicatif: "→ Subly displays it in your target language with the translation of the unknown word"
- Sous-texte: "(so you can learn new words without needing to click)"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/explanation-4`

**Notes techniques:**
- Montrer traduction inline entre parenthèses
- Image placeholder Phase 1

---

### Écran 5: Multiple Unknown Words Example
**Route:** `/onboarding/explanation-4`
**Progress:** 20%
**Back button:** Visible

**Contenu:**
- Titre: "If a subtitle contains more than one word that you don't know"
- **Exemple visuel:**
  - Texte français: "Je le souhaite vraiment"
  - Annotations: "known | unknown | unknown" (2 mots en rouge)
  - Flèche vers bas (↓)
  - Cadre noir: "I really wish so"
- Texte explicatif: "→ Subly displays it in your native language"
- Sous-texte: "(so you don't loose time trying to understand it)"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/comparison`

**Notes techniques:**
- Texte en langue native (anglais dans exemple)
- Image placeholder Phase 1

---

### Écran 6: Subly vs Traditional Apps
**Route:** `/onboarding/comparison`
**Progress:** 25%
**Back button:** Visible

**Contenu:**
- Titre: "Subly vs traditional apps"
- **Graphique (image fournie Phase 3):**
  - Axe X: Time
  - Axe Y: New vocabulary acquired
  - Courbe rouge (traditional apps): pic début → chute rapide
  - Courbe noire (Subly): montée progressive et constante
  - Annotations sur graphique:
    - "burst of efforts at the begining" (pic rouge)
    - "the learners gives up after a few week" (chute)
    - "with traditional apps" (courbe rouge)
    - "with Subly" (courbe noire)
- Texte: "With Subly, learners stay consistent (because they learn through Netflix shows, the most engaging content in the world)"
- Bouton: "Continue" (noir)

**Comportement:**
- Click "Continue" → `/onboarding/target-language`

**Notes techniques:**
- Graphique = image fournie par l'utilisateur
- Placeholder Phase 1 avec description claire

---

### Écran 7: Select Target Language
**Route:** `/onboarding/target-language`
**Progress:** 30%
**Back button:** Visible

**Contenu:**
- Titre: "Please select your target language"
- Sous-titre: "(the language you want to learn)"
- **Radio buttons:**
  - ⚪ French
  - ⚪ Brazilian Portuguese
- Bouton: "Continue" (noir, disabled si aucune sélection)

**Comportement:**
- Sélection → stocker dans React Context (`targetLang`)
- Click "Continue" → `/onboarding/native-language`

**Notes techniques:**
- State management: React Context + sessionStorage
- Validation: Bouton disabled tant que rien sélectionné
- Cette sélection détermine les word lists du vocab test

---

### Écran 8: Select Native Language
**Route:** `/onboarding/native-language`
**Progress:** 35%
**Back button:** Visible

**Contenu:**
- Titre: "Please select your native language"
- Sous-titre: "(You will be able to change this language at anytime)"
- **Radio buttons (13 langues):**
  - ⚪ English
  - ⚪ French
  - ⚪ Spanish
  - ⚪ German
  - ⚪ Italian
  - ⚪ Portuguese
  - ⚪ Polish
  - ⚪ Dutch
  - ⚪ Swedish
  - ⚪ Danish
  - ⚪ Czech
  - ⚪ Japanese
  - ⚪ Korean
- Bouton: "Continue" (noir, disabled si aucune sélection)

**Comportement:**
- Sélection → stocker dans React Context (`nativeLang`)
- Click "Continue" → `/onboarding/vocab-test-intro`

**Notes techniques:**
- Liste complète des 13 langues supportées
- State management: React Context + sessionStorage

---

### Écran 9: Vocab Test Introduction
**Route:** `/onboarding/vocab-test-intro`
**Progress:** 40%
**Back button:** Visible

**Contenu:**
- Titre: "Now, it's time to test your vocabulary level"
- Texte: "To define your vocabulary level, we picked the list of the 5000 most used words in **{language}** ordered by frequency."
- Bouton: "Continue" (noir)

**Comportement:**
- Click "Continue" → `/onboarding/vocab-test-explanation`

**Notes techniques:**
- `{language}` dynamique basé sur `targetLang` du Context
  - Si `targetLang === 'fr'` → "French"
  - Si `targetLang === 'pt-BR'` → "Brazilian Portuguese"

---

### Écran 10: Vocab Test Explanation
**Route:** `/onboarding/vocab-test-explanation`
**Progress:** 45%
**Back button:** Visible

**Contenu:**
- Paragraphe 1: "We'll show you words selected from this list and you'll tell us if you know them or not."
- Paragraphe 2: "This will allow us to evaluate, approximately, how many of the most used words you know which will be your 'vocabulary level' Subly."
- Paragraphe 3: "(You'll be able to redo the test at anytime)"
- Bouton: "Start" (noir)

**Comportement:**
- Click "Start" → `/onboarding/vocab-test` (premier niveau)

**Notes techniques:**
- Séparation écran 9 + 10 pour meilleure lisibilité

---

### Écrans 11-13: Vocab Test Screens (Dynamique)
**Route:** `/onboarding/vocab-test`
**Progress:** 45-50% (fixe pendant le test)
**Back button:** Visible

**Contenu répété (jusqu'à 12 niveaux):**
- Mots affichés (6 mots séparés par virgules):
  - **Exemple FR niveau 100:** "lui, penser, soi, parce, très, après"
  - **Exemple FR niveau 200:** "sûr, mieux, dernier, jusque, moins, minute"
  - **Exemple PT niveau 100:** "ele, como, falar, mesmo, dever, onde"
- Sous-texte: "(Those words are part of the **{level}** most used words in **{language}**)"
- **Boutons (2 options):**
  - "There is one or several words I don't now" (bouton blanc avec bordure)
  - "I know all the words" (bouton noir)

**Comportement:**
- Click "I know all the words" → Niveau suivant
- Click "There is one or several words I don't now" → **STOP** le test
  - Niveau final = niveau actuel
  - Transition: Animation loading 3s
  - Redirect: `/onboarding/vocab-results`

**Notes techniques Phase 1:**
- Hardcoder la liste des 12 niveaux (static data)
- State: `currentLevel` (index 0-11)
- Click "I know all" → `setCurrentLevel(currentLevel + 1)`

**Word Lists:**

**Portuguese (PT-BR):**
```
100: ele, como, falar, mesmo, dever, onde
200: mundo, tentar, lugar, nome, importante, último
300: morrer, certeza, enquanto, olá, contra, corpo
500: errar, serviço, preço, uma, considerar, vai
700: sentar, clicar, cerca, câmera, vermelho, principalmente
1000: observar, membro, americano, desaparecer, apoiar, mamãe
1500: cobrir, relacionar, proteção, expressão, lua, particular
2000: reclamar, impacto, honra, móvel, tribunal, pior
2500: imóvel, duplo, vendedor, olhe, estender, energético
3000: influenciar, mínimo, sensor, ocasião, assegurar, telhado
4000: verso, ousar, puxa, mole, entretenimento, blusa
5000: exausto, art., surdo, deusa, box, parece
```

**French (FR):**
```
100: lui, penser, soi, parce, très, après
200: sûr, mieux, dernier, jusque, moins, minute
300: continuer, voulais, gros, espérer, suivre, amour
500: dur, réponse, préparer, page, tirer, exactement
700: principal, propos, arme, augmenter, concerner, gérer
1000: évidemment, supérieur, réveiller, épisode, attraper, rendez-vous
1500: sors, campagne, soupe, coller, fiche, réaction
2000: commencer, pardon, drogue, porc, essai, saveur
2500: contexte, soudainement, guérir, marketing, assistant, introduire
3000: emballer, petit-déjeuner, ai-je, moi, assis, rédiger
4000: calendrier, généreux, touriste, vigueur, honorer, pousse
5000: résistant, optique, reportage, gémissement, résulter, amande
```

---

### Écran 14: Loading - Defining Level
**Route:** Transition dans `/onboarding/vocab-test`
**Progress:** 50% (fixe pendant loading)
**Back button:** Disabled pendant loading

**Contenu:**
- Titre: "Defining your vocabulary level..."
- Barre de chargement horizontale (progress bar secondaire)
  - Animation: 0% → 100% en 2-3 secondes

**Comportement:**
- Animation CSS pure
- Après 3s → Redirect automatique vers `/onboarding/vocab-results`

**Notes techniques:**
- `setTimeout(() => router.push('/onboarding/vocab-results'), 3000)`
- But: Créer anticipation

---

### Écran 15: Vocab Test Results
**Route:** `/onboarding/vocab-results`
**Progress:** 55%
**Back button:** Visible

**Contenu:**
- Emoji: 🎉
- Titre: "You know approximately **{level}** words of the most used words in **{language}**"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/vocab-benefits`

**Notes techniques:**
- `{level}` et `{language}` depuis Context
- Exemple: "You know approximately **2000** words of the most used words in **French**"

---

### Écran 16: Vocab Test Benefits
**Route:** `/onboarding/vocab-benefits`
**Progress:** 60%
**Back button:** Visible

**Contenu:**
- Texte 1: "On average, users with this level aquire **30 new words per episode**."
- Texte 2: "Which means you will double the number of words you know just by watching a few series with Subly 🥳"
- Bouton: "Ok" (noir)

**Comportement:**
- Click "Ok" → `/onboarding/auth`

**Notes techniques:**
- Texte statique pour MVP

---

### Écran 17: Save Your Infos (AUTH SCREEN) 🔐
**Route:** `/onboarding/auth`
**Progress:** 65%
**Back button:** Visible

**Contenu:**
- Titre: "Save your infos"
- Bouton: "Connect with google" (avec logo Google, bouton noir)

**Comportement Phase 1:**
- Click → Simuler auth
- Redirect → `/onboarding/pricing-intro`

**Comportement Phase 2:**
- Click → Google OAuth via Supabase
- Après auth:
  1. INSERT `user_settings` (target_lang, native_lang)
  2. INSERT `vocab_levels` (language, level, tested_at)
  3. Redirect → `/onboarding/pricing-intro`

**Notes techniques:**
- **PREMIER écran avec authentification** (delayed auth strategy)

---

### Écran 18: Pricing - Try for Free
**Route:** `/onboarding/pricing-intro`
**Progress:** 70%
**Back button:** Visible

**Contenu:**
- Titre: "We want you to try Subly for free"
- Sous-titre avec checkmark: "✓ No Payment Due Now"
- Bouton: "Try for 0.00$" (noir)
- Texte en dessous: "After, Just **9$ per year** for full access"

**Comportement:**
- Click "Try for 0.00$" → `/onboarding/pricing-details`

**Notes techniques:**
- Wording: "$9 per year" pour clarté

---

### Écran 19: Pricing - Trial Details (2 ÉTAPES) ✅
**Route:** `/onboarding/pricing-details`
**Progress:** 75%
**Back button:** Visible

**Contenu:**
- Titre: "Start your 3-day FREE trial to continue"
- **Timeline verticale (2 étapes seulement):**
  - **● Today**
    - "Unlock the full potential of Subly"
  - **● In 3 days - Billing**
    - "You'll be charged $9, unless you cancel before."
- Texte "Good to know": "You'll be able to cancel your trial at any time through the 'manage subscription' button"
- Bouton: "Start My 3-Day Free Trial" (noir)
- Texte en dessous: "3 days free, then just **$9/year**"

**Comportement Phase 1:**
- Click → Redirect `/onboarding/complete`

**Comportement Phase 2:**
- Click → Créer Stripe Checkout Session
  - Mode: `subscription`
  - Price: `price_XXX` ($9/year)
  - Trial: `trial_period_days: 3`
  - Success URL: `/onboarding/complete`
  - Cancel URL: `/onboarding/pricing-details`

**Notes techniques:**
- Timeline: 2 points uniquement (pas d'email reminder)
- CSS flexbox + border-left pour ligne verticale

---

### Écran 20: (EXTERNE) Stripe Checkout
**Route:** Externe (https://checkout.stripe.com/...)
**Progress:** N/A
**Back button:** N/A

**Contenu:**
- Page Stripe standard
- Produit: "Subly Annual Subscription"
- Prix: $9.00/year
- Trial: 3 days free
- Carte test: 4242 4242 4242 4242

**Comportement:**
- Après paiement → Webhook Stripe → INSERT `subscriptions`
- Redirect success → `/onboarding/complete`
- Redirect cancel → `/onboarding/pricing-details`

---

### Écran 21: Complete - You're All Set! 🎉
**Route:** `/onboarding/complete`
**Progress:** 100%
**Back button:** Disabled

**Contenu:**
- Avatar utilisateur (photo Google ou icône par défaut)
- Titre: "Congrats you're all set!"
- Texte explicatif: "You can start using the extension: when watching Netflix, click on the Subly icon to make this pop-up appear, then click on the button 'Process subtitles' to adapt the Netflix subtitles to your level."
- **Image:** Screenshot de la popup extension sur Netflix
- Texte en dessous: "As you can see, through this pop-up you can change your languages and your level at any time."

**Comportement:**
- Écran terminal: User peut fermer le tab

**Notes techniques:**
- Image screenshot fournie Phase 3
- Placeholder Phase 1
- Footer feedback présent

---

## 🔧 Détails Techniques d'Implémentation

### Structure de Dossiers
```
webapp-next/src/
├── app/
│   ├── welcome/page.tsx (Écran 1)
│   └── onboarding/
│       ├── layout.tsx (Progress + Back + Footer)
│       ├── explanation-1/page.tsx
│       ├── explanation-2/page.tsx
│       ├── explanation-3/page.tsx
│       ├── explanation-4/page.tsx
│       ├── comparison/page.tsx
│       ├── target-language/page.tsx
│       ├── native-language/page.tsx
│       ├── vocab-test-intro/page.tsx
│       ├── vocab-test-explanation/page.tsx
│       ├── vocab-test/page.tsx
│       ├── vocab-results/page.tsx
│       ├── vocab-benefits/page.tsx
│       ├── auth/page.tsx
│       ├── pricing-intro/page.tsx
│       ├── pricing-details/page.tsx
│       └── complete/page.tsx
├── contexts/
│   └── OnboardingContext.tsx
└── components/onboarding/
    ├── ProgressBar.tsx
    ├── BackButton.tsx
    ├── FeedbackBanner.tsx
    └── ImagePlaceholder.tsx
```

### Progress Map
```typescript
const PROGRESS_MAP: Record<string, number> = {
  '/welcome': 0,
  '/onboarding/explanation-1': 5,
  '/onboarding/explanation-2': 10,
  '/onboarding/explanation-3': 15,
  '/onboarding/explanation-4': 20,
  '/onboarding/comparison': 25,
  '/onboarding/target-language': 30,
  '/onboarding/native-language': 35,
  '/onboarding/vocab-test-intro': 40,
  '/onboarding/vocab-test-explanation': 45,
  '/onboarding/vocab-test': 50,
  '/onboarding/vocab-results': 55,
  '/onboarding/vocab-benefits': 60,
  '/onboarding/auth': 65,
  '/onboarding/pricing-intro': 70,
  '/onboarding/pricing-details': 75,
  '/onboarding/complete': 100,
}
```

---

## 📝 Images à Fournir (Phase 3)

1. **Subly's magic:** Logo S + Logo N + icône baguette magique
2. **Known words:** "Je le souhaite vraiment" avec annotations vertes
3. **One unknown word:** "Je le souhaite vraiment" avec 1 mot rouge + traduction
4. **Multiple unknown words:** "Je le souhaite vraiment" avec 2 mots rouges
5. **Graph Subly vs traditional apps:** Courbes rouge (chute) vs noire (montée)
6. **Extension popup screenshot:** Screenshot de la popup sur Netflix

---

**Last Updated:** January 13, 2025
**Status:** ✅ Phase 3 COMPLETE - Staging Production-Ready
**Next Steps:** Phase 4 (Production Deployment) or additional testing
