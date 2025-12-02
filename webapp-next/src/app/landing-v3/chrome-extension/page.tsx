'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import Image from 'next/image'

export default function ChromeExtensionPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Chrome + Extension image */}
        <div className="flex justify-center">
          <Image
            src="/landing/intro-chrome-subly.svg"
            alt="Chrome extension"
            width={200}
            height={200}
          />
        </div>

        {/* Explanation text */}
        <div className="space-y-6 text-lg">
          <p>
            Subly is a Chrome extension (a little tool that you can add to your Chrome browser on your computer).
          </p>

          <p>
            When you watch Netflix on Chrome on your computer, Subly adapts the subtitles to your level.
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/explanation-1')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
