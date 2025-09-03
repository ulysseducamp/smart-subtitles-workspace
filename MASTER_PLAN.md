# MASTER PLAN - Smart Netflix Subtitles V0

## Project Overview & Goals

**Objective**: Create a Chrome extension that extracts Netflix subtitles, processes them through an intelligent fusion algorithm, and injects personalized bilingual subtitles back into Netflix.

**Core Innovation**: Adaptive subtitle system that shows target language subtitles when vocabulary is known, native language when multiple words are unknown, and inline translations for single unknown words.

**Target Users**: Language learners who want Netflix subtitles adapted to their vocabulary level.

## Technical Stack Decisions

### Backend Service: Railway
- **Primary need**: Python FastAPI server for subtitle fusion algorithm
- **Key requirement**: Native Python support with `simplemma` lemmatization library
- **Development priority**: Git-based automatic deployment for rapid algorithm iteration
- **Cost**: Hobby plan $5/month minimum, Pro plan $20/month for production

### Database Service: Supabase ✅ (COMPLETED)
- **Status**: Phase 1 completed - project configured and frequency lists uploaded
- **Developer experience**: Visual dashboard and auto-generated REST APIs
- **Future-ready**: Built-in authentication system for V1 user accounts
- **Cost**: Free tier covers development and initial production usage

### Web Application Platform: Vercel
- **Specialization**: Optimized for React/Next.js frontends with global CDN
- **Complementary role**: Handles web dashboard while Railway manages Python backend
- **Integration**: Direct connection to Supabase for user data
- **Cost**: Free tier sufficient for expected usage

## Development Phases

### Phase 1: Database Setup ✅ (COMPLETED)

**Status**: All database infrastructure is operational

**Completed Tasks**:
- ✅ Supabase project created and configured
- ✅ Frequency lists uploaded (fr-5000.txt, en-10000.txt, etc.)
- ✅ API REST auto-generated and tested
- ✅ Database connectivity validated

### Phase 2: Backend API Development (Priority 2)

**Status**: Phase 2.1 completed locally, Phase 2.2 (Railway deployment) pending

#### **Étape 2.1 : Migration algorithme vers FastAPI ✅ (COMPLETED)**

**Status**: FastAPI backend with CLI wrapper is fully operational locally

**Completed Tasks**:
- ✅ FastAPI application structure created
- ✅ `/fuse-subtitles` endpoint implemented with proper form handling
- ✅ CLI integration with Node.js subtitle fusion algorithm
- ✅ File upload handling for SRT files and frequency lists
- ✅ Temporary file management and cleanup
- ✅ Error handling and HTTP status codes
- ✅ Endpoint testing and validation
- ✅ Response model implementation (SubtitleResponse)

**Technical Implementation**:
- ✅ Form data handling for request parameters
- ✅ File upload processing for target_srt, native_srt, frequency_list
- ✅ CLI command execution with proper parameter passing
- ✅ JSON response generation with success/error handling
- ✅ Resource cleanup to prevent temp file accumulation

#### **Étape 2.2 : Déploiement Railway (PENDING)**

**Objective**: Deploy FastAPI backend to Railway for internet accessibility

**Required Actions**:
1. **Configure Railway project** with Git-based automatic deployment
2. **Connect API to Supabase database** for frequency lists
3. **Create main endpoint** `/fusion-subtitles` that takes two SRT files and returns hybrid SRT
4. **Test API** with existing SRT files
5. **Validate internet accessibility** for Chrome extension integration

**Important Note**: Railway deployment must be completed before Phase 3, as the Chrome extension requires internet-accessible API endpoints.

### Phase 3: Chrome Extension Integration (Priority 3)

#### **Étape 3.1 : Extension UI Enhancement (2-3 hours)**

**Objective**: Add subtitle fusion controls to existing Chrome extension

**Actions**:
1. **Add dropdown controls** to extension popup:
   - Target language selection
   - Native language selection
   - Vocabulary level (top N words)
   - Inline translation toggle
2. **Integrate with existing extraction logic** (already functional)
3. **Add loading states** during API processing

#### **Étape 3.2 : API Integration (2-3 hours)**

**Objective**: Connect extension to Railway backend

**Actions**:
1. **Modify subtitle injection system** to use API results instead of local processing
2. **Implement API calls** to `/fuse-subtitles` endpoint
3. **Handle API responses** and inject processed subtitles
4. **Add error handling** for API failures

**Technical Notes**:
- **Keep existing injection logic**: WebVTT → blob → track injection (already working)
- **Add API layer**: Extension → Railway API → CLI processing → Results → Injection
- **Maintain performance**: API processing happens once per episode, not per subtitle

### Phase 4: Testing & Polish (Priority 4)

#### **Étape 4.1 : End-to-End Testing (2-3 hours)**

**Objective**: Validate complete workflow from Netflix to processed subtitles

**Test Scenarios**:
1. **Netflix subtitle extraction** → Verify existing functionality works
2. **API processing** → Test with various SRT files and language combinations
3. **Subtitle injection** → Validate processed subtitles appear correctly
4. **Performance validation** → Ensure <10 second processing time is acceptable

#### **Étape 4.2 : Error Handling & Edge Cases (1-2 hours)**

**Objective**: Robust error handling for production use

**Focus Areas**:
1. **API timeout handling** (set 5-minute timeout for CLI processing)
2. **File format validation** (ensure SRT files are valid before processing)
3. **Fallback mechanisms** (show original subtitles if processing fails)
4. **User feedback** (clear error messages and loading states)

## Timeline & Success Metrics

### **Development Timeline (Total: 6-8 days)**

- **Days 1-2**: ✅ CLI wrapper implementation (COMPLETED), Railway deployment (PENDING)
- **Days 3-4**: Chrome extension UI enhancement and API integration
- **Days 5-6**: End-to-end testing and error handling
- **Days 7-8**: Polish, documentation, and production readiness

### **Success Metrics**

**Performance Targets**:
- **Processing time**: <10 seconds per episode (V0 acceptable)
- **API reliability**: 99%+ success rate
- **User experience**: Seamless subtitle replacement in Netflix

**Quality Targets**:
- **Subtitle accuracy**: Match CLI output quality
- **Language support**: French, English, Portuguese (existing CLI capabilities)
- **Vocabulary adaptation**: Proper detection of known/unknown words

## Future Enhancements (Post-V0)

### **Performance Optimization**
- **Incremental CLI migration**: Port critical components to Python for better performance
- **Batch processing**: Process subtitles in chunks if full episode processing is too slow
- **Caching system**: Redis integration for repeated subtitle requests

### **Feature Expansion**
- **User accounts**: Leverage Supabase authentication for personalized settings
- **Vocabulary tracking**: Store user progress and adapt subtitles accordingly
- **Multiple language support**: Expand beyond current language combinations

## Risk Mitigation

### **Technical Risks**
- **CLI integration complexity**: Mitigated by wrapper approach and existing CLI testing
- **Performance bottlenecks**: Acceptable for V0, optimization planned for future versions
- **API reliability**: Railway's proven infrastructure reduces deployment risks

### **User Experience Risks**
- **Processing delays**: 5-10 seconds acceptable for episode-based processing
- **Error handling**: Robust fallbacks ensure Netflix experience remains functional
- **Browser compatibility**: Chrome extension approach leverages existing Netflix integration

## Architecture Philosophy

### **Separation of Concerns**
- **Railway**: Python FastAPI wrapper + CLI execution
- **Supabase**: Frequency lists and user data management
- **Chrome Extension**: Netflix integration and user interface
- **TypeScript CLI**: Core subtitle fusion algorithm (preserved)

### **Development Priorities**
1. **Functionality first**: Get working system with existing components
2. **User experience**: Seamless Netflix integration
3. **Performance**: Acceptable processing times for V0
4. **Maintainability**: Clean separation for future enhancements

### **Rejected Approaches**
- **Full algorithm migration**: Too risky and time-consuming for V0
- **Real-time processing**: Not needed for episode-based workflow
- **Complex infrastructure**: Keep it simple with proven services

---

**Next Action**: Complete Phase 2.2 - Railway Deployment
**Success Criteria**: FastAPI backend deployed and accessible from internet with working `/fuse-subtitles` endpoint
**Timeline**: 2-3 hours deployment configuration, 1 hour testing

**Previous Action**: ✅ Phase 2.1 - FastAPI Backend Implementation (COMPLETED)
**Success Criteria**: ✅ Working `/fuse-subtitles` endpoint that processes SRT files via CLI (LOCAL)
**Timeline**: ✅ 2-3 hours implementation, 1 hour testing (COMPLETED)

**Important Note**: Railway deployment must be completed before Phase 3, as the Chrome extension requires internet-accessible API endpoints.
