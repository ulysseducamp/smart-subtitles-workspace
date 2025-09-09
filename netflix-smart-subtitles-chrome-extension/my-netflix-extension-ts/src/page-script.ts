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
// This script is injected into Netflix pages and implements JSON hijacking to extract subtitles
// Following Subadub's immediate injection approach

import { SubtitleTrack, ExtensionMessage, SmartSubtitlesSettings } from './types/netflix';
import { railwayAPIClient } from './api/railwayClient';

(function initializeNetflixSubtitleExtractor(): void {
  console.log('Netflix Subtitle Downloader: Page script loaded - starting JSON hijacking immediately');

  // Constants from Subadub analysis
  const WEBVTT_FMT = 'webvtt-lssdh-ios8';
  
  // Injection-related constants (from Subadub)
  const TRACK_ELEM_ID = 'netflix-subtitle-track';
  const CUSTOM_SUBS_ELEM_ID = 'netflix-custom-subs';
  
  // Netflix content profiles for API interception
  const NETFLIX_PROFILES = [
    'heaac-2-dash',
    'heaac-2hq-dash',
    'playready-h264mpl30-dash',
    'playready-h264mpl31-dash',
    'playready-h264hpl30-dash',
    'playready-h264hpl31-dash',
    'vp9-profile0-L30-dash-cenc',
    'vp9-profile0-L31-dash-cenc',
    'dfxp-ls-sdh',
    'simplesdh',
    'nflx-cmisc',
    'BIF240',
    'BIF320'
  ];

  // Caching system for subtitle data
  const trackListCache = new Map<number, SubtitleTrack[]>(); // from movie ID to list of available tracks
  const webvttCache = new Map<string, Blob>(); // from 'movieID/trackID' to blob
  let currentMovieId: number | null = null;
  let selectedTrackId: string | null = null;

  // Injection state variables (simplified)
  let currentBlobUrl: string | null = null; // Track current blob URL for cleanup

  // Smart Subtitles state variables
  let smartSubtitlesEnabled = false;
  let currentSettings: SmartSubtitlesSettings | null = null;
  let isProcessingSubtitles = false;
  let processedSubtitlesCache = new Map<string, string>(); // Cache for processed subtitles

  // Function to request current state from content script with improved error handling
  async function requestCurrentState(): Promise<{enabled: boolean, settings: SmartSubtitlesSettings | null}> {
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        console.log('Smart Netflix Subtitles: State request timeout - assuming disabled');
        resolve({enabled: false, settings: null});
      }, 2000); // Increased timeout

      const handleResponse = (event: MessageEvent) => {
        if (event.data.type === 'NETFLIX_SUBTITLES_STATE_RESPONSE') {
          clearTimeout(timeout);
          window.removeEventListener('message', handleResponse);
          console.log('Smart Netflix Subtitles: Received state response:', event.data.data);
          resolve(event.data.data);
        }
      };

      window.addEventListener('message', handleResponse);
      
      // Request state from content script
      console.log('Smart Netflix Subtitles: Requesting current state from content script...');
      notifyContentScript({
        type: 'NETFLIX_SUBTITLES_REQUEST',
        action: 'GET_CURRENT_STATE'
      });
    });
  }

  // Function to find subtitle-related properties in Netflix API objects
  function findSubtitlesProperty(obj: any): string[] | null {
    for (const key in obj) {
      const value = obj[key];
      if (Array.isArray(value)) {
        if (key === 'profiles' || value.some((item: string) => NETFLIX_PROFILES.includes(item))) {
          return value;
        }
      }
      if (typeof value === 'object' && value !== null) {
        const prop = findSubtitlesProperty(value);
        if (prop) {
          return prop;
        }
      }
    }
    return null;
  }

  // Function to extract movie text tracks from Netflix API response
  function extractMovieTextTracks(movieObj: any): void {
    const movieId = movieObj.movieId as number;
    console.log('Netflix Subtitle Downloader: Extracting tracks for movie ID:', movieId);

    // Update current movie ID when we detect new content
    currentMovieId = movieId;
    if (!currentMovieId) {
      selectedTrackId = null;
    }

    const usableTracks: SubtitleTrack[] = [];
    
    if (!movieObj.timedtexttracks) {
      console.log('Netflix Subtitle Downloader: No timedtexttracks found');
      return;
    }

    console.log('Netflix Subtitle Downloader: Found timedtexttracks:', movieObj.timedtexttracks);
    
    for (const track of movieObj.timedtexttracks) {
      console.log('Netflix Subtitle Downloader: Processing track:', track.language);
      
      // Skip forced narratives and "none" tracks
      if (track.isForcedNarrative || track.isNoneTrack) {
        console.log('Netflix Subtitle Downloader: Skipping forced/none track');
        continue;
      }

      if (!track.ttDownloadables) {
        console.log('Netflix Subtitle Downloader: No ttDownloadables found');
        continue;
      }

      const webvttDL = track.ttDownloadables[WEBVTT_FMT];
      console.log('Netflix Subtitle Downloader: WebVTT downloadable:', webvttDL);
      
      if (!webvttDL || !webvttDL.urls) {
        console.log('Netflix Subtitle Downloader: No WebVTT URLs found');
        continue;
      }

      const bestUrl = webvttDL.urls[0].url;
      if (!bestUrl) {
        console.log('Netflix Subtitle Downloader: No valid URL found');
        continue;
      }

      const isClosedCaptions = track.rawTrackType === 'closedcaptions';

      usableTracks.push({
        id: track.new_track_id,
        language: track.language,
        languageDescription: track.languageDescription,
        bestUrl: bestUrl,
        isClosedCaptions: isClosedCaptions,
      });
    }

    console.log('Netflix Subtitle Downloader: Caching movie tracks:', movieId, usableTracks);
    trackListCache.set(movieId, usableTracks);
    
    // Notify content script about available tracks
    notifyContentScript({
      type: 'NETFLIX_SUBTITLES',
      action: 'TRACKS_AVAILABLE',
      data: {
        movieId: movieId,
        tracks: usableTracks
      }
    });

    // TRIGGER SUBTITLE INJECTION - Start injection when tracks are available
    console.log('Netflix Subtitle Downloader: Triggering subtitle injection after track discovery');
    reconcileSubtitleInjection();

    // AUTO-PROCESS SMART SUBTITLES - Request current state and process if enabled
    if (usableTracks.length > 0) {
      console.log('Smart Netflix Subtitles: Requesting current state for auto-processing...');
      
      // Retry mechanism for state requests
      const tryAutoProcessing = async (retryCount = 0) => {
        try {
          const {enabled, settings} = await requestCurrentState();
          
          if (enabled && settings) {
            console.log('Smart Netflix Subtitles: Auto-processing subtitles for movie ID:', movieId);
            await processSmartSubtitles(settings);
          } else {
            console.log('Smart Netflix Subtitles: Extension disabled or no settings, skipping auto-processing');
            console.log('Smart Netflix Subtitles: State received - enabled:', enabled, 'settings:', settings);
          }
        } catch (error) {
          console.error('Smart Netflix Subtitles: Failed to get current state:', error);
          
          // Retry up to 2 times with increasing delay
          if (retryCount < 2) {
            console.log(`Smart Netflix Subtitles: Retrying state request (${retryCount + 1}/2)...`);
            setTimeout(() => tryAutoProcessing(retryCount + 1), 1000 * (retryCount + 1));
          } else {
            console.log('Smart Netflix Subtitles: Max retries reached, skipping auto-processing');
          }
        }
      };
      
      tryAutoProcessing();
    }
  }

  // Function to convert WebVTT text to plain text plus "simple" tags (allowed in SRT)
  const TAG_REGEX = RegExp('</?([^>]*)>', 'ig');
  function vttTextToSimple(s: string, netflixRTLFix = true): string {
    let simpleText = s;

    // Strip tags except simple ones (i, u, b)
    simpleText = simpleText.replace(TAG_REGEX, function (match, p1) {
      return ['i', 'u', 'b'].includes(p1.toLowerCase()) ? match : '';
    });

    if (netflixRTLFix) {
      // Handle RTL text direction fixes
      const lines = simpleText.split('\n');
      const newLines: string[] = [];
      for (const line of lines) {
        if (line.startsWith('&lrm;')) {
          newLines.push('\u202a' + line.slice(5) + '\u202c');
        } else if (line.startsWith('&rlm;')) {
          newLines.push('\u202b' + line.slice(5) + '\u202c');
        } else {
          newLines.push(line);
        }
      }
      simpleText = newLines.join('\n');
    }

    return simpleText;
  }

  // Function to format time for SRT format
  function formatTime(t: number): string {
    const date = new Date(0, 0, 0, 0, 0, 0, t * 1000);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    const ms = date.getMilliseconds().toString().padStart(3, '0');
    return hours + ':' + minutes + ':' + seconds + ',' + ms;
  }

  // Function to convert WebVTT to SRT using browser's TextTrack API (Subadub approach)
  function convertWebVTTToSRTUsingTextTrack(webvttBlob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      // Create a temporary video element to use TextTrack API
      const tempVideo = document.createElement('video');
      const tempTrack = document.createElement('track');
      
      tempTrack.kind = 'subtitles';
      tempTrack.default = true;
      tempVideo.appendChild(tempTrack);
      
      // Create object URL for the WebVTT blob
      const trackUrl = URL.createObjectURL(webvttBlob);
      tempTrack.src = trackUrl;
      
      tempTrack.addEventListener('load', function() {
        try {
          const srtChunks: string[] = [];
          let idx = 1;
          
          // Use the browser's parsed cues (positioning info automatically filtered)
          for (const cue of tempTrack.track!.cues!) {
            const cleanedText = vttTextToSimple((cue as any).text, true);
            srtChunks.push(idx + '\n' + formatTime(cue.startTime) + ' --> ' + formatTime(cue.endTime) + '\n' + cleanedText + '\n\n');
            idx++;
          }
          
          // Clean up
          URL.revokeObjectURL(trackUrl);
          tempVideo.remove();
          
          resolve(srtChunks.join(''));
        } catch (error) {
          // Clean up on error
          URL.revokeObjectURL(trackUrl);
          tempVideo.remove();
          reject(error);
        }
      }, false);
      
      tempTrack.addEventListener('error', function() {
        // Clean up on error
        URL.revokeObjectURL(trackUrl);
        tempVideo.remove();
        reject(new Error('Failed to load WebVTT track'));
      }, false);
    });
  }

  // Function to download subtitle file
  async function downloadSubtitle(trackId: string): Promise<string> {
    console.log('Netflix Subtitle Downloader: Downloading subtitle for track:', trackId);
    
    if (!currentMovieId) {
      throw new Error('No current movie ID');
    }

    const trackList = trackListCache.get(currentMovieId);
    if (!trackList) {
      throw new Error('No track list found for current movie');
    }

    const track = trackList.find(t => t.id === trackId);
    if (!track) {
      throw new Error('Track not found');
    }

    const cacheKey = currentMovieId + '/' + trackId;
    
    // Check if we have cached data
    if (!webvttCache.has(cacheKey)) {
      console.log('Netflix Subtitle Downloader: Fetching WebVTT from:', track.bestUrl);
      
      try {
        const response = await fetch(track.bestUrl);
        if (!response.ok) {
          throw new Error('Failed to fetch WebVTT file');
        }
        
        const blob = await response.blob();
        webvttCache.set(cacheKey, blob);
        console.log('Netflix Subtitle Downloader: WebVTT cached successfully');
      } catch (error) {
        console.error('Netflix Subtitle Downloader: Error fetching WebVTT:', error);
        throw error;
      }
    }

    const webvttBlob = webvttCache.get(cacheKey)!;
    
    // Use the new TextTrack-based conversion (Subadub approach)
    const srtContent = await convertWebVTTToSRTUsingTextTrack(webvttBlob);

    // Generate filename
    let filename = 'netflix_subtitle';
    if (currentMovieId) {
      filename += '_' + currentMovieId;
    }
    filename += '_' + track.language + '.srt';

    // Create and trigger download
    const srtBlob = new Blob([srtContent], { type: 'text/srt' });
    const srtUrl = URL.createObjectURL(srtBlob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = srtUrl;
    downloadLink.download = filename;
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    // Clean up
    URL.revokeObjectURL(srtUrl);
    
    console.log('Netflix Subtitle Downloader: Subtitle downloaded:', filename);
    return filename;
  }

  // Function to notify content script
  function notifyContentScript(message: ExtensionMessage): void {
    window.postMessage(message, '*');
  }

  // INJECTION FUNCTIONS (Based on Subadub implementation)
  
  // Function to create and inject track element with test WebVTT
  function addTrackElem(videoElem: HTMLVideoElement, blob: Blob, srclang: string, isLoading: boolean = false): void {
    console.log('Netflix Subtitle Downloader: Adding track element for injection');
    
    // Always clean up existing elements and blob URL first
    removeTrackElem();
    
    const trackElem = document.createElement('track');
    trackElem.id = TRACK_ELEM_ID;
    
    // Create and track new blob URL
    currentBlobUrl = URL.createObjectURL(blob);
    trackElem.src = currentBlobUrl;
    
    trackElem.kind = 'subtitles';
    trackElem.default = true;
    trackElem.srclang = srclang;
    videoElem.appendChild(trackElem);
    trackElem.track!.mode = 'hidden'; // This can only be set after appending

    trackElem.addEventListener('load', function() {
      console.log('Netflix Subtitle Downloader: Track loaded successfully');
    }, false);

    // Create custom subtitle overlay div (based on Subadub styling)
    const customSubsElem = document.createElement('div');
    customSubsElem.id = CUSTOM_SUBS_ELEM_ID;
    const textColor = isLoading ? '#4CAF50' : 'white'; // Green for loading, white for normal
    customSubsElem.style.cssText = `position: absolute; bottom: 20vh; left: 0; right: 0; color: ${textColor}; font-size: 3vw; text-align: center; user-select: text; -moz-user-select: text; z-index: 100; pointer-events: none`;

    // Handle cue changes for real-time subtitle display
    trackElem.addEventListener('cuechange', function(e) {
      // Remove all children
      while (customSubsElem.firstChild) {
        customSubsElem.removeChild(customSubsElem.firstChild);
      }

      const track = e.target as HTMLTrackElement;
      console.log('Netflix Subtitle Downloader: Active cues:', track.track?.activeCues);
      
      if (track.track?.activeCues) {
        for (const cue of track.track.activeCues) {
          const cueElem = document.createElement('div');
          cueElem.style.cssText = 'background: rgba(0,0,0,0.8); white-space: pre-wrap; padding: 0.2em 0.3em; margin: 10px auto; width: fit-content; width: -moz-fit-content; pointer-events: auto';
          cueElem.innerHTML = vttTextToSimple((cue as any).text, true); // May contain simple tags like <i> etc.
          customSubsElem.appendChild(cueElem);
        }
      }
    }, false);

    // Append overlay to the player (Enhanced player detection - Solution C Enhanced)
    let playerElem = document.querySelector('.watch-video');
    
    // Fallback selectors for different Netflix DOM structures (avoiding billboard elements)
    if (!playerElem) {
      playerElem = document.querySelector('[data-uia="video-player"]');
    }
    if (!playerElem) {
      playerElem = document.querySelector('.VideoPlayer');
    }
    if (!playerElem) {
      playerElem = document.querySelector('.player-container');
    }
    if (!playerElem) {
      playerElem = document.querySelector('[data-testid="video-player"]');
    }
    if (!playerElem) {
      playerElem = document.querySelector('.netflix-player');
    }
    if (!playerElem) {
      // More specific fallback: avoid billboard/trailer elements
      const allVideoElements = document.querySelectorAll('[class*="video"], [class*="player"]');
      for (const elem of allVideoElements) {
        const className = elem.className.toLowerCase();
        // Skip billboard, trailer, and other non-video elements
        if (!className.includes('billboard') && !className.includes('trailer') && !className.includes('preview')) {
          playerElem = elem;
          break;
        }
      }
    }

    if (!playerElem) {
      console.error('Netflix Subtitle Downloader: Could not find player element to append subtitles to');
      console.log('Netflix Subtitle Downloader: Available video-related elements:', {
        watchVideo: document.querySelector('.watch-video'),
        videoPlayer: document.querySelector('[data-uia="video-player"]'),
        videoPlayerClass: document.querySelector('.VideoPlayer'),
        playerContainer: document.querySelector('.player-container'),
        testIdPlayer: document.querySelector('[data-testid="video-player"]'),
        netflixPlayer: document.querySelector('.netflix-player'),
        videoElements: document.querySelectorAll('[class*="video"]'),
        playerElements: document.querySelectorAll('[class*="player"]'),
        watchElements: document.querySelectorAll('[class*="watch"]')
      });
      return;
    }

    console.log('Netflix Subtitle Downloader: Found player element:', playerElem);
    playerElem.appendChild(customSubsElem);
    console.log('Netflix Subtitle Downloader: Track element and overlay added successfully');
  }

  // Function to remove track element and overlay
  function removeTrackElem(): void {
    // Clean up tracked blob URL first to prevent memory leaks
    if (currentBlobUrl) {
      URL.revokeObjectURL(currentBlobUrl);
      currentBlobUrl = null;
    }
    
    const trackElem = document.getElementById(TRACK_ELEM_ID);
    if (trackElem) {
      trackElem.remove();
    }

    const customSubsElem = document.getElementById(CUSTOM_SUBS_ELEM_ID);
    if (customSubsElem) {
      customSubsElem.remove();
    }
  }

  // Function to convert SRT to WebVTT format (simplified)
  function convertSRTToWebVTT(srtContent: string): string {
    const lines = srtContent.split('\n');
    let webvttContent = 'WEBVTT\n\n';
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      // Skip empty lines and numbers
      if (!line || /^\d+$/.test(line)) continue;
      
      // Check if line contains timestamp
      if (line.includes('-->')) {
        // Convert timestamps: , -> .
        const timestamps = line.replace(/,/g, '.');
        webvttContent += timestamps + '\n';
        
        // Add subtitle text until next empty line
        while (++i < lines.length && lines[i].trim()) {
          webvttContent += lines[i].trim() + '\n';
        }
        webvttContent += '\n';
      }
    }
    
    return webvttContent;
  }

  // Function to create loading WebVTT for visual feedback
  function createLoadingWebVTT(): string {
    return `WEBVTT

00:00:00.000 --> 01:00:00.000
Loading smart subtitles...`;
  }

  // Function to create loading WebVTT blob
  function createLoadingWebVTTBlob(): Blob {
    const webvttContent = createLoadingWebVTT();
    return new Blob([webvttContent], { type: 'text/vtt' });
  }

  // Main reconciliation function (Subadub-style conditional injection - Solution C Enhanced)
  function reconcileSubtitleInjection(): void {
    const videoElem = document.querySelector('video');
    
    // Only inject when we have proper conditions (like Subadub)
    if (videoElem && currentMovieId) {
      // Check if we have cached tracks for this movie
      const cachedTracks = trackListCache.get(currentMovieId);
      
      if (cachedTracks && cachedTracks.length > 0) {
        // Use the first available track for basic subtitle injection
        const firstTrack = cachedTracks[0];
        const cacheKey = `${currentMovieId}/${firstTrack.id}`;
        
        if (webvttCache.has(cacheKey)) {
          const cachedBlob = webvttCache.get(cacheKey)!;
          console.log('Netflix Subtitle Downloader: Using cached subtitle blob for injection');
          
          // More robust comparison: check if we already have a blob with the same content
          const shouldUpdate = currentBlobUrl === null; // Only update if no current blob
          
          if (shouldUpdate) {
            console.log('Netflix Subtitle Downloader: Updating subtitle injection - new blob detected');
            
            addTrackElem(videoElem, cachedBlob, firstTrack.language);
          } else {
            console.log('Netflix Subtitle Downloader: No update needed - same blob content');
          }
        } else {
          console.log('Netflix Subtitle Downloader: No cached blob available for injection');
        }
      } else {
        console.log('Netflix Subtitle Downloader: No cached tracks available for injection');
      }
    } else {
      console.log('Netflix Subtitle Downloader: No video element or movie ID available for injection');
      
      // Clean up when no video or movie ID
      if (currentBlobUrl) {
        console.log('Netflix Subtitle Downloader: Cleaning up subtitle injection');
        removeTrackElem();
      }
    }
  }

  // SMART SUBTITLES FUNCTIONS

  // Function to process subtitles with Railway API
  async function processSmartSubtitles(settings: SmartSubtitlesSettings): Promise<void> {
    console.log('Smart Netflix Subtitles: Processing subtitles with settings:', settings);
    
    if (!currentMovieId) {
      throw new Error('No current movie ID available');
    }

    // Check if we already have processed subtitles for this movie
    const cacheKey = `${currentMovieId}_${settings.targetLanguage}_${settings.vocabularyLevel}`;
    if (processedSubtitlesCache.has(cacheKey)) {
      console.log('Smart Netflix Subtitles: Using cached processed subtitles');
      const cachedWebVTT = processedSubtitlesCache.get(cacheKey)!;
      const blob = new Blob([cachedWebVTT], { type: 'text/vtt' });
      const videoElem = document.querySelector('video');
      if (videoElem) {
        addTrackElem(videoElem, blob, settings.targetLanguage);
        console.log('Smart Netflix Subtitles: Cached processed subtitles injected successfully');
      }
      return;
    }

    isProcessingSubtitles = true;
    smartSubtitlesEnabled = true;
    currentSettings = settings;
    
    console.log('Smart Netflix Subtitles: Updated state - enabled:', smartSubtitlesEnabled, 'settings:', currentSettings);

    try {
      // Get available tracks for current movie
      const tracks = trackListCache.get(currentMovieId);
      if (!tracks || tracks.length === 0) {
        throw new Error('No subtitle tracks available');
      }

      // Find target and native language tracks
      const targetTrack = tracks.find(track => track.language === settings.targetLanguage);
      const nativeTrack = tracks.find(track => track.language === settings.nativeLanguage);

      if (!targetTrack) {
        throw new Error(`Target language ${settings.targetLanguage} not available`);
      }
      if (!nativeTrack) {
        throw new Error(`Native language ${settings.nativeLanguage} not available`);
      }

      // Show loading message with intelligent delay (Option 1)
      // Wait for tracks to stabilize before showing loading message
      setTimeout(() => {
        const videoElem = document.querySelector('video');
        if (videoElem) {
          const loadingBlob = createLoadingWebVTTBlob();
          addTrackElem(videoElem, loadingBlob, settings.targetLanguage, true);
          console.log('Smart Netflix Subtitles: Loading message displayed (with delay)');
        }
      }, 1500); // 1.5 second delay to allow tracks to stabilize

      console.log('Smart Netflix Subtitles: Found tracks:', { targetTrack, nativeTrack });

      // Download and convert subtitles to SRT
      const targetSrt = await downloadAndConvertToSRT(targetTrack);
      const nativeSrt = await downloadAndConvertToSRT(nativeTrack);

      // Process with Railway API (frequency lists are now handled server-side)
      console.log('Smart Netflix Subtitles: Sending to Railway API...');
      const apiResponse = await railwayAPIClient.processSubtitles(
        targetSrt,
        nativeSrt,
        settings
      );

      if (apiResponse.success && apiResponse.output_srt) {
        console.log('Smart Netflix Subtitles: API processing successful');
        
        // Cache the processed subtitles
        const cacheKey = `${currentMovieId}-${settings.targetLanguage}-${settings.nativeLanguage}-${settings.vocabularyLevel}`;
        processedSubtitlesCache.set(cacheKey, apiResponse.output_srt);

        // Convert processed SRT to WebVTT and inject
        const processedWebVTT = convertSRTToWebVTT(apiResponse.output_srt);
        const processedBlob = new Blob([processedWebVTT], { type: 'text/vtt' });
        
        const videoElem = document.querySelector('video');
        if (videoElem) {
          addTrackElem(videoElem, processedBlob, settings.targetLanguage);
          console.log('Smart Netflix Subtitles: Processed subtitles injected successfully - loading message replaced');
        }

        // Notify content script of success
        notifyContentScript({
          type: 'NETFLIX_SUBTITLES',
          action: 'SMART_SUBTITLES_SUCCESS',
          data: {
            stats: apiResponse.stats,
            message: 'Smart subtitles processed successfully'
          }
        });

      } else {
        throw new Error(apiResponse.error || 'API processing failed');
      }

    } catch (error) {
      console.error('Smart Netflix Subtitles: Processing failed:', error);
      
      // Fallback to original subtitles
      console.log('Smart Netflix Subtitles: Falling back to original subtitles');
      smartSubtitlesEnabled = false;
      
      // Re-inject original subtitles
      const videoElem = document.querySelector('video');
      if (videoElem && currentMovieId) {
        const tracks = trackListCache.get(currentMovieId);
        if (tracks && tracks.length > 0) {
          const originalTrack = tracks.find(track => track.language === settings.targetLanguage);
          if (originalTrack) {
            const originalSrt = await downloadAndConvertToSRT(originalTrack);
            const originalWebVTT = convertSRTToWebVTT(originalSrt);
            const originalBlob = new Blob([originalWebVTT], { type: 'text/vtt' });
            addTrackElem(videoElem, originalBlob, settings.targetLanguage);
            console.log('Smart Netflix Subtitles: Original subtitles restored - loading message replaced');
          }
        }
      }

      // Notify content script of error
      notifyContentScript({
        type: 'NETFLIX_SUBTITLES',
        action: 'SMART_SUBTITLES_ERROR',
        data: {
          error: error instanceof Error ? error.message : 'Unknown error',
          message: 'Falling back to original subtitles'
        }
      });

    } finally {
      isProcessingSubtitles = false;
    }
  }

  // Function to download and convert subtitle to SRT
  async function downloadAndConvertToSRT(track: SubtitleTrack): Promise<string> {
    const cacheKey = currentMovieId + '/' + track.id;
    
    // Check if we have cached WebVTT data
    if (!webvttCache.has(cacheKey)) {
      console.log('Smart Netflix Subtitles: Fetching WebVTT from:', track.bestUrl);
      
      const response = await fetch(track.bestUrl);
      if (!response.ok) {
        throw new Error('Failed to fetch WebVTT file');
      }
      
      const blob = await response.blob();
      webvttCache.set(cacheKey, blob);
    }

    const webvttBlob = webvttCache.get(cacheKey)!;
    return await convertWebVTTToSRTUsingTextTrack(webvttBlob);
  }

  // Note: Frequency lists are now handled server-side by Railway API

  // Function to handle messages from content script
  function handleContentScriptMessage(event: MessageEvent): void {
    if (event.data.type === 'NETFLIX_SUBTITLES_REQUEST') {
      console.log('Netflix Subtitle Downloader: Received request from content script:', event.data);
      
      switch (event.data.action) {
        case 'GET_TRACKS':
          if (currentMovieId && trackListCache.has(currentMovieId)) {
            notifyContentScript({
              type: 'NETFLIX_SUBTITLES',
              action: 'TRACKS_AVAILABLE',
              data: {
                movieId: currentMovieId,
                tracks: trackListCache.get(currentMovieId)!
              }
            });
          } else {
            notifyContentScript({
              type: 'NETFLIX_SUBTITLES',
              action: 'NO_TRACKS',
              data: { message: 'No tracks available' }
            });
          }
          break;
          
        case 'DOWNLOAD_SUBTITLE':
          downloadSubtitle(event.data.data.trackId)
            .then(filename => {
              notifyContentScript({
                type: 'NETFLIX_SUBTITLES',
                action: 'DOWNLOAD_SUCCESS',
                data: { filename: filename }
              });
            })
            .catch(error => {
              console.error('Netflix Subtitle Downloader: Download error:', error);
              notifyContentScript({
                type: 'NETFLIX_SUBTITLES',
                action: 'DOWNLOAD_ERROR',
                data: { error: error instanceof Error ? error.message : 'Unknown error' }
              });
            });
          break;

        case 'processSmartSubtitles':
          if (event.data.settings) {
            processSmartSubtitles(event.data.settings)
              .then(() => {
                console.log('Smart Netflix Subtitles: Processing completed successfully');
              })
              .catch(error => {
                console.error('Smart Netflix Subtitles: Processing failed:', error);
              });
          } else {
            console.error('Smart Netflix Subtitles: No settings provided');
            notifyContentScript({
              type: 'NETFLIX_SUBTITLES',
              action: 'SMART_SUBTITLES_ERROR',
              data: { error: 'No settings provided' }
            });
          }
          break;
      }
    }
  }

  // IMMEDIATE JSON HIJACKING - Start capturing ALL JSON traffic from the beginning
  console.log('Netflix Subtitle Downloader: Starting JSON hijacking immediately');
  
  const originalStringify = JSON.stringify;
  JSON.stringify = function(value: any): string {
    // Inject WebVTT format into Netflix API requests
    const prop = findSubtitlesProperty(value);
    if (prop) {
      console.log('Netflix Subtitle Downloader: Injecting WebVTT format into request');
      prop.unshift(WEBVTT_FMT);
    }
    return originalStringify.apply(this, arguments as any);
  };

  const originalParse = JSON.parse;
  JSON.parse = function(): any {
    const value = originalParse.apply(this, arguments as any);
    
    // Capture subtitle data from Netflix API responses
    if (value && value.result && value.result.movieId && value.result.timedtexttracks) {
      console.log('Netflix Subtitle Downloader: Captured Netflix API response');
      extractMovieTextTracks(value.result);
    }
    
    // Also check for alternative response formats
    if (value && value.result && value.result.result && value.result.result.timedtexttracks) {
      console.log('Netflix Subtitle Downloader: Captured alternative Netflix API response');
      extractMovieTextTracks(value.result.result);
    }
    
    // Check for movies object format
    if (value && value.result && value.result.movies) {
      for (const movieId in value.result.movies) {
        const movie = value.result.movies[movieId];
        if (movie && movie.timedtexttracks) {
          console.log('Netflix Subtitle Downloader: Captured movies object response');
          extractMovieTextTracks(movie);
        }
      }
    }
    
    return value;
  };

  // Set up message listener
  window.addEventListener('message', handleContentScriptMessage);

  // Polling-based movie ID detection (inspired by Subadub)
  const POLL_INTERVAL_MS = 500;
  let lastKnownMovieId: number | null = null;
  
  setInterval(function() {
    let videoId: number | null = null;
    const videoIdElem = document.querySelector('*[data-videoid]');
    if (videoIdElem) {
      const dsetIdStr = videoIdElem.getAttribute('data-videoid');
      if (dsetIdStr) {
        videoId = +dsetIdStr;
      }
    }

    // Check if movie ID has changed
    if (videoId !== lastKnownMovieId) {
      console.log('Netflix Subtitle Downloader: Movie ID changed from', lastKnownMovieId, 'to', videoId);
      
      // Reset state when movie changes (key fix for auto-processing)
      lastKnownMovieId = videoId;
      currentMovieId = videoId;
      selectedTrackId = null;
      isProcessingSubtitles = false; // ← CRITICAL: Reset processing state
      
      // Clear processed subtitles cache for new movie
      processedSubtitlesCache.clear();
      
      // Reset smart subtitles state to force fresh state request
      smartSubtitlesEnabled = false;
      currentSettings = null;
      
      // Reconcile subtitle injection
      reconcileSubtitleInjection();
    }
  }, POLL_INTERVAL_MS);

  // Initial setup - check for existing video elements
  reconcileSubtitleInjection();
  
  console.log('Netflix Subtitle Downloader: Page script initialized - JSON hijacking and subtitle injection active (event-driven)');
})();
