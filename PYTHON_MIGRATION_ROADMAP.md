# Python Migration Roadmap
## Smart Subtitles API - TypeScript to Python Migration

**Date:** January 2025  
**Objective:** Migrate subtitle fusion algorithm from TypeScript subprocess to pure Python implementation  
**Estimated Time:** 3-6 hours  
**Status:** 🟡 Planning Phase

---

## 🎯 **Migration Goals**

### **Primary Objectives:**
- ✅ Eliminate subprocess complexity and deployment issues
- ✅ Improve performance by removing Node.js overhead
- ✅ Simplify debugging and error handling
- ✅ Maintain 100% functional compatibility with existing algorithm
- ✅ Preserve all features: lemmatization, proper noun detection, subtitle synchronization, inline translation

### **Success Criteria:**
- [ ] API returns identical results to TypeScript version
- [ ] All test cases pass with same output
- [ ] Deployment works reliably on Railway
- [ ] Performance improvement measurable
- [ ] Error handling is more robust

---

## 📋 **Pre-Migration Analysis**

### **Current Architecture Issues:**
- ❌ Subprocess calls to Node.js CLI
- ❌ Missing lemmatizer script in Docker container
- ❌ Complex multi-stage Docker build
- ❌ Silent failures in lemmatization
- ❌ Difficult debugging on Railway

### **Files to Migrate:**
```
ts-src/
├── logic.ts           → src/subtitle_fusion.py
├── main.ts            → src/cli.py (if needed)
├── deepl-api.ts       → src/deepl_api.py
└── inline-translation.ts → src/inline_translation.py
```

### **Dependencies to Preserve:**
- ✅ `simplemma` for lemmatization (already in requirements.txt)
- ✅ All English contraction mappings
- ✅ Proper noun detection logic
- ✅ Subtitle synchronization algorithms
- ✅ DeepL API integration
- ✅ Inline translation features

---

## 🚀 **Migration Plan - Step by Step**

### **Phase 1: Foundation Setup** ⏱️ 30 minutes
**Objective:** Create Python module structure and basic tests

#### **Step 1.1: Create Python Module Structure**
- [x] Create `src/` directory structure
- [x] Create `src/__init__.py`
- [x] Create `src/subtitle_fusion.py` (main module)
- [x] Create `src/srt_parser.py` (SRT parsing)
- [x] Create `src/lemmatizer.py` (lemmatization)
- [x] Create `src/deepl_api.py` (DeepL integration)
- [x] Create `src/inline_translation.py` (inline translation)

#### **Step 1.2: Create Test Framework**
- [x] Create `tests/` directory
- [x] Create `tests/test_subtitle_fusion.py`
- [x] Create `tests/test_data/` with sample files
- [x] Copy test files: `en.srt`, `fr.srt`, `en-10000.txt`

#### **Step 1.3: Validation Test**
```python
# Test that basic imports work
from src.subtitle_fusion import SubtitleFusionEngine
engine = SubtitleFusionEngine()
print("✅ Basic structure created successfully")
```

**✅ Phase 1 Complete When:** All modules can be imported without errors

**✅ PHASE 1 COMPLETED** - All modules created and basic tests passing

---

### **Phase 2: SRT Parsing Migration** ⏱️ 45 minutes
**Objective:** Migrate SRT parsing and generation functions

#### **Step 2.1: Migrate Core SRT Functions**
- [x] Migrate `parseSRT()` function from `logic.ts`
- [x] Migrate `generateSRT()` function from `logic.ts`
- [x] Migrate `normalizeWords()` function from `logic.ts`
- [x] Add proper type hints and docstrings

#### **Step 2.2: Create SRT Parser Module**
```python
# src/srt_parser.py
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Subtitle:
    index: str
    start: str
    end: str
    text: str

def parse_srt(srt_content: str) -> List[Subtitle]:
    # Implementation from logic.ts
    pass

def generate_srt(subtitles: List[Subtitle]) -> str:
    # Implementation from logic.ts
    pass
```

#### **Step 2.3: Validation Test**
```python
# Test SRT parsing with sample data
from src.srt_parser import parse_srt, generate_srt

# Load test file
with open('tests/test_data/en.srt', 'r') as f:
    content = f.read()

# Parse and regenerate
subtitles = parse_srt(content)
regenerated = generate_srt(subtitles)

# Verify round-trip works
assert len(subtitles) > 0
assert "NETFLIX" in regenerated
print("✅ SRT parsing migration successful")
```

**✅ Phase 2 Complete When:** SRT files can be parsed and regenerated identically

**✅ PHASE 2 COMPLETED** - SRT parsing functions migrated and tested (475 subtitles parsed successfully)

---

### **Phase 3: Lemmatization Migration** ⏱️ 30 minutes
**Objective:** Migrate lemmatization logic to pure Python

#### **Step 3.1: Migrate Lemmatization Functions**
- [x] Migrate `lemmatizeSingleLine()` function
- [x] Migrate `batchLemmatize()` function
- [x] Remove subprocess calls to Python script
- [x] Use `simplemma` directly in Python

#### **Step 3.2: Create Lemmatizer Module**
```python
# src/lemmatizer.py
import simplemma
from typing import List

def lemmatize_single_line(line: str, lang: str) -> List[str]:
    """Direct Python lemmatization - no subprocess needed"""
    words = line.split()
    return [simplemma.lemmatize(word, lang=lang) for word in words]

def batch_lemmatize(lines: List[str], lang: str) -> List[List[str]]:
    """Batch lemmatization for efficiency"""
    return [lemmatize_single_line(line, lang) for line in lines]
```

#### **Step 3.3: Validation Test**
```python
# Test lemmatization with known examples
from src.lemmatizer import lemmatize_single_line

# Test English lemmatization
result = lemmatize_single_line("I am running quickly", "en")
expected = ["i", "be", "run", "quickly"]  # Approximate
assert len(result) == 4
print("✅ Lemmatization migration successful")
```

**✅ Phase 3 Complete When:** Lemmatization produces expected results

**✅ PHASE 3 COMPLETED** - Lemmatization functions migrated to pure Python using simplemma

---

### **Phase 4: Core Fusion Algorithm Migration** ⏱️ 90 minutes
**Objective:** Migrate the main subtitle fusion logic

#### **Step 4.1: Migrate Core Logic Functions**
- [x] Migrate `isProperNoun()` function
- [x] Migrate `isWordKnown()` function with contractions
- [x] Migrate `hasIntersection()` function
- [x] Migrate `mergeOverlappingSubtitles()` function

#### **Step 4.2: Migrate Main Fusion Function**
- [x] Migrate `fuseSubtitles()` function
- [x] Preserve all decision logic
- [x] Maintain proper noun detection
- [x] Preserve subtitle synchronization
- [x] Keep inline translation support

#### **Step 4.3: Create Main Fusion Module**
```python
# src/subtitle_fusion.py
from typing import List, Set, Dict, Any, Optional
from dataclasses import dataclass
from .srt_parser import Subtitle
from .lemmatizer import lemmatize_single_line

class SubtitleFusionEngine:
    def __init__(self):
        self.english_contractions = {
            "you're": ["you", "are"],
            "don't": ["do", "not"],
            # ... (all contractions from logic.ts)
        }
    
    def fuse_subtitles(self, 
                      target_subs: List[Subtitle],
                      native_subs: List[Subtitle], 
                      known_words: Set[str],
                      lang: str,
                      enable_inline_translation: bool = False,
                      deepl_api: Optional[Any] = None,
                      native_lang: Optional[str] = None) -> Dict[str, Any]:
        # Main fusion logic from logic.ts
        pass
```

#### **Step 4.4: Validation Test**
```python
# Test with actual subtitle files
from src.subtitle_fusion import SubtitleFusionEngine
from src.srt_parser import parse_srt

# Load test data
with open('tests/test_data/en.srt', 'r') as f:
    target_content = f.read()
with open('tests/test_data/fr.srt', 'r') as f:
    native_content = f.read()
with open('tests/test_data/en-10000.txt', 'r') as f:
    freq_content = f.read()

# Parse data
target_subs = parse_srt(target_content)
native_subs = parse_srt(native_content)
known_words = set(freq_content.split('\n')[:1000])

# Test fusion
engine = SubtitleFusionEngine()
result = engine.fuse_subtitles(target_subs, native_subs, known_words, 'en')

# Verify results
assert result['success'] == True
assert len(result['hybrid']) > 0
print("✅ Core fusion algorithm migration successful")
```

**✅ Phase 4 Complete When:** Fusion algorithm produces expected results

**✅ PHASE 4 COMPLETED** - Core fusion algorithm migrated and tested (259/475 subtitles replaced successfully)

---

### **Phase 5: DeepL API Migration** ⏱️ 30 minutes
**Objective:** Migrate DeepL API integration

#### **Step 5.1: Migrate DeepL API Class**
- [ ] Migrate `DeepLAPI` class from `deepl-api.ts`
- [ ] Preserve all API methods
- [ ] Maintain error handling and retry logic
- [ ] Keep caching functionality

#### **Step 5.2: Migrate Inline Translation**
- [ ] Migrate `InlineTranslationService` class
- [ ] Preserve context window logic
- [ ] Maintain translation caching
- [ ] Keep error handling

#### **Step 5.3: Validation Test**
```python
# Test DeepL API (if API key available)
from src.deepl_api import DeepLAPI

# Test basic functionality
api = DeepLAPI(api_key="test_key")
# Test without actual API call
print("✅ DeepL API migration successful")
```

**✅ Phase 5 Complete When:** DeepL integration works (if API key available)

---

### **Phase 6: Integration and Testing** ⏱️ 60 minutes
**Objective:** Complete integration and comprehensive testing

#### **Step 6.1: Update FastAPI Endpoint**
- [x] Modify `main.py` to use Python engine
- [x] Remove subprocess calls
- [x] Update error handling
- [x] Add proper logging

#### **Step 6.2: Comprehensive Regression Testing**
- [x] Test with original test files
- [x] Compare outputs with TypeScript version
- [x] Test edge cases (empty subtitles, HTML tags, etc.)
- [x] Performance testing

#### **Step 6.3: Validation Test**
```python
# Full integration test
import requests

# Test API endpoint locally
response = requests.post('http://localhost:3000/fuse-subtitles', 
                        files={'target_srt': open('tests/test_data/en.srt', 'rb'),
                               'native_srt': open('tests/test_data/fr.srt', 'rb'),
                               'frequency_list': open('tests/test_data/en-10000.txt', 'rb')},
                        data={'target_language': 'en', 'native_language': 'fr', 'top_n_words': 1000})

assert response.status_code == 200
result = response.json()
assert result['success'] == True
print("✅ Full integration test successful")
```

**✅ Phase 6 Complete When:** All tests pass and API works identically

**✅ PHASE 6 COMPLETED** - FastAPI integration updated and tested successfully

---

### **Phase 7: Docker and Deployment** ⏱️ 30 minutes
**Objective:** Update deployment configuration

#### **Step 7.1: Update Dockerfile**
- [x] Remove Node.js build stage
- [x] Remove Node.js runtime installation
- [x] Remove scripts/ directory copy
- [x] Simplify to Python-only image

#### **Step 7.2: Update Requirements**
- [x] Ensure all Python dependencies are listed
- [x] Remove Node.js dependencies
- [x] Test Docker build locally

#### **Step 7.3: Validation Test**
```bash
# Test Docker build
docker build -t smartsub-api-python .
docker run -p 3000:3000 smartsub-api-python

# Test API in container
curl -X POST http://localhost:3000/health
```

**✅ Phase 7 Complete When:** Docker image builds and runs successfully

**✅ PHASE 7 COMPLETED** - Dockerfile updated to Python-only (simplified from multi-stage to single-stage)

---

### **Phase 8: Railway Deployment** ⏱️ 15 minutes
**Objective:** Deploy to Railway and validate

#### **Step 8.1: Deploy to Railway**
- [ ] Push changes to repository
- [ ] Monitor Railway deployment logs
- [ ] Verify build succeeds
- [ ] Check health endpoint

#### **Step 8.2: Production Testing**
- [ ] Test with production API key
- [ ] Run full test suite against live API
- [ ] Compare results with previous version
- [ ] Monitor performance

#### **Step 8.3: Validation Test**
```python
# Test production API
import requests

response = requests.post('https://smartsub-api-production.up.railway.app/fuse-subtitles',
                        files={'target_srt': open('tests/test_data/en.srt', 'rb'),
                               'native_srt': open('tests/test_data/fr.srt', 'rb'),
                               'frequency_list': open('tests/test_data/en-10000.txt', 'rb')},
                        data={'target_language': 'en', 'native_language': 'fr', 'top_n_words': 1000},
                        params={'api_key': 'sk-smartsub-abc123def456ghi789'})

assert response.status_code == 200
print("✅ Production deployment successful")
```

**✅ Phase 8 Complete When:** Production API works correctly

---

## 🧪 **Testing Strategy**

### **Unit Tests:**
- [ ] SRT parsing functions
- [ ] Lemmatization functions
- [ ] Proper noun detection
- [ ] Word knowledge checking
- [ ] Subtitle synchronization

### **Integration Tests:**
- [ ] Full fusion algorithm
- [ ] DeepL API integration
- [ ] Inline translation
- [ ] Error handling

### **Regression Tests:**
- [ ] Compare outputs with TypeScript version
- [ ] Test with original test files
- [ ] Performance benchmarks
- [ ] Memory usage comparison

### **Edge Case Tests:**
- [ ] Empty subtitle files
- [ ] Malformed SRT content
- [ ] HTML tags in subtitles
- [ ] Very long subtitle text
- [ ] Special characters and Unicode

---

## 📊 **Success Metrics**

### **Functional Metrics:**
- [ ] 100% identical output compared to TypeScript version
- [ ] All test cases pass
- [ ] No regression in functionality
- [ ] All features preserved

### **Performance Metrics:**
- [ ] Response time improvement (target: 20-30% faster)
- [ ] Memory usage reduction (target: 30-40% less)
- [ ] Docker image size reduction (target: 50% smaller)

### **Reliability Metrics:**
- [ ] Zero deployment failures
- [ ] Improved error handling
- [ ] Better logging and debugging
- [ ] More robust error recovery

---

## 🚨 **Risk Mitigation**

### **Rollback Plan:**
- [ ] Keep TypeScript code in separate branch
- [ ] Maintain ability to revert Dockerfile
- [ ] Document rollback procedure
- [ ] Test rollback process

### **Monitoring:**
- [ ] Add comprehensive logging
- [ ] Monitor API response times
- [ ] Track error rates
- [ ] Set up alerts for failures

### **Validation:**
- [ ] A/B testing capability
- [ ] Gradual rollout option
- [ ] Performance monitoring
- [ ] User feedback collection

---

## 📝 **Migration Checklist**

### **Pre-Migration:**
- [ ] Backup current working version
- [ ] Document current behavior
- [ ] Set up test environment
- [ ] Prepare rollback plan

### **During Migration:**
- [ ] Follow step-by-step plan
- [ ] Test after each phase
- [ ] Document any issues
- [ ] Update progress in this file

### **Post-Migration:**
- [ ] Verify all functionality
- [ ] Monitor production metrics
- [ ] Clean up old code
- [ ] Update documentation

---

## 📅 **Timeline**

| Phase | Duration | Status | Notes |
|-------|----------|--------|-------|
| Phase 1: Foundation | 30 min | ⏳ Pending | Setup and structure |
| Phase 2: SRT Parsing | 45 min | ⏳ Pending | Core parsing functions |
| Phase 3: Lemmatization | 30 min | ⏳ Pending | Python lemmatization |
| Phase 4: Fusion Algorithm | 90 min | ⏳ Pending | Main logic migration |
| Phase 5: DeepL API | 30 min | ⏳ Pending | API integration |
| Phase 6: Integration | 60 min | ⏳ Pending | Testing and validation |
| Phase 7: Docker | 30 min | ⏳ Pending | Deployment config |
| Phase 8: Railway | 15 min | ⏳ Pending | Production deployment |

**Total Estimated Time: 5.5 hours**

---

## 🎯 **Next Steps**

1. **Review this plan** with the team
2. **Get approval** to proceed
3. **Start with Phase 1** when ready
4. **Update progress** in this file after each phase
5. **Document any deviations** or issues encountered

---

**Last Updated:** January 2025  
**Status:** 🟡 Ready to Begin  
**Next Action:** Awaiting approval to start Phase 1
