'use client'

import { useState, useEffect, Suspense } from 'react'
import { Button } from '@/components/ui/button'
import { useRouter, useSearchParams } from 'next/navigation'
import { useLanding } from '@/contexts/LandingContext'

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

function VocabTestContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { targetLanguage, setVocabLevel } = useLanding()
  const [loading, setLoading] = useState(false)

  // Get current level from URL (default 100)
  const currentLevel = parseInt(searchParams.get('level') || '100')

  // Get word lists for current target language
  const wordLists = targetLanguage === 'fr' ? FR_WORDS : PT_WORDS
  const currentWords = wordLists.find(w => w.level === currentLevel)

  // Get language name
  const languageName = targetLanguage === 'fr' ? 'French' : 'Brazilian Portuguese'

  // Get next level
  const currentIndex = LEVELS.indexOf(currentLevel)
  const nextLevel = LEVELS[currentIndex + 1]

  const handleDontKnow = () => {
    setLoading(true)
    setVocabLevel(currentLevel)

    // Show loading for 2 seconds, then redirect to analyzing page
    setTimeout(() => {
      router.push('/landing/setup/analyzing')
    }, 2000)
  }

  const handleKnowAll = () => {
    if (nextLevel) {
      // Go to next level
      router.push(`/landing/setup/vocab-test?level=${nextLevel}`)
    } else {
      // Completed all levels
      setVocabLevel(5000)
      setLoading(true)
      setTimeout(() => {
        router.push('/landing/setup/analyzing')
      }, 2000)
    }
  }

  if (!currentWords) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <p>Invalid level</p>
      </div>
    )
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8">
        {/* Title */}
        <div className="text-center space-y-2">
          <h2 className="text-xl text-muted-foreground">
            Do you know all these words?
          </h2>
          <p className="text-4xl font-bold">{currentWords.words}</p>
        </div>

        {/* Buttons */}
        {loading ? (
          <div className="text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]" />
            <p className="mt-4 text-muted-foreground">Loading...</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            <Button
              size="lg"
              variant="outline"
              onClick={handleDontKnow}
              className="w-full"
            >
              There is one or several words I don't know
            </Button>
            <Button
              size="lg"
              onClick={handleKnowAll}
              className="w-full"
            >
              I know all the words
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

export default function VocabTestPage() {
  return (
    <Suspense fallback={
      <div className="flex-1 flex items-center justify-center">
        <p>Loading...</p>
      </div>
    }>
      <VocabTestContent />
    </Suspense>
  )
}
