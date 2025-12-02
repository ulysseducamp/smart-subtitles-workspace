'use client'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export default function AuthPage() {
  const { signInWithGoogle } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleGoogleSignIn = async () => {
    setLoading(true)
    try {
      // Pass redirect parameter to specify where to go after OAuth
      await signInWithGoogle('/landing-v3/setup/post-auth')
    } catch (error) {
      console.error('Auth error:', error)
      alert('Authentication failed. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      {/* Title */}
      <h1 className="text-4xl font-bold text-center mb-4">
        Now it's time to connect with Google
      </h1>

      {/* Description */}
      <p className="text-lg text-center mb-12">
        So we can save your infos.<br />
        (and send you an email with a link to download the extension later if you're not on your computer yet)
      </p>

      <Button
        onClick={handleGoogleSignIn}
        size="lg"
        className="gap-2"
        disabled={loading}
      >
        {loading ? (
          'Connecting...'
        ) : (
          <>
            <img src="/Google__G__logo.svg" alt="Google logo" className="w-5 h-5" />
            Connect with Google
          </>
        )}
      </Button>
    </div>
  )
}
