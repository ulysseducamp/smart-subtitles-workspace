import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { useNavigate } from 'react-router-dom'
import { supabase } from '@/lib/supabase'

export default function Results() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const [vocabLevel, setVocabLevel] = useState<number>(0)

  useEffect(() => {
    // Fetch vocab level from database
    const fetchVocabLevel = async () => {
      const { data } = await supabase
        .from('vocab_levels')
        .select('level')
        .eq('user_id', user?.id)
        .order('tested_at', { ascending: false })
        .limit(1)
        .single()

      if (data) setVocabLevel(data.level)
    }

    fetchVocabLevel()
  }, [user])

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button */}
      <div className="absolute top-4 right-4">
        <Button variant="ghost" onClick={signOut}>
          Log out
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-md mx-auto w-full">
        <h1 className="text-3xl font-bold text-center mb-6">
          You know approximately {vocabLevel.toLocaleString()} of the most used words
        </h1>

        <div className="text-muted-foreground mb-8 w-full">
          <p className="mb-4">
            Thanks to this information, Subly will be able to adapt the subtitles to your level:
          </p>
          <ul className="space-y-3 list-disc list-inside">
            <li>When a subtitle contains one unknown word, Subly will display the subtitle in your target language with the translation of the unknown word next to it.</li>
            <li>When a subtitle contains more than one word that you don't know, Subly will replace the subtitle by its version in your native language.</li>
          </ul>
        </div>

        <Button onClick={() => navigate('/onboarding/pricing')} className="w-full">
          Continue
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
