# Webapp Next.js - CLAUDE.md

## Overview

Next.js 15 full-stack webapp for user onboarding, authentication, and billing. Deployed on Vercel with Supabase backend and Stripe payments.

## Tech Stack

- **Framework**: Next.js 15 + App Router + TypeScript
- **UI**: Tailwind CSS v4 + Shadcn UI
- **Auth**: Supabase SSR (@supabase/ssr)
- **Payments**: Stripe (test mode staging, live mode production)
- **Analytics**: Vercel Analytics (page views, funnel tracking)
- **Notifications**: Sonner

**Status**: ✅ PRODUCTION LIVE (Phase 4 complete - January 13, 2025)

## Development

```bash
npm run dev  # localhost:3000
npm run build
```

## Deployment

### Environments
- **Staging**: `staging-subly-extension.vercel.app` (branch: `develop`) ✅
- **Production**: `subly-extension.vercel.app` (branch: `main`) ✅ LIVE

### Vercel Configuration
- **Framework Preset**: Next.js
- **Root Directory**: `webapp-next`
- **Build Command**: `npm run build`

### Environment Variables (per environment in Vercel)

**Development:**
```
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_SUPABASE_URL=https://dqjbkbdgvtewrgxrfqil.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Preview (staging):**
```
NEXT_PUBLIC_APP_URL=https://staging-subly-extension.vercel.app
(same Supabase/Stripe keys as dev)
```

**Production:**
```
NEXT_PUBLIC_APP_URL=https://subly-extension.vercel.app
(production Stripe keys when ready)
```

## Routes

### Onboarding Flow (9 pages)
1. `/welcome` - Google OAuth
2. `/onboarding/languages` - Language selection (OAuth callback destination)
3. `/onboarding/vocab-test` - Vocab test (12 levels)
4. `/onboarding/results` - Test results
5. `/onboarding/pricing` - Stripe checkout ($9/year, 3-day trial)
6. `/onboarding/pin-extension` - Extension setup
7. `/onboarding/complete` - Success screen
8. `/welcome-back` - Returning users
9. `/subscribe` - Expired trial

### Vocab Test/Retest Flow (Standalone - ✅ Complete)
1. `/vocab-test/intro` - Test introduction (triggered from extension)
2. `/vocab-test/explanation` - Test explanation
3. `/vocab-test/test` - Vocab test (12 levels: 100-5000)
4. `/vocab-test/results` - Results + "Go back to Netflix" button

**Features**: Separate VocabTestContext, saves to `vocab_levels` table, message passing to extension for auto-refresh.

### API Routes (Stripe)
- `/api/stripe/checkout` - Create checkout session
- `/api/stripe/webhook` - Handle Stripe webhooks
- `/api/stripe/portal` - Customer portal session

## Supabase OAuth

### Configuration
- **Site URL**: `https://subly-extension.vercel.app`
- **Callback**: `/auth/callback` → redirects to `/onboarding/languages` (new) or `/welcome-back` (returning)

### Redirect URLs (in Supabase Dashboard)
Add BOTH wildcards AND exact callbacks for all environments:
- `http://localhost:3000/*` + `http://localhost:3000/auth/callback`
- `https://staging-subly-extension.vercel.app/*` + `.../auth/callback`
- `https://subly-extension.vercel.app/*` + `.../auth/callback`

## Stripe Integration

### Product
- **Name**: "Subly Premium"
- **Price**: $19.99/year (early customers grandfathered at $9/year)
- **Trial**: 3 days (configured in code via `subscription_data.trial_period_days`)
- **Staging**: TEST mode (card: 4242 4242 4242 4242, price ID: `price_1Sc5hPCpd12v3sCmbEJ3EBmC`)
- **Production**: LIVE mode (real cards, price ID: `price_1Sc77rCpd12v3sCm1s2LqWi2`)

### Webhooks
- **Staging**: `https://staging-subly-extension.vercel.app/api/stripe/webhook` ✅ Tested
- **Production**: `https://subly-extension.vercel.app/api/stripe/webhook` ✅ Verified (January 13, 2025)
- **Events**: `checkout.session.completed`, `customer.subscription.*`
- **Signature verification**: Required via `STRIPE_WEBHOOK_SECRET` (different per environment)
- **Status**: All events returning 200 OK in production

### Customer Portal
✅ Active in both TEST and LIVE modes. Tested and functional for subscription management (cancel, update payment).

### Automated Emails (Resend)
- **Service**: Resend with custom domain `sublyy.com`
- **Sender**: `Subly <noreply@sublyy.com>`
- **Trigger**: Sent automatically after Stripe `checkout.session.completed` (landing flow only)
- **Content**: Extension download link + setup instructions
- **Flow detection**: Uses `session.metadata.flow === 'landing'` to distinguish flows
- **DNS**: Configured via IONOS (DKIM, SPF, MX records verified)
- **Backward compatibility**: Old onboarding flow receives no email

## Analytics

### Vercel Analytics

**Vercel Analytics** tracks basic user behavior. Automatically enabled via `<Analytics />` component in `app/layout.tsx`.

- **Free tier**: 50K events/month
- **Tracks**: Page views, unique visitors, bounce rate, top pages
- **Use case**: Basic metrics
- **Dashboard**: Vercel project → Analytics tab

### PostHog Analytics (✅ Configured - January 2025)

**PostHog** provides advanced product analytics with session replay and funnel analysis. Configured via `PostHogProvider` in `src/providers/PostHogProvider.tsx`.

**Features**:
- ✅ **Session Replay**: Watch user interactions, clicks, time on page
- ✅ **Funnel Analysis**: Track conversion through landing tunnel (20 steps)
- ✅ **Auto-capture**: Automatic event tracking (pageviews, clicks, etc.)
- ✅ **Privacy-first**: Masks all inputs, sensitive data, and Stripe iframes

**Configuration**:
- **Project ID**: 107396
- **Host**: `https://eu.i.posthog.com`
- **API Key**: `phc_KDT8LPdCMBCmCrN70dYu4FU3I1YbEco3bbCdv3fMdlw` (public key, safe to expose)
- **Pageview tracking**: Automatic via `defaults: '2025-11-30'`

**Environment Variables**:
```bash
NEXT_PUBLIC_POSTHOG_KEY=phc_KDT8LPdCMBCmCrN70dYu4FU3I1YbEco3bbCdv3fMdlw
NEXT_PUBLIC_POSTHOG_HOST=https://eu.i.posthog.com
```

**Primary Use Case**: Analyze **Landing Funnel** (20 steps):
- **Partie 1: Discovery** (7 steps) - `/landing/*` pages
- **Partie 2: Setup** (13 steps) - `/landing/setup/*` pages

**Documentation**: See `POSTHOG_SETUP.md` for complete funnel setup guide

**Dashboard**: https://app.posthog.com/project/107396

## Extension Integration

Webapp syncs auth session to Chrome extension via `chrome.runtime.sendMessage()` after OAuth. See `lib/syncExtension.ts`.

**Extension ID**: `lhkamocmjgjikhmfiogfdjhlhffoaaek` (Chrome Web Store)
**Status**: Submitted to Chrome Web Store (Phase 3)

Extension `manifest.json` must include in `externally_connectable.matches`:
- `http://localhost:3000/*`
- `https://staging-subly-extension.vercel.app/*`
- `https://subly-extension.vercel.app/*`

## Key Files

- `app/` - Pages (file-based routing)
- `app/api/stripe/` - Stripe API routes
- `contexts/AuthContext.tsx` - Auth state management
- `lib/supabase/client.ts` - Browser Supabase client
- `lib/supabase/server.ts` - Server Supabase client
- `middleware.ts` - Session refresh middleware
- `lib/syncExtension.ts` - Extension session sync

## Common Issues

### OAuth redirects to template page (/)
- Check Vercel is building `webapp-next/` not `webapp/`
- Verify Framework Preset is Next.js, not Vite
- Ensure Supabase has exact callback URL configured

### Stripe redirects to localhost instead of staging
- Check `NEXT_PUBLIC_APP_URL` is set correctly per environment (Development/Preview/Production)
- Redeploy after changing env vars

### Build fails with Stripe apiVersion error
- Remove `apiVersion` parameter from Stripe initialization
- Let Stripe use default version: `new Stripe(process.env.STRIPE_SECRET_KEY!)`

### Webhook signature verification fails
- Ensure `STRIPE_WEBHOOK_SECRET` matches webhook endpoint secret in Stripe Dashboard
- Use raw body for signature verification: `await req.text()`
