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

(function initializeNetflixSubtitleExtractor() {
  console.log('Netflix Subtitle Downloader: Page script loaded - starting JSON hijacking immediately');

  // Constants from Subadub analysis
  const POLL_INTERVAL_MS = 500;
  const WEBVTT_FMT = 'webvtt-lssdh-ios8';
  
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
  const trackListCache = new Map(); // from movie ID to list of available tracks
  const webvttCache = new Map(); // from 'movieID/trackID' to blob
  let currentMovieId = null;
  let selectedTrackId = null;

  // Function to find subtitle-related properties in Netflix API objects
  function findSubtitlesProperty(obj) {
    for (let key in obj) {
      let value = obj[key];
      if (Array.isArray(value)) {
        if (key === 'profiles' || value.some(item => NETFLIX_PROFILES.includes(item))) {
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
  function extractMovieTextTracks(movieObj) {
    const movieId = movieObj.movieId;
    console.log('Netflix Subtitle Downloader: Extracting tracks for movie ID:', movieId);

    const usableTracks = [];
    
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
  }

  // Function to convert WebVTT text to plain text plus "simple" tags (allowed in SRT)
  const TAG_REGEX = RegExp('</?([^>]*)>', 'ig');
  function vttTextToSimple(s, netflixRTLFix = true) {
    let simpleText = s;

    // Strip tags except simple ones (i, u, b)
    simpleText = simpleText.replace(TAG_REGEX, function (match, p1) {
      return ['i', 'u', 'b'].includes(p1.toLowerCase()) ? match : '';
    });

    if (netflixRTLFix) {
      // Handle RTL text direction fixes
      const lines = simpleText.split('\n');
      const newLines = [];
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
  function formatTime(t) {
    const date = new Date(0, 0, 0, 0, 0, 0, t * 1000);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    const ms = date.getMilliseconds().toString().padStart(3, '0');
    return hours + ':' + minutes + ':' + seconds + ',' + ms;
  }

  // Function to convert WebVTT to SRT using browser's TextTrack API (Subadub approach)
  function convertWebVTTToSRTUsingTextTrack(webvttBlob) {
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
          const srtChunks = [];
          let idx = 1;
          
          // Use the browser's parsed cues (positioning info automatically filtered)
          for (const cue of tempTrack.track.cues) {
            const cleanedText = vttTextToSimple(cue.text, true);
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
  async function downloadSubtitle(trackId) {
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

    const webvttBlob = webvttCache.get(cacheKey);
    
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
  function notifyContentScript(message) {
    window.postMessage(message, '*');
  }

  // Function to handle messages from content script
  function handleContentScriptMessage(event) {
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
                tracks: trackListCache.get(currentMovieId)
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
          downloadSubtitle(event.data.trackId)
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
                data: { error: error.message }
              });
            });
          break;
      }
    }
  }

  // IMMEDIATE JSON HIJACKING - Start capturing ALL JSON traffic from the beginning
  console.log('Netflix Subtitle Downloader: Starting JSON hijacking immediately');
  
  const originalStringify = JSON.stringify;
  JSON.stringify = function(value) {
    // Inject WebVTT format into Netflix API requests
    let prop = findSubtitlesProperty(value);
    if (prop) {
      console.log('Netflix Subtitle Downloader: Injecting WebVTT format into request');
      prop.unshift(WEBVTT_FMT);
    }
    return originalStringify.apply(this, arguments);
  };

  const originalParse = JSON.parse;
  JSON.parse = function() {
    const value = originalParse.apply(this, arguments);
    
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

  // Poll for movie ID changes (ONLY for video changes, not for injection timing)
  function updateCurrentMovieId() {
    let videoId = null;
    const videoIdElem = document.querySelector('*[data-videoid]');
    if (videoIdElem) {
      const dsetIdStr = videoIdElem.dataset.videoid;
      if (dsetIdStr) {
        videoId = +dsetIdStr;
      }
    }

    currentMovieId = videoId;
    if (!currentMovieId) {
      selectedTrackId = null;
    }
  }

  // Initialize
  function initialize() {
    console.log('Netflix Subtitle Downloader: Initializing page script');
    
    // Set up message listener
    window.addEventListener('message', handleContentScriptMessage);
    
    // Start polling for movie ID changes (like Subadub)
    setInterval(updateCurrentMovieId, POLL_INTERVAL_MS);
    
    // Initial movie ID check
    updateCurrentMovieId();
    
    console.log('Netflix Subtitle Downloader: Page script initialized - JSON hijacking active');
  }

  // Start initialization immediately
  initialize();
})();
