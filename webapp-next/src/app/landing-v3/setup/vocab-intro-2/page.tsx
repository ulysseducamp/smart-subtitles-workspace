'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function VocabIntro2Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Text content */}
        <p className="text-lg">
          This will allow us to evaluate, approximately, how many of the most used words you know which is your "level" for Subly.
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/setup/vocab-test')}
          className="w-full md:w-auto"
        >
          Start
        </Button>
      </div>
    </div>
  )
}
