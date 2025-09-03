# Smart Subtitles - Master Document

## 1. Project Overview

### Core Concept and Vision
Smart Subtitles is an adaptive bilingual subtitle system that creates personalized learning experiences by intelligently switching between target language (language being learned) and native language subtitles based on the user's vocabulary knowledge. The system uses frequency lists to determine which words the user "knows" and makes real-time decisions about subtitle language selection.

### Target Users and Use Cases
- **Language learners** at intermediate to advanced levels
- **Self-directed learners** who want personalized content
- **Educators** creating adaptive learning materials
- **Content creators** producing bilingual educational content

### Key Value Proposition
- **Adaptive Learning**: Automatically adjusts difficulty based on vocabulary knowledge
- **Seamless Experience**: No manual switching between subtitle languages
- **Vocabulary Building**: Inline translation for single unknown words
- **Time Synchronization**: Advanced algorithm for perfect subtitle timing alignment
- **Multi-language Support**: Works with English, French, Portuguese, Spanish, German, and Italian

## 2. Technical Architecture

### Technology Stack
- **TypeScript**: Core application logic and type safety
- **Node.js**: Runtime environment for CLI application
- **Python 3**: Lemmatization using `simplemma` library
- **DeepL API**: High-quality translation service for inline translations
- **SRT Format**: Standard subtitle format for input/output

### Data Flow and Processing Pipeline

```
Input Files → Parse SRT → Merge Overlapping → Vocabulary Analysis → Decision Engine → Output SRT
     ↓              ↓              ↓                ↓                ↓              ↓
  Target SRT    Subtitle     Temporal        Word Frequency    Language      Hybrid SRT
  Native SRT    Objects      Alignment       Lemmatization    Selection     + Statistics
  Frequency     (Index,      (Combine        (Stem words      (Target vs    (Performance
  List          Time,        overlapping     for accurate     Native)       metrics)
                Text)        subtitles)      matching)
```

### Key Algorithms

#### Bidirectional Time Synchronization
The system implements a sophisticated algorithm for aligning subtitles between different language versions:

1. **Temporal Intersection Detection**: Uses `hasIntersection()` function to find overlapping subtitle segments
2. **Overlapping Subtitle Merging**: Combines multiple overlapping subtitles into single segments
3. **Time Range Mapping**: Maps subtitle timing between target and native language versions
4. **Fallback Handling**: Graceful degradation when perfect alignment isn't possible

#### Vocabulary Analysis Engine
- **Lemmatization**: Uses Python `simplemma` for accurate word stemming
- **Proper Noun Detection**: Intelligent identification of names, places, brands
- **Contraction Handling**: Special processing for English contractions (e.g., "don't" → "do", "not")
- **Frequency-based Knowledge**: Assumes user knows top N most frequent words

#### Decision Engine Logic
```
For each target subtitle:
1. Extract and lemmatize words
2. Check against known vocabulary set
3. If all words known → Show target language
4. If multiple unknown words → Show native language
5. If single unknown word → Apply inline translation (if enabled)
6. Fallback to native language if translation fails
```

### File Structure and Important Modules

```
prototype/
├── src/
│   ├── main.ts              # CLI entry point and argument parsing
│   ├── logic.ts             # Core subtitle processing algorithms
│   ├── deepl-api.ts         # DeepL API integration with caching
│   ├── inline-translation.ts # Inline translation service
│   └── logic.ts.backup      # Backup of previous logic implementation
├── scripts/
│   └── lemmatizer.py        # Python lemmatization script
├── frequency-lists/         # Word frequency data for multiple languages
├── tests/
│   └── test-deepl.ts        # DeepL API integration tests
├── dist/                    # Compiled JavaScript output
└── *.srt                    # Sample subtitle files
```

## 3. Current Implementation Status

### ✅ Completed Features
- **Core Subtitle Processing**: SRT parsing, generation, and manipulation
- **Vocabulary-based Selection**: Intelligent language switching based on word frequency
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions
- **Inline Translation**: Single-word translation using DeepL API
- **Proper Noun Detection**: Smart identification of names and places
- **Contraction Handling**: English contraction processing
- **Overlapping Subtitle Merging**: Temporal alignment of complex subtitle sequences
- **CLI Interface**: Command-line tool with comprehensive argument parsing
- **Performance Statistics**: Detailed metrics and reporting
- **Multi-language Support**: English, French, Portuguese, Spanish, German, Italian

### 🔄 In Progress Components
- **Error Handling**: Robust error recovery and fallback mechanisms
- **Performance Optimization**: Caching and rate limiting for API calls
- **Testing Suite**: Comprehensive test coverage for all modules

### ⏳ Planned/TODO Items
- **Chrome Extension**: Netflix integration for real-time subtitle processing
- **Web Interface**: User-friendly web application
- **Advanced Vocabulary Tracking**: User progress monitoring
- **Machine Learning Integration**: Adaptive vocabulary learning
- **Batch Processing**: Handle multiple video files
- **Subtitle Quality Assessment**: Automatic quality scoring

### Status of Each Major Module

| Module | Status | Completion | Notes |
|--------|--------|------------|-------|
| `main.ts` | ✅ Complete | 100% | CLI interface and argument parsing |
| `logic.ts` | ✅ Complete | 100% | Core subtitle processing algorithms |
| `deepl-api.ts` | ✅ Complete | 100% | DeepL integration with caching |
| `inline-translation.ts` | ✅ Complete | 100% | Inline translation service |
| `lemmatizer.py` | ✅ Complete | 100% | Python lemmatization script |
| Test Suite | 🔄 Partial | 30% | Basic DeepL API tests only |

## 4. Technical Decisions & Rationale

### Why Specific Libraries Were Chosen

#### TypeScript
- **Type Safety**: Prevents runtime errors and improves code quality
- **Developer Experience**: Better IDE support and refactoring capabilities
- **Future-proofing**: Easier to maintain and extend as project grows

#### Python for Lemmatization
- **simplemma Library**: Superior lemmatization quality compared to JavaScript alternatives
- **Language Support**: Excellent support for multiple languages
- **Accuracy**: More accurate word stemming for vocabulary analysis

#### DeepL API
- **Translation Quality**: Superior to Google Translate for educational content
- **Context Support**: Can provide context for better translation accuracy
- **Rate Limiting**: Built-in support for API rate limiting
- **Caching**: Efficient caching mechanism to reduce API calls

### Architecture Decisions Made

#### Hybrid TypeScript/Python Approach
- **Separation of Concerns**: TypeScript for business logic, Python for specialized NLP
- **Performance**: Python subprocess calls only when needed for lemmatization
- **Maintainability**: Each language handles what it does best

#### CLI-First Design
- **Simplicity**: Easy to integrate with existing workflows
- **Automation**: Can be scripted and automated
- **Foundation**: Provides solid base for future web/extension development

#### Caching Strategy
- **Translation Caching**: 24-hour cache for DeepL translations
- **Memory Efficiency**: Prevents redundant API calls
- **Cost Optimization**: Reduces API usage costs

### Trade-offs Considered

#### Performance vs. Accuracy
- **Lemmatization**: Chose accuracy (Python) over performance (pure JavaScript)
- **Translation**: Caching balances cost vs. real-time translation needs
- **Processing**: Batch processing vs. real-time streaming

#### Complexity vs. Functionality
- **Proper Noun Detection**: Complex logic for better accuracy
- **Contraction Handling**: Extensive mapping for English contractions
- **Time Synchronization**: Sophisticated algorithm for perfect alignment

### Performance Considerations

#### Memory Usage
- **Frequency Lists**: Loaded once and kept in memory for fast access
- **Translation Cache**: Limited size with timestamp-based expiration
- **Subtitle Objects**: Efficient data structures for large subtitle files

#### Processing Speed
- **Batch Lemmatization**: Processes multiple lines at once
- **Parallel Processing**: Potential for future optimization
- **Early Exit**: Stops processing when decision is made

## 5. Key Challenges & Solutions

### Subtitle Synchronization Problems

#### Challenge: Temporal Misalignment
**Problem**: Different language subtitle files often have different timing and segmentation.

**Solution**: 
- Implemented `mergeOverlappingSubtitles()` function
- Created `hasIntersection()` for temporal overlap detection
- Added fallback mechanisms for imperfect alignment

#### Challenge: Subtitle Segmentation Differences
**Problem**: Target and native language subtitles may split content differently.

**Solution**:
- Combines multiple overlapping native subtitles
- Maintains chronological order in merged content
- Preserves original timing boundaries

### Technical Hurdles Encountered

#### Challenge: Proper Noun Detection
**Problem**: Distinguishing between proper nouns and regular capitalized words.

**Solution**:
- Implemented context-aware proper noun detection
- Uses frequency list to determine if capitalized word is common
- Handles sentence-initial capitalization correctly

#### Challenge: English Contraction Processing
**Problem**: Contractions like "don't" need special handling for vocabulary analysis.

**Solution**:
- Created comprehensive `ENGLISH_CONTRACTIONS` mapping
- Expands contractions before vocabulary checking
- Maintains original text for display purposes

#### Challenge: API Rate Limiting
**Problem**: DeepL API has rate limits that could cause failures.

**Solution**:
- Implemented configurable rate limiting delays
- Added retry logic with exponential backoff
- Created efficient caching to minimize API calls

### Solutions Implemented or Attempted

#### Successful Solutions
- **Bidirectional Synchronization**: Advanced algorithm for perfect timing alignment
- **Inline Translation**: Seamless single-word translation integration
- **Caching System**: Efficient translation caching with expiration
- **Error Recovery**: Graceful fallback when translations fail

#### Attempted Solutions
- **Pure JavaScript Lemmatization**: Rejected due to inferior accuracy
- **Simple Time Matching**: Replaced with sophisticated overlap detection
- **Basic Vocabulary Checking**: Enhanced with proper noun detection

### Known Limitations

#### Current Limitations
- **Language Support**: Limited to languages supported by simplemma and DeepL
- **Subtitle Format**: Only supports SRT format (could extend to others)
- **Vocabulary Model**: Assumes frequency-based knowledge (could be personalized)
- **Real-time Processing**: CLI-based, not real-time streaming

#### Technical Constraints
- **API Dependencies**: Requires DeepL API key for inline translation
- **Python Dependency**: Requires Python 3 and simplemma for lemmatization
- **Memory Usage**: Frequency lists loaded entirely into memory
- **Processing Speed**: Sequential processing (could be parallelized)

## 6. Development Setup

### Dependencies and Installation

#### Prerequisites
```bash
# Node.js (v16 or higher)
node --version

# Python 3 (for lemmatization)
python3 --version

# TypeScript compiler
npm install -g typescript
```

#### Project Setup
```bash
# Clone repository
git clone <repository-url>
cd prototype

# Install Node.js dependencies
npm install

# Install Python dependencies
pip3 install simplemma

# Build TypeScript
npm run build
```

#### Required Files
- **Frequency Lists**: Place in `frequency-lists/` directory
- **SRT Files**: Target and native language subtitle files
- **DeepL API Key**: For inline translation feature (optional)

### How to Run/Test the Project

#### Basic Usage
```bash
# Build the project
npm run build

# Run with basic parameters
node dist/main.js --target fr.srt --native en.srt --freq frequency-lists/fr-5000.txt --out hybrid.srt --topN 2000 --lang fr --native-lang en

# Run with inline translation
node dist/main.js --target fr.srt --native en.srt --freq frequency-lists/fr-5000.txt --out hybrid.srt --topN 2000 --lang fr --native-lang en --inline-translation
```

#### Testing
```bash
# Run DeepL API tests
npm test

# Test specific components
node tests/test-deepl.js
```

### Development Workflow

#### Code Structure
- **TypeScript Source**: All logic in `src/` directory
- **Python Scripts**: Lemmatization in `scripts/` directory
- **Compiled Output**: JavaScript in `dist/` directory
- **Tests**: Test files in `tests/` directory

#### Development Process
1. **Edit TypeScript**: Modify files in `src/`
2. **Build**: Run `npm run build` to compile
3. **Test**: Run `npm test` for basic testing
4. **Manual Testing**: Test with real SRT files
5. **Iterate**: Refine based on results

#### Debugging
- **Console Logging**: Extensive logging in main processing loop
- **Error Handling**: Graceful error recovery with fallbacks
- **Statistics**: Detailed performance metrics output

## 7. Future Roadmap

### Chrome Extension Development Plans

#### Phase 1: Foundation (Q1 2024)
- **Browser Integration**: Chrome extension manifest and basic structure
- **SRT Processing**: Port core subtitle processing to extension
- **UI Components**: Basic popup interface for configuration

#### Phase 2: Netflix Integration (Q2 2024)
- **Content Script**: Inject into Netflix pages
- **Subtitle Extraction**: Real-time subtitle capture
- **Dynamic Processing**: Process subtitles as they appear
- **User Interface**: Overlay controls for language switching

#### Phase 3: Advanced Features (Q3 2024)
- **Vocabulary Tracking**: User progress monitoring
- **Personalization**: Adaptive learning based on user performance
- **Offline Support**: Cached translations and processing
- **Analytics**: Learning progress and statistics

### TypeScript Migration from Python Prototype

#### Current State
- **Hybrid Approach**: TypeScript main logic, Python for lemmatization
- **Subprocess Calls**: Python script called via Node.js child_process

#### Migration Goals
- **Pure TypeScript**: Eliminate Python dependency
- **Performance**: Native JavaScript lemmatization
- **Deployment**: Easier deployment without Python requirements
- **Maintenance**: Single language codebase

#### Migration Strategy
1. **Research**: Find high-quality JavaScript lemmatization libraries
2. **Prototype**: Test accuracy and performance
3. **Gradual Migration**: Replace Python calls one by one
4. **Validation**: Ensure accuracy matches current implementation

### Features to Implement

#### Short-term (Next 3 months)
- **Web Interface**: User-friendly web application
- **Batch Processing**: Handle multiple video files
- **Advanced Error Handling**: Better error recovery and reporting
- **Performance Optimization**: Parallel processing and caching improvements

#### Medium-term (3-6 months)
- **Machine Learning Integration**: Adaptive vocabulary learning
- **Subtitle Quality Assessment**: Automatic quality scoring
- **Multi-format Support**: VTT, ASS, and other subtitle formats
- **Cloud Processing**: Server-side processing for large files

#### Long-term (6+ months)
- **Mobile App**: iOS and Android applications
- **Social Features**: Share learning progress and recommendations
- **Content Marketplace**: Curated educational content
- **Advanced Analytics**: Detailed learning insights and recommendations

### Technical Debt and Improvements

#### Code Quality
- **Test Coverage**: Comprehensive unit and integration tests
- **Documentation**: API documentation and code comments
- **Type Safety**: Stricter TypeScript configuration
- **Error Handling**: More robust error recovery

#### Performance
- **Parallel Processing**: Multi-threaded subtitle processing
- **Memory Optimization**: Streaming processing for large files
- **Caching Strategy**: More sophisticated caching mechanisms
- **API Optimization**: Batch API calls and better rate limiting

#### User Experience
- **Configuration**: User-friendly configuration management
- **Progress Tracking**: Real-time processing progress
- **Error Reporting**: Better error messages and suggestions
- **Accessibility**: Screen reader support and keyboard navigation

---

*This master document provides a comprehensive overview of the Smart Subtitles project and serves as the primary reference for development decisions, architecture understanding, and future planning. It should be updated as the project evolves and new features are implemented.*
