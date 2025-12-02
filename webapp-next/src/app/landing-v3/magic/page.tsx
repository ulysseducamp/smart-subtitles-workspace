'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'

export default function MagicPage() {
  const router = useRouter()
  const { targetLanguage, nativeLanguage } = useLandingV3()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Netflix subtitle demonstration */}
        <img
          src="/landing/magic-demonstration.png"
          alt="Subly subtitle demonstration on Netflix"
          className="w-48 mx-auto"
        />

        {/* Title below image */}
        <h1 className="text-4xl font-bold">
          Subly's magic
        </h1>

        {/* Text with dynamic language values */}
        <div className="space-y-4">
          <p className="text-lg">
            When you watch Netflix, for each subtitle, Subly chooses if it should be displayed in <strong>{targetLanguage}</strong> or in <strong>{nativeLanguage}</strong> based on your level.
          </p>
          <p className="text-lg">
            But how do we know your "level"?
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/vocab-level')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
