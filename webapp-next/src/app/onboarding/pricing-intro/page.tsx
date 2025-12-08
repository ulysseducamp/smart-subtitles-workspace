'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useOnboarding } from '@/contexts/OnboardingContext'
import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export default function PricingIntroPage() {
  const router = useRouter()
  const { user } = useAuth()
  const { targetLang, nativeLang, vocabLevel } = useOnboarding()
  const [saved, setSaved] = useState(false)

  // Sauvegarder dans Supabase après auth
  useEffect(() => {
    const saveToSupabase = async () => {
      // Attendre que user soit disponible + données Context chargées
      if (!user || !targetLang || !nativeLang || !vocabLevel || saved) return

      console.log('💾 Saving to Supabase...', { targetLang, nativeLang, vocabLevel })

      const supabase = createClient()

      try {
        // 1. Sauvegarder user_settings
        await supabase.from('user_settings').upsert({
          user_id: user.id,
          target_lang: targetLang,
          native_lang: nativeLang,
        })

        // 2. Sauvegarder vocab_levels
        await supabase.from('vocab_levels').upsert(
          {
            user_id: user.id,
            language: targetLang,
            level: vocabLevel,
            tested_at: new Date().toISOString(),
          },
          { onConflict: 'user_id,language' }
        )

        // 3. Clean sessionStorage (plus besoin)
        sessionStorage.removeItem('onboarding_data')
        console.log('✅ Saved to Supabase + cleaned sessionStorage')
        setSaved(true)
      } catch (error) {
        console.error('❌ Failed to save to Supabase:', error)
      }
    }

    saveToSupabase()
  }, [user, targetLang, nativeLang, vocabLevel, saved])

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        We want you to try Subly for free
      </h1>

      <div className="flex items-center gap-2 mb-12">
        <span className="text-2xl">✓</span>
        <span className="text-lg">No Payment Due Now</span>
      </div>

      <Button onClick={() => router.push('/onboarding/pricing-details')} size="lg" className="mb-4">
        Try for $0.00
      </Button>

      <p className="text-center text-muted-foreground">
        After, Just <strong>$19.99 per year</strong> for full access
      </p>
    </div>
  )
}
