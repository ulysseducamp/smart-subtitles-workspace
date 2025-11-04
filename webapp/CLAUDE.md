# Webapp (Vite) - CLAUDE.md

⚠️ **DEPRECATED - Legacy Vite webapp. Use `webapp-next/` (Next.js) for active development.**

## Overview

React SPA for user onboarding, authentication, and account management. Replaced by Next.js for Stripe integration (Phase 2B).

**Active webapp:** `webapp-next/` (Next.js 15 + Stripe)
**Status:** To be archived after production deployment

## Tech Stack

- **Framework**: React 19 + Vite + TypeScript
- **UI**: Tailwind CSS v3 + Shadcn UI components
- **Auth**: Supabase Auth (Google OAuth)
- **Routing**: React Router v6
- **Notifications**: Sonner (toast library)

## Development

```bash
npm run dev  # localhost:5173
npm run build
```

## Deployment

### Environments
- **Staging**: `staging-subly-extension.vercel.app` (branch: `develop`)
- **Production**: `subly-extension.vercel.app` (branch: `main`)

### Vercel Configuration
- **Root Directory**: `webapp`
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### Environment Variables (Vercel Dashboard)
```
VITE_SUPABASE_URL=https://dqjbkbdgvtewrgxrfqil.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### SPA Routing Fix
`vercel.json` required for React Router to work on Vercel:
```json
{
  "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]
}
```

## Supabase OAuth Setup

### Site URL
`https://subly-extension.vercel.app` (production default)

### Redirect URLs (BOTH required)
**Wildcards** (allows all pages):
- `http://localhost:5173/*`
- `https://staging-subly-extension.vercel.app/*`
- `https://subly-extension.vercel.app/*`

**Exact URLs** (OAuth redirect target):
- `http://localhost:5173/onboarding/languages`
- `https://staging-subly-extension.vercel.app/onboarding/languages`
- `https://subly-extension.vercel.app/onboarding/languages`

**Why Both?** OAuth checks exact URLs first, then falls back to wildcards. Without exact URLs, OAuth may redirect to Site URL instead of `redirectTo` parameter.

## Routes

### Authentication Flow
1. `/welcome` - Landing page with Google OAuth button
2. `/onboarding/languages` - Language selection (OAuth redirect target)
3. `/onboarding/vocab-test` - Vocabulary level test
4. `/onboarding/results` - Test results
5. `/onboarding/pin-extension` - Extension setup guide
6. `/onboarding/complete` - Success screen
7. `/welcome-back` - Returning users (skips onboarding)

### Redirect Logic
OAuth redirects to `/onboarding/languages`, then React checks:
- **New user** (no `user_settings`): Stay on `/onboarding/languages`
- **Returning user** (has `user_settings`): Redirect to `/welcome-back`

## Key Files

- `src/contexts/AuthContext.tsx` - Auth state management
- `src/lib/supabase.ts` - Supabase client configuration
- `src/lib/syncExtension.ts` - Session sync with Chrome extension
- `vercel.json` - SPA routing configuration

## Extension Integration

Webapp syncs auth session to Chrome extension via `chrome.runtime.sendMessage()` after OAuth success. See `src/lib/syncExtension.ts`.

**Extension ID** (in `syncExtension.ts`): `hpgaiiooldnocggkkmehaboncfbmhkhf`

**Extension manifest.json** must include in `externally_connectable`:
```json
{
  "matches": [
    "http://localhost:5173/*",
    "https://staging-subly-extension.vercel.app/*",
    "https://subly-extension.vercel.app/*"
  ]
}
```

## Common Issues

### OAuth redirects to wrong URL
- Ensure exact URL (`/onboarding/languages`) is in Supabase Redirect URLs
- Site URL should be production domain
- `window.location.origin` in `redirectTo` handles dynamic environments

### 404 on page refresh
- Ensure `vercel.json` exists with rewrites configuration
- Vercel must serve `index.html` for all routes (SPA pattern)

### Environment variables not working
- Must use `VITE_` prefix for Vite to expose to client
- Set in Vercel Dashboard under "Environment Variables"
- Redeploy after changing env vars
