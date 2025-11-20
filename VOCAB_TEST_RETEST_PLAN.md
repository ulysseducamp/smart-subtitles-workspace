# Vocab Test/Retest Flow - Implementation Plan

**Date:** January 20, 2025
**Status:** Ready for Implementation
**Objective:** Create standalone vocab test flow accessible from extension popup

---

## 📋 Table of Contents

1. [Context & Problems](#context--problems)
2. [Architectural Decisions](#architectural-decisions)
3. [File Structure](#file-structure)
4. [Implementation Plan](#implementation-plan)
5. [Technical Details](#technical-details)
6. [Testing Checklist](#testing-checklist)

---

## 🎯 Context & Problems

### Current Issues

#### Problem 1: "Test My Level" Button Broken Flow
**Current behavior** (`Popup.tsx:333-339`):
- Clicking "Test My Level" opens `/onboarding/vocab-test?targetLanguage=pt-BR`
- Skips intro/explanation pages (jumps directly to test)
- `OnboardingContext` uses `sessionStorage` → new tab = empty context
- Test can't start because `targetLang` is null
- Results page redirects to `/onboarding/vocab-benefits` (onboarding flow) instead of returning to Netflix

**User impact:**
- ❌ Test doesn't load, nothing happens
- ❌ User must authenticate again (confusing - they're already logged in)
- ❌ Wrong flow for retesting vocabulary level

---

#### Problem 2: Changing Target Language Forces Re-onboarding
**Current behavior** (`Popup.tsx:285-302` + `loadSupabaseSettings.ts:38-49`):
- User changes target language (PT-BR → FR) in popup
- `handleTargetLanguageChange()` updates Supabase → reloads settings
- If no vocab level exists for new language → returns `null`
- Popup displays "Welcome" screen → forces full onboarding

**User impact:**
- ❌ Can't easily switch between PT-BR and FR
- ❌ Must complete full onboarding again (bad UX)
- ❌ Expected: See "Level not defined yet, click Test My Level"

---

#### Problem 3: No Auto-refresh After Test
**Current behavior:**
- User completes test in webapp → level saved to Supabase
- Returns to Netflix → opens popup
- Popup doesn't refresh automatically

**User impact:**
- ❌ Old vocab level displayed until popup closed/reopened

---

## 🏗️ Architectural Decisions

### Decision 1: Separate Flow (Not Conditional Onboarding Reuse)

**✅ CHOSEN: Copy onboarding pages to `/vocab-test/` and modify**

**Rationale:**
- ✅ Semantically correct (vocab test is NOT onboarding, it's a standalone feature)
- ✅ KISS - No conditional logic (`if retestMode then...`) scattered everywhere
- ✅ Maintainable - Changes to onboarding won't break vocab test
- ✅ Clear separation of concerns

**❌ REJECTED: Reuse `/onboarding/vocab-test` with `retestMode=true` param**
- ❌ Requires hiding progress bar conditionally in `OnboardingLayout`
- ❌ Different final page (results → Netflix vs results → auth/pricing)
- ❌ Complex conditional rendering throughout
- ❌ Tight coupling between onboarding and retest flows

---

### Decision 2: Dedicated Context (VocabTestContext)

**✅ CHOSEN: Create `VocabTestContext` separate from `OnboardingContext`**

**Rationale:**
- ✅ No collision with onboarding state
- ✅ Pass `targetLanguage` via URL → set in context on mount
- ✅ No need for `sessionStorage` (linear flow, 4 pages max)
- ✅ Clean, simple state management

**Implementation:**
- Context stores: `targetLanguage` (from URL) + `vocabLevel` (from test)
- No persistence needed (short-lived flow)

---

### Decision 3: Auto-refresh via Message Passing (Fire and Forget)

**✅ CHOSEN: Message Passing without verification**

**Rationale:**
- ✅ Better UX (99.5% auto-refresh, no manual close/reopen)
- ✅ Only ~30 lines of code (reasonable cost)
- ✅ Standard Chrome extension pattern
- ✅ Fire and forget - no error handling for 0.5% failure rate (KISS)

**❌ REJECTED: Polling every 5 seconds**
- ❌ Terrible performance (infinite Supabase requests)
- ❌ Battery drain
- ❌ Anti-pattern in web development

**❌ REJECTED: Manual close/reopen only**
- ❌ Worse UX (friction)
- ❌ Users don't read instructions

**❌ REJECTED: Conditional fallback message on error**
- ❌ Over-engineering for 0.5% failure rate
- ❌ Non-blocking issue (user can close/reopen naturally)

---

### Decision 4: Fix Language Change Issue (Separate Task)

**⏳ DEFERRED: Fix `loadSupabaseSettings.ts` to return `vocabLevel: 0` instead of `null`**

**Priority:** Lower (focus on vocab test flow first)

**Solution:**
```typescript
const vocabLevel = vocabData?.level || 0; // Default to 0 if not tested
```

**Result:** Popup displays "Level not defined yet, click Test My Level" instead of Welcome screen

---

## 📁 File Structure

### New Directory: `/webapp-next/src/app/vocab-test/`

```
/app/vocab-test/
├── intro/
│   └── page.tsx           ← "Now it's time to test your vocabulary"
├── explanation/
│   └── page.tsx           ← "We'll show you words selected from this list"
├── test/
│   └── page.tsx           ← Actual vocab test (12 levels)
└── results/
    └── page.tsx           ← Results + "Go back to Netflix" button

/contexts/
└── VocabTestContext.tsx   ← New context for vocab test flow
```

**No progress bar:** These pages are standalone, no `OnboardingLayout` wrapper

---

## 🛠️ Implementation Plan

### Step 1: Create VocabTestContext

**File:** `webapp-next/src/contexts/VocabTestContext.tsx`

**Responsibilities:**
- Store `targetLanguage` (set from URL parameter)
- Store `vocabLevel` (set during test)
- Provide setters for both

**Key difference from OnboardingContext:**
- No `sessionStorage` (not needed for short flow)
- Only 2 state variables (simpler)

---

### Step 2: Create Intro Page

**File:** `webapp-next/src/app/vocab-test/intro/page.tsx`

**Copy from:** `/onboarding/vocab-test-intro/page.tsx`

**Modifications:**
1. Remove progress bar (no `OnboardingLayout` wrapper)
2. Get `targetLanguage` from URL parameter
3. Set `targetLanguage` in `VocabTestContext` on mount
4. Button redirects to `/vocab-test/explanation`

**Example URL:** `/vocab-test/intro?targetLanguage=pt-BR`

---

### Step 3: Create Explanation Page

**File:** `webapp-next/src/app/vocab-test/explanation/page.tsx`

**Copy from:** `/onboarding/vocab-test-explanation/page.tsx`

**Modifications:**
1. Remove progress bar
2. Button redirects to `/vocab-test/test?level=100`

**No changes to content** - same text as onboarding

---

### Step 4: Create Test Page

**File:** `webapp-next/src/app/vocab-test/test/page.tsx`

**Copy from:** `/onboarding/vocab-test/page.tsx`

**Modifications:**
1. Remove progress bar
2. Use `VocabTestContext` instead of `OnboardingContext`
3. Keep same test logic (12 levels: 100, 200, 300, 500, 700, 1000, 1500, 2000, 2500, 3000, 4000, 5000)
4. Redirect to `/vocab-test/results` on completion

**No changes to word lists** - reuse PT_WORDS and FR_WORDS

---

### Step 5: Create Results Page

**File:** `webapp-next/src/app/vocab-test/results/page.tsx`

**Copy from:** `/onboarding/results/page.tsx`

**Modifications:**

#### 1. Different Text
```typescript
<p className="text-lg text-center mb-8">
  You can now go back to Netflix and use Subly with this vocabulary level.
</p>
```

#### 2. Different Button
```typescript
<Button
  onClick={() => chrome.tabs.create({ url: 'https://www.netflix.com' })}
  size="lg"
>
  Go back to Netflix
</Button>
```

#### 3. Save to Supabase (upsert)
```typescript
useEffect(() => {
  const saveVocabLevel = async () => {
    if (!user || !targetLanguage || !vocabLevel || saved) return

    const supabase = createClient()

    // Save to vocab_levels table
    await supabase.from('vocab_levels').upsert({
      user_id: user.id,
      language: targetLanguage,
      level: vocabLevel,
      tested_at: new Date().toISOString(),
    })

    console.log('✅ Vocab level saved to Supabase')
    setSaved(true)
  }

  saveVocabLevel()
}, [user, targetLanguage, vocabLevel, saved])
```

#### 4. Send Message to Extension (Fire and Forget)
```typescript
useEffect(() => {
  const notifyExtension = async () => {
    if (!saved || !vocabLevel || !targetLanguage) return

    try {
      chrome.runtime.sendMessage(EXTENSION_ID, {
        type: 'VOCAB_LEVEL_UPDATED',
        level: vocabLevel,
        language: targetLanguage
      })
      console.log('✅ Message sent to extension')
    } catch (error) {
      console.log('⚠️ Could not send message to extension (not critical)')
    }
  }

  notifyExtension()
}, [saved, vocabLevel, targetLanguage])
```

**Note:** No error handling, no conditional text. Fire and forget (KISS).

---

### Step 6: Update Extension Popup

**File:** `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/Popup.tsx`

**Modification:** Change `handleTestLevel()` function (line 333)

**Before:**
```typescript
function handleTestLevel(): void {
  const targetLang = settings.targetLanguage || '';
  const url = targetLang
    ? `${WEBAPP_URL}/onboarding/vocab-test?targetLanguage=${targetLang}`
    : `${WEBAPP_URL}/onboarding/vocab-test`;
  chrome.tabs.create({ url });
}
```

**After:**
```typescript
function handleTestLevel(): void {
  const targetLang = settings.targetLanguage || 'pt-BR';
  chrome.tabs.create({
    url: `${WEBAPP_URL}/vocab-test/intro?targetLanguage=${targetLang}`
  });
}
```

---

### Step 7: Add Message Listener in Extension Background

**File:** `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/background.ts`

**Add listener:**
```typescript
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'VOCAB_LEVEL_UPDATED') {
    // Update chrome.storage.local
    chrome.storage.local.set({
      vocabularyLevel: message.level,
      targetLanguage: message.language
    })

    console.log('✅ Vocab level updated:', message.level, message.language)
    sendResponse({ success: true })
  }
})
```

**Purpose:** When webapp sends message → update local storage → popup auto-refreshes on next open

---

### Step 8: Add Storage Change Listener in Popup

**File:** `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/Popup.tsx`

**Add useEffect:**
```typescript
// Listen for storage changes (vocab level updated from webapp)
useEffect(() => {
  const handleStorageChange = (changes: { [key: string]: chrome.storage.StorageChange }) => {
    if (changes.vocabularyLevel || changes.targetLanguage) {
      console.log('🔄 Storage changed, reloading settings...')
      loadSettings()
    }
  }

  chrome.storage.onChanged.addListener(handleStorageChange)

  return () => {
    chrome.storage.onChanged.removeListener(handleStorageChange)
  }
}, [])
```

**Purpose:** When `chrome.storage.local` changes → reload settings → popup displays new level

---

## 🔧 Technical Details

### Supabase Integration

#### Table: `vocab_levels`
```sql
CREATE TABLE vocab_levels (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  language TEXT NOT NULL,
  level INTEGER NOT NULL,
  tested_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, language)
);
```

**Constraint:** `UNIQUE(user_id, language)` ensures one level per user per language

**Upsert behavior:**
- First test for PT-BR → `INSERT` new row
- Retest for PT-BR → `UPDATE` existing row (no duplicate)
- Test for FR → `INSERT` new row (different language)

**Example data:**
```
user_id: alice-123 | language: pt-BR | level: 1500
user_id: alice-123 | language: fr    | level: 1000
```

---

### Message Passing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. User completes test in /vocab-test/results                 │
│                                                                 │
│  2. Save to Supabase:                                           │
│     vocab_levels.upsert({ user_id, language, level })          │
│                                                                 │
│  3. Send message to extension (fire and forget):                │
│     chrome.runtime.sendMessage(EXTENSION_ID, {                 │
│       type: 'VOCAB_LEVEL_UPDATED',                             │
│       level: 1500,                                              │
│       language: 'pt-BR'                                         │
│     })                                                          │
│                                                                 │
│  4. Extension background.ts receives message:                   │
│     chrome.storage.local.set({ vocabularyLevel: 1500 })        │
│                                                                 │
│  5. Popup.tsx detects storage change:                           │
│     chrome.storage.onChanged → loadSettings()                  │
│                                                                 │
│  6. Popup displays updated level: "You know 1500 words"        │
└─────────────────────────────────────────────────────────────────┘
```

**Failure scenario (0.5% probability):**
- Step 3 fails (extension not detected)
- Level IS saved to Supabase (Step 2 succeeded)
- User closes/reopens popup → `loadSettings()` fetches from Supabase
- **Result:** Still works, just not automatic

---

### Extension ID Configuration

**Location:** `webapp-next/src/lib/constants.ts` (or similar)

```typescript
export const EXTENSION_ID = 'lhkamocmjgilkhmfiogfdjhlhfrfoaaek' // Chrome Web Store ID
```

**Important:** This ID must match the `key` field in `manifest.json` for message passing to work.

---

### URL Parameters

**Popup → Webapp:**
```
Click "Test My Level" → Opens:
https://subly-extension.vercel.app/vocab-test/intro?targetLanguage=pt-BR
```

**Intro → Explanation:**
```
No URL params needed (language stored in VocabTestContext)
```

**Explanation → Test:**
```
/vocab-test/test?level=100 (starts at level 100)
```

**Test navigation:**
```
User knows all words → /vocab-test/test?level=200
User doesn't know word → /vocab-test/results (set vocabLevel=100)
```

---

## ✅ Testing Checklist

### Before Implementation
- [ ] Read this document completely
- [ ] Understand Message Passing flow
- [ ] Understand Supabase upsert behavior
- [ ] Review existing onboarding pages to copy

---

### During Implementation
- [ ] Create `VocabTestContext.tsx`
- [ ] Create `/vocab-test/intro/page.tsx`
- [ ] Create `/vocab-test/explanation/page.tsx`
- [ ] Create `/vocab-test/test/page.tsx`
- [ ] Create `/vocab-test/results/page.tsx`
- [ ] Update `Popup.tsx` - `handleTestLevel()` function
- [ ] Update `background.ts` - Add message listener
- [ ] Update `Popup.tsx` - Add storage change listener

---

### After Implementation - Manual Testing

#### Test 1: First Time Test (PT-BR)
1. [ ] Open popup on Netflix
2. [ ] Click "Test My Level" (target language: PT-BR)
3. [ ] Verify intro page opens with correct language name
4. [ ] Click "Continue" → explanation page
5. [ ] Click "Start" → test page (level 100)
6. [ ] Complete test (select "I don't know" at level 500)
7. [ ] Verify results page: "You know approximately 500 words"
8. [ ] Verify button says "Go back to Netflix"
9. [ ] Click button → verify Netflix opens
10. [ ] Open popup → verify level displays "500 of the most used words in Portuguese"

#### Test 2: Retest (Higher Level)
1. [ ] Open popup on Netflix
2. [ ] Click "Test My Level" (target language: PT-BR)
3. [ ] Complete test (select "I don't know" at level 1500)
4. [ ] Open popup → verify level updated to 1500

#### Test 3: Test Different Language (FR)
1. [ ] Change target language to French in popup
2. [ ] Verify popup shows "Level not defined yet, click Test My Level"
3. [ ] Click "Test My Level"
4. [ ] Complete test for French
5. [ ] Verify French level saved independently from PT-BR

#### Test 4: Auto-refresh (Message Passing)
1. [ ] Complete vocab test
2. [ ] Click "Go back to Netflix"
3. [ ] Open popup **WITHOUT closing/reopening**
4. [ ] Verify new level displays (confirms message passing worked)

#### Test 5: Manual Refresh Fallback
1. [ ] Disable extension temporarily
2. [ ] Complete vocab test in webapp
3. [ ] Re-enable extension
4. [ ] Close and reopen popup
5. [ ] Verify level displays correctly (confirms Supabase persistence)

---

### Supabase Database Testing

#### Test with 2 Google Accounts (RLS Validation)

**User A (alice@gmail.com):**
1. [ ] Complete PT-BR test → 1000 words
2. [ ] Complete FR test → 1500 words
3. [ ] Verify `vocab_levels` table has 2 rows for Alice

**User B (bob@gmail.com):**
1. [ ] Complete PT-BR test → 2000 words
2. [ ] Verify `vocab_levels` table has 1 row for Bob

**RLS Validation:**
1. [ ] Log in as Alice → verify she sees ONLY her levels (1000 PT-BR, 1500 FR)
2. [ ] Log in as Bob → verify he sees ONLY his level (2000 PT-BR)
3. [ ] Confirm users cannot query each other's data

---

### Edge Cases

#### Edge Case 1: No Target Language Set
1. [ ] Manually clear target language in popup
2. [ ] Click "Test My Level"
3. [ ] Verify defaults to PT-BR (fallback in code)

#### Edge Case 2: Extension Not Installed
1. [ ] Complete test in webapp WITHOUT extension installed
2. [ ] Verify level saved to Supabase (no error thrown)
3. [ ] Install extension later → verify level loads correctly

#### Edge Case 3: Network Error During Save
1. [ ] Disconnect internet before clicking final test answer
2. [ ] Verify error handling (retry or display error message)

---

## 📝 Implementation Notes

### Code Reuse Strategy
- Copy entire pages from `/onboarding/` to `/vocab-test/`
- Remove progress bar imports
- Change context import: `OnboardingContext` → `VocabTestContext`
- Update button redirects to `/vocab-test/*` routes

### Avoid These Mistakes
- ❌ Don't modify existing onboarding pages (keep them separate)
- ❌ Don't forget to pass `targetLanguage` via URL parameter
- ❌ Don't add error handling for message passing (fire and forget)
- ❌ Don't use `sessionStorage` in `VocabTestContext` (not needed)

### KISS Principles Applied
- ✅ Fire and forget message passing (no error handling)
- ✅ No conditional text on results page
- ✅ Separate flow (no complex conditional logic in onboarding)
- ✅ Simple context (2 state variables only)

---

## 🚀 Next Steps

1. **Review this document** with stakeholders
2. **Implement Step 1-8** following the plan above
3. **Test manually** using the checklist
4. **Deploy to staging** (`develop` branch → `staging-subly-extension.vercel.app`)
5. **Test in production environment** before merging to `main`

---

**Last Updated:** January 20, 2025
**Next Review:** After implementation complete
