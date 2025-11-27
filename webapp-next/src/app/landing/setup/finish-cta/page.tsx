'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Lightbulb } from 'lucide-react'

export default function FinishCtaPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          Finish setting up Subly
        </h1>

        {/* Description */}
        <p className="text-lg">
          Now that we know the words that you know (approximately), There are just a few steps left to set-up Subly entirely.
        </p>

        {/* Good to know */}
        <div className="flex items-start gap-3 text-left bg-muted p-4 rounded-lg">
          <Lightbulb className="h-5 w-5 mt-1 flex-shrink-0" />
          <p className="text-sm">
            <strong>Good to know:</strong> You can do it on your phone/computer/tablet.
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing/setup/native-language')}
          className="w-full md:w-auto"
        >
          Finish setting up Subly
        </Button>
      </div>
    </div>
  )
}
