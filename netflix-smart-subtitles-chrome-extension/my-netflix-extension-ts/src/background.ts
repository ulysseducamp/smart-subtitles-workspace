/**
 * Background Service Worker for Smart Netflix Subtitles
 * Handles extension installation and opens webapp onboarding
 */

import { supabase } from './lib/supabase'

// Allowed origins for message passing (security)
const ALLOWED_ORIGINS = [
  'http://localhost:5173', // Local dev
  'https://subly.app',     // Production
]

// Open onboarding webapp on first install
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    // Open welcome page in new tab
    chrome.tabs.create({
      url: 'http://localhost:5173/welcome' // Local dev (will be changed to production URL later)
    });
  }
});

// Listen for session sync messages from webapp
chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
  console.log('📨 Received message from webapp:', message, 'from:', sender.url)

  // SECURITY: Validate sender origin
  const senderOrigin = sender.url ? new URL(sender.url).origin : null
  if (!senderOrigin || !ALLOWED_ORIGINS.includes(senderOrigin)) {
    console.error('❌ Rejected message from unauthorized origin:', senderOrigin)
    sendResponse({ success: false, error: 'Unauthorized origin' })
    return true
  }

  // Handle SYNC_SESSION message
  if (message.type === 'SYNC_SESSION' && message.session) {
    const { access_token, refresh_token } = message.session

    // Set session in Supabase (will auto-store in chrome.storage.local via adapter)
    supabase.auth.setSession({
      access_token,
      refresh_token,
    }).then(({ data, error }) => {
      if (error) {
        console.error('❌ Failed to set session:', error)
        sendResponse({ success: false, error: error.message })
      } else {
        console.log('✅ Session synced successfully:', data.user?.email)
        sendResponse({ success: true })
      }
    })

    // Return true to indicate we'll respond asynchronously
    return true
  }

  // Unknown message type
  console.warn('⚠️ Unknown message type:', message.type)
  sendResponse({ success: false, error: 'Unknown message type' })
  return true
})

// Log background script is loaded
console.log('Smart Netflix Subtitles: Background service worker loaded');
