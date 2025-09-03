# Smart Subtitles - Global Master Document

## 1. Project Overview

### Core Concept and Vision
Smart Subtitles is a comprehensive language learning platform that creates personalized Netflix viewing experiences through intelligent bilingual subtitle adaptation. The system automatically switches between target language (language being learned) and native language subtitles based on the user's vocabulary knowledge, making language learning seamless and engaging.

### Project Scope
This repository contains three interconnected subprojects that work together to deliver the complete Smart Subtitles experience:

1. **Chrome Extension** (`netflix-smart-subtitles-chrome-extension/`): Netflix integration for subtitle extraction and injection ✅ **COMPLETED**
2. **Subtitle Fusion Algorithm** (`subtitles-fusion-algorithm-public/`): Core TypeScript/Node.js engine for intelligent subtitle processing ✅ **COMPLETED**
3. **API Backend** (`smartsub-api/`): FastAPI server that orchestrates the fusion process and manages data 🔄 **Phase 2.1 COMPLETED, Phase 2.2 (Railway) PENDING**

### Key Objectives
- **Adaptive Learning**: Automatically adjust subtitle difficulty based on vocabulary knowledge
- **Seamless Netflix Integration**: Extract, process, and inject personalized subtitles in real-time
- **Vocabulary Building**: Provide inline translations for unknown words
- **Multi-language Support**: Support English, French, Portuguese, Spanish, German, and Italian
- **Performance**: Process subtitles in under 10 seconds for episode-based workflow

### Target Users
- **Language learners** at intermediate to advanced levels
- **Netflix viewers** who want personalized subtitle experiences
- **Self-directed learners** seeking adaptive content
- **Educators** creating personalized learning materials

## 2. Tech Stack & Dependencies

### Chrome Extension
- **TypeScript**: v5.3.2 - Core development language ✅ **COMPLETED**
- **Webpack**: v5.89.0 - Build system ✅ **COMPLETED**
- **Chrome Extension APIs**: Manifest V3 compatible ✅ **COMPLETED**
- **Node.js**: v16+ - Development environment ✅ **COMPLETED**

**Dependencies**:
```json
{
  "@types/chrome": "^0.0.260",
  "@types/node": "^20.10.0",
  "copy-webpack-plugin": "^11.0.0",
  "ts-loader": "^9.5.1",
  "typescript": "^5.3.2",
  "webpack": "^5.89.0",
  "webpack-cli": "^5.1.4"
}
```

### Subtitle Fusion Algorithm
- **TypeScript**: v5.0.0 - Core application logic ✅ **COMPLETED**
- **Node.js**: v16+ - Runtime environment ✅ **COMPLETED**
- **Python 3**: Lemmatization using `simplemma` library ✅ **COMPLETED**
- **DeepL API**: Translation service integration ✅ **COMPLETED**

**Dependencies**:
```json
{
  "@types/node": "^20.8.10",
  "typescript": "^5.0.0",
  "@types/dotenv": "^6.1.1",
  "dotenv": "^17.2.1",
  "node-snowball": "^0.8.0",
  "snowball": "^0.3.1"
}
```

**Python Dependencies**:
```
simplemma==0.9.1
```

### API Backend
- **Python**: v3.11+ - Backend runtime ✅ **COMPLETED**
- **FastAPI**: v0.104.1 - Web framework ✅ **COMPLETED**
- **Uvicorn**: v0.24.0 - ASGI server ✅ **COMPLETED**
- **Supabase**: v2.3.4 - Database and storage 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **Simplemma**: v0.9.1 - Lemmatization 🔄 **STRUCTURE READY, INTEGRATION PENDING**

**Dependencies**:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
supabase==2.3.4
simplemma==0.9.1
```

## 3. Project Architecture

### High-Level Architecture
```
Chrome Extension (Netflix) ✅ COMPLETED
         ↓
    API Backend (FastAPI) 🔄 Phase 2.1 COMPLETED, Phase 2.2 PENDING
         ↓
Subtitle Fusion Algorithm (TypeScript/Node.js) ✅ COMPLETED
         ↓
    Supabase Database 🔄 STRUCTURE READY, INTEGRATION PENDING
```

### Directory Structure & Roles

#### Root Level
- **`MASTER_PLAN.md`**: Strategic development roadmap and phase planning ✅ **UPDATED**
- **`MASTER_DOC.md`**: This comprehensive project documentation ✅ **UPDATED**
- **`TRANSIENT_PLAN_FOR_2.2.md`**: Railway deployment plan 🔄 **ACTIVE PLANNING**

#### Chrome Extension (`netflix-smart-subtitles-chrome-extension/`) ✅ **COMPLETED**
- **`my-netflix-extension-ts/`**: TypeScript version (primary) ✅ **PRODUCTION READY**
  - **`src/`**: Source code with TypeScript ✅ **COMPLETED**
  - **`dist/`**: Compiled JavaScript output ✅ **COMPLETED**
  - **`manifest.json`**: Chrome extension configuration ✅ **COMPLETED**
- **`my-netflix-extension/`**: JavaScript version (legacy) ✅ **FUNCTIONAL**
- **`reference/subadub/`**: Reference implementation based on Subadub ✅ **REFERENCE READY**

#### Subtitle Fusion Algorithm (`subtitles-fusion-algorithm-public/`) ✅ **COMPLETED**
- **`src/`**: Core TypeScript source code ✅ **COMPLETED**
- **`scripts/`**: Python lemmatization scripts ✅ **COMPLETED**
- **`frequency-lists/`**: Word frequency data for multiple languages ✅ **COMPLETED**
- **`dist/`**: Compiled JavaScript output ✅ **COMPLETED**
- **`tests/`**: Test files and validation 🔄 **BASIC TESTS ONLY**

#### API Backend (`smartsub-api/`) 🔄 **Phase 2.1 COMPLETED, Phase 2.2 PENDING**
- **`main.py`**: FastAPI application entry point ✅ **COMPLETED**
- **`src/`**: Core Python modules 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **`venv/`**: Python virtual environment ✅ **READY**
- **`requirements.txt`**: Python dependencies ✅ **COMPLETED**

### Core Module Interactions

#### 1. Chrome Extension → API Backend ✅ **READY FOR INTEGRATION**
- **Extraction**: Chrome extension extracts Netflix subtitles using JSON hijacking ✅ **COMPLETED**
- **Upload**: Ready to send SRT files to `/fuse-subtitles` endpoint ✅ **API READY**
- **Injection**: Receives processed subtitles and injects them back into Netflix ✅ **COMPLETED**

#### 2. API Backend → Fusion Algorithm ✅ **COMPLETED**
- **Orchestration**: FastAPI manages file uploads and CLI execution ✅ **COMPLETED**
- **CLI Wrapper**: Executes TypeScript fusion algorithm as subprocess ✅ **COMPLETED**
- **Response Handling**: Processes results and returns to extension ✅ **COMPLETED**

#### 3. Data Management 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **Supabase**: Stores frequency lists and user data 🔄 **PROJECT CONFIGURED, INTEGRATION PENDING**
- **Frequency Lists**: Multi-language vocabulary data for algorithm decisions ✅ **UPLOADED TO SUPABASE**
- **User Progress**: Future implementation for personalized learning

## 4. Key Components & Files

### Chrome Extension Core Files ✅ **COMPLETED**
- **`content-script.ts`**: Message passing between popup and page script ✅ **COMPLETED**
- **`page-script.ts`**: JSON hijacking for Netflix subtitle extraction ✅ **COMPLETED**
- **`popup.ts`**: User interface and Chrome extension API communication ✅ **COMPLETED**
- **`types/netflix.d.ts`**: TypeScript definitions for Netflix data structures ✅ **COMPLETED**

### Subtitle Fusion Algorithm Core Files ✅ **COMPLETED**
- **`main.ts`**: CLI entry point with argument parsing ✅ **COMPLETED**
- **`logic.ts`**: Core subtitle processing algorithms (686 lines) ✅ **COMPLETED**
- **`deepl-api.ts`**: DeepL API integration with caching and rate limiting ✅ **COMPLETED**
- **`inline-translation.ts`**: Single-word translation service ✅ **COMPLETED**
- **`scripts/lemmatizer.py`**: Python lemmatization using simplemma ✅ **COMPLETED**

### API Backend Core Files 🔄 **Phase 2.1 COMPLETED, Phase 2.2 PENDING**
- **`main.py`**: FastAPI application with `/fuse-subtitles` endpoint ✅ **COMPLETED**
- **`src/supabase_client.py`**: Database connection and frequency list management 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **`src/fusion_algorithm.py`**: Python wrapper for fusion logic 🔄 **PLACEHOLDER, CLI INTEGRATION WORKS**
- **`src/deepl_client.py`**: DeepL API client for Python backend 🔄 **STRUCTURE READY, INTEGRATION PENDING**

### Critical Algorithms & Functions

#### Subtitle Processing (`logic.ts`) ✅ **COMPLETED**
- **`fuseSubtitles()`**: Main fusion function with vocabulary-based decisions ✅ **COMPLETED**
- **`mergeOverlappingSubtitlesInSRT()`**: Temporal alignment algorithm ✅ **COMPLETED**
- **`hasIntersection()`**: Time overlap detection ✅ **COMPLETED**
- **`batchLemmatize()`**: Python subprocess for word stemming ✅ **COMPLETED**

#### Netflix Integration (`page-script.ts`) ✅ **COMPLETED**
- **JSON Hijacking**: Overrides `JSON.parse` to intercept Netflix API responses ✅ **COMPLETED**
- **WebVTT Processing**: Converts Netflix subtitle format to SRT ✅ **COMPLETED**
- **Immediate Injection**: Page script injection for reliable detection ✅ **COMPLETED**

#### API Orchestration (`main.py`) ✅ **COMPLETED**
- **File Management**: Temporary file creation and cleanup ✅ **COMPLETED**
- **CLI Execution**: Subprocess management with timeout handling ✅ **COMPLETED**
- **Error Handling**: Comprehensive error responses and fallbacks ✅ **COMPLETED**

## 5. Current Features

### ✅ Implemented Features

#### Chrome Extension ✅ **COMPLETED**
- **Automatic Subtitle Detection**: Detects available subtitle tracks on Netflix ✅ **COMPLETED**
- **Multiple Language Support**: Supports all Netflix subtitle languages ✅ **COMPLETED**
- **SRT Format Download**: Downloads subtitles in standard SRT format ✅ **COMPLETED**
- **Immediate Injection**: Uses Subadub's approach for reliable detection ✅ **COMPLETED**
- **TypeScript Architecture**: Modern development with type safety ✅ **COMPLETED**
- **Subtitle Injection System**: WebVTT track injection with custom overlay ✅ **COMPLETED**
- **Memory Management**: Robust blob URL cleanup system ✅ **COMPLETED**

#### Subtitle Fusion Algorithm ✅ **COMPLETED**
- **SRT Parsing & Generation**: Full SubRip format support ✅ **COMPLETED**
- **Vocabulary-based Selection**: Intelligent language switching based on word frequency ✅ **COMPLETED**
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions ✅ **COMPLETED**
- **Inline Translation**: Single-word translation using DeepL API ✅ **COMPLETED**
- **Proper Noun Detection**: Smart identification of names and places ✅ **COMPLETED**
- **Contraction Handling**: English contraction processing ✅ **COMPLETED**
- **Overlapping Subtitle Merging**: Temporal alignment of complex sequences ✅ **COMPLETED**
- **CLI Interface**: Comprehensive command-line tool ✅ **COMPLETED**
- **Multi-language Support**: 6 languages with lemmatization ✅ **COMPLETED**

#### API Backend ✅ **Phase 2.1 COMPLETED**
- **FastAPI Framework**: Modern Python web framework ✅ **COMPLETED**
- **File Upload Handling**: Multipart file processing ✅ **COMPLETED**
- **CLI Integration**: Subprocess execution of fusion algorithm ✅ **COMPLETED**
- **CORS Support**: Chrome extension compatibility ✅ **COMPLETED**
- **Error Handling**: Comprehensive error responses ✅ **COMPLETED**
- **Health Checks**: Service monitoring endpoints ✅ **COMPLETED**

### 🔄 Partially Implemented
- **Supabase Integration**: Basic structure ready, full integration pending 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **User Authentication**: Framework ready, implementation pending
- **Performance Metrics**: Basic stats, needs enhancement
- **Error Recovery**: Basic fallbacks, needs robust handling

## 6. Pending Tasks & Roadmap

### High Priority (Phase 2.2 - ACTIVE)
- **Railway Deployment**: Deploy FastAPI backend to Railway for internet accessibility 🔄 **IN PROGRESS**
- **Complete Supabase Integration**: Implement frequency list loading from database 🔄 **STRUCTURE READY, INTEGRATION PENDING**
- **Enhance Error Handling**: Add robust fallback mechanisms and user feedback
- **Performance Optimization**: Reduce processing time from CLI execution

### Medium Priority (Phase 3)
- **Chrome Extension UI**: Add subtitle fusion controls to popup
- **User Account System**: Leverage Supabase authentication
- **Vocabulary Progress Tracking**: Store and adapt to user learning progress
- **Batch Processing**: Handle multiple episodes efficiently
- **Caching System**: Redis integration for repeated requests

### Low Priority (Future Enhancements)
- **Machine Learning Integration**: Adaptive vocabulary learning algorithms
- **Subtitle Quality Assessment**: Automatic quality scoring
- **Web Dashboard**: User-friendly web interface
- **Mobile Support**: React Native or PWA implementation

### Known Issues & Technical Debt
- **Python Dependency**: TypeScript algorithm requires Python for lemmatization ✅ **ACCEPTED FOR V0**
- **CLI Integration**: Subprocess execution adds complexity and latency ✅ **ACCEPTED FOR V0**
- **File Management**: Temporary file handling could be optimized ✅ **FUNCTIONAL FOR V0**
- **Error Recovery**: Limited fallback mechanisms for API failures 🔄 **IMPROVEMENT NEEDED**

### Development Phases
1. **Phase 1**: Database Setup ✅ **COMPLETED**
2. **Phase 2.1**: CLI Wrapper Implementation ✅ **COMPLETED**
3. **Phase 2.2**: Railway Deployment 🔄 **IN PROGRESS**
4. **Phase 3**: Chrome Extension Integration ✅ **READY FOR INTEGRATION**
5. **Phase 4**: Testing & Polish ✅ **READY FOR TESTING**

## 7. AI Coding Guidelines

### Code Organization & Structure

#### File Naming Conventions
- **TypeScript**: `camelCase.ts` for source files, `kebab-case.ts` for test files ✅ **IMPLEMENTED**
- **Python**: `snake_case.py` for all Python files ✅ **IMPLEMENTED**
- **Directories**: `kebab-case` for multi-word directories ✅ **IMPLEMENTED**
- **Constants**: `UPPER_SNAKE_CASE` for global constants ✅ **IMPLEMENTED**

#### Project Structure Standards
```
project-name/
├── src/                    # Source code ✅ **IMPLEMENTED**
├── dist/                   # Compiled output ✅ **IMPLEMENTED**
├── tests/                  # Test files 🔄 **BASIC IMPLEMENTATION**
├── docs/                   # Documentation ✅ **IMPLEMENTED**
├── scripts/                # Utility scripts ✅ **IMPLEMENTED**
├── package.json            # Node.js dependencies ✅ **IMPLEMENTED**
├── requirements.txt        # Python dependencies ✅ **IMPLEMENTED**
└── README.md              # Project documentation ✅ **IMPLEMENTED**
```

### Coding Style Rules

#### TypeScript/JavaScript ✅ **IMPLEMENTED**
- **Type Safety**: Always use TypeScript with strict mode ✅ **IMPLEMENTED**
- **Async/Await**: Prefer async/await over Promises ✅ **IMPLEMENTED**
- **Error Handling**: Use try-catch blocks with specific error types ✅ **IMPLEMENTED**
- **Documentation**: JSDoc comments for public functions ✅ **IMPLEMENTED**
- **Imports**: Use ES6 import/export syntax ✅ **IMPLEMENTED**

#### Python ✅ **IMPLEMENTED**
- **Type Hints**: Use type hints for all function parameters and returns ✅ **IMPLEMENTED**
- **Async Support**: Use async/await for FastAPI endpoints ✅ **IMPLEMENTED**
- **Error Handling**: Use specific exception types and proper error messages ✅ **IMPLEMENTED**
- **Documentation**: Docstrings for all functions and classes 🔄 **BASIC IMPLEMENTATION**
- **Formatting**: Follow PEP 8 style guidelines ✅ **IMPLEMENTED**

### Architectural Decisions

#### Separation of Concerns ✅ **IMPLEMENTED**
- **Chrome Extension**: Handle Netflix integration and user interface ✅ **COMPLETED**
- **API Backend**: Manage file processing and orchestration ✅ **COMPLETED**
- **Fusion Algorithm**: Focus on subtitle processing logic ✅ **COMPLETED**
- **Database**: Store configuration and user data 🔄 **STRUCTURE READY, INTEGRATION PENDING**

#### Data Flow Patterns ✅ **IMPLEMENTED**
- **Request/Response**: Use Pydantic models for API validation ✅ **IMPLEMENTED**
- **Message Passing**: Chrome extension uses message-based communication ✅ **IMPLEMENTED**
- **File Processing**: Temporary file approach for CLI integration ✅ **IMPLEMENTED**
- **Error Propagation**: Consistent error handling across all layers ✅ **IMPLEMENTED**

#### Performance Considerations 🔄 **PARTIALLY IMPLEMENTED**
- **Caching**: Implement caching for frequency lists and API responses 🔄 **BASIC IMPLEMENTATION**
- **Batch Processing**: Process multiple subtitles when possible ✅ **IMPLEMENTED**
- **Async Operations**: Use non-blocking operations for I/O ✅ **IMPLEMENTED**
- **Resource Management**: Proper cleanup of temporary files and connections ✅ **IMPLEMENTED**

### Documentation Standards

#### Code Documentation 🔄 **PARTIALLY IMPLEMENTED**
- **Function Headers**: Clear description of purpose, parameters, and returns 🔄 **BASIC IMPLEMENTATION**
- **Complex Logic**: Inline comments explaining algorithm steps ✅ **IMPLEMENTED**
- **API Endpoints**: Comprehensive endpoint documentation with examples ✅ **IMPLEMENTED**
- **Error Cases**: Document all possible error conditions and responses ✅ **IMPLEMENTED**

#### Project Documentation ✅ **IMPLEMENTED**
- **README Files**: Each subproject should have its own README ✅ **IMPLEMENTED**
- **API Documentation**: Use FastAPI's automatic documentation ✅ **IMPLEMENTED**
- **Architecture Diagrams**: Visual representation of system components ✅ **IMPLEMENTED**
- **Setup Instructions**: Step-by-step development environment setup ✅ **IMPLEMENTED**

### Testing & Quality Assurance

#### Testing Strategy 🔄 **BASIC IMPLEMENTATION**
- **Unit Tests**: Test individual functions and components 🔄 **BASIC IMPLEMENTATION**
- **Integration Tests**: Test interactions between modules 🔄 **BASIC IMPLEMENTATION**
- **End-to-End Tests**: Test complete workflows ✅ **READY FOR TESTING**
- **Performance Tests**: Validate processing time requirements ✅ **READY FOR TESTING**

#### Code Quality Tools ✅ **IMPLEMENTED**
- **TypeScript**: Use strict mode and ESLint for code quality ✅ **IMPLEMENTED**
- **Python**: Use mypy for type checking and flake8 for style 🔄 **BASIC IMPLEMENTATION**
- **Pre-commit Hooks**: Automated code quality checks 🔄 **NOT IMPLEMENTED**
- **Continuous Integration**: Automated testing on pull requests 🔄 **NOT IMPLEMENTED**

### Future Development Guidelines

#### When Adding New Features
1. **Update Documentation**: Modify relevant README and master documents ✅ **IMPLEMENTED**
2. **Add Tests**: Include unit and integration tests 🔄 **BASIC IMPLEMENTATION**
3. **Update Dependencies**: Add new packages to requirements/package.json ✅ **IMPLEMENTED**
4. **Error Handling**: Implement proper error handling and fallbacks ✅ **IMPLEMENTED**
5. **Performance Impact**: Consider performance implications and optimize ✅ **IMPLEMENTED**

#### When Modifying Existing Code
1. **Maintain Compatibility**: Ensure changes don't break existing functionality ✅ **IMPLEMENTED**
2. **Update Types**: Modify TypeScript interfaces and Python type hints ✅ **IMPLEMENTED**
3. **Test Thoroughly**: Run existing tests and add new ones if needed 🔄 **BASIC IMPLEMENTATION**
4. **Document Changes**: Update inline documentation and README files ✅ **IMPLEMENTED**

#### Integration Guidelines
1. **API Contracts**: Maintain consistent API interfaces across versions ✅ **IMPLEMENTED**
2. **Data Formats**: Use standardized formats (SRT, JSON) for data exchange ✅ **IMPLEMENTED**
3. **Error Handling**: Implement consistent error response formats ✅ **IMPLEMENTED**
4. **Configuration**: Use environment variables for configurable values ✅ **IMPLEMENTED**

---

**Last Updated**: January 2025  
**Version**: 2.1.0 (Phase 2.1 Complete, Phase 2.2 Pending)  
**Status**: FastAPI Backend Complete, Railway Deployment Pending, Chrome Extension Ready for Integration  
**Maintainer**: Smart Subtitles Development Team  
**License**: AGPL-3.0-or-later

**Next Milestone**: Complete Phase 2.2 (Railway Deployment) to enable Chrome Extension integration
