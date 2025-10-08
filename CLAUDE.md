# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Smart Subtitles - a comprehensive language learning platform that creates personalized Netflix viewing experiences through intelligent bilingual subtitle adaptation. The system automatically switches between target language subtitles and native language subtitles based on the user's vocabulary knowledge.

## Architecture

The project consists of three main components working together:

1. **Chrome Extension** (`netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/`) - Netflix integration for subtitle extraction and injection
2. **FastAPI Backend** (`smartsub-api/`) - Subtitle processing API with Python fusion algorithm
3. **Reference Implementation** (`netflix-smart-subtitles-chrome-extension/reference/`) - Based on Subadub extension

### High-Level Data Flow
```
Chrome Extension (Netflix) → FastAPI API → Python Fusion Algorithm → Processed Subtitles → Chrome Extension
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
- **Development/Testing**: ALWAYS use `npm run build:staging` → Extension pointe vers `smartsub-api-staging.up.railway.app`
- **Production/Distribution**: Use `npm run build:production` → Extension pointe vers `smartsub-api-production.up.railway.app`
- **Branch staging**: `develop` → auto-deploy to staging API
- **Branch production**: `main` → auto-deploy to production API

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

# Run specific API test
python test_fuse_subtitles_endpoint.py
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
- **Three-script pattern**: `popup.ts` ↔ `content-script.ts` ↔ `page-script.ts`
- **JSON Hijacking**: Intercepts Netflix API responses by overriding `JSON.parse()`
- **Message Passing**: Chrome extension message system for cross-context communication
- **State Management**: Persistent settings via `chrome.storage.local`
- **Manual Processing**: User must click "Process Subtitles" button (auto-processing disabled to prevent Netflix preload corruption)

### API Backend Architecture
- **Pure Python Fusion**: Direct function calls to Python subtitle fusion algorithm (migrated from TypeScript)
- **In-Memory Frequency Lists**: Startup loading of word frequency data for vocabulary decisions
- **Proxy Architecture**: Server-side API key management for security
- **Rate Limiting**: Custom in-memory rate limiter (10 requests/minute per IP)
- **File Validation**: Size limits (5MB) and type validation for security

### Subtitle Fusion Algorithm
- **Vocabulary-Based Selection**: Intelligent language switching based on word frequency rankings
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions
- **Lemmatization**: Uses `simplemma` library for word stemming across languages
- **Inline Translation**: DeepL API integration for unknown words
- **Contraction Handling**: English contraction expansion for better vocabulary matching
- **TokenMapping System**: Industry-standard NLP approach for preserving word alignment during processing

## Key Implementation Details

### Netflix Integration (`page-script.ts`)
- Overrides `JSON.parse` to capture subtitle data from Netflix API responses
- Converts WebVTT format to SRT using browser TextTrack API
- Implements polling mechanism for detecting episode changes
- Handles subtitle injection via custom WebVTT track creation

### Subtitle Processing (`smartsub-api/src/subtitle_fusion.py`)
- Core fusion algorithm with vocabulary-based language switching
- Processes approximately 72% of subtitles with intelligent replacements
- Supports 4 languages: English (EN), French (FR), Portuguese (PT), Spanish (ES)
- Maintains temporal alignment between different subtitle versions
- **TokenMapping System**: Resolves word alignment issues between original and processed words using industry-standard NLP tokenization approach

### Security Implementation
- **API Key Protection**: Server-side proxy prevents client-side API key exposure
- **CORS Security**: Restricted to Netflix domains only
- **File Size Validation**: DoS protection with 5MB upload limits
- **Rate Limiting**: Custom implementation prevents abuse

## Supported Languages

- **13 Safe Languages**: English, French, Spanish, German, Italian, Portuguese, Polish, Dutch, Swedish, Danish, Czech, Japanese, Korean
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
- `src/popup/popup.ts` - User interface and settings management
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
- `smartsub-api/requirements.txt` - Python dependencies
- `Dockerfile` - Multi-stage build for Node.js + Python deployment
- `MASTER_DOC.md` - Comprehensive project documentation (720+ lines)

## Recent Critical Bug Fixes (January 2025)

### Multi-Language Support Extension ✅ **COMPLETED**
**Feature**: Extended native language support from 3 to 13 languages with BCP47 normalization.
- **Implementation**: Extended DeepL mappings, added Netflix BCP47 variant mapping (es-ES→es, pt-BR→pt)
- **UI Enhancement**: Dynamic native language dropdown with "(Undetected)" state and help text
- **Error Reduction**: Removed false-positive error messages due to Netflix lazy loading

**Code Location**: `deepl_api.py`, `content-script.ts`, `popup.ts`, `popup.html`

### Word Alignment Bug Resolution
**Problem**: Basic Portuguese words ("as", "de", "para") were incorrectly translated despite high vocabulary levels due to word-to-lemma alignment issues.

**Root Cause**: The `normalize_words()` function filtered out certain words (single letters, contractions), creating index misalignment between `original_words` and `lemmatized_words` arrays.

**Solution**: Implemented TokenMapping system (`subtitle_fusion.py:TokenMapping`) that preserves alignment between original and processed words using industry-standard NLP tokenization approaches (similar to spaCy, Hugging Face).

**Code Location**: `smartsub-api/src/subtitle_fusion.py`
- `TokenMapping` dataclass with original_index, original_word, normalized_word, lemmatized_word, is_filtered
- `create_alignment_mapping()` function (~40 lines)
- Integration in main `fuse_subtitles()` processing loop

**Validation**: Railway logs confirm proper alignment:
```
DIAGNOSTIC[33]: mot_original='você', mot_lemmatisé='você', mot_recherche='você', rang=7
DECISION[33]: mot='você', lemmatisé='você', recherche='você', connu=OUI (trouvé dans known_words)
```

### Portuguese Lemmatization Bug Resolution ✅ **COMPLETED** (January 2025)
**Problem**: Portuguese word "uma" (rank 26) incorrectly lemmatized to non-existent "umar" by simplemma, causing false unknown word detection.

**Root Cause**: Known issue in Portuguese NLP tools (spaCy Issue #1718, simplemma) where function words are incorrectly lemmatized.

**Solution**: Smart conditional lemmatization based on frequency ranking - top 200 frequent words preserved in original form.

**Implementation**:
- `smart_lemmatize_line()` and `should_lemmatize_word()` in `lemmatizer.py`
- Modified `create_alignment_mapping()` to use smart lemmatization
- Universal solution for all languages with 200-word threshold

**Results**: "uma" preserved as "uma" instead of lemmatized to "umar", function words correctly recognized.

**Code Location**: `smartsub-api/src/lemmatizer.py`, `smartsub-api/src/subtitle_fusion.py`

### Diagnostic Logging Enhancement
Added comprehensive logging system in `frequency_loader.py:get_word_rank()` and `subtitle_fusion.py` for debugging word processing decisions with original word, lemmatized word, frequency rank, and final decision tracking.

### OpenAI Translation Performance Optimization ✅ **COMPLETED** (January 2025)
**Problem**: Translation processing took 7-10 seconds per episode due to conservative concurrency limits.

**Solution**: Increased parallel API requests from 5 to 8 concurrent requests using native FastAPI async/await pattern.

**Implementation**: 3-file minimal change - `main.py:291` (pass parameter), `subtitle_fusion.py:418` (add parameter), `subtitle_fusion.py:689` (use parameter).

**Results**: Translation time reduced 7.80s → 3.95s (-49%), total processing 10.03s → 6.87s (-32%). Rate limit usage: 38% of OpenAI's 500 RPM limit.

**Code Location**: `smartsub-api/main.py`, `smartsub-api/src/subtitle_fusion.py`

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