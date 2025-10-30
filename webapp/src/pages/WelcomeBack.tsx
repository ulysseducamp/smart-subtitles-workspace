import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { ManageSubscriptionButton } from '@/components/ManageSubscriptionButton'

export default function WelcomeBack() {
  const { signOut } = useAuth()

  const handleOpenNetflix = () => {
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
      <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-md mx-auto w-full">
        <h1 className="text-4xl font-bold text-center mb-6">
          Welcome back! 👋
        </h1>

        <p className="text-lg text-center mb-8 text-muted-foreground">
          Your extension is already set up and ready to use. Head to Netflix and enjoy
          your personalized subtitles!
        </p>

        <Button onClick={handleOpenNetflix} size="lg" className="w-full">
          Go to Netflix
        </Button>

        <Button
          variant="ghost"
          onClick={() => window.close()}
          className="mt-4"
        >
          Close this tab
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
