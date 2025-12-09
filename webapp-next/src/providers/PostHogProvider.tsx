'use client'

import posthog from 'posthog-js'
import { PostHogProvider as PHProvider } from 'posthog-js/react'
import { useEffect } from 'react'

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Only initialize PostHog on the client side with valid credentials
    if (
      typeof window !== 'undefined' &&
      process.env.NEXT_PUBLIC_POSTHOG_KEY &&
      process.env.NEXT_PUBLIC_POSTHOG_HOST
    ) {
      posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
        api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
        person_profiles: 'identified_only', // Only create profiles for identified users

        // Modern pageview tracking (2025 defaults) - automatically handles $pageview and $pageleave
        defaults: '2025-11-30',

        // Session replay configuration with privacy-first approach
        session_recording: {
          maskAllInputs: true, // Mask all input fields by default
          maskTextSelector: '[data-sensitive]', // Additional sensitive elements
          recordCrossOriginIframes: false, // Don't record iframes for privacy
        },

        // Capture performance metrics
        capture_performance: true,

        // Disable in development for cleaner logs (optional)
        loaded: (posthog) => {
          if (process.env.NODE_ENV === 'development') {
            console.log('PostHog loaded successfully')
          }
        },
      })
    }
  }, [])

  // Return children directly if PostHog is not configured (fail gracefully)
  if (!process.env.NEXT_PUBLIC_POSTHOG_KEY || !process.env.NEXT_PUBLIC_POSTHOG_HOST) {
    console.warn('PostHog: Missing environment variables. Analytics disabled.')
    return <>{children}</>
  }

  return <PHProvider client={posthog}>{children}</PHProvider>
}
