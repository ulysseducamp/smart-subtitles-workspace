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

import 'dotenv/config';

export interface DeepLConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  maxRetries: number;
  retryDelay: number;
  rateLimitDelay?: number;
}

export interface DeepLRequest {
  text: string[];
  source_lang: string;
  target_lang: string;
  context?: string;
}

export interface DeepLResponse {
  translations: Array<{
    detected_source_language: string;
    text: string;
  }>;
}

export interface TranslationCache {
  [key: string]: {
    translation: string;
    timestamp: number;
  };
}

export class DeepLAPI {
  private config: DeepLConfig;
  private cache: TranslationCache = {};
  private requestCount = 0;
  private lastRequestTime = 0;
  private readonly CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours
  private rateLimitDelay: number;

  constructor(config: Partial<DeepLConfig> = {}) {
    this.config = {
      apiKey: config.apiKey || process.env.DEEPL_API_KEY || '',
      baseUrl: config.baseUrl || process.env.DEEPL_BASE_URL || 'https://api-free.deepl.com/v2/translate',
      timeout: config.timeout || parseInt(process.env.DEEPL_TIMEOUT || '5000'),
      maxRetries: config.maxRetries || parseInt(process.env.DEEPL_MAX_RETRIES || '3'),
      retryDelay: config.retryDelay || parseInt(process.env.DEEPL_RETRY_DELAY || '1000'),
      rateLimitDelay: config.rateLimitDelay || parseInt(process.env.DEEPL_RATE_LIMIT_DELAY || '500'),
    };
    this.rateLimitDelay = this.config.rateLimitDelay || parseInt(process.env.DEEPL_RATE_LIMIT_DELAY || '500');
    
    // Add API key validation
    if (!this.config.apiKey) {
      throw new Error('DeepL API key is required. Please set DEEPL_API_KEY environment variable.');
    }
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private getCacheKey(text: string, sourceLang: string, targetLang: string, context?: string): string {
    return `${text}|${sourceLang}|${targetLang}|${context || ''}`;
  }

  private isCacheValid(timestamp: number): boolean {
    return Date.now() - timestamp < this.CACHE_DURATION;
  }

  private async makeRequest(request: DeepLRequest, retryCount = 0): Promise<DeepLResponse> {
    // Rate limiting
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.rateLimitDelay) {
      await this.delay(this.rateLimitDelay - timeSinceLastRequest);
    }

    const formData = new URLSearchParams();
    formData.append('auth_key', this.config.apiKey);
    formData.append('text', request.text.join('\n'));
    formData.append('source_lang', request.source_lang);
    formData.append('target_lang', request.target_lang);
    
    if (request.context) {
      formData.append('context', request.context);
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);

    try {
      const response = await fetch(this.config.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      this.lastRequestTime = Date.now();
      this.requestCount++;

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`DeepL API error ${response.status}: ${errorText}`);
      }

      const data = await response.json() as DeepLResponse;
      return data;
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('DeepL API request timed out');
      }

      if (retryCount < this.config.maxRetries) {
        const delay = this.config.retryDelay * Math.pow(2, retryCount);
        console.warn(`DeepL API request failed, retrying in ${delay}ms (attempt ${retryCount + 1}/${this.config.maxRetries})`);
        await this.delay(delay);
        return this.makeRequest(request, retryCount + 1);
      }

      throw error;
    }
  }

  async translateWord(
    word: string,
    sourceLang: string,
    targetLang: string,
    context?: string
  ): Promise<string> {
    const cacheKey = this.getCacheKey(word, sourceLang, targetLang, context);
    
    // Check cache first
    if (this.cache[cacheKey] && this.isCacheValid(this.cache[cacheKey].timestamp)) {
      return this.cache[cacheKey].translation;
    }

    try {
      const request: DeepLRequest = {
        text: [word],
        source_lang: sourceLang.toUpperCase(),
        target_lang: targetLang.toUpperCase(),
        context,
      };

      const response = await this.makeRequest(request);
      const translation = response.translations[0]?.text || word;

      // Cache the result
      this.cache[cacheKey] = {
        translation,
        timestamp: Date.now(),
      };

      return translation;
    } catch (error) {
      console.error('DeepL translation failed:', error);
      throw error;
    }
  }

  async translateWithContext(
    text: string,
    sourceLang: string,
    targetLang: string,
    contextLines: string[]
  ): Promise<string> {
    const context = contextLines.join('\n');
    return this.translateWord(text, sourceLang, targetLang, context);
  }

  getStats(): { requestCount: number; cacheSize: number } {
    return {
      requestCount: this.requestCount,
      cacheSize: Object.keys(this.cache).length,
    };
  }

  clearCache(): void {
    this.cache = {};
  }
} 