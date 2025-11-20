'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

interface VocabTestContextType {
  // Target language for the test
  targetLanguage: string | null
  // Vocab level determined by the test
  vocabLevel: number | null

  // Setters
  setTargetLanguage: (lang: string) => void
  setVocabLevel: (level: number) => void
}

const VocabTestContext = createContext<VocabTestContextType | undefined>(undefined)

export function VocabTestProvider({ children }: { children: ReactNode }) {
  const [targetLanguage, setTargetLanguage] = useState<string | null>(null)
  const [vocabLevel, setVocabLevel] = useState<number | null>(null)

  return (
    <VocabTestContext.Provider
      value={{
        targetLanguage,
        vocabLevel,
        setTargetLanguage,
        setVocabLevel,
      }}
    >
      {children}
    </VocabTestContext.Provider>
  )
}

export function useVocabTest() {
  const context = useContext(VocabTestContext)
  if (context === undefined) {
    throw new Error('useVocabTest must be used within VocabTestProvider')
  }
  return context
}
