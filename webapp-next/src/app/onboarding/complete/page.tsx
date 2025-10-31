'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'

export default function Complete() {
  const { signOut } = useAuth()

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
          🎉 Congrats, you're all set!
        </h1>

        <p className="text-lg text-center mb-8 max-w-xl">
          You can start using the extension: when watching Netflix, click on the Subly icon to make this pop-up appear, then click on the button "Process subtitles" to adapt Netflix subtitles to your level.
        </p>

        <div className="mb-6 w-full">
          <img
            src="/Netflix+pop-up.jpg"
            alt="Subly extension popup on Netflix"
            className="w-full max-w-[500px] mx-auto rounded-lg shadow-lg"
          />
        </div>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
