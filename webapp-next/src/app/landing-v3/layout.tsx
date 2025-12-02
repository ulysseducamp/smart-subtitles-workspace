'use client'

import { usePathname } from 'next/navigation'
import { LandingV3Provider } from '@/contexts/LandingV3Context'
import { ProgressBarWithBack } from '@/components/ProgressBarWithBack'
import { FeedbackBanner } from '@/components/FeedbackBanner'

// Map pathname to progress percentage (Part 1: "How it works" - écrans 1-17)
function getDiscoveryProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing-v3': 0,
    '/landing-v3/target-language': 10,
    '/landing-v3/native-language': 20,
    '/landing-v3/magic': 30,
    '/landing-v3/vocab-level': 35,
    '/landing-v3/frequency-list': 40,
    '/landing-v3/studies': 45,
    '/landing-v3/belief': 50,
    '/landing-v3/level-question': 55,
    // Vocab test intro/test/results handled by setup layout (60-75%)
    '/landing-v3/chrome-extension': 80,
    '/landing-v3/explanation-1': 85,
    '/landing-v3/explanation-2': 90,
    '/landing-v3/explanation-3': 92,
    '/landing-v3/automatic-system': 95,
    // reach-fluency has no progress bar (transition screen)
    // Note: /landing-v3/setup/* routes have their own layout with "How it works" progression
  }
  return progressMap[pathname] ?? 0
}

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  // Don't show progress bar on /landing-v3/setup/* routes (they have their own layout)
  const isSetupRoute = pathname.startsWith('/landing-v3/setup')

  if (isSetupRoute) {
    // Setup routes have their own layout (with FeedbackBanner in setup/layout.tsx)
    return <LandingV3Provider>{children}</LandingV3Provider>
  }

  // Don't show progress bar on first landing page (user hasn't started yet)
  const isLandingPage = pathname === '/landing-v3'

  // reach-fluency is transition screen - no progress bar
  const isTransitionScreen = pathname === '/landing-v3/reach-fluency'

  if (isLandingPage || isTransitionScreen) {
    return (
      <LandingV3Provider>
        <div className="min-h-screen flex flex-col pb-20">
          {children}
          <FeedbackBanner />
        </div>
      </LandingV3Provider>
    )
  }

  const progress = getDiscoveryProgress(pathname)

  return (
    <LandingV3Provider>
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
    </LandingV3Provider>
  )
}
