'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function AutomaticSystemPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Main text */}
        <div className="space-y-6 text-lg">
          <p>
            With this automatic translation system, users with your level are exposed, on average, to 300 new words per episode.
          </p>

          <p>
            If we estimate that you need to be exposed 10 times to a word to master it, it means that you would master 30 new words per episode.
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/reach-fluency')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
