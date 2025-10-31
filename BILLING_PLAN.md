# BILLING & PAYMENT IMPLEMENTATION PLAN

**Date Created:** January 29, 2025
**Status:** Phase 2A - Frontend Implementation
**Trial Duration:** 14 days
**Initial Pricing:** $1/month (first 10 users)

---

## 📋 PHASE 2A - FRONTEND ROADMAP (Current)

**Goal:** Build and validate all UI flows without backend integration

### Step 1: Setup & Preparation (30min)
- [x] Create `<PricingCard>` reusable component (see Section 3.1)
- [x] Install any missing Shadcn components (`npm install`)
- [x] Create mockup utility functions (see Section 3.2)
- [x] **✅ TEST 1:** Run `npm run dev`, verify webapp loads

### Step 2: Pricing Page (1h)
- [x] Create `/onboarding/pricing` page (see Section 3.3)
- [x] Use `<PricingCard context="onboarding">`
- [x] Add "Start Free Trial" button → Simple alert mockup
- [x] Update routing in App.tsx (see Section 3.4)
- [x] **✅ TEST 2:** Navigate to `/onboarding/pricing`, verify UI renders

### Step 3: Subscribe Page (30min)
- [x] Create `/subscribe` page for expired trials (see Section 3.5)
- [x] Reuse `<PricingCard context="expired">`
- [x] Add "Subscribe Now" button → Same alert mockup
- [x] **✅ TEST 3:** Navigate to `/subscribe`, verify UI renders

### Step 4: Manage Subscription Button (45min)
- [x] Create `<ManageSubscriptionButton>` component (see Section 3.6)
- [x] Add to header (top-right, next to Logout)
- [x] Button opens alert mockup (simulate Stripe Portal)
- [x] Test on `/pin-extension`, `/complete`, `/welcome-back` pages
- [x] **✅ TEST 4:** Click button, verify alert shows "Stripe Portal (mockup)"

### Step 5: Update Onboarding Flow (30min)
- [x] Update `Results.tsx` → Navigate to `/pricing` (see Section 3.7)
- [x] Verify routing: Results → Pricing → Pin Extension → Complete
- [x] **✅ TEST 5:** Complete full onboarding flow (Welcome → Complete)

### Step 6: Extension Popup Mockup (30min) - SIMPLIFIED APPROACH (Option B+)
- [x] Add subscription status HTML element below Process Subtitles button
- [x] Add CSS styling for subscription status text
- [x] Update TypeScript types to include `isSubscribed` field
- [x] Load `isSubscribed` from chrome.storage.local (default: false)
- [x] Create `updateSubscriptionStatus()` function to show/hide text
- [x] Modify `processSubtitles()` to redirect to `/subscribe` when not subscribed
- [x] Build extension: `npm run build:staging` ✅
- [x] **✅ TEST 6:** Load extension, test subscription check with console commands

### Step 7: End-to-End Flow Testing (1h)
- [x] **Flow 1:** Complete onboarding → Pricing mockup ✅ PASSED (January 30, 2025)
- [x] **Flow 2:** Click "Manage Subscription" → Portal mockup ✅ PASSED (January 30, 2025)
- [x] **Flow 3:** Extension popup redirect to /subscribe ✅ PASSED (January 30, 2025)
- [x] Document any UX issues: Removed "Manage subscription" link from Subscribe page (cleaner UX)
- [x] **✅ TEST 7:** All 3 flows work without errors ✅ PASSED

### Step 8: Code Review & Cleanup (30min)
- [x] Remove console.logs - None found in new files ✅
- [x] Check all mockup alerts have "(mockup)" in text ✅
- [x] No dead code detected ✅
- [x] Commit to git: "feat(billing): Complete Phase 2A frontend" ✅
- [x] **✅ FINAL:** Push to `develop` branch, verify Vercel preview ✅

**Total Time Estimate:** 6 hours
**Deliverables:** Fully functional UI flows (mockups only, no backend)

---

## 📋 PHASE 2B - BACKEND ROADMAP (Next)

**Goal:** Connect frontend to Stripe API (replace mockups with real integration)

### Step 1: Stripe Setup (30min)
- [ ] Create Stripe account (test mode)
- [ ] Create product "Subly Premium" (see Section 5.1)
- [ ] Create 3 prices: $1, $2, $5/month (see Section 5.2)
- [ ] Enable Stripe Checkout
- [ ] Enable Customer Portal (allow cancellation)
- [ ] **✅ TEST 1:** Test checkout with card `4242 4242 4242 4242`

### Step 2: Backend Endpoints (3h)
- [ ] Create `/create-checkout-session` endpoint (see Section 5.3)
- [ ] Create `/create-portal-session` endpoint (see Section 5.4)
- [ ] Create `/stripe-webhook` handler (see Section 5.5)
- [ ] Add Stripe SDK to requirements.txt
- [ ] **✅ TEST 2:** cURL test endpoints, verify responses

### Step 3: Webhook Configuration (30min)
- [ ] Deploy backend to Railway
- [ ] Configure webhook endpoint in Stripe Dashboard (see Section 5.6)
- [ ] Add webhook secret to environment variables
- [ ] **✅ TEST 3:** Trigger test webhook, verify Supabase update

### Step 4: Frontend Integration (1h)
- [ ] Replace mockup alerts with real API calls (see Section 5.7)
- [ ] Update `VITE_USE_MOCKUPS=false` in production
- [ ] Test checkout flow with real Stripe Checkout
- [ ] **✅ TEST 4:** Complete checkout, verify redirect to /pin-extension

### Step 5: Extension Integration (1h)
- [ ] Replace `checkSubscriptionMockup()` with real Supabase query (see Section 5.8)
- [ ] Remove debug controls from production build
- [ ] Test blocking logic with different subscription statuses
- [ ] **✅ TEST 5:** Extension blocks when status='canceled'

### Step 6: End-to-End Testing (1h)
- [ ] Test full flow: Signup → Trial → Payment → Use extension
- [ ] Test cancellation flow: Cancel → Extension blocks
- [ ] Test webhook events in Stripe Dashboard logs
- [ ] Verify Supabase data updates correctly
- [ ] **✅ TEST 6:** All flows work with real Stripe

**Total Time Estimate:** 7 hours
**Deliverables:** Fully functional payment system (production-ready)

---

## 🎯 KEY DECISIONS

### Decision 1: Trial WITH Credit Card Upfront ✅

**Choice:** Stripe Checkout with 14-day free trial, credit card required at signup

**Rationale:**
- ✅ **3x simpler implementation** (165 lines vs 400+ lines)
- ✅ **2-5x better conversion** (25-50% vs 10-15%)
- ✅ **Automatic trial management** by Stripe
- ✅ **Stripe Portal for cancellation** (0 lines of code)
- ✅ **Automatic emails** from Stripe (no email service needed)

**Alternative Rejected:** Trial WITHOUT card
- ❌ 20h dev time vs 6h
- ❌ Manual trial tracking (CRON jobs)
- ❌ Custom payment method collection page
- ❌ Low conversion rate

---

### Decision 2: Trial Duration = 14 Days ✅

**Choice:** 14-day free trial (was considering 7 or 30 days)

**Rationale:**
- Long enough for user to test on multiple episodes
- Short enough to maintain urgency
- Industry standard (Netflix, Spotify use similar)
- Easy to change via single variable if needed

---

### Decision 3: Post-Trial Behavior = Full Block ✅

**Choice:** After trial ends without payment, extension is completely blocked

**Alternatives Rejected:**
- ❌ 1 episode/week free tier (too complex for MVP)
- ❌ Feature downgrade (too complex for MVP)

**Implementation:** Simple status check: `if status !== 'trialing' or 'active' → block`

---

### Decision 4: No Refund Policy (Trial Sufficient) ✅

**Choice:** No refund policy needed

**Rationale:**
- 14-day free trial is generous
- User can cancel anytime during trial (never charged)
- Simplifies legal/support burden

---

### Decision 5: Cancellation via Stripe Portal ✅

**Choice:** Use Stripe Customer Portal (hosted by Stripe)

**Rationale:**
- 0 lines of code required
- Stripe handles all UI/UX
- Also provides: update card, view invoices, reactivate subscription
- Standard industry pattern

**Implementation:** Single "Manage Subscription" button → opens Portal

---

### Decision 6: Pricing Strategy - Progressive Manual Pricing ✅

**Strategy:** Start low, increase gradually as product matures

**Pricing Tiers:**
- **First 10 users:** $1/month (reward early adopters, compensate for bugs)
- **Next 90 users (10-100):** $2/month
- **Next 900 users (100-1000):** $5/month
- **1000+ users:** TBD (likely $9.99/month)

**Technical Implementation:**
```python
# Config variable (change manually)
CURRENT_PRICE_ID = "price_1_dollar"  # → "price_2_dollars" after 10 users
```

**Important:** Existing users keep their original price (Stripe doesn't auto-migrate)

---

### Decision 7: No Advanced Features for MVP ✅

**Excluded from Phase 2 (add later if needed):**
- ❌ Annual pricing (monthly only for now)
- ❌ Student discounts
- ❌ Custom refund policy
- ❌ Freemium tier
- ❌ Custom email notifications (Stripe auto-emails sufficient)

---

## 🚀 USER WORKFLOWS

### Workflow 1: New User Signs Up and Subscribes

```
1. Install extension → Opens webapp at /welcome
2. Google OAuth → Authenticated
3. /onboarding/languages → Selects PT-BR + French
4. /onboarding/vocab-test → Tests vocabulary → 2000 words
5. /onboarding/results → "You know 2000 words"
6. 💳 /onboarding/pricing → Clicks "Start Free Trial"
   → Redirects to Stripe Checkout
   → Enters credit card
   → Stripe creates subscription (status='trialing')
7. Webhook → Saves to Supabase subscriptions table
8. Redirect → /onboarding/pin-extension
9. /onboarding/complete → "You're all set!"
10. Uses extension on Netflix for 14 days (no charge)
11. Day 15 → Stripe automatically charges $1 (status='active')
12. Continues using extension ✅
```

---

### Workflow 2: User Cancels During Trial

```
1-9. Same as Workflow 1
10. Day 5 → User clicks "Manage Subscription" button (top-right)
11. Stripe Portal opens in new tab
12. User clicks "Cancel subscription"
13. Stripe sends webhook → status='canceled' in Supabase
14. Extension immediately blocked (popup shows "Subscribe to continue")
15. User is NEVER charged ✅
```

---

### Workflow 3: User Cancels After 2 Months of Payment

```
1-12. Same as Workflow 1 (user has paid $1 + $1 = $2 total)
13. Month 3 → User clicks "Manage Subscription"
14. Stripe Portal → Cancels subscription
15. Webhook → status='canceled'
16. Extension blocked
17. Stripe stops charging ✅
```

---

### Workflow 4: Trial Expires, User Not Subscribed

```
1-10. User completes trial but never entered card (edge case)
11. Day 15 → Stripe fails to charge (no payment method)
12. Webhook → status='past_due' or 'canceled'
13. User opens extension popup
14. checkSubscriptionStatus() → status invalid
15. Popup shows:
    ┌──────────────────────────────────┐
    │ Your trial has ended             │
    │ Subscribe to continue ($1/month) │
    │ [Subscribe Now] ← Opens /pricing │
    └──────────────────────────────────┘
16. User clicks → /pricing page → Stripe Checkout → Subscribes ✅
```

---

## 🎨 UI/UX DESIGN DECISIONS

### Paywall Placement

**Location:** `/onboarding/pricing` (between Results and Pin Extension)

**Rationale:**
- User has already invested time (sunk cost effect)
- User has seen the value (tested vocabulary, saw results)
- Before final "complete" screen (natural checkpoint)

**UI Elements:**
```
┌─────────────────────────────────────┐
│  Start Your 14-Day Free Trial      │
├─────────────────────────────────────┤
│  $1/month after trial               │
│  (Special price for first 10 users) │
│                                     │
│  ✅ Adapt subtitles to your level  │
│  ✅ AI inline translations         │
│  ✅ Works on any device            │
│  ✅ Cancel anytime                 │
│                                     │
│  Trial ends: February 12, 2025     │
│  You won't be charged until then   │
│                                     │
│  [Start Free Trial] ← Stripe       │
└─────────────────────────────────────┘
```

---

### "Manage Subscription" Button

**Location:** Top-right corner, next to "Log out" button

**Visible on:** All onboarding pages + webapp pages (after signup)

**Behavior:** Opens Stripe Customer Portal in new tab

**Code (React):**
```tsx
<div className="header-actions">
  <Button variant="ghost" onClick={handleManageSubscription}>
    Manage Subscription
  </Button>
  <Button variant="ghost" onClick={signOut}>
    Log out
  </Button>
</div>
```

---

### "Not Subscribed" State (Extension Popup)

**Trigger:** User opens popup, subscription status is invalid

**UI:**
```
┌─────────────────────────────────┐
│  ⚠️ Your trial has ended        │
├─────────────────────────────────┤
│  Subscribe to continue using    │
│  Subly for $1/month             │
│                                 │
│  [Subscribe Now]                │
│                                 │
│  (Process Subtitles button      │
│   is hidden/disabled)           │
└─────────────────────────────────┘
```

**"Subscribe Now" button:** Opens `/pricing` in new tab

---

### "Not Subscribed" Page (Webapp)

**Route:** `/subscribe` (or reuse `/pricing`)

**Trigger:** User navigates from extension popup or direct link

**UI:**
```
┌─────────────────────────────────────┐
│  Your free trial has ended          │
├─────────────────────────────────────┤
│  Subscribe to continue using Subly  │
│                                     │
│  💳 $1/month                        │
│  ✅ Cancel anytime                 │
│  ✅ Works on any device            │
│                                     │
│  [Subscribe Now]                    │
│                                     │
│  Already subscribed?                │
│  [Manage your subscription]         │
└─────────────────────────────────────┘
```

---

## 📧 EMAIL NOTIFICATIONS (Automatic via Stripe)

**Setup:** Enable in Stripe Dashboard → Settings → Emails

**Emails Sent Automatically (0 code required):**
1. ✅ **Successful payment** (after trial ends, first charge)
2. ✅ **Failed payment** (if card declined)
3. ✅ **Upcoming invoice** (2 days before trial ends)
4. ✅ **Subscription canceled** (confirmation email)

**Email Preview (Day 12 of trial):**
```
Subject: Your Subly trial ends in 2 days

Hi [User],

Your 14-day free trial of Subly ends on February 12, 2025.

You'll be charged $1.00 on that date unless you cancel.

To cancel: [Manage Subscription] (opens Stripe Portal)

Thanks,
The Subly Team
```

---

## 🔧 TECHNICAL IMPLEMENTATION SUMMARY

### MVP Checklist (Phase 2 - Billing)

**Frontend (Webapp):**
- [ ] `/onboarding/pricing` page (40 lines)
- [ ] "Manage Subscription" button component (10 lines)
- [ ] `/subscribe` page for expired trials (30 lines)
- [ ] Update onboarding flow routing (10 lines)

**Backend (FastAPI):**
- [ ] `POST /create-checkout-session` endpoint (30 lines)
- [ ] `POST /create-portal-session` endpoint (15 lines)
- [ ] `POST /stripe-webhook` handler (50 lines)

**Extension (Chrome):**
- [ ] `checkSubscriptionStatus()` function (30 lines)
- [ ] "Not subscribed" UI in popup (20 lines)

**Stripe Setup (Dashboard):**
- [ ] Create product "Subly Premium"
- [ ] Create prices: $1, $2, $5 per month
- [ ] Enable Stripe Checkout
- [ ] Enable Customer Portal (allow cancellation)
- [ ] Configure webhook endpoint
- [ ] Enable automatic emails

**Database (Supabase):**
- ✅ Already created in Phase 1B (subscriptions table)
- [ ] Add RLS policies for subscriptions (if not done)

**Total Estimated Time:** 6 hours development

---

## 🎯 COMPLEXITY COMPARISON

| Feature | With Card Upfront | Without Card |
|---------|------------------|--------------|
| **Lines of code** | 165 | 400+ |
| **Dev time** | 6h | 20h |
| **Endpoints** | 2 | 6+ |
| **Pages (webapp)** | 1 | 3+ |
| **Trial tracking** | Stripe (auto) | Manual (CRON) |
| **Cancellation** | Portal (0 lines) | Custom (50 lines) |
| **Emails** | Stripe (auto) | Custom service |
| **Bugs risk** | Low | High |
| **Conversion rate** | 25-50% | 10-15% |

**Decision:** With card upfront = clear winner for solo dev

---

## 📊 SUBSCRIPTION STATUS LOGIC

### Status Values (Stripe → Supabase)

| Stripe Status | Supabase Status | Extension Access |
|--------------|----------------|-----------------|
| `trialing` | `trialing` | ✅ Allowed |
| `active` | `active` | ✅ Allowed |
| `past_due` | `past_due` | ❌ Blocked |
| `canceled` | `canceled` | ❌ Blocked |
| `unpaid` | `unpaid` | ❌ Blocked |
| (none) | (null) | ❌ Blocked |

### Extension Check Logic

```typescript
// popup.ts
const { data: sub } = await supabase
  .from('subscriptions')
  .select('status')
  .eq('user_id', user.id)
  .single()

// Allow access only if trialing or active
const hasAccess = sub && ['trialing', 'active'].includes(sub.status)

if (!hasAccess) {
  showNotSubscribedUI()
} else {
  showNormalUI()
}
```

---

## 🔄 WEBHOOK EVENTS TO HANDLE

### Essential Webhooks (Phase 2)

**1. `checkout.session.completed`**
```python
# User completed Stripe Checkout → Save subscription
user_id = session.metadata.user_id
await supabase.from('subscriptions').insert({
    'user_id': user_id,
    'stripe_customer_id': session.customer,
    'stripe_subscription_id': session.subscription,
    'status': 'trialing'
})
```

**2. `customer.subscription.updated`**
```python
# Subscription status changed (trialing → active, active → canceled)
sub = event.data.object
await supabase.from('subscriptions').update({
    'status': sub.status
}).eq('stripe_subscription_id', sub.id)
```

**3. `customer.subscription.deleted`**
```python
# Subscription canceled
sub = event.data.object
await supabase.from('subscriptions').update({
    'status': 'canceled'
}).eq('stripe_subscription_id', sub.id)
```

### Optional Webhooks (Phase 3+)

- `invoice.payment_succeeded` (track successful payments)
- `invoice.payment_failed` (alert user of failed payment)

---

## 🚀 ROADMAP (To Be Filled)

### Phase 2A: Frontend Implementation (Week 1)

**Goal:** Build all UI flows without backend integration

- [ ] Create `/onboarding/pricing` page with mockup
- [ ] Add "Manage Subscription" button (links to mockup)
- [ ] Create `/subscribe` page for expired trials
- [ ] Create Stripe Checkout mockup page (simulate flow)
- [ ] Create Stripe Portal mockup page (simulate cancellation)
- [ ] Update onboarding flow routing
- [ ] Test all user flows end-to-end
- [ ] Validate UX with manual testing

**Deliverables:**
- Complete UI flows (no backend)
- All pages designed and styled
- User flows tested and validated

---

### Phase 2B: Backend Integration (Week 2)

**Goal:** Connect frontend to Stripe API

- [ ] Setup Stripe account + test mode
- [ ] Create product and prices ($1, $2, $5)
- [ ] Implement `/create-checkout-session` endpoint
- [ ] Implement `/create-portal-session` endpoint
- [ ] Implement `/stripe-webhook` handler
- [ ] Configure webhook endpoint in Stripe Dashboard
- [ ] Test checkout flow with test cards
- [ ] Test webhook reception and Supabase updates
- [ ] Test cancellation flow via Portal

**Deliverables:**
- Fully functional payment system
- Webhooks working and tested
- Stripe Dashboard configured

---

### Phase 2C: Extension Integration (Week 3)

**Goal:** Block extension based on subscription status

- [ ] Implement `checkSubscriptionStatus()` in popup
- [ ] Show "Not subscribed" UI when blocked
- [ ] Test blocking logic with different statuses
- [ ] Test end-to-end: signup → trial → payment → cancel
- [ ] Verify RLS policies prevent status manipulation

**Deliverables:**
- Extension blocks correctly when not subscribed
- All user workflows tested

---

### Phase 2D: Testing & Launch (Week 4)

**Goal:** Production-ready billing system

- [ ] Test with real credit card (test mode)
- [ ] Verify Stripe emails are sent correctly
- [ ] Test trial expiration flow
- [ ] Test cancellation during trial (no charge)
- [ ] Test cancellation after payment (no future charges)
- [ ] Switch to Stripe production mode
- [ ] Deploy to production
- [ ] Monitor first 10 users

**Deliverables:**
- Production billing system live
- Monitoring in place
- Ready for first paying users

---

## 📝 OPEN QUESTIONS / DECISIONS PENDING

- [ ] **Account page design:** Where to place "Manage Subscription" button?
  - Option A: Top-right header (next to Logout) ✅ **CHOSEN**
  - Option B: Dedicated /account page

- [ ] **Pricing page copy:** Exact wording for trial messaging
  - Draft: "Start Your 14-Day Free Trial - $1/month after"

- [ ] **Post-cancellation message:** What to show when user cancels?
  - Option A: "Subscription canceled. Access until [end date]"
  - Option B: Immediate block

- [ ] **Failed payment handling:** What happens if payment fails after trial?
  - Stripe default: Retry 3 times, then cancel
  - Custom: Send notification, give 7-day grace period?

---

## 🎓 LESSONS LEARNED (To Be Filled During Implementation)

_This section will be updated as we implement the billing system_

---

---

## 📖 SECTION 3 - PHASE 2A CODE DETAILS

### Section 3.1: `<PricingCard>` Reusable Component

**Purpose:** DRY principle - Single component used in both `/pricing` and `/subscribe`

```tsx
// webapp/src/components/PricingCard.tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface PricingCardProps {
  context: 'onboarding' | 'expired'
  onCheckout: () => void
}

export function PricingCard({ context, onCheckout }: PricingCardProps) {
  const title = context === 'onboarding'
    ? 'Start Your 14-Day Free Trial'
    : 'Your trial has ended'

  const buttonText = context === 'onboarding'
    ? 'Start Free Trial'
    : 'Subscribe Now'

  const trialEndDate = new Date()
  trialEndDate.setDate(trialEndDate.getDate() + 14)

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="text-center">
          <p className="text-4xl font-bold">$1/month</p>
          {context === 'onboarding' && (
            <p className="text-sm text-muted-foreground">
              Special price for first 10 users
            </p>
          )}
        </div>

        <ul className="space-y-2">
          <li>✅ Adapt subtitles to your level</li>
          <li>✅ AI inline translations</li>
          <li>✅ Works on any device</li>
          <li>✅ Cancel anytime</li>
        </ul>

        {context === 'onboarding' && (
          <p className="text-sm text-muted-foreground">
            Trial ends: {trialEndDate.toLocaleDateString()}
            <br />
            You won't be charged until then
          </p>
        )}

        <Button onClick={onCheckout} size="lg" className="w-full">
          {buttonText}
        </Button>

        {context === 'expired' && (
          <p className="text-sm text-center text-muted-foreground">
            Already subscribed? <a href="/account" className="underline">Manage subscription</a>
          </p>
        )}
      </CardContent>
    </Card>
  )
}
```

---

### Section 3.2: Mockup Utility Functions

**Purpose:** Simple alerts to simulate Stripe (no complex pages)

```tsx
// webapp/src/utils/mockups.ts
export function simulateStripeCheckout(onSuccess: () => void) {
  const confirmed = window.confirm(
    '🎨 MOCKUP: Stripe Checkout\n\n' +
    'Simulate successful payment?\n' +
    '(Real Stripe integration in Phase 2B)'
  )

  if (confirmed) {
    // Simulate processing delay
    setTimeout(() => {
      alert('✅ Payment successful (mockup)')
      onSuccess()
    }, 1000)
  }
}

export function simulateStripePortal() {
  const action = window.confirm(
    '🎨 MOCKUP: Stripe Customer Portal\n\n' +
    'Simulate subscription cancellation?\n' +
    '(Real Portal opens in Phase 2B)'
  )

  if (action) {
    alert('✅ Subscription canceled (mockup)')
    // In Phase 2B, webhook will update Supabase
  }
}
```

---

### Section 3.3: `/onboarding/pricing` Page

```tsx
// webapp/src/pages/onboarding/Pricing.tsx
import { useNavigate } from 'react-router-dom'
import { PricingCard } from '@/components/PricingCard'
import { simulateStripeCheckout } from '@/utils/mockups'

export default function Pricing() {
  const navigate = useNavigate()

  const handleCheckout = () => {
    simulateStripeCheckout(() => {
      navigate('/onboarding/pin-extension')
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <PricingCard context="onboarding" onCheckout={handleCheckout} />
    </div>
  )
}
```

---

### Section 3.4: Update Routing in App.tsx

```tsx
// webapp/src/App.tsx
import Pricing from './pages/onboarding/Pricing'
import Subscribe from './pages/Subscribe'

// Add to <Routes>
<Route path="/onboarding/pricing" element={<Pricing />} />
<Route path="/subscribe" element={<Subscribe />} />
```

---

### Section 3.5: `/subscribe` Page (Reuses PricingCard)

```tsx
// webapp/src/pages/Subscribe.tsx
import { PricingCard } from '@/components/PricingCard'
import { simulateStripeCheckout } from '@/utils/mockups'

export default function Subscribe() {
  const handleCheckout = () => {
    simulateStripeCheckout(() => {
      window.close() // Close tab after subscription
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <PricingCard context="expired" onCheckout={handleCheckout} />
    </div>
  )
}
```

---

### Section 3.6: `<ManageSubscriptionButton>` Component

```tsx
// webapp/src/components/ManageSubscriptionButton.tsx
import { Button } from '@/components/ui/button'
import { simulateStripePortal } from '@/utils/mockups'

export function ManageSubscriptionButton() {
  return (
    <Button variant="ghost" onClick={simulateStripePortal}>
      Manage Subscription
    </Button>
  )
}

// Add to header in Welcome.tsx, Pricing.tsx, Complete.tsx, etc.
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'

<div className="absolute top-4 right-4 flex gap-2">
  <ManageSubscriptionButton />
  <Button variant="ghost" onClick={signOut}>Log out</Button>
</div>
```

---

### Section 3.7: Update Results.tsx Navigation

```tsx
// webapp/src/pages/onboarding/Results.tsx
// Change navigation from /pin-extension to /pricing

<Button onClick={() => navigate('/onboarding/pricing')}>
  Continue
</Button>
```

---

### Section 3.8: Extension - checkSubscriptionMockup()

```typescript
// extension/src/popup/popup.ts
function checkSubscriptionMockup() {
  chrome.storage.local.get(['mockSubscriptionStatus'], (result) => {
    const status = result.mockSubscriptionStatus || 'expired'

    console.log('[MOCKUP] Subscription status:', status)

    if (status === 'trialing' || status === 'active') {
      showNormalUI()
    } else {
      showNotSubscribedUI()
    }
  })
}

// Call on popup load
document.addEventListener('DOMContentLoaded', () => {
  checkSubscriptionMockup()
})
```

---

### Section 3.9: Debug Controls (DEV Mode Only)

```typescript
// extension/src/popup/popup.ts
function addDebugControls() {
  // Only show in development builds
  const isDev = !('update_url' in chrome.runtime.getManifest())
  if (!isDev) return

  const debugDiv = document.createElement('div')
  debugDiv.style.cssText = 'border: 2px solid red; padding: 8px; margin: 8px; background: #fee;'
  debugDiv.innerHTML = `
    <p style="margin: 0 0 8px 0; font-weight: bold;">🔧 DEBUG MODE</p>
    <button id="mock-trialing" style="margin-right: 8px;">Set: Trialing</button>
    <button id="mock-active" style="margin-right: 8px;">Set: Active</button>
    <button id="mock-expired">Set: Expired</button>
  `

  document.body.insertBefore(debugDiv, document.body.firstChild)

  document.getElementById('mock-trialing')!.onclick = () => {
    chrome.storage.local.set({ mockSubscriptionStatus: 'trialing' })
    location.reload()
  }

  document.getElementById('mock-active')!.onclick = () => {
    chrome.storage.local.set({ mockSubscriptionStatus: 'active' })
    location.reload()
  }

  document.getElementById('mock-expired')!.onclick = () => {
    chrome.storage.local.set({ mockSubscriptionStatus: 'expired' })
    location.reload()
  }
}

// Call after DOMContentLoaded
addDebugControls()
```

---

### Section 3.10: Modify "Process Subtitles" Button (Option B+ - Simplified)

**Purpose:** Redirect to `/subscribe` when user is not subscribed (simple approach)

```typescript
// extension/src/popup/popup.ts

function handleProcessSubtitlesClick(isSubscribed: boolean) {
  if (!isSubscribed) {
    // Not subscribed → Open /subscribe page
    const webappUrl = process.env.WEBAPP_URL || 'http://localhost:5173'
    chrome.tabs.create({ url: `${webappUrl}/subscribe` })
    return
  }

  // Subscribed → Normal behavior (process subtitles)
  // ... existing subtitle processing code ...
}

function updateProcessButtonUI(isSubscribed: boolean) {
  const processButton = document.getElementById('process-subtitles-button')
  const subscriptionText = document.getElementById('subscription-required-text')

  if (!isSubscribed) {
    // Show "Subscription required" text below button
    if (!subscriptionText) {
      const text = document.createElement('p')
      text.id = 'subscription-required-text'
      text.style.cssText = 'color: #888; font-size: 12px; text-align: center; margin-top: 4px;'
      text.textContent = 'Subscription required'
      processButton?.parentElement?.appendChild(text)
    }
  } else {
    // Hide text if subscribed
    subscriptionText?.remove()
  }
}

// Example usage in checkSubscriptionMockup()
function checkSubscriptionMockup() {
  chrome.storage.local.get(['mockSubscriptionStatus'], (result) => {
    const status = result.mockSubscriptionStatus || 'expired'
    const isSubscribed = ['trialing', 'active'].includes(status)

    updateProcessButtonUI(isSubscribed)

    // Attach click handler
    const processButton = document.getElementById('process-subtitles-button')
    processButton?.addEventListener('click', () => {
      handleProcessSubtitlesClick(isSubscribed)
    })
  })
}
```

**Result:**
- **If subscribed:** Button works normally
- **If NOT subscribed:** Button opens `/subscribe` page + shows "Subscription required" text below

---

## 📖 SECTION 4 - TEST FLOWS (Phase 2A)

### Section 4.1: Flow 1 - Complete Onboarding

**Steps:**
1. Open webapp at `http://localhost:5173/welcome`
2. Click "Create account" → Google OAuth (use test account)
3. Select PT-BR + French on `/languages`
4. Complete vocab test → Select 2000 words
5. See results: "You know 2000 words"
6. Click "Continue" → `/onboarding/pricing` page loads
7. Verify: Pricing card shows "$1/month", "Start Free Trial" button
8. Click "Start Free Trial" → Alert mockup appears
9. Confirm alert → Navigate to `/pin-extension`
10. Verify: Flow completes without errors ✅

**Pass Criteria:**
- All pages load correctly
- Mockup alert shows "(mockup)" in text
- Navigation works: Results → Pricing → Pin Extension

---

### Section 4.2: Flow 2 - Manage Subscription

**Steps:**
1. On any onboarding page (e.g., `/welcome`)
2. Verify: "Manage Subscription" button visible (top-right)
3. Click button → Alert mockup appears
4. Verify: Alert says "Stripe Customer Portal (mockup)"
5. Confirm alert → Subscription canceled message
6. No errors in console ✅

**Pass Criteria:**
- Button visible on all pages
- Mockup alert shows correctly
- No navigation errors

---

### Section 4.3: Flow 3 - Extension Not Subscribed (Option B+ - Simplified)

**Steps:**
1. Build extension: `npm run build:staging` (in extension directory)
2. Load unpacked extension in Chrome
3. Open extension popup
4. Verify: Debug controls visible (red border, 3 buttons)
5. Click "Set: Expired" button
6. Popup reloads → Text "Subscription required" appears below "Process Subtitles" button
7. Verify: "Process Subtitles" button is still VISIBLE (not hidden)
8. Click "Process Subtitles" button
9. New tab opens at `/subscribe` (instead of processing subtitles)
10. Verify: Pricing card shows "Subscribe to continue" ✅

**Pass Criteria:**
- Debug controls only visible in dev mode
- Text "Subscription required" shows when expired
- Process button remains visible but redirects to /subscribe
- Subscribe page opens correctly

---

## 📖 SECTION 5 - PHASE 2B CODE DETAILS

### Section 5.1: Create Stripe Product

**Stripe Dashboard Steps:**
1. Login to Stripe Dashboard → Test mode
2. Products → Create product
3. Name: "Subly Premium"
4. Description: "Smart subtitle adaptation for language learning"
5. Save product

---

### Section 5.2: Create Stripe Prices

**Create 3 prices for progressive pricing:**

```
Price 1 (Early Adopters):
- Name: $1/month (First 10 users)
- Amount: $1.00 USD
- Billing: Monthly recurring
- Price ID: price_xxxxx (copy this)

Price 2 (First 100):
- Name: $2/month (Users 11-100)
- Amount: $2.00 USD
- Billing: Monthly recurring
- Price ID: price_yyyyy (copy this)

Price 3 (Standard):
- Name: $5/month (Standard pricing)
- Amount: $5.00 USD
- Billing: Monthly recurring
- Price ID: price_zzzzz (copy this)
```

---

### Section 5.3: Backend - /create-checkout-session

```python
# smartsub-api/main.py
import stripe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Config (change manually as user count grows)
CURRENT_PRICE_ID = "price_xxxxx"  # $1/month initially

class CheckoutRequest(BaseModel):
    userId: str
    email: str

@app.post("/create-checkout-session")
async def create_checkout(request: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            mode='subscription',
            customer_email=request.email,
            line_items=[{
                'price': CURRENT_PRICE_ID,
                'quantity': 1
            }],
            subscription_data={
                'trial_period_days': 14,
                'metadata': {'user_id': request.userId}
            },
            success_url='https://subly-extension.vercel.app/onboarding/pin-extension',
            cancel_url='https://subly-extension.vercel.app/onboarding/pricing',
        )

        return {'url': session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

### Section 5.4: Backend - /create-portal-session

```python
# smartsub-api/main.py
class PortalRequest(BaseModel):
    userId: str

@app.post("/create-portal-session")
async def create_portal(request: PortalRequest):
    try:
        # Get customer ID from Supabase
        result = await supabase.from_('subscriptions') \
            .select('stripe_customer_id') \
            .eq('user_id', request.userId) \
            .single() \
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail='No subscription found')

        # Create portal session
        session = stripe.billing_portal.Session.create(
            customer=result.data['stripe_customer_id'],
            return_url='https://subly-extension.vercel.app/account'
        )

        return {'url': session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

### Section 5.5: Backend - /stripe-webhook

```python
# smartsub-api/main.py
from fastapi import Request

@app.post("/stripe-webhook")
async def webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid payload')
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail='Invalid signature')

    # Handle checkout.session.completed
    if event.type == 'checkout.session.completed':
        session = event.data.object
        user_id = session.metadata.get('user_id')

        await supabase.from_('subscriptions').insert({
            'user_id': user_id,
            'stripe_customer_id': session.customer,
            'stripe_subscription_id': session.subscription,
            'status': 'trialing'
        }).execute()

    # Handle subscription status updates
    elif event.type == 'customer.subscription.updated':
        subscription = event.data.object

        await supabase.from_('subscriptions').update({
            'status': subscription.status
        }).eq('stripe_subscription_id', subscription.id).execute()

    # Handle subscription deletion
    elif event.type == 'customer.subscription.deleted':
        subscription = event.data.object

        await supabase.from_('subscriptions').update({
            'status': 'canceled'
        }).eq('stripe_subscription_id', subscription.id).execute()

    return {'received': True}
```

---

### Section 5.6: Webhook Configuration

**Stripe Dashboard Steps:**
1. Developers → Webhooks → Add endpoint
2. Endpoint URL: `https://smartsub-api-production.up.railway.app/stripe-webhook`
3. Events to listen:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy webhook signing secret → Add to Railway env vars

---

### Section 5.7: Replace Mockups with Real API Calls

```tsx
// webapp/src/utils/stripe.ts (replaces mockups.ts)
const API_URL = import.meta.env.VITE_API_URL

export async function createCheckoutSession(userId: string, email: string) {
  const response = await fetch(`${API_URL}/create-checkout-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId, email })
  })

  const { url } = await response.json()
  window.location.href = url // Redirect to Stripe Checkout
}

export async function createPortalSession(userId: string) {
  const response = await fetch(`${API_URL}/create-portal-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId })
  })

  const { url } = await response.json()
  window.open(url, '_blank') // Open Portal in new tab
}

// Update PricingCard.tsx to use real API
import { createCheckoutSession } from '@/utils/stripe'

const handleCheckout = () => {
  createCheckoutSession(user.id, user.email)
}
```

---

### Section 5.8: Extension - Real Subscription Check

```typescript
// extension/src/popup/popup.ts
import { supabase } from '../lib/supabase'

async function checkSubscriptionStatus() {
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    console.error('No user logged in')
    return
  }

  const { data: subscription, error } = await supabase
    .from('subscriptions')
    .select('status')
    .eq('user_id', user.id)
    .single()

  if (error || !subscription) {
    showNotSubscribedUI()
    return
  }

  const hasAccess = ['trialing', 'active'].includes(subscription.status)

  if (hasAccess) {
    showNormalUI()
  } else {
    showNotSubscribedUI()
  }
}

// Remove debug controls in production
// (No addDebugControls() call)
```

---

**Last Updated:** January 29, 2025
**Next Review:** After Phase 2A (Frontend Implementation)
