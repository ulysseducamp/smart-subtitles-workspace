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

console.log('Netflix Subtitle Downloader: Content script loaded');

// Subtitle data storage
let availableTracks = [];
let currentMovieId = null;

// Function to inject page script into the page context IMMEDIATELY
function injectPageScript() {
  console.log('Netflix Subtitle Downloader: Injecting page script immediately');
  
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('page-script.js');
  script.onload = function() {
    console.log('Netflix Subtitle Downloader: Page script loaded successfully');
    this.remove(); // Clean up the script tag
  };
  script.onerror = function() {
    console.error('Netflix Subtitle Downloader: Failed to load page script');
  };
  
  // Use Subadub's immediate injection approach
  document.head.insertBefore(script, document.head.firstChild);
}

// Function to get episode/movie title
function getNetflixTitle() {
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
    if (element && element.textContent.trim()) {
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
function handlePageScriptMessage(event) {
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
    }
  }
}

// Function to send message to page script
function sendMessageToPageScript(message) {
  window.postMessage({
    type: 'NETFLIX_SUBTITLES_REQUEST',
    ...message
  }, '*');
}

// Function to handle messages from popup
function handlePopupMessage(request, sender, sendResponse) {
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
      movieId: currentMovieId
    });
  } else if (request.action === 'downloadSubtitle') {
    // Request subtitle download from page script
    console.log('Netflix Subtitle Downloader: Requesting subtitle download:', request.trackId);
    sendMessageToPageScript({
      action: 'DOWNLOAD_SUBTITLE',
      trackId: request.trackId
    });
    
    sendResponse({
      success: true,
      message: 'Download request sent'
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
