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

## 📋 PHASE 2 - BILLING & SUBSCRIPTION (WEEK 2)

**Objective**: Implement payment system with Stripe for subscription management

### Stripe Setup (Day 1 - 2 hours)

- [ ] **Stripe Account** (30min)
  - [ ] Create Stripe account
  - [ ] Enable test mode
  - [ ] Configure products and pricing
  - [ ] Note: API keys (test + production)

- [ ] **Stripe Integration** (1h 30min)
  - [ ] Install Stripe SDK in webapp
  - [ ] Create checkout session endpoint
  - [ ] Setup webhook endpoint for Stripe events
  - [ ] Configure Supabase Edge Function for webhooks [voir Code 8]

### Billing UI (Day 2 - 2 hours)

- [ ] **Pricing Page** (1h)
  - [ ] Display subscription plans
  - [ ] "Subscribe" button → Stripe Checkout
  - [ ] Free trial banner

- [ ] **Account Management** (1h)
  - [ ] View current subscription
  - [ ] Cancel subscription button
  - [ ] Update payment method
  - [ ] Billing history

### Testing & Validation (Day 3 - 2 hours)

- [ ] **End-to-End Testing**
  - [ ] Test checkout flow (test cards)
  - [ ] Test webhook reception
  - [ ] Test subscription activation
  - [ ] Test cancellation flow
  - [ ] Verify RLS policies enforce subscription status

**Duration**: 1 week (6h billing + rest for polish)
**Target completion**: October 29, 2025

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
