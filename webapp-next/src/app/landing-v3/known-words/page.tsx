'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { ArrowDown } from 'lucide-react'

export default function KnownWordsPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          If a subtitle contains only words that you know
        </h1>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowDown className="h-12 w-12 text-muted-foreground" />
        </div>

        {/* Subtitle */}
        <h2 className="text-3xl font-bold">
          Subly displays it in your target language
        </h2>

        {/* Explanation text */}
        <p className="text-lg">
          (Since you know all the necessary words to understand it)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/explanation-4')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
