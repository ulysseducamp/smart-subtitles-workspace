'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'

export default function HowToUsePage() {
  const { signOut } = useAuth()

  const handleGoToNetflix = () => {
    window.open('https://www.netflix.com', '_blank')
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header buttons */}
      <div className="absolute top-4 right-4 flex gap-2">
        <ManageSubscriptionButton />
        <Button variant="ghost" onClick={signOut}>
          Log out
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto w-full">
        <h1 className="text-4xl font-bold text-center mb-8">
          Congrats you're all set! How to use Subly now?
        </h1>

        {/* 3 Steps */}
        <div className="mb-8 space-y-4 w-full max-w-md text-left">
          <div>
            <p className="text-base">
              <strong>Step 1:</strong> Start watching something on Netflix
            </p>
          </div>

          <div>
            <p className="text-base">
              <strong>Step 2:</strong> Click on the Subly Icon to make our pop-up appear
            </p>
          </div>

          <div>
            <p className="text-base">
              <strong>Step 3:</strong> click on "Process subtitles" to adapt the subtitles from Netflix to your level.
            </p>
          </div>
        </div>

        {/* Image demonstration */}
        <div className="mb-8">
          <img
            src="/click-process.png"
            alt="Click process subtitles"
            className="w-full max-w-md h-auto rounded-lg"
          />
        </div>

        <Button
          onClick={handleGoToNetflix}
          size="lg"
          className="w-full max-w-md"
        >
          Go to Netflix
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
