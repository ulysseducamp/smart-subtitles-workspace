'use client'

import { usePathname } from 'next/navigation'
import { ProgressBarWithBack } from '@/components/ProgressBarWithBack'
import { FeedbackBanner } from '@/components/FeedbackBanner'

// Section 1 fin: "How it works" progress (écrans 10-13: 60% → 75%)
function getHowItWorksProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing-v3/setup/vocab-intro-1': 60,
    '/landing-v3/setup/vocab-intro-2': 65,
    '/landing-v3/setup/results': 70,
    // After results, user exits /setup and goes to /landing-v3/chrome-extension (80-100% in main layout)
  }
  return progressMap[pathname] ?? 0
}

// Section 2: "Setting up Subly" progress (écrans 19-24+: 50% → 100%)
function getSettingUpProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing-v3/setup/main-struggles': 50,
    '/landing-v3/setup/you-are-in-good-hands': 60,
    '/landing-v3/setup/learning-duration': 70,
    '/landing-v3/setup/study-frequency': 80,
    '/landing-v3/setup/comparison': 85,
    '/landing-v3/setup/auth': 90,
    '/landing-v3/setup/post-auth': 93,
    '/landing-v3/setup/pricing': 96,
    '/landing-v3/setup/analyzing': 98,
    '/landing-v3/setup/results': 99,
    '/landing-v3/setup/finish-cta': 99,
    '/landing-v3/setup/complete': 100,
  }
  return progressMap[pathname] ?? 0
}

export default function SetupLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  // Écran 18: Transition "reach-fluency" - PAS de barre de progression
  const isTransition = pathname === '/landing-v3/setup/reach-fluency'

  // Vocab test - PAS de barre de progression (durée variable selon niveau)
  const isVocabTest = pathname.includes('vocab-test') && !pathname.includes('vocab-intro')

  if (isTransition || isVocabTest) {
    return (
      <div className="min-h-screen flex flex-col pb-20">
        <div className="flex-1 flex flex-col">
          {children}
        </div>
        <FeedbackBanner />
      </div>
    )
  }

  // Section 1 (écrans 10-13): Barre "How it works"
  const isSection1 = pathname.match(/vocab-intro|results/)

  if (isSection1) {
    const progress = getHowItWorksProgress(pathname)

    return (
      <div className="min-h-screen flex flex-col pb-20">
        <div className="sticky top-0 bg-background z-10 border-b">
          <div className="max-w-2xl mx-auto w-full px-4 py-3">
            <ProgressBarWithBack
              progress={progress}
              label="How it works"
              showBackButton={true}
            />
          </div>
        </div>
        <div className="flex-1 flex flex-col">
          {children}
        </div>
        <FeedbackBanner />
      </div>
    )
  }

  // Section 2 (écrans 19-24+): Barre "Setting up Subly" (commence à 50%)
  const progress = getSettingUpProgress(pathname)
  const isComplete = pathname.includes('/complete')

  return (
    <div className="min-h-screen flex flex-col pb-20">
      {/* Hide progress bar on complete screen */}
      {!isComplete && (
        <div className="sticky top-0 bg-background z-10 border-b">
          <div className="max-w-2xl mx-auto w-full px-4 py-3">
            <ProgressBarWithBack
              progress={progress}
              label="Setting up Subly"
            />
          </div>
        </div>
      )}
      <div className="flex-1 flex flex-col">
        {children}
      </div>
      <FeedbackBanner />
    </div>
  )
}
