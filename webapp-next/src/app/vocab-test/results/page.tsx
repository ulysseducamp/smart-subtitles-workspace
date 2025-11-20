'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { useVocabTest } from '@/contexts/VocabTestContext'
import { useAuth } from '@/contexts/AuthContext'
import { createClient } from '@/lib/supabase/client'

const EXTENSION_ID = 'lhkamocmjgjikhmfiogfdjhlhffoaaek'

export default function VocabTestResults() {
  const { user } = useAuth()
  const { vocabLevel, targetLanguage } = useVocabTest()
  const [saved, setSaved] = useState(false)

  // Get language name
  const getLanguageName = (code: string | null) => {
    if (code === 'fr') return 'French'
    if (code === 'pt-BR') return 'Brazilian Portuguese'
    return 'your target language'
  }

  const languageName = getLanguageName(targetLanguage)

  // Save vocab level to Supabase
  useEffect(() => {
    const saveVocabLevel = async () => {
      if (!user || !targetLanguage || !vocabLevel || saved) return

      console.log('💾 Saving vocab level to Supabase...', { targetLanguage, vocabLevel })

      const supabase = createClient()

      try {
        // Save to vocab_levels table (upsert)
        const { error } = await supabase.from('vocab_levels').upsert(
          {
            user_id: user.id,
            language: targetLanguage,
            level: vocabLevel,
            tested_at: new Date().toISOString(),
          },
          { onConflict: 'user_id,language' }
        )

        if (error) {
          console.error('❌ Failed to save vocab level:', error)
          return
        }

        console.log('✅ Vocab level saved to Supabase')
        setSaved(true)
      } catch (error) {
        console.error('❌ Error saving vocab level:', error)
      }
    }

    saveVocabLevel()
  }, [user, targetLanguage, vocabLevel, saved])

  // Send message to extension (fire and forget)
  useEffect(() => {
    const notifyExtension = async () => {
      if (!saved || !vocabLevel || !targetLanguage) return

      // Check if chrome.runtime is available
      if (typeof chrome === 'undefined' || !chrome.runtime) {
        console.warn('⚠️ Chrome runtime not available - skipping extension notification')
        return
      }

      try {
        chrome.runtime.sendMessage(EXTENSION_ID, {
          type: 'VOCAB_LEVEL_UPDATED',
          level: vocabLevel,
          language: targetLanguage,
        })
        console.log('✅ Message sent to extension (fire and forget)')
      } catch (error) {
        console.log('⚠️ Could not send message to extension (not critical):', error)
      }
    }

    notifyExtension()
  }, [saved, vocabLevel, targetLanguage])

  // Open Netflix
  const handleGoBackToNetflix = () => {
    window.open('https://www.netflix.com', '_blank')
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <div className="text-8xl mb-8">🎉</div>

      <h1 className="text-4xl font-bold text-center mb-8">
        You know approximately <strong>{vocabLevel || 100}</strong> of the most used words in <strong>{languageName}</strong>
      </h1>

      <p className="text-lg text-center mb-8">
        You can now go back to Netflix and use Subly with this vocabulary level.
      </p>

      <Button onClick={handleGoBackToNetflix} size="lg">
        Go back to Netflix
      </Button>
    </div>
  )
}
