'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function IntroPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Chrome + Subly icons */}
        <div className="flex justify-center my-8">
          <img
            src="/landing/intro-chrome-subly.svg"
            alt="Chrome and Subly logos"
            className="w-48 h-auto"
          />
        </div>

        {/* Text below image */}
        <p className="text-lg">
          Subly is a Chrome extension (a little tool that you can add to your Chrome browser on your desktop)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/magic')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
