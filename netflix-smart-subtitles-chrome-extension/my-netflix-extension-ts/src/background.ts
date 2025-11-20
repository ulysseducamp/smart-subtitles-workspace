/**
 * Background Service Worker for Smart Netflix Subtitles
 * Handles extension installation and opens webapp onboarding
 */

import { supabase } from './lib/supabase'

// Webapp URL (set by webpack based on environment)
const WEBAPP_URL = process.env.WEBAPP_URL || 'http://localhost:3000';

// Allowed origins for message passing (security)
const ALLOWED_ORIGINS = [
  'http://localhost:3000',                              // Local dev (Next.js)
  'https://staging-subly-extension.vercel.app',         // Staging
  'https://subly-extension.vercel.app',                 // Production
]

// Open onboarding webapp on first install
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    // Open welcome page in new tab (URL set by webpack based on build environment)
    chrome.tabs.create({
      url: `${WEBAPP_URL}/welcome`
    });
  }
});

// Listen for messages from popup (internal)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 Received internal message:', message)

  // Handle OPEN_STRIPE_PORTAL message
  if (message.type === 'OPEN_STRIPE_PORTAL' && message.userId) {
    // Make API call from background (no CORS issues)
    fetch(`${WEBAPP_URL}/api/stripe/portal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId: message.userId }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.url) {
          // Open portal in new tab
          chrome.tabs.create({ url: data.url })
          sendResponse({ success: true })
        } else {
          console.error('❌ Failed to get portal URL:', data.error)
          sendResponse({ success: false, error: data.error })
        }
      })
      .catch(error => {
        console.error('❌ Error calling portal API:', error)
        sendResponse({ success: false, error: error.message })
      })

    // Return true to indicate we'll respond asynchronously
    return true
  }

  // Unknown message type
  console.warn('⚠️ Unknown internal message type:', message.type)
  sendResponse({ success: false, error: 'Unknown message type' })
  return true
})

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

  // Handle VOCAB_LEVEL_UPDATED message
  if (message.type === 'VOCAB_LEVEL_UPDATED' && message.level && message.language) {
    console.log('📊 Vocab level updated:', message.level, message.language)

    // Update chrome.storage.local
    chrome.storage.local.set({
      vocabularyLevel: message.level,
      targetLanguage: message.language
    }, () => {
      console.log('✅ Vocab level updated in storage')
      sendResponse({ success: true })
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
