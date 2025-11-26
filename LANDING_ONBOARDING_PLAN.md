# Landing Onboarding Plan

**Date**: November 24, 2025
**Status**: ✅ Plan validated - Ready for implementation
**Goal**: Create a pre-download onboarding flow that educates users and captures payment BEFORE extension installation.

---

## 📋 Overview

### Current Flow (Chrome Web Store)
```
Chrome Web Store → Install Extension → background.ts opens /welcome
→ /onboarding/* (auth, languages, vocab test, pricing)
```

### New Flow (Marketing Funnel)
```
Marketing Link → /landing (discovery)
→ /landing/setup/* (configuration + vocab test)
→ /landing/auth (Google OAuth - creates Supabase account)
→ /landing/pricing (Stripe checkout - 3-day trial)
→ /landing/download (download extension link)
→ User installs extension → Already has account → Signs in manually
```

---

## 🎯 Goals & Strategy

### Business Goals
- **Reduce friction**: Users understand value BEFORE installing extension
- **Qualify leads**: Only paying users install extension (reduce support burden)
- **Mobile-first**: Capture mobile traffic (Instagram, TikTok) → Pay on mobile → Install on desktop
- **A/B testing**: Test different messaging/pricing without updating extension

### Technical Goals
- **Reuse existing code**: VocabTest, Stripe, Supabase, Shadcn UI components
- **Separate flows**: `/landing/*` vs `/onboarding/*` (no conflicts)
- **Responsive**: Works on mobile (375px) and desktop (1280px+)
- **Analytics**: Track drop-off at each step (Vercel Analytics already installed)
- **KISS principle**: Simple architecture, no over-engineering

---

## 📱 Complete Screen Flow (17 screens)

### Part 1: Discovery (7 screens) - "Discover how it works"
**Progress bar**: 7 steps, button text: "OK"
**Top label**: "Discover how it works"

1. **Landing Page** (`/landing`)
   - Layout: Image (Netflix screenshot) + Text side-by-side on desktop, stacked on mobile
   - Heading: "Netflix Subtitles Adapted to Your Level"
   - Button: "Discover how it works" (with arrow icon)
   - Image: Netflix screenshot with Subly in action (placeholder for now)

2. **Extension Intro** (`/landing/intro`)
   - Heading: "Subly is a Chrome extension"
   - Text: "A little tool that you can add to your Chrome browser on your desktop"
   - Images: Chrome icon + Subly icon (horizontal layout)
   - Button: "OK"

3. **Magic Explanation** (`/landing/magic`)
   - Heading: "Subly is magic"
   - Text: "When you watch Netflix, for each subtitle..."
   - (Explanation screen - see wireframe for full text)
   - Button: "OK"

4. **Known Words Visual** (`/landing/known-words`)
   - Heading: "If a subtitle contains only words that you know"
   - Visual: 3 colored subtitle boxes showing known/unknown words
   - Text: "Flash... Subly displays it in your target language"
   - Button: "OK"

5. **Explanation 4** (`/landing/explanation-4`)
   - (Another explanation screen with image - see wireframe)
   - Button: "OK"

6. **Explanation 5** (`/landing/explanation-5`)
   - (Another explanation screen - see wireframe)
   - Button: "OK"

7. **Comparison** (`/landing/comparison`)
   - Heading: "Subly vs Traditional Apps"
   - Visual: Graph/curve showing Subly advantage over traditional apps
   - Text: (See wireframe for details)
   - Button: "OK" → Navigates to Part 2

---

### Part 2: Setup (10+ screens) - "Setting Up Subly"
**Progress bar**: ~13 steps (variable due to vocab test), button text: "Continue"
**Top label**: "Setting Up Subly"
**Back button**: Active EXCEPT during vocab test

8. **Vocab Level Intro** (`/landing/setup/vocab-intro`)
   - Heading: "Know Your Vocabulary at the True Level"
   - Button: "Discover Your Level"
   - (Transition screen between Part 1 and Part 2)

9. **Target Language Selection** (`/landing/setup/target-language`)
   - Heading: "First, select your target language"
   - Radio buttons: Portuguese (BR), French
   - **Auto-navigation**: Click radio → 400ms delay → Navigate (no confirm button)
   - **Implementation**: Inline code in page (4 lines), no separate component/hook

10. **Explanation Pre-Test 1** (`/landing/setup/explanation-1`)
    - (Explanation screen before vocab test)
    - Button: "Continue"

11. **Explanation Pre-Test 2** (`/landing/setup/explanation-2`)
    - Text: "This will help us evaluate approximately how many of the most used words you know, which will be your vocabulary level"
    - Button: "Continue" → Starts vocab test

12-X. **Vocab Test Screens** (`/landing/setup/vocab-test`)
    - **Reuse existing VocabTestContext** from `/vocab-test/test/page.tsx`
    - Number of screens: Variable (depends on user answers, ~6-12 screens)
    - **Progress bar**: Frozen during test (doesn't advance)
    - **Back button**: HIDDEN during test
    - Last screen: "I don't know all the words" button

X+1. **Loading Analysis** (`/landing/setup/analyzing`)
    - Loading bar: "Analyzing your level..."
    - (Same as current onboarding)

X+2. **Results** (`/landing/setup/results`)
    - Heading: "Congrats, you know approximately [100] words"
    - Text: "Of the most used words in [Portuguese/French]"
    - Additional text explaining vocab level (see wireframe)
    - Button: "Continue"

X+3. **Finish Setup CTA** (`/landing/setup/finish-cta`)
    - Heading: "Finish setting up Subly"
    - Text: "You've done the hardest part! Now let's finalize your setup."
    - Button: "Finish setting up Subly"

X+4. **Native Language Selection** (`/landing/setup/native-language`)
    - Heading: "Select your native language"
    - Radio buttons: 13 languages (English, French, Spanish, German, etc.)
    - **Auto-navigation**: Click radio → 400ms delay → Navigate
    - **Implementation**: Inline code in page (4 lines), no separate component/hook

X+5. **Connect Google** (`/landing/setup/auth`)
    - Heading: "Now it's time to connect with Google"
    - Text: (See wireframe - slightly different from current onboarding)
    - Button: "Connect with Google" → Triggers Supabase OAuth
    - **Backend**: Creates Supabase account + saves `user_settings` (target_lang, native_lang, vocab_level)

X+6. **Post-Auth Screen** (`/landing/setup/post-auth`)
    - (Screen with image + text, see wireframe)
    - Button: "Continue"

X+7. **Reminder Email Info** (`/landing/setup/reminder`)
    - Heading: "We'll send you a reminder before your trial ends"
    - **Icon**: Mail icon with notification badge (1) - **INLINE** (5 lines, no separate component)
    - Text: "We'll send you an email 2 days before your trial ends to remind you that you'll be charged $9/year"
    - Button: "Continue"

X+8. **Pricing/Trial** (`/landing/setup/pricing`)
    - Heading: "Start your 3-day free trial"
    - **Timeline (3 points - vertical)** - **INLINE** (~30 lines, no separate component):
      - 📍 Day 0: Today - Start trial
      - 📍 Day 2: We'll send you a reminder
      - 📍 Day 3: First payment ($9/year)
    - Text: (See wireframe for full details)
    - Button: "Start My 3-Day Free Trial" → Stripe Checkout

X+9. **Stripe Checkout** (Stripe hosted page)
    - Standard Stripe checkout interface
    - Product: Subly Premium - $9/year
    - 3-day trial configured via `subscription_data.trial_period_days`

X+10. **All Set / Download** (`/landing/setup/complete`)
    - Heading: "You are all set!"
    - Text: "If you are on your computer, you can download the extension directly here: [Download Extension]"
    - Text: "Otherwise, we've sent you an email with the download link."
    - Link: `https://chrome.google.com/webstore/detail/lhkamocmjgjikhmfiogfdjhlhffoaaek`
    - Additional text: Instructions for installing extension (see wireframe)
    - **No device detection**: Same text shown on all devices (KISS)

---

## 🏗️ File Structure (Ultra-KISS)

### New Files to Create

```
webapp-next/src/
├── app/
│   └── landing/
│       ├── page.tsx                        # Landing page (screen 1)
│       ├── intro/page.tsx                  # Extension intro (screen 2)
│       ├── magic/page.tsx                  # Magic explanation (screen 3)
│       ├── known-words/page.tsx            # Visual explanation (screen 4)
│       ├── explanation-4/page.tsx          # Explanation 4 (screen 5)
│       ├── explanation-5/page.tsx          # Explanation 5 (screen 6)
│       ├── comparison/page.tsx             # Subly vs traditional (screen 7)
│       ├── layout.tsx                      # Part 1 layout with progress bar
│       └── setup/
│           ├── page.tsx                    # Redirect to vocab-intro
│           ├── vocab-intro/page.tsx        # Vocab intro (screen 8)
│           ├── target-language/page.tsx    # Target language (screen 9)
│           ├── explanation-1/page.tsx      # Pre-test explanation 1 (screen 10)
│           ├── explanation-2/page.tsx      # Pre-test explanation 2 (screen 11)
│           ├── vocab-test/page.tsx         # Vocab test (screens 12-X)
│           ├── analyzing/page.tsx          # Loading screen
│           ├── results/page.tsx            # Test results
│           ├── finish-cta/page.tsx         # Finish setup CTA
│           ├── native-language/page.tsx    # Native language selection
│           ├── auth/page.tsx               # Google OAuth
│           ├── post-auth/page.tsx          # Post-auth screen
│           ├── reminder/page.tsx           # Reminder email info
│           ├── pricing/page.tsx            # Pricing/trial timeline
│           ├── complete/page.tsx           # Download extension
│           └── layout.tsx                  # Part 2 layout with progress bar
│
├── contexts/
│   └── LandingContext.tsx                  # Landing flow state management
│
└── components/
    └── ProgressBarWithBack.tsx             # Reusable progress bar + back button

```

### Files to Reuse (No Changes)

```
webapp-next/src/
├── contexts/
│   ├── VocabTestContext.tsx               # ✅ Reuse for vocab test
│   └── AuthContext.tsx                    # ✅ Reuse for auth state
│
├── components/
│   ├── ui/                                # ✅ All Shadcn UI components
│   ├── BackButton.tsx                     # ✅ Reuse (used by ProgressBarWithBack)
│   ├── FeedbackBanner.tsx                 # ✅ Reuse at bottom
│   └── ImagePlaceholder.tsx               # ✅ Reuse for images
│
└── lib/
    └── supabase/                          # ✅ Reuse for auth + data

```

### Components Summary (Ultra-KISS)

**New components to create**: **1 only**
- `ProgressBarWithBack.tsx` - Reusable progress bar with back button (~30 lines)

**Inline code (no separate components)**:
- Radio auto-navigation: 4 lines x2 pages = 8 lines total
- Timeline 3 points: ~30 lines inline in pricing page
- Mail icon with badge: ~5 lines inline in reminder page

**Principle**: Don't create a component until it's used 2-3 times.

---

## 🎨 Design System

### Typography (Max 3 sizes per screen)

```css
/* Primary heading */
.heading-1 {
  font-size: 2rem;        /* 32px */
  font-weight: 600;
  line-height: 1.2;
}

/* Body text */
.body {
  font-size: 1rem;        /* 16px */
  font-weight: 400;
  line-height: 1.5;
}

/* Secondary/caption */
.caption {
  font-size: 0.875rem;    /* 14px */
  font-weight: 400;
  line-height: 1.4;
}
```

### Responsive Layout

**Desktop (>768px)**:
```css
.landing-container {
  max-width: 600px;       /* Centered content */
  margin: 0 auto;
  padding: 40px 24px;     /* Vertical + horizontal spacing */
}

.image-container {
  max-width: 400px;       /* Images not too wide */
  margin: 0 auto 24px;    /* Centered + bottom spacing */
}
```

**Mobile (<768px)**:
```css
.landing-container {
  padding: 24px 16px;     /* Reduced padding */
}

.image-container {
  max-width: 100%;        /* Full width (minus padding) */
}
```

**Exception - Screen 1 (Landing Page)**:
- Desktop: Image + text side-by-side (2-column grid)
- Mobile: Image on top, text below (stacked)

### Colors (Tailwind CSS v4)

Uses existing project theme:
- Primary: Default button color
- Muted: Background for secondary sections
- Foreground: Text color
- Border: Dividers and outlines

### Spacing

Consistent spacing scale (Tailwind):
- `gap-2` (8px) - Between small elements
- `gap-4` (16px) - Between sections
- `mb-8` (32px) - Between major sections
- `p-4` (16px) - Card padding
- `p-8` (32px) - Page padding

---

## 🔧 Technical Implementation

### Context Management (Simplified - KISS)

**LandingContext.tsx** (new):
```typescript
interface LandingContextType {
  // ✅ ONLY business data (no navigation state)
  targetLanguage: string | null
  nativeLanguage: string | null
  vocabLevel: number | null

  // Actions
  setTargetLanguage: (lang: string) => void
  setNativeLanguage: (lang: string) => void
  setVocabLevel: (level: number) => void
}

// ✅ Includes sessionStorage persistence (20 lines)
// - Save to sessionStorage on every change
// - Load from sessionStorage on mount
// - Clear sessionStorage after Supabase save
```

**Why simplified**:
- Navigation managed by Next.js Router (`router.push()`)
- Progress bars read `usePathname()` (like onboarding actuel)
- No manual step tracking (`discoveryStep`, `setupStep`)
- Result: Context 50% simpler, same behavior

**VocabTestContext** (reuse):
- Import from existing `/vocab-test` flow
- Same logic for dynamic test progression
- Saves to `vocab_levels` table on completion

**AuthContext** (reuse):
- Google OAuth via Supabase
- Session management
- Sign in/sign out

### sessionStorage Persistence (✅ ADDED)

**Why needed for landing flow** (different from onboarding actuel):

| Critère | Onboarding actuel | Landing flow (nouveau) |
|---------|-------------------|------------------------|
| Flow length | 5-7 screens (~5 min) | 17 screens (~10 min) |
| Device | Desktop only | Mobile + Desktop |
| Refresh risk | Low (desktop, few distractions) | **High** (mobile, auto-refresh on app switch) |
| Cost of data loss | Acceptable (restart 5 min) | **Unacceptable** (lose vocab test ~10 min) |

**Decision**: Add sessionStorage for landing flow (protects mobile users).

**Implementation**:
```typescript
// Save on every change
useEffect(() => {
  sessionStorage.setItem('landing_data', JSON.stringify({
    targetLanguage,
    nativeLanguage,
    vocabLevel
  }))
}, [targetLanguage, nativeLanguage, vocabLevel])

// Load on mount
useEffect(() => {
  const saved = sessionStorage.getItem('landing_data')
  if (saved) {
    const data = JSON.parse(saved)
    setTargetLanguage(data.targetLanguage)
    setNativeLanguage(data.nativeLanguage)
    setVocabLevel(data.vocabLevel)
  }
}, [])

// Clear after Supabase save (in pricing page)
sessionStorage.removeItem('landing_data')
```

**Cost**: +20 lines
**Benefit**: User can refresh without losing data (critical for mobile)

### Progress Bars (Simplified)

**ProgressBarWithBack.tsx** (one component for both parts):
```typescript
interface ProgressBarWithBackProps {
  progress: number           // 0-100
  showBackButton?: boolean   // Default true
  label?: string             // Optional top label
}
```

**Part 1 - Discovery (7 steps)**:
```typescript
// landing/layout.tsx
const pathname = usePathname()
const progress = getDiscoveryProgress(pathname)  // Simple map

<div>
  <p className="text-sm text-muted-foreground mb-2">Discover how it works</p>
  <ProgressBarWithBack progress={progress} />
</div>

function getDiscoveryProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing': 0,
    '/landing/intro': 14,
    '/landing/magic': 28,
    '/landing/known-words': 42,
    '/landing/explanation-4': 56,
    '/landing/explanation-5': 70,
    '/landing/comparison': 85,
  }
  return progressMap[pathname] ?? 0
}
```

**Part 2 - Setup (~13 steps, variable)**:
```typescript
// landing/setup/layout.tsx
const pathname = usePathname()
const progress = getSetupProgress(pathname)
const isVocabTest = pathname.includes('vocab-test')

<div>
  <p className="text-sm text-muted-foreground mb-2">Setting Up Subly</p>
  <ProgressBarWithBack progress={progress} showBackButton={!isVocabTest} />
</div>

function getSetupProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing/setup/vocab-intro': 7,
    '/landing/setup/target-language': 14,
    '/landing/setup/explanation-1': 21,
    '/landing/setup/explanation-2': 28,
    '/landing/setup/vocab-test': 35,      // Frozen during test
    '/landing/setup/analyzing': 42,
    '/landing/setup/results': 49,
    '/landing/setup/finish-cta': 56,
    '/landing/setup/native-language': 63,
    '/landing/setup/auth': 70,
    '/landing/setup/post-auth': 77,
    '/landing/setup/reminder': 84,
    '/landing/setup/pricing': 91,
    '/landing/setup/complete': 100,
  }
  return progressMap[pathname] ?? 0
}
```

**Back Button Behavior**:
- Active by default
- Hidden during vocab test (`showBackButton={!isVocabTest}`)
- Uses `router.back()` (browser history)

### Radio Auto-Navigation (Inline)

**No separate component/hook** - inline code in 2 pages:

```typescript
// target-language/page.tsx
const [selected, setSelected] = useState<string | null>(null)
const router = useRouter()

const handleSelect = (value: string) => {
  setSelected(value)
  setTimeout(() => router.push('/landing/setup/explanation-1'), 400)
}

<RadioGroup value={selected} onValueChange={handleSelect}>
  <RadioGroupItem value="pt-BR">Portuguese (BR)</RadioGroupItem>
  <RadioGroupItem value="fr">French</RadioGroupItem>
</RadioGroup>
```

**Same pattern in native-language/page.tsx** (4 lines duplicated).

**Principle**: Wait for 3rd usage before creating hook/component.

### Backend Integration

**Google OAuth Flow**:
```typescript
// /landing/setup/auth/page.tsx
const handleGoogleSignIn = async () => {
  const supabase = createClient()

  await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_APP_URL}/landing/setup/post-auth`,
    }
  })
}
```

**Save to Supabase (after OAuth)**:
```typescript
// /landing/setup/pricing/page.tsx (or post-auth)
useEffect(() => {
  const saveToSupabase = async () => {
    if (!user || !targetLanguage || !nativeLanguage || !vocabLevel) return

    // Save user_settings
    await supabase.from('user_settings').upsert({
      user_id: user.id,
      target_lang: targetLanguage,
      native_lang: nativeLanguage,
    })

    // Save vocab_levels
    await supabase.from('vocab_levels').upsert({
      user_id: user.id,
      language: targetLanguage,
      level: vocabLevel,
      tested_at: new Date().toISOString(),
    })

    // Clean sessionStorage (no longer needed)
    sessionStorage.removeItem('landing_data')
  }

  saveToSupabase()
}, [user, targetLanguage, nativeLanguage, vocabLevel])
```

**Stripe Checkout**:
```typescript
// /landing/setup/pricing/page.tsx
const handleCheckout = async () => {
  const response = await fetch('/api/stripe/checkout', {
    method: 'POST',
    body: JSON.stringify({
      userId: user.id,
      email: user.email,
      successUrl: `${window.location.origin}/landing/setup/complete`,
      cancelUrl: `${window.location.origin}/landing/setup/pricing`,
    }),
  })

  const { url } = await response.json()
  window.location.href = url
}
```

**Extension Download Link**:
```typescript
// /landing/setup/complete/page.tsx
const CHROME_WEB_STORE_URL =
  'https://chrome.google.com/webstore/detail/lhkamocmjgjikhmfiogfdjhlhffoaaek'

<a
  href={CHROME_WEB_STORE_URL}
  target="_blank"
  rel="noopener noreferrer"
  className="text-blue-500 underline"
>
  Download Subly Extension
</a>
```

---

## 📊 Analytics Tracking

**Vercel Analytics** (already installed):
```typescript
import { track } from '@vercel/analytics'

// Track screen views
useEffect(() => {
  track('landing_screen_viewed', {
    screen: 'target_language',
    part: 'setup',
    step: 2,
  })
}, [])

// Track user actions
const handleLanguageSelect = (language: string) => {
  track('language_selected', {
    type: 'target',
    language,
  })
  // ... rest of logic
}
```

**Key Events to Track**:
- `landing_started` - User lands on `/landing`
- `discovery_completed` - User finishes Part 1
- `vocab_test_started` - User starts vocab test
- `vocab_test_completed` - User finishes vocab test
- `auth_completed` - User connects Google account
- `checkout_started` - User clicks "Start trial" button
- `checkout_completed` - Stripe checkout success
- `extension_download_clicked` - User clicks download link

**Funnel Analysis**:
```
Landing (100%)
  → Intro (X%)
  → Target Language (X%)
  → Vocab Test (X%)
  → Auth (X%)
  → Checkout (X%)
  → Download (X%)
```

View in Vercel Dashboard → Analytics → Custom Events

---

## ⚙️ Backend Requirements

### Supabase Schema (Existing - No Changes)

**user_settings**:
```sql
CREATE TABLE user_settings (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id),
  target_lang TEXT NOT NULL,
  native_lang TEXT NOT NULL,
  subscription_status TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**vocab_levels**:
```sql
CREATE TABLE vocab_levels (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  language TEXT NOT NULL,
  level INTEGER NOT NULL,
  tested_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, language)
);
```

### Stripe Configuration

**Product**: Subly Premium
**Price**: $9/year
**Trial**: 3 days (configured in code via `subscription_data.trial_period_days`)

**Staging (TEST mode)**:
- Product ID: `prod_xxx`
- Price ID: `price_1SScLTCpd12v3sCmb1baxznb`
- Webhook: `https://staging-subly-extension.vercel.app/api/stripe/webhook`

**Production (LIVE mode)**:
- Product ID: `prod_yyy` (separate from TEST)
- Price ID: `price_xxx` (separate from TEST)
- Webhook: `https://subly-extension.vercel.app/api/stripe/webhook`

**Webhook Events**:
- `checkout.session.completed` - User completes payment
- `customer.subscription.created` - Subscription created
- `customer.subscription.updated` - Subscription changed
- `customer.subscription.deleted` - Subscription canceled

### Email System (Future - Phase 3)

**MVP**: Stripe Native Emails
- Stripe sends default receipts
- Customize logo/colors in Stripe Dashboard
- Includes trial reminder emails automatically
- Zero code required

**Future**: Resend Custom Emails (if needed)
- Custom branding
- Personalized download links
- Setup: 10 minutes, free tier: 100 emails/day

---

## 🚀 Implementation Plan (avec tests intermédiaires)

### Phase 1: Frontend Shell (4-5 hours)

**Goal**: Build complete UI skeleton with navigation, no backend logic.

---

#### Step 1.1: Setup Structure (30 min)
- [ ] Create `/app/landing` directory structure
- [ ] Create `/app/landing/setup` subdirectory
- [ ] Create `LandingContext.tsx` with sessionStorage (~80 lines)
- [ ] Create layout files (`landing/layout.tsx`, `setup/layout.tsx`)

**🧪 TEST CHECKPOINT 1.1** (5 min):
```bash
# Start dev server
cd webapp-next && npm run dev

# Tests to perform:
✓ Navigate to http://localhost:3000/landing
✓ Check console: no errors related to LandingContext
✓ Open React DevTools → Components → Look for LandingProvider
✓ Verify Context provides: targetLanguage, nativeLanguage, vocabLevel (all null)
```

**Expected result**: Page loads without errors, Context is accessible.

---

#### Step 1.2: Shared Component (30 min)
- [ ] Create `ProgressBarWithBack.tsx` (progress bar + back button, ~30 lines)
- [ ] Wire up in `landing/layout.tsx` with mock progress (50%)

**🧪 TEST CHECKPOINT 1.2** (5 min):
```bash
# Tests to perform:
✓ Refresh http://localhost:3000/landing
✓ Verify progress bar appears at top (50% filled)
✓ Verify back button appears (arrow icon)
✓ Click back button → Check console for navigation attempt
✓ Inspect with browser DevTools → Progress bar should be Shadcn UI <Progress>
```

**Expected result**: Progress bar displays correctly, back button clickable.

---

#### Step 1.3: Part 1 - Discovery Screens (1.5 hours)
- [ ] `/landing/page.tsx` - Landing page (image + text side-by-side)
- [ ] `/landing/intro/page.tsx` - Extension intro
- [ ] `/landing/magic/page.tsx` - Magic explanation

**🧪 TEST CHECKPOINT 1.3a** (5 min) - After first 3 screens:
```bash
# Tests to perform:
✓ Navigate to http://localhost:3000/landing
✓ Click "Discover how it works" → Should navigate to /landing/intro
✓ Click "OK" → Should navigate to /landing/magic
✓ Click "OK" → Should navigate to next screen
✓ Click back button → Should go back to previous screen
✓ Check progress bar updates (0% → 14% → 28%)
```

**Expected result**: Navigation works, progress bar updates.

- [ ] `/landing/known-words/page.tsx` - Visual explanation
- [ ] `/landing/explanation-4/page.tsx` - Explanation 4
- [ ] `/landing/explanation-5/page.tsx` - Explanation 5
- [ ] `/landing/comparison/page.tsx` - Subly vs traditional

**🧪 TEST CHECKPOINT 1.3b** (5 min) - After all 7 screens:
```bash
# Tests to perform:
✓ Navigate through all 7 screens: /landing → /landing/intro → ... → /landing/comparison
✓ Verify progress bar progression: 0% → 14% → 28% → 42% → 56% → 70% → 85%
✓ Click back button on each screen → Verify it goes to previous screen
✓ On /landing/comparison, click "OK" → Should navigate to /landing/setup/vocab-intro
✓ Verify label above progress bar says "Discover how it works"
```

**Expected result**: All 7 screens work, navigation smooth, progress bar accurate.

---

#### Step 1.4: Part 2 - Setup Screens (2 hours)

**Batch 1: Vocab flow (4 pages)**
- [ ] `/landing/setup/vocab-intro/page.tsx` - Vocab intro
- [ ] `/landing/setup/target-language/page.tsx` - Target language (radio auto-nav inline)
- [ ] `/landing/setup/explanation-1/page.tsx` - Pre-test explanation 1
- [ ] `/landing/setup/explanation-2/page.tsx` - Pre-test explanation 2

**🧪 TEST CHECKPOINT 1.4a** (5 min) - After Batch 1:
```bash
# Tests to perform:
✓ Navigate to http://localhost:3000/landing/setup/vocab-intro
✓ Click "Discover Your Level" → Navigate to target-language
✓ Click Portuguese radio button → Wait 400ms → Auto-navigate to explanation-1
✓ Verify: console.log shows "Selected: pt-BR" (from LandingContext)
✓ Click "Continue" → Navigate to explanation-2
✓ Verify progress bar label changed to "Setting Up Subly"
✓ Verify progress updates: 7% → 14% → 21% → 28%
✓ Click back button → Verify it works
```

**Expected result**: Radio auto-nav works (400ms delay), Context updates, progress bar accurate.

**Batch 2: Test & Results (3 pages)**
- [ ] `/landing/setup/vocab-test/page.tsx` - Vocab test placeholder (mock screen)
- [ ] `/landing/setup/analyzing/page.tsx` - Loading screen
- [ ] `/landing/setup/results/page.tsx` - Test results

**🧪 TEST CHECKPOINT 1.4b** (5 min) - After Batch 2:
```bash
# Tests to perform:
✓ Navigate to /landing/setup/vocab-test
✓ Verify back button is HIDDEN (important!)
✓ Click "Mock: Complete Test" → Navigate to analyzing
✓ Wait 2 seconds → Auto-navigate to results
✓ Verify results page shows vocab level from Context (mock: 1000)
✓ Click back button on results page → Verify it works now
```

**Expected result**: Back button hidden during test, auto-navigation works, Context stores vocab level.

**Batch 3: Auth & Payment (7 pages)**
- [ ] `/landing/setup/finish-cta/page.tsx` - Finish setup CTA
- [ ] `/landing/setup/native-language/page.tsx` - Native language (radio auto-nav inline)
- [ ] `/landing/setup/auth/page.tsx` - Google OAuth placeholder
- [ ] `/landing/setup/post-auth/page.tsx` - Post-auth screen
- [ ] `/landing/setup/reminder/page.tsx` - Reminder email info (mail icon inline)
- [ ] `/landing/setup/pricing/page.tsx` - Pricing timeline (3 points inline)
- [ ] `/landing/setup/complete/page.tsx` - Download extension

**🧪 TEST CHECKPOINT 1.4c** (10 min) - After Batch 3:
```bash
# Tests to perform:
✓ Navigate to /landing/setup/finish-cta → Click "Finish setting up"
✓ On native-language: Click English radio → Wait 400ms → Auto-navigate
✓ Verify Context: nativeLanguage = "en"
✓ On auth page: Click "Mock: Sign in with Google" → Navigate to post-auth
✓ On reminder page: Verify mail icon with badge (1) displays
✓ On pricing page: Verify 3-point timeline displays (Day 0, Day 2, Day 3)
✓ Click "Start trial" → Navigate to complete
✓ On complete page: Verify download link displays
✓ Progress bar: 56% → 63% → 70% → 77% → 84% → 91% → 100%
```

**Expected result**: All screens work, timeline displays correctly, progress reaches 100%.

---

#### Step 1.5: sessionStorage Testing (30 min)

**🧪 TEST CHECKPOINT 1.5** (15 min) - sessionStorage persistence:
```bash
# Tests to perform:
✓ Navigate to /landing
✓ Click through to /landing/setup/target-language
✓ Select Portuguese → Auto-navigate
✓ Open DevTools → Application → Session Storage → Check "landing_data"
✓ Verify: { targetLanguage: "pt-BR", nativeLanguage: null, vocabLevel: null }
✓ Continue to native-language page → Select English
✓ Refresh page → Check sessionStorage still contains data
✓ Verify Context restored: targetLanguage = "pt-BR", nativeLanguage = "en"
✓ Continue navigation → Verify data persists through refreshes
```

**Expected result**: sessionStorage saves/loads correctly, data persists through refreshes.

**🧪 TEST CHECKPOINT 1.5b** (10 min) - Full flow test:
```bash
# Complete end-to-end navigation test:
✓ Start at /landing
✓ Click through ALL 17 screens (use "OK"/"Continue" buttons)
✓ Verify NO errors in console
✓ Verify progress bar reaches 100% at /landing/setup/complete
✓ Click back button multiple times → Verify it navigates backwards correctly
✓ Verify back button was hidden during vocab test page
✓ Check sessionStorage contains final state:
  { targetLanguage: "pt-BR", nativeLanguage: "en", vocabLevel: 1000 }
```

**Expected result**: Complete flow works end-to-end, no console errors, sessionStorage correct.

**Deliverable**: Complete UI flow with navigation and sessionStorage persistence. ✅ All tests passed.

---

### Phase 2: Design & Responsive (2-3 hours)

**Goal**: Polish design, ensure mobile/desktop responsive, add animations.

---

#### Step 2.1: Typography & Spacing (30 min)
- [ ] Apply 3-size typography system (heading 32px, body 16px, caption 14px)
- [ ] Verify max 2-3 font sizes per screen
- [ ] Apply consistent spacing (gap-2, gap-4, mb-8, p-4, p-8)

**🧪 TEST CHECKPOINT 2.1** (5 min):
```bash
# Tests to perform:
✓ Open any 3 screens (e.g., /landing, /landing/intro, /landing/setup/vocab-intro)
✓ Use browser DevTools → Inspect text elements
✓ Verify only 2-3 font sizes per screen (32px, 16px, 14px)
✓ Check spacing between elements: consistent gap-4 (16px) or mb-8 (32px)
✓ Test readability: text should be clear, not cramped
```

**Expected result**: Typography consistent across all screens, spacing uniform.

---

#### Step 2.2: Responsive Layout (1 hour)
- [ ] Landing page: Image + text side-by-side (desktop), stacked (mobile)
- [ ] All other screens: Centered content, max-width 600px
- [ ] Images: Full width (minus padding), max-width 400px

**🧪 TEST CHECKPOINT 2.2** (10 min):
```bash
# Desktop test (1280px+):
✓ Navigate to /landing → Verify image + text side-by-side
✓ Navigate to /landing/intro → Verify content centered, max-width 600px
✓ Check images: should be max 400px wide, centered
✓ Check margins: 24px left/right padding visible

# Mobile test (375px):
✓ Open Chrome DevTools → Toggle device toolbar → iPhone SE (375px)
✓ Navigate to /landing → Verify image stacked above text (not side-by-side)
✓ Check images: should be full-width minus 16px padding (343px)
✓ Check text: should wrap properly, readable
✓ Scroll through 5-6 screens → Verify all responsive
```

**Expected result**: Desktop layout side-by-side, mobile layout stacked, all text readable.

---

#### Step 2.3: Animations & Transitions (1 hour)
- [ ] Radio auto-nav: 400ms delay with checkmark animation
- [ ] Button hover states
- [ ] Page transitions (fade-in)
- [ ] Progress bar smooth animation
- [ ] Loading spinner (analyzing screen)

**🧪 TEST CHECKPOINT 2.3** (10 min):
```bash
# Animation tests:
✓ Navigate to /landing/setup/target-language
✓ Click Portuguese radio → Verify checkmark appears (animation)
✓ Wait 400ms → Verify smooth navigation to next screen
✓ Hover over any button → Verify hover effect (color change/shadow)
✓ Navigate between screens → Verify smooth fade-in transition
✓ Check progress bar → Verify smooth animation (not instant jump)
✓ Navigate to /landing/setup/analyzing → Verify loading spinner spins

# Performance check:
✓ Open DevTools → Performance tab → Record navigation
✓ Verify animations run at 60fps (no jank)
✓ Check page load time: should be <500ms
```

**Expected result**: All animations smooth (60fps), no janky transitions, loading spinner visible.

**Deliverable**: Polished, responsive UI with smooth animations. ✅ All tests passed.

---

### Phase 3: Backend Integration (2-3 hours) - ✅ UPDATED

**Goal**: Connect frontend to Supabase, VocabTest, Stripe by **reusing onboarding code**.

**Strategy**: Copier-coller du code de l'onboarding actuel + adapter pour le landing flow.

---

#### Step 3.1: VocabTest Integration (15 min)
- [ ] **Copy** `/app/onboarding/vocab-test/page.tsx` → `/app/landing/setup/vocab-test/page.tsx`
- [ ] Replace `useOnboarding()` with `useLanding()`
- [ ] Update navigation routes: `/onboarding/` → `/landing/setup/`
- [ ] No changes needed for back button/progress bar (already managed by layout)

**🧪 TEST CHECKPOINT 3.1** (5 min - Localhost):
```bash
# VocabTest integration tests:
✓ Navigate to http://localhost:3000/landing/setup/vocab-test?level=100
✓ Verify: Real vocab test UI loads (PT/FR word lists)
✓ Answer 2-3 questions → Click "I don't know all the words"
✓ Wait 3 seconds (loading) → Navigate to /landing/setup/results
✓ Verify: Results page shows vocab level from Context
✓ Check browser console: vocabLevel should be logged
✓ Check sessionStorage: landing_data contains vocabLevel
```

**Expected result**: Real vocab test works, navigation correct, data saved.

---

#### Step 3.2: Google OAuth (30 min) - **Option A (Flexible)**
- [ ] **Modify** `AuthContext.signInWithGoogle()` to accept optional `redirectTo` parameter
- [ ] **Copy** `/app/onboarding/auth/page.tsx` → `/app/landing/setup/auth/page.tsx`
- [ ] Call `signInWithGoogle('/auth/callback?redirect=/landing/setup/post-auth')`
- [ ] **Modify** `/app/auth/callback/route.ts` to read `redirect` param and use it
- [ ] Handle auth errors gracefully (already in AuthContext)

**🧪 TEST CHECKPOINT 3.2a** (5 min - Localhost):
```bash
# Landing OAuth flow:
✓ Navigate to http://localhost:3000/landing/setup/auth
✓ Click "Connect with Google" button
✓ Complete Google OAuth
✓ Verify: Redirects back to /landing/setup/post-auth (not /onboarding/languages)
✓ Open React DevTools → Check AuthContext → user object exists
✓ Check browser console: No errors
```

**🧪 TEST CHECKPOINT 3.2b** (10 min - **Staging - CRITICAL**):
```bash
# REGRESSION TEST - Onboarding actuel NE DOIT PAS CASSER:
✓ Navigate to https://staging-subly-extension.vercel.app/onboarding/auth
✓ Click "Connect with Google"
✓ Complete Google OAuth
✓ Verify: Redirects to /onboarding/languages (NOT /landing/*)
✓ Verify: Onboarding flow still works end-to-end
✓ Check browser console: No errors
```

**Expected result**: Landing OAuth works + Onboarding actuel intact.

---

#### Step 3.3: Supabase Data Persistence (20 min)
- [ ] **Copy** useEffect logic from `/app/onboarding/pricing-intro/page.tsx`
- [ ] **Paste** into `/app/landing/setup/post-auth/page.tsx` (or pricing page)
- [ ] Replace `useOnboarding()` with `useLanding()`
- [ ] Change sessionStorage key: `'onboarding_data'` → `'landing_data'`
- [ ] UPSERT logic already handles duplicates (no changes needed)

**🧪 TEST CHECKPOINT 3.3** (10 min - Localhost):
```bash
# Data persistence tests:
✓ Complete landing flow: target lang → vocab test → native lang → auth → post-auth
✓ Wait 2-3 seconds (useEffect runs)
✓ Open Supabase Dashboard → Auth → Users → Find test user
✓ Navigate to: Table Editor → user_settings
✓ Verify: Row exists with correct target_lang, native_lang
✓ Navigate to: Table Editor → vocab_levels
✓ Verify: Row exists with correct language, level, tested_at
✓ Check browser DevTools → Application → Session Storage
✓ Verify: landing_data is DELETED (cleared after save)
✓ Check browser console: "✅ Saved to Supabase + cleaned sessionStorage"

# UPSERT test:
✓ Repeat auth with same Google account
✓ Verify: No duplicate rows (UPSERT works)
```

**Expected result**: Data saved correctly, sessionStorage cleared, no duplicates.

---

#### Step 3.4: Stripe Checkout (45 min) - **Option A (Flexible + Secure)**

**Backend (API modification):**
- [ ] **Modify** `/app/api/stripe/checkout/route.ts` to accept `successUrl` and `cancelUrl` in request body
- [ ] **Add validation**: Only allow URLs matching `/onboarding/*` or `/landing/*` (whitelist)
- [ ] **Reject** any other URLs (security)
- [ ] **Fallback** to default onboarding URLs if not provided (backward compatibility)

**Frontend (Landing page):**
- [ ] **Copy** `handleCheckout` from `/app/onboarding/pricing-details/page.tsx`
- [ ] **Paste** into `/app/landing/setup/pricing/page.tsx`
- [ ] **Add** `successUrl: '/landing/setup/complete'` and `cancelUrl: '/landing/setup/pricing'` to request body

**🧪 TEST CHECKPOINT 3.4a** (10 min - Localhost):
```bash
# Landing Stripe checkout:
✓ Navigate to http://localhost:3000/landing/setup/pricing
✓ Click "Start My 3-Day Free Trial"
✓ Verify: Redirects to Stripe Checkout (stripe.com)
✓ Fill test card: 4242 4242 4242 4242, exp: 12/34, CVC: 123
✓ Click "Subscribe"
✓ Verify: Redirects to /landing/setup/complete (NOT /onboarding/complete)
✓ Check browser console: No errors

# Cancel test:
✓ Click "Start trial" again → Click browser back button during Stripe
✓ Verify: Redirects to /landing/setup/pricing
```

**🧪 TEST CHECKPOINT 3.4b** (15 min - **Staging - CRITICAL**):
```bash
# REGRESSION TEST - Onboarding Stripe NE DOIT PAS CASSER:
✓ Navigate to https://staging-subly-extension.vercel.app/onboarding/pricing-details
✓ Click "Start My 3-Day Free Trial"
✓ Complete Stripe checkout with test card
✓ Verify: Redirects to /onboarding/complete (NOT /landing/*)
✓ Check Stripe Dashboard → Payment successful
✓ Check Stripe Dashboard → Webhooks → 200 OK
✓ Check Supabase → user_settings → subscription_status updated
✓ Verify: Onboarding Stripe flow still works perfectly
```

**🧪 TEST CHECKPOINT 3.4c** (5 min - Localhost Security):
```bash
# Security validation test:
✓ Modify request body to send successUrl: 'https://evil.com'
✓ Verify: API returns 400 error "Invalid URL"
✓ Check console: "URL must start with /onboarding/ or /landing/"
✓ Retry with valid URL (/landing/setup/complete) → Works
```

**Expected result**: Landing Stripe works + Onboarding Stripe intact + Security validation active.

---

#### Step 3.5: Analytics Tracking (30 min)
- [ ] Add `track()` calls for key events (landing_started, discovery_completed, etc.)

**🧪 TEST CHECKPOINT 3.5** (10 min):
```bash
# Analytics tests:
✓ Open Vercel Dashboard → Select project → Analytics tab
✓ Complete full flow: /landing → ... → /landing/setup/complete
✓ Wait 2 minutes (analytics delay)
✓ Refresh Vercel Analytics dashboard
✓ Verify custom events appear:
  - landing_started
  - discovery_completed (after /landing/comparison)
  - vocab_test_started
  - vocab_test_completed
  - auth_completed
  - checkout_started
  - checkout_completed (after Stripe success)
  - extension_download_clicked
✓ Check funnel: Verify event sequence correct
✓ Check console: Verify track() calls logged (if in dev mode)
```

**Expected result**: All events tracked in Vercel Analytics, funnel visible.

**Deliverable**: Fully functional landing flow with backend integration. ✅ All tests passed (localhost + staging regression tests).

**⚠️ CRITICAL**: Phase 3 modifies shared code (AuthContext + Stripe API). **Staging tests mandatory** before production.

---

### Phase 4: Testing & Polish (2-3 hours) - ✅ ALREADY DONE

**Status**: Phase 4.1 (Real Images) already completed during Phase 1. Phase 4.2-4.3 will be done during Phase 5 staging tests.

**Goal**: Test all flows, fix bugs, add real images.

#### Step 4.1: Real Images (30 min)
- [ ] Replace placeholder images with real images (provided by user)
- [ ] Optimize images (max 200KB per image)
- [ ] Test image loading on slow connection (Chrome DevTools Network throttling)

#### Step 4.2: End-to-End Testing (1.5 hours)
- [ ] Test full flow on staging: Landing → Discovery → Setup → Auth → Checkout → Download
- [ ] Test mobile flow: Pay on mobile, download link works on desktop
- [ ] Test sessionStorage: Refresh at various steps, data persists
- [ ] Test edge cases:
  - [ ] User closes tab mid-onboarding (sessionStorage persists)
  - [ ] User clicks back button during vocab test (button hidden)
  - [ ] User clicks back button after auth (works)
  - [ ] User cancels Stripe checkout (redirect to pricing)
  - [ ] User completes checkout twice (idempotency)

#### Step 4.3: Bug Fixes & Polish (1 hour)
- [ ] Fix any bugs found during testing
- [ ] Polish animations/transitions
- [ ] Verify typography consistency
- [ ] Verify responsive layout on real devices

**Deliverable**: Production-ready landing flow.

---

### Phase 5: Deployment (1.5 hours) - ✅ UPDATED WORKFLOW

**Goal**: Deploy to staging (regression tests), then production.

**Workflow**: Localhost → Staging (CRITICAL) → Production

---

#### Step 5.1: Staging Deployment & Regression Tests (45 min) - **MANDATORY**

**Why staging is mandatory**:
- We modified **shared code** (AuthContext + Stripe API)
- Onboarding actuel must continue to work
- Regression tests required before production

**Deployment**:
- [ ] Push Phase 3 code to `develop` branch
- [ ] Verify auto-deploy to `staging-subly-extension.vercel.app`
- [ ] Wait 2-3 minutes for deployment to complete

**🧪 REGRESSION TESTS (CRITICAL - 30 min)**:
```bash
# Test 1: Onboarding actuel - OAuth
✓ Navigate to https://staging-subly-extension.vercel.app/onboarding/auth
✓ Complete Google OAuth
✓ Verify: Redirects to /onboarding/languages (NOT /landing/*)
✓ Complete full onboarding flow → No errors

# Test 2: Onboarding actuel - Stripe
✓ Navigate to https://staging-subly-extension.vercel.app/onboarding/pricing-details
✓ Complete Stripe checkout
✓ Verify: Redirects to /onboarding/complete (NOT /landing/*)
✓ Check Stripe Dashboard → Payment successful, webhooks 200 OK

# Test 3: Landing flow - Full E2E
✓ Navigate to https://staging-subly-extension.vercel.app/landing
✓ Complete full flow: Discovery → Setup → Auth → Stripe → Complete
✓ Verify: All redirects correct (/landing/* not /onboarding/*)
✓ Check Supabase: Data saved correctly
✓ Check Stripe: Payment successful

# Test 4: Edge cases
✓ Cancel Stripe checkout → Redirects to correct cancel URL
✓ Refresh during flow → sessionStorage persists
✓ Back button works correctly (hidden during vocab test)
```

**Expected result**: ✅ Onboarding actuel 100% intact + Landing flow works perfectly.

**If regression tests fail**: ❌ DO NOT MERGE TO PRODUCTION. Fix issues first.

---

#### Step 5.2: Production Deployment (30 min)

**Pre-deployment checklist**:
- [ ] ✅ All staging regression tests passed
- [ ] ✅ User approval obtained
- [ ] ✅ No errors in staging logs

**Deployment**:
- [ ] Merge `develop` → `main` via GitHub PR
- [ ] Add PR description: "Landing flow Phase 3 - Backend integration (AuthContext + Stripe modified)"
- [ ] Verify auto-deploy to `subly-extension.vercel.app`
- [ ] Wait 2-3 minutes for deployment

**🧪 PRODUCTION SMOKE TESTS (15 min)**:
```bash
# Quick sanity checks (not full regression):
✓ Navigate to https://subly-extension.vercel.app/onboarding/auth
✓ Test OAuth → Verify works
✓ Navigate to https://subly-extension.vercel.app/landing
✓ Test landing flow → Verify works
✓ Check Vercel logs → No errors
```

**Post-deployment monitoring**:
- [ ] Monitor Vercel logs for 1 hour
- [ ] Check Sentry/error tracking (if installed)
- [ ] Monitor Stripe webhooks dashboard

**Deliverable**: Landing flow live in production + Onboarding actuel intact.

---

## 🎯 Phase 3 Architecture Decisions (November 25, 2025)

### Summary of Decisions

| Decision | Option Chosen | Rationale |
|----------|--------------|-----------|
| **OAuth Redirect** | Option A: Parameterized `redirectTo` in AuthContext | Scalable for future A/B testing (3+ onboarding flows expected) |
| **Stripe URLs** | Option A: URLs as parameters with validation | Same rationale + security via whitelist |
| **Deployment** | Localhost → Staging (regression tests) → Production | Modified shared code requires staging validation |

---

### OAuth - Option A (Flexible)

**Implementation**:
- Modify `AuthContext.signInWithGoogle()` to accept optional `redirectTo` parameter
- Modify `/app/auth/callback/route.ts` to read `redirect` URL param and use it for final redirect
- Each page specifies where to redirect after OAuth

**Advantages**:
- ✅ **Scalable**: Support for unlimited future flows (A/B testing onboardings)
- ✅ **Explicit**: Each flow controls its own redirect path
- ✅ **DRY**: No code duplication across flows

**Trade-offs**:
- ⚠️ **Shared code modification**: Requires regression testing of onboarding actuel
- ⚠️ **Backward compatibility**: Must work for both landing and existing onboarding

**Alternative rejected (Option B - URL detection)**:
- Less scalable (callback becomes giant switch/case with many flows)
- Implicit behavior harder to debug

---

### Stripe - Option A (Flexible + Secure)

**Implementation**:
- Modify `/app/api/stripe/checkout/route.ts` to accept `successUrl` and `cancelUrl` in request body
- Add validation: **Whitelist** URLs matching `/onboarding/*` or `/landing/*`
- Reject any URLs outside whitelist (security)
- Fallback to default onboarding URLs if not provided (backward compatibility)

**Security validation** (10 lines):
```typescript
const isValidUrl = (url: string) => {
  return url.startsWith('/onboarding/') || url.startsWith('/landing/')
}

if (successUrl && !isValidUrl(successUrl)) {
  return Response.json({ error: 'Invalid successUrl' }, { status: 400 })
}
```

**Advantages**:
- ✅ **Scalable**: Support for unlimited future flows
- ✅ **Explicit**: Each page controls redirect behavior
- ✅ **Secure**: Whitelist prevents redirect attacks
- ✅ **DRY**: One API endpoint for all flows

**Trade-offs**:
- ⚠️ **Shared code modification**: Requires regression testing
- ⚠️ **Security risk**: Mitigated by whitelist validation

**Alternatives rejected**:
- **Option B** (Separate endpoints): Code duplication, not scalable
- **Option C** (Header detection): Fragile, implicit, hard to debug

---

### Deployment Workflow

**Chosen**: Localhost → Staging (MANDATORY) → Production

**Why staging is mandatory**:
1. Modified **shared code** (AuthContext + Stripe API)
2. Onboarding actuel used by production users must continue working
3. Regression tests required before production deployment

**Regression tests coverage**:
- ✅ Onboarding OAuth flow (must redirect to /onboarding/languages)
- ✅ Onboarding Stripe flow (must redirect to /onboarding/complete)
- ✅ Landing OAuth flow (must redirect to /landing/setup/post-auth)
- ✅ Landing Stripe flow (must redirect to /landing/setup/complete)

**If staging is skipped**: High risk of breaking production onboarding flow for active users.

---

### Code Reuse Strategy

**Principle**: **Copier-coller** du code de l'onboarding actuel + adapter pour le landing.

**Rationale**:
- ✅ Zero risk (code already tested in production)
- ✅ Consistency (same patterns across flows)
- ✅ Speed (2-3h instead of 4-5h)
- ✅ Maintainability (if we fix a bug in onboarding, easy to apply to landing)

**What we copy-paste**:
1. **VocabTest** (95% identical, just change context + routes)
2. **Supabase save logic** (100% identical, just change sessionStorage key)
3. **Stripe checkout** (100% identical, just add URL parameters)

**What we modify**:
1. **AuthContext** (add optional `redirectTo` parameter)
2. **Stripe API** (add URL parameters + validation)

---

### Time Estimates (Revised)

| Phase | Original Estimate | Revised Estimate | Reason |
|-------|------------------|------------------|--------|
| **Phase 3.1** (VocabTest) | 1h | 15 min | Copy-paste strategy |
| **Phase 3.2** (OAuth) | 1h | 30 min | Reuse + small modification |
| **Phase 3.3** (Supabase) | 1h | 20 min | Copy-paste exact logic |
| **Phase 3.4** (Stripe) | 1.5h | 45 min | Copy-paste + validation |
| **Phase 3.5** (Analytics) | 30 min | 30 min (optional) | No change |
| **Total** | 4-5h | **2-3h** | ~50% time savings |

---

## 📝 Architecture Decisions (Documented - Original Plan)

### Design Decisions
- **Typography**: Max 3 sizes per screen (heading 32px, body 16px, caption 14px) ✅
- **Images**: Placeholders for Phase 1, real images in Phase 4 ✅
- **Responsive**: Desktop-first wireframes, mobile adaptation by developer ✅
- **Colors**: Reuse existing theme (Tailwind CSS v4 + Shadcn UI) ✅

### UX Decisions
- **Radio auto-nav**: 400ms delay for visual feedback before navigation ✅
- **Back button**: Hidden during vocab test (dynamic, can't go back) ✅
- **Progress bar**: Frozen during vocab test (variable number of screens) ✅
- **Trial reminder**: 3-point timeline to reduce "trial trap" anxiety ✅
- **Device detection**: None (same text on mobile/desktop for MVP) ✅

### Technical Decisions (KISS Applied)
- **LandingContext**: 3 fields only (targetLang, nativeLang, vocabLevel) - no navigation state ✅
- **sessionStorage**: Added (different from onboarding actuel - justified by longer flow + mobile) ✅
- **Components**: 1 new component only (`ProgressBarWithBack`) ✅
- **Inline code**: Radio auto-nav, timeline, mail icon (wait for 2-3 usages before abstracting) ✅
- **Progress bars**: Read `usePathname()` for current step (no manual tracking) ✅
- **Auth**: Manual sign-in after extension install (no auto-loading for MVP) ✅
- **Email**: Stripe native emails for MVP, Resend for custom later ✅
- **Analytics**: Vercel Analytics (already installed, no code needed) ✅
- **Domain**: Use `subly-extension.vercel.app` (free Vercel domain) ✅

### Backend Decisions
- **Subscription check**: Block at "Process Subtitles" if not paid (not at sign-in) ✅
- **User without payment**: Can create account, can't use extension until paid ✅
- **Extension install**: User manually signs in with "Already have account" button ✅
- **Data save timing**: AFTER Google OAuth (same as onboarding actuel) ✅

### Rule of Two/Three (DRY Applied Correctly)
- **Don't abstract until pattern used 2-3 times** ✅
- Radio auto-nav: Used 2x → Inline (wait for 3rd time)
- Timeline: Used 1x → Inline (wait for 2nd time)
- Mail icon: Used 1x → Inline (wait for 2nd time)

### Future Improvements (Not in MVP)
- [ ] Auto-loading settings after extension install (detect existing session)
- [ ] Custom Resend emails after checkout (better branding)
- [ ] Device detection (show different text on mobile vs desktop)
- [ ] Email reminder if user doesn't install extension after 1 day
- [ ] A/B testing different pricing (Vercel Edge Config)

---

## ⏱️ Time Estimates (Revised - Realistic)

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| **Phase 1: Frontend Shell** | Structure, context, components, 17 pages, navigation | 4-5 hours |
| **Phase 2: Design & Responsive** | Typography, layout, animations | 2-3 hours |
| **Phase 3: Backend Integration** | VocabTest, Auth, Supabase, Stripe | 4-5 hours |
| **Phase 4: Testing & Polish** | Images, E2E testing, bug fixes | 2-3 hours |
| **Phase 5: Deployment** | Staging → Production | 1 hour |
| **Total** | | **13-17 hours** |

**Buffer**: +20% for unexpected issues (15-20h total)

**Note**: Times assume uninterrupted work. Add buffer for breaks, unexpected bugs, and iterations based on user feedback.

---

## ✅ Success Criteria

### Functional Requirements
- ✅ User can complete full flow: Landing → Discovery → Setup → Auth → Checkout → Download
- ✅ Progress bars update correctly (Part 1: 7 steps, Part 2: ~13 steps)
- ✅ Back button works everywhere EXCEPT during vocab test
- ✅ Radio buttons auto-navigate after 400ms delay
- ✅ sessionStorage persists data through refreshes
- ✅ Vocab test integrates correctly (reuses VocabTestContext)
- ✅ Google OAuth creates Supabase account
- ✅ User settings saved to Supabase (target_lang, native_lang, vocab_level)
- ✅ Stripe checkout redirects to success page
- ✅ Webhook updates subscription status in Supabase
- ✅ Download link opens Chrome Web Store

### Design Requirements
- ✅ Responsive on mobile (375px) and desktop (1280px+)
- ✅ Max 2-3 font sizes per screen
- ✅ Images respect margins (not full-width)
- ✅ Consistent spacing (Tailwind scale)
- ✅ Smooth animations (radio checkmark, page transitions)

### Analytics Requirements
- ✅ Vercel Analytics tracks all screen views
- ✅ Key events tracked (auth, checkout, download)
- ✅ Funnel drop-off visible in dashboard

### Backend Requirements
- ✅ Supabase OAuth working (staging + production)
- ✅ Stripe checkout working (TEST mode staging, LIVE mode production)
- ✅ Webhook receiving events (200 OK responses)
- ✅ Data persisting correctly (user_settings, vocab_levels)

---

## 🐛 Known Limitations

### Current Limitations (MVP)
- **Manual sign-in after install**: User must click "Already have account" after installing extension (no auto-loading in MVP)
- **No email customization**: Using Stripe default emails (no custom branding in MVP)
- **No device detection**: Same text shown on mobile and desktop (no conditional messaging in MVP)

### Future Enhancements
- Auto-loading settings after extension install (detect existing Supabase session)
- Custom Resend emails with better branding
- Device-specific messaging (mobile vs desktop)
- Email reminder if user doesn't install extension after payment
- A/B testing different pricing/messaging

---

## 📚 References

### Existing Code to Study
- `/app/onboarding/*` - Current onboarding flow (after extension install)
- `/app/vocab-test/*` - Standalone vocab test flow
- `/contexts/VocabTestContext.tsx` - Vocab test logic
- `/contexts/OnboardingContext.tsx` - Onboarding state (no sessionStorage - different context)
- `/app/onboarding/pricing-intro/page.tsx` - Where Supabase save happens (AFTER auth)
- `/app/onboarding/layout.tsx` - Progress bar implementation

### Wireframes
- Part 1 (Discovery): `/Users/ulysse/Documents/01 PROJECTS/smart-subs/transient/Screenshot 2025-11-24 at 10.31.09.png`
- Part 2 (Setup): `/Users/ulysse/Documents/01 PROJECTS/smart-subs/transient/Screenshot 2025-11-24 at 10.45.21.png`

### Documentation
- Main CLAUDE.md: `/CLAUDE.md`
- Webapp CLAUDE.md: `/webapp-next/CLAUDE.md`
- Onboarding Flow: `/ONBOARDING_FLOW.md`
- Vocab Test Plan: `/VOCAB_TEST_RETEST_PLAN.md`

---

## 🚦 Status & Next Steps

**Current Status**: ✅ Plan validated by user (November 24, 2025)

**Approved Decisions**:
- ✅ Ultra-KISS architecture (1 component, inline code where appropriate)
- ✅ sessionStorage for data persistence (protects mobile users)
- ✅ Radio auto-nav inline (no hook, no component)
- ✅ Timeline inline (no component until 2nd usage)
- ✅ Mail icon inline (no component)
- ✅ Realistic time estimate (13-17h)

**Next Step**: Begin Phase 1 (Frontend Shell) on user signal.

---

**Ready for implementation** 🚀
