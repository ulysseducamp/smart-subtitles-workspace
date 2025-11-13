'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface OnboardingContextType {
  // User selections during onboarding
  targetLang: string | null
  nativeLang: string | null
  vocabLevel: number | null

  // Setters
  setTargetLang: (lang: string) => void
  setNativeLang: (lang: string) => void
  setVocabLevel: (level: number) => void
}

const OnboardingContext = createContext<OnboardingContextType | undefined>(undefined)

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [targetLang, setTargetLang] = useState<string | null>(null)
  const [nativeLang, setNativeLang] = useState<string | null>(null)
  const [vocabLevel, setVocabLevel] = useState<number | null>(null)

  // Au mount: Restaurer depuis sessionStorage si existe
  useEffect(() => {
    const saved = sessionStorage.getItem('onboarding_data')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        if (data.targetLang) setTargetLang(data.targetLang)
        if (data.nativeLang) setNativeLang(data.nativeLang)
        if (data.vocabLevel) setVocabLevel(data.vocabLevel)
      } catch (e) {
        console.error('Failed to restore sessionStorage:', e)
      }
    }
  }, [])

  // À chaque changement: Sauvegarder dans sessionStorage
  useEffect(() => {
    if (targetLang || nativeLang || vocabLevel) {
      const data = { targetLang, nativeLang, vocabLevel }
      sessionStorage.setItem('onboarding_data', JSON.stringify(data))
    }
  }, [targetLang, nativeLang, vocabLevel])

  return (
    <OnboardingContext.Provider
      value={{
        targetLang,
        nativeLang,
        vocabLevel,
        setTargetLang,
        setNativeLang,
        setVocabLevel,
      }}
    >
      {children}
    </OnboardingContext.Provider>
  )
}

export function useOnboarding() {
  const context = useContext(OnboardingContext)
  if (context === undefined) {
    throw new Error('useOnboarding must be used within OnboardingProvider')
  }
  return context
}
