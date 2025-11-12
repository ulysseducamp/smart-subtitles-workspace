'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/contexts/OnboardingContext'

export default function VocabTestIntroPage() {
  const router = useRouter()
  const { targetLang } = useOnboarding()

  // Get language name from code
  const getLanguageName = (code: string | null) => {
    if (code === 'fr') return 'French'
    if (code === 'pt-BR') return 'Brazilian Portuguese'
    return 'your target language'
  }

  const languageName = getLanguageName(targetLang)

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        Now, it's time to test your vocabulary level
      </h1>

      <p className="text-lg text-center mb-8">
        To define your vocabulary level, we picked the list of the 5000 most used words in <strong>{languageName}</strong> ordered by frequency.
      </p>

      <Button onClick={() => router.push('/onboarding/vocab-test-explanation')} size="lg">
        Continue
      </Button>
    </div>
  )
}
