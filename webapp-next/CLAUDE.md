# Webapp Next.js - CLAUDE.md

## Overview

Next.js 15 full-stack webapp for user onboarding, authentication, and billing. Deployed on Vercel with Supabase backend and Stripe payments.

## Tech Stack

- **Framework**: Next.js 15 + App Router + TypeScript
- **UI**: Tailwind CSS v4 + Shadcn UI
- **Auth**: Supabase SSR (@supabase/ssr)
- **Payments**: Stripe (test mode)
- **Notifications**: Sonner

## Development

```bash
npm run dev  # localhost:3000
npm run build
```

## Deployment

### Environments
- **Staging**: `staging-subly-extension.vercel.app` (branch: `develop`) ✅
- **Production**: `subly-extension.vercel.app` (branch: `main`) - pending

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
5. `/onboarding/pricing` - Stripe checkout ($1/month, 14-day trial)
6. `/onboarding/pin-extension` - Extension setup
7. `/onboarding/complete` - Success screen
8. `/welcome-back` - Returning users
9. `/subscribe` - Expired trial

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
- **Price**: $1/month (ID: `price_1SNtWWCdkaUrc0RrUnNRVpya`)
- **Trial**: 14 days
- **Mode**: Test (use card: 4242 4242 4242 4242)

### Webhooks
- **URL**: `https://staging-subly-extension.vercel.app/api/stripe/webhook`
- **Events**: `checkout.session.completed`, `customer.subscription.*`
- **Signature verification**: Required via `STRIPE_WEBHOOK_SECRET`

### Customer Portal
Enabled in Stripe Dashboard for subscription management (cancel, update payment).

## Extension Integration

Webapp syncs auth session to Chrome extension via `chrome.runtime.sendMessage()` after OAuth. See `lib/syncExtension.ts`.

**Extension ID**: `hpgaiiooldnocggkkmehaboncfbmhkhf`

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
