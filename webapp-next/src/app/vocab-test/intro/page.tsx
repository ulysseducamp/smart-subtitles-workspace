'use client'

import { useEffect, Suspense } from 'react'
import { Button } from '@/components/ui/button'
import { useRouter, useSearchParams } from 'next/navigation'
import { useVocabTest } from '@/contexts/VocabTestContext'

function VocabTestIntroContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { setTargetLanguage, targetLanguage } = useVocabTest()

  // Get targetLanguage from URL and set in context on mount
  useEffect(() => {
    const langFromUrl = searchParams.get('targetLanguage')
    if (langFromUrl) {
      setTargetLanguage(langFromUrl)
    } else {
      // Fallback to PT-BR if no language specified
      setTargetLanguage('pt-BR')
    }
  }, [searchParams, setTargetLanguage])

  // Get language name from code
  const getLanguageName = (code: string | null) => {
    if (code === 'fr') return 'French'
    if (code === 'pt-BR') return 'Brazilian Portuguese'
    return 'your target language'
  }

  const languageName = getLanguageName(targetLanguage)

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        Let's test your vocabulary level!
      </h1>

      <p className="text-lg text-center mb-8">
        To define your vocabulary level, we picked the list of the 5000 most used words in <strong>{languageName}</strong> ordered by frequency.
      </p>

      <Button onClick={() => router.push('/vocab-test/explanation')} size="lg">
        Continue
      </Button>
    </div>
  )
}

export default function VocabTestIntroPage() {
  return (
    <Suspense fallback={<div className="flex-1 flex items-center justify-center">Loading...</div>}>
      <VocabTestIntroContent />
    </Suspense>
  )
}
