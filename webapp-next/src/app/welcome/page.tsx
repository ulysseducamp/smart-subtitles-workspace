'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { FeedbackBanner } from '@/components/FeedbackBanner'

export default function WelcomePage() {
  const { signInWithGoogle } = useAuth()
  const router = useRouter()

  const handleStart = () => {
    router.push('/onboarding/explanation-1')
  }

  const handleLogin = async () => {
    try {
      await signInWithGoogle()
      // Redirect handled by Supabase redirectTo option → /welcome-back
    } catch (error) {
      console.error('Auth error:', error)
    }
  }

  return (
    <div className="min-h-screen flex flex-col pb-20">
      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <h1 className="text-4xl font-bold text-center mb-4 max-w-2xl">
          Welcome to Subly, the extension beloved by reddit users 🤖
        </h1>

        <p className="text-lg text-center mb-8 text-muted-foreground">
          To use subly, you first need to complete a few steps
        </p>

        <Button onClick={handleStart} size="lg" className="mb-4">
          Start
        </Button>

        <button
          onClick={handleLogin}
          className="text-sm text-primary underline hover:no-underline"
        >
          Already have an account? login with google
        </button>
      </div>

      {/* Fixed feedback banner */}
      <FeedbackBanner />
    </div>
  )
}
