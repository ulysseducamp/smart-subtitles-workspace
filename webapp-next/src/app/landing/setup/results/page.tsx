'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLanding } from '@/contexts/LandingContext'
import { PartyPopper } from 'lucide-react'

export default function ResultsPage() {
  const router = useRouter()
  const { vocabLevel, targetLanguage } = useLanding()

  // Get language name for display
  const languageName = targetLanguage === 'fr' ? 'French' : 'Brazilian Portuguese'

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Party icon */}
        <div className="flex justify-center">
          <PartyPopper className="h-16 w-16" />
        </div>

        {/* Title */}
        <h1 className="text-3xl font-bold">
          Congrats! you know approximately {vocabLevel} of the most used words in {languageName}
        </h1>

        {/* Explanation */}
        <p className="text-lg">
          On average, users with this level aquire 30 new words per episode.
        </p>

        <p className="text-lg">
          Which means you will double the number of words you know just by watching a few series with Subly 🤯
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/setup/finish-cta')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
