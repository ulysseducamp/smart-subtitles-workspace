'use client'

import { Lightbulb } from 'lucide-react'

export default function CompletePage() {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          You're all set!
        </h1>

        {/* Description */}
        <div className="space-y-4 text-lg">
          <p>
            We just sent you an email to download the extension (if needed, verify your spam folder)
          </p>

          <p>
            If you're on your computer you can download the extension directly{' '}
            <a
              href="https://chromewebstore.google.com/detail/subly/lhkamocmjgjikhmfiogfdjhlhffoaaek"
              target="_blank"
              rel="noopener noreferrer"
              className="underline font-semibold"
            >
              here
            </a>
          </p>

          <p className="text-muted-foreground">
            After the download, click on "Already have an account, connect with google" to load the infos you already entered.
          </p>
        </div>

        {/* Good to know callout */}
        <div className="bg-muted rounded-lg p-6 flex items-start gap-3 text-left">
          <Lightbulb className="h-6 w-6 flex-shrink-0 mt-0.5" />
          <p className="text-base">
            <span className="font-semibold">Good to know:</span> you can contact me at unducamp.pro@gmail.com
          </p>
        </div>
      </div>
    </div>
  )
}
