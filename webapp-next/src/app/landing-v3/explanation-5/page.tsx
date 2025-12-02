'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { ArrowDown } from 'lucide-react'

export default function Explanation5Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          If a subtitle contains more than one word that you don't know
        </h1>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowDown className="h-12 w-12 text-muted-foreground" />
        </div>

        {/* Subtitle */}
        <h2 className="text-3xl font-bold">
          Subly displays it in your native language
        </h2>

        {/* Explanation text */}
        <p className="text-lg">
          (so you focus on subtitles adapted to your level)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/comparison')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
