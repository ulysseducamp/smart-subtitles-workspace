'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

// Portuguese word lists
const PT_WORDS = [
  { level: 100, words: 'ele, como, falar, mesmo, dever, onde' },
  { level: 200, words: 'mundo, tentar, lugar, nome, importante, último' },
  { level: 300, words: 'morrer, certeza, enquanto, olá, contra, corpo' },
  { level: 500, words: 'errar, serviço, preço, uma, considerar, vai' },
  { level: 700, words: 'sentar, clicar, cerca, câmera, vermelho, principalmente' },
  { level: 1000, words: 'observar, membro, americano, desaparecer, apoiar, mamãe' },
  { level: 1500, words: 'cobrir, relacionar, proteção, expressão, lua, particular' },
  { level: 2000, words: 'reclamar, impacto, honra, móvel, tribunal, pior' },
  { level: 2500, words: 'imóvel, duplo, vendedor, olhe, estender, energético' },
  { level: 3000, words: 'influenciar, mínimo, sensor, ocasião, assegurar, telhado' },
  { level: 4000, words: 'verso, ousar, puxa, mole, entretenimento, blusa' },
  { level: 5000, words: 'exausto, art., surdo, deusa, box, parece' },
]

// French word lists
const FR_WORDS = [
  { level: 100, words: 'lui, penser, soi, parce, très, après' },
  { level: 200, words: 'sûr, mieux, dernier, jusque, moins, minute' },
  { level: 300, words: 'continuer, voulais, gros, espérer, suivre, amour' },
  { level: 500, words: 'dur, réponse, préparer, page, tirer, exactement' },
  { level: 700, words: 'principal, propos, arme, augmenter, concerner, gérer' },
  { level: 1000, words: 'évidemment, supérieur, réveiller, épisode, attraper, rendez-vous' },
  { level: 1500, words: 'sors, campagne, soupe, coller, fiche, réaction' },
  { level: 2000, words: 'commencer, pardon, drogue, porc, essai, saveur' },
  { level: 2500, words: 'contexte, soudainement, guérir, marketing, assistant, introduire' },
  { level: 3000, words: 'emballer, petit-déjeuner, ai-je, moi, assis, rédiger' },
  { level: 4000, words: 'calendrier, généreux, touriste, vigueur, honorer, pousse' },
  { level: 5000, words: 'résistant, optique, reportage, gémissement, résulter, amande' },
]

export default function VocabTest() {
  const { user, signOut } = useAuth()
  const router = useRouter()
  const [selectedLevel, setSelectedLevel] = useState<number | null>(null)
  const [targetLang, setTargetLang] = useState<string>('')
  const [saving, setSaving] = useState(false)
  const supabase = createClient()

  useEffect(() => {
    // Fetch target_lang from user_settings
    const fetchTargetLang = async () => {
      const { data } = await supabase
        .from('user_settings')
        .select('target_lang')
        .eq('user_id', user?.id)
        .single()

      if (data) setTargetLang(data.target_lang)
    }

    fetchTargetLang()
  }, [user, supabase])

  const handleConfirm = async () => {
    if (!selectedLevel) return

    setSaving(true)
    try {
      // Save to vocab_levels table
      const { error: dbError } = await supabase
        .from('vocab_levels')
        .upsert({
          user_id: user?.id,
          language: targetLang,
          level: selectedLevel,
          tested_at: new Date().toISOString(),
        }, {
          onConflict: 'user_id,language'
        })

      if (dbError) throw dbError

      router.push('/onboarding/results')
    } catch (err) {
      console.error('Error saving vocab level:', err)
    } finally {
      setSaving(false)
    }
  }

  // Get word lists for current target language
  const wordLists = targetLang === 'fr' ? FR_WORDS : PT_WORDS

  return (
    <div className="min-h-screen flex flex-col pb-20">
      {/* Logout button */}
      <div className="absolute top-4 right-4">
        <Button variant="ghost" onClick={signOut}>
          Log out
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto w-full">
        <h1 className="text-3xl font-bold text-center mb-4">
          Estimate your vocabulary level
        </h1>

        <p className="text-sm text-muted-foreground mb-6 text-center max-w-xl">
          Select the first group of words in which there is at least one word you don't know.
          You should read each group one by one, and as soon as you find a group that contains
          a word you don't know, stop there and select that group.
          <br /><br />
          These groups are based on the list of the 10,000 most commonly used words in your target language.
          The first group is made up of randomly selected words from the 100 most common words,
          the second group comes from the 200 most common words, and so on.
          <br /><br />
          This way, your answer will help me roughly estimate how many of the most common
          words you already know in your target language.
        </p>

        <RadioGroup
          value={selectedLevel?.toString()}
          onValueChange={(value) => setSelectedLevel(parseInt(value))}
          className="w-full space-y-3"
        >
          {wordLists.map(({ level, words }) => (
            <div key={level} className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent cursor-pointer">
              <RadioGroupItem value={level.toString()} id={`level-${level}`} />
              <Label htmlFor={`level-${level}`} className="flex-1 cursor-pointer">
                {words} ({level} words)
              </Label>
            </div>
          ))}

          {/* Special option: knows all words */}
          <div className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent cursor-pointer">
            <RadioGroupItem value="5000" id="level-all" />
            <Label htmlFor="level-all" className="flex-1 cursor-pointer font-semibold">
              I know all the words above (5000 words - advanced level)
            </Label>
          </div>
        </RadioGroup>

        <Button
          onClick={handleConfirm}
          disabled={!selectedLevel || saving}
          className="w-full mt-6"
        >
          {saving ? 'Saving...' : 'Confirm'}
        </Button>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
