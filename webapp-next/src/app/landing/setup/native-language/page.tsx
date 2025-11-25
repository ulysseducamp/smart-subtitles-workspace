'use client'

import { useRouter } from 'next/navigation'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useLanding } from '@/contexts/LandingContext'
import { useState } from 'react'

const NATIVE_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'French' },
  { code: 'es', name: 'Spanish' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'pl', name: 'Polish' },
  { code: 'nl', name: 'Dutch' },
  { code: 'sv', name: 'Swedish' },
  { code: 'da', name: 'Danish' },
  { code: 'cs', name: 'Czech' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' },
]

export default function NativeLanguagePage() {
  const router = useRouter()
  const { nativeLanguage, setNativeLanguage } = useLanding()
  const [selectedLanguage, setSelectedLanguage] = useState(nativeLanguage || '')

  const handleLanguageChange = (value: string) => {
    setSelectedLanguage(value)
    setNativeLanguage(value)

    // Auto-navigation after 400ms (inline implementation - KISS)
    setTimeout(() => {
      router.push('/landing/setup/auth')
    }, 400)
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8">
        {/* Title */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold">
            Select your native language
          </h1>
          <p className="text-sm text-muted-foreground">
            (You will be able to change it at anytime)
          </p>
        </div>

        {/* Radio buttons */}
        <RadioGroup value={selectedLanguage} onValueChange={handleLanguageChange}>
          {NATIVE_LANGUAGES.map((lang) => (
            <div key={lang.code} className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-muted cursor-pointer">
              <RadioGroupItem value={lang.code} id={lang.code} />
              <Label htmlFor={lang.code} className="flex-1 cursor-pointer text-lg">
                {lang.name}
              </Label>
            </div>
          ))}
        </RadioGroup>
      </div>
    </div>
  )
}
