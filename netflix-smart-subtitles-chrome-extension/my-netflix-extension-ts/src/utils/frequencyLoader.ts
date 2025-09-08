/*
 * Frequency List Loader Utility
 * Loads and manages frequency lists for different languages
 */

export interface FrequencyList {
  language: string;
  words: Set<string>;
  count: number;
}

export class FrequencyLoader {
  private static instance: FrequencyLoader;
  private cache: Map<string, FrequencyList> = new Map();

  private constructor() {}

  public static getInstance(): FrequencyLoader {
    if (!FrequencyLoader.instance) {
      FrequencyLoader.instance = new FrequencyLoader();
    }
    return FrequencyLoader.instance;
  }

  /**
   * Load frequency list for a specific language
   */
  public async loadFrequencyList(language: string, maxWords: number = 5000): Promise<FrequencyList> {
    const cacheKey = `${language}-${maxWords}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    try {
      const filename = this.getFrequencyListFilename(language);
      const response = await fetch(chrome.runtime.getURL(`src/assets/${filename}`));
      
      if (!response.ok) {
        throw new Error(`Failed to load frequency list for ${language}: ${response.statusText}`);
      }

      const text = await response.text();
      const words = new Set<string>();
      
      // Parse the frequency list (one word per line)
      const lines = text.split('\n');
      let count = 0;
      
      for (const line of lines) {
        const word = line.trim().toLowerCase();
        if (word && count < maxWords) {
          words.add(word);
          count++;
        }
      }

      const frequencyList: FrequencyList = {
        language,
        words,
        count
      };

      this.cache.set(cacheKey, frequencyList);
      console.log(`Frequency list loaded for ${language}: ${count} words`);
      
      return frequencyList;
    } catch (error) {
      console.error(`Error loading frequency list for ${language}:`, error);
      throw error;
    }
  }

  /**
   * Get the filename for a language's frequency list
   */
  private getFrequencyListFilename(language: string): string {
    const languageMap: Record<string, string> = {
      'fr': 'fr-5000.txt',
      'en': 'en-10000.txt',
      'pt': 'pt-10000.txt'
    };

    const filename = languageMap[language.toLowerCase()];
    if (!filename) {
      throw new Error(`Unsupported language: ${language}`);
    }

    return filename;
  }

  /**
   * Check if a word is in the frequency list
   */
  public async isWordKnown(word: string, language: string, maxWords: number = 5000): Promise<boolean> {
    const frequencyList = await this.loadFrequencyList(language, maxWords);
    return frequencyList.words.has(word.toLowerCase());
  }

  /**
   * Get available languages
   */
  public getAvailableLanguages(): string[] {
    return ['fr', 'en', 'pt'];
  }

  /**
   * Clear cache (useful for testing or memory management)
   */
  public clearCache(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   */
  public getCacheStats(): { size: number; languages: string[] } {
    return {
      size: this.cache.size,
      languages: Array.from(this.cache.keys())
    };
  }
}

// Export singleton instance
export const frequencyLoader = FrequencyLoader.getInstance();
