# Netflix Subtitle Downloader - TypeScript Version

A Chrome extension that downloads subtitles from Netflix episodes and movies. This is the TypeScript version of the original JavaScript extension.

**Inspired by and based on Subadub** (https://github.com/colingogogo/subadub)  
**Subadub Copyright (c) 2018 Russel Simmons - MIT License**

## Features

- **Automatic Subtitle Detection**: Automatically detects available subtitle tracks on Netflix
- **Multiple Language Support**: Supports all subtitle languages available for the content
- **SRT Format**: Downloads subtitles in standard SRT format
- **Closed Captions Support**: Includes closed captions when available
- **Immediate Injection**: Uses Subadub's immediate injection approach for reliable detection

## Architecture

The extension uses a three-script architecture:

```
popup.ts ↔ content-script.ts ↔ page-script.ts
```

- **popup.ts**: User interface and Chrome extension API communication
- **content-script.ts**: Message passing between popup and page script
- **page-script.ts**: JSON hijacking to intercept Netflix API responses

## Development Setup

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

### Build Commands

- **Development build with watch mode**:
  ```bash
  npm run dev
  ```

- **Production build**:
  ```bash
  npm run build
  ```

- **Type checking**:
  ```bash
  npm run type-check
  ```

- **Clean build directory**:
  ```bash
  npm run clean
  ```

### Loading the Extension

1. Build the extension: `npm run build`
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the `dist` folder
5. Navigate to Netflix and start watching content
6. Click the extension icon to download subtitles

## TypeScript Structure

```
src/
├── popup/
│   ├── popup.ts          # Popup interface logic
│   ├── popup.html        # Popup HTML
│   └── popup.css         # Popup styles
├── content-script.ts     # Content script for message passing
├── page-script.ts        # JSON hijacking and subtitle extraction
└── types/
    └── netflix.d.ts      # TypeScript type definitions
```

## Key Features Preserved

- **JSON Hijacking**: The core mechanism that intercepts Netflix API responses
- **Immediate Injection**: Page script is injected immediately for reliable detection
- **Message Passing**: Robust communication between all extension components
- **Subtitle Processing**: WebVTT to SRT conversion using browser TextTrack API
- **Caching**: Efficient caching of subtitle data and WebVTT files

## Technical Details

### JSON Hijacking Mechanism

The extension uses JSON hijacking to intercept Netflix API responses:

```typescript
// Override JSON.parse to capture subtitle data
const originalParse = JSON.parse;
JSON.parse = function(): any {
  const value = originalParse.apply(this, arguments as any);
  
  // Capture subtitle data from Netflix API responses
  if (value && value.result && value.result.movieId && value.result.timedtexttracks) {
    extractMovieTextTracks(value.result);
  }
  
  return value;
};
```

### Subtitle Format Conversion

Uses the browser's TextTrack API to convert WebVTT to SRT format, preserving timing and formatting while filtering out positioning information.

## License

MIT License - Based on Subadub by Russel Simmons

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run type checking: `npm run type-check`
5. Build and test: `npm run build`
6. Submit a pull request

## Troubleshooting

- **No subtitles found**: Refresh the Netflix page and try again
- **Extension not working**: Ensure you're on a Netflix video page
- **Build errors**: Run `npm run clean` and try building again
- **Type errors**: Run `npm run type-check` to identify issues
