'use client'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export default function AuthPage() {
  const { signInWithGoogle } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleGoogleAuth = async () => {
    setLoading(true)
    try {
      // Trigger Google OAuth (redirect to Google)
      await signInWithGoogle()
    } catch (error) {
      console.error('Auth error:', error)
      alert('Authentication failed. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-12">
        Save your infos
      </h1>

      <Button
        onClick={handleGoogleAuth}
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
