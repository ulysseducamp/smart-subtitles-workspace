# Popup Redesign Implementation Plan

**Date:** January 27, 2025
**Phase:** 1B - Design Work
**Objective:** Deploy webapp to production, then redesign popup to match USER_FLOW.md specifications (Section 3.1)
**Approach:** Deploy-first strategy (DevOps best practice), then HTML/CSS vanilla popup redesign (no React migration - deferred to Phase 3)

---

## 🎯 Goals

### Part 1: Webapp Deployment (PREREQUISITE)
1. Deploy webapp to Vercel production
2. Configure environment variables for production
3. Add webapp URL variable to extension config
4. Enable end-to-end testing in real conditions

### Part 2: Popup Redesign
1. Remove Smart Subtitles toggle (unnecessary - settings always active)
2. Replace Vocabulary Level dropdown with read-only Card display
3. Add "Test my level" button that opens webapp vocab test (production URL)
4. Add feedback banner at bottom of popup
5. Keep Shadcn-like visual style without framework dependency

---

## 📐 Rationale: Why Deploy Webapp First?

**"Deploy early, deploy often"** - DevOps best practice

### ✅ Benefits:
1. **End-to-end testing in real conditions** - Test onboarding + extension with production URLs
2. **No technical debt** - No hardcoded localhost URLs to refactor later
3. **Architecture consistency** - Extension already has staging/production split for API
4. **Multi-device testing** - Validates Supabase sync across machines
5. **OAuth stability** - Production URLs are stable (localhost changes on restart)
6. **Minimal cost** - Vercel deploys Vite in 2 clicks, ~30 minutes setup
7. **Zero risk** - Webapp is functional, Supabase is already in production
8. **Phase 1B validation** - "Auth & Data Sync" includes deployment verification

### 📊 Cost vs Benefit:
- **Time investment:** 30 minutes deployment setup
- **Gain:** No refactoring needed, real testing, beta-tester ready
- **Alternative cost:** Technical debt + Phase 3 refactor (60+ minutes)

**Decision:** Deploy first = pragmatic choice

---

## 📋 PART 1: Webapp Deployment (Deploy First!)

### Step 1: Deploy Webapp to Vercel (15 minutes)

**Actions:**
1. Create free Vercel account at https://vercel.com
2. Connect GitHub repository
3. Import `webapp/` directory as new project
4. Configure build settings:
   - **Framework Preset:** Vite
   - **Root Directory:** `webapp`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variables in Vercel dashboard:
   - `VITE_SUPABASE_URL` = (your Supabase project URL)
   - `VITE_SUPABASE_ANON_KEY` = (your Supabase anon key)
6. Deploy → Note production URL (e.g., `subly-webapp.vercel.app`)

**Testing:**
- [ ] Visit production URL → Verify welcome page loads
- [ ] Complete Google OAuth flow → Verify redirect works
- [ ] Complete onboarding → Verify data saves to Supabase

---

### Step 2: Configure Supabase Redirect URLs (5 minutes)

**Actions:**
1. Open Supabase Dashboard → Authentication → URL Configuration
2. Add **Site URL:** `https://subly-webapp.vercel.app`
3. Add to **Redirect URLs:**
   - `https://subly-webapp.vercel.app/onboarding/languages` (production)
   - `http://localhost:5173/onboarding/languages` (keep for dev)

**Testing:**
- [ ] Test OAuth from production URL → Verify redirect works
- [ ] Test OAuth from localhost → Verify still works (dual setup)

---

### Step 3: Add WEBAPP_URL Variable to Extension (10 minutes)

**File:** `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/webpack.config.js`

**Action:** Add environment variable definition in webpack config:
```javascript
plugins: [
  new webpack.DefinePlugin({
    'process.env.WEBAPP_URL': JSON.stringify(
      process.env.NODE_ENV === 'production'
        ? 'https://subly-webapp.vercel.app'
        : 'http://localhost:5173'
    )
  })
]
```

**File:** `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/popup.ts`

**Action:** Create constant at top of file (after imports):
```typescript
// Webapp URL (changes based on build environment)
const WEBAPP_URL = process.env.WEBAPP_URL || 'http://localhost:5173';
```

**Usage:** When opening webapp routes (e.g., vocab test):
```typescript
chrome.tabs.create({ url: `${WEBAPP_URL}/vocab-test` });
```

**Testing:**
- [ ] Build staging: `npm run build:staging` → Verify uses localhost
- [ ] Build production: `npm run build:production` → Verify uses Vercel URL
- [ ] Install extension → Click test button → Verify opens correct URL

---

## 📋 PART 2: Popup Redesign (After Webapp Deployed)

### 1️⃣ Remove Smart Subtitles Toggle

**File:** `popup.html`
- **Action:** Delete lines 28-39 (entire toggle container)
- **Rationale:** User already completed onboarding → settings exist → no need for ON/OFF toggle. Manual "Process Subtitles" button is the only trigger needed.

**File:** `popup.ts`
- **Action:** Remove `enabled: boolean` from `SmartSubtitlesSettings` interface (line 29)
- **Action:** Remove `STORAGE_KEYS.SMART_SUBTITLES_ENABLED` constant (line 36)
- **Action:** Delete `updateFormState()` function (lines 204-221) - no longer needed
- **Action:** Remove all references to `currentSettings.enabled` throughout file
- **Action:** Dropdowns should always be enabled (remove disabled logic)

---

### 2️⃣ Replace Vocabulary Level Dropdown with Card

**File:** `popup.html`
- **Action:** Replace lines 61-116 (entire vocabulary level dropdown section)
- **New HTML structure:**
  ```
  <div class="form-group">
    <div class="vocab-header">
      <label>Vocabulary Level</label>
      <button id="test-level-btn" class="test-level-btn">Test my level</button>
    </div>

    <div class="vocab-card">
      <div id="vocab-display">
        <!-- Dynamically populated by JavaScript -->
      </div>
    </div>
  </div>
  ```

**File:** `popup.css`
- **Action:** Add Shadcn-like styles for Card component
- **Key styles:**
  - `.vocab-header` - Flexbox layout with space-between (label left, button right)
  - `.test-level-btn` - Small button, transparent background, indigo border/text (#6366f1)
  - `.vocab-card` - Light gray background (#f9fafb), subtle border (#e5e7eb), 8px border-radius
  - `.vocab-text` - 14px font, dark gray text (#374151)
  - `.vocab-text strong` - Bold weight (600), darker color (#111827)

**File:** `popup.ts`
- **Action:** Add `updateVocabDisplay()` function
  - **Case 1:** Vocabulary level exists → Display "You know **X** of the most used words in **[Language]**"
  - **Case 2:** No level for current target language → Display "Your vocabulary level in [Language] is not defined yet, please click on the button 'test my level' above"
  - Use `currentSettings.vocabularyLevel` and `currentSettings.targetLanguage` from Supabase

- **Action:** Add `getLanguageName(code: string)` helper function
  - Converts language codes to readable names:
    - `pt-BR` → `Portuguese`
    - `fr` → `French`
    - `en` → `English`

- **Action:** Call `updateVocabDisplay()` in `loadSettings()` after Supabase data loads
- **Action:** Call `updateVocabDisplay()` when user changes target language

---

### 3️⃣ Add "Test my level" Button Functionality

**File:** `popup.ts`
- **Action:** Add event listener for `#test-level-btn`
- **Behavior:** Opens webapp at `/vocab-test` route in new tab
- **URL:** Uses `WEBAPP_URL` constant (automatically staging/production aware)
- **Code:** `chrome.tabs.create({ url: `${WEBAPP_URL}/vocab-test` })`

**Synchronization logic (automatic - no extra code needed):**
1. User clicks "Test my level" → Opens webapp `/vocab-test` (production or localhost based on build)
2. User completes test → Level saved to Supabase `vocab_levels` table
3. User closes webapp tab, returns to Netflix
4. User re-opens popup → `loadSupabaseSettings()` automatically loads updated level
5. `updateVocabDisplay()` renders new level

**No polling, no WebSocket needed** → Supabase handles sync, popup reload triggers update.

---

### 4️⃣ Add Feedback Banner

**File:** `popup.html`
- **Action:** Add feedback banner before `</div><!-- container -->`
- **HTML:**
  ```
  <div class="feedback-banner">
    Any feedback? Please, send me an email at <a href="mailto:unducamp.pro@gmail.com">unducamp.pro@gmail.com</a>
  </div>
  ```

**File:** `popup.css`
- **Action:** Add banner styles
- **Key styles:**
  - Margin-top: 16px, padding-top: 16px
  - Border-top: 1px solid #e5e7eb (separator line)
  - Text-align: center, font-size: 12px, color: #6b7280 (gray)
  - Link color: #6366f1 (indigo), underline on hover

---

## 🎨 Shadcn Design System Colors (Reference)

Use these exact colors for Shadcn-like appearance:

- **Card background:** `#f9fafb` (gray-50)
- **Border color:** `#e5e7eb` (gray-200)
- **Text primary:** `#111827` (gray-900)
- **Text secondary:** `#374151` (gray-700)
- **Text muted:** `#6b7280` (gray-500)
- **Accent/Primary:** `#6366f1` (indigo-500)
- **Border radius:** 8px (cards), 6px (buttons)
- **Spacing:** 16px padding, 8px margins (consistent with Shadcn defaults)

---

## 📁 Files to Modify

### Part 1: Webapp Deployment
1. ⚙️ Vercel dashboard (create project, configure env vars)
2. ⚙️ Supabase dashboard (add production redirect URLs)
3. ✏️ `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/webpack.config.js`
4. ✏️ `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/popup.ts` (add WEBAPP_URL constant)

### Part 2: Popup Redesign
1. ✏️ `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/popup.html`
2. ✏️ `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/popup.ts`
3. ✏️ `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/popup/popup.css`

---

## ⚠️ Anti-Patterns to Avoid (KISS Principle)

### ❌ DO NOT:
1. Create a reusable component system → Overkill for 1 Card
2. Add state management library → `currentSettings` object is sufficient
3. Implement polling/WebSocket for level sync → Supabase + popup reload is enough
4. Add complex animations → Simple hover effects are sufficient
5. Create CSS-in-JS system → Vanilla CSS with clear class names works fine
6. Add a theming system → Hardcoded Shadcn colors are sufficient for now
7. Migrate to React → Deferred to Phase 3 (per ROADMAP.md line 362)

### ✅ DO:
1. Modify existing 3 files (HTML, TS, CSS)
2. Reuse `loadSupabaseSettings()` (already tested and working)
3. Use Shadcn color palette (hardcoded CSS variables)
4. Keep JavaScript simple (string interpolation, no templating engine)
5. Test with 2 cases: level defined + level undefined

---

## 🧪 Testing Checklist (After Implementation)

### Part 1: Webapp Deployment Tests
- [ ] **Test 1:** Production URL loads
  - Visit `https://subly-webapp.vercel.app` → Verify welcome page appears

- [ ] **Test 2:** OAuth flow in production
  - Complete Google OAuth from production URL → Verify redirect works

- [ ] **Test 3:** Supabase sync in production
  - Complete onboarding from production → Check Supabase Dashboard for data

- [ ] **Test 4:** Extension staging build
  - Build with `npm run build:staging` → Verify opens localhost webapp

- [ ] **Test 5:** Extension production build
  - Build with `npm run build:production` → Verify opens Vercel webapp

### Part 2: Popup Redesign Tests
- [ ] **Test 6:** User with defined level (pt-BR, 2000)
  - Open popup → Verify displays "You know 2000 of the most used words in Portuguese"

- [ ] **Test 7:** User without level for French
  - Change target_lang to FR in dropdown → Verify displays "not defined yet" message

- [ ] **Test 8:** "Test my level" button (production)
  - Click button → Verify webapp opens at production URL in new tab

- [ ] **Test 9:** Synchronization after test
  - Complete vocab test in webapp → Close webapp tab
  - Re-open popup → Verify level displays updated value

- [ ] **Test 10:** Feedback banner
  - Verify banner appears at bottom of popup
  - Verify email link works (opens mail client)

- [ ] **Test 11:** Toggle removal
  - Verify dropdowns are always enabled (no disabled state)
  - Verify "Process Subtitles" button works without toggle

- [ ] **Test 12:** Visual consistency
  - Compare Card styling to Shadcn Card in webapp
  - Verify colors match Shadcn palette (gray-50, indigo-500, etc.)

---

## ⏱️ Time Estimate

### Part 1: Webapp Deployment
- Create Vercel account + deploy: **15 minutes**
- Configure Supabase redirect URLs: **5 minutes**
- Add WEBAPP_URL to extension config: **10 minutes**
- Testing (5 deployment tests): **10 minutes**

**Part 1 Total: ~40 minutes**

### Part 2: Popup Redesign
- Remove toggle: **5 minutes**
- Create Card HTML/CSS: **15 minutes**
- Add `updateVocabDisplay()` logic: **10 minutes**
- Add "Test my level" button event: **5 minutes**
- Add feedback banner: **5 minutes**
- Testing (7 redesign tests): **10 minutes**

**Part 2 Total: ~50 minutes**

**Grand Total: ~90 minutes (1.5 hours)**

---

## 🔗 Related Documentation

- **USER_FLOW.md** - Section 3.1 (Normal Usage Flow) - Source of design specifications
- **ROADMAP.md** - Line 220-223 (Popup UI Design task)
- **ROADMAP.md** - Line 362 (Future React migration note - Phase 3)
- **CLAUDE.md** - Line 3 (KEEP IT SIMPLE principle)

---

## 📝 Implementation Order

### PART 1: Webapp Deployment (Do First!)
1. **Step 1:** Deploy webapp to Vercel (create account, import project, configure env vars)
2. **Step 2:** Add production URL to Supabase redirect URLs
3. **Step 3:** Add WEBAPP_URL variable to webpack.config.js
4. **Step 4:** Add WEBAPP_URL constant in popup.ts
5. **Step 5:** Test deployment (5 deployment test cases)

### PART 2: Popup Redesign (After Deployment)
6. **Step 6:** Remove toggle (HTML + TypeScript cleanup)
7. **Step 7:** Add Card HTML structure to popup.html
8. **Step 8:** Add CSS styles for Card (Shadcn-like)
9. **Step 9:** Add `updateVocabDisplay()` and `getLanguageName()` functions
10. **Step 10:** Add "Test my level" button event listener (uses WEBAPP_URL)
11. **Step 11:** Add feedback banner HTML + CSS
12. **Step 12:** Test all 12 test cases (5 deployment + 7 redesign)
13. **Step 13:** Build extension (`npm run build:staging` and `build:production`) and test both in Chrome

---

## 🚨 Critical Reminders

1. **Deploy webapp FIRST** - Do not start popup redesign before webapp is live on Vercel
2. **No React migration** - Popup remains HTML/CSS vanilla only (Phase 3 task)
3. **Reuse existing Supabase logic** - Don't reinvent `loadSupabaseSettings()`
4. **Use WEBAPP_URL constant** - Never hardcode localhost or production URLs
5. **Test with real Supabase data** - Use existing user with defined vocab level
6. **Keep it simple** - Card = `<div>` with CSS, not a complex component
7. **Test both builds** - Staging (localhost) AND production (Vercel) must work

---

**Status:** Ready for implementation
**Next Action:** Start with Part 1, Step 1 (Deploy webapp to Vercel)
