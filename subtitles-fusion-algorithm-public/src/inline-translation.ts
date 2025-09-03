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

import { Subtitle } from './logic';
import { DeepLAPI } from './deepl-api';

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

export interface InlineTranslationResult {
  text: string;
  translationApplied: boolean;
  error?: string;
}

export interface TranslationContext {
  sourceLang: string;
  targetLang: string;
  contextWindow: number;
}

export class InlineTranslationService {
  private deeplAPI: DeepLAPI;
  private context: TranslationContext;

  constructor(deeplAPI: DeepLAPI, context: TranslationContext) {
    this.deeplAPI = deeplAPI;
    this.context = context;
  }

  /**
   * Gets context lines around a specific subtitle index
   */
  private getContextLines(
    subtitles: Subtitle[],
    currentIndex: number,
    windowSize: number
  ): string[] {
    const start = Math.max(0, currentIndex - windowSize);
    const end = Math.min(subtitles.length, currentIndex + windowSize + 1);
    
    return subtitles
      .slice(start, end)
      .map(sub => sub.text)
      .filter(Boolean);
  }

  /**
   * Formats the inline translation according to the specification
   */
  private formatInlineTranslation(
    originalText: string,
    unknownWord: string,
    translation: string
  ): string {
    // Find the word in the original text (case-insensitive)
    const wordRegex = new RegExp(`\\b${unknownWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
    const match = wordRegex.exec(originalText);
    
    if (!match) {
      return originalText; // Fallback if word not found
    }

    const before = originalText.substring(0, match.index);
    const after = originalText.substring(match.index + match[0].length);
    
    return `${before}${match[0]} (${translation})${after}`;
  }

  /**
   * Processes a subtitle line with inline translation for single unknown words
   */
  async processSubtitleWithInlineTranslation(
    subtitle: Subtitle,
    subtitles: Subtitle[],
    unknownWords: string[],
    knownWords: Set<string>,
    isProperNoun: (word: string, sentence: string, frequencyList: Set<string>) => boolean
  ): Promise<InlineTranslationResult> {
    // Only apply inline translation if there's exactly one unknown word
    if (unknownWords.length !== 1) {
      return {
        text: subtitle.text,
        translationApplied: false,
      };
    }

    const unknownWord = unknownWords[0];
    
    // Check if it's a proper noun or a number (should not be translated)
    if (isProperNoun(unknownWord, subtitle.text, knownWords) || /^\d+$/.test(unknownWord)) {
      return {
        text: subtitle.text,
        translationApplied: false,
      };
    }

    try {
      // Get context window
      const subtitleIndex = subtitles.findIndex(sub => sub.index === subtitle.index);
      const contextLines = this.getContextLines(
        subtitles,
        subtitleIndex,
        this.context.contextWindow
      );

      // Translate the unknown word with context
      const translation = await this.deeplAPI.translateWithContext(
        unknownWord,
        this.context.sourceLang,
        this.context.targetLang,
        contextLines
      );

      // Format the result with inline translation
      const formattedText = this.formatInlineTranslation(
        subtitle.text,
        unknownWord,
        translation
      );

      return {
        text: formattedText,
        translationApplied: true,
      };
    } catch (error) {
      console.error(`Failed to translate word "${unknownWord}":`, error);
      return {
        text: subtitle.text,
        translationApplied: false,
        error: error instanceof Error ? error.message : 'Unknown translation error',
      };
    }
  }

  /**
   * Processes multiple subtitles with inline translation
   */
  async processSubtitlesWithInlineTranslation(
    subtitles: Subtitle[],
    knownWords: Set<string>,
    isProperNoun: (word: string, sentence: string, frequencyList: Set<string>) => boolean,
    normalizeWords: (text: string) => string[],
    batchLemmatize: (lines: string[], lang: string) => string[][]
  ): Promise<{
    processedSubtitles: Subtitle[];
    inlineTranslationCount: number;
    errorCount: number;
  }> {
    const processedSubtitles: Subtitle[] = [];
    let inlineTranslationCount = 0;
    let errorCount = 0;

    // Batch lemmatize all subtitle lines for efficiency
    const subtitleLines = subtitles.map(sub => normalizeWords(sub.text).join(' '));
    const lemmatizedWords = batchLemmatize(subtitleLines, this.context.sourceLang);

    for (let i = 0; i < subtitles.length; i++) {
      const subtitle = subtitles[i];
      const lemmatizedLine = lemmatizedWords[i];
      const originalWords = subtitle.text.split(/\s+/);

      // Find unknown words (excluding proper nouns and numbers)
      const unknownWords = lemmatizedLine.filter((word, j) => {
        const origWord = originalWords[j] || word;
        const isKnown = isWordKnown(word, knownWords, this.context.sourceLang);
        const isProper = isProperNoun(origWord, subtitle.text, knownWords);
        
        // NEW: Check if word is a number (consists entirely of digits)
        const isNumber = /^\d+$/.test(word);
        
        return !isKnown && !isProper && !isNumber;
      });

      if (unknownWords.length === 1) {
        // Apply inline translation
        const result = await this.processSubtitleWithInlineTranslation(
          subtitle,
          subtitles,
          unknownWords,
          knownWords,
          isProperNoun
        );

        if (result.translationApplied) {
          inlineTranslationCount++;
        } else if (result.error) {
          errorCount++;
        }

        processedSubtitles.push({
          ...subtitle,
          text: result.text,
        });
      } else {
        // Keep original subtitle (no inline translation needed)
        processedSubtitles.push(subtitle);
      }
    }

    return {
      processedSubtitles,
      inlineTranslationCount,
      errorCount,
    };
  }
} 