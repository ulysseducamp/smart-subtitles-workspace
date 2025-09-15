# Security Audit Plan - Smart Subtitles

## 🎯 Overview

This document outlines the security vulnerabilities found in the Smart Subtitles project and the remediation plan to address them. The audit was conducted focusing on 4 critical areas: Secrets Management, API Key Exposure, Input Validation, and Transport Security.

## 📊 Status Overview

| Priority | Issue | Status | Risk Level |
|----------|-------|--------|------------|
| 1.1 | Hardcoded API Key in Test File | ✅ **COMPLETED** | Critical |
| 2.1 | Client-Side API Key Storage (Chrome Extension) | ✅ **COMPLETED** | Critical |
| 2.2 | API Key in URL Parameters | ✅ **COMPLETED** | Critical |
| 2.3 | DeepL API Key Exposure Risk | ✅ **RESOLVED** | High |
| 3.1 | No File Size Limits | ❌ **PENDING** | High |
| 3.2 | Insufficient Input Sanitization | ❌ **PENDING** | High |
| 3.3 | No Rate Limiting | ❌ **PENDING** | High |
| 3.4 | Weak Timestamp Validation | ❌ **PENDING** | Medium |
| 4.1 | Overly Permissive CORS | ❌ **PENDING** | Medium |
| 4.2 | HTTP Health Check in Docker | ❌ **PENDING** | Low |
| 4.3 | No Content Security Policy | ❌ **PENDING** | Low |

## 🔍 Detailed Findings

### 1. SECRETS MANAGEMENT AUDIT ✅ **COMPLETED**

#### 1.1 Hardcoded API Key in Test File ✅ **RESOLVED**
- **File**: `smartsub-api/test_api_key.py:11`
- **Issue**: Hardcoded API key `"sk-smartsub-abc123def456ghi789"`
- **Impact**: API key exposed in version control
- **Solution Applied**:
  - ✅ Changed API key in Railway dashboard
  - ✅ Modified test file to use `os.getenv("API_KEY")`
  - ✅ Added `python-dotenv` dependency for automatic `.env` loading
  - ✅ Added validation to ensure API key is found

**Code Changes Made**:
```python
# Before (VULNERABLE)
API_KEY = "sk-smartsub-abc123def456ghi789"

# After (SECURE)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

**Test Results**:
- ✅ Test without API key: Status 401 (correct)
- ✅ Test with valid API key: Status 200 (correct)
- ✅ Health endpoint: Status 200 (correct)

---

### 2. API KEY EXPOSURE ANALYSIS 🔄 **IN PROGRESS**

#### 2.1 Client-Side API Key Storage ✅ **COMPLETED**

- **File**: `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/api/railwayClient.ts:39`
- **Issue**: API key stored in browser extension and transmitted in URL parameters
- **Impact**: API key visible in network requests, browser dev tools, extension source
- **Remediation**:
  1. Removed `RAILWAY_API_KEY` from Chrome extension code
  2. Modified extension to use proxy endpoint `/proxy-railway`
  3. API key now stored securely on server side only
- **Status**: ✅ **COMPLETED**

#### 2.2 API Key in URL Parameters ✅ **COMPLETED**
- **File**: `netflix-smart-subtitles-chrome-extension/my-netflix-extension-ts/src/api/railwayClient.ts:86-88`
- **Issue**: API key passed as query parameter `api_key: this.apiKey`
- **Impact**: API key logged in server logs, browser history, network monitoring
- **Remediation**:
  1. Removed API key from URL parameters in extension
  2. Created proxy endpoint that handles API key authentication server-side
  3. Extension now calls proxy without exposing API key
- **Status**: ✅ **COMPLETED**

#### 2.3 DeepL API Key Exposure Risk ✅ **RESOLVED**
- **File**: `smartsub-api/main.py:132`
- **Issue**: DeepL API key accepted from client requests (initial concern)
- **Audit Finding**: DeepL API key is *not* accepted from client requests; it's used server-side only via `os.getenv("DEEPL_API_KEY")`. The Chrome extension does not make direct calls to DeepL.
- **Status**: ✅ **RESOLVED**

---

## 🎉 **IMPLEMENTATION SUMMARY**

### **Proxy Solution Successfully Implemented**

**Architecture Change:**
```
BEFORE (VULNERABLE):
Extension Chrome → API Railway (with exposed API key)

AFTER (SECURE):
Extension Chrome → Proxy Endpoint → API Railway (with secure API key)
```

**Key Changes Made:**
1. **Backend**: Added `/proxy-railway` endpoint in FastAPI
2. **Extension**: Removed `RAILWAY_API_KEY` from client-side code
3. **Security**: API key now stored securely on server only
4. **Testing**: Verified proxy functionality works correctly

**Security Benefits:**
- ✅ API key no longer exposed in browser extension
- ✅ API key no longer transmitted in URL parameters
- ✅ API key no longer visible in network requests
- ✅ API key no longer accessible via browser dev tools

---

### 3. INPUT VALIDATION - SRT FILE PROCESSING ❌ **PENDING**

#### 3.1 No File Size Limits ❌ **PENDING**
- **File**: `smartsub-api/main.py:126-135`
- **Issue**: No file size validation on uploaded SRT files
- **Impact**: Potential DoS attacks via large file uploads
- **Proposed Solution**:
```python
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
if target_srt.size > MAX_FILE_SIZE or native_srt.size > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")
```

#### 3.2 Insufficient Input Sanitization ❌ **PENDING**
- **File**: `smartsub-api/src/srt_parser.py:18-56`
- **Issue**: Basic regex parsing without comprehensive validation
- **Impact**: Potential buffer overflow or injection attacks
- **Status**: ❌ **PENDING**

#### 3.3 No Rate Limiting ❌ **PENDING**
- **File**: `smartsub-api/main.py:126`
- **Issue**: No rate limiting on `/fuse-subtitles` endpoint
- **Impact**: API abuse, resource exhaustion
- **Proposed Solution**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/fuse-subtitles")
@limiter.limit("10/minute")
async def fuse_subtitles(request: Request, ...):
```

#### 3.4 Weak Timestamp Validation ❌ **PENDING**
- **File**: `smartsub-api/src/srt_parser.py:40-44`
- **Issue**: Basic timestamp format check without bounds validation
- **Impact**: Potential integer overflow or malformed data processing
- **Status**: ❌ **PENDING**

---

### 4. HTTPS AND TRANSPORT SECURITY ❌ **PENDING**

#### 4.1 Overly Permissive CORS ❌ **PENDING**
- **File**: `smartsub-api/main.py:45-51`
- **Issue**: `allow_origins=["*"]` allows any origin
- **Impact**: Potential CSRF attacks, data theft
- **Proposed Solution**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.netflix.com", "chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

#### 4.2 HTTP Health Check in Docker ❌ **PENDING**
- **File**: `smartsub-api/Dockerfile:32`
- **Issue**: Health check uses HTTP instead of HTTPS
- **Impact**: Man-in-the-middle attacks on health checks
- **Status**: ❌ **PENDING**

#### 4.3 No Content Security Policy ❌ **PENDING**
- **File**: Chrome extension manifest and API responses
- **Issue**: No CSP headers defined
- **Impact**: XSS attacks, script injection
- **Status**: ❌ **PENDING**

---

## 🚀 Next Actions (Priority Order)

### Immediate (Next Session)
1. **Fix Chrome Extension API Key Exposure**
   - Remove API key from client-side code
   - Implement server-side proxy or session-based authentication
   - Update webpack configuration

### High Priority
2. **Add File Size Limits**
   - Implement 5MB limit for SRT files
   - Add file type validation

3. **Implement Rate Limiting**
   - Add basic rate limiting (10 requests/minute)
   - Install and configure slowapi

### Medium Priority
4. **Restrict CORS Origins**
   - Limit to Netflix and Chrome extension origins
   - Remove wildcard permissions

5. **Add Security Headers**
   - Implement CSP headers
   - Add X-Frame-Options, X-Content-Type-Options

### Low Priority
6. **Improve Input Validation**
   - Add comprehensive SRT parsing validation
   - Implement timestamp bounds checking

---

## 📝 Implementation Notes

### Environment Variables
- **Production**: Railway dashboard environment variables
- **Development**: Local `.env` file (not committed to git)
- **Testing**: Export variables in terminal for test execution

### Testing Commands
```bash
# Start server with API key
export API_KEY=your_api_key_here
python3 main.py

# Run security tests
python test_api_key.py
```

### Security Score
- **Before**: 3/10 (Critical vulnerabilities present)
- **Current**: 5/10 (First critical issue resolved)
- **Target**: 8/10 (Production-ready security)

---

## 🔧 Technical Decisions Made

### Why python-dotenv?
- Standard in Python ecosystem
- Automatic `.env` file loading
- No manual environment variable management
- Consistent with industry best practices

### Why Manual Environment Variables for Testing?
- Simpler than complex `.env` file management
- Faster for quick security validation
- No additional dependencies for basic testing

### Why Keep Current CORS for Now?
- V0 development phase
- Chrome extension needs broad access
- Will be restricted in production

---

## 📚 References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [Chrome Extension Security](https://developer.chrome.com/docs/extensions/mv3/security/)

---

**Last Updated**: January 2025  
**Next Review**: After Chrome Extension security fixes  
**Maintainer**: Smart Subtitles Development Team
