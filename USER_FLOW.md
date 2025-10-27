# USER FLOW - Smart Subtitles Extension

**Date:** October 2025
**Status:** Approved for Phase 1B implementation
**Wireframes:** See `/Users/ulysse/Downloads/Screenshot 2025-10-13 at 20.12.22.png`

---

## 1. KEY DECISIONS & RATIONALE

### Decision 1: Auth Required From Start ✅

**Choice:** Google OAuth required immediately after welcome screen (before language selection)

**Rationale:**
- **Simplicity:** Single data source (Supabase) - no chrome.storage.local migration needed
- **Multi-device sync:** Settings automatically sync across devices from day 1
- **Data safety:** No risk of losing settings when switching devices
- **Standard pattern:** Same as Grammarly, Loom, Notion (professional UX)
- **Implementation:** Supabase Google OAuth = 30 min setup (very simple)

**Trade-off accepted:**
- Slight onboarding friction (+1 step)
- Requires Google account (99% of Chrome users have one)

**Mitigation:**
- Clear messaging: "Sign in with Google to save your settings across devices"
- Benefits visible: "✓ Works on any computer ✓ No password needed ✓ Takes 5 seconds"

### Decision 2: Google OAuth Only (Phase 1) ✅

**Choice:** Google OAuth only - no email/password for Phase 1

**Rationale:**
- Covers 90%+ of target users (Chrome = Google ecosystem)
- Simpler implementation (no password reset, email verification)
- Non-breaking: Can add email/password later without migration

**Future:** Add email/password in Phase 2+ if user demand

### Decision 3: Supabase as Single Source of Truth ✅

**Choice:** All user data in Supabase from start - no local storage persistence

**Rationale:**
- Eliminates sync complexity
- Professional architecture
- Scales to 50,000+ users easily

**Data stored:**
- `user_settings`: target_lang, native_lang
- `vocab_levels`: vocabulary test results per language (supports multi-language testing)
- `known_words`: user's vocabulary list (for future features)
- `subscriptions`: billing status (Phase 2)

---

## 2. MAIN ONBOARDING FLOW (7 Steps)

### Entry Point
**Trigger:** User installs extension from Chrome Web Store
**Action:** Extension opens webapp in new tab at `http://localhost:5173/welcome`

---

### Step 1: Welcome Screen

**Route:** `/welcome`

**UI Elements:**
- **Logout button** (top-right corner, visible ONLY after user is authenticated)
- Ulysse's photo (personal touch)
- Headline: "Thanks for downloading my extension, my name is Ulysse and I learned to code just to build this extension. Hope you'll enjoy it!"
- Copy: "To use the extension, you first need to create an account and set it up"
- Primary button: "Create an account and set up Subly"
- Subtext: "It only takes 3 steps"
- Link below button: "Already have an account? login with google" (underlined, triggers Google OAuth)
- **Fixed feedback banner** (bottom of screen): "Any feedback? Please, send me an email at unducamp.pro@gmail.com"

**User Action:**
- Clicks "Create an account and set up Subly" → Google OAuth popup (new user)
- OR clicks "login with google" → Google OAuth popup (returning user)

**Data Collected:** None

**Next:** Step 2 (Auth via Google OAuth popup)

---

### Step 2: Google Authentication 🆕

**Route:** N/A (OAuth popup triggered from `/welcome`)

**UI Elements:**
- Standard Google OAuth popup (handled by Google)
- On `/welcome` page: "Step 1: create an account so Subly can save your settings"
- Primary button: "Continue with google" (Google logo + text)
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:** Clicks "Continue with Google" → Google OAuth popup

**Technical:**
```typescript
await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:5173/onboarding/languages'
  }
})
```

**Data Collected:**
- Google user ID
- Email
- Name (optional)

**Redirect Logic After Auth:**
- Check if `user_settings` exists in Supabase
- **If target_lang + native_lang + vocab_level exist:** → `/onboarding/complete` (returning user)
- **If target_lang + native_lang exist but not vocab_level:** → `/onboarding/vocab-test`
- **If nothing exists:** → `/onboarding/languages` (new user)

**Next:** Step 3 (Language Selection) OR Skip to complete if returning user

**Edge Case:** If auth fails → Show error message + retry button

---

### Step 3: Language Selection

**Route:** `/onboarding/languages`

**UI Elements:**
- **Logout button** (top-right corner)
- Headline: "Select your languages"
- Form:
  - Label: "Target language" (language you want to learn)
  - Dropdown: Select with 3 options (Portuguese 🇧🇷, French 🇫🇷, English 🇺🇸)
  - Label: "Native language" (your native language)
  - Dropdown: Select with 13 options (see Technical Specs section)
- Primary button: "Next"
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:**
1. Selects target language
2. Selects native language
3. Clicks "Next"

**Validation:**
- Target language required
- Native language required
- Target ≠ Native (show error if same)

**Data Collected:**
- `target_lang` (pt-BR | fr | en)
- `native_lang` (13 language codes - see specs)

**Saved to:** Supabase `user_settings` table

**Next:** Step 4 (Vocabulary Test)

---

### Step 4: Vocabulary Test

**Route:** `/onboarding/vocab-test`

**UI Elements:**
- **Logout button** (top-right corner)
- Headline: "Estimate your vocabulary level"
- Explanation paragraph:
  > "Select the first group of words in which there is at least one word you don't know. You should read each group one by one, and as soon as you find a group that contains a word you don't know, stop there and select that group.
  >
  > These groups are based on the list of the 10,000 most commonly used portuguese words. The first group is made up of randomly selected words from the 100 most common words, the second group comes from the 200 most common words, and so on.
  >
  > This way, your answer will help me roughly estimate how many of the most common portuguese words you already know."
- Radio button group (13 options):
  - ○ ele, como, falar, mesmo, dever, onde (100 words)
  - ○ mundo, tentar, lugar, nome, importante, último (200 words)
  - ○ morrer, certeza, enquanto, olá, contra, corpo (300 words)
  - ○ errar, serviço, preço, uma, considerar, vai (500 words)
  - ○ sentar, clicar, cerca, câmera, vermelho, principalmente (700 words)
  - ○ observar, membro, americano, desaparecer, apoiar, mamãe (1000 words)
  - ○ cobrir, relacionar, proteção, expressão, lua, particular (1500 words)
  - ○ reclamar, impacto, honra, móvel, tribunal, pior (2000 words)
  - ○ imóvel, duplo, vendedor, olhe, estender, energético (2500 words)
  - ○ influenciar, mínimo, sensor, ocasião, assegurar, telhado (3000 words)
  - ○ verso, ousar, puxa, mole, entretenimento, blusa (4000 words)
  - ○ exausto, art., surdo, deusa, box, parece (5000 words)
  - ○ **I know all the words above** (5000 words - advanced level)
- Primary button: "Confirm"
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:**
1. Reads word lists sequentially
2. Selects ONE radio button (first group containing unknown word, OR last option if knows all)
3. Clicks "Confirm"

**Validation:**
- Must select exactly 1 option (radio buttons enforce this)
- If nothing selected → Disable "Confirm" button + show error message

**Technical Note:**
- **Mapping:** Group selected = level stored (Option B - direct mapping)
- Example: User selects "300 words" radio → Store `300` in database
- Special case: "I know all words above" → Store `5000`

**Data Collected:**
- `vocab_level` (number: 100 | 200 | 300 | 500 | 700 | 1000 | 1500 | 2000 | 2500 | 3000 | 4000 | 5000)

**Saved to:** Supabase `vocab_levels` table (with `language` = target_lang)

**Next:** Step 5 (Test Results)

---

### Step 5: Test Results

**Route:** `/onboarding/results`

**UI Elements:**
- **Logout button** (top-right corner)
- Headline: "You know approximately [X] of the most used words"
  - [X] = dynamic number from vocab test (e.g., "2,000")
- Explanation paragraph: Contextualizes the result, explains what this means
- Primary button: "OK"
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:** Clicks "OK"

**Data Collected:** None (just displays previous result)

**Next:** Step 6 (Pin Extension)

---

### Step 6: Pin Extension (Bonus Step)

**Route:** `/onboarding/pin-extension`

**UI Elements:**
- **Logout button** (top-right corner)
- Headline: "Bonus: Pin the extension for quick access"
- Animated GIF/Screenshot: Shows how to pin extension in Chrome toolbar
- Primary button: "I have done it"
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:**
1. Pins extension (optional - not enforced)
2. Clicks "I have done it"

**Data Collected:** None

**Note:** This is a "nice to have" step - not blocking

**Next:** Step 7 (Congratulations)

---

### Step 7: Congratulations (Final Screen)

**Route:** `/onboarding/complete`

**UI Elements:**
- **Logout button** (top-right corner)
- Headline: "Congrats, you're all set!"
- Instructions:
  1. "Start using the extension when watching Netflix"
  2. "Click on the Subly icon to make the popup appear"
  3. "Then click the button 'Process subtitles' to adapt subtitles to your level"
- Screenshot: Shows extension popup on Netflix with "Process subtitles" button highlighted
- Additional tips paragraph (optional)
- Primary button: "Start watching on Netflix" (optional - opens netflix.com)
- **Fixed feedback banner** (bottom): Same as Step 1

**User Action:** Closes tab or clicks to Netflix

**Data Collected:** None

**Onboarding Complete:** ✅

**User can now use extension on Netflix**

---

## 3. POPUP USAGE (Post-Onboarding)

### 3.1 Normal Usage Flow

**Trigger:** User is on Netflix + clicks extension icon

**Popup displays:**

```
┌─────────────────────────────────┐
│  Smart Subtitles                │
├─────────────────────────────────┤
│  Target Language                │
│  [Portuguese (BR)      ▼]       │
│                                 │
│  Native Language                │
│  [French               ▼]       │
│                                 │
│  Vocabulary Level  [Test my level]│
│  ┌───────────────────────────┐ │
│  │ You know 2000             │ │
│  │ of the most used words    │ │
│  │ in Portuguese             │ │
│  └───────────────────────────┘ │
│                                 │
│  [Process Subtitles]            │
│                                 │
│  Any feedback? email me at      │
│  unducamp.pro@gmail.com         │
└─────────────────────────────────┘
```

**UI Elements:**
- **Target Language dropdown:** Select from 3 languages (PT-BR, FR, EN)
- **Native Language dropdown:** Select from 13 languages
- **Vocabulary Level card (read-only):** Displays "You know X of the most used words in [language]"
- **"Test my level" button:** Opens webapp vocab test in new tab (route: `/vocab-test`)
- **"Process Subtitles" button:** Triggers subtitle processing with current settings
- **Feedback banner (static):** "Any feedback? email me at unducamp.pro@gmail.com" (bottom of popup)

**User Actions:**
1. (Optional) Change target/native language
2. (Optional) Click "Test my level" to re-test vocabulary
3. Click "Process Subtitles" to apply settings

**Data Flow:**
- Settings read from Supabase on popup open
- Query `vocab_levels` table for current target_lang
- If no level found → Display "not defined yet" message (see 3.2)
- Changes to language saved to Supabase immediately
- Extension uses settings to process subtitles

---

### 3.2 Vocabulary Level Not Defined Yet

**Trigger:** User changes target_lang to language they haven't tested

**Popup displays:**

```
┌─────────────────────────────────┐
│  Vocabulary Level  [Test my level]│
│  ┌───────────────────────────┐ │
│  │ Your vocabulary level in  │ │
│  │ Portuguese is not defined │ │
│  │ yet, please click on the  │ │
│  │ button "test my level"    │ │
│  │ above                     │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

**Behavior:**
- "Process Subtitles" button **disabled** until level is tested
- User must click "Test my level" to enable subtitle processing

---

### 3.3 "Test My Level" Re-test Flow

**Trigger:** User clicks "Test my level" button in popup

**Flow:**
1. Opens webapp in new tab at `/vocab-test`
2. Page reads `target_lang` from Supabase (`user_settings` table)
3. Shows vocabulary test for that language (same as onboarding Step 4)
4. User selects level for current target language
5. Clicks "Confirm"
6. Level saved to `vocab_levels` table with `language` = target_lang
7. Popup reflects new level immediately (via Supabase sync)
8. User closes webapp tab, returns to Netflix

**Note:** No confirmation needed - level updates automatically after test

---

### 3.4 First-Time Popup (Edge Case)

**Trigger:** User clicks extension icon BEFORE completing onboarding

**Popup displays:**
- Ulysse's photo
- Message: "Thanks for downloading my extension..."
- Button: "Set up the extension"

**User Action:** Clicks button → Opens webapp at `/welcome` (Step 1)

**Purpose:** Ensures user always completes onboarding before using extension

---

## 4. EDGE CASES & ERROR HANDLING

### Priority 1: Must Handle Now

#### EC1: User Reinstalls Extension
**Scenario:** User uninstalls then reinstalls extension

**Solution:**
1. Extension opens webapp at `/welcome`
2. User clicks "Set up extension"
3. Auth screen detects existing Supabase account
4. Google OAuth succeeds
5. Backend checks if `user_settings` exists in Supabase
6. **If exists:** Skip onboarding → Show "Welcome back" message → Close tab
7. **If not exists:** Continue normal onboarding flow

**Technical:**
```typescript
// After auth success
const { data } = await supabase
  .from('user_settings')
  .select('*')
  .eq('user_id', user.id)
  .single()

if (data) {
  // Show welcome back screen
  router.push('/welcome-back')
} else {
  // Continue onboarding
  router.push('/onboarding/languages')
}
```

#### EC2: Multi-Device Sync
**Scenario:** User installs extension on PC + Laptop

**Solution:** Supabase automatically syncs settings
- PC: Sets target=PT, native=FR, level=2000
- Laptop: Opens extension → Reads same settings from Supabase ✅

**No special code needed** - Supabase handles this automatically

#### EC3: Google Auth Failure
**Scenario:** User closes Google OAuth popup or denies permission

**Solution:**
- Show error message: "Authentication required to continue"
- Show retry button: "Try again with Google"
- No way to skip (auth is required)

**Technical:**
```typescript
try {
  await supabase.auth.signInWithOAuth({ provider: 'google' })
} catch (error) {
  setError('Authentication failed. Please try again.')
}
```

#### EC4: Invalid Language Combination
**Scenario:** User selects same language for target and native

**Solution:**
- Disable "Next" button when target === native
- Show inline error: "Target and native languages must be different"

**Technical:**
```typescript
const isValid = targetLang && nativeLang && targetLang !== nativeLang
<Button disabled={!isValid}>Next</Button>
```

#### EC5: No Vocabulary Test Selection
**Scenario:** User clicks "Confirm" without selecting any radio button

**Solution:**
- Disable "Confirm" button until selection made
- Show error message: "Please select one option to continue"

**Technical:**
```typescript
const [selectedLevel, setSelectedLevel] = useState<number | null>(null)
<Button disabled={!selectedLevel}>Confirm</Button>
```

---

### Priority 2: Nice to Have (Defer to Later)

#### EC6: Interrupted Onboarding
**Scenario:** User closes tab during Step 4, then reopens extension

**Current behavior:** Starts from Step 1 (welcome)

**Future improvement:** Save progress to Supabase, resume from last step

**Deferred because:** Onboarding is quick (3-5 minutes), low impact

#### EC7: Language Change Suggestion
**Scenario:** User changes target language from PT→ES in popup

**Current behavior:** Keeps existing vocab level (2000)

**Future improvement:**
- Detect language change
- Show banner: "Your vocabulary level may differ in Spanish. Want to re-test?"
- Button: "Test my level in Spanish"

**Deferred because:** Complex logic, low frequency use case

#### EC8: Offline Usage
**Scenario:** User has no internet, opens extension

**Current behavior:** Supabase queries fail, settings don't load

**Future improvement:**
- Cache last settings in `chrome.storage.local`
- Use cached settings if Supabase unavailable
- Show warning: "Using cached settings (offline)"

**Deferred because:** Requires dual storage architecture, low priority

---

## 5. TECHNICAL SPECIFICATIONS

### 5.1 Supported Languages

**Target Languages (3):**
- `pt-BR` - Portuguese (Brazil) 🇧🇷
- `fr` - French 🇫🇷
- `en` - English (US) 🇺🇸

**Native Languages (13):**
- `en` - English 🇬🇧🇺🇸
- `fr` - French 🇫🇷
- `es` - Spanish 🇪🇸
- `de` - German 🇩🇪
- `it` - Italian 🇮🇹
- `pt` - Portuguese 🇵🇹
- `pl` - Polish 🇵🇱
- `nl` - Dutch 🇳🇱
- `sv` - Swedish 🇸🇪
- `da` - Danish 🇩🇰
- `cs` - Czech 🇨🇿
- `ja` - Japanese 🇯🇵
- `ko` - Korean 🇰🇷

**Note:** Netflix BCP47 variants (es-ES, pt-BR) automatically normalized to base language codes

---

### 5.2 Vocabulary Levels

**Available levels:**
- 500 words (Beginner)
- 1,000 words (Elementary)
- 2,000 words (Intermediate)
- 5,000 words (Advanced)
- 10,000 words (Near-native)

**Default:** 2,000 words (if test fails/skipped - though shouldn't happen)

**Storage:** Integer in Supabase `user_settings.vocab_level`

---

### 5.3 Database Schema

**Table 1: `user_settings`**
```sql
create table user_settings (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  target_lang text not null,
  native_lang text not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now(),
  unique(user_id)
);

-- Enable RLS
alter table user_settings enable row level security;
```

**Table 2: `vocab_levels`** (Multi-language support)
```sql
create table vocab_levels (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  language text not null,  -- 'pt-BR', 'fr', 'en'
  level integer not null,  -- 100, 200, 300, 500, 700, 1000, 1500, 2000, 2500, 3000, 4000, 5000
  tested_at timestamp with time zone default now(),
  unique(user_id, language)
);

-- Enable RLS
alter table vocab_levels enable row level security;

-- Index for fast lookups
create index vocab_levels_user_id_idx on vocab_levels(user_id);
create index vocab_levels_language_idx on vocab_levels(language);
```

**Table 3: `subscriptions`** (Phase 2 - created now, used later)
```sql
create table subscriptions (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  stripe_customer_id text,
  stripe_subscription_id text,
  status text not null,  -- 'active', 'canceled', 'past_due'
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now(),
  unique(user_id)
);

-- Enable RLS
alter table subscriptions enable row level security;
```

**Row Level Security Policies:**
```sql
-- user_settings policies
create policy "Users can view own settings"
  on user_settings for select
  using (auth.uid() = user_id);

create policy "Users can insert own settings"
  on user_settings for insert
  with check (auth.uid() = user_id);

create policy "Users can update own settings"
  on user_settings for update
  using (auth.uid() = user_id);

-- vocab_levels policies
create policy "Users can view own vocab levels"
  on vocab_levels for select
  using (auth.uid() = user_id);

create policy "Users can insert own vocab levels"
  on vocab_levels for insert
  with check (auth.uid() = user_id);

create policy "Users can update own vocab levels"
  on vocab_levels for update
  using (auth.uid() = user_id);

create policy "Users can delete own vocab levels"
  on vocab_levels for delete
  using (auth.uid() = user_id);

-- subscriptions policies
create policy "Users can view own subscription"
  on subscriptions for select
  using (auth.uid() = user_id);

create policy "Users can insert own subscription"
  on subscriptions for insert
  with check (auth.uid() = user_id);

create policy "Users can update own subscription"
  on subscriptions for update
  using (auth.uid() = user_id);
```

---

### 5.4 Routes & Components

**Webapp Routes:**
```
/welcome                    → Step 1: Welcome screen
/auth                       → Step 2: Google OAuth
/onboarding/languages       → Step 3: Language selection
/onboarding/vocab-test      → Step 4: Vocabulary test
/onboarding/results         → Step 5: Test results
/onboarding/pin-extension   → Step 6: Pin extension
/onboarding/complete        → Step 7: Congratulations
/welcome-back               → Returning user screen
/vocab-test                 → Standalone vocab test (from popup)
```

**Extension Popup:**
- Single page: `popup.html` with settings panel
- Opens webapp links in new tabs when needed

---

### 5.5 Shadcn UI Components Needed

**Already Installed (Phase 1A):**
- `Button` - Primary actions ✅
- `Select` - Language dropdowns ✅
- `RadioGroup` - Vocabulary test ✅
- `Label` - Form labels ✅

**To Install (Phase 1B):**
- `Card` - Content containers for popup vocab level display
- `Alert` - Error messages (auth failures, validation errors)

**Not Needed:**
- `Input` - NOT required (Google OAuth only, no email/password forms)

**Installation Commands:**
```bash
cd webapp
npx shadcn@latest add card
npx shadcn@latest add alert
```

---

## 6. DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    INSTALLATION                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: Welcome (webapp)                               │
│  - Show Ulysse photo + message                          │
│  - Button: "Set up extension"                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: Auth (webapp)                                  │
│  - Google OAuth popup                                   │
│  - Supabase creates user session                        │
│  - Check if user_settings exists                        │
│    → If exists: Skip to welcome-back                    │
│    → If not: Continue onboarding                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Languages (webapp)                             │
│  - Select target_lang (PT/FR/EN)                        │
│  - Select native_lang (13 options)                      │
│  - Save to Supabase user_settings                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: Vocab Test (webapp)                            │
│  - Show word lists with radio buttons                   │
│  - User selects level                                   │
│  - Save vocab_level to Supabase                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 5: Results (webapp)                               │
│  - Display vocab level result                           │
│  - Explain what it means                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 6: Pin Extension (webapp)                         │
│  - Show GIF/screenshot                                  │
│  - User pins (optional)                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 7: Complete (webapp)                              │
│  - Congrats message                                     │
│  - Usage instructions                                   │
│  - Screenshot of popup                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 NETFLIX USAGE                           │
│  - User opens Netflix                                   │
│  - Clicks extension icon → Popup                        │
│  - Popup reads settings from Supabase                   │
│  - User clicks "Process Subtitles"                      │
│  - Extension calls Railway API with settings            │
│  - Subtitle processing applied                          │
└─────────────────────────────────────────────────────────┘
```

---

## 7. IMPLEMENTATION CHECKLIST

### Phase 1B (This Phase)

- [ ] **Supabase Setup**
  - [ ] Create Supabase project
  - [ ] Enable Google OAuth provider
  - [ ] Configure redirect URLs
  - [ ] Create `user_settings` table + RLS policies

- [ ] **Auth Implementation**
  - [ ] Install `@supabase/supabase-js` in webapp
  - [ ] Create `lib/supabase.ts` client
  - [ ] Create `contexts/AuthContext.tsx`
  - [ ] Create `/auth` page with Google OAuth button
  - [ ] Test auth flow end-to-end

- [ ] **Onboarding Pages**
  - [ ] Create `/welcome` page (Step 1)
  - [ ] Create `/auth` page (Step 2)
  - [ ] Create `/onboarding/languages` page (Step 3)
  - [ ] Create `/onboarding/vocab-test` page (Step 4)
  - [ ] Create `/onboarding/results` page (Step 5)
  - [ ] Create `/onboarding/pin-extension` page (Step 6)
  - [ ] Create `/onboarding/complete` page (Step 7)
  - [ ] Create `/welcome-back` page (returning users)

- [ ] **Popup Integration**
  - [ ] Install `@supabase/supabase-js` in extension
  - [ ] Create Chrome Storage Adapter
  - [ ] Update popup to read from Supabase
  - [ ] Add "Test my level" link
  - [ ] Test popup → webapp communication

- [ ] **Edge Cases**
  - [ ] Handle reinstall scenario (check existing settings)
  - [ ] Handle auth failure (retry button)
  - [ ] Validate language selection (target ≠ native)
  - [ ] Validate vocab test selection (required)

- [ ] **Testing**
  - [ ] Test complete onboarding flow
  - [ ] Test returning user flow
  - [ ] Test multi-device sync
  - [ ] Test popup settings update
  - [ ] Test "Test my level" re-test flow

---

## 8. FUTURE ENHANCEMENTS (Post-Phase 1B)

### Enhancement 1: Email/Password Auth
**Priority:** Medium
**Timeline:** Phase 2+
**Description:** Add email/password signup option alongside Google OAuth

### Enhancement 2: Smart Language Change Detection
**Priority:** Low
**Timeline:** Phase 3+
**Description:** Suggest vocab re-test when user changes target language

### Enhancement 3: Onboarding Progress Persistence
**Priority:** Low
**Timeline:** Phase 3+
**Description:** Save onboarding progress, allow resume if interrupted

### Enhancement 4: Offline Mode
**Priority:** Low
**Timeline:** Phase 4+
**Description:** Cache settings locally for offline usage

### Enhancement 5: Advanced Vocabulary Test
**Priority:** Medium
**Timeline:** Phase 2+
**Description:** More sophisticated test with adaptive difficulty

### Enhancement 6: Onboarding Analytics
**Priority:** Medium
**Timeline:** Phase 2+
**Description:** Track where users drop off in onboarding, optimize flow

---

## 9. WIREFRAME REFERENCES

**Source:** `/Users/ulysse/Downloads/Screenshot 2025-10-13 at 20.12.22.png`

**Screens included:**
1. Welcome screen (Step 1) - Photo + message + button
2. Language selection (Step 3) - Two dropdowns + Next button
3. Vocabulary test (Step 4) - Radio buttons + Confirm button
4. Test results (Step 5) - Result display + OK button
5. Pin extension (Step 6) - GIF + "I have done it" button
6. Congratulations (Step 7) - Instructions + screenshot
7. Popup (post-onboarding) - Settings panel + Process button
8. Popup (first-time) - Welcome message + Setup button

**Note:** Auth screen (Step 2) not in wireframes - to be designed with Google OAuth button

---

## 10. SUCCESS METRICS

**Onboarding Completion Rate:**
- Target: >80% of users complete all 7 steps
- Track drop-off at each step
- Optimize bottlenecks

**Auth Success Rate:**
- Target: >95% successful Google OAuth
- Monitor auth failures
- Improve error handling if needed

**Time to Complete:**
- Target: <5 minutes for full onboarding
- Measure average time per step
- Simplify if too long

**Multi-Device Usage:**
- Target: 20% of users use on 2+ devices within first month
- Validates multi-device sync value

**Re-test Rate:**
- Target: 10% of users click "Test my level" after onboarding
- Indicates engagement with feature

---

**Document Version:** 2.0
**Last Updated:** January 17, 2025
**Next Review:** After Phase 1B implementation
**Changes in v2.0:**
- Added multi-language vocab_levels table (supports testing multiple languages)
- Updated popup UI design (Card component for vocab display, no dropdown)
- Added fixed feedback banner on all onboarding pages
- Added logout button (top-right, visible after auth)
- Updated vocab test with real Portuguese words (13 radio options)
- Clarified Google OAuth only (no email/password in Phase 1B)
- Added subscriptions table (Phase 2 - structure created now)
- Updated redirect logic after auth (detects returning users)
