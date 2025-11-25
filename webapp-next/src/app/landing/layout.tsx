'use client'

import { usePathname } from 'next/navigation'
import { LandingProvider } from '@/contexts/LandingContext'
import { ProgressBarWithBack } from '@/components/ProgressBarWithBack'
import { FeedbackBanner } from '@/components/FeedbackBanner'

// Map pathname to progress percentage (Part 1: Discovery - 7 steps)
function getDiscoveryProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing': 0,
    '/landing/intro': 14,
    '/landing/magic': 28,
    '/landing/known-words': 42,
    '/landing/explanation-4': 56,
    '/landing/explanation-5': 70,
    '/landing/comparison': 85,
  }
  return progressMap[pathname] ?? 0
}

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  // Don't show progress bar on /landing/setup/* routes (they have their own layout)
  const isSetupRoute = pathname.startsWith('/landing/setup')

  if (isSetupRoute) {
    // Setup routes have their own layout (with FeedbackBanner in setup/layout.tsx)
    return <LandingProvider>{children}</LandingProvider>
  }

  // Don't show progress bar on first landing page (user hasn't started yet)
  const isLandingPage = pathname === '/landing'

  if (isLandingPage) {
    return (
      <LandingProvider>
        <div className="min-h-screen flex flex-col pb-20">
          {children}
          <FeedbackBanner />
        </div>
      </LandingProvider>
    )
  }

  const progress = getDiscoveryProgress(pathname)

  return (
    <LandingProvider>
      <div className="min-h-screen flex flex-col pb-20">
        {/* Progress bar with label */}
        <div className="sticky top-0 bg-background z-10 border-b">
          <div className="max-w-2xl mx-auto w-full px-4 py-3">
            <ProgressBarWithBack progress={progress} label="How it works" />
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 flex flex-col">
          {children}
        </div>

        {/* Fixed feedback banner */}
        <FeedbackBanner />
      </div>
    </LandingProvider>
  )
}
