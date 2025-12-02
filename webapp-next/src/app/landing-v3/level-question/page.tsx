'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function LevelQuestionPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          Do you want to know your level?
        </h1>

        {/* Subtitle */}
        <p className="text-lg">
          Take our quick vocabulary test to find out how many words you know
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/setup/vocab-intro-1')}
          className="w-full md:w-auto"
        >
          Start
        </Button>

        {/* Duration indicator below button */}
        <p className="text-sm text-muted-foreground">
          (it takes only 30sec)
        </p>
      </div>
    </div>
  )
}
