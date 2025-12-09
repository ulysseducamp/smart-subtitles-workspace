'use client'

import { AuthProvider } from '@/contexts/AuthContext'
import { PostHogProvider } from '@/providers/PostHogProvider'
import { Toaster } from 'sonner'

export function ClientProviders({ children }: { children: React.ReactNode }) {
  return (
    <PostHogProvider>
      <AuthProvider>
        {children}
        <Toaster position="top-center" />
      </AuthProvider>
    </PostHogProvider>
  )
}
