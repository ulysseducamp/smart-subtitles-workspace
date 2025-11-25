'use client'

import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'

export default function WelcomeBack() {
  const router = useRouter()
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
        <h1 className="text-4xl font-bold text-center mb-4">
          Welcome back!
        </h1>

        <p className="text-lg text-center mb-8 text-muted-foreground">
          Please, pin the extension for quick access
        </p>

        {/* GIF demonstration */}
        <div className="mb-8">
          <img
            src="/pin-extension-demo.gif"
            alt="How to pin the extension"
            className="w-48 h-auto rounded-lg border border-border"
          />
        </div>

        <Button
          onClick={() => router.push('/welcome-back/how-to-use')}
          size="lg"
          className="w-full max-w-md"
        >
          I've done it
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
