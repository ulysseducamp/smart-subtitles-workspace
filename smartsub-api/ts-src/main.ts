/*
 * Smart Subtitles
 * Copyright (C) 2025 Smart Subtitles Contributors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

// src/main.ts
import 'dotenv/config';
import { readFileSync, writeFileSync } from 'fs';
import { parseSRT, generateSRT, fuseSubtitles, mergeOverlappingSubtitlesInSRT } from './logic.js';
import { DeepLAPI } from './deepl-api.js';

function printUsage() {
  console.log(`Usage: node dist/main.js --target <target.srt> --native <native.srt> --freq <freq.txt> --out <hybrid.srt> --topN <number> --lang <language_code> --native-lang <native_language_code> [--inline-translation] [--deepl-key <api_key>]\n\nArguments:\n  --target   SRT file in the target language (the language being learned)\n  --native   SRT file in the native language (the fallback translation)\n  --freq     Frequency list for the target language (e.g., fr_50k.txt)\n  --out      Output hybrid SRT file\n  --topN     Number of most frequent target language words considered 'known'\n  --lang     Language code for lemmatization (e.g., 'en', 'fr')\n  --native-lang Language code for native language translation (e.g., 'en', 'fr', 'pt')\n  --inline-translation  Enable inline translation for single unknown words\n  --deepl-key DeepL API key (optional, uses default if not provided)\n\nExample:\n  node dist/main.js --target fr.srt --native en.srt --freq fr_50k.txt --out hybrid.srt --topN 2000 --lang fr --native-lang en --inline-translation\n`);
}

function parseArgs(): { 
  target?: string; 
  native?: string; 
  freq?: string; 
  out?: string; 
  topN?: string; 
  lang?: string;
  nativeLang?: string;
  inlineTranslation?: boolean;
  deeplKey?: string;
} {
  const args = process.argv.slice(2);
  const argMap: { 
    target?: string; 
    native?: string; 
    freq?: string; 
    out?: string; 
    topN?: string; 
    lang?: string;
    nativeLang?: string;
    inlineTranslation?: boolean;
    deeplKey?: string;
  } = {};
  
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    const value = args[i + 1];
    
    if (key === '--inline-translation') {
      argMap.inlineTranslation = true;
      continue;
    }
    
    if (!key.startsWith('--') || !value) {
      printUsage();
      process.exit(1);
    }
    
    // Convert kebab-case to camelCase (e.g., --native-lang -> nativeLang)
    const argKey = key.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase()) as keyof typeof argMap;
    if (argKey !== 'inlineTranslation') {
      argMap[argKey] = value;
    }
    i++; // Skip the value in the next iteration
  }
  
  return argMap;
}

async function main() {
  const startTime = Date.now();
  const argMap = parseArgs();
  const { target, native, freq, out, topN, lang, nativeLang, inlineTranslation, deeplKey } = argMap;
  
  if (!target || !native || !freq || !out || !topN || !lang) {
    printUsage();
    process.exit(1);
  }

  // Only require nativeLang if inline translation is enabled
  if (inlineTranslation && !nativeLang) {
    console.error('Error: --native-lang is required when --inline-translation is enabled.');
    printUsage();
    process.exit(1);
  }

  const topNInt = parseInt(topN, 10);
  if (isNaN(topNInt) || topNInt <= 0) {
    console.error('Error: --topN must be a positive integer.');
    process.exit(1);
  }

  // Initialize DeepL API if inline translation is enabled
  let deeplAPI: DeepLAPI | undefined;
  if (inlineTranslation) {
    console.log('Initializing DeepL API for inline translation...');
    
    // Add validation for API key
    if (!process.env.DEEPL_API_KEY && !deeplKey) {
      console.error('ERROR: DeepL API key is required. Please set DEEPL_API_KEY environment variable or use --deepl-key argument.');
      process.exit(1);
    }
    
    deeplAPI = new DeepLAPI({
      apiKey: deeplKey || process.env.DEEPL_API_KEY || '',
      baseUrl: process.env.DEEPL_BASE_URL || 'https://api-free.deepl.com/v2/translate',
      timeout: parseInt(process.env.DEEPL_TIMEOUT || '5000'),
      maxRetries: parseInt(process.env.DEEPL_MAX_RETRIES || '3'),
      retryDelay: parseInt(process.env.DEEPL_RETRY_DELAY || '1000'),
      rateLimitDelay: parseInt(process.env.DEEPL_RATE_LIMIT_DELAY || '1000'),
    });
  }

  // Load frequency list and extract first N words
  const freqLines = readFileSync(freq, 'utf-8')
    .split(/\r?\n/)
    .filter(Boolean);
  const knownWords = new Set(
    freqLines.slice(0, topNInt).map(line => line.split(' ')[0].toLowerCase())
  );

  const srtTarget = readFileSync(target, 'utf-8');
  const srtNative = readFileSync(native, 'utf-8');
  let subsTarget = parseSRT(srtTarget);
  let subsNative = parseSRT(srtNative);

  // Log the number of subtitles detected in each file
  console.log('Target:', subsTarget.length, 'Native:', subsNative.length);

  // Merge overlapping subtitles in both files before vocabulary analysis
  console.log('Merging overlapping subtitles in input files...');
  const mergedTargetSRT = mergeOverlappingSubtitlesInSRT(generateSRT(subsTarget));
  const mergedNativeSRT = mergeOverlappingSubtitlesInSRT(generateSRT(subsNative));
  
  // Re-parse the merged files
  subsTarget = parseSRT(mergedTargetSRT);
  subsNative = parseSRT(mergedNativeSRT);
  
  console.log('After merging - Target:', subsTarget.length, 'Native:', subsNative.length);

  if (inlineTranslation) {
    console.log('Processing with inline translation enabled...');
    console.log(`Translating to native language: ${nativeLang}`);
  }

  // Show the target language subtitle if all words are known, otherwise show the native language subtitle
  const { hybrid, replacedCount, replacedWithOneUnknown, inlineTranslationCount, errorCount, translatedWords } = 
    await fuseSubtitles(subsTarget, subsNative, knownWords, lang, inlineTranslation, deeplAPI, nativeLang);

  // Generate the final SRT file (no post-processing merge needed since input is already clean)
  const finalSRT = generateSRT(hybrid);
  
  writeFileSync(out, finalSRT, 'utf-8');
  
  // Calculate operation duration
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  // Format duration
  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    const minutes = Math.floor(ms / 60000);
    const seconds = ((ms % 60000) / 1000).toFixed(1);
    return `${minutes}m ${seconds}s`;
  };

  // Calculate percentages
  const kept = subsTarget.length - replacedCount;
  const percentKept = ((kept / subsTarget.length) * 100).toFixed(1);
  const percentInline = ((inlineTranslationCount / subsTarget.length) * 100).toFixed(1);
  const percentInlineVsKept = kept > 0 ? ((inlineTranslationCount / kept) * 100).toFixed(1) : '0.0';

  // Get words translated multiple times
  const multipleTranslatedWords = Array.from(translatedWords.entries())
    .filter(([_, count]) => count > 1)
    .sort((a, b) => b[1] - a[1]) // Sort by count descending
    .map(([word, count]) => `${word} (translated ${count} times)`);

  // Calculate number of unique words translated
  const uniqueWordsTranslated = translatedWords.size;

  // Get list of all unique words that were translated
  const uniqueWordsList = Array.from(translatedWords.keys()).sort();

  // Output the new format
  console.log(`Hybrid SRT written to ${out} (top ${topNInt} frequent target language words known)`);
  console.log(`Subtitles kept in target language: ${kept}/${subsTarget.length} (${percentKept}%)`);
  console.log(`Subtitles with inline translation: ${inlineTranslationCount}/${subsTarget.length} (${percentInline}%)`);
  console.log(`Subs with inline translation compared to kept in target language: ${inlineTranslationCount}/${kept} (${percentInlineVsKept}%)`);
  console.log('—');
  
  if (inlineTranslation) {
    console.log(`Number of translation errors: ${errorCount}`);
    const deeplStats = deeplAPI?.getStats();
    if (deeplStats) {
      console.log(`DeepL API requests made: ${deeplStats.requestCount}`);
      console.log(`Translation cache size: ${deeplStats.cacheSize}`);
    }
    console.log('—');
  }

  if (multipleTranslatedWords.length > 0) {
    console.log(`Same word translated several times: ${multipleTranslatedWords.join(', ')}`);
    console.log('—');
  }

  console.log(`Number of new words translated: ${uniqueWordsTranslated}`);
  console.log(`New words: ${uniqueWordsList.join(', ')}`);
  console.log('—');

  console.log(`Operation duration: ${formatDuration(duration)}`);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
}); 