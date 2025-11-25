'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Check } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { useLanding } from '@/contexts/LandingContext'
import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export default function PostAuthPage() {
  const router = useRouter()
  const { user } = useAuth()
  const { targetLanguage, nativeLanguage, vocabLevel } = useLanding()
  const [saved, setSaved] = useState(false)

  // Save to Supabase after auth
  useEffect(() => {
    const saveToSupabase = async () => {
      // Wait for user + Context data to be loaded
      if (!user || !targetLanguage || !nativeLanguage || !vocabLevel || saved) return

      console.log('💾 Saving to Supabase...', { targetLanguage, nativeLanguage, vocabLevel })

      const supabase = createClient()

      try {
        // 1. Save user_settings
        await supabase.from('user_settings').upsert({
          user_id: user.id,
          target_lang: targetLanguage,
          native_lang: nativeLanguage,
        })

        // 2. Save vocab_levels
        await supabase.from('vocab_levels').upsert(
          {
            user_id: user.id,
            language: targetLanguage,
            level: vocabLevel,
            tested_at: new Date().toISOString(),
          },
          { onConflict: 'user_id,language' }
        )

        // 3. Clean sessionStorage (no longer needed)
        sessionStorage.removeItem('landing_data')
        console.log('✅ Saved to Supabase + cleaned sessionStorage')
        setSaved(true)
      } catch (error) {
        console.error('❌ Failed to save to Supabase:', error)
      }
    }

    saveToSupabase()
  }, [user, targetLanguage, nativeLanguage, vocabLevel, saved])

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold mb-8">
          We want you to try Subly for free
        </h1>

        {/* Screen illustration */}
        <div className="flex justify-center mb-8">
          <img
            src="/landing/post-auth-screen.png"
            alt="Subly on screen illustration"
            className="w-full max-w-lg"
          />
        </div>

        {/* CTA section with 16px spacing */}
        <div className="space-y-4">
          {/* No Payment Due Now */}
          <div className="flex items-center justify-center gap-2 text-base">
            <Check className="h-5 w-5" />
            <span>No Payment Due Now</span>
          </div>

          {/* Button */}
          <Button
            size="lg"
            onClick={() => router.push('/landing/setup/reminder')}
            className="w-full md:w-auto"
          >
            Try for 0.00$
          </Button>

          {/* Pricing info */}
          <p className="text-base text-muted-foreground">
            After, Just 9$ per year (0,75$/mo)
          </p>
        </div>
      </div>
    </div>
  )
}
