# Smart Subtitles

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

An adaptive bilingual subtitle system that creates personalized learning experiences by intelligently switching between target language and native language subtitles based on the user's vocabulary knowledge.

## Overview

Smart Subtitles uses frequency lists to determine which words the user "knows" and makes real-time decisions about subtitle language selection. The system provides:

- **Adaptive Learning**: Automatically adjusts difficulty based on vocabulary knowledge
- **Seamless Experience**: No manual switching between subtitle languages
- **Vocabulary Building**: Inline translation for single unknown words
- **Time Synchronization**: Advanced algorithm for perfect subtitle timing alignment
- **Multi-language Support**: Works with English, French, Portuguese, Spanish, German, and Italian

## License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

### AGPL-3.0 Requirements

As this project is licensed under AGPL-3.0, if you use this software as a web service or network application, you **must** provide users with access to the source code. This means:

- If you deploy this software as a web application, you must provide a link to the source code
- Users must be able to download and modify the source code
- Any modifications you make must also be licensed under AGPL-3.0
- The source code must be available for at least 3 years

For more information about AGPL-3.0 requirements, see [https://www.gnu.org/licenses/agpl-3.0](https://www.gnu.org/licenses/agpl-3.0).

## Installation

### Prerequisites

- Node.js (v16 or higher)
- Python 3 (for lemmatization)
- TypeScript compiler

### Setup

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

### Required Files

- **Frequency Lists**: Place in `frequency-lists/` directory
- **SRT Files**: Target and native language subtitle files
- **DeepL API Key**: For inline translation feature (optional)

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your DeepL API key in `.env`:
   ```bash
   DEEPL_API_KEY=your_actual_deepl_api_key_here
   ```

3. Optionally adjust other configuration values in `.env`

### Environment Variables

- `DEEPL_API_KEY`: Your DeepL API key (required)
- `DEEPL_BASE_URL`: DeepL API endpoint (default: https://api-free.deepl.com/v2/translate)
- `DEEPL_TIMEOUT`: Request timeout in ms (default: 5000)
- `DEEPL_MAX_RETRIES`: Maximum API call retries (default: 3)
- `DEEPL_RETRY_DELAY`: Delay between retries in ms (default: 1000)
- `DEEPL_RATE_LIMIT_DELAY`: Delay between API calls in ms (default: 500)

## Usage

### Basic Usage

```bash
# Build the project
npm run build

# Run with basic parameters
node dist/main.js --target fr.srt --native en.srt --freq frequency-lists/fr-5000.txt --out hybrid.srt --topN 2000 --lang fr --native-lang en

# Run with inline translation
node dist/main.js --target fr.srt --native en.srt --freq frequency-lists/fr-5000.txt --out hybrid.srt --topN 2000 --lang fr --native-lang en --inline-translation
```

### Command Line Options

- `--target`: Target language SRT file (language being learned)
- `--native`: Native language SRT file (user's native language)
- `--freq`: Frequency list file for vocabulary analysis
- `--out`: Output file for hybrid subtitles
- `--topN`: Number of most frequent words to consider "known"
- `--lang`: Target language code (fr, en, es, de, it, pt)
- `--native-lang`: Native language code
- `--inline-translation`: Enable inline translation for single unknown words

## Features

### Core Functionality

- **SRT Parsing and Generation**: Full support for SubRip subtitle format
- **Vocabulary-based Selection**: Intelligent language switching based on word frequency
- **Bidirectional Synchronization**: Advanced time alignment between subtitle versions
- **Inline Translation**: Single-word translation using DeepL API
- **Proper Noun Detection**: Smart identification of names and places
- **Contraction Handling**: English contraction processing
- **Overlapping Subtitle Merging**: Temporal alignment of complex subtitle sequences

### Supported Languages

- English (en)
- French (fr)
- Portuguese (pt)
- Spanish (es)
- German (de)
- Italian (it)

## Development

### Project Structure

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

### Testing

```bash
# Run DeepL API tests
npm test

# Test specific components
node tests/test-deepl.js
```

### Development Workflow

1. **Edit TypeScript**: Modify files in `src/`
2. **Build**: Run `npm run build` to compile
3. **Test**: Run `npm test` for basic testing
4. **Manual Testing**: Test with real SRT files
5. **Iterate**: Refine based on results

## Contributing

We welcome contributions! Please note that this project is licensed under AGPL-3.0, which means:

- All contributions must be licensed under AGPL-3.0
- Any derivative works must also be open source
- If you use this software as a web service, you must provide source code access

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
npm install

# Install Python dependencies
pip3 install simplemma

# Build the project
npm run build

# Run tests
npm test
```

## Roadmap

### Planned Features

- **Chrome Extension**: Netflix integration for real-time subtitle processing
- **Web Interface**: User-friendly web application
- **Advanced Vocabulary Tracking**: User progress monitoring
- **Machine Learning Integration**: Adaptive vocabulary learning
- **Batch Processing**: Handle multiple video files
- **Subtitle Quality Assessment**: Automatic quality scoring

### Technical Improvements

- **Pure TypeScript Migration**: Eliminate Python dependency
- **Performance Optimization**: Parallel processing and caching improvements
- **Enhanced Error Handling**: Better error recovery and reporting
- **Comprehensive Testing**: Full test coverage for all modules

## Support

For questions, issues, or contributions, please:

1. Check the [documentation](docs/MASTER_DOCUMENT.md)
2. Search existing issues
3. Create a new issue with detailed information

## License

Copyright (C) 2025 Smart Subtitles Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
