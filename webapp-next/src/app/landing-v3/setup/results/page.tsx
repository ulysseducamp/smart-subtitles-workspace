'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'
import { PartyPopper } from 'lucide-react'

export default function ResultsPage() {
  const router = useRouter()
  const { vocabLevel, targetLanguage } = useLandingV3()

  // Get language name for display
  const languageName = targetLanguage === 'French' ? 'French' : 'Brazilian Portuguese'

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Party icon */}
        <div className="flex justify-center">
          <PartyPopper className="h-16 w-16" />
        </div>

        {/* Title with dynamic number */}
        <h1 className="text-3xl font-bold">
          Congrats! You know approximately {vocabLevel} of the most used words in {languageName}
        </h1>

        {/* Explanation */}
        <p className="text-lg">
          On average, thanks to Subly, user with this level master 30 new words per episode watched.
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/chrome-extension')}
          className="w-full md:w-auto"
        >
          Discover how
        </Button>
      </div>
    </div>
  )
}
