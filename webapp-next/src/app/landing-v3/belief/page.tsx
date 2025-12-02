'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'

export default function BeliefPage() {
  const router = useRouter()
  const { targetLanguage } = useLandingV3()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Text content with dynamic target language */}
        <div className="space-y-6 text-lg">
          <p>
            We believe that if you want to learn <strong>{targetLanguage}</strong> efficiently, you should focus on mastering the most used words first.
          </p>
          <p>
            That's why Subly defines your level by testing how many of the most used words you know
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/level-question')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
