'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface LandingContextType {
  targetLanguage: string | null
  nativeLanguage: string | null
  vocabLevel: number | null
  setTargetLanguage: (lang: string) => void
  setNativeLanguage: (lang: string) => void
  setVocabLevel: (level: number) => void
}

const LandingContext = createContext<LandingContextType | undefined>(undefined)

export function LandingProvider({ children }: { children: ReactNode }) {
  const [targetLanguage, setTargetLanguage] = useState<string | null>(null)
  const [nativeLanguage, setNativeLanguage] = useState<string | null>(null)
  const [vocabLevel, setVocabLevel] = useState<number | null>(null)

  // Load from sessionStorage on mount
  useEffect(() => {
    const saved = sessionStorage.getItem('landing_data')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        setTargetLanguage(data.targetLanguage || null)
        setNativeLanguage(data.nativeLanguage || null)
        setVocabLevel(data.vocabLevel || null)
      } catch (error) {
        console.error('Failed to parse landing_data from sessionStorage:', error)
      }
    }
  }, [])

  // Save to sessionStorage on every change
  useEffect(() => {
    sessionStorage.setItem('landing_data', JSON.stringify({
      targetLanguage,
      nativeLanguage,
      vocabLevel
    }))
  }, [targetLanguage, nativeLanguage, vocabLevel])

  return (
    <LandingContext.Provider value={{
      targetLanguage,
      nativeLanguage,
      vocabLevel,
      setTargetLanguage,
      setNativeLanguage,
      setVocabLevel
    }}>
      {children}
    </LandingContext.Provider>
  )
}

export function useLanding() {
  const context = useContext(LandingContext)
  if (!context) {
    throw new Error('useLanding must be used within LandingProvider')
  }
  return context
}
