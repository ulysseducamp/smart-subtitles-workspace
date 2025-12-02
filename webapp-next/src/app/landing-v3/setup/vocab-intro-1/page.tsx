'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'

export default function VocabIntro1Page() {
  const router = useRouter()
  const { targetLanguage } = useLandingV3()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Text content with dynamic target language */}
        <div className="space-y-6 text-lg">
          <p>
            To define your vocabulary level, we picked the list of the 5000 most used words in <strong>{targetLanguage || 'your target language'}</strong> ordered by frequency.
          </p>
          <p>
            We'll show you words selected from this list and you'll tell us if you know them or not.
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/setup/vocab-intro-2')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
