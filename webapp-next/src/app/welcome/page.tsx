'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'

export default function WelcomePage() {
  const { user, signInWithGoogle, signOut } = useAuth()
  const router = useRouter()
  const supabase = createClient()

  // Check if returning user (has settings in Supabase)
  useEffect(() => {
    const checkReturningUser = async () => {
      if (user) {
        const { data } = await supabase
          .from('user_settings')
          .select('*')
          .eq('user_id', user.id)
          .single()

        if (data) {
          // Returning user with settings
          router.push('/welcome-back')
        }
      }
    }

    checkReturningUser()
  }, [user, router, supabase])

  const handleAuth = async () => {
    try {
      await signInWithGoogle()
      // Redirect handled by Supabase redirectTo option
    } catch (error) {
      console.error('Auth error:', error)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button (top-right, only visible after auth) */}
      {user && (
        <div className="absolute top-4 right-4">
          <Button variant="ghost" onClick={signOut}>
            Log out
          </Button>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <img
          src="/ulysse-photo.jpg"
          alt="Ulysse"
          className="w-32 h-32 rounded-full mb-6 object-cover bg-muted"
          onError={(e) => {
            e.currentTarget.style.display = 'none'
          }}
        />

        <h1 className="text-3xl font-bold text-center mb-4 max-w-2xl">
          Thanks for downloading Subly, my name is Ulysse and I learned
          to code just to build this extension. Hope you'll enjoy it!
        </h1>

        <p className="text-lg text-center mb-6">
          To use the extension, you first need to create an account and set it up
        </p>

        <Button onClick={handleAuth} size="lg" className="mb-2">
          Create an account and set up Subly
        </Button>

        <p className="text-sm text-muted-foreground mb-4">
          It only takes 3 steps
        </p>

        <button
          onClick={handleAuth}
          className="text-sm text-primary underline hover:no-underline"
        >
          Already have an account? login with google
        </button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
