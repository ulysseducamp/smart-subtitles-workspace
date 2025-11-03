'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import type { User } from '@supabase/supabase-js'
import { createClient } from '@/lib/supabase/client'
import { syncSessionToExtension } from '@/lib/syncExtension'
import { toast } from 'sonner'

type AuthContextType = {
  user: User | null
  loading: boolean
  signInWithGoogle: () => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
      if (session?.user) {
        console.log('✅ User authenticated:', session.user)
      }
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null)
      if (session?.user) {
        console.log('🔄 Auth state changed:', event, session.user)
      }

      // CRITICAL: Sync session to extension on SIGNED_IN and TOKEN_REFRESHED
      // This prevents extension from using stale refresh tokens
      if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
        console.log('🔄 Syncing session to extension after', event)
        syncSessionToExtension(session)

        // Show success toast only on SIGNED_IN (not on token refresh)
        if (event === 'SIGNED_IN' && session?.user?.email) {
          toast.success(`You are now connected with ${session.user.email}`, {
            duration: 3000,
          })
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [supabase])

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    })
    if (error) throw error
  }

  const signOut = async () => {
    try {
      const { error } = await supabase.auth.signOut()
      if (error) throw error

      // Redirect to welcome page after successful sign out
      window.location.href = '/welcome'
    } catch (error) {
      console.error('Sign out error:', error)
      toast.error('Failed to sign out')
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
