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

import { NetflixSubtitle, NetflixManifest, NetflixMoviesResponse, NetflixAlternativeResponse, SubtitleTrack, ExtensionMessage } from './types/netflix';

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
  let showSubsState = true;
  let currentBlobUrl: string | null = null; // Track current blob URL for cleanup

  // SRT file content for injection (real subtitles from E06.srt)
  const SRT_CONTENT = `1
00:00:56,916 --> 00:00:59,541
O mundo era mais bonito
na sua cabeça, pai.

2
00:01:13,833 --> 00:01:17,750
CEM ANOS DE SOLIDÃO

3
00:01:28,333 --> 00:01:31,958
<i>Il avait fait le tour du monde 65 fois,</i>

4
00:01:33,250 --> 00:01:36,583
<i>enrôlé dans un équipage</i>
<i>de marins apatrides.</i>

5
00:01:37,625 --> 00:01:38,958
<i>Havia naufragado</i>

6
00:01:39,583 --> 00:01:43,250
<i>et avait dérivé pendant deux semaines</i>
<i>dans la mer du Japon.</i>

7
00:01:44,833 --> 00:01:46,833
On a perdu le navire dans une tempête.

8
00:01:47,791 --> 00:01:52,000
On est restés à la dérive
pendant des jours, moi et un autre marin,

9
00:01:53,000 --> 00:01:54,666
agrippés à une planche.

10
00:01:56,416 --> 00:01:58,083
Fui o único sobrevivente (survivant).

11
00:01:58,666 --> 00:02:01,500
Você disse que eram dois.
O que houve com o outro?

12
00:02:02,000 --> 00:02:03,791
Acabou morrendo de insolação (insolation).

13
00:02:04,291 --> 00:02:05,541
Mas salvou minha vida.

14
00:02:06,083 --> 00:02:06,958
Ele salgou

15
00:02:07,791 --> 00:02:08,625
a carne (la viande).

16
00:02:09,166 --> 00:02:10,250
Tinha um sabor (saveur)

17
00:02:10,916 --> 00:02:11,833
que era doce (sucré).

18
00:02:11,916 --> 00:02:13,458
<i>Úrsula chorava na mesa</i>

19
00:02:13,541 --> 00:02:16,708
<i>comme si elle lisait les lettres</i>
<i>qui n'étaient jamais arrivées</i>

20
00:02:17,458 --> 00:02:22,708
<i>e nas quais José Arcadio contava</i>
<i>seus feitos e desventuras…</i>

21
00:02:22,791 --> 00:02:24,916
Você sempre teve um lar (maison) aqui, filho.

22
00:02:25,666 --> 00:02:27,916
Toute cette nourriture jetée aux cochons…

23
00:02:35,166 --> 00:02:37,833
Quando você desapareceu,
fui atrás de você.

24
00:02:40,125 --> 00:02:43,583
jusqu'à ne plus trouver
aucun signe de toi nulle part.

25
00:02:44,916 --> 00:02:47,125
e eu não soube mais onde te procurar (recherche).

26
00:02:52,500 --> 00:02:53,458
Quem é você?

27
00:02:54,166 --> 00:02:55,791
Eu me chamo Pietro Crespi.

28
00:02:55,875 --> 00:02:57,166
Noivo da Rebeca.

29
00:02:59,458 --> 00:03:00,541
E você é?

30
00:03:01,125 --> 00:03:02,208
Ela é sua irmã.

31
00:03:10,791 --> 00:03:11,708
Irmãozinho.

32
00:03:14,041 --> 00:03:14,958
José Arcadio.

33
00:03:33,000 --> 00:03:34,125
Por onde andou?

34
00:03:36,541 --> 00:03:37,375
Por aí.

35
00:03:52,458 --> 00:03:54,916
Quando me casei,
me mudei pro segundo andar.

36
00:04:02,791 --> 00:04:05,625
E Arcadio dormiu aqui
até o dia em que saiu de casa.

37
00:04:06,750 --> 00:04:07,583
Arcadio?

38
00:04:08,666 --> 00:04:09,500
O seu filho.

39
00:04:13,291 --> 00:04:14,416
Eu me lembro…

40
00:04:16,208 --> 00:04:19,083
quand tu faisais le mur,
tu revenais à l'aube

41
00:04:19,166 --> 00:04:21,041
et tu me racontais tes aventures.

42
00:04:26,375 --> 00:04:28,333
E um dia decidi te perguntar:

43
00:04:30,833 --> 00:04:33,000
"O que sentia com isso tudo?"

44
00:04:36,833 --> 00:04:37,833
E você disse…

45
00:04:39,875 --> 00:04:41,583
"É como um terremoto (tremblement de terre)."

46
00:04:44,916 --> 00:04:46,625
Tinha razão. Você se lembra?

47
00:04:48,875 --> 00:04:50,666
Il suffit que toi, tu te rappelles.

48
00:04:54,541 --> 00:04:55,833
Você se casou?

49
00:04:59,875 --> 00:05:00,833
Eu me casei

50
00:05:02,041 --> 00:05:03,416
e fiquei viúvo (veuf).

51
00:05:04,208 --> 00:05:05,166
Fim de história.`;

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

  // Function to update current movie ID from DOM (event-driven)
  function updateCurrentMovieId(): void {
    let videoId: number | null = null;
    const videoIdElem = document.querySelector('*[data-videoid]');
    if (videoIdElem) {
      const dsetIdStr = videoIdElem.getAttribute('data-videoid');
      if (dsetIdStr) {
        videoId = +dsetIdStr; // Convert to number like in original JS version
      }
    }

    currentMovieId = videoId;
    if (!currentMovieId) {
      selectedTrackId = null;
    }
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
  function addTrackElem(videoElem: HTMLVideoElement, blob: Blob, srclang: string): void {
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
    customSubsElem.style.cssText = 'position: absolute; bottom: 20vh; left: 0; right: 0; color: white; font-size: 3vw; text-align: center; user-select: text; -moz-user-select: text; z-index: 100; pointer-events: none';

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

  // Function to update subtitle display visibility
  function updateSubtitleDisplay(): void {
    const subsElem = document.getElementById(CUSTOM_SUBS_ELEM_ID);
    if (subsElem) {
      if (showSubsState) {
        subsElem.style.visibility = 'visible';
      } else {
        subsElem.style.visibility = 'hidden';
      }
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

  // Function to create test WebVTT blob from SRT content
  function createTestWebVTTBlob(): Blob {
    const webvttContent = convertSRTToWebVTT(SRT_CONTENT);
    return new Blob([webvttContent], { type: 'text/vtt' });
  }

  // Main reconciliation function (Subadub-style conditional injection - Solution C Enhanced)
  function reconcileSubtitleInjection(): void {
    const videoElem = document.querySelector('video');
    
    // Only inject when we have proper conditions (like Subadub)
    if (videoElem && currentMovieId) {
      // For test implementation, use test WebVTT
      const newBlob = createTestWebVTTBlob();
      
      // More robust comparison: check if we already have a blob with the same content
      const shouldUpdate = true; // Simplified logic
      
      if (shouldUpdate) {
        console.log('Netflix Subtitle Downloader: Updating subtitle injection - new blob detected');
        
        addTrackElem(videoElem, newBlob, 'en'); // Use English as default for test
      } else {
        console.log('Netflix Subtitle Downloader: No update needed - same blob content');
      }
    } else {
      // Clean up when no video or movie ID
      if (true) { // Simplified logic
        console.log('Netflix Subtitle Downloader: Cleaning up subtitle injection');
        removeTrackElem();
      }
    }
  }

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
  
  // Set up keyboard shortcuts for subtitle control (like Subadub)
  document.body.addEventListener('keydown', function(e) {
    if ((e.keyCode === 83) && !e.altKey && !e.ctrlKey && !e.metaKey) { // unmodified S key
      console.log('Netflix Subtitle Downloader: Toggle subtitle display');
      showSubsState = !showSubsState;
      updateSubtitleDisplay();
    }
  }, false);

  // Event-driven video detection using MutationObserver
  const videoObserver = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const element = node as Element;
            // Check if the added element is a video or contains a video
            if (element.tagName === 'VIDEO' || element.querySelector('video')) {
              console.log('Netflix Subtitle Downloader: Video element detected via MutationObserver');
              updateCurrentMovieId();
              reconcileSubtitleInjection();
            }
          }
        }
      }
    }
  });

  // Start observing DOM changes for video elements
  videoObserver.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Initial setup - check for existing video elements
  updateCurrentMovieId();
  reconcileSubtitleInjection();
  
  console.log('Netflix Subtitle Downloader: Page script initialized - JSON hijacking and subtitle injection active (event-driven)');
})();
