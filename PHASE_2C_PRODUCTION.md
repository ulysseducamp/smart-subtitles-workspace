# Phase 2C - Production Deployment

**Status**: Not started
**Duration**: 4-6 hours (realistic estimate)
**Goal**: Deploy Next.js webapp to production with live Stripe integration
**Date**: TBD

---

## 📋 Pre-requisites Checklist

Before starting Phase 2C, verify:

- [ ] Staging has been stable for 24-48h (no critical bugs)
- [ ] All Phase 12 tests passed ✅
- [ ] Staging logs are clean (Vercel + Stripe + Supabase)
- [ ] Extension built in staging mode works correctly
- [ ] Team aligned on deployment timing

---

## 🎯 Overview

This phase transitions from **test mode** (staging) to **live mode** (production):

**What changes:**
- Stripe keys: `sk_test_*` → `sk_live_*`
- Stripe webhook: New endpoint + new secret
- Stripe product/price: Test mode → Live mode
- App URL: `staging-subly-extension.vercel.app` → `subly-extension.vercel.app`
- Extension build: `npm run build:staging` → `npm run build:production`

**What stays the same:**
- Supabase URL (same instance for staging + production)
- Supabase Anon Key (same for staging + production)
- Database schema (already configured)
- Codebase (no code changes needed)

---

## 📝 Detailed Checklist

### 1️⃣ Pre-Deployment Setup (1h)

#### 1.1 Backup & Safety (15min)

- [ ] **Backup Supabase database** (optionnel - skip si données de test uniquement)
  ```bash
  # Supabase Dashboard → Database → Backups
  # Create manual backup before deployment
  # Note: Pas nécessaire si toutes les données sont de test
  ```

- [ ] **Create git tag for current state**
  ```bash
  git checkout develop
  git pull origin develop
  git tag v1.0.0-pre-production
  git push origin v1.0.0-pre-production
  ```

- [ ] **Document rollback plan** (see section below)

#### 1.2 Stripe Live Mode Setup (45min)

- [ ] **1. Login to Stripe Dashboard → Switch to LIVE mode** (top-left toggle)

- [ ] **2. Create product "Subly Premium" in LIVE mode**
  - Navigate to: Products → Add product
  - Name: `Subly Premium`
  - Description: `Smart subtitles for language learning on Netflix`
  - Click "Add product"
  - **Note Product ID**: `prod_XXXXX` (save for reference)

- [ ] **3. Create price $1/month with 14-day trial**
  - In product page → Add another price
  - Price: `$1.00 USD`
  - Billing period: `Monthly`
  - Click "Add pricing"
  - Click on the new price → Edit
  - Enable "Free trial" → `14 days`
  - Save
  - **Copy Price ID**: `price_1XXXXX` (CRITICAL - needed for env vars)

- [ ] **4. Verify Customer Portal enabled in LIVE mode**
  - Settings → Billing → Customer portal
  - Toggle "Enable customer portal" ON
  - Enable "Cancel subscription" option
  - Save

- [ ] **5. Get live API keys**
  - Developers → API keys → Reveal live secret key
  - **Copy `sk_live_XXXXX`** (CRITICAL - keep secure)
  - **Copy `pk_live_XXXXX`** (publishable key - not currently needed but good to have)

---

### 2️⃣ Webhook Configuration (45min)

#### 2.1 Create Production Webhook

- [ ] **1. Create webhook endpoint in Stripe Dashboard (LIVE mode)**
  - Developers → Webhooks → Add endpoint
  - Endpoint URL: `https://subly-extension.vercel.app/api/stripe/webhook`
  - Description: `Subly Production Webhook`
  - Events to listen to (select 4):
    - `checkout.session.completed`
    - `customer.subscription.created`
    - `customer.subscription.updated`
    - `customer.subscription.deleted`
  - Click "Add endpoint"

- [ ] **2. Copy webhook signing secret**
  - Click on the newly created webhook
  - **Copy Signing Secret**: `whsec_XXXXX` (CRITICAL)

#### 2.2 Test Webhook (BEFORE deployment)

- [ ] **3. Test webhook with Stripe CLI**
  ```bash
  # Install Stripe CLI if not installed: brew install stripe/stripe-cli/stripe

  # Login to Stripe (LIVE mode)
  stripe login

  # Forward webhooks to local Next.js (for testing)
  # First, run Next.js locally: npm run dev (in webapp-next/)
  stripe listen --forward-to localhost:3000/api/stripe/webhook --live

  # Trigger test event (in another terminal)
  stripe trigger checkout.session.completed --live

  # Verify: Check terminal shows [200] response
  ```

- [ ] **Verify webhook signature verification works** (check Next.js console logs)

---

### 3️⃣ Vercel Environment Configuration (30min)

- [ ] **1. Navigate to Vercel Dashboard**
  - Project: `subly-extension` (or your project name)
  - Settings → Environment Variables

- [ ] **2. Add/Update Production environment variables**

**IMPORTANT**: Select "Production" environment for each variable below:

| Variable Name | Value | Environment | Notes |
|--------------|-------|-------------|-------|
| `NEXT_PUBLIC_APP_URL` | `https://subly-extension.vercel.app` | Production | ✅ Already set |
| `NEXT_PUBLIC_SUPABASE_URL` | `https://dqjbkbdgvtewrgxrfqil.supabase.co` | Production | ✅ Already set (same as staging) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` | Production | ✅ Already set (same as staging) |
| `STRIPE_SECRET_KEY` | `sk_live_XXXXX` | Production | 🔄 **UPDATE** with live key |
| `STRIPE_WEBHOOK_SECRET` | `whsec_XXXXX` | Production | 🔄 **UPDATE** with production webhook secret |
| `STRIPE_PRICE_ID_MONTHLY` | `price_1XXXXX` | Production | ⭐ **NEW** - Add live price ID |

**How to add/update:**
- Click "Add New" (or "Edit" for existing vars)
- Name: (from table above)
- Value: (paste from Stripe Dashboard)
- Environments: Check ONLY "Production"
- Save

- [ ] **3. Verify Preview (staging) environment variables unchanged**
  - `STRIPE_SECRET_KEY` should still be `sk_test_*` for Preview
  - `STRIPE_WEBHOOK_SECRET` should still be `whsec_test_*` for Preview
  - `STRIPE_PRICE_ID_MONTHLY` should still be test price for Preview

---

### 4️⃣ Code Update (ONLY if using hardcoded price_id) (15min)

**Skip this step if you already use `process.env.STRIPE_PRICE_ID_MONTHLY`**

- [ ] **1. Verify code uses environment variable**
  ```bash
  # Check if hardcoded:
  grep -r "price_1SNtWW" webapp-next/src/

  # If found, replace with:
  process.env.STRIPE_PRICE_ID_MONTHLY
  ```

- [ ] **2. If code needs update:**
  ```typescript
  // webapp-next/src/app/api/stripe/checkout/route.ts

  // ❌ BEFORE (hardcoded test price)
  line_items: [{
    price: 'price_1SNtWWCdkaUrc0RrUnNRVpya',
    quantity: 1,
  }],

  // ✅ AFTER (environment variable)
  line_items: [{
    price: process.env.STRIPE_PRICE_ID_MONTHLY!,
    quantity: 1,
  }],
  ```

- [ ] **3. Commit changes (if any)**
  ```bash
  git add .
  git commit -m "feat: Use STRIPE_PRICE_ID_MONTHLY env var for production compatibility"
  git push origin develop
  ```

---

### 5️⃣ Git Workflow & Deployment (30min)

- [ ] **1. Create PR from develop to main**
  ```bash
  # Option A: Via GitHub UI (recommended)
  # - Go to GitHub repo → Pull requests → New PR
  # - Base: main, Compare: develop
  # - Title: "Phase 2C - Production Deployment"
  # - Description: "Deploy Next.js webapp to production with live Stripe"

  # Option B: Via command line
  gh pr create --base main --head develop --title "Phase 2C - Production Deployment"
  ```

- [ ] **2. Review PR**
  - Verify no secrets in code (run `git grep -i "sk_live"` → should be empty)
  - Check environment variables configured in Vercel
  - Verify staging still stable

- [ ] **3. Merge PR**
  - Click "Merge pull request" on GitHub
  - Confirm merge
  - **Vercel auto-deploys to production** (wait 2-3 minutes)

- [ ] **4. Create production tag**
  ```bash
  git checkout main
  git pull origin main
  git tag v1.0.0-production
  git push origin v1.0.0-production
  ```

- [ ] **5. Verify Vercel deployment**
  - Vercel Dashboard → Deployments → Check latest deployment status
  - Should show: "Ready" with production domain
  - Click "View deployment" → Should open `https://subly-extension.vercel.app`

- [ ] **6. Check build logs**
  - Vercel deployment → Build logs
  - Verify no errors (especially Stripe/Supabase related)

---

### 6️⃣ Production Testing (2h)

#### 6.1 Basic Flow Tests (30min)

- [ ] **Test 1: Homepage loads**
  - Navigate to: `https://subly-extension.vercel.app/welcome`
  - Verify: Page loads, no console errors
  - Verify: Image (ulysse-photo.jpg) displays

- [ ] **Test 2: Google OAuth flow**
  - Click "Create an account and set up Subly"
  - Complete Google OAuth (use incognito window)
  - Verify redirect to `/onboarding/languages` ✅
  - Verify user created in Supabase (Dashboard → Authentication → Users)

- [ ] **Test 3: Complete onboarding (7 pages)**
  - Languages → Select PT-BR + French → Next
  - Vocab test → Complete test → Next
  - Results → View results → Next
  - Pricing → **STOP HERE** (don't click "Start free trial" yet)

#### 6.2 Stripe Integration Tests (1h)

- [ ] **Test 4: Stripe Checkout flow**
  - On Pricing page → Click "Start free trial"
  - Verify redirect to Stripe Checkout (hosted page)
  - **Use test card**: `4242 4242 4242 4242`
    - Expiry: Any future date (e.g., 12/26)
    - CVC: Any 3 digits (e.g., 123)
    - Postal code: Any (e.g., 12345)
  - Complete checkout
  - Verify redirect to `/onboarding/pin-extension` ✅

- [ ] **Test 5: Webhook reception**
  - Stripe Dashboard (LIVE mode) → Developers → Webhooks
  - Click on production webhook
  - Click "Events" tab
  - Verify: `checkout.session.completed` event shows [200 OK] response
  - Timestamp should match your test (within last 5 minutes)

- [ ] **Test 6: Subscription created in Supabase**
  - Supabase Dashboard → Table Editor → `subscriptions` table
  - Verify: New row with your user_id
  - Verify fields:
    - `stripe_customer_id`: `cus_XXXXX`
    - `stripe_subscription_id`: `sub_XXXXX`
    - `status`: `trialing` (14-day trial active)
    - `created_at`: Recent timestamp

- [ ] **Test 7: Customer Portal (cancel subscription)**
  - Complete onboarding → `/onboarding/complete`
  - Click "Manage Subscription" button
  - Verify redirect to Stripe Customer Portal
  - Click "Cancel subscription" → Confirm
  - Verify: Subscription status changes to `canceled` in Supabase

- [ ] **Test 8: Webhook for cancellation**
  - Stripe Dashboard → Webhooks → Events
  - Verify: `customer.subscription.deleted` event shows [200 OK]
  - Supabase → `subscriptions` table
  - Verify: Status updated to `canceled`

#### 6.3 Extension Integration Tests (30min)

- [ ] **Test 9: Build extension in production mode**
  ```bash
  cd netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/
  npm run build:production  # Points to production webapp URL
  ```

- [ ] **Test 10: Load extension in Chrome**
  - Chrome → Extensions → Developer mode ON
  - Load unpacked → Select `dist/` folder
  - Verify extension loads (no errors in console)

- [ ] **Test 11: Extension opens production webapp**
  - Click extension icon → Should open `https://subly-extension.vercel.app/welcome`
  - Verify: NOT staging URL (not `staging-subly-extension.vercel.app`)

- [ ] **Test 12: Extension reads subscription from Supabase**
  - Complete onboarding on production
  - Open extension popup
  - Verify: Shows subscription status (active/trialing)
  - Verify: NOT redirected to `/subscribe` page (means subscription detected)

#### 6.4 RLS Isolation Test (15min)

- [ ] **Test 13: Multi-user data isolation**
  - Create 2nd Google account (or use existing)
  - User A: Complete onboarding → PT-BR 2000
  - User B: Complete onboarding → PT-BR 1000
  - Open browser console → Check Supabase queries
  - Verify: User A sees ONLY their 2000 level (not 1000)
  - Verify: User B sees ONLY their 1000 level (not 2000)
  - **Pass criteria**: No data leakage between users ✅

---

### 7️⃣ Monitoring Setup (1h)

#### 7.1 Vercel Monitoring

- [ ] **1. Enable Vercel Analytics** (optional but recommended)
  - Vercel Dashboard → Analytics → Enable
  - Free tier: 2500 events/month

- [ ] **2. Check Runtime Logs**
  - Vercel → Deployments → Click production deployment → Runtime Logs
  - Filter: "Error" level
  - Verify: No critical errors in last hour

- [ ] **3. Setup error alerts** (optional)
  - Vercel → Settings → Notifications
  - Enable: "Deployment failed" + "Build failed"
  - Add email/Slack webhook

#### 7.2 Stripe Monitoring

- [ ] **4. Bookmark Stripe Dashboard pages**
  - Webhooks: `https://dashboard.stripe.com/webhooks` (monitor delivery)
  - Events: `https://dashboard.stripe.com/events` (see all API events)
  - Customers: `https://dashboard.stripe.com/customers` (user subscriptions)

- [ ] **5. Enable webhook failure alerts**
  - Stripe Dashboard → Webhooks → Click production webhook
  - Settings → Enable "Email me when endpoint is automatically disabled"
  - Add your email: `unducamp.pro@gmail.com`

- [ ] **6. Monitor webhook delivery for 1-2 hours**
  - Every 15 minutes: Check Webhooks tab
  - Verify: All events show [200 OK]
  - If [400] or [500]: Investigate immediately (check Vercel logs)

#### 7.3 Supabase Monitoring

- [ ] **7. Check database performance**
  - Supabase → Reports → Database
  - Verify: No slow queries, no connection errors

- [ ] **8. Monitor RLS policies**
  - Supabase → Database → Policies
  - Verify: All tables have RLS enabled ✅

---

### 8️⃣ Post-Deployment Validation (30min)

- [ ] **1. Document production URLs**
  ```markdown
  # Production URLs (for quick reference)
  - Webapp: https://subly-extension.vercel.app
  - Supabase: https://dqjbkbdgvtewrgxrfqil.supabase.co
  - Stripe Dashboard: https://dashboard.stripe.com (LIVE mode)
  ```

- [ ] **2. Update ROADMAP.md**
  - Check Phase 2C boxes ✅
  - Add completion date
  - Update status to "COMPLETED"

- [ ] **3. Final smoke tests**
  - Signup → Onboarding → Checkout → Extension (full E2E)
  - Repeat with different Google account
  - Verify both users isolated (RLS working)

- [ ] **4. Clean up test data** (optional)
  - Supabase → Authentication → Delete test users
  - Stripe → Customers → Cancel test subscriptions
  - OR: Keep 1-2 test accounts for ongoing validation

- [ ] **5. Announce deployment** (internal/team)
  - "Production deployed ✅"
  - "Live at: https://subly-extension.vercel.app"
  - "Stripe live mode active"

---

## 🚨 Rollback Plan

If critical issues arise during/after deployment:

### Scenario 1: Vercel deployment fails

```bash
# Revert to previous deployment in Vercel Dashboard
# Vercel → Deployments → Previous deployment → Redeploy
```

### Scenario 2: Webhook issues (subscriptions not created)

```bash
# Immediate fix: Revert to staging webhook temporarily
# 1. Vercel → Env vars → Switch STRIPE_WEBHOOK_SECRET back to test
# 2. Stripe → Disable production webhook
# 3. Re-enable staging webhook
# 4. Debug locally, then redeploy
```

### Scenario 3: Critical bug in production

```bash
# Emergency rollback to develop branch
git checkout main
git revert HEAD  # Reverts last merge
git push origin main
# Vercel auto-redeploys previous working state
```

### Scenario 4: Stripe configuration error

- Disable production webhook in Stripe Dashboard
- Switch Vercel env vars back to test mode
- Debug locally with staging setup
- Fix and redeploy

---

## ✅ Success Criteria

Phase 2C is complete when:

- [x] Production webapp loads at `https://subly-extension.vercel.app`
- [x] OAuth flow works (Google login)
- [x] Stripe checkout works (test card 4242...)
- [x] Webhook delivers to production endpoint [200 OK]
- [x] Subscriptions created in Supabase with correct status
- [x] Extension (production build) opens production URL
- [x] RLS isolation verified (2+ users)
- [x] No errors in Vercel/Stripe/Supabase logs (1-2h monitoring)
- [x] Rollback plan documented and understood

---

## 📚 Reference Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Stripe Dashboard (LIVE)**: https://dashboard.stripe.com (toggle top-left)
- **Supabase Dashboard**: https://supabase.com/dashboard/project/dqjbkbdgvtewrgxrfqil
- **Stripe Test Cards**: https://stripe.com/docs/testing#cards

---

## 🔐 Security Checklist (Final Verification)

- [ ] No `sk_live_*` keys in git history (`git log -p | grep sk_live` → empty)
- [ ] No `sk_live_*` keys in code (`grep -r "sk_live" webapp-next/src/` → empty)
- [ ] All secrets in Vercel environment variables only
- [ ] Webhook signature verification enabled (verify in code)
- [ ] RLS policies active on all tables (Supabase Dashboard)
- [ ] HTTPS only (Vercel handles automatically)
- [ ] CORS configured correctly (Next.js handles automatically)

---

## ⏱️ Time Breakdown (Realistic)

| Task | Estimated Time | Notes |
|------|---------------|-------|
| Pre-deployment setup | 1h | Backup, safety measures |
| Stripe live mode setup | 45min | Create product, price, webhook |
| Webhook testing | 45min | Stripe CLI, verify signature |
| Vercel env configuration | 30min | Add/update production env vars |
| Git workflow & deployment | 30min | PR, merge, tag |
| Production testing | 2h | E2E flows, Stripe, extension |
| Monitoring setup | 1h | Vercel, Stripe, Supabase alerts |
| Post-deployment | 30min | Docs, smoke tests, announcement |
| **TOTAL** | **6h 10min** | Buffer included |

**Realistic range**: 4-6 hours (depends on issues encountered)

---

**Last updated**: TBD
**Next steps**: Phase 3 - Chrome Web Store submission
