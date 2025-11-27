'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function VocabIntroPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          Do you know your vocabulary level?
        </h1>

        {/* Description */}
        <p className="text-lg">
          Discover it now by answering a few questions. In the mean time, your answers will allow us to set-up subly for you
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/setup/target-language')}
          className="w-full md:w-auto"
        >
          Discover your level
        </Button>

        {/* Additional note */}
        <p className="text-sm text-muted-foreground">
          (it takes 30sec, you can do it from your phone/computer/tablet)
        </p>
      </div>
    </div>
  )
}
