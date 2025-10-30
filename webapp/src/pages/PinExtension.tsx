import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'
import { useNavigate } from 'react-router-dom'

export default function PinExtension() {
  const { signOut } = useAuth()
  const navigate = useNavigate()

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
        <h1 className="text-3xl font-bold text-center mb-6">
          Bonus: Pin the extension for quick access
        </h1>

        <div className="mb-8 w-full max-w-lg">
          <img
            src="/pin-extension-demo.gif"
            alt="How to pin the extension in Chrome"
            className="w-full max-w-[200px] mx-auto rounded-lg shadow-lg"
          />
        </div>

        <p className="text-muted-foreground text-center mb-6">
          Click on the puzzle icon in Chrome's toolbar, then click the pin icon next to
          "Subly" to keep it visible.
        </p>

        <Button onClick={() => navigate('/onboarding/complete')} className="w-full max-w-xs">
          I have done it
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
