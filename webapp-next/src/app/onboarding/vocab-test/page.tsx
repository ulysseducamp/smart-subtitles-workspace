'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useRouter, useSearchParams } from 'next/navigation'
import { useOnboarding } from '@/contexts/OnboardingContext'

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

const LEVELS = [100, 200, 300, 500, 700, 1000, 1500, 2000, 2500, 3000, 4000, 5000]

export default function VocabTest() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { targetLang, setVocabLevel } = useOnboarding()
  const [loading, setLoading] = useState(false)

  // Get current level from URL (default 100)
  const currentLevel = parseInt(searchParams.get('level') || '100')

  // Get word lists for current target language
  const wordLists = targetLang === 'fr' ? FR_WORDS : PT_WORDS
  const currentWords = wordLists.find(w => w.level === currentLevel)

  // Get language name
  const languageName = targetLang === 'fr' ? 'French' : 'Brazilian Portuguese'

  // Get next level
  const currentIndex = LEVELS.indexOf(currentLevel)
  const nextLevel = LEVELS[currentIndex + 1]

  const handleDontKnow = () => {
    setLoading(true)
    setVocabLevel(currentLevel)

    // Show loading for 3 seconds, then redirect
    setTimeout(() => {
      router.push('/onboarding/results')
    }, 3000)
  }

  const handleKnowAll = () => {
    if (nextLevel) {
      // Go to next level
      router.push(`/onboarding/vocab-test?level=${nextLevel}`)
    } else {
      // Completed all levels
      setVocabLevel(5000)
      setLoading(true)
      setTimeout(() => {
        router.push('/onboarding/results')
      }, 3000)
    }
  }

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <h1 className="text-2xl font-bold mb-8">Analyzing your results...</h1>
        <div className="w-full max-w-md h-2 bg-muted rounded-full overflow-hidden">
          <div className="h-full bg-primary animate-pulse" style={{ width: '100%' }} />
        </div>
      </div>
    )
  }

  if (!currentWords) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <p className="text-red-500">Invalid level</p>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-6">
        {currentWords.words}
      </h1>

      <p className="text-center text-muted-foreground mb-12">
        (Those words are part of the <strong>{currentLevel}</strong> most used words in <strong>{languageName}</strong>)
      </p>

      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-2xl">
        <Button
          onClick={handleDontKnow}
          variant="outline"
          size="lg"
          className="flex-1"
        >
          There is one or several words I don't know
        </Button>

        <Button
          onClick={handleKnowAll}
          size="lg"
          className="flex-1"
        >
          I know all the words
        </Button>
      </div>
    </div>
  )
}
