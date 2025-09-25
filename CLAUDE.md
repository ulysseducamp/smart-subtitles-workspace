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

# Production build
npm run build

# Type checking
npm run type-check

# Clean build artifacts
npm run clean

# Linting
npm run lint
```

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
- **Auto-Processing**: Automatic subtitle processing on episode changes with polling mechanism

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

- **English (EN)**: Full support with contraction handling
- **French (FR)**: Lemmatization and frequency-based vocabulary
- **Portuguese (PT)**: Simplified pt-BR → pt mapping
- **Spanish (ES)**: Complete frequency list integration

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

### Diagnostic Logging Enhancement
Added comprehensive logging system in `frequency_loader.py:get_word_rank()` and `subtitle_fusion.py` for debugging word processing decisions with original word, lemmatized word, frequency rank, and final decision tracking.