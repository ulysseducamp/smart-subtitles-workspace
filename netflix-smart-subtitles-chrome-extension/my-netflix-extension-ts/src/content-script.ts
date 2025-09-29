/*
 * Netflix Subtitle Downloader
 * Copyright (C) 2025 Based on Subadub by Russel Simmons
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

// Netflix Subtitle Downloader
// Inspired by and based on Subadub (https://github.com/colingogogo/subadub)
// Subadub Copyright (c) 2018 Russel Simmons - MIT License
// This script runs on Netflix pages and injects the page script immediately

import { SubtitleTrack, ExtensionMessage, ChromeMessage, ChromeResponse, SmartSubtitlesSettings } from './types/netflix';

console.log('Netflix Subtitle Downloader: Content script loaded');

// Netflix BCP47 language code variants mapping to base language codes
const NETFLIX_LANGUAGE_VARIANTS: Record<string, string> = {
  // Spanish variants
  'es-ES': 'es',    // Spain Spanish
  'es-419': 'es',   // Latin American Spanish
  'es-MX': 'es',    // Mexican Spanish
  'es-AR': 'es',    // Argentine Spanish

  // Portuguese variants
  'pt-BR': 'pt',    // Brazilian Portuguese
  'pt-PT': 'pt',    // European Portuguese

  // English variants
  'en-US': 'en',    // American English
  'en-GB': 'en',    // British English
  'en-CA': 'en',    // Canadian English
  'en-AU': 'en',    // Australian English

  // French variants
  'fr-FR': 'fr',    // France French
  'fr-CA': 'fr',    // Canadian French

  // German variants
  'de-DE': 'de',    // German Germany
  'de-AT': 'de',    // Austrian German

  // Italian variants
  'it-IT': 'it',    // Italian Italy

  // Dutch variants
  'nl-NL': 'nl',    // Netherlands Dutch
  'nl-BE': 'nl',    // Belgian Dutch

  // Polish variants
  'pl-PL': 'pl',    // Polish Poland

  // Swedish variants
  'sv-SE': 'sv',    // Swedish Sweden

  // Danish variants
  'da-DK': 'da',    // Danish Denmark

  // Czech variants
  'cs-CZ': 'cs',    // Czech Republic

  // Japanese variants
  'ja-JP': 'ja',    // Japanese Japan

  // Korean variants
  'ko-KR': 'ko',    // Korean Republic of Korea
};

// Function to normalize Netflix BCP47 language codes to base language codes
function normalizeLanguageCode(code: string): string {
  return NETFLIX_LANGUAGE_VARIANTS[code] || code;
}

// Subtitle data storage
let availableTracks: SubtitleTrack[] = [];
let currentMovieId: number | null = null;

// Function to inject page script into the page context IMMEDIATELY
function injectPageScript(): void {
  console.log('Netflix Subtitle Downloader: Injecting page script immediately');
  
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('page-script.js');
  script.onload = function() {
    console.log('Netflix Subtitle Downloader: Page script loaded successfully');
    script.remove(); // Clean up the script tag
  };
  script.onerror = function() {
    console.error('Netflix Subtitle Downloader: Failed to load page script');
  };
  
  // Use Subadub's immediate injection approach
  document.head.insertBefore(script, document.head.firstChild);
}

// Function to get episode/movie title
function getNetflixTitle(): string {
  // Try multiple selectors to find the title
  const titleSelectors = [
    'h1[data-uia="hero-title"]',
    'h1.title',
    '.title',
    '[data-uia="hero-title"]',
    'h1'
  ];
  
  for (const selector of titleSelectors) {
    const element = document.querySelector(selector);
    if (element && element.textContent && element.textContent.trim()) {
      return element.textContent.trim();
    }
  }
  
  // Fallback: try to extract from URL
  const url = window.location.href;
  const match = url.match(/\/watch\/(\d+)/);
  if (match) {
    return `Netflix Video (ID: ${match[1]})`;
  }
  
  return 'Unknown Title';
}

// Function to handle messages from page script
function handlePageScriptMessage(event: MessageEvent): void {
  // Guard: origin + source + basic schema
  const allowedOrigins = new Set(['https://www.netflix.com', 'https://netflix.com']);
  if (!allowedOrigins.has(event.origin)) {
    return;
  }
  if (event.source !== window) {
    return;
  }
  if (!event.data || typeof event.data !== 'object' || typeof (event.data as any).type !== 'string') {
    return;
  }
  if (event.data.type === 'NETFLIX_SUBTITLES') {
    console.log('Netflix Subtitle Downloader: Received message from page script:', event.data);
    
    switch (event.data.action) {
      case 'TRACKS_AVAILABLE':
        availableTracks = event.data.data.tracks || [];
        currentMovieId = event.data.data.movieId;
        console.log('Netflix Subtitle Downloader: Available tracks updated:', availableTracks);
        break;
        
      case 'NO_TRACKS':
        availableTracks = [];
        console.log('Netflix Subtitle Downloader: No tracks available');
        break;
        
      case 'DOWNLOAD_SUCCESS':
        console.log('Netflix Subtitle Downloader: Download successful:', event.data.data.filename);
        break;
        
      case 'DOWNLOAD_ERROR':
        console.error('Netflix Subtitle Downloader: Download error:', event.data.data.error);
        break;

      case 'SMART_SUBTITLES_SUCCESS':
        console.log('Smart Netflix Subtitles: Processing successful:', event.data.data);
        // Forward success message to popup if needed
        break;

      case 'SMART_SUBTITLES_ERROR':
        console.error('Smart Netflix Subtitles: Processing error:', event.data.data.error);
        // Forward error message to popup if needed
        break;
    }
  } else if (event.data.type === 'NETFLIX_SUBTITLES_REQUEST') {
    console.log('Netflix Subtitle Downloader: Received request from page script:', event.data);
    
    if (event.data.action === 'GET_CURRENT_STATE') {
      console.log('Netflix Subtitle Downloader: Getting current state from chrome.storage.local...');
      
      // Get current state from chrome.storage.local with better error handling
      chrome.storage.local.get(['smartSubtitlesEnabled', 'targetLanguage', 'nativeLanguage', 'vocabularyLevel']).then(result => {
        let enabled = false;
        let settings: SmartSubtitlesSettings | null = null;
        
        console.log('Netflix Subtitle Downloader: Storage result:', result);
        
        if (result.smartSubtitlesEnabled && result.targetLanguage && result.nativeLanguage && result.vocabularyLevel) {
          enabled = true;
          settings = {
            enabled: true,
            targetLanguage: result.targetLanguage,
            nativeLanguage: result.nativeLanguage,
            vocabularyLevel: result.vocabularyLevel
          };
        }
        
        console.log('Netflix Subtitle Downloader: Sending state response - enabled:', enabled, 'settings:', settings);
        
        // Send response to page script
        window.postMessage({
          type: 'NETFLIX_SUBTITLES_STATE_RESPONSE',
          data: { enabled, settings }
        }, window.location.origin);
      }).catch(error => {
        console.error('Netflix Subtitle Downloader: Failed to get state from storage:', error);
        // Send error response
        window.postMessage({
          type: 'NETFLIX_SUBTITLES_STATE_RESPONSE',
          data: { enabled: false, settings: null }
        }, window.location.origin);
      });
    }
  }
}

// Function to send message to page script
function sendMessageToPageScript(message: Omit<ExtensionMessage, 'type'>): void {
  window.postMessage({
    type: 'NETFLIX_SUBTITLES_REQUEST',
    ...message
  }, window.location.origin);
}

// Function to handle messages from popup
function handlePopupMessage(
  request: ChromeMessage, 
  sender: chrome.runtime.MessageSender, 
  sendResponse: (response: ChromeResponse) => void
): void {
  console.log('Netflix Subtitle Downloader: Received message from popup:', request);
  
  if (request.action === 'checkNetflixPage') {
    // Always return true for Netflix pages - let page script handle the details
    const title = getNetflixTitle();
    console.log('Netflix Subtitle Downloader: Netflix page detected:', title);
    
    sendResponse({
      success: true,
      isNetflixEpisode: true,
      title: title,
      url: window.location.href
    });
  } else if (request.action === 'getSubtitles') {
    // Request available subtitles from page script
    console.log('Netflix Subtitle Downloader: Requesting subtitles from page script');
    sendMessageToPageScript({ action: 'GET_TRACKS' });
    
    // Send current tracks if available
    sendResponse({
      success: true,
      tracks: availableTracks,
      movieId: currentMovieId || undefined
    });
  } else if (request.action === 'downloadSubtitle') {
    // Request subtitle download from page script
    console.log('Netflix Subtitle Downloader: Requesting subtitle download:', request.trackId);
    sendMessageToPageScript({
      action: 'DOWNLOAD_SUBTITLE',
      data: { trackId: request.trackId! }
    });
    
    sendResponse({
      success: true,
      message: 'Download request sent'
    });
  } else if (request.action === 'processSmartSubtitles') {
    // Request Smart Subtitles processing from page script
    console.log('Smart Netflix Subtitles: Requesting subtitle processing:', request.settings);
    sendMessageToPageScript({
      action: 'processSmartSubtitles',
      settings: request.settings
    });

    sendResponse({
      success: true,
      message: 'Smart subtitles processing started'
    });
  } else if (request.action === 'getAvailableSubtitleTracks') {
    // Return available subtitle language codes for native language dropdown

    // Extract language codes from available tracks
    const availableLanguages = availableTracks.map(track => track.language).filter(Boolean);

    // Normalize BCP47 variants to base language codes (es-ES → es, pt-BR → pt)
    const normalizedLanguages = availableLanguages.map(normalizeLanguageCode);

    const uniqueLanguages = [...new Set(normalizedLanguages)]; // Remove duplicates

    sendResponse({
      success: true,
      availableLanguages: uniqueLanguages
    });
  } else {
    console.log('Netflix Subtitle Downloader: Unknown message action:', request.action);
    sendResponse({
      success: false,
      error: 'Unknown action'
    });
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener(handlePopupMessage);

// Listen for messages from page script
window.addEventListener('message', handlePageScriptMessage);

// INJECT PAGE SCRIPT IMMEDIATELY - no polling, no readiness checks
console.log('Netflix Subtitle Downloader: Injecting page script immediately');
injectPageScript();

// Log when content script is ready
console.log('Netflix Subtitle Downloader: Content script ready and listening for messages');
