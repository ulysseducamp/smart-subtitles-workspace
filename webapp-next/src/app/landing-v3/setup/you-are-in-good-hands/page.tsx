'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'

export default function YouAreInGoodHandsPage() {
  const router = useRouter()
  const { mainStruggle } = useLandingV3()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          You are in good hands
        </h1>

        {/* Main text */}
        <div className="space-y-6 text-lg">
          <p>
            Studies have shown that consuming a lot of content is actually the key to improve all the important aspects of language learning, including {mainStruggle}.
          </p>

          <p>
            Why? Because our brains are wired to acquire a new language the same way we acquired our native language, by being exposed to it a lot.
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/setup/learning-duration')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
