/*
 * API Types
 * Type definitions for Railway API communication
 */

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface SubtitleProcessingRequest {
  targetSrt: string;
  nativeSrt: string;
  frequencyList: string;
  settings: {
    targetLanguage: string;
    nativeLanguage: string;
    vocabularyLevel: number;
  };
}

export interface SubtitleProcessingResponse {
  success: boolean;
  processedSrt?: string;
  stats?: {
    totalSubtitles: number;
    replacedSubtitles: number;
    replacementRate: number;
    processingTime: number;
  };
  error?: string;
}

export interface APIError {
  code: string;
  message: string;
  details?: any;
}

export interface APIConfig {
  baseUrl: string;
  apiKey: string;
  timeout: number;
  retryAttempts: number;
}
