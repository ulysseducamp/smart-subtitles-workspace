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

import { spawnSync } from 'child_process';
import path from 'path';
import { DeepLAPI } from './deepl-api.js';
import { InlineTranslationService } from './inline-translation.js';

export interface Subtitle {
  index: string;
  start: string;
  end: string;
  text: string;
}

export function parseSRT(srt: string): Subtitle[] {
  const blocks = srt.split(/\r?\n\r?\n/);
  return blocks.map(block => {
    const lines = block.split(/\r?\n/);
    const index = lines[0];
    const [start, end] = lines[1]?.split(' --> ') || [null, null];
    const text = lines.slice(2).join('\n');
    return { index, start, end, text };
  }).filter(b => b.index && b.start && b.end);
}

export function generateSRT(subs: Subtitle[]): string {
  return subs.map(s => `${s.index}\n${s.start} --> ${s.end}\n${s.text}\n`).join('\n');
}

export function normalizeWords(text: string): string[] {
  return text
    .replace(/[^\p{L}\p{N}\s']/gu, ' ')
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean);
}

function getProjectRoot(): string {
  // Assuming this script is in 'src' folder at project root
  return path.join(__dirname, '..');
}

export function batchLemmatize(lines: string[], lang: string): string[][] {
    const projectRoot = getProjectRoot();
    const scriptPath = path.join(projectRoot, 'scripts', 'lemmatizer.py');
    const input = lines.join('\n');
    const pythonProcess = spawnSync('python3', [scriptPath, lang], {
        input,
        encoding: 'utf-8'
    });
    if (pythonProcess.error) {
        console.error("Failed to start subprocess.", pythonProcess.error);
        return lines.map(() => []);
    }
    if (pythonProcess.stderr && pythonProcess.stderr.length > 0) {
        console.error("Error from lemmatizer script:", pythonProcess.stderr);
        return lines.map(() => []);
    }
    return pythonProcess.stdout.trim().split(/\r?\n/).map(line => line.split(/\s+/).filter(Boolean));
}

export function lemmatizeSingleLine(line: string, lang: string): string[] {
    const projectRoot = getProjectRoot();
    const scriptPath = path.join(projectRoot, 'scripts', 'lemmatizer.py');
    const pythonProcess = spawnSync('python3', [scriptPath, lang], {
        input: line,
        encoding: 'utf-8'
    });
    if (pythonProcess.error) {
        console.error("Failed to start subprocess.", pythonProcess.error);
        return [];
    }
    if (pythonProcess.stderr && pythonProcess.stderr.length > 0) {
        console.error("Error from lemmatizer script:", pythonProcess.stderr);
        return [];
    }
    return pythonProcess.stdout.trim().split(/\s+/).filter(Boolean);
}

/**
 * Determines if a word is a proper noun according to the following rules:
 * 1. If the word is capitalized and NOT at the beginning of the sentence, it's a proper noun.
 * 2. If the word is capitalized and IS at the beginning of the sentence:
 *    - If it exists in the frequency list, it's a normal word.
 *    - If it does NOT exist in the frequency list, it's a proper noun.
 *
 * @param word The word to check (may include punctuation)
 * @param sentence The full sentence containing the word
 * @param frequencyList The set of known words (lemmatized, lowercase)
 * @returns true if the word is a proper noun, false otherwise
 */
export function isProperNoun(word: string, sentence: string, frequencyList: Set<string>): boolean {
  // Remove HTML tags from the word
  const noHtmlWord = word.replace(/<[^>]*>/g, '');
  // Remove leading/trailing punctuation from the word
  const cleanedWord = noHtmlWord.replace(/^[\p{P}]+|[\p{P}]+$/gu, '');
  if (!cleanedWord) return false;

  // If not capitalized, not a proper noun
  if (cleanedWord[0] !== cleanedWord[0].toUpperCase() || cleanedWord.toLowerCase() === cleanedWord) {
    return false;
  }

  // Find the first word in the sentence (after trimming leading spaces)
  const sentenceTrimmed = sentence.trim();
  // Split on whitespace, but keep punctuation attached for first word
  const firstWordMatch = sentenceTrimmed.match(/^([\p{L}\p{N}'-]+)/u);
  const firstWord = firstWordMatch ? firstWordMatch[1] : '';

  // Is this word at the beginning of the sentence?
  if (cleanedWord === firstWord) {
    // If the word (lowercased) is in the frequency list, it's a normal word
    if (frequencyList.has(cleanedWord.toLowerCase())) {
      return false;
    } else {
      return true; // Not in frequency list, treat as proper noun
    }
  } else {
    // Not at beginning, capitalized → proper noun
    return true;
  }
}

// Helper to strip HTML tags
const stripHtml = (str: string) => str.replace(/<[^>]*>/g, '');

// English contractions mapping for smart frequency list checking
const ENGLISH_CONTRACTIONS: Record<string, string[]> = {
  // Personal pronouns + be/have/will/would
  "you're": ["you", "are"],
  "you'll": ["you", "will"], 
  "you've": ["you", "have"],
  "you'd": ["you", "would"],
  "I'm": ["I", "am"],
  "I'll": ["I", "will"],
  "I've": ["I", "have"],
  "I'd": ["I", "would"],
  "we're": ["we", "are"],
  "we'll": ["we", "will"],
  "we've": ["we", "have"],
  "we'd": ["we", "would"],
  "they're": ["they", "are"],
  "they'll": ["they", "will"],
  "they've": ["they", "have"],
  "they'd": ["they", "would"],
  "he's": ["he", "is"],
  "he'll": ["he", "will"],
  "he'd": ["he", "would"],
  "she's": ["she", "is"],
  "she'll": ["she", "will"],
  "she'd": ["she", "would"],
  "it's": ["it", "is"],
  "it'll": ["it", "will"],
  "it'd": ["it", "would"],
  
  // Common verbs with not
  "don't": ["do", "not"],
  "doesn't": ["does", "not"],
  "didn't": ["did", "not"],
  "can't": ["can", "not"],
  "couldn't": ["could", "not"],
  "won't": ["will", "not"],
  "wouldn't": ["would", "not"],
  "shouldn't": ["should", "not"],
  "mustn't": ["must", "not"],
  "haven't": ["have", "not"],
  "hasn't": ["has", "not"],
  "hadn't": ["had", "not"],
  "isn't": ["is", "not"],
  "aren't": ["are", "not"],
  "wasn't": ["was", "not"],
  "weren't": ["were", "not"],
  
  // Demonstratives
  "that's": ["that", "is"],
  "that'll": ["that", "will"],
  "that'd": ["that", "would"],
  "there's": ["there", "is"],
  "there'll": ["there", "will"],
  "there'd": ["there", "would"],
  "here's": ["here", "is"],
  "here'll": ["here", "will"],
  "here'd": ["here", "would"],
  
  // Question words
  "who's": ["who", "is"],
  "who'll": ["who", "will"],
  "who'd": ["who", "would"],
  "what's": ["what", "is"],
  "what'll": ["what", "will"],
  "what'd": ["what", "would"],
  "where's": ["where", "is"],
  "where'll": ["where", "will"],
  "where'd": ["where", "would"],
  "when's": ["when", "is"],
  "when'll": ["when", "will"],
  "when'd": ["when", "would"],
  "why's": ["why", "is"],
  "why'll": ["why", "will"],
  "why'd": ["why", "would"],
  "how's": ["how", "is"],
  "how'll": ["how", "will"],
  "how'd": ["how", "would"],
  
  // Other common contractions
  "let's": ["let", "us"],
  "ma'am": ["madam"],
  "o'clock": ["of", "the", "clock"],
  "y'all": ["you", "all"],
  "gonna": ["going", "to"],
  "wanna": ["want", "to"],
  "gotta": ["got", "to"],
  "lemme": ["let", "me"],
  "gimme": ["give", "me"],
  "outta": ["out", "of"],
  "kinda": ["kind", "of"],
  "sorta": ["sort", "of"],
  "lotta": ["lot", "of"],
  "lotsa": ["lots", "of"],
  "cuppa": ["cup", "of"],
  "ain't": ["am", "not"],  // or "are not", "is not", "has not", "have not"
};

/**
 * Get the expanded form of a contraction for English
 * @param word The word to check
 * @returns Array of words if it's a contraction, null otherwise
 */
function getContractionExpansion(word: string): string[] | null {
  const wordLower = word.toLowerCase();
  const expansion = ENGLISH_CONTRACTIONS[wordLower];
  if (expansion) {
    // Preserve the original case of the first letter if it was capitalized
    if (word[0] === word[0].toUpperCase()) {
      return expansion.map((w, i) => 
        i === 0 ? w.charAt(0).toUpperCase() + w.slice(1) : w
      );
    }
    return expansion;
  }
  return null;
}

/**
 * Check if a word is known, including checking contractions for English
 * @param word The word to check
 * @param knownWords Set of known words
 * @param language The language code
 * @returns true if the word is known
 */
function isWordKnown(word: string, knownWords: Set<string>, language: string): boolean {
  const wordLower = word.toLowerCase();
  
  // First check if the word itself is known
  if (knownWords.has(wordLower)) {
    return true;
  }
  
  // For English, check if it's a contraction and if ALL words in the expansion are known
  if (language === 'en') {
    const expansion = getContractionExpansion(word);
    if (expansion) {
      // Check if ALL words in the expansion are known
      return expansion.every(expandedWord => 
        knownWords.has(expandedWord.toLowerCase())
      );
    }
  }
  
  return false;
}

function srtTimeToMs(time: string): number {
  try {
    const parts = time.split(/[:,]/);
    const h = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);
    const s = parseInt(parts[2], 10);
    const ms = parseInt(parts[3], 10);
    if (isNaN(h) || isNaN(m) || isNaN(s) || isNaN(ms)) return 0;
    return h * 3600000 + m * 60000 + s * 1000 + ms;
  } catch (e) {
    return 0;
  }
}

function hasIntersection(start1: string, end1: string, start2: string, end2: string): boolean {
    const start1Ms = srtTimeToMs(start1);
    const end1Ms = srtTimeToMs(end1);
    const start2Ms = srtTimeToMs(start2);
    const end2Ms = srtTimeToMs(end2);

    const intersectionStart = Math.max(start1Ms, start2Ms);
    const intersectionEnd = Math.min(end1Ms, end2Ms);

    return intersectionEnd - intersectionStart > 500;
}

export async function fuseSubtitles(
  targetSubs: Subtitle[],
  nativeSubs: Subtitle[],
  knownWords: Set<string>,
  language: string,
  enableInlineTranslation = false,
  deeplAPI?: DeepLAPI,
  nativeLang?: string
): Promise<{ 
  hybrid: Subtitle[]; 
  replacedCount: number; 
  replacedWithOneUnknown: number; 
  inlineTranslationCount: number; 
  errorCount: number;
  translatedWords: Map<string, number>;
}> {
  let replacedCount = 0;
  let replacedWithOneUnknown = 0;
  let inlineTranslationCount = 0;
  let errorCount = 0;
  let debugShown = 0;
  const translatedWords = new Map<string, number>();

  const finalSubtitles: Subtitle[] = [];
  const processedTargetIndices = new Set<string>();

  // Initialize inline translation service if enabled
  let inlineTranslationService: InlineTranslationService | null = null;
  if (enableInlineTranslation && deeplAPI) {
    inlineTranslationService = new InlineTranslationService(deeplAPI, {
      sourceLang: language,
      targetLang: getTargetLanguage(language, nativeLang),
      contextWindow: 2,
    });
  }

  for (let i = 0; i < targetSubs.length; i++) {
    const currentTargetSub = targetSubs[i];

    if (processedTargetIndices.has(currentTargetSub.index)) {
      continue;
    }

    // Lemmatize this specific subtitle individually
    const currentLine = normalizeWords(stripHtml(currentTargetSub.text)).join(' ');
    const lemmatizedWords = lemmatizeSingleLine(currentLine, language);
    const originalWords = stripHtml(currentTargetSub.text).split(/\s+/);

    // Add null check for lemmatizedWords
    if (!lemmatizedWords || !Array.isArray(lemmatizedWords)) {
      console.warn(`Warning: No lemmatized words found for subtitle ${currentTargetSub.index}, skipping.`);
      finalSubtitles.push(currentTargetSub);
      processedTargetIndices.add(currentTargetSub.index);
      continue;
    }

    // DETAIL FOR FIRST 20 SUBTITLES
    const shouldShowDetails = debugShown < 20;
    
    if (shouldShowDetails) {
      console.log(`\nSubtitle analysed: ${currentTargetSub.index} - "${currentTargetSub.text}"`);
    }

    // Analyze each word
    const properNouns: string[] = [];
    const lemmatizedWordsList: string[] = [];
    const unknownWordsList: string[] = [];

    const unknownWords = lemmatizedWords.filter((word, j) => {
      const origWord = originalWords[j] || word;
      const isKnown = isWordKnown(word, knownWords, language);
      const isProper = isProperNoun(origWord, currentTargetSub.text, knownWords);
      
      // NEW: Check if word is a number (consists entirely of digits)
      const isNumber = /^\d+$/.test(word);
      
      lemmatizedWordsList.push(word);
      
      if (isProper) {
        properNouns.push(origWord);
      } else if (!isKnown && !isNumber) {
        unknownWordsList.push(word);
      }

      return !isKnown && !isProper && !isNumber;
    });

    if (shouldShowDetails) {
      console.log(`Proper nouns: ${properNouns.join(', ') || 'none'}`);
      console.log(`Words lemmatised: ${lemmatizedWordsList.join(', ')}`);
      console.log(`Unknown words: ${unknownWordsList.join(', ') || 'none'}`);
    }

    if (unknownWords.length === 0) {
      if (shouldShowDetails) {
        console.log(`Decision: kept in target language`);
        console.log(`Reason: all words are known or proper nouns`);
      }
      finalSubtitles.push(currentTargetSub);
      processedTargetIndices.add(currentTargetSub.index);
      debugShown++;
      continue;
    }

    // Handle single unknown word with inline translation
    if (unknownWords.length === 1 && inlineTranslationService) {
      try {
        const result = await inlineTranslationService.processSubtitleWithInlineTranslation(
          currentTargetSub,
          targetSubs,
          unknownWords,
          knownWords,
          isProperNoun
        );

        if (result.translationApplied) {
          inlineTranslationCount++;
          // Track the translated word
          const translatedWord = unknownWords[0];
          translatedWords.set(translatedWord, (translatedWords.get(translatedWord) || 0) + 1);
          
          if (shouldShowDetails) {
            console.log(`Decision: inline translation applied`);
            console.log(`Reason: single unknown word translated`);
          }
          
          finalSubtitles.push({
            ...currentTargetSub,
            text: result.text,
          });
        } else if (result.error) {
          errorCount++;
          if (shouldShowDetails) {
            console.log(`Decision: replaced with native subtitle`);
            console.log(`Reason: inline translation failed - ${result.error}`);
          }
          
          // Fallback to replacement with native subtitle
          const intersectingNativeSubs = nativeSubs.filter(nativeSub =>
            hasIntersection(currentTargetSub.start, currentTargetSub.end, nativeSub.start, nativeSub.end)
          );

          if (intersectingNativeSubs.length > 0) {
            const combinedNativeSub = {
              text: intersectingNativeSubs.map(s => s.text).join('\n'),
              start: intersectingNativeSubs[0].start,
              end: intersectingNativeSubs[intersectingNativeSubs.length - 1].end,
            };

            const replacementSub = {
              index: '',
              start: currentTargetSub.start,
              end: currentTargetSub.end,
              text: combinedNativeSub.text,
            };

            finalSubtitles.push(replacementSub);
            replacedCount++;
            replacedWithOneUnknown++;
          } else {
            if (shouldShowDetails) {
              console.log(`Decision: kept in target language`);
              console.log(`Reason: no native subtitle found`);
            }
            finalSubtitles.push(currentTargetSub);
          }
        } else {
          if (shouldShowDetails) {
            console.log(`Decision: kept in target language`);
            console.log(`Reason: inline translation failed`);
          }
          finalSubtitles.push(currentTargetSub);
        }
      } catch (error) {
        console.error('Inline translation failed:', error);
        errorCount++;
        if (shouldShowDetails) {
          console.log(`Decision: kept in target language`);
          console.log(`Reason: inline translation error`);
        }
        // Fallback to original behavior
        finalSubtitles.push(currentTargetSub);
      }
      
      processedTargetIndices.add(currentTargetSub.index);
      debugShown++;
      continue;
    }

    // Handle multiple unknown words - replace with native subtitle
    if (shouldShowDetails) {
      console.log(`Decision: replaced with native subtitle`);
      console.log(`Reason: ${unknownWords.length} unknown words detected`);
    }
    
    const intersectingNativeSubs = nativeSubs.filter(nativeSub =>
      hasIntersection(currentTargetSub.start, currentTargetSub.end, nativeSub.start, nativeSub.end)
    );

    if (intersectingNativeSubs.length === 0) {
      if (shouldShowDetails) {
        console.log(`Decision: kept in target language`);
        console.log(`Reason: no native subtitle found`);
      }
      finalSubtitles.push(currentTargetSub);
      processedTargetIndices.add(currentTargetSub.index);
      debugShown++;
      continue;
    }

    // Find all target subtitles that overlap with the native subtitle time range
    const combinedNativeSub = {
      text: intersectingNativeSubs.map(s => s.text).join('\n'),
      start: intersectingNativeSubs[0].start,
      end: intersectingNativeSubs[intersectingNativeSubs.length - 1].end,
    };

    // Find all target subtitles that overlap with this native subtitle
    const overlappingTargetSubs = targetSubs.filter(sub =>
      !processedTargetIndices.has(sub.index) && hasIntersection(combinedNativeSub.start, combinedNativeSub.end, sub.start, sub.end)
    );

    if (overlappingTargetSubs.length === 0) {
      if (shouldShowDetails) {
        console.log(`Decision: kept in target language`);
        console.log(`Reason: no overlapping target subtitles found`);
      }
      finalSubtitles.push(currentTargetSub);
      processedTargetIndices.add(currentTargetSub.index);
      debugShown++;
      continue;
    }

    // Create a single replacement subtitle that covers the entire overlapping time range
    const replacementSub = {
      index: '', // Will be re-indexed later
      start: overlappingTargetSubs[0].start,
      end: overlappingTargetSubs[overlappingTargetSubs.length - 1].end,
      text: combinedNativeSub.text,
    };

    if (shouldShowDetails) {
      console.log(`Decision: replaced with native subtitle`);
      console.log(`Reason: ${overlappingTargetSubs.length} overlapping subtitles replaced`);
    }

    finalSubtitles.push(replacementSub);
    replacedCount += overlappingTargetSubs.length;
    
    // Mark all overlapping target subtitles as processed
    overlappingTargetSubs.forEach(sub => processedTargetIndices.add(sub.index));
    debugShown++;
  }

  const reIndexedHybrid = finalSubtitles.map((s, i) => ({ ...s, index: String(i + 1) }));
  return { 
    hybrid: reIndexedHybrid, 
    replacedCount, 
    replacedWithOneUnknown, 
    inlineTranslationCount, 
    errorCount,
    translatedWords
  };
}

/**
 * Helper function to determine target language for translation based on native subtitle file
 */
function getTargetLanguage(sourceLang: string, nativeLang?: string): string {
  // If native language is specified, use it as the translation target
  if (nativeLang) {
    return nativeLang;
  }
  
  // Fallback to language mapping if native language not specified
  const languageMap: { [key: string]: string } = {
    'en': 'fr',
    'fr': 'en',
    'pt': 'en',
    'es': 'en',
    'de': 'en',
    'it': 'en',
  };
  
  return languageMap[sourceLang] || 'en';
} 

/**
 * Merges subtitles with any temporal overlap by combining their text with line breaks.
 * Handles complex cases where multiple subtitles form an overlapping chain.
 * 
 * @param subtitles Array of subtitles to process
 * @returns Array of subtitles with overlapping entries merged
 */
export function mergeOverlappingSubtitles(subtitles: Subtitle[]): Subtitle[] {
  if (subtitles.length === 0) return subtitles;

  // Convert SRT time strings to milliseconds for easier comparison
  const subtitlesWithMs = subtitles.map(sub => ({
    ...sub,
    startMs: srtTimeToMs(sub.start),
    endMs: srtTimeToMs(sub.end)
  }));

  const merged: Subtitle[] = [];
  const processed = new Set<number>();

  for (let i = 0; i < subtitlesWithMs.length; i++) {
    if (processed.has(i)) continue;

    const current = subtitlesWithMs[i];
    const overlappingGroup: typeof subtitlesWithMs = [current];
    processed.add(i);

    // Find all subtitles that overlap with the current one
    let foundNewOverlap = true;
    while (foundNewOverlap) {
      foundNewOverlap = false;
      
      for (let j = 0; j < subtitlesWithMs.length; j++) {
        if (processed.has(j)) continue;

        const other = subtitlesWithMs[j];
        
        // Check if this subtitle overlaps with any subtitle in the current group
        const hasOverlap = overlappingGroup.some(groupSub => 
          (groupSub.startMs < other.endMs) && (other.startMs < groupSub.endMs)
        );

        if (hasOverlap) {
          overlappingGroup.push(other);
          processed.add(j);
          foundNewOverlap = true;
        }
      }
    }

    // Sort the overlapping group by start time to maintain chronological order
    overlappingGroup.sort((a, b) => a.startMs - b.startMs);

    // Create merged subtitle
    const mergedSubtitle: Subtitle = {
      index: overlappingGroup[0].index, // Keep the first subtitle's index
      start: overlappingGroup[0].start, // Use earliest start time
      end: overlappingGroup[overlappingGroup.length - 1].end, // Use latest end time
      text: overlappingGroup.map(sub => sub.text).join('\n') // Combine text with line breaks
    };

    merged.push(mergedSubtitle);
  }

  return merged;
} 

/**
 * Merges overlapping subtitles in an SRT file by parsing the file content,
 * applying the merge logic, and returning the corrected SRT content.
 * 
 * @param srtContent The SRT file content as a string
 * @returns The corrected SRT content with overlapping subtitles merged
 */
export function mergeOverlappingSubtitlesInSRT(srtContent: string): string {
  // Parse the SRT content into subtitle objects
  const subtitles = parseSRT(srtContent);
  
  // Apply the merge logic
  const mergedSubtitles = mergeOverlappingSubtitles(subtitles);
  
  // Generate the corrected SRT content
  return generateSRT(mergedSubtitles);
} 
