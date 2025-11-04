# 🗺️ SMART SUBTITLES - ROADMAP

**Strategy**: Auth Direct → Paiement → Launch
**Status**: Phase 1B in progress (Supabase Auth setup)

---

## ✅ PHASE 1A - WEBAPP FOUNDATION (COMPLETED)

**Objective**: Setup modern webapp architecture with React, Vite, Shadcn UI

- [x] Revert to clean state (phase1a-start tag)
- [x] Create webapp with Vite + React + TypeScript
- [x] Install Shadcn UI components (Button, Select, RadioGroup, Label)
- [x] Add React Router with /onboarding and /dashboard routes
- [x] Extension opens webapp on install
- [x] Validation: Extension opens localhost:5173/onboarding ✅

**Duration**: 2-3 hours
**Date completed**: October 15, 2025

---

## 🚧 PHASE 1B - AUTHENTICATION & DATA SYNC (IN PROGRESS)

**Objective**: Setup Supabase Auth (Google OAuth only) for user accounts and data synchronization

**Strategy**: Incremental testing after each major component (pragmatic approach)

### Backend Setup (Day 1 - 4 hours)

---

#### Step 1: Supabase Project + Database (30min)

- [x] **Supabase Project Setup**
  - [x] Create Supabase account
  - [x] Create new project "Subly"
  - [x] Note: Project URL + Anon Key + Service Role Key
    - Anon Key: Frontend (webapp + extension)
    - Service Role Key: Backend admin (Phase 2 - not used in 1B)

- [x] **Database Schema** (Use Supabase Dashboard - NOT MCP)
  - [x] Create `user_settings` table [voir Code 1]
  - [x] Create `vocab_levels` table [voir Code 1b - multi-language support]
  - [x] Create `subscriptions` table [voir Code 1c - Phase 2 structure]
  - [x] Create `known_words` table [voir Code 2]
  - [x] Setup Row Level Security (RLS) policies [voir Code 3]

- [x] **✅ TEST 1 (5-10min)** - Database Validation
  - [x] Login to Supabase Dashboard
  - [x] Verify 4 tables created with RLS policies
  - [x] Verify 3-4 RLS policies per table
  - **Pass criteria:** Tables created, RLS enabled, no errors ✅ PASSED

---

#### Step 2: Authentication Configuration (30min)

- [x] **Enable Google OAuth**
  - [x] Enable Google OAuth provider in Supabase dashboard
  - [x] Configure redirect URLs (localhost:5173 + production)
  - [x] Create Google Cloud OAuth credentials (Client ID and Secret)

- [x] **✅ TEST 2 (5min)** - OAuth Flow
  - [x] Test OAuth URL directly in incognito window
  - [x] Click "Sign in with Google" → Complete OAuth flow
  - [x] Verify user appears in `auth.users` table
  - **Pass criteria:** OAuth flow completes, user created in auth.users ✅ PASSED (User: unducamp.pro@gmail.com)

---

#### Step 3: Webapp Integration (1h 30min)

- [x] **Install Dependencies**
  - [x] `npm install @supabase/supabase-js` in webapp/
  - [x] `npx shadcn@latest add card alert toast` (Shadcn components)

- [x] **Create Supabase Client**
  - [x] Create `webapp/src/lib/supabase.ts` [voir Code 4]
  - [x] Create `.env.local` with VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY
  - [x] Create AuthContext React component [voir Code 5]

- [x] **Create Onboarding Pages** (7 pages total)
  - [x] Create `/welcome` page with Google OAuth button [voir Code 6]
  - [x] Create `/onboarding/languages` page (target + native language selection)
  - [x] Create `/onboarding/vocab-test` page (12 vocab levels)
  - [x] Create `/onboarding/results` page (display vocab level)
  - [x] Create `/onboarding/pin-extension` page (bonus step)
  - [x] Create `/onboarding/complete` page (congrats + instructions)
  - [x] Create `/welcome-back` page (returning users)

- [x] **Update App.tsx**
  - [x] Wrap app with AuthProvider
  - [x] Add all 7 routes
  - [x] Implement redirect logic after auth (detect returning users)

- [x] **✅ TEST 3 (10min)** - Webapp Auth
  - [x] Run `npm run dev` in webapp/
  - [x] Open localhost:5173/welcome
  - [x] Click "Continue with Google" → Complete OAuth
  - [x] Check browser console: `user` object visible
  - [x] Verify redirect to `/onboarding/languages`
  - **Pass criteria:** OAuth flow works, user object in console, redirect OK ✅ PASSED

- [x] **✅ TEST 4 (5min)** - Onboarding Flow
  - [x] Complete onboarding: Languages → Vocab test → Complete
  - [x] Check Supabase Dashboard: Verify rows created in `user_settings` and `vocab_levels`
  - **Pass criteria:** Data saved correctly in database ✅ PASSED (pt-BR + fr, level 700)

---

#### Step 4: Extension Integration (30min + 30min Message Passing)

- [x] **Install Dependencies**
  - [x] `npm install @supabase/supabase-js` in extension/
  - [x] Create Chrome Storage Adapter [voir Code 7]
  - [x] Configure Supabase client in extension

**🔗 Step 4b: Message Passing Implementation (30min) - CRITICAL**

**Problem:** Webapp and Extension = 2 separate domains (localhost:5173 vs chrome-extension://xxx)
Session in webapp localStorage is NOT accessible to extension chrome.storage.local

**Solution:** Transfer tokens from webapp to extension after OAuth

**Implementation Plan (30min):**

1. **Manifest (5min)** - Add `externally_connectable` + `key`
   - [x] Generate extension key for fixed ID in dev
   - [x] Add `externally_connectable` to manifest.json
   - [x] Add localhost:5173 and production URL to matches

2. **Webapp (10min)** - Send tokens to extension after OAuth
   - [x] Create `syncSessionToExtension()` utility function
   - [x] Call after OAuth success (implemented via AuthContext SIGNED_IN event)
   - [x] Add timeout (2s) + error handling
   - [x] Sync on TOKEN_REFRESHED event (prevents token desync)

3. **Extension (10min)** - Receive and store tokens
   - [x] Add `chrome.runtime.onMessageExternal` listener in background.ts
   - [x] Validate sender origin (security)
   - [x] Call `supabase.auth.setSession()` with received tokens
   - [x] Store session in chrome.storage.local via adapter

4. **Test (5min)** - Validate end-to-end flow
   - [x] Get extension ID from Chrome and update webapp
   - [x] Complete onboarding in webapp
   - [x] Open extension popup
   - [x] Verify settings display (pt-BR, fr, 700)

**Critical Fix: Rolling Refresh Tokens**
- Supabase invalidates old refresh_token when webapp auto-refreshes (after ~50min)
- Extension's stored refresh_token becomes invalid
- Solution: Re-sync tokens on TOKEN_REFRESHED event in webapp

- [x] **✅ TEST 5 (5min)** - Extension Reads Supabase ✅ PASSED (January 20, 2025)
  - [x] Build extension: `npm run build:staging`
  - [x] Load extension in Chrome
  - [x] Open extension popup
  - [x] Verify: Settings displayed (target_lang ✅, vocab_level ✅, native_lang ⚠️ minor bug)
  - **Pass criteria:** Extension reads user settings from Supabase ✅
  - **Note:** Native language display bug identified (non-blocking, data loads correctly)

---

#### Step 5: Final Testing (30min) - CRITICAL

- [x] **✅ TEST 6 (10min)** - RLS Isolation (CRITICAL) ✅ PASSED (January 20, 2025)
  - [x] Create 2nd Google account
  - [x] User A: Complete onboarding → PT-BR, 1500 + FR, 1500
  - [x] User B: Complete onboarding → PT-BR, 1000
  - [x] Verify: User A shows ONLY 1500 (not 1000)
  - [x] Verify: User B shows ONLY 1000 (not 1500)
  - **Pass criteria:** Users cannot see each other's data ✅
  - **Note:** 2 distinct user_ids in database, data properly isolated

- [x] **✅ TEST 7 (5min)** - CASCADE DELETE ✅ PASSED (January 20, 2025)
  - [x] User B: Deleted via Supabase Dashboard (Authentication tab)
  - [x] Verify: All User B data deleted from `vocab_levels` ✅
  - [x] Verify: All User B data deleted from `user_settings` ✅
  - **Pass criteria:** No orphaned data remains ✅

- [x] **✅ TEST 8 (5min)** - UNIQUE Constraint ✅ PASSED (January 20, 2025)
  - [x] User A: Test PT-BR → 700 words (initial)
  - [x] User A: Re-test PT-BR → 1500 words (change level)
  - [x] Verify: Only 1 row in `vocab_levels` for (User A, PT-BR)
  - [x] Verify: Level updated to 1500 (ON CONFLICT UPDATE)
  - **Pass criteria:** No duplicate rows, level updated correctly ✅

- [x] **✅ TEST 9 (5min)** - Session Persistence ✅ PASSED (January 20, 2025)
  - [x] Login to webapp
  - [x] Refresh page (F5)
  - [x] Verify: User still logged in (no redirect to /welcome)
  - **Pass criteria:** Session persists across page refresh ✅

- [x] **✅ TEST 10 (5min)** - Multi-Language Support ✅ PASSED (January 20, 2025)
  - [x] User A: Test PT-BR → 700 (then 1500)
  - [x] User A: Test FR → 1500
  - [x] Verify: 2 rows in `vocab_levels` table (one per language)
  - **Pass criteria:** Multiple languages stored independently ✅

### Design Work (Days 2-5)

- [ ] **Onboarding Flow Design**
  - [x] Step 1: Welcome screen
  - [x] Step 2: Language selection (target + native)
    - [ ] Remove English from target language options (keep only PT-BR + FR for now)
  - [x] Step 3: Vocabulary test
    - [x] Implement dynamic vocab test (PT-BR + FR word lists) ✅ (January 27, 2025)
  - [x] Step 4: Pin extension reminder
  - [x] Step 5: Success message

- [ ] **Subtitles Appearance**
  - [ ] Font styling improvements
  - [ ] Color scheme updates
  - [ ] Positioning options
  - [ ] Inline translation styling

- [x] **Popup UI Design** ✅ (January 28, 2025)
  - [x] Settings panel redesign (removed toggle, added vocab Card)
  - [x] Language selector UI (kept existing dropdowns)
  - [x] Quick actions menu (added "Test my level" button + feedback banner)
  - **Implementation details:**
    - Removed Smart Subtitles toggle (always enabled)
    - Replaced vocab level dropdown with read-only Shadcn Card
    - Added "Test my level" button linking to `/onboarding/vocab-test`
    - Added feedback banner with contact email
    - Fixed WEBAPP_URL in background.ts (uses env variable)
    - Fixed externally_connectable in manifest.json (includes staging URL)
  - **Commit:** `bcd37d4` - feat(popup): Complete Phase 1B popup redesign


**Duration**: 1 week (4h backend + rest for design)
**Target completion**: October 22, 2025

---

## 📋 PHASE 2 - BILLING & SUBSCRIPTION (REVISED - Week 2-3)

**Status**: Phase 2A complete ✅, Phase 2B in progress
**Objective**: Migrate to Next.js and implement Stripe payment system

---

### 🎉 PHASE 2A - FRONTEND MOCKUPS (COMPLETED ✅ January 30, 2025)

**Duration**: 6 hours
**Deliverables**: UI flows with mockups (no backend)

- [x] **Pricing & Subscribe Pages** (2h)
  - [x] `/onboarding/pricing` page with 14-day trial offer
  - [x] `/subscribe` page for expired subscriptions
  - [x] Reusable `<PricingCard>` component

- [x] **Manage Subscription** (1h)
  - [x] `<ManageSubscriptionButton>` component
  - [x] Added to PinExtension, Complete, WelcomeBack pages

- [x] **Extension Integration** (1h)
  - [x] Subscription check in popup (redirect to /subscribe)
  - [x] Added `isSubscribed` field to types

- [x] **Testing** (2h)
  - [x] Flow 1: Onboarding → Pricing ✅
  - [x] Flow 2: Manage Subscription button ✅
  - [x] Flow 3: Extension popup redirect ✅

**Result**: Fully functional UI with alert mockups, ready for backend integration

---

### 🚧 PHASE 2B - NEXT.JS MIGRATION (IN PROGRESS - Days 1-2)

**Decision made**: January 30, 2025
**Rationale**: Next.js provides integrated full-stack architecture (frontend + backend API routes) vs maintaining separate Vite frontend + FastAPI backend for billing

**Duration**: 1-2 days (10-14h)
**Goal**: Migrate from Vite to Next.js 15 with App Router

**Day 1: Setup & Migration (6-8h)** ✅ **COMPLETED (October 31, 2025)**

- [x] **Initialize Next.js** (1h) ✅
  - [x] Create Next.js 15 project with App Router
  - [x] Configure TypeScript, Tailwind, Shadcn UI
  - [x] Setup project structure

- [x] **Migrate Supabase** (1h) ✅
  - [x] Install @supabase/ssr package (cookie-based auth for Next.js)
  - [x] Create browser + server Supabase clients
  - [x] Create middleware for session refresh
  - [x] Configure env vars (.env.local)
  - [x] Test auth connection

- [x] **Migrate Components** (2-3h) ✅
  - [x] Copy all React components (PricingCard, ManageSubscriptionButton, etc.)
  - [x] Add `'use client'` directives
  - [x] Update imports for Next.js structure
  - [x] Migrate utils (mockups.ts)

- [x] **Migrate Pages** (2-3h) ✅
  - [x] All 9 pages: welcome, welcome-back, subscribe, onboarding/* (languages, vocab-test, results, pricing, pin-extension, complete)
  - [x] Update routing to Next.js file-based structure (app/welcome/page.tsx)
  - [x] Replace useNavigate() with useRouter() from next/navigation
  - [x] Test navigation and routing

- [x] **AuthContext Migration** (1h) ✅
  - [x] Create contexts/AuthContext.tsx with 'use client'
  - [x] Create components/ClientProviders.tsx wrapper
  - [x] Integrate with app/layout.tsx
  - [x] Install sonner for toasts
  - [x] Create lib/syncExtension.ts

- [x] **End-to-End Auth Testing** (2h) ✅
  - [x] Test 7.1: Google OAuth (welcome → languages) ✅
  - [x] Test 7.2: Complete onboarding flow (7 pages) ✅
  - [x] Test 7.3: Session persistence (F5 refresh) ✅
  - [x] Test 7.4: RLS isolation (3 Google accounts tested) ✅

**Bugs Fixed During Day 1:**
- 🐛 Images missing (ulysse-photo.jpg, pin-extension-demo.gif, Netflix+pop-up.jpg) → Copied to public/
- 🐛 OAuth redirect wrong domain → Supabase URLs updated (localhost:3000 added)
- 🐛 401 Unauthorized on user_settings → RLS policies WITH CHECK added (USING + WITH CHECK required for upsert)
- 🐛 Hydration mismatch on pricing page → Date formatting fixed with explicit 'en-US' locale
- 🐛 @types/chrome missing → Installed for TypeScript compilation

**Reference Documentation:**
- Full migration plan: `NEXT_MIGRATION_PLAN.md`
- All phases + tests documented with checkboxes

**Day 2: Stripe Integration (4-6h)** ✅ **COMPLETED (November 3, 2025)**

- [x] **Stripe Setup** (30min) ✅ COMPLETED
  - [x] Created Stripe "Subly" business (test mode)
  - [x] Product: "Subly Premium" (ID: `prod_TKYdxerk6gjUJe`)
  - [x] Price: $1/month (ID: `price_1SNtWWCdkaUrc0RrUnNRVpya`)
  - [x] Enabled Customer Portal with cancellation

- [x] **Create API Routes** (2-3h) ✅ COMPLETED
  - [x] `/app/api/stripe/checkout/route.ts` - Create session with 14-day trial
  - [x] `/app/api/stripe/portal/route.ts` - Customer portal session
  - [x] `/app/api/stripe/webhook/route.ts` - Handle Stripe events (customer.subscription.*)

- [x] **Frontend Integration** (1h) ✅ COMPLETED
  - [x] Replace mockups with real API calls in `/onboarding/pricing` and `/subscribe`
  - [x] Update PricingCard and ManageSubscriptionButton components

- [x] **Localhost Testing** (2h) ✅ ALL TESTS PASSED
  - [x] **Phase 9 Tests**: Stripe CLI + localhost:3000
    - [x] Test 9.1: Signup → Trial → Stripe Checkout ✅
    - [x] Test 9.2: Webhook events (checkout.session.completed) ✅
    - [x] Test 9.3: Customer Portal (cancel subscription) ✅
    - [x] Test 9.4: RLS isolation (multi-user) ✅
  - [x] **Phase 10 Tests**: Extension localhost configuration
    - [x] Test 10.1: Extension opens localhost:3000 ✅
    - [x] Test 10.2: Extension reads subscription from Supabase ✅
  - [x] **Phase 11 Tests**: Complete E2E flow
    - [x] Test 11.1: Signup → Trial → Extension verification ✅
    - [x] Test 11.2: Subscription created in Supabase (status: trialing) ✅
    - [x] All Stripe CLI webhooks returned [200] ✅

**Architecture after Phase 2B:**
```
Next.js Monolith (Vercel)
  ├─ Frontend (React App Router pages)
  ├─ Backend (API routes for Stripe)
  └─ Calls FastAPI (subtitle processing - unchanged)

Supabase (Database + Auth - unchanged)
Stripe (Payment processing)
```

---

### ✅ PHASE 12 - STAGING DEPLOYMENT (COMPLETED - November 4, 2025)

**Duration**: 4 hours (cache issues added complexity)
**Goal**: Deploy to Vercel staging and validate E2E flow with real webhooks

**Staging Deployment** ✅ **COMPLETED**
- [x] Git commit and push to develop branch
- [x] Vercel auto-deployment triggered for staging-subly-extension.vercel.app
- [x] Stripe webhook configured for staging URL
- [x] Webhook signing secret added to Vercel environment variables
- [x] Vercel redeployment to apply new env vars
- [x] Extension built in staging mode (`npm run build:staging`)

**🐛 CRITICAL ISSUE - Vercel Wrong Directory** ✅ **RESOLVED**

**Root Cause**: Vercel was building wrong directory (`webapp/` Vite instead of `webapp-next/` Next.js)

**Resolution**:
- [x] Changed Vercel Framework Preset: Vite → Next.js
- [x] Changed Vercel Root Directory: `webapp` → `webapp-next`
- [x] Fixed Stripe `apiVersion` TypeScript error (removed parameter)
- [x] Added Supabase OAuth callback URLs for staging/production
- [x] Configured `NEXT_PUBLIC_APP_URL` per environment (Development/Preview/Production)

**Commits**:
- `5f2f327` - fix(stripe): Remove apiVersion to use Stripe default
- `017d73c` - fix(vercel): Add prebuild script to clear .next cache before build

**Staging Tests** ✅ **ALL PASSED**
- [x] Test 12.1: Signup → Trial → Stripe Checkout (staging) ✅
- [x] Test 12.2: Webhook received by Vercel (not Stripe CLI) ✅
- [x] Test 12.3: OAuth redirect to `/onboarding/languages` ✅
- [x] Test 12.4: Stripe redirect to `/onboarding/pin-extension` ✅
- [x] Test 12.5: Complete E2E flow on staging ✅

**Environment Configuration Finalized**:
- **Development**: `NEXT_PUBLIC_APP_URL=http://localhost:3000`
- **Preview**: `NEXT_PUBLIC_APP_URL=https://staging-subly-extension.vercel.app`
- **Production**: `NEXT_PUBLIC_APP_URL=https://subly-extension.vercel.app`

---

### 🎯 PHASE 2C - PRODUCTION DEPLOYMENT (Day 3)

**Duration**: 4-6 hours (realistic estimate)
**Goal**: Deploy Next.js webapp to production with live Stripe integration

**📄 Detailed checklist: [PHASE_2C_PRODUCTION.md](./PHASE_2C_PRODUCTION.md)**

- [ ] **Pre-Deployment Setup** (1h)
  - [ ] Backup Supabase database
  - [ ] Create git tag v1.0.0-pre-production
  - [ ] Document rollback plan

- [ ] **Stripe Live Mode Setup** (1h 30min)
  - [ ] Create "Subly Premium" product in LIVE mode
  - [ ] Create $1/month price with 14-day trial (note price_id)
  - [ ] Create production webhook + copy signing secret
  - [ ] Test webhook with Stripe CLI (--live mode)
  - [ ] Add STRIPE_PRICE_ID_MONTHLY env var to code (if hardcoded)

- [ ] **Vercel Configuration** (30min)
  - [ ] Add production Stripe keys (sk_live_*, whsec_live_*, price_id)
  - [ ] Verify Supabase env vars unchanged (same instance as staging)
  - [ ] Verify NEXT_PUBLIC_APP_URL set to production domain

- [ ] **Git Workflow & Deployment** (30min)
  - [ ] Create PR: develop → main
  - [ ] Review (verify no secrets in code)
  - [ ] Merge PR (Vercel auto-deploys)
  - [ ] Create git tag v1.0.0-production

- [ ] **Production Testing** (2h)
  - [ ] E2E flow: Signup → Onboarding → Stripe Checkout (test card 4242...)
  - [ ] Verify webhook [200 OK] in Stripe Dashboard
  - [ ] Verify subscription created in Supabase (status: trialing)
  - [ ] Test Customer Portal (cancel subscription)
  - [ ] Build extension production mode + test integration
  - [ ] RLS isolation test (2 Google accounts)

- [ ] **Monitoring** (1h)
  - [ ] Setup Vercel error alerts
  - [ ] Enable Stripe webhook failure alerts
  - [ ] Monitor webhook delivery (1-2h)
  - [ ] Check Vercel/Stripe/Supabase logs (no errors)

- [ ] **Post-Deployment** (30min)
  - [ ] Update ROADMAP.md (check boxes, add completion date)
  - [ ] Final smoke tests
  - [ ] **✅ FINAL:** Production ready

**Total Phase 2 Duration**: 2-3 days (was 1 week)
**Target completion**: February 2, 2025

---

### 🧹 NETTOYAGE POST-MIGRATION (30 min)

**Objectif**: Supprimer l'ancien webapp Vite une fois Next.js validé en production

**🚨 ATTENTION: Faire ces étapes SEULEMENT après déploiement production Next.js réussi**

- [ ] Tester staging Next.js pendant 24-48h (pas de bugs critiques)
- [ ] Déployer Next.js en production (`git push origin main`)
- [ ] Vérifier que production fonctionne (auth, billing, extension)
- [ ] **BACKUP webapp/ Vite** (zip ou git tag) avant suppression
- [ ] Supprimer dossier `webapp/` (ancien Vite)
- [ ] Renommer `webapp-next/` → `webapp/` (optionnel)
- [ ] Mettre à jour `.gitignore` si nécessaire
- [ ] Supprimer `NEXT_MIGRATION_PLAN.md` (migration complète)
- [ ] Commit: `git commit -m "chore: Remove old Vite webapp after Next.js migration"`

---

## 🚀 PHASE 3 - PRODUCTION LAUNCH (WEEK 3)

**Objective**: Deploy to production and launch on Chrome Web Store

### Production Setup

- [ ] **Infrastructure**
  - [ ] Deploy webapp to Vercel/Netlify
  - [ ] Update Supabase redirect URLs (production domain)
  - [ ] Update Stripe webhook URL (production)
  - [ ] Configure environment variables

- [ ] **Extension Build**
  - [ ] Build extension for production (`npm run build:production`)
  - [ ] Test production build locally
  - [ ] Prepare Chrome Web Store assets

### Launch

- [ ] **Chrome Web Store Submission**
  - [ ] Upload extension package
  - [ ] Add screenshots and description
  - [ ] Submit for review

- [ ] **Monitoring**
  - [ ] Setup error tracking (Sentry)
  - [ ] Monitor Supabase usage
  - [ ] Monitor Stripe webhooks
  - [ ] Setup analytics

**Duration**: 1 week
**Target completion**: November 5, 2025

---

## 🔮 PHASE 4 - POST-LAUNCH IMPROVEMENTS (ONGOING)

- [ ] User feedback integration
- [ ] Performance optimizations
- [ ] Additional language support
- [ ] Advanced statistics dashboard
- [ ] Mobile companion app (future)

---

## 📝 NOTES & DECISIONS

### Architecture Decisions

**Webapp externe vs Extension Pages** (October 15, 2025)
- ✅ **Decision**: Webapp externe (localhost:5173 → production URL)
- **Reason**: Auth + multi-device sync + account management requires backend
- **Pattern**: Same as Language Reactor, Grammarly, Loom

**Anonymous Sign-ins vs Direct Auth** (October 15, 2025)
- ✅ **Decision**: Direct Auth (Google OAuth only for Phase 1B)
- **Reason**: Avoid 2-step setup (anonymous then convert), cleaner architecture
- **Trade-off**: Signup required before testing (acceptable for our use case)
- **Future**: Email/Password can be added in Phase 2+ without migration

**Session Sharing: Message Passing** (January 18, 2025)
- ✅ **Decision**: Message Passing (webapp → extension token transfer)
- **Reason**: Webapp and Extension = 2 separate domains, sessions not auto-shared
- **Pattern**: Standard for Firebase, Auth0, Supabase Chrome extensions
- **Implementation**:
  - Webapp sends access_token + refresh_token via `chrome.runtime.sendMessage`
  - Extension receives via `onMessageExternal` and calls `supabase.auth.setSession()`
  - Sync on TOKEN_REFRESHED to prevent Supabase rolling token desync
- **Security**: Validate sender origin, timeout handling, fixed extension ID
- **Trade-off**: 30min implementation vs 3h refactor to extension-first OAuth
- **Alternatives Considered**:
  - Extension-first OAuth: Rejected (onboarding already in React webapp)
  - Cookie-based: Rejected (requires sensitive permissions, complex setup)
  - Double login: Rejected (bad UX)

**Vite vs Next.js for Webapp** (January 30, 2025)
- ✅ **Decision**: Migrate from Vite to Next.js 15 (App Router)
- **Reason**: Full-stack architecture needed for Stripe integration (billing backend)
- **Analysis**:
  - **Before**: Vite frontend + separate FastAPI backend for billing = 2 deployments, CORS, auth complexity
  - **After**: Next.js monolith = frontend + backend API routes in one codebase
- **Benefits**:
  - Industry standard for SaaS (Stripe docs recommend Next.js)
  - Built-in API routes (no separate backend service needed)
  - Future-proof for analytics, admin dashboard, server actions
  - Better DX (hot reload frontend + backend)
  - No technical debt vs FastAPI billing split
- **What stays unchanged**:
  - FastAPI subtitle processing backend (Railway) - called as external API
  - Supabase database schema (no changes)
  - Chrome extension (no changes)
  - React components (copy-paste with `'use client'`)
- **Migration cost**: 1-2 days now vs 2-4 days later + refactor billing
- **Alternatives Considered**:
  - Option A: Add billing routes to existing FastAPI (subtitle processing) backend
    - Rejected: Mixes subtitle processing + billing concerns, not clean architecture
  - Option B: Keep Vite + create separate FastAPI billing backend
    - Rejected: 2 backends to maintain, CORS complexity, auth sharing issues
  - Option C: Supabase Edge Functions for billing
    - Rejected: Deno runtime (not Node.js), cold start latency, debugging harder
- **Consensus**: ChatGPT + Claude + Senior Dev analysis all recommended Next.js

**Future Architecture Reevaluation** (Phase 3 Note)
- **Trigger**: When popup UI is migrated to React + Shadcn
- **Consideration**: At that point, React will be bundled in extension anyway
- **Option**: Evaluate migrating onboarding into extension (chrome-extension:// domain)
  - Would eliminate message passing complexity
  - Single domain = simpler auth flow
  - Decision deferred until Phase 3 (after popup React migration)
- **Action**: Reassess based on message passing stability in production

---

## 📚 CODE REFERENCE

### Code 1: user_settings table schema

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

### Code 1b: vocab_levels table schema (Multi-language support)

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

### Code 1c: subscriptions table schema (Phase 2 - structure created now)

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

### Code 2: known_words table schema

```sql
create table known_words (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  word text not null,
  language text not null,
  added_at timestamp with time zone default now(),
  unique(user_id, word, language)
);

-- Enable RLS
alter table known_words enable row level security;

-- Index for fast lookups
create index known_words_user_id_idx on known_words(user_id);
create index known_words_word_idx on known_words(word);
```

### Code 3: Row Level Security policies

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

-- known_words policies
create policy "Users can view own words"
  on known_words for select
  using (auth.uid() = user_id);

create policy "Users can insert own words"
  on known_words for insert
  with check (auth.uid() = user_id);

create policy "Users can delete own words"
  on known_words for delete
  using (auth.uid() = user_id);
```

### Code 4: Supabase client configuration (webapp)

```typescript
// webapp/src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Code 5: AuthContext React component

```typescript
// webapp/src/contexts/AuthContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'
import { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'

type AuthContextType = {
  user: User | null
  loading: boolean
  signInWithGoogle: () => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/onboarding/languages` }
    })
    if (error) throw error
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }

  return (
    <AuthContext.Provider value={{ user, loading, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

### Code 6: Welcome page with Google OAuth (Simplified - Google OAuth only)

```typescript
// webapp/src/pages/Welcome.tsx
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { useNavigate } from 'react-router-dom'

export default function Welcome() {
  const { user, signInWithGoogle, signOut } = useAuth()
  const navigate = useNavigate()

  const handleAuth = async () => {
    try {
      await signInWithGoogle()
      // Redirect handled by Supabase redirectTo option
    } catch (error) {
      console.error('Auth error:', error)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button (top-right, only visible after auth) */}
      {user && (
        <div className="absolute top-4 right-4">
          <Button variant="ghost" onClick={signOut}>
            Log out
          </Button>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <img
          src="/ulysse-photo.jpg"
          alt="Ulysse"
          className="w-32 h-32 rounded-full mb-6"
        />

        <h1 className="text-3xl font-bold text-center mb-4">
          Thanks for downloading my extension, my name is Ulysse and I learned
          to code just to build this extension. Hope you'll enjoy it!
        </h1>

        <p className="text-lg text-center mb-6">
          To use the extension, you first need to create an account and set it up
        </p>

        <Button onClick={handleAuth} size="lg" className="mb-2">
          Create an account and set up Subly
        </Button>

        <p className="text-sm text-muted-foreground mb-4">
          It only takes 3 steps
        </p>

        <button
          onClick={handleAuth}
          className="text-sm text-primary underline"
        >
          Already have an account? login with google
        </button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
```

### Code 7: Chrome Storage Adapter for Supabase

```typescript
// extension/src/lib/supabase-storage-adapter.ts
import { SupabaseClientOptions } from '@supabase/supabase-js'

export const chromeStorageAdapter: SupabaseClientOptions['auth']['storage'] = {
  getItem: async (key: string) => {
    const result = await chrome.storage.local.get(key)
    return result[key] || null
  },
  setItem: async (key: string, value: string) => {
    await chrome.storage.local.set({ [key]: value })
  },
  removeItem: async (key: string) => {
    await chrome.storage.local.remove(key)
  },
}

// extension/src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import { chromeStorageAdapter } from './supabase-storage-adapter'

export const supabase = createClient(
  process.env.VITE_SUPABASE_URL!,
  process.env.VITE_SUPABASE_ANON_KEY!,
  {
    auth: {
      storage: chromeStorageAdapter,
      autoRefreshToken: true,
      persistSession: true,
    },
  }
)
```

### Code 8: Stripe webhook handler (Supabase Edge Function)

```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@12.0.0?target=deno'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
})

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')!
  const body = await req.text()

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')!
    )
  } catch (err) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 })
  }

  // Handle subscription events
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      const userId = session.metadata?.user_id

      if (userId) {
        await supabase
          .from('subscriptions')
          .insert({
            user_id: userId,
            stripe_customer_id: session.customer,
            stripe_subscription_id: session.subscription,
            status: 'active',
          })
      }
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

  return new Response(JSON.stringify({ received: true }), { status: 200 })
})
```

---

**Last updated**: January 17, 2025
**Next milestone**: Complete Supabase Auth setup (Phase 1B)

**Changes in v2.0:**
- Updated project name to "Subly"
- Google OAuth only for Phase 1B (no email/password)
- Added vocab_levels table for multi-language support
- Added subscriptions table (Phase 2 structure)
- Simplified AuthContext (removed signIn/signUp functions)
- Updated Welcome page with Google OAuth button
- Added Shadcn Card and Alert components
- Added fixed feedback banner on all pages
- Updated RLS policies for new tables

**Changes in v2.1:**
- Added incremental testing strategy (10 tests total)
- Specified use of Supabase Dashboard (not MCP) for database setup
- Clarified Service Role Key usage (Phase 2 only)
- Structured Phase 1B in 5 clear steps with tests after each
- Added explicit pass criteria for each test

**Changes in v2.2 (Implementation Clarifications - January 2025):**
- **Vocab Levels**: Confirmed 12 levels (100, 200, 300, 500, 700, 1000, 1500, 2000, 2500, 3000, 4000, 5000) as per Code 1b
- **Webapp Routes**: 7 new routes replace existing Phase 1A routes (/welcome, /onboarding/languages, /onboarding/vocab-test, /onboarding/results, /onboarding/pin-extension, /onboarding/complete, /welcome-back)
- **OAuth Redirect**: Use `window.location.origin` for dynamic dev/prod redirect URLs
- **Extension Background**: Modified to open `/welcome` route (instead of `/onboarding`)
- **Database Tables**: Create all 4 tables in Phase 1B (user_settings, vocab_levels, subscriptions, known_words) even if known_words unused until Phase 3
- **Shadcn Components**: Install Card, Alert, Toast (Toast for success/error notifications)
