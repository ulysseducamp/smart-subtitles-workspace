'use client'

import { usePathname } from 'next/navigation'
import { OnboardingProvider } from '@/contexts/OnboardingContext'
import { BackButton } from '@/components/BackButton'
import { FeedbackBanner } from '@/components/FeedbackBanner'
import { Progress } from '@/components/ui/progress'

// Map pathname to progress percentage (~7% increments for uniform progression)
function getProgressPercentage(pathname: string): number {
  const progressMap: Record<string, number> = {
    '/onboarding/explanation-1': 7,
    '/onboarding/explanation-2': 14,
    '/onboarding/explanation-3': 21,
    '/onboarding/explanation-4': 28,
    '/onboarding/comparison': 35,
    '/onboarding/target-language': 42,
    '/onboarding/native-language': 49,
    '/onboarding/vocab-test-intro': 56,
    '/onboarding/vocab-test-explanation': 63,
    '/onboarding/vocab-test': 70,
    '/onboarding/results': 77,
    '/onboarding/vocab-benefits': 84,
    '/onboarding/auth': 95, // Almost full - last onboarding step
  }

  return progressMap[pathname] ?? 0
}

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const progress = getProgressPercentage(pathname)

  // Hide progress bar on pricing and complete pages
  const hideProgressBar = [
    '/onboarding/pricing-intro',
    '/onboarding/pricing-details',
    '/onboarding/complete',
  ].includes(pathname)

  return (
    <OnboardingProvider>
      <div className="min-h-screen flex flex-col pb-20">
        {/* Progress bar with back button - hidden on pricing/complete pages */}
        {!hideProgressBar && (
          <div className="sticky top-0 bg-background z-10 border-b">
            <div className="max-w-2xl mx-auto w-full p-4">
              <div className="flex items-center gap-2">
                <BackButton />
                <Progress value={progress} className="flex-1" />
              </div>
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
    </OnboardingProvider>
  )
}
