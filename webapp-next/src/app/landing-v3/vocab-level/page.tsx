'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function VocabLevelPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          Do you know your level?
        </h1>

        {/* Text content */}
        <div className="space-y-4 text-lg">
          <p>
            Probably not very precisely. At Subly, we don't like notion like A1, A2, B1, ...
          </p>
          <p>
            We prefere another system, called "Frequency lists" (the secret of the best polyglots)
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/frequency-list')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
