# Onboarding Flow - Subly Extension

**Date:** January 2025
**Status:** 🚧 EN COURS - Phase 1 (Frontend Only)
**Pricing:** $9/year subscription + 3-day free trial
**Auth Strategy:** Delayed auth (after vocab test) for higher conversion
**Email Reminder:** Non (pas de mention dans l'UI)

---

## 📋 Implementation Plan

### Phase 1: Frontend Only (Coquille Vide) 🚧
- [ ] **Setup:** Créer structure de base + components partagés
  - [ ] Créer `OnboardingLayout.tsx` avec progress bar + back button + footer
  - [ ] Créer `OnboardingContext.tsx` pour gérer l'état de progression
  - [ ] Créer composant `<BackButton />` avec flèche
  - [ ] Créer composant `<FeedbackBanner />` (footer)
  - [ ] Créer composant `<ImagePlaceholder />` pour images temporaires
- [ ] **Test intermédiaire #1:** Vérifier layout sur 2 pages test (navigation + progress bar)
- [ ] **Écrans 1-5:** Welcome + Explanation flow
  - [ ] `/welcome` - Welcome screen
  - [ ] `/onboarding/explanation-1` - Subly's magic
  - [ ] `/onboarding/explanation-2` - Known words example
  - [ ] `/onboarding/explanation-3` - One unknown word
  - [ ] `/onboarding/explanation-4` - Multiple unknown words
- [ ] **Test intermédiaire #2:** Vérifier progress bar avance correctement (0% → 20%)
- [ ] **Écrans 6-10:** Comparison + Languages + Vocab test intro
  - [ ] `/onboarding/comparison` - Subly vs traditional apps
  - [ ] `/onboarding/target-language` - Select target language
  - [ ] `/onboarding/native-language` - Select native language
  - [ ] `/onboarding/vocab-test-intro` - Vocab test introduction
  - [ ] `/onboarding/vocab-test-explanation` - Vocab test explanation
- [ ] **Écrans 11-16:** Vocab test + Results
  - [ ] `/onboarding/vocab-test` - Dynamic vocab test (UI only, static data)
  - [ ] Ajouter loading animation (3s) après test
  - [ ] `/onboarding/vocab-results` - Display results with emoji
  - [ ] `/onboarding/vocab-benefits` - Benefits explanation
- [ ] **Test intermédiaire #3:** Flow complet écrans 1-16 (navigation avant/arrière)
- [ ] **Écrans 17-19:** Auth + Pricing
  - [ ] `/onboarding/auth` - Google auth screen (button only, no logic)
  - [ ] `/onboarding/pricing-intro` - Try for free teaser
  - [ ] `/onboarding/pricing-details` - Trial timeline + details (2 étapes)
- [ ] **Écran 20:** Complete
  - [ ] `/onboarding/complete` - Final success screen
- [ ] **Polish Frontend:**
  - [ ] Ajouter placeholders pour 6 images visuelles avec annotations claires
  - [ ] Vérifier responsive mobile/desktop sur tous les écrans
  - [ ] Vérifier progress bar + back button sur tous les écrans
  - [ ] Vérifier footer présent partout
- [ ] **✅ Test final Phase 1:** L'utilisateur teste le flow complet et valide l'UX

### Phase 2: Backend Integration
- [ ] **Stripe Setup:**
  - [ ] Créer nouveau produit Stripe: "Subly Annual" - $9/year
  - [ ] Configurer trial de 3 jours dans code (subscription_data.trial_period_days: 3)
  - [ ] Tester avec price_id en mode TEST
- [ ] **Auth + Vocab Test:**
  - [ ] Implémenter Google Auth à `/onboarding/auth`
  - [ ] Brancher vocab test dynamique avec vraies listes PT/FR
  - [ ] Logique d'arrêt du test ("I don't know" → stop)
  - [ ] Stocker sélections dans React Context + sessionStorage
- [ ] **Test intermédiaire #4:** Vocab test avec données réelles + calcul niveau
- [ ] **Stripe Integration:**
  - [ ] Créer `/api/stripe/checkout-annual` (ou modifier existant)
  - [ ] Passer `trial_period_days: 3` dans session Stripe
  - [ ] Configurer success_url → `/onboarding/complete`
  - [ ] Configurer cancel_url → `/onboarding/pricing-details`
- [ ] **Webhook Stripe:**
  - [ ] Modifier `/api/stripe/webhook` pour gérer $9/year subscription
  - [ ] Event `checkout.session.completed` → sauver dans `subscriptions`
  - [ ] Event `customer.subscription.updated` → update status
  - [ ] Event `customer.subscription.deleted` → cancel status
- [ ] **Supabase Sync:**
  - [ ] Après auth → INSERT dans `user_settings` (target_lang, native_lang)
  - [ ] Après auth → INSERT dans `vocab_levels` (language, level, tested_at)
  - [ ] Après paiement → INSERT dans `subscriptions` (stripe_customer_id, status='trialing')
- [ ] **Test intermédiaire #5:** Flow complet avec carte test 4242... → vérifier DB
- [ ] **✅ Test final Phase 2:** Flow complet avec 2 comptes Google (RLS validation)

### Phase 3: Polish & Extension Integration
- [ ] **Images visuelles:**
  - [ ] Intégrer image 1: Subly's magic (S + N = wand)
  - [ ] Intégrer image 2: Known words example
  - [ ] Intégrer image 3: One unknown word example
  - [ ] Intégrer image 4: Multiple unknown words example
  - [ ] Intégrer image 5: Subly vs traditional apps graph
  - [ ] Intégrer image 6: Extension popup screenshot (écran complete)
- [ ] **Extension Integration:**
  - [ ] Ajouter bouton "Manage Subscription" dans `Popup.tsx`
  - [ ] Lier bouton → `/api/stripe/portal` → ouvre Customer Portal
  - [ ] Tester flow: Install extension → Onboarding → Paiement → Popup fonctionne
- [ ] **Déploiement Staging:**
  - [ ] Deploy sur Vercel staging (branch `develop`)
  - [ ] Configurer Stripe webhook staging
  - [ ] Test end-to-end sur staging
- [ ] **✅ Test final Phase 3:** Flow complet production-ready

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

**Last Updated:** January 2025
**Status:** ✅ Ready for Phase 1 implementation
**Next Steps:** Create layout + first 3 pages for Test #1
