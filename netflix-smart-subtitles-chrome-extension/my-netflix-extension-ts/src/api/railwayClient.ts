/*
 * Railway API Client
 * Handles secure communication with the Smart Subtitles Railway API
 */

import { SmartSubtitlesSettings } from '../types/netflix';

export interface RailwayAPIResponse {
  success: boolean;
  output_srt?: string;
  stats?: {
    total_subtitles: number;
    replaced_subtitles: number;
    replacement_rate: number;
    processing_time: number;
  };
  error?: string;
}

export interface RailwayAPIRequest {
  target_srt: string;
  native_srt: string;
  target_language: string;
  native_language: string;
  top_n_words: number;
  enable_inline_translation: boolean;
}

export class RailwayAPIClient {
  private static instance: RailwayAPIClient;
  private baseUrl: string;
  private apiKey: string;
  private endpoint: string;
  private timeout: number;

  private constructor() {
    // Get configuration from environment variables (injected by webpack)
    this.baseUrl = process.env.RAILWAY_API_URL || 'https://smartsub-api-production.up.railway.app';
    this.apiKey = process.env.RAILWAY_API_KEY || '';
    this.endpoint = process.env.FUSE_SUBTITLES_ENDPOINT || '/fuse-subtitles';
    this.timeout = 30000; // 30 seconds timeout
  }

  public static getInstance(): RailwayAPIClient {
    if (!RailwayAPIClient.instance) {
      RailwayAPIClient.instance = new RailwayAPIClient();
    }
    return RailwayAPIClient.instance;
  }

  /**
   * Process subtitles using the Railway API
   */
  public async processSubtitles(
    targetSrt: string,
    nativeSrt: string,
    settings: SmartSubtitlesSettings
  ): Promise<RailwayAPIResponse> {
    console.log('Railway API Client: Processing subtitles with settings:', settings);

    if (!this.apiKey) {
      throw new Error('API key not configured');
    }

    if (!targetSrt || !nativeSrt) {
      throw new Error('Missing required subtitle data');
    }

    const requestData: RailwayAPIRequest = {
      target_srt: targetSrt,
      native_srt: nativeSrt,
      target_language: settings.targetLanguage,
      native_language: settings.nativeLanguage,
      top_n_words: settings.vocabularyLevel,
      enable_inline_translation: false // Disabled for now
    };

    const url = `${this.baseUrl}${this.endpoint}`;
    const params = new URLSearchParams({
      api_key: this.apiKey
    });

    try {
      console.log('Railway API Client: Sending request to:', url);
      
      const formData = new FormData();
      formData.append('target_srt', new Blob([targetSrt], { type: 'text/plain' }), 'target.srt');
      formData.append('native_srt', new Blob([nativeSrt], { type: 'text/plain' }), 'native.srt');
      formData.append('target_language', requestData.target_language);
      formData.append('native_language', requestData.native_language);
      formData.append('top_n_words', requestData.top_n_words.toString());
      formData.append('enable_inline_translation', requestData.enable_inline_translation.toString());

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      const response = await fetch(`${url}?${params}`, {
        method: 'POST',
        body: formData,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      console.log('Railway API Client: Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Railway API Client: API error:', errorText);
        
        if (response.status === 401) {
          throw new Error('Invalid API key');
        } else if (response.status === 400) {
          throw new Error('Invalid request data');
        } else if (response.status === 500) {
          throw new Error('Server error occurred');
        } else {
          throw new Error(`API request failed: ${response.status} ${response.statusText}`);
        }
      }

      const result: RailwayAPIResponse = await response.json();
      console.log('Railway API Client: Processing result:', result);

      if (!result.success) {
        throw new Error(result.error || 'Unknown API error');
      }

      return result;

    } catch (error) {
      console.error('Railway API Client: Request failed:', error);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Request timeout - API took too long to respond');
        }
        throw error;
      }
      
      throw new Error('Network error occurred');
    }
  }

  /**
   * Test API connectivity
   */
  public async testConnection(): Promise<boolean> {
    try {
      const url = `${this.baseUrl}/health`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(url, {
        method: 'GET',
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      return response.ok;
    } catch (error) {
      console.error('Railway API Client: Connection test failed:', error);
      return false;
    }
  }

  /**
   * Get API configuration info (without exposing sensitive data)
   */
  public getConfigInfo(): { baseUrl: string; hasApiKey: boolean; endpoint: string } {
    return {
      baseUrl: this.baseUrl,
      hasApiKey: !!this.apiKey,
      endpoint: this.endpoint
    };
  }
}

// Export singleton instance
export const railwayAPIClient = RailwayAPIClient.getInstance();
