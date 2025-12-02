'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface LandingV3ContextType {
  // Section 1: Languages
  targetLanguage: string | null
  nativeLanguage: string | null
  vocabLevel: number | null

  // Section 2: Qualification
  mainStruggle: string | null
  learningDuration: string | null
  studyFrequency: string | null

  // Actions
  setTargetLanguage: (lang: string) => void
  setNativeLanguage: (lang: string) => void
  setVocabLevel: (level: number) => void
  setMainStruggle: (struggle: string) => void
  setLearningDuration: (duration: string) => void
  setStudyFrequency: (frequency: string) => void
}

const LandingV3Context = createContext<LandingV3ContextType | undefined>(undefined)

export function LandingV3Provider({ children }: { children: ReactNode }) {
  const [targetLanguage, setTargetLanguage] = useState<string | null>(null)
  const [nativeLanguage, setNativeLanguage] = useState<string | null>(null)
  const [vocabLevel, setVocabLevel] = useState<number | null>(null)
  const [mainStruggle, setMainStruggle] = useState<string | null>(null)
  const [learningDuration, setLearningDuration] = useState<string | null>(null)
  const [studyFrequency, setStudyFrequency] = useState<string | null>(null)

  // Load from sessionStorage on mount
  useEffect(() => {
    const saved = sessionStorage.getItem('landing_v3_data')
    if (saved) {
      try {
        const data = JSON.parse(saved)
        setTargetLanguage(data.targetLanguage || null)
        setNativeLanguage(data.nativeLanguage || null)
        setVocabLevel(data.vocabLevel || null)
        setMainStruggle(data.mainStruggle || null)
        setLearningDuration(data.learningDuration || null)
        setStudyFrequency(data.studyFrequency || null)
      } catch (error) {
        console.error('Failed to parse landing_v3_data from sessionStorage:', error)
      }
    }
  }, [])

  // Save to sessionStorage on every change
  useEffect(() => {
    sessionStorage.setItem('landing_v3_data', JSON.stringify({
      targetLanguage,
      nativeLanguage,
      vocabLevel,
      mainStruggle,
      learningDuration,
      studyFrequency
    }))
  }, [targetLanguage, nativeLanguage, vocabLevel, mainStruggle, learningDuration, studyFrequency])

  return (
    <LandingV3Context.Provider value={{
      targetLanguage,
      nativeLanguage,
      vocabLevel,
      mainStruggle,
      learningDuration,
      studyFrequency,
      setTargetLanguage,
      setNativeLanguage,
      setVocabLevel,
      setMainStruggle,
      setLearningDuration,
      setStudyFrequency
    }}>
      {children}
    </LandingV3Context.Provider>
  )
}

export function useLandingV3() {
  const context = useContext(LandingV3Context)
  if (!context) {
    throw new Error('useLandingV3 must be used within LandingV3Provider')
  }
  return context
}
