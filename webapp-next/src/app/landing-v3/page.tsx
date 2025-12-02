'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'

export default function LandingPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-5xl font-bold">
          Subly
        </h1>

        {/* Netflix screenshot - responsive (desktop/mobile) */}
        <picture className="block w-full max-w-3xl mx-auto">
          <source media="(min-width: 768px)" srcSet="/landing/landing-hero-desktop.png" />
          <img
            src="/landing/landing-hero-mobile.png"
            alt="Netflix with Subly subtitles"
            className="w-full h-auto"
          />
        </picture>

        {/* Button */}
        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/target-language')}
          className="w-full md:w-auto"
        >
          Discover how it works
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
