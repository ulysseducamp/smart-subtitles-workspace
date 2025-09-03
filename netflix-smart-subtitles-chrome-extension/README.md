# Netflix Subtitle Downloader

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

A Chrome extension designed to download subtitles from Netflix episodes and movies, with advanced subtitle injection and overlay capabilities. This project provides both JavaScript and TypeScript implementations with modern build systems and type safety.

## Features

- **Subtitle Extraction**: Automatically detects and extracts available subtitle tracks from Netflix's API
- **Subtitle Download**: Download subtitles in SRT format for offline use
- **Subtitle Injection**: Replace Netflix's native subtitles with custom subtitle overlays
- **Real-time Integration**: Support for real SRT content integration with adaptive subtitle functionality
- **Multiple Languages**: Support for multiple languages and subtitle types
- **Type Safety**: TypeScript version with modern development practices and strict type checking
- **Memory Management**: Robust blob URL cleanup system to prevent memory leaks

## Project Structure

This project consists of three main components:

1. **Active Development (JavaScript)**: `my-netflix-extension/` - A fully functional Chrome extension
2. **TypeScript Version**: `my-netflix-extension-ts/` - A TypeScript rewrite with modern build system
3. **Reference Implementation**: `reference/subadub/` - An existing Netflix subtitle extension used as reference

## Installation

### Prerequisites

- Google Chrome or Chromium-based browser
- Node.js (for TypeScript version development)

### For Users

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd prototype-extension-v6
   ```

2. **JavaScript Version**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `my-netflix-extension/` folder

3. **TypeScript Version**:
   ```bash
   cd my-netflix-extension-ts
   npm install
   npm run build
   ```
   - Load the `dist/` folder as an unpacked extension in Chrome

### For Developers

1. Clone the repository and install dependencies:
   ```bash
   git clone <repository-url>
   cd prototype-extension-v6/my-netflix-extension-ts
   npm install
   ```

2. Development workflow:
   ```bash
   # Type checking
   npm run type-check
   
   # Development build with watch mode
   npm run dev
   
   # Production build
   npm run build
   
   # Clean build artifacts
   npm run clean
   ```

## Usage

1. **Install the extension** following the installation instructions above
2. **Navigate to Netflix** and start playing any movie or TV show
3. **Click the extension icon** in your browser toolbar
4. **Select your preferred subtitle** from the available options
5. **Download or inject** the subtitles as needed

### Subtitle Injection

The extension can replace Netflix's native subtitles with custom overlays:
- Automatically detects when subtitles are available
- Provides seamless integration with Netflix's player
- Supports real SRT content for adaptive subtitle functionality
- Includes memory leak prevention through robust blob URL cleanup

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow the existing code style** and conventions
3. **Add tests** for new functionality (when applicable)
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description of changes

### Development Guidelines

- Use TypeScript for new features in the TypeScript version
- Follow the existing architecture patterns
- Ensure memory management best practices are followed
- Test thoroughly on Netflix's interface

## License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

### AGPL-3.0 Requirements

As this project is licensed under AGPL-3.0, please note the following important requirements:

- **Source Code Availability**: If you use this software as a web service, you must provide users with access to the source code
- **Network Interaction**: The AGPL-3.0 license requires that if you run a modified version of this software on a server and let other users communicate with it there, your server must also allow them to download the source code corresponding to the modified version running there
- **Copyleft**: Any modifications to this software must also be licensed under AGPL-3.0

### For Web Applications

If you use this extension as part of a web application or service:
- You must provide a link to the source code in your application's interface
- Users must be able to access the complete source code of your modified version
- The source code must be available for as long as you offer the service

For more information about AGPL-3.0 requirements, see [https://www.gnu.org/licenses/agpl-3.0](https://www.gnu.org/licenses/agpl-3.0).

## Acknowledgments

- Based on the original Subadub extension by Russel Simmons
- Built with modern web technologies and Chrome Extension APIs
- Enhanced with TypeScript for improved development experience

## Support

For issues, questions, or contributions:
- Check existing issues in the repository
- Create a new issue with detailed information
- Follow the contributing guidelines for pull requests

---

**Note**: This extension is designed for educational and personal use. Please respect Netflix's terms of service and use responsibly.
