'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLanding } from '@/contexts/LandingContext'

export default function Explanation1Page() {
  const router = useRouter()
  const { targetLanguage } = useLanding()

  // Get language name for display
  const languageName = targetLanguage === 'fr' ? 'French' : 'Brazilian Portuguese'

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Explanation text */}
        <p className="text-lg">
          To define your vocabulary level, we picked the list of the 5000 most used words in {languageName} ordered by frequency.
        </p>

        <p className="text-lg">
          We'll show you words selected from this list and you'll tell us if you know them or not.
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/setup/explanation-2')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
