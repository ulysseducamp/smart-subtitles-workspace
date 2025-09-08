/*
 * Smart Netflix Subtitles
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

// Smart Netflix Subtitles
// This script handles the popup interface and communicates with the content script

import { SubtitleTrack, ChromeTab, ChromeMessage, ChromeResponse } from '../types/netflix';

console.log('Smart Netflix Subtitles: Popup script loaded');

// Interface for Smart Subtitles settings
interface SmartSubtitlesSettings {
  enabled: boolean;
  targetLanguage: string;
  nativeLanguage: string;
  vocabularyLevel: number;
}

// Get DOM elements
const smartSubtitlesToggle = document.getElementById('smart-subtitles-toggle') as HTMLInputElement;
const targetLanguageSelect = document.getElementById('target-language') as HTMLSelectElement;
const nativeLanguageSelect = document.getElementById('native-language') as HTMLSelectElement;
const vocabularyLevelSelect = document.getElementById('vocabulary-level') as HTMLSelectElement;
const processBtn = document.getElementById('process-btn') as HTMLButtonElement;
const statusMessage = document.getElementById('status-message') as HTMLDivElement;
const loadingIndicator = document.getElementById('loading-indicator') as HTMLDivElement;

// Legacy elements (for backward compatibility)
const subtitleSelect = document.getElementById('subtitle-select') as HTMLSelectElement;
const downloadBtn = document.getElementById('download-btn') as HTMLButtonElement;
const legacySection = document.getElementById('legacy-section') as HTMLDivElement;

// State management
let currentSettings: SmartSubtitlesSettings = {
  enabled: false,
  targetLanguage: '',
  nativeLanguage: '',
  vocabularyLevel: 0
};

let isProcessing = false;

// Function to show status message
function showStatus(message: string, type: 'info' | 'error' | 'success' = 'info'): void {
  statusMessage.textContent = message;
  statusMessage.className = `status ${type}`;
  console.log('Smart Netflix Subtitles: Status:', message);
}

// Function to clear status message
function clearStatus(): void {
  statusMessage.textContent = '';
  statusMessage.className = 'status';
}

// Function to show loading indicator
function showLoading(): void {
  loadingIndicator.style.display = 'flex';
  processBtn.disabled = true;
  processBtn.textContent = 'Processing...';
}

// Function to hide loading indicator
function hideLoading(): void {
  loadingIndicator.style.display = 'none';
  processBtn.disabled = false;
  processBtn.textContent = 'Process Subtitles';
}

// Function to validate form
function validateForm(): boolean {
  if (!currentSettings.enabled) {
    return false;
  }

  if (!currentSettings.targetLanguage) {
    showStatus('Please select a target language', 'error');
    return false;
  }

  if (!currentSettings.nativeLanguage) {
    showStatus('Please select a native language', 'error');
    return false;
  }

  if (currentSettings.targetLanguage === currentSettings.nativeLanguage) {
    showStatus('Target and native languages must be different', 'error');
    return false;
  }

  if (!currentSettings.vocabularyLevel) {
    showStatus('Please select a vocabulary level', 'error');
    return false;
  }

  return true;
}

// Function to update form state based on toggle
function updateFormState(): void {
  const isEnabled = smartSubtitlesToggle.checked;
  
  targetLanguageSelect.disabled = !isEnabled;
  nativeLanguageSelect.disabled = !isEnabled;
  vocabularyLevelSelect.disabled = !isEnabled;
  processBtn.disabled = !isEnabled || isProcessing;

  currentSettings.enabled = isEnabled;

  if (!isEnabled) {
    clearStatus();
    hideLoading();
  }
}

// Function to update process button state
function updateProcessButton(): void {
  const canProcess = currentSettings.enabled && 
                    currentSettings.targetLanguage && 
                    currentSettings.nativeLanguage && 
                    currentSettings.vocabularyLevel &&
                    currentSettings.targetLanguage !== currentSettings.nativeLanguage &&
                    !isProcessing;

  processBtn.disabled = !canProcess;
}

// Function to handle language selection changes
function handleLanguageChange(): void {
  currentSettings.targetLanguage = targetLanguageSelect.value;
  currentSettings.nativeLanguage = nativeLanguageSelect.value;
  
  updateProcessButton();
  
  // Clear any previous validation errors
  if (currentSettings.targetLanguage && currentSettings.nativeLanguage) {
    clearStatus();
  }
}

// Function to handle vocabulary level change
function handleVocabularyLevelChange(): void {
  currentSettings.vocabularyLevel = parseInt(vocabularyLevelSelect.value) || 0;
  updateProcessButton();
  
  if (currentSettings.vocabularyLevel) {
    clearStatus();
  }
}

// Function to process subtitles
async function processSubtitles(): Promise<void> {
  console.log('Smart Netflix Subtitles: Processing subtitles with settings:', currentSettings);
  
  if (!validateForm()) {
    return;
  }

  if (isProcessing) {
    return;
  }

  isProcessing = true;
  showLoading();
  clearStatus();

  try {
    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      throw new Error('No active tab found');
    }

    // Check if we're on Netflix
    if (!tab.url || !tab.url.includes('netflix.com')) {
      throw new Error('Please navigate to Netflix first');
    }

    // Send message to content script to process subtitles
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'processSmartSubtitles',
      settings: currentSettings
    } as ChromeMessage) as ChromeResponse;

    console.log('Smart Netflix Subtitles: Processing response:', response);

    if (response && response.success) {
      showStatus('Smart subtitles processed successfully!', 'success');
    } else {
      throw new Error(response?.error || 'Failed to process subtitles');
    }

  } catch (error) {
    console.error('Smart Netflix Subtitles: Error processing subtitles:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    showStatus(`Error: ${errorMessage}`, 'error');
  } finally {
    isProcessing = false;
    hideLoading();
  }
}

// Function to check if we're on a Netflix episode page
async function checkNetflixPage(): Promise<void> {
  console.log('Smart Netflix Subtitles: Checking if on Netflix episode page...');
  
  try {
    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      showStatus('No active tab found', 'error');
      return;
    }
    
    console.log('Smart Netflix Subtitles: Active tab URL:', tab.url);
    
    // Check if we're on a Netflix page
    if (!tab.url || !tab.url.includes('netflix.com')) {
      showStatus('Please navigate to Netflix to use Smart Subtitles', 'error');
      disableAllControls();
      return;
    }
    
    // Send message to content script to check if it's an episode page
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'checkNetflixPage'
    } as ChromeMessage) as ChromeResponse;
    
    console.log('Smart Netflix Subtitles: Content script response:', response);
    
    if (response && response.success) {
      if (response.isNetflixEpisode) {
        showStatus(`Ready: ${response.title}`, 'success');
        enableSmartSubtitlesControls();
      } else {
        showStatus('Please navigate to a Netflix episode or movie', 'error');
        disableAllControls();
      }
    } else {
      showStatus('Error checking Netflix page', 'error');
      disableAllControls();
    }
    
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error checking Netflix page:', error);
    
    // Check if the error is because content script isn't loaded
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    if (errorMessage.includes('Could not establish connection')) {
      showStatus('Please refresh the Netflix page and try again', 'error');
    } else {
      showStatus('Error: ' + errorMessage, 'error');
    }
    
    disableAllControls();
  }
}

// Function to enable Smart Subtitles controls
function enableSmartSubtitlesControls(): void {
  smartSubtitlesToggle.disabled = false;
  updateFormState();
}

// Function to disable all controls
function disableAllControls(): void {
  smartSubtitlesToggle.disabled = true;
  targetLanguageSelect.disabled = true;
  nativeLanguageSelect.disabled = true;
  vocabularyLevelSelect.disabled = true;
  processBtn.disabled = true;
  
  // Also disable legacy controls
  subtitleSelect.disabled = true;
  downloadBtn.disabled = true;
}

// Function to load available subtitles (legacy functionality)
async function loadSubtitles(): Promise<void> {
  console.log('Smart Netflix Subtitles: Loading available subtitles...');
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];
    
    if (!tab) {
      showStatus('No active tab found', 'error');
      return;
    }
    
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'getSubtitles'
    } as ChromeMessage) as ChromeResponse;
    
    console.log('Smart Netflix Subtitles: Subtitles response:', response);
    
    if (response && response.success) {
      const tracks = response.tracks || [];
      populateSubtitleDropdown(tracks);
      
      if (tracks.length > 0) {
        // Show legacy section if subtitles are available
        legacySection.style.display = 'block';
        showStatus(`Found ${tracks.length} subtitle track(s)`, 'success');
      } else {
        legacySection.style.display = 'none';
        showStatus('No subtitle tracks found', 'info');
      }
    } else {
      showStatus('Error loading subtitles', 'error');
      populateSubtitleDropdown([]);
    }
    
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error loading subtitles:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    showStatus('Error loading subtitles: ' + errorMessage, 'error');
    populateSubtitleDropdown([]);
  }
}

// Function to populate subtitle dropdown (legacy functionality)
function populateSubtitleDropdown(tracks: SubtitleTrack[]): void {
  console.log('Smart Netflix Subtitles: Populating dropdown with tracks:', tracks);
  
  // Clear existing options
  subtitleSelect.innerHTML = '';
  
  if (!tracks || tracks.length === 0) {
    subtitleSelect.innerHTML = '<option value="">No subtitles available</option>';
    downloadBtn.disabled = true;
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
  
  // Enable download button
  downloadBtn.disabled = false;
  console.log('Smart Netflix Subtitles: Dropdown populated with', tracks.length, 'tracks');
}

// Function to handle download button click (legacy functionality)
async function handleDownloadClick(): Promise<void> {
  console.log('Smart Netflix Subtitles: Download button clicked');
  
  const selectedValue = subtitleSelect.value;
  if (!selectedValue) {
    showStatus('Please select a subtitle first', 'error');
    return;
  }
  
  console.log('Smart Netflix Subtitles: Downloading subtitle track:', selectedValue);
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
    
    console.log('Smart Netflix Subtitles: Download response:', response);
    
    if (response && response.success) {
      showStatus('Download started!', 'success');
    } else {
      showStatus('Error starting download', 'error');
    }
    
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error downloading subtitle:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    showStatus('Error downloading subtitle: ' + errorMessage, 'error');
  }
}

// Function to initialize the popup
function initializePopup(): void {
  console.log('Smart Netflix Subtitles: Initializing popup...');
  
  // Set initial state
  disableAllControls();
  clearStatus();
  hideLoading();
  
  // Check Netflix page when popup opens
  checkNetflixPage();
  
  // Add event listeners for Smart Subtitles controls
  smartSubtitlesToggle.addEventListener('change', updateFormState);
  targetLanguageSelect.addEventListener('change', handleLanguageChange);
  nativeLanguageSelect.addEventListener('change', handleLanguageChange);
  vocabularyLevelSelect.addEventListener('change', handleVocabularyLevelChange);
  processBtn.addEventListener('click', processSubtitles);
  
  // Add event listeners for legacy controls
  downloadBtn.addEventListener('click', handleDownloadClick);
  subtitleSelect.addEventListener('change', function() {
    const selectedValue = this.value;
    downloadBtn.disabled = !selectedValue;
  });
  
  console.log('Smart Netflix Subtitles: Popup initialized');
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePopup);

// Also initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializePopup);
} else {
  initializePopup();
}