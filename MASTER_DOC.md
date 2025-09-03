# Smart Subtitles - Global Master Document

## 1. Project Overview

### Core Concept and Vision
Smart Subtitles is a comprehensive language learning platform that creates personalized Netflix viewing experiences through intelligent bilingual subtitle adaptation. The system automatically switches between target language (language being learned) and native language subtitles based on the user's vocabulary knowledge, making language learning seamless and engaging.

### Project Scope
This repository contains three interconnected subprojects that work together to deliver the complete Smart Subtitles experience:

1. **Chrome Extension** (`netflix-smart-subtitles-chrome-extension/`): Netflix integration for subtitle extraction and injection
2. **Subtitle Fusion Algorithm** (`subtitles-fusion-algorithm-public/`): Core TypeScript/Node.js engine for intelligent subtitle processing
3. **API Backend** (`smartsub-api/`): FastAPI server that orchestrates the fusion process and manages data

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
- **TypeScript**: v5.3.2 - Core development language
- **Webpack**: v5.89.0 - Build system
- **Chrome Extension APIs**: Manifest V3 compatible
- **Node.js**: v16+ - Development environment

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
- **TypeScript**: v5.0.0 - Core application logic
- **Node.js**: v16+ - Runtime environment
- **Python 3**: Lemmatization using `simplemma` library
- **DeepL API**: Translation service integration

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
- **Python**: v3.11+ - Backend runtime
- **FastAPI**: v0.104.1 - Web framework
- **Uvicorn**: v0.24.0 - ASGI server
- **Supabase**: v2.3.4 - Database and storage
- **Simplemma**: v0.9.1 - Lemmatization

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
Chrome Extension (Netflix) 
         ↓
    API Backend (FastAPI)
         ↓
Subtitle Fusion Algorithm (TypeScript/Node.js)
         ↓
    Supabase Database
```

### Directory Structure & Roles

#### Root Level
- **`MASTER_PLAN.md`**: Strategic development roadmap and phase planning
- **`MASTER_DOC.md`**: This comprehensive project documentation

#### Chrome Extension (`netflix-smart-subtitles-chrome-extension/`)
- **`my-netflix-extension-ts/`**: TypeScript version (primary)
  - **`src/`**: Source code with TypeScript
  - **`dist/`**: Compiled JavaScript output
  - **`manifest.json`**: Chrome extension configuration
- **`my-netflix-extension/`**: JavaScript version (legacy)
- **`reference/subadub/`**: Reference implementation based on Subadub

#### Subtitle Fusion Algorithm (`subtitles-fusion-algorithm-public/`)
- **`src/`**: Core TypeScript source code
- **`scripts/`**: Python lemmatization scripts
- **`frequency-lists/`**: Word frequency data for multiple languages
- **`dist/`**: Compiled JavaScript output
- **`tests/`**: Test files and validation

#### API Backend (`smartsub-api/`)
- **`main.py`**: FastAPI application entry point
- **`src/`**: Core Python modules
- **`venv/`**: Python virtual environment
- **`requirements.txt`**: Python dependencies

### Core Module Interactions

#### 1. Chrome Extension → API Backend
- **Extraction**: Chrome extension extracts Netflix subtitles using JSON hijacking
- **Upload**: Sends SRT files to `/fuse-subtitles` endpoint
- **Injection**: Receives processed subtitles and injects them back into Netflix

#### 2. API Backend → Fusion Algorithm
- **Orchestration**: FastAPI manages file uploads and CLI execution
- **CLI Wrapper**: Executes TypeScript fusion algorithm as subprocess
- **Response Handling**: Processes results and returns to extension

#### 3. Data Management
- **Supabase**: Stores frequency lists and user data
- **Frequency Lists**: Multi-language vocabulary data for algorithm decisions
- **User Progress**: Future implementation for personalized learning

## 4. Key Components & Files

### Chrome Extension Core Files
- **`content-script.ts`**: Message passing between popup and page script
- **`page-script.ts`**: JSON hijacking for Netflix subtitle extraction
- **`popup.ts`**: User interface and Chrome extension API communication
- **`types/netflix.d.ts`**: TypeScript definitions for Netflix data structures

### Subtitle Fusion Algorithm Core Files
- **`main.ts`**: CLI entry point with argument parsing
- **`logic.ts`**: Core subtitle processing algorithms (686 lines)
- **`deepl-api.ts`**: DeepL API integration with caching and rate limiting
- **`inline-translation.ts`**: Single-word translation service
- **`scripts/lemmatizer.py`**: Python lemmatization using simplemma

### API Backend Core Files
- **`main.py`**: FastAPI application with `/fuse-subtitles` endpoint
- **`src/supabase_client.py`**: Database connection and frequency list management
- **`src/fusion_algorithm.py`**: Python wrapper for fusion logic (placeholder)
- **`src/deepl_client.py`**: DeepL API client for Python backend

### Critical Algorithms & Functions

#### Subtitle Processing (`logic.ts`)
- **`fuseSubtitles()`**: Main fusion function with vocabulary-based decisions
- **`mergeOverlappingSubtitlesInSRT()`**: Temporal alignment algorithm
- **`hasIntersection()`**: Time overlap detection
- **`batchLemmatize()`**: Python subprocess for word stemming

#### Netflix Integration (`page-script.ts`)
- **JSON Hijacking**: Overrides `JSON.parse` to intercept Netflix API responses
- **WebVTT Processing**: Converts Netflix subtitle format to SRT
- **Immediate Injection**: Page script injection for reliable detection

#### API Orchestration (`main.py`)
- **File Management**: Temporary file creation and cleanup
- **CLI Execution**: Subprocess management with timeout handling
- **Error Handling**: Comprehensive error responses and fallbacks

## 5. Current Features

### ✅ Implemented Features

#### Chrome Extension
- **Automatic Subtitle Detection**: Detects available subtitle tracks on Netflix
- **Multiple Language Support**: Supports all Netflix subtitle languages
- **SRT Format Download**: Downloads subtitles in standard SRT format
- **Immediate Injection**: Uses Subadub's approach for reliable detection
- **TypeScript Architecture**: Modern development with type safety

#### Subtitle Fusion Algorithm
- **SRT Parsing & Generation**: Full SubRip format support
- **Vocabulary-based Selection**: Intelligent language switching based on word frequency
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions
- **Inline Translation**: Single-word translation using DeepL API
- **Proper Noun Detection**: Smart identification of names and places
- **Contraction Handling**: English contraction processing
- **Overlapping Subtitle Merging**: Temporal alignment of complex sequences
- **CLI Interface**: Comprehensive command-line tool
- **Multi-language Support**: 6 languages with lemmatization

#### API Backend
- **FastAPI Framework**: Modern Python web framework
- **File Upload Handling**: Multipart file processing
- **CLI Integration**: Subprocess execution of fusion algorithm
- **CORS Support**: Chrome extension compatibility
- **Error Handling**: Comprehensive error responses
- **Health Checks**: Service monitoring endpoints

### 🔄 Partially Implemented
- **Supabase Integration**: Basic structure, needs full implementation
- **User Authentication**: Framework ready, implementation pending
- **Performance Metrics**: Basic stats, needs enhancement
- **Error Recovery**: Basic fallbacks, needs robust handling

## 6. Pending Tasks & Roadmap

### High Priority (Phase 2)
- **Complete Supabase Integration**: Implement frequency list loading from database
- **Enhance Error Handling**: Add robust fallback mechanisms and user feedback
- **Performance Optimization**: Reduce processing time from CLI execution
- **Chrome Extension UI**: Add subtitle fusion controls to popup

### Medium Priority (Phase 3)
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
- **Python Dependency**: TypeScript algorithm requires Python for lemmatization
- **CLI Integration**: Subprocess execution adds complexity and latency
- **File Management**: Temporary file handling could be optimized
- **Error Recovery**: Limited fallback mechanisms for API failures

### Development Phases
1. **Phase 1**: Database Setup ✅ (COMPLETED)
2. **Phase 2**: CLI Wrapper Implementation (IN PROGRESS)
3. **Phase 3**: Chrome Extension Integration (PLANNED)
4. **Phase 4**: Testing & Polish (PLANNED)

## 7. AI Coding Guidelines

### Code Organization & Structure

#### File Naming Conventions
- **TypeScript**: `camelCase.ts` for source files, `kebab-case.ts` for test files
- **Python**: `snake_case.py` for all Python files
- **Directories**: `kebab-case` for multi-word directories
- **Constants**: `UPPER_SNAKE_CASE` for global constants

#### Project Structure Standards
```
project-name/
├── src/                    # Source code
├── dist/                   # Compiled output
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### Coding Style Rules

#### TypeScript/JavaScript
- **Type Safety**: Always use TypeScript with strict mode
- **Async/Await**: Prefer async/await over Promises
- **Error Handling**: Use try-catch blocks with specific error types
- **Documentation**: JSDoc comments for public functions
- **Imports**: Use ES6 import/export syntax

#### Python
- **Type Hints**: Use type hints for all function parameters and returns
- **Async Support**: Use async/await for FastAPI endpoints
- **Error Handling**: Use specific exception types and proper error messages
- **Documentation**: Docstrings for all functions and classes
- **Formatting**: Follow PEP 8 style guidelines

### Architectural Decisions

#### Separation of Concerns
- **Chrome Extension**: Handle Netflix integration and user interface
- **API Backend**: Manage file processing and orchestration
- **Fusion Algorithm**: Focus on subtitle processing logic
- **Database**: Store configuration and user data

#### Data Flow Patterns
- **Request/Response**: Use Pydantic models for API validation
- **Message Passing**: Chrome extension uses message-based communication
- **File Processing**: Temporary file approach for CLI integration
- **Error Propagation**: Consistent error handling across all layers

#### Performance Considerations
- **Caching**: Implement caching for frequency lists and API responses
- **Batch Processing**: Process multiple subtitles when possible
- **Async Operations**: Use non-blocking operations for I/O
- **Resource Management**: Proper cleanup of temporary files and connections

### Documentation Standards

#### Code Documentation
- **Function Headers**: Clear description of purpose, parameters, and returns
- **Complex Logic**: Inline comments explaining algorithm steps
- **API Endpoints**: Comprehensive endpoint documentation with examples
- **Error Cases**: Document all possible error conditions and responses

#### Project Documentation
- **README Files**: Each subproject should have its own README
- **API Documentation**: Use FastAPI's automatic documentation
- **Architecture Diagrams**: Visual representation of system components
- **Setup Instructions**: Step-by-step development environment setup

### Testing & Quality Assurance

#### Testing Strategy
- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test interactions between modules
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Validate processing time requirements

#### Code Quality Tools
- **TypeScript**: Use strict mode and ESLint for code quality
- **Python**: Use mypy for type checking and flake8 for style
- **Pre-commit Hooks**: Automated code quality checks
- **Continuous Integration**: Automated testing on pull requests

### Future Development Guidelines

#### When Adding New Features
1. **Update Documentation**: Modify relevant README and master documents
2. **Add Tests**: Include unit and integration tests
3. **Update Dependencies**: Add new packages to requirements/package.json
4. **Error Handling**: Implement proper error handling and fallbacks
5. **Performance Impact**: Consider performance implications and optimize

#### When Modifying Existing Code
1. **Maintain Compatibility**: Ensure changes don't break existing functionality
2. **Update Types**: Modify TypeScript interfaces and Python type hints
3. **Test Thoroughly**: Run existing tests and add new ones if needed
4. **Document Changes**: Update inline documentation and README files

#### Integration Guidelines
1. **API Contracts**: Maintain consistent API interfaces across versions
2. **Data Formats**: Use standardized formats (SRT, JSON) for data exchange
3. **Error Handling**: Implement consistent error response formats
4. **Configuration**: Use environment variables for configurable values

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintainer**: Smart Subtitles Development Team  
**License**: AGPL-3.0-or-later
