# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL: Development Philosophy

**KEEP IT SIMPLE** - Always prefer the simplest solution that works. Avoid over-engineering, premature abstractions, and complex data structures when simple constants or if/else statements suffice. Follow YAGNI (You Aren't Gonna Need It) - only build what's needed NOW, not what might be needed later.

## 🔒 CRITICAL: Security Principles

**NEVER compromise on security.** Always follow these principles:

### Secrets & API Keys
- **NEVER commit** API keys, secrets, tokens, or credentials to git
- **ALWAYS use environment variables** for sensitive data (Stripe keys, Supabase keys, API secrets)
- **NEVER expose** backend API keys in client-side code (extension or webapp)
- Use `.env` files for local development, Railway/Vercel env vars for production
- When adding new secrets, immediately update `.gitignore` to exclude them

### Code Security Patterns
- **Server-side only**: Stripe secret keys, webhook secrets, admin operations
- **Client-side safe**: Stripe publishable keys, Supabase anon keys (with RLS enabled)
- **Validate ALL user inputs** before processing (both frontend and backend)
- **Use Row Level Security (RLS)** in Supabase for data isolation
- **Rate limiting**: Implement on all public endpoints to prevent abuse
- **HTTPS only**: Never transmit sensitive data over HTTP

### Stripe-Specific Security
- **Test mode first**: Always test with `pk_test_*` and `sk_test_*` keys before production
- **Webhook signature verification**: ALWAYS verify webhook signatures before processing
- **Idempotency**: Handle duplicate webhook events gracefully
- **Never trust client data**: Always verify prices/products server-side, not from client

### When in Doubt
- If unsure about security implications, **ASK before implementing**
- Follow principle of least privilege: give minimum permissions necessary
- Security > convenience: If a feature requires compromising security, reject it

---

## Project Overview

This is Smart Subtitles (Subly) - a comprehensive language learning platform that creates personalized Netflix viewing experiences through intelligent bilingual subtitle adaptation. The system automatically switches between target language subtitles and native language subtitles based on the user's vocabulary knowledge.

**Production Status (January 21, 2025):**
- ✅ **Webapp**: LIVE on `subly-extension.vercel.app` (Stripe LIVE mode active)
- ⏳ **Extension**: Submitted to Chrome Web Store (awaiting approval, 1-2 days)
- ✅ **API**: LIVE on `smartsub-api-production.up.railway.app`
- ✅ **Features Complete**: Onboarding, Auth, Billing, Vocab Test/Retest, Subtitle Processing

## Architecture

The project consists of three main components:

1. **Chrome Extension** (`netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/`) - React popup + Netflix integration
2. **Webapp** (`webapp-next/`) - Next.js 15 for auth, onboarding, billing, vocab testing
3. **FastAPI Backend** (`smartsub-api/`) - Python subtitle fusion algorithm API

### High-Level Data Flow
```
Chrome Extension (Netflix) → FastAPI API → Python Fusion Algorithm → Processed Subtitles → Chrome Extension
Extension ↔ Webapp (Supabase Auth + Sync) → Multi-device data synchronization
```

## Development Commands

### Chrome Extension (TypeScript)
```bash
cd netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/

# Development build with watch mode
npm run dev

# IMPORTANT: Environment-specific builds
npm run build:staging     # ← Pour développement (pointe vers staging API)
npm run build:production  # ← Pour utilisateurs finaux (pointe vers production API)

# NEVER use npm run build directly - always specify staging or production!

# Type checking
npm run type-check

# Clean build artifacts
npm run clean

# Linting
npm run lint
```

### Environment Workflow Rules
- **Development/Testing**: ALWAYS use `npm run build:staging` → Extension pointe vers `smartsub-api-staging.up.railway.app` + `staging-subly-extension.vercel.app`
- **Production/Distribution**: Use `npm run build:production` → Extension pointe vers `smartsub-api-production.up.railway.app` + `subly-extension.vercel.app`
- **Branch staging**: `develop` → auto-deploy to staging API
- **Branch production**: `main` → auto-deploy to production API
- **WEBAPP_URL**: Configured via webpack.config.js, injected at build time (no manual changes needed)

### Webapp Next.js (Active - ✅ PRODUCTION LIVE)
```bash
cd webapp-next/

# Development server with hot reload
npm run dev  # Runs on http://localhost:3000

# Build for production
npm run build
```

**Tech Stack:** Next.js 15 + App Router + TypeScript + Tailwind CSS v4 + Shadcn UI + Supabase SSR + Stripe + Resend
**Status:** ✅ Production deployment complete (January 13, 2025)

**Onboarding Flow (9 pages):**
1. `/welcome` - Welcome + Google OAuth
2. `/onboarding/languages` - Target/native language selection
3. `/onboarding/vocab-test` - Dynamic vocab test (12 levels: 100-5000)
4. `/onboarding/results` - Display vocab level
5. `/onboarding/pricing` - Stripe checkout ($9/year, 3-day trial)
6. `/onboarding/pin-extension` - Pin extension guide
7. `/onboarding/complete` - Setup complete
8. `/welcome-back` - Returning users
9. `/subscribe` - Expired trial page

**Vocab Test/Retest Flow (✅ COMPLETE - November 20, 2025):**
- **Standalone flow**: `/vocab-test/intro` → `/vocab-test/explanation` → `/vocab-test/test` → `/vocab-test/results`
- **Trigger**: Extension popup "Test My Level" button opens `/vocab-test/intro?targetLanguage=pt-BR`
- **Context**: Separate `VocabTestContext` (independent from onboarding)
- **Multi-language**: Each language has independent vocab level in Supabase
- **Auto-refresh**: Message passing extension ↔ webapp updates popup without reload
- **Storage**: `vocab_levels` table (user_id, language, level, tested_at) with UNIQUE constraint
- **Documentation**: `VOCAB_TEST_RETEST_PLAN.md` - Full implementation details + test results

**Stripe Integration (✅ LIVE):**
- **API Routes**: `/api/stripe/checkout`, `/api/stripe/webhook`, `/api/stripe/portal`
- **Product**: "Subly Premium" - $9/year with 3-day trial
- **Webhook**: Handles `checkout.session.completed`, `customer.subscription.*` (verified in production)
- **Customer Portal**: Active in both TEST and LIVE modes
- **Automated Emails**: Resend sends extension download link after checkout (landing flow only, from `noreply@sublyy.com`)

**Deployment:**
- **Staging**: `staging-subly-extension.vercel.app` (branch: `develop`) - Stripe TEST mode
- **Production**: `subly-extension.vercel.app` (branch: `main`) ✅ LIVE - Stripe LIVE mode
- **Vercel Settings**: Framework: Next.js, Root: `webapp-next`

**Environment Variables (per environment):**
- **Development**: `NEXT_PUBLIC_APP_URL=http://localhost:3000`
- **Preview**: `NEXT_PUBLIC_APP_URL=https://staging-subly-extension.vercel.app`
- **Production**: `NEXT_PUBLIC_APP_URL=https://subly-extension.vercel.app`
- Plus: Supabase URL/keys, Stripe keys/webhook secret, Resend API key

**Supabase OAuth:**
- **Site URL**: `https://subly-extension.vercel.app`
- **Callback**: `/auth/callback` → redirects to `/onboarding/languages` (new user) or `/welcome-back` (returning)
- **Redirect URLs**: Both wildcards (`/*`) AND exact callbacks (`/auth/callback`) required for all environments (localhost:3000, staging, production)
- **IMPORTANT - Manual Site URL switching**: Supabase only supports ONE Site URL at a time. Change it manually in Supabase Dashboard → Authentication → URL Configuration based on where you're testing:
  - Testing on **localhost**: Set Site URL to `http://localhost:3000`
  - Testing on **staging**: Set Site URL to `https://staging-subly-extension.vercel.app`
  - Testing on **production**: Set Site URL to `https://subly-extension.vercel.app`
  - This is a known Supabase limitation - Site URL acts as fallback when redirectTo doesn't match whitelist

**Key Differences from Vite:**
- File-based routing vs React Router
- `useRouter()` from `next/navigation` vs `useNavigate()`
- `'use client'` directive required for useState/useEffect/handlers
- `NEXT_PUBLIC_*` env vars vs `VITE_*`
- Port 3000 vs 5173

### Webapp Vite (Legacy - Phase 1B complete, will be archived)
```bash
cd webapp/

# Development server with hot reload
npm run dev  # Runs on http://localhost:5173

# Build for production
npm run build
```

**Status:** ✅ Phase 1B complete (auth + onboarding working). **LEGACY - Replaced by Next.js webapp (Phase 2B/2C complete).**

**Tech Stack:** React 19 + Vite + TypeScript + Tailwind CSS v3 + Shadcn UI + Supabase Auth

**Note**: This webapp is now archived. Next.js webapp is live in production.

### FastAPI Backend
```bash
cd smartsub-api/

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Run tests
python -m pytest tests/
```

### Docker Build (Full Stack)
```bash
# Build Docker image (includes both Node.js CLI and Python API)
docker build -t smartsub-api .

# Run container
docker run -p 3000:3000 smartsub-api
```

## Core Architecture Patterns

### Chrome Extension Architecture
- **Three-script pattern**: `Popup.tsx` (React) ↔ `content-script.ts` ↔ `page-script.ts`
- **JSON Hijacking**: Intercepts Netflix API responses by overriding `JSON.parse()`
- **Message Passing**: Chrome extension message system for cross-context communication
- **State Management**: Supabase (primary) + `chrome.storage.local` (fallback)
- **Manual Processing**: User must click "Process Subtitles" button (auto-processing disabled to prevent Netflix preload corruption)
- **Permissions**: Uses `activeTab` instead of `tabs` to avoid "Read browsing history" warning (displays only Netflix site access warning)

### Webapp Architecture (Next.js - Production Ready)
- **Tech Stack**: Next.js 15 + App Router + TypeScript + Tailwind CSS v4 + Shadcn UI + Stripe + Vercel Analytics
- **Routing**: File-based routing (`app/welcome/page.tsx`)
- **Auth**: Supabase SSR (@supabase/ssr) with cookie-based sessions
- **Analytics**: Vercel Analytics for onboarding funnel tracking
- **Backend**: Next.js API Routes for Stripe (checkout, webhook, portal) ✅
- **Data Sync**: Supabase for multi-device synchronization
- **Pattern**: External webapp for auth + subscription management
- **Deployment**: Vercel staging active, production pending
- **Legacy**: Vite webapp exists, to be archived post-production launch

### API Backend Architecture
- **Pure Python Fusion**: Direct function calls to Python subtitle fusion algorithm (migrated from TypeScript)
- **In-Memory Frequency Lists**: Startup loading of word frequency data for vocabulary decisions
- **Proxy Architecture**: Server-side API key management for security
- **Rate Limiting**: Custom in-memory rate limiter (10 requests/minute per IP)
- **File Validation**: Size limits (5MB) and type validation for security

### Subtitle Fusion Algorithm
- **Vocabulary-Based Selection**: Intelligent language switching based on word frequency rankings
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions
- **Lemmatization**: Uses `simplemma` library for word stemming across languages (smart top-200 preservation)
- **Inline Translation**: OpenAI GPT-4.1 Nano (primary) + DeepL (fallback) via regex word boundaries
- **Native Fallback**: Replaces with native subtitle if translation fails
- **Proper Noun Detection**: 2-phase detection (capitalization → lemmatization → frequency check) to distinguish proper nouns from rare words

## Key Implementation Details

### Netflix Integration (`page-script.ts`)
- Overrides `JSON.parse` to capture subtitle data from Netflix API responses
- Converts WebVTT format to SRT using browser TextTrack API
- Implements polling mechanism for detecting episode changes
- Handles subtitle injection via custom WebVTT track creation

### Subtitle Processing (`smartsub-api/src/subtitle_fusion.py`)
- Core fusion algorithm with vocabulary-based language switching
- ~30% inline translations, ~20% native replacements per episode (typical)
- Supports 4 languages: English (EN), French (FR), Portuguese (PT), Spanish (ES)
- Maintains temporal alignment between different subtitle versions
- **Word Analysis**: `_analyze_subtitle_words()` with 2-phase proper noun detection (Nov 2025 refactor)
- **Translation Application**: `apply_translation()` with regex word boundaries to prevent partial matches
- **Native Fallback**: Graceful degradation when translation fails (~0% with GPT-4.1 Nano)

### Security Implementation
- **API Key Protection**: Server-side proxy prevents client-side API key exposure
- **CORS Security**: Restricted to Netflix domains only
- **File Size Validation**: DoS protection with 5MB upload limits
- **Rate Limiting**: Custom implementation prevents abuse

## Supported Languages

- **Target Languages (User-Selectable)**: Portuguese (PT-BR), French (FR)
- **Native Languages**: 13 languages (English, French, Spanish, German, Italian, Portuguese, Polish, Dutch, Swedish, Danish, Czech, Japanese, Korean)
- **Backend Support**: API supports EN/FR/PT/ES (EN removed from UI only, backend unchanged)
- **BCP47 Normalization**: Netflix regional variants (es-ES, pt-BR, etc.) automatically mapped to base languages
- **Dynamic Detection**: Extension detects available Netflix subtitle languages in real-time
- **DeepL Integration**: All supported languages have proper DeepL API mapping for translations

## Testing

### Running Chrome Extension Tests
Load the extension in Chrome Developer mode:
1. `npm run build` in the TypeScript directory
2. Load `dist/` folder as unpacked extension
3. Navigate to Netflix and test subtitle processing

### Running API Tests
```bash
# Comprehensive API testing
python test_fuse_subtitles_endpoint.py

# Unit tests for core modules
python -m pytest tests/ -v
```

## Deployment

### Railway Deployment (Production)
- Live API: `https://smartsub-api-production.up.railway.app`
- Multi-stage Docker build with Node.js + Python runtime
- Environment variables for API keys and configuration
- Health checks and monitoring enabled

### Chrome Web Store
- **Status**: ✅ Production-ready (Phase 4 complete - January 13, 2025)
- **Extension ID**: `lhkamocmjgjikhmfiogfdjhlhffoaaek`
- **Name**: Subly - Smart Netflix Subtitles
- **Version**: 1.1.0+ (production deployment with Stripe LIVE)
- **Note**: manifest.json `"key"` field must match Chrome Web Store for updates
- **Build**: Use `npm run build:production` for Chrome Web Store submissions

### Local Development
- Chrome extension runs locally via developer mode
- API server runs on localhost with CORS enabled for development
- Docker setup available for full-stack local testing

## Environment Variables

```bash
# Required for API functionality
DEEPL_API_KEY=your_deepl_api_key_here
RAILWAY_API_KEY=your_railway_api_key_here
API_KEY=your_api_authentication_key_here

# Optional configuration
MAX_FILE_SIZE=5242880  # 5MB in bytes
```

## Common Development Tasks

### Adding New Language Support
1. Add frequency list file to `smartsub-api/src/frequency_lists/`
2. Update language mapping in `frequency_loader.py`
3. Add lemmatization support in `lemmatizer.py`
4. Update DeepL language code mapping in `deepl_api.py`
5. Add to TARGET_LANGUAGES in `webapp/src/pages/Languages.tsx`
6. Add to target-language dropdown in `popup.html`

### Debugging Chrome Extension Issues
1. Check browser console for page-script errors
2. Inspect extension popup for UI issues
3. Monitor network requests to API endpoint
4. Verify Chrome storage for persistent settings

### Testing Subtitle Processing
1. Use test SRT files in `smartsub-api/tests/`
2. Test with different language combinations
3. Verify vocabulary-based switching logic
4. Check inline translation functionality

## Important Files

### Chrome Extension Core Files
- `src/page-script.ts` - Netflix integration and JSON hijacking (918 lines)
- `src/popup/Popup.tsx` - React UI with Shadcn + Tailwind v4
- `src/popup/index.tsx` - React entry point
- `src/content-script.ts` - Message passing coordination
- `src/api/railwayClient.ts` - API communication client

### Backend Core Files
- `main.py` - FastAPI application with security middleware (240+ lines)
- `src/subtitle_fusion.py` - Core fusion algorithm (Python migration)
- `src/srt_parser.py` - SRT format parsing and generation
- `src/frequency_loader.py` - In-memory frequency list management
- `src/deepl_api.py` - DeepL integration with language mapping

### Configuration Files
- `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/package.json` - Extension dependencies and build scripts
- `webapp/package.json` - Webapp dependencies (React, Vite, Shadcn UI)
- `smartsub-api/requirements.txt` - Python dependencies
- `Dockerfile` - Multi-stage build for Node.js + Python deployment
- `ROADMAP.md` - Phase 1B-3 roadmap (Supabase Auth → Billing → Launch)

## Recent Architecture Changes (October 2025)

### Phase 1A - Webapp Foundation ✅ **COMPLETED**
**Decision**: External webapp instead of in-extension React for onboarding/dashboard/account management.

**Rationale**:
- Multi-device sync requires backend (Supabase)
- Auth + subscription management needs web interface
- Pattern used by Language Reactor, Grammarly, Loom

**Implementation**:
- Created `webapp/` with React 19 + Vite + TypeScript
- Installed Shadcn UI components (Button, Select, RadioGroup, Label)
- Added React Router with `/onboarding` and `/dashboard`
- Extension opens webapp on install via background service worker

**Code Location**: `webapp/`, `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/background.ts`

### Phase 1B - Supabase Auth + Popup Redesign ✅ **COMPLETED** (January 2025)
**Auth**: Google OAuth + Supabase session sync between webapp and extension
**Popup Redesign**:
- Removed Smart Subtitles toggle (always enabled)
- Replaced vocab dropdown with read-only Card displaying level from Supabase
- Added "Test my level" button linking to `/onboarding/vocab-test`
- Added feedback banner with contact email
- Fixed `background.ts` to use `WEBAPP_URL` env variable (staging/production)
- Fixed `manifest.json` `externally_connectable` to allow staging + production URLs
**Code**: `src/popup/popup.{ts,html,css}` (vanilla JS - migrated to React in Phase 1C)

### Phase 1C - Extension Popup React Migration ✅ **COMPLETED** (November 2025)
**Tech Stack**: React 19 + Shadcn UI + Tailwind v4 + Webpack 5
**Implementation**:
- Migrated vanilla JS popup to React + TypeScript
- Added Shadcn components (Button, Select, Card, Label)
- Configured Tailwind v4 with PostCSS (CSS-first config)
- Welcome popup for new users (no vocab level)
- Inline Supabase sync on language change (KISS - reuses `loadSettings()`)
- Fixed vocab level reload bug when switching languages

**Bundle**: 480KB (React + Shadcn), acceptable for popup
**Code**: `src/popup/{Popup.tsx,index.tsx,styles.css}`, `postcss.config.js`, `components.json`

---

## Recent Critical Bug Fixes (January 2025)

### Chrome Extension Permission Optimization ✅ **COMPLETED** (November 2025)
**Problem**: Extension displayed alarming "Read your browsing history" warning during installation, reducing user trust.

**Root Cause**: `"tabs"` permission grants access to sensitive tab properties (url, title) across all tabs, triggering privacy warning.

**Solution**: Replaced `"tabs"` with `"activeTab"` permission in manifest.json.
- **activeTab**: Temporary access to current tab only when user clicks extension icon (no warning)
- **Zero code changes**: All `chrome.tabs.query()` and `chrome.tabs.sendMessage()` calls work identically

**Results**: Installation warning reduced from 2 to 1 - only displays necessary "Read and change data on www.netflix.com" (required for subtitle injection).

**Code Location**: `manifest.json` lines 10-13

### Multi-Language Support Extension ✅ **COMPLETED**
**Feature**: Extended native language support from 3 to 13 languages with BCP47 normalization.
- **Implementation**: Extended DeepL mappings, added Netflix BCP47 variant mapping (es-ES→es, pt-BR→pt)
- **UI Enhancement**: Dynamic native language dropdown with "(Undetected)" state and help text
- **Error Reduction**: Removed false-positive error messages due to Netflix lazy loading

**Code Location**: `deepl_api.py`, `content-script.ts`, `Popup.tsx`

### Word Alignment Bug Resolution ✅ **COMPLETED** (Nov 2025 - Architecture Refactor)
**Problem**: "Marie-Antoinette" split into 2 words → "et" incorrectly translated inside "Antoin**et (and)**te"

**Root Cause**: Complex TokenMapping alignment + hyphenated word splitting + index-based translation application

**Solution (Architecture Refactor - Nov 2025)**: Simplified approach with regex word boundaries
- **Removed**: TokenMapping system, `create_alignment_mapping()` (~100 lines dead code)
- **Added**: `apply_translation()` with regex `\b + word + \b` + IGNORECASE flag
- **Added**: `_analyze_subtitle_words()` for 2-phase proper noun detection (capitalization → lemmatization → frequency check)
- **Added**: `get_full_list()` to distinguish rare words (translate) vs proper nouns (keep)

**Benefits**: 75% complexity reduction, bug 100% resolved, architecture simplified

**Code Location**: `smartsub-api/src/subtitle_fusion.py`
- `apply_translation()` lines 18-59
- `_analyze_subtitle_words()` lines 169-283
- See `smartsub-api/WORD_ALIGNMENT_ARCHITECTURE.md` for full architectural decisions

### Portuguese Lemmatization Bug Resolution ✅ **COMPLETED** (January 2025)
**Problem**: Portuguese word "uma" (rank 26) incorrectly lemmatized to non-existent "umar" by simplemma, causing false unknown word detection.

**Root Cause**: Known issue in Portuguese NLP tools (spaCy Issue #1718, simplemma) where function words are incorrectly lemmatized.

**Solution**: Smart conditional lemmatization based on frequency ranking - top 200 frequent words preserved in original form.

**Implementation**:
- `smart_lemmatize_line()` and `should_lemmatize_word()` in `lemmatizer.py`
- Used in `_analyze_subtitle_words()` for proper noun detection (Nov 2025 refactor)
- Universal solution for all languages with 200-word threshold

**Results**: "uma" preserved as "uma" instead of lemmatized to "umar", function words correctly recognized.

**Code Location**: `smartsub-api/src/lemmatizer.py`

### Diagnostic Logging Enhancement
Added comprehensive logging system in `frequency_loader.py:get_word_rank()` and `subtitle_fusion.py` for debugging word processing decisions with original word, lemmatized word, frequency rank, and final decision tracking.

### Translation Index Misalignment Bug ✅ **FIXED** (January 2025)
**Problem**: 33% translation failures (116/348 words) - index-based matching broke when OpenAI returned N±X translations instead of exactly N.

**Root Cause**: System used index-based matching (`translations[idx]`). When OpenAI returned 14/18 translations, indices shifted causing wrong translations applied to wrong subtitles.

**Solution**: Dict-based matching with word keys instead of index matching. Tolerates count mismatches gracefully.

**Implementation**:
- `openai_translator.py`: Changed return type `List[str]` → `Dict[str, str]`, removed dead cache code
- `subtitle_fusion.py`: Changed from `translations[idx]` to `translations.get(word)` for word-based lookup
- Total changes: 2 files, 28 additions, 30 deletions (-2 lines net)

**Results**: Translation success 67% → 96.6% (348 sent → 238 received in Episode 1 test).

**Code Location**: `smartsub-api/src/openai_translator.py`, `smartsub-api/src/subtitle_fusion.py`

### OpenAI Punctuation Normalization Bug ✅ **FIXED** (January 2025)
**Problem**: 17-32% translation failures due to OpenAI normalizing punctuation in returned words.

**Pattern**: OpenAI strips brackets and punctuation from words:
- Sent: `['sighs]', '[boy]', 'sorrindo.', 'experiência?']`
- Received: `['sighs', 'boy', 'sorrindo', 'experiência']`
- Result: Dict lookup fails (key mismatch)

**Solution**: Pre-clean punctuation before sending to OpenAI, then rebuild with correct placement.

**Implementation**:
- `clean_word_for_translation()`: Strips leading/trailing punctuation (ASCII + Unicode)
- `extract_trailing_punctuation()`: Extracts trailing punctuation for reapplication
- Translation placement: `word (translation)punctuation` (e.g., "tensão (tension)]")

**Results**: Translation success 67% → 79.8% (206/258 translations applied successfully)

**Code Location**: `smartsub-api/src/subtitle_fusion.py` - Two utility functions + modified translation flow

### OpenAI Translation Performance Optimization ✅ **COMPLETED** (January 2025)
**Problem**: Translation processing took 7-10 seconds per episode due to conservative concurrency limits.

**Solution**: Increased parallel API requests from 5 to 8 concurrent requests using native FastAPI async/await pattern.

**Implementation**: 3-file minimal change - `main.py:291` (pass parameter), `subtitle_fusion.py:418` (add parameter), `subtitle_fusion.py:689` (use parameter).

**Results**: Translation time reduced 7.80s → 3.95s (-49%), total processing 10.03s → 6.87s (-32%). Rate limit usage: 38% of OpenAI's 500 RPM limit.

**Code Location**: `smartsub-api/main.py`, `smartsub-api/src/subtitle_fusion.py`

### Subtitle Loss Bug - Cache Deduplication Removal ✅ **COMPLETED** (January 2025)
**Problem**: Subtitles with same unknown word (e.g., "suspira" in PT 100, 496, 700) disappeared - only last subtitle kept due to dict overwriting.

**Solution**: Replaced `word_to_subtitle_mapping` dict with `subtitles_to_translate` list of tuples. Each (word, subtitle) preserved, no deduplication.

**Results**: All subtitles preserved. Cost increase: +$0.00002/episode (+30% tokens, negligible). Code simplified (-20 lines).

**Code Location**: `smartsub-api/src/subtitle_fusion.py` lines 509-869

### Perfect Contextual Translation ✅ **COMPLETED** (January 2025)
**Problem**: Same word translated identically regardless of context (e.g., "banco" = "banque" in both "sentei no banco" and "Banco do Brasil").

**Solution**: Each (word, subtitle) tuple gets unique context translation using unique keys (word_0, word_1, etc.). No word deduplication.

**Results**: Context-perfect translations for language learning. Cost: +50% tokens (+$0.00002/episode), +1s latency. Quality over cost for educational product.

**Code Location**: `smartsub-api/src/subtitle_fusion.py` lines 774-869

### Double Subtitle Display - Avalanche Fix ✅ **COMPLETED** (January 2025)
**Problem**: PT and FR subtitles displayed simultaneously on Netflix. PT 633 (4 unknown words) combined FR 629+630, "avalanching" PT 632 into replacement, preventing its inline translation.

**Solution**: Filter FR candidates by comparing overlap with previous PT subtitle (symmetry with existing "next PT" logic). FR 629 excluded from PT 633 (better match with PT 632: 1.958s vs 0.625s).

**Results**: No double display. PT 632 receives inline translation, PT 633 replaced by FR 630 only (not FR 629+630 block).

**Code Location**: `smartsub-api/src/subtitle_fusion.py` - `_get_previous_target_subtitle()` helper, lines 658-692 filtering logic

## Memory Leak Resolution (January 2025)

### Problem Resolution ✅ **COMPLETED**
**Problem**: Chrome extension experienced memory corruption after 40+ minutes of continuous Netflix viewing, causing subtitle malfunction requiring Cmd+Shift+R to fix.

**Root Cause**: Chrome puts extension processes to sleep after extended periods (~40+ minutes), causing memory corruption in Netflix subtitle injection system.

**Solution**: Minimal polling approach (20 lines) that prevents Chrome from putting the extension to sleep:

```typescript
// MINIMAL POLLING SOLUTION - PREVENTS 40+ MINUTE MEMORY LEAKS
let pollingStartTime = Date.now();
setInterval(() => {
  const videoElement = document.querySelector('video');
  const playerElement = document.querySelector('.watch-video');
  const ourTrackExists = document.getElementById(TRACK_ELEM_ID) !== null;

  const elapsed = Date.now() - pollingStartTime;
  if (elapsed % 300000 < 1000) { // Every 5 minutes
    console.log('Smart Netflix Subtitles: Polling active - preventing memory leaks', {
      timeElapsed: `${Math.floor(elapsed / 1000)}s`,
      hasVideo: !!videoElement,
      hasPlayer: !!playerElement,
      hasOurTrack: ourTrackExists
    });
  }
}, 1000);
```

**Code Location**: `src/page-script.ts` lines 925-948

**Testing Results**: ✅ 46+ minutes stable operation, ✅ polling logs appearing every 5 minutes, ✅ all core functionality preserved

## Netflix Preload Issue Resolution (January 2025)

### Problem Resolution ✅ **COMPLETED**
**Problem**: Subtitles became incorrect at ~36 minutes consistently, requiring manual refresh to fix.

**Root Cause**: Netflix preloads next episode data around 36 minutes, triggering auto-processing of wrong subtitle tracks while current episode still playing.

**Solution**: Complete auto-processing removal - manual "Process Subtitles" button click required:

```typescript
// AUTO-PROCESSING DISABLED - User must manually click "Process Subtitles" button
// This prevents processing Netflix preload data (which caused subtitle corruption at ~36min)
console.log('Smart Netflix Subtitles: Auto-processing disabled - subtitles available for manual processing');
```

**Code Changes**:
- Removed 40 lines of auto-processing logic from `extractMovieTextTracks()`
- Preserved manual processing flow via popup button
- Cleaned up debugging artifacts (70+ lines)

**Testing Results**: ✅ 40+ minutes stable operation, ✅ no subtitle corruption, ✅ Netflix preload detected but ignored

### EasySubs Future Architecture Analysis
**Decision**: Chose minimal polling solution over complex EasySubs refactor for this specific memory leak problem.

**EasySubs Approach Reserved for Future**: When adding multiple streaming platforms, advanced UI features, or learning analytics - documented in MASTER_DOC.md "Memory Leak Resolution & Future Architecture" section.

**Key Lesson**: Simple solutions for simple problems. Complex architecture only when complexity is genuinely needed (YAGNI principle).

## Extension-Webapp Supabase Sync (January 2025)

### Current Implementation: Inline Sync (KISS)
When user changes language in popup → Updates 2 places:
1. `chrome.storage.local` (instant, local persistence)
2. Supabase `user_settings` table (multi-device sync) - **INLINE in handlers**

**Why Inline?** YAGNI principle - Only 2 call sites, simple UPDATE query, easier debugging.

**Security:** ✅ RLS policies enforce user isolation, session validated before UPDATE.

**Future Trigger:** If sync logic becomes complex (retry, offline queue, >3 fields) → Refactor to centralized service.

**Code:** `src/popup/Popup.tsx` lines 285-329

---

## Development Best Practices (Lessons Learned)

### ROADMAP Progress Tracking
- **Always Check Boxes**: When implementing tasks from ROADMAP.md, ALWAYS check off `[ ]` → `[x]` for completed items immediately after finishing them
- **Show Progress**: Checking boxes provides clear visual progress tracking and prevents duplicate work
- **Mark Dates**: Add completion dates (e.g., `✅ PASSED (January 20, 2025)`) for historical reference
- **Update Details**: Update task details if actual implementation differs from plan (e.g., different test values)
- **Systematic Approach**: Read ROADMAP.md at start of session, check boxes as you complete each step, verify all related checkboxes are updated before moving to next major task

### Migration Plan Tracking
- **Check Off As You Go**: When following markdown migration plans (e.g., NEXT_MIGRATION_PLAN.md), ALWAYS check off `[ ]` → `[x]` for completed items immediately after finishing them
- **Mark Phase Status**: Update phase headers with status indicators:
  - `✅ COMPLÉTÉ` for fully completed phases
  - `🚧 EN COURS (1/9 pages)` for partially completed phases with progress count
  - `⏳ À TESTER` for items awaiting user testing/validation
- **Real-Time Updates**: Update checkboxes during work, not after the entire session
- **Test Tracking**: Mark intermediate test results with `✅ RÉUSSI` or `❌ ÉCHOUÉ` to track validation
- **Never Skip This**: Checking off items prevents confusion about what's done and what remains

### Railway Deployment
- **Cache Issues**: Railway caches Docker layers aggressively - use cache busting or modify requirements.txt to force rebuilds
- **Test Locally First**: Always test new dependencies locally before Railway deployment
- **Check Build Logs**: First thing to check when deployments fail
- **Custom Implementations**: Often simpler and more reliable than external libraries for critical features

### Rate Limiting
- **Custom > External**: Custom in-memory rate limiter (20 lines) more reliable than external library on Railway
- **HTTP Middleware**: Correct place for rate limiting (before validation)
- **In-Memory OK**: Sufficient for single-instance deployments

### Problem-Solution Matching
- **KISS Principle**: Keep It Simple, Stupid - avoid over-engineering
- **Match Complexity**: Simple solutions for simple problems (e.g., minimal polling for memory leak vs full EasySubs refactor)
- **Incremental Testing**: Test at each step, don't batch changes
- **Git Safety**: Always commit working state before major changes

### Translation Architecture
- **Dict vs Index Matching**: Dict-based matching tolerates count mismatches, index-based breaks on N±X returns
- **Punctuation Handling**: Pre-clean words before translation, reapply punctuation after (NLP best practice)
- **Diagnostic Logging**: Essential for debugging LLM API inconsistencies
- **Contextual Translation**: Each (word, subtitle) pair needs unique context for quality language learning
- **Known Limitation**: Dict collisions when same cleaned word appears multiple times in one batch (~0.5-1% frequency)

---

## 🔄 Technical Debt & Future Refactoring

### Current Architecture (Phase 1 - MVP - January 2025)

**Onboarding Flow:**
- **Approach:** Hybrid (structured but simple - no over-engineering)
- **Components:** Separate files for ProgressBar, BackButton, FeedbackBanner, ImagePlaceholder
  - Reason: Ultra-simple (10-15 lines each), keeps layout readable
  - Total: 6 files, ~130 lines
- **Context:** Simple React state only (no sessionStorage, no persistence)
  - Decision: YAGNI - Users can restart onboarding if they refresh (rare case)
- **What we avoided:** sessionStorage, clearOnboardingData(), complex state management

**Why this approach?**
- ✅ Avoids premature optimization (YAGNI principle)
- ✅ Future-proof (components ready for reuse without refactoring)
- ✅ Maintainable (layout stays <100 lines even with Phase 2/3 additions)
- ✅ Standard (follows Next.js/Shadcn UI patterns)

### Future Refactoring Triggers

**Add sessionStorage when:**
- Analytics show >5% of users refresh during onboarding and lose data
- Support requests about lost onboarding progress become frequent
- Implementation: ~30 lines in OnboardingContext.tsx

**Refactor layout when:**
- OnboardingLayout.tsx exceeds 200 lines
- Need to reuse components (ProgressBar, etc.) in dashboard or other pages outside onboarding
- Consider: Extract to shared components library

**Consider state management library when:**
- App has >5 contexts with complex interdependencies
- Need global state synchronization across multiple features
- Options: Zustand (lightweight), Redux Toolkit (enterprise)

**Add form validation library when:**
- Onboarding forms become more complex (>5 input fields per page)
- Need advanced validation (async validation, dependent fields)
- Options: Zod + React Hook Form

### Technical Debt Monitoring

**Low Priority (monitor, don't fix yet):**
- sessionStorage for onboarding persistence
- Split components into shared library

**Medium Priority (fix if it becomes painful):**
- Refactor OnboardingLayout if it exceeds 200 lines
- Add analytics to track user drop-off points

**High Priority (fix immediately if occurs):**
- Context provider nesting exceeds 3 levels
- Component files exceed 300 lines
- Duplication of same code in >3 places

### Decision Log

**January 2025 - Onboarding Architecture:**
- ✅ Chose hybrid approach (structured but simple)
- ❌ Rejected full KISS (everything in 1 file) - would become unmaintainable
- ❌ Rejected full structure (sessionStorage, complex state) - premature optimization
- **Result:** Sweet spot for MVP that scales to Phase 2/3