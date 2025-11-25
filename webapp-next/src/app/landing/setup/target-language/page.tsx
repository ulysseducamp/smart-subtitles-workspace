'use client'

import { useRouter } from 'next/navigation'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useLanding } from '@/contexts/LandingContext'
import { useState } from 'react'

export default function TargetLanguagePage() {
  const router = useRouter()
  const { targetLanguage, setTargetLanguage } = useLanding()
  const [selectedLanguage, setSelectedLanguage] = useState(targetLanguage || '')

  const handleLanguageChange = (value: string) => {
    setSelectedLanguage(value)
    setTargetLanguage(value)

    // Auto-navigation after 400ms (inline implementation - KISS)
    setTimeout(() => {
      router.push('/landing/setup/explanation-1')
    }, 400)
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8">
        {/* Title */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold">
            First, select your target language
          </h1>
          <p className="text-lg text-muted-foreground">
            (the language you want to learn)
          </p>
        </div>

        {/* Radio buttons */}
        <RadioGroup value={selectedLanguage} onValueChange={handleLanguageChange}>
          <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-muted cursor-pointer">
            <RadioGroupItem value="pt-BR" id="pt-BR" />
            <Label htmlFor="pt-BR" className="flex-1 cursor-pointer text-lg">
              Portuguese (BR)
            </Label>
          </div>
          <div className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-muted cursor-pointer">
            <RadioGroupItem value="fr" id="fr" />
            <Label htmlFor="fr" className="flex-1 cursor-pointer text-lg">
              French
            </Label>
          </div>
        </RadioGroup>
      </div>
    </div>
  )
}
