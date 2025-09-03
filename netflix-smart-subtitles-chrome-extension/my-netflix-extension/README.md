# Netflix Subtitle Downloader - TypeScript Migration Complete

This Chrome extension downloads subtitles from Netflix episodes and movies using JSON hijacking to intercept Netflix's subtitle API. The project now includes both the original JavaScript version and a complete TypeScript migration.

## Project Structure

```
prototype-extension-v6/
├── my-netflix-extension/          # Original JavaScript version
│   ├── manifest.json
│   ├── popup.html + popup.js
│   ├── content-script.js
│   └── page-script.js
└── my-netflix-extension-ts/       # NEW - TypeScript version
    ├── src/
    │   ├── popup/
    │   │   ├── popup.ts
    │   │   ├── popup.html
    │   │   └── popup.css
    │   ├── content-script.ts
    │   ├── page-script.ts
    │   └── types/
    │       └── netflix.d.ts
    ├── dist/ (webpack output)
    ├── manifest.json
    ├── package.json
    ├── tsconfig.json
    ├── webpack.config.js
    └── .cursorrules
```

## TypeScript Migration - COMPLETE ✅

### What Was Accomplished

✅ **Complete TypeScript Conversion** - All scripts converted with proper type annotations  
✅ **Build System Setup** - Webpack + TypeScript compilation  
✅ **Type Safety** - Comprehensive type definitions for Netflix API and extension messages  
✅ **Functionality Preserved** - Exact same behavior as original JavaScript version  
✅ **Critical Bug Fixed** - Type synchronization issue resolved (string vs number for movie IDs)  

### Key Technical Achievements

- **JSON Hijacking Preserved** - Core subtitle extraction mechanism intact
- **Message Passing Maintained** - Communication between popup ↔ content-script ↔ page-script
- **Netflix API Types** - Complete TypeScript interfaces for Netflix responses
- **Chrome Extension Types** - Proper typing for Chrome extension APIs
- **Build Process** - Production-ready webpack configuration

### Critical Bug Resolution

**Problem Identified:** Type mismatch between movie IDs
- **JavaScript version:** `currentMovieId` = number (e.g., `80179293`)
- **TypeScript version:** `currentMovieId` = string (e.g., `"80179293"`)
- **Result:** Cache lookup failures causing "No track list found for current movie"

**Solution Applied:**
- Converted `currentMovieId` to `number | null` type
- Added `+dsetIdStr` conversion in `updateCurrentMovieId()`
- Updated cache type to `Map<number, SubtitleTrack[]>`
- Synchronized all TypeScript interfaces

## How to Test

### JavaScript Version (Original)
1. Load `my-netflix-extension/` folder in Chrome extensions
2. Test on Netflix episode pages
3. Verify subtitle detection and download functionality

### TypeScript Version (New)
1. **Build the extension:**
   ```bash
   cd my-netflix-extension-ts
   npm install
   npm run build
   ```
2. **Load the extension:** Select `my-netflix-extension-ts/dist/` folder in Chrome extensions
3. **Test functionality:** Same as JavaScript version - should work identically

## Development Workflow

### TypeScript Development
```bash
cd my-netflix-extension-ts
npm run dev          # Development build with watch mode
npm run build        # Production build
npm run type-check   # TypeScript validation
npm run clean        # Clean build directory
```

### Key Files
- `src/page-script.ts` - **Most critical** - JSON hijacking and subtitle extraction
- `src/content-script.ts` - Message passing and script injection
- `src/popup/popup.ts` - UI logic and Chrome API communication
- `src/types/netflix.d.ts` - TypeScript type definitions

## Current Functionality (Both Versions)

✅ Netflix page detection  
✅ Episode/movie page detection  
✅ JSON hijacking for subtitle extraction  
✅ Subtitle track discovery and caching  
✅ WebVTT to SRT conversion  
✅ Subtitle download functionality  
✅ Popup interface with language selection  
✅ Communication between all components  
✅ **TypeScript type safety (TS version only)**  

## Technical Implementation

### JSON Hijacking (Preserved in Both Versions)
- **API Interception**: Hijacks `JSON.stringify` and `JSON.parse` to intercept Netflix API calls
- **WebVTT Injection**: Injects `webvtt-lssdh-ios8` format into Netflix profile requests
- **Data Capture**: Captures subtitle track metadata from API responses
- **Caching**: Implements track and WebVTT blob caching for performance

### Communication Flow
1. **Content Script** → Injects **Page Script** into Netflix page
2. **Page Script** → Hijacks JSON methods and captures subtitle data
3. **Page Script** → Sends subtitle tracks to **Content Script** via `window.postMessage`
4. **Content Script** → Forwards data to **Popup** via `chrome.tabs.sendMessage`
5. **Popup** → Displays available languages and handles download requests

### Subtitle Processing
- **Format Support**: WebVTT to SRT conversion
- **Text Processing**: Handles HTML tags, RTL text direction
- **File Naming**: Automatic filename generation with movie ID and language
- **Download**: Blob-based file download with proper MIME types

## Troubleshooting

### JavaScript Version
- If you see "Could not establish connection" error, refresh the Netflix page
- Make sure you're on a Netflix episode page (URL contains `/watch/`)
- Check browser console for detailed error messages

### TypeScript Version
- **Build errors:** Run `npm run clean` and try building again
- **Type errors:** Run `npm run type-check` to identify issues
- **Extension loading:** Make sure to load the `dist/` folder, not the source folder
- **Runtime errors:** Check that all TypeScript types are properly synchronized

## Known Limitations

- Only works on Netflix episode/movie pages (not homepage or browse pages)
- Requires Netflix to have subtitle tracks available for the content
- Depends on Netflix's current API structure (may break with updates)
- Download happens in the page context (not extension context)

## Next Steps (Future Enhancements)

- Add subtitle preview functionality
- Support for forced narratives and special subtitle types
- Better error handling for API changes
- Keyboard shortcuts for quick access
- Settings panel for user preferences
- **TypeScript-specific:** Add unit tests with Jest, ESLint configuration

## Acknowledgments

This extension is inspired by and based on [Subadub](https://github.com/colingogogo/subadub) by Russel Simmons, which is licensed under the MIT License. The core subtitle extraction technique using JSON hijacking and WebVTT format injection is derived from Subadub's implementation.

## Migration Success Criteria - ALL MET ✅

- ✅ Extension loads and appears in Chrome correctly
- ✅ Can extract Netflix subtitles exactly like before
- ✅ TypeScript compilation succeeds without errors
- ✅ All Chrome extension APIs properly typed
- ✅ No runtime errors in Netflix player
- ✅ JSON hijacking mechanism preserved exactly
- ✅ Message passing reliability maintained
- ✅ Netflix subtitle URL extraction logic intact
- ✅ Download functionality working perfectly
