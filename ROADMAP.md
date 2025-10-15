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

**Objective**: Setup Supabase Auth (Google OAuth + Email/Password) for user accounts and data synchronization

### Backend Setup (Day 1 - 4 hours)

- [ ] **Supabase Project Setup** (30min)
  - [ ] Create Supabase account
  - [ ] Create new project "smart-subtitles"
  - [ ] Note: Project URL + Anon Key

- [ ] **Database Schema** (30min)
  - [ ] Create `user_settings` table [voir Code 1]
  - [ ] Create `known_words` table [voir Code 2]
  - [ ] Setup Row Level Security (RLS) policies [voir Code 3]

- [ ] **Authentication Configuration** (1h)
  - [ ] Enable Google OAuth provider
  - [ ] Configure redirect URLs (localhost + production)
  - [ ] Enable Email/Password authentication
  - [ ] Configure email templates

- [ ] **Webapp Integration** (1h 30min)
  - [ ] Install `@supabase/supabase-js` in webapp
  - [ ] Create Supabase client configuration [voir Code 4]
  - [ ] Create AuthContext React component [voir Code 5]
  - [ ] Create Login/Signup page UI [voir Code 6]
  - [ ] Add "Sign in with Google" button
  - [ ] Add Email/Password form

- [ ] **Extension Integration** (30min)
  - [ ] Install `@supabase/supabase-js` in extension
  - [ ] Configure Supabase client in extension
  - [ ] Add custom Storage Adapter for chrome.storage [voir Code 7]

- [ ] **Testing** (30min)
  - [ ] Test Google OAuth flow
  - [ ] Test Email/Password signup
  - [ ] Test session persistence
  - [ ] Verify sync between webapp and extension

### Design Work (Days 2-5)

- [ ] **Onboarding Flow Design**
  - [ ] Step 1: Welcome screen
  - [ ] Step 2: Language selection (target + native)
  - [ ] Step 3: Vocabulary test
  - [ ] Step 4: Pin extension reminder
  - [ ] Step 5: Success message

- [ ] **Subtitles Appearance**
  - [ ] Font styling improvements
  - [ ] Color scheme updates
  - [ ] Positioning options
  - [ ] Inline translation styling

- [ ] **Popup UI Design**
  - [ ] Settings panel redesign
  - [ ] Language selector UI
  - [ ] Quick actions menu

- [ ] **Dashboard UI Polish**
  - [ ] Known words list view
  - [ ] Learning statistics charts
  - [ ] Profile settings page

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
- ✅ **Decision**: Direct Auth (Google OAuth + Email/Password)
- **Reason**: Avoid 2-step setup (anonymous then convert), cleaner architecture
- **Trade-off**: Signup required before testing (acceptable for our use case)

**LocalStorage vs Message Passing vs Supabase** (October 15, 2025)
- ✅ **Decision**: Supabase direct (no message passing)
- **Reason**: Permanent code, multi-device sync, no migration needed
- **Cost**: 1-2h setup vs 0h LocalStorage + 1-2h migration later (same total time)

---

## 📚 CODE REFERENCE

### Code 1: user_settings table schema

```sql
create table user_settings (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  target_lang text not null,
  native_lang text not null,
  vocab_level integer default 5000,
  inline_translation boolean default true,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now(),
  unique(user_id)
);

-- Enable RLS
alter table user_settings enable row level security;
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
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
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

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw error
  }

  const signUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) throw error
  }

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/onboarding` }
    })
    if (error) throw error
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signInWithGoogle, signOut }}>
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

### Code 6: Login/Signup page UI

```typescript
// webapp/src/pages/Login.tsx
import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function Login() {
  const { signIn, signUp, signInWithGoogle } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (isSignUp) {
        await signUp(email, password)
      } else {
        await signIn(email, password)
      }
    } catch (error) {
      console.error('Auth error:', error)
    }
  }

  return (
    <div className="max-w-md mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">
        {isSignUp ? 'Create Account' : 'Sign In'}
      </h1>

      <Button
        onClick={signInWithGoogle}
        variant="outline"
        className="w-full mb-4"
      >
        Continue with Google
      </Button>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">Or</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <Button type="submit" className="w-full">
          {isSignUp ? 'Sign Up' : 'Sign In'}
        </Button>
      </form>

      <p className="mt-4 text-center text-sm">
        {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
        <button
          onClick={() => setIsSignUp(!isSignUp)}
          className="text-primary underline"
        >
          {isSignUp ? 'Sign In' : 'Sign Up'}
        </button>
      </p>
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

**Last updated**: October 15, 2025
**Next milestone**: Complete Supabase Auth setup (Phase 1B)
