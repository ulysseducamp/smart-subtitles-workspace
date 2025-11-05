import type { Session } from '@supabase/supabase-js'

const EXTENSION_ID = 'lhkamocmjgjikhmfiogfdjhlhffoaaek'

/**
 * Syncs the Supabase session to the Chrome extension
 * This allows the extension to access user settings from Supabase
 *
 * CRITICAL: Must be called on SIGNED_IN and TOKEN_REFRESHED events
 * to prevent extension from using stale refresh tokens
 */
export async function syncSessionToExtension(session: Session | null) {
  if (!session) {
    console.log('⏭️ No session to sync to extension')
    return
  }

  // Check if chrome.runtime is available
  if (typeof chrome === 'undefined' || !chrome.runtime) {
    console.warn('⚠️ Chrome runtime not available - cannot sync to extension')
    return
  }

  try {
    console.log('📤 Sending session to extension...')

    // Use chrome.runtime.sendMessage with extension ID (works from web pages)
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Extension sync timeout (2s) - extension may not be installed'))
      }, 2000)

      chrome.runtime.sendMessage(
        EXTENSION_ID,
        {
          type: 'SYNC_SESSION',
          session: {
            access_token: session.access_token,
            refresh_token: session.refresh_token,
          },
        },
        (response) => {
          clearTimeout(timeout)
          if (chrome.runtime.lastError) {
            reject(new Error(chrome.runtime.lastError.message))
          } else {
            resolve(response)
          }
        }
      )
    })

    console.log('✅ Session synced to extension successfully')
  } catch (error) {
    // Non-blocking error - extension might not be installed
    console.warn('⚠️ Could not sync session to extension:', error)
    // Don't throw - this is optional functionality
  }
}
