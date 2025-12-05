# LANDING V3 - Plan de Développement

## 🎯 Objectif

Créer un **3ème parcours d'onboarding** (`/landing-v3`) pour A/B testing, optimisé pour la conversion. Ce parcours améliore `/landing` en :
- Posant les questions de langue **plus tôt** (écrans 2-3) pour personnaliser l'explication
- Ajoutant des **questions de qualification** (struggles, learning duration, frequency)
- Réorganisant l'**ordre des écrans d'explication** pour une meilleure clarté
- Utilisant une **personnalisation dynamique** ({TL}, {NL}, {choice}) pour plus d'engagement

---

## 📊 Vue d'ensemble du Flow

### SECTION 1 : "How it works" (écrans 1-16)
**Objectif** : Expliquer le concept AVANT de collecter les infos personnelles
**Barre de progression** : "How it works" (0% → 100%)
**Navigation** : Auto-navigation sur les radios buttons des langues

### SECTION 2 : "Setting up Subly" (écrans 17-22)
**Objectif** : Qualification + Auth + Pricing
**Barre de progression** : "Setting up Subly" (**commence à 50%** car vocab test déjà fait)
**Navigation** : Classique avec boutons "Continue"

### SECTION 3 : Suite identique à `/landing`
Post-auth → Pricing → Complete (100% identique à `/landing/setup/post-auth` et suivants)

---

## 📝 Détail de chaque écran

### SECTION 1 : "How it works"

#### Écran 1 : Landing Page
**Route** : `/landing-v3` (page principale)
**Status** : ✅ **IDENTIQUE à `/landing/page.tsx`**
**Contenu** :
- Titre : "Subly"
- Image : Netflix hero (desktop/mobile responsive)
- Bouton : "Discover how it works" → `/landing-v3/intro`

---

#### Écran 2 : Target Language Selection
**Route** : `/landing-v3/target-language`
**Status** : 🆕 **NOUVEAU** (s'inspirer de `/onboarding/target-language`)
**Barre de progression** : "How it works" (~10%)
**Contenu** :
- Titre : "What language do you want to learn?"
- Radio buttons : Portuguese, French (liste extensible)
- **Navigation** : Auto-navigation au clic (pas de bouton "Continue")
- **Stockage** : Sauvegarder dans Context `targetLanguage` (ex: "Portuguese", "French")

**Code technique** :
```tsx
const handleLanguageSelect = (language: string) => {
  setTargetLanguage(language) // Context
  router.push('/landing-v3/native-language')
}
```

---

#### Écran 3 : Native Language Selection
**Route** : `/landing-v3/native-language`
**Status** : 🆕 **NOUVEAU** (s'inspirer de `/onboarding/native-language`)
**Barre de progression** : "How it works" (~20%)
**Contenu** :
- Titre : "What is your native language?"
- Radio buttons : 13 langues (English, French, Spanish, German, Italian, Portuguese, Polish, Dutch, Swedish, Danish, Czech, Japanese, Korean)
- **Navigation** : Auto-navigation au clic
- **Stockage** : Sauvegarder dans Context `nativeLanguage` (ex: "English", "French")

---

#### Écran 4 : Subly's Magic
**Route** : `/landing-v3/magic`
**Status** : ✏️ **MODIFIER `/landing/magic/page.tsx`**
**Barre de progression** : "How it works" (~30%)
**Contenu** :
- Image : `/landing/magic-demonstration.png` (identique)
- Titre : "Subly's magic"
- Texte : **DYNAMIQUE** avec `{targetLanguage}` et `{nativeLanguage}`
  - "When you watch Netflix, for each subtitle, Subly chooses if it should be displayed in **{targetLanguage}** or in **{nativeLanguage}** (based on the words you know and don't know)"
- Bouton : "Ok" → `/landing-v3/vocab-level`

**Code technique** :
```tsx
const { targetLanguage, nativeLanguage } = useOnboardingContext()

<p className="text-lg">
  When you watch Netflix, for each subtitle, Subly chooses if it should be displayed in <strong>{targetLanguage}</strong> or in <strong>{nativeLanguage}</strong> (based on the words you know and don't know)
</p>
```

---

#### Écran 5 : You Know Your Level
**Route** : `/landing-v3/vocab-level`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (~35%)
**Contenu** :
- Titre : "You know your level"
- Texte : [Texte du wireframe - à récupérer du wireframe si disponible, sinon demander à l'utilisateur]
- Bouton : "Ok" → `/landing-v3/frequency-list`

---

#### Écran 6 : Frequency List Explanation
**Route** : `/landing-v3/frequency-list`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (~40%)
**Contenu** :
- Titre : [À récupérer du wireframe]
- Texte : **DYNAMIQUE** avec `{targetLanguage}`
  - "A frequency list is the list of the most used words in a language"
  - Mentions de `{targetLanguage}` dans le texte (remplacer "TL" par `{targetLanguage}`)
- **Note** : Le mot "studies" est du texte normal, **pas un lien**, pas de gras
- Bouton : "Ok" → `/landing-v3/studies`

---

#### Écran 7 : Studies
**Route** : `/landing-v3/studies`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (~45%)
**Contenu** :
- Titre : [À récupérer du wireframe]
- Texte : [Texte du wireframe avec mention "studies" en texte normal]
- Bouton : "Ok" → `/landing-v3/belief`

---

#### Écran 8 : We Believe
**Route** : `/landing-v3/belief`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (~50%)
**Contenu** :
- Titre : "We believe that if you want..."
- Texte : [Texte complet du wireframe]
- Bouton : "Ok" → `/landing-v3/level-question`

---

#### Écran 9 : Do You Want to Know Your Level?
**Route** : `/landing-v3/level-question`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (~55%)
**Contenu** :
- Titre : "Do you want to know your level?"
- Texte : [Texte du wireframe si disponible]
- Bouton : "Start" → `/landing-v3/setup/vocab-intro`

---

#### Écran 10 : Vocab Test Intro
**Route** : `/landing-v3/setup/vocab-intro`
**Status** : ✏️ **MODIFIER `/landing/setup/vocab-intro/page.tsx`**
**Barre de progression** : "How it works" (~60%)
**Contenu** :
- Garder les écrans d'intro actuels de `/landing/setup/vocab-intro`
- **Modification** : Ne PAS demander les langues (déjà collectées en écrans 2-3)
- Passer directement au test avec `targetLanguage` et `nativeLanguage` du Context

---

#### Écran 11 : Vocab Test
**Route** : `/landing-v3/setup/vocab-test`
**Status** : ✅ **IDENTIQUE à `/landing/setup/vocab-test`**
**Barre de progression** : "How it works" (~70%)
**Contenu** :
- Test de vocabulaire 12 niveaux (100-5000)
- Utilise `targetLanguage` du Context

---

#### Écran 12 : Congrats
**Route** : `/landing-v3/setup/congrats`
**Status** : 🆕 **NOUVEAU** (s'inspirer de l'écran avec icône fête dans `/onboarding`)
**Barre de progression** : "How it works" (~75%)
**Contenu** :
- Icône : 🎉 (même icône que dans `/onboarding`, à localiser)
- Titre : "Congrats!"
- Texte : [Texte du wireframe]
- Bouton : "Continue" → `/landing-v3/setup/chrome-extension`

**Note** : Chercher dans `/onboarding` l'écran avec l'icône de fête pour réutiliser la même image

---

#### Écran 13 : Subly is a Chrome Extension
**Route** : `/landing-v3/setup/chrome-extension`
**Status** : ✏️ **MODIFIER** (écran existe dans `/onboarding`)
**Barre de progression** : "How it works" (~80%)
**Contenu** :
- Image : Réutiliser l'image de l'écran Chrome extension existant dans `/onboarding`
- Titre : "Subly is a Chrome extension"
- Texte : **NOUVEAU texte du wireframe** (différent de l'onboarding précédent)
- Bouton : "Continue" → `/landing-v3/setup/explanation-1`

---

#### Écran 14-16 : How It Works Explanations
**Routes** :
- `/landing-v3/setup/explanation-1`
- `/landing-v3/setup/explanation-2`
- `/landing-v3/setup/explanation-3`

**Status** : ✏️ **MODIFIER `/landing/setup/explanation-*`**
**Barre de progression** : "How it works" (80% → 100%)
**Ordre** : ⚠️ **Différent de `/landing`** :

1. **Explanation 1** : "If a subtitle contains **only words that you know**"
   - Texte : "Subly displays it in **{targetLanguage}**" (dynamique)
   - Image : Subtitle en target language

2. **Explanation 2** : "If a subtitle contains **more than one word that you don't know**"
   - Texte : "Subly displays it in **{nativeLanguage}**" (dynamique)
   - Image : Subtitle en native language

3. **Explanation 3** : "If a subtitle contains **exactly one word that you don't know**"
   - Texte : "Subly translates this word inline"
   - Image : Subtitle avec traduction inline

**Code technique** :
```tsx
const { targetLanguage, nativeLanguage } = useOnboardingContext()

<p>Subly displays it in <strong>{targetLanguage}</strong></p>
```

---

#### Écran 17 : Automatic Translation System
**Route** : `/landing-v3/setup/automatic-system`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "How it works" (100% - dernière étape)
**Contenu** :
- Titre : "With this automatic translation system..."
- Texte : [Texte du wireframe]
- Bouton : "Continue" → `/landing-v3/setup/reach-fluency`

---

#### Écran 18 : Reach Fluency (Transition)
**Route** : `/landing-v3/setup/reach-fluency`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : ⚠️ **PAS DE BARRE** (transition entre Section 1 et 2)
**Contenu** :
- Titre : "If you use Subly you will reach..."
- Texte : [Texte du wireframe]
- Bouton : "Continue" → `/landing-v3/setup/main-struggles`

**Note importante** : Cet écran marque la transition entre l'explication et le setup. Pas de barre de progression pour signaler visuellement le changement de phase.

---

### SECTION 2 : "Setting up Subly"

#### Écran 19 : Main Struggles
**Route** : `/landing-v3/setup/main-struggles`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "Setting up Subly" (**commence à 50%**)
**Contenu** :
- Titre : "What are your main struggles with **{targetLanguage}**?" (dynamique)
- Radio buttons : [Options du wireframe]
- **Navigation** : Auto-navigation au clic (comme écrans de langues)
- **Stockage** : Sauvegarder dans Context `mainStruggle` (ex: "Grammar", "Vocabulary", etc.)

**Code technique** :
```tsx
const { targetLanguage } = useOnboardingContext()

<h1>What are your main struggles with <strong>{targetLanguage}</strong>?</h1>
```

---

#### Écran 20 : You Are in Good Hands
**Route** : `/landing-v3/setup/good-hands`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "Setting up Subly" (~60%)
**Contenu** :
- Titre : "You are in good hands"
- Texte : **DYNAMIQUE** avec `{mainStruggle}`
  - Intégrer la réponse de l'écran précédent : "We know that {mainStruggle} is challenging, but..."
- Bouton : "Continue" → `/landing-v3/setup/learning-duration`

**Code technique** :
```tsx
const { mainStruggle } = useOnboardingContext()

<p>We know that <strong>{mainStruggle}</strong> is challenging, but...</p>
```

---

#### Écran 21 : Learning Duration
**Route** : `/landing-v3/setup/learning-duration`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "Setting up Subly" (~70%)
**Contenu** :
- Titre : "For how long have you been learning **{targetLanguage}**?" (dynamique)
- Radio buttons : [Options du wireframe - ex: "Less than 1 year", "1-3 years", "3+ years"]
- **Navigation** : Auto-navigation au clic
- **Stockage** : Sauvegarder dans Context `learningDuration` (optionnel, pas réutilisé après)

---

#### Écran 22 : Study Frequency
**Route** : `/landing-v3/setup/study-frequency`
**Status** : 🆕 **NOUVEAU**
**Barre de progression** : "Setting up Subly" (~80%)
**Contenu** :
- Titre : "How often do you study/practice/learn **{targetLanguage}**?" (dynamique)
- Radio buttons : [Options du wireframe - ex: "Daily", "Few times a week", "Weekly"]
- **Navigation** : Auto-navigation au clic
- **Stockage** : Sauvegarder dans Context `studyFrequency` (optionnel)

---

#### Écran 23 : Subly vs Traditional Apps
**Route** : `/landing-v3/setup/comparison`
**Status** : ✅ **IDENTIQUE à `/landing/comparison`**
**Barre de progression** : "Setting up Subly" (~90%)
**Contenu** :
- Image de comparaison (même que `/landing`)
- Texte : "Subly vs traditional apps"
- Bouton : "Continue" → `/landing-v3/setup/auth`

---

#### Écran 24 : Google Authentication
**Route** : `/landing-v3/setup/auth`
**Status** : ✅ **IDENTIQUE à `/landing/setup/auth`**
**Barre de progression** : "Setting up Subly" (~95%)
**Contenu** :
- Titre : "Now it's time to connect with Google"
- Texte : "So we can save your infos..."
- Bouton : "Connect with Google" → OAuth flow

---

### SECTION 3 : Suite identique à `/landing`

**Routes** :
- `/landing-v3/setup/post-auth`
- `/landing-v3/setup/pricing`
- `/landing-v3/setup/analyzing`
- `/landing-v3/setup/results`
- `/landing-v3/setup/finish-cta`
- `/landing-v3/setup/complete`

**Status** : ✅ **100% IDENTIQUE à `/landing/setup/*`**
**Barre de progression** : "Setting up Subly" (95% → 100%)

---

## 🏗️ Architecture Technique

### Context : OnboardingContext

Créer un Context pour stocker les données utilisateur pendant le parcours.

**Fichier** : `webapp-next/src/contexts/LandingV3Context.tsx`

**État** :
```tsx
interface LandingV3ContextType {
  // Section 1: Languages
  targetLanguage: string | null
  nativeLanguage: string | null

  // Section 2: Qualification
  mainStruggle: string | null
  learningDuration: string | null
  studyFrequency: string | null

  // Actions
  setTargetLanguage: (lang: string) => void
  setNativeLanguage: (lang: string) => void
  setMainStruggle: (struggle: string) => void
  setLearningDuration: (duration: string) => void
  setStudyFrequency: (frequency: string) => void
}
```

**Utilisation** :
- Wrap `/landing-v3` avec `<LandingV3Provider>`
- Importer dans chaque page : `const { targetLanguage, nativeLanguage } = useLandingV3Context()`
- Texte dynamique : `<p>Learn {targetLanguage}...</p>`

**Stockage** : En mémoire uniquement (React state), pas de sessionStorage pour MVP (principe YAGNI)

---

### Layouts : Double Barre de Progression

#### Layout 1 : "How it works"
**Fichier** : `/landing-v3/layout.tsx`
**Barre** : "How it works" (0% → 100%)
**Écrans** : 1-18 (jusqu'à `/reach-fluency` exclus)

#### Layout 2 : "Setting up Subly"
**Fichier** : `/landing-v3/setup/layout.tsx`
**Barre** : "Setting up Subly" (**50% → 100%**)
**Écrans** : 19-24+

**Code technique** :
```tsx
// Dans /landing-v3/setup/layout.tsx
const progressValue = calculateProgress() // Commence à 50

<ProgressBarWithBack
  title="Setting up Subly"
  progress={progressValue}
/>
```

---

### Composants Partagés

**Réutiliser** (déjà dans `/components`) :
- `BackButton.tsx`
- `ProgressBarWithBack.tsx`
- `FeedbackBanner.tsx`
- `ImagePlaceholder.tsx`
- `PricingCard.tsx`

**À créer** (si nécessaire) :
- `RadioButtonGroup.tsx` - Pour les écrans de sélection (langues, struggles, etc.)

---

## 📋 Checklist de Développement

### Phase 0 : Setup Initial
- [ ] Copier `/landing` → `/landing-v3`
  ```bash
  cp -r webapp-next/src/app/landing webapp-next/src/app/landing-v3
  ```
- [ ] Créer `contexts/LandingV3Context.tsx`
- [ ] Wrap `/landing-v3` avec `<LandingV3Provider>`
- [ ] Modifier routes internes (`router.push('/landing-v3/...')`)

**🧪 TEST #1 : Vérifier que la copie fonctionne**
- [ ] `npm run dev`
- [ ] Naviguer vers `http://localhost:3000/landing-v3`
- [ ] Vérifier que les écrans existants s'affichent (intro, magic, etc.)
- [ ] Vérifier que le Context est accessible (console.log dans un écran)

---

### Phase 1 : Section 1 - Questions de Langues (Écrans 2-3)
- [ ] Créer `/landing-v3/target-language/page.tsx`
  - [ ] Radio buttons (Portuguese, French)
  - [ ] Auto-navigation au clic
  - [ ] Sauvegarder dans Context `targetLanguage`

- [ ] Créer `/landing-v3/native-language/page.tsx`
  - [ ] Radio buttons (13 langues)
  - [ ] Auto-navigation au clic
  - [ ] Sauvegarder dans Context `nativeLanguage`

- [ ] Modifier `/landing-v3/page.tsx` (écran 1)
  - [ ] Bouton → `/landing-v3/target-language` (au lieu de `/intro`)

**🧪 TEST #2 : Navigation + Stockage Langues**
- [ ] Parcourir écrans 1 → 2 → 3
- [ ] Vérifier que les langues sont bien sauvegardées dans Context
- [ ] Vérifier l'auto-navigation (clic radio = next screen)
- [ ] Console.log `targetLanguage` et `nativeLanguage` sur écran 3

---

### Phase 2 : Section 1 - Écrans Personnalisés (Écrans 4-9)
- [ ] Modifier `/landing-v3/magic/page.tsx`
  - [ ] Texte dynamique avec `{targetLanguage}` et `{nativeLanguage}`
  - [ ] Bouton → `/landing-v3/vocab-level`

- [ ] Créer `/landing-v3/vocab-level/page.tsx`
- [ ] Créer `/landing-v3/frequency-list/page.tsx` (texte dynamique `{targetLanguage}`)
- [ ] Créer `/landing-v3/studies/page.tsx`
- [ ] Créer `/landing-v3/belief/page.tsx`
- [ ] Créer `/landing-v3/level-question/page.tsx`

**🧪 TEST #3 : Personnalisation Dynamique**
- [ ] Parcourir écrans 1 → 9
- [ ] Vérifier que `{targetLanguage}` et `{nativeLanguage}` s'affichent correctement
- [ ] Tester avec Portuguese + English
- [ ] Tester avec French + Spanish
- [ ] Vérifier que les textes sont fluides (pas de "undefined")

---

### Phase 3 : Section 1 - Vocab Test + Explications (Écrans 10-17)
- [ ] Modifier `/landing-v3/setup/vocab-intro/page.tsx`
  - [ ] Skip les questions de langues
  - [ ] Utiliser `targetLanguage` et `nativeLanguage` du Context

- [ ] Vérifier `/landing-v3/setup/vocab-test/page.tsx` (doit fonctionner tel quel)

- [ ] Créer `/landing-v3/setup/congrats/page.tsx`
  - [ ] Trouver l'icône fête dans `/onboarding`
  - [ ] Réutiliser la même image

- [ ] Modifier `/landing-v3/setup/chrome-extension/page.tsx`
  - [ ] Nouveau texte du wireframe
  - [ ] Même image que `/onboarding`

- [ ] Modifier `/landing-v3/setup/explanation-1/page.tsx`
  - [ ] Texte : "Only words you know" → `{targetLanguage}`
  - [ ] Vérifier ordre (c'est le 1er)

- [ ] Modifier `/landing-v3/setup/explanation-2/page.tsx`
  - [ ] Texte : "More than one word" → `{nativeLanguage}`
  - [ ] Vérifier ordre (c'est le 2ème)

- [ ] Modifier `/landing-v3/setup/explanation-3/page.tsx`
  - [ ] Texte : "Exactly one word" → inline translation
  - [ ] Vérifier ordre (c'est le 3ème)

- [ ] Créer `/landing-v3/setup/automatic-system/page.tsx`

**🧪 TEST #4 : Section 1 Complète**
- [ ] Parcourir écrans 1 → 17 (toute la section "How it works")
- [ ] Vérifier la barre de progression "How it works" (0% → 100%)
- [ ] Faire le vocab test complet
- [ ] Vérifier l'ordre des explanations (1. only words → 2. more than one → 3. exactly one)
- [ ] Vérifier que les textes dynamiques sont corrects

---

### Phase 4 : Transition + Section 2 (Écrans 18-22)
- [ ] Créer `/landing-v3/setup/reach-fluency/page.tsx`
  - [ ] ⚠️ **PAS de barre de progression** sur cet écran

- [ ] Modifier `/landing-v3/setup/layout.tsx`
  - [ ] Barre "Setting up Subly" commence à **50%**
  - [ ] Progresser de 50% → 100% sur écrans 19-24

- [ ] Créer `/landing-v3/setup/main-struggles/page.tsx`
  - [ ] Titre dynamique avec `{targetLanguage}`
  - [ ] Radio buttons + auto-navigation
  - [ ] Sauvegarder dans Context `mainStruggle`

- [ ] Créer `/landing-v3/setup/good-hands/page.tsx`
  - [ ] Texte dynamique avec `{mainStruggle}`

- [ ] Créer `/landing-v3/setup/learning-duration/page.tsx`
  - [ ] Titre dynamique avec `{targetLanguage}`
  - [ ] Radio buttons + auto-navigation

- [ ] Créer `/landing-v3/setup/study-frequency/page.tsx`
  - [ ] Titre dynamique avec `{targetLanguage}`
  - [ ] Radio buttons + auto-navigation

**🧪 TEST #5 : Transition + Section 2**
- [ ] Parcourir écrans 17 → 22
- [ ] Vérifier que l'écran 18 (reach-fluency) n'a PAS de barre
- [ ] Vérifier que la barre "Setting up Subly" **commence à 50%** (écran 19)
- [ ] Vérifier que la barre progresse bien (50% → ~90%)
- [ ] Tester les questions de qualification (struggles, duration, frequency)
- [ ] Vérifier que `{mainStruggle}` s'affiche correctement sur écran 20

---

### Phase 5 : Section 2 Fin + Section 3 (Écrans 23-24+)
- [ ] Vérifier `/landing-v3/setup/comparison/page.tsx` (doit être identique à `/landing`)
- [ ] Vérifier `/landing-v3/setup/auth/page.tsx` (doit être identique)
- [ ] Vérifier suite post-auth (pricing, etc.) - doit être identique

**🧪 TEST #6 : Section 2 Complète + Auth**
- [ ] Parcourir écrans 19 → 24 (auth)
- [ ] Vérifier la barre "Setting up Subly" (50% → 100%)
- [ ] Faire l'auth Google
- [ ] Vérifier que le flow post-auth fonctionne (pricing, etc.)

---

### Phase 6 : Test Final Bout en Bout
**🧪 TEST #7 : Flow Complet**
- [ ] Parcourir TOUT le flow de l'écran 1 → Complete
- [ ] Tester avec **Portuguese + English**
  - [ ] Vérifier tous les textes dynamiques
  - [ ] Faire le vocab test complet
  - [ ] Répondre aux questions de qualification
  - [ ] Aller jusqu'au pricing

- [ ] Tester avec **French + Spanish**
  - [ ] Vérifier que les textes changent bien
  - [ ] Refaire le flow complet

- [ ] Vérifier les 2 barres de progression
  - [ ] "How it works" : 0% → 100%
  - [ ] Écran transition sans barre
  - [ ] "Setting up Subly" : 50% → 100%

- [ ] Tester navigation arrière (BackButton)
  - [ ] Vérifier que le Context est préservé
  - [ ] Revenir de l'écran 10 → écran 4 → vérifier que les langues sont toujours là

- [ ] Tester sur mobile (responsive)
  - [ ] Images responsive
  - [ ] Boutons full-width sur mobile

---

### Phase 7 : Polissage Final
- [ ] Vérifier les textes des wireframes (copier exactement)
- [ ] Vérifier les assets (images, icônes)
- [ ] Vérifier les liens de navigation (aucun lien cassé)
- [ ] Vérifier les erreurs console (0 erreur)
- [ ] Vérifier l'accessibilité (contraste, alt text)
- [ ] Vérifier la performance (Lighthouse score)

**🧪 TEST #8 : Test Utilisateur Réel**
- [ ] Faire tester par une personne externe (famille/ami)
- [ ] Observer où elle bloque / hésite
- [ ] Noter les feedbacks UX
- [ ] Ajuster si nécessaire

---

## 🎨 Assets à Réutiliser

### Images de `/landing` (déjà existantes)
- `/landing/landing-hero-desktop.png` - Écran 1
- `/landing/landing-hero-mobile.png` - Écran 1
- `/landing/magic-demonstration.png` - Écran 4

### Images de `/onboarding` (à localiser)
- Icône fête 🎉 - Écran 12 (congrats)
- Image Chrome extension - Écran 13
- Images explanations (3 images) - Écrans 14-16

### Images de `/landing/comparison` (déjà existantes)
- Image comparaison Subly vs apps - Écran 23

---

## 📊 Métriques à Suivre (Post-Lancement)

Pour l'A/B testing, suivre dans Vercel Analytics :

**Conversion** :
- % qui complètent écran 9 (vocab test start)
- % qui complètent le vocab test
- % qui arrivent à l'auth (écran 24)
- % qui payent (pricing)

**Engagement** :
- Temps moyen par écran
- Taux de rebond par écran
- Écrans avec le plus de drop-off

**Comparaison** :
- `/landing` vs `/landing-v3`
- Taux de conversion final (signup + payment)

---

## 🚀 Déploiement

### Staging (Develop Branch)
1. Créer PR : `feature/landing-v3` → `develop`
2. Merge → auto-deploy sur `staging-subly-extension.vercel.app`
3. Tester sur staging : `https://staging-subly-extension.vercel.app/landing-v3`

### Production (Main Branch)
1. Créer PR : `develop` → `main`
2. Merge → auto-deploy sur `subly-extension.vercel.app`
3. Activer A/B testing :
   - 50% utilisateurs → `/landing` (contrôle)
   - 50% utilisateurs → `/landing-v3` (test)

### Rollback si Nécessaire
Si `/landing-v3` performe moins bien :
```bash
rm -rf webapp-next/src/app/landing-v3
git commit -m "Remove landing-v3 (A/B test completed)"
```

---

## 🎯 Next Steps Après A/B Test

**Si `/landing-v3` gagne** :
1. Renommer `/landing-v3` → `/landing`
2. Supprimer l'ancien `/landing`
3. Supprimer `/onboarding` (obsolète)

**Si `/landing` gagne** :
1. Supprimer `/landing-v3`
2. Garder `/landing` tel quel

**Si besoin d'itérer** :
- Créer `/landing-v4` avec les learnings de v3
- Recommencer l'A/B test

---

## ✅ Checklist Résumée

**Setup** : ✅ Copie + Context + Test initial
**Section 1** : ✅ Langues → Écrans personnalisés → Vocab test → Explanations
**Transition** : ✅ Pas de barre + Barre 50%
**Section 2** : ✅ Questions qualification → Comparison → Auth
**Section 3** : ✅ Suite identique
**Tests** : ✅ 8 tests intermédiaires stratégiques
**Déploiement** : ✅ Staging → Production → A/B test

---

**Temps estimé** : 1-2 jours de développement (si copie depuis `/landing`)
**Complexité** : Moyenne (personnalisation dynamique + double barre de progression)
**Risque** : Faible (isolation complète, aucun impact sur `/landing` existant)

🚀 **Prêt à commencer ?** Cocher la première case de Phase 0 !
