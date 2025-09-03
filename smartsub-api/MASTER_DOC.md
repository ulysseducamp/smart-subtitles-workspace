# SmartSub API - Master Documentation

## 1. Project Overview

**SmartSub API** is a FastAPI backend service designed to provide bilingual adaptive subtitles for Netflix content. The system intelligently fuses target language subtitles with native language subtitles based on user vocabulary levels, creating personalized subtitle experiences.

**Key Objectives:**
- Generate bilingual subtitles that adapt to user's vocabulary proficiency
- Support multiple languages (EN, FR, PT, ES, DE, IT)
- Integrate with Chrome extension for Netflix
- Provide inline translation capabilities via DeepL API
- Manage frequency lists and vocabulary analysis

**Scope:** Backend API service that processes SRT subtitle files and returns hybrid bilingual subtitles optimized for language learning.

## 2. Tech Stack & Dependencies

### Core Framework
- **FastAPI** v0.104.1 - Modern Python web framework for building APIs
- **Uvicorn** v0.24.0 - ASGI server for running FastAPI applications

### External Services
- **Supabase** v2.3.4 - Backend-as-a-Service for data management
- **DeepL API** - Machine translation service for inline translations

### Language Processing
- **Simplemma** v0.9.1 - Lemmatization library for multiple languages
- **Python-multipart** v0.0.6 - File upload handling

### Development & Deployment
- **Python 3.x** - Core runtime
- **Docker** - Containerization (referenced in CLI paths)
- **Node.js** - CLI integration for subtitle processing

## 3. Project Architecture

### Directory Structure
```
smartsub-api/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── src/                   # Core business logic modules
│   ├── deepl_client.py    # DeepL API integration
│   ├── fusion_algorithm.py # Subtitle fusion core logic
│   ├── lemmatizer_service.py # Word lemmatization
│   └── supabase_client.py # Database operations
├── utils/                 # Utility functions
│   ├── srt_parser.py      # SRT file handling
│   └── vocabulary_analyzer.py # Vocabulary analysis engine
└── __pycache__/           # Python bytecode cache
```

### Core Module Interactions
1. **Main API** (`main.py`) receives requests and orchestrates processing
2. **Fusion Algorithm** coordinates subtitle merging and vocabulary decisions
3. **Vocabulary Analyzer** determines which words need translation
4. **Lemmatizer Service** normalizes words for analysis
5. **DeepL Client** provides inline translations
6. **Supabase Client** manages frequency lists and user data
7. **SRT Parser** handles subtitle file I/O

### Data Flow
```
Upload SRT Files → Parse & Analyze → Vocabulary Decision → Fusion Algorithm → Generate Hybrid SRT → Return Response
```

## 4. Key Components & Files

### Core Application (`main.py`)
- **FastAPI App**: Main application with CORS middleware for Chrome extension
- **SubtitleRequest/Response Models**: Pydantic models for API validation
- **Fuse Subtitles Endpoint**: Main `/fuse-subtitles` POST endpoint
- **CLI Integration**: Subprocess execution of Node.js subtitle processing

### Business Logic (`src/`)
- **FusionAlgorithm**: Core subtitle fusion logic (currently placeholder)
- **VocabularyAnalyzer**: Decision engine for translation strategies
- **LemmatizerService**: Word normalization using Simplemma
- **DeepLClient**: Translation API integration with caching
- **SupabaseClient**: Database operations for frequency lists

### Utilities (`utils/`)
- **SRTParser**: SRT file parsing and generation utilities
- **VocabularyAnalyzer**: Advanced vocabulary analysis with proper noun detection

## 5. Current Features

### ✅ Implemented Features
- **FastAPI Server**: Running on port 3000 with health checks (updated from 8001 due to port blocking)
- **CORS Support**: Configured for Chrome extension integration
- **File Upload Handling**: Accepts SRT files and frequency lists
- **CLI Integration**: Subprocess execution of subtitle processing
- **Basic Error Handling**: Timeout and error response management
- **Temporary File Management**: Secure file handling with cleanup

### 🔄 Partially Implemented
- **DeepL Integration**: Client structure exists, needs actual API calls
- **Supabase Connection**: Client structure exists, needs database setup
- **Lemmatization**: Basic structure with Simplemma integration

### ❌ Not Yet Implemented
- **Subtitle Fusion Algorithm**: Core logic is placeholder
- **Vocabulary Analysis Engine**: Decision making for translation strategies
- **SRT Parsing**: File parsing utilities are placeholder
- **Frequency List Management**: Database integration not functional

## 6. Pending Tasks & Roadmap

### High Priority (Phase 1)
- [ ] **Implement Subtitle Fusion Algorithm** (`src/fusion_algorithm.py`)
  - Port TypeScript logic from `subtitles-fusion-algorithm-public/src/logic.ts`
  - Implement subtitle overlap detection and merging
  - Add vocabulary-based decision making

- [ ] **Complete SRT Parser** (`utils/srt_parser.py`)
  - Port SRT parsing logic from TypeScript implementation
  - Add validation and error handling
  - Implement subtitle object generation

- [ ] **Finish Vocabulary Analyzer** (`utils/vocabulary_analyzer.py`)
  - Port proper noun detection logic
  - Implement frequency-based word analysis
  - Add translation strategy decision engine

### Medium Priority (Phase 2)
- [ ] **DeepL API Integration** (`src/deepl_client.py`)
  - Implement actual translation calls
  - Add 24-hour caching system
  - Add API key validation

- [ ] **Supabase Integration** (`src/supabase_client.py`)
  - Set up database connection
  - Implement frequency list storage/retrieval
  - Add user data management

- [ ] **Lemmatizer Service** (`src/lemmatizer_service.py`)
  - Port exact logic from existing Python script
  - Add contraction handling
  - Implement language-specific processing

### Low Priority (Phase 3)
- [ ] **Enhanced Error Handling**
  - Add detailed logging
  - Implement retry mechanisms
  - Add input validation

- [ ] **Performance Optimization**
  - Add async processing for large files
  - Implement result caching
  - Add progress tracking

- [ ] **Testing & Documentation**
  - Add unit tests
  - API documentation
  - Integration tests

## 7. AI Coding Guidelines

### Code Style & Conventions
- **Python Standards**: Follow PEP 8 with 4-space indentation
- **Type Hints**: Use type annotations for all function parameters and returns
- **Async/Await**: Use async functions for I/O operations
- **Error Handling**: Use proper exception handling with specific error types
- **Documentation**: Include docstrings for all functions and classes

### Naming Conventions
- **Files**: Use snake_case (e.g., `deepl_client.py`)
- **Classes**: Use PascalCase (e.g., `VocabularyAnalyzer`)
- **Functions**: Use snake_case (e.g., `fuse_subtitles`)
- **Variables**: Use snake_case (e.g., `target_language`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)

### Architectural Decisions
- **Modular Design**: Keep business logic separate from API layer
- **Dependency Injection**: Use environment variables for configuration
- **Error Propagation**: Return structured error responses
- **File Handling**: Use temporary files with proper cleanup
- **CLI Integration**: Maintain subprocess execution for existing Node.js logic

### Code Organization Rules
1. **Single Responsibility**: Each module should have one clear purpose
2. **Separation of Concerns**: API, business logic, and utilities should be separate
3. **Configuration**: Use environment variables for external service credentials
4. **Error Handling**: Provide meaningful error messages and proper HTTP status codes
5. **Testing**: Write testable code with clear interfaces

### Future Development Guidelines
- **Consistency**: Follow existing patterns when adding new features
- **Documentation**: Update this master document when adding new components
- **Integration**: Ensure new features work with existing Chrome extension
- **Performance**: Consider async processing for time-consuming operations
- **Security**: Validate all inputs and sanitize file uploads

---

**Last Updated**: Generated from codebase analysis  
**Version**: 0.1.0  
**Status**: Development Phase - Core functionality implementation in progress
