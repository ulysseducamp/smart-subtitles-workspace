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

// Storage keys for chrome.storage.local
const STORAGE_KEYS = {
  SMART_SUBTITLES_ENABLED: 'smartSubtitlesEnabled',
  TARGET_LANGUAGE: 'targetLanguage',
  NATIVE_LANGUAGE: 'nativeLanguage',
  VOCABULARY_LEVEL: 'vocabularyLevel'
} as const;

// Supported languages mapping (Netflix code -> DeepL code)
// 13 safe languages (no RTL/Chinese/Next-gen)
const SUPPORTED_NATIVE_LANGUAGES: Record<string, string> = {
  'en': 'English',
  'fr': 'French',
  'es': 'Spanish',
  'de': 'German',
  'it': 'Italian',
  'pt': 'Portuguese',
  'pt-BR': 'Portuguese (Brazil)',
  'pl': 'Polish',
  'nl': 'Dutch',
  'sv': 'Swedish',
  'da': 'Danish',
  'cs': 'Czech',
  'ja': 'Japanese',
  'ko': 'Korean'
};

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

// Function to save settings to chrome.storage.local
async function saveSettings(): Promise<void> {
  try {
    const settings = {
      [STORAGE_KEYS.SMART_SUBTITLES_ENABLED]: currentSettings.enabled,
      [STORAGE_KEYS.TARGET_LANGUAGE]: currentSettings.targetLanguage,
      [STORAGE_KEYS.NATIVE_LANGUAGE]: currentSettings.nativeLanguage,
      [STORAGE_KEYS.VOCABULARY_LEVEL]: currentSettings.vocabularyLevel
    };
    
    await chrome.storage.local.set(settings);
    console.log('Smart Netflix Subtitles: Settings saved to storage:', settings);
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error saving settings:', error);
  }
}

// Function to load settings from chrome.storage.local
async function loadSettings(): Promise<void> {
  try {
    const result = await chrome.storage.local.get([
      STORAGE_KEYS.SMART_SUBTITLES_ENABLED,
      STORAGE_KEYS.TARGET_LANGUAGE,
      STORAGE_KEYS.NATIVE_LANGUAGE,
      STORAGE_KEYS.VOCABULARY_LEVEL
    ]);
    
    console.log('Smart Netflix Subtitles: Loaded settings from storage:', result);
    
    // Update current settings with loaded values (with defaults)
    const isFirstLaunch = !result[STORAGE_KEYS.SMART_SUBTITLES_ENABLED] && 
                         !result[STORAGE_KEYS.TARGET_LANGUAGE] && 
                         !result[STORAGE_KEYS.NATIVE_LANGUAGE] && 
                         !result[STORAGE_KEYS.VOCABULARY_LEVEL];
    
    if (isFirstLaunch) {
      console.log('Smart Netflix Subtitles: First launch detected - using default disabled state');
    }
    
    currentSettings.enabled = result[STORAGE_KEYS.SMART_SUBTITLES_ENABLED] || false;
    currentSettings.targetLanguage = result[STORAGE_KEYS.TARGET_LANGUAGE] || '';
    currentSettings.nativeLanguage = result[STORAGE_KEYS.NATIVE_LANGUAGE] || '';
    currentSettings.vocabularyLevel = result[STORAGE_KEYS.VOCABULARY_LEVEL] || 0;
    
    // Update UI with loaded settings
    smartSubtitlesToggle.checked = currentSettings.enabled;
    targetLanguageSelect.value = currentSettings.targetLanguage;
    nativeLanguageSelect.value = currentSettings.nativeLanguage;
    vocabularyLevelSelect.value = currentSettings.vocabularyLevel.toString();
    
    console.log('Smart Netflix Subtitles: Settings loaded and UI updated:', currentSettings);
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error loading settings:', error);
    // Keep default values if loading fails
  }
}

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

  // Save settings when toggle changes
  saveSettings();

  if (!isEnabled) {
    clearStatus();
    hideLoading();
  }
}

// Function to load available native languages from Netflix
async function loadAvailableNativeLanguages(): Promise<void> {
  try {
    // Get the current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true }) as ChromeTab[];

    if (!tab) {
      console.log('Smart Netflix Subtitles: No active tab found for language detection');
      return;
    }

    // Check if on Netflix page
    if (!tab.url?.includes('netflix.com')) {
      console.log('Smart Netflix Subtitles: Not on Netflix page, using default languages');
      populateNativeLanguageDropdown([]);
      return;
    }

    // Request available subtitle tracks from content script
    const response = await chrome.tabs.sendMessage(tab.id!, {
      action: 'getAvailableSubtitleTracks'
    } as ChromeMessage) as ChromeResponse;

    if (response && response.success && response.availableLanguages) {
      populateNativeLanguageDropdown(response.availableLanguages);
    } else {
      console.log('Smart Netflix Subtitles: No subtitle tracks found, using default languages');
      populateNativeLanguageDropdown([]);
    }
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error loading available languages:', error);
    populateNativeLanguageDropdown([]);
  }
}

// Function to populate native language dropdown
function populateNativeLanguageDropdown(availableLanguages: string[]): void {
  // Clear existing options except the first one
  nativeLanguageSelect.innerHTML = '<option value="">Select a language</option>';

  // Get languages that are both available on Netflix and supported by extension
  const supportedAndAvailable: Array<{code: string, name: string, available: boolean}> = [];

  // Add all supported languages, mark availability
  Object.keys(SUPPORTED_NATIVE_LANGUAGES).forEach(code => {
    const isAvailable = availableLanguages.includes(code);
    supportedAndAvailable.push({
      code,
      name: SUPPORTED_NATIVE_LANGUAGES[code],
      available: isAvailable
    });
  });

  // Sort by name for better UX
  supportedAndAvailable.sort((a, b) => a.name.localeCompare(b.name));

  // Add options to dropdown
  supportedAndAvailable.forEach(lang => {
    const option = document.createElement('option');
    option.value = lang.code;
    option.textContent = lang.available ? lang.name : `${lang.name} (Undetected)`;
    option.disabled = !lang.available;
    if (!lang.available) {
      option.style.color = '#999';
      option.style.fontStyle = 'italic';
    }
    nativeLanguageSelect.appendChild(option);
  });
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
  
  // Save settings when language changes
  saveSettings();
  
  updateProcessButton();
  
  // Clear any previous validation errors
  if (currentSettings.targetLanguage && currentSettings.nativeLanguage) {
    clearStatus();
  }
}

// Function to handle vocabulary level change
function handleVocabularyLevelChange(): void {
  currentSettings.vocabularyLevel = parseInt(vocabularyLevelSelect.value) || 0;
  
  // Save settings when vocabulary level changes
  saveSettings();
  
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
async function initializePopup(): Promise<void> {
  console.log('Smart Netflix Subtitles: Initializing popup...');

  // Set initial state
  disableAllControls();
  clearStatus();
  hideLoading();

  // Load saved settings first
  await loadSettings();

  // Load available native languages from Netflix
  await loadAvailableNativeLanguages();

  // Update form state based on loaded settings
  updateFormState();

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
  
  console.log('Smart Netflix Subtitles: Popup initialized with loaded settings');
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePopup);

// Also initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializePopup);
} else {
  initializePopup();
}