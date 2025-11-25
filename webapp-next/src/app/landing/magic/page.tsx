'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function MagicPage() {
  const router = useRouter()

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

        {/* Text from wireframe */}
        <p className="text-lg">
          When you watch Netflix, for each subtitle, Subly choose if it should be displayed in your target language or in your native language (based on the words you know and don't know)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/known-words')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
