'use client'

import { usePathname } from 'next/navigation'
import { ProgressBarWithBack } from '@/components/ProgressBarWithBack'
import { FeedbackBanner } from '@/components/FeedbackBanner'

// Map pathname to progress percentage (Part 2: Setup - ~13 steps)
function getSetupProgress(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/landing/setup/vocab-intro': 7,
    '/landing/setup/target-language': 14,
    '/landing/setup/explanation-1': 21,
    '/landing/setup/explanation-2': 28,
    '/landing/setup/vocab-test': 35,      // Frozen during test
    '/landing/setup/analyzing': 42,
    '/landing/setup/results': 49,
    '/landing/setup/finish-cta': 56,
    '/landing/setup/native-language': 63,
    '/landing/setup/auth': 70,
    '/landing/setup/post-auth': 77,
    '/landing/setup/reminder': 84,
    '/landing/setup/pricing': 91,
    '/landing/setup/complete': 100,
  }
  return progressMap[pathname] ?? 0
}

export default function SetupLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const progress = getSetupProgress(pathname)

  // Hide entire progress bar during vocab test, vocab-intro, and complete (setup finished)
  const isVocabTest = pathname.includes('vocab-test') && !pathname.includes('results')
  const isVocabIntro = pathname.includes('vocab-intro')
  const isComplete = pathname.includes('/complete')
  const hideProgressBar = isVocabTest || isVocabIntro || isComplete
  const showBackButton = !isVocabTest

  return (
    <div className="min-h-screen flex flex-col pb-20">
      {/* Progress bar with label - hidden during vocab test, vocab-intro, and complete */}
      {!hideProgressBar && (
        <div className="sticky top-0 bg-background z-10 border-b">
          <div className="max-w-2xl mx-auto w-full px-4 py-3">
            <ProgressBarWithBack
              progress={progress}
              label="Setting Up Subly"
              showBackButton={showBackButton}
            />
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {children}
      </div>

      {/* Fixed feedback banner */}
      <FeedbackBanner />
    </div>
  )
}
