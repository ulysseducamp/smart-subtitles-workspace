/**
 * Background Service Worker for Smart Netflix Subtitles
 * Handles extension installation and opens webapp onboarding
 */

// Open onboarding webapp on first install
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    // Open onboarding in new tab
    chrome.tabs.create({
      url: 'http://localhost:5173/onboarding' // Local dev (will be changed to production URL later)
    });
  }
});

// Log background script is loaded
console.log('Smart Netflix Subtitles: Background service worker loaded');
