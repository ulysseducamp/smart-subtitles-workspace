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
// This script handles the popup interface and communicates with the content script

import { SubtitleTrack, ChromeTab, ChromeMessage, ChromeResponse } from '../types/netflix';

console.log('Netflix Subtitle Downloader: Popup script loaded');

// Get DOM elements
const subtitleSelect = document.getElementById('subtitle-select') as HTMLSelectElement;
const downloadBtn = document.getElementById('download-btn') as HTMLButtonElement;
const statusMessage = document.getElementById('status-message') as HTMLDivElement;

// Function to show status message
function showStatus(message: string, type: 'info' | 'error' | 'success' = 'info'): void {
  statusMessage.textContent = message;
  statusMessage.className = `status ${type}`;
  console.log('Netflix Subtitle Downloader: Status:', message);
}

// Function to clear status message
function clearStatus(): void {
  statusMessage.textContent = '';
  statusMessage.className = 'status';
}

// Function to disable all controls
function disableControls(): void {
  subtitleSelect.disabled = true;
  downloadBtn.disabled = true;
}

// Function to enable controls (for when we have subtitle data)
function enableControls(): void {
  subtitleSelect.disabled = false;
  downloadBtn.disabled = false;
}

// Function to populate subtitle dropdown
function populateSubtitleDropdown(tracks: SubtitleTrack[]): void {
  console.log('Netflix Subtitle Downloader: Populating dropdown with tracks:', tracks);
  
  // Clear existing options
  subtitleSelect.innerHTML = '';
  
  if (!tracks || tracks.length === 0) {
    subtitleSelect.innerHTML = '<option value="">No subtitles available</option>';
    disableControls();
    return;
  }
  
  // Add default option
  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.textContent = 'Select a subtitle...';
  subtitleSelect.appendChild(defaultOption);
  
  // Add track options
  tracks.forEach(track => {
    const option = document.createElement('option');
    option.value = track.id;
    option.textContent = track.languageDescription + (track.isClosedCaptions ? ' [CC]' : '');
    subtitleSelect.appendChild(option);
  });
  
  // Enable controls
  enableControls();
  console.log('Netflix Subtitle Downloader: Dropdown populated with', tracks.length, 'tracks');
}

// Function to load available subtitles
async function loadSubtitles(): Promise<void> {
  console.log('Netflix Subtitle Downloader: Loading available subtitles...');
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      showStatus('No active tab found', 'error');
      return;
    }
    
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'getSubtitles'
    } as ChromeMessage) as ChromeResponse;
    
    console.log('Netflix Subtitle Downloader: Subtitles response:', response);
    
    if (response && response.success) {
      const tracks = response.tracks || [];
      populateSubtitleDropdown(tracks);
      
      if (tracks.length > 0) {
        showStatus(`Found ${tracks.length} subtitle track(s)`, 'success');
      } else {
        showStatus('No subtitle tracks found', 'info');
      }
    } else {
      showStatus('Error loading subtitles', 'error');
      populateSubtitleDropdown([]);
    }
    
  } catch (error) {
    console.error('Netflix Subtitle Downloader: Error loading subtitles:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    showStatus('Error loading subtitles: ' + errorMessage, 'error');
    populateSubtitleDropdown([]);
  }
}

// Function to check if we're on a Netflix episode page
async function checkNetflixPage(): Promise<void> {
  console.log('Netflix Subtitle Downloader: Checking if on Netflix episode page...');
  
  try {
    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      showStatus('No active tab found', 'error');
      return;
    }
    
    console.log('Netflix Subtitle Downloader: Active tab URL:', tab.url);
    
    // Check if we're on a Netflix page
    if (!tab.url || !tab.url.includes('netflix.com')) {
      showStatus('Not on Netflix', 'error');
      disableControls();
      return;
    }
    
    // Send message to content script to check if it's an episode page
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'checkNetflixPage'
    } as ChromeMessage) as ChromeResponse;
    
    console.log('Netflix Subtitle Downloader: Content script response:', response);
    
    if (response && response.success) {
      if (response.isNetflixEpisode) {
        showStatus(`Found: ${response.title}`, 'success');
        // Load available subtitles
        await loadSubtitles();
      } else {
        showStatus(response.message || 'Not on Netflix episode page', 'error');
        disableControls();
      }
    } else {
      showStatus('Error checking Netflix page', 'error');
      disableControls();
    }
    
  } catch (error) {
    console.error('Netflix Subtitle Downloader: Error checking Netflix page:', error);
    
    // Check if the error is because content script isn't loaded
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    if (errorMessage.includes('Could not establish connection')) {
      showStatus('Please refresh the Netflix page and try again', 'error');
    } else {
      showStatus('Error: ' + errorMessage, 'error');
    }
    
    disableControls();
  }
}

// Function to handle download button click
async function handleDownloadClick(): Promise<void> {
  console.log('Netflix Subtitle Downloader: Download button clicked');
  
  const selectedValue = subtitleSelect.value;
  if (!selectedValue) {
    showStatus('Please select a subtitle first', 'error');
    return;
  }
  
  console.log('Netflix Subtitle Downloader: Downloading subtitle track:', selectedValue);
  showStatus('Downloading subtitle...', 'info');
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      showStatus('No active tab found', 'error');
      return;
    }
    
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'downloadSubtitle',
      trackId: selectedValue
    } as ChromeMessage) as ChromeResponse;
    
    console.log('Netflix Subtitle Downloader: Download response:', response);
    
    if (response && response.success) {
      showStatus('Download started!', 'success');
    } else {
      showStatus('Error starting download', 'error');
    }
    
  } catch (error) {
    console.error('Netflix Subtitle Downloader: Error downloading subtitle:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    showStatus('Error downloading subtitle: ' + errorMessage, 'error');
  }
}

// Function to initialize the popup
function initializePopup(): void {
  console.log('Netflix Subtitle Downloader: Initializing popup...');
  
  // Set initial state
  disableControls();
  clearStatus();
  
  // Check Netflix page when popup opens
  checkNetflixPage();
  
  // Add event listeners
  downloadBtn.addEventListener('click', handleDownloadClick);
  
  // Add change listener to subtitle select
  subtitleSelect.addEventListener('change', function() {
    const selectedValue = this.value;
    if (selectedValue) {
      downloadBtn.disabled = false;
    } else {
      downloadBtn.disabled = true;
    }
  });
  
  console.log('Netflix Subtitle Downloader: Popup initialized');
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePopup);

// Also initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializePopup);
} else {
  initializePopup();
}
