'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/contexts/OnboardingContext'

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
  const { setNativeLang } = useOnboarding()
  const [selected, setSelected] = useState<string>('')

  const handleContinue = () => {
    setNativeLang(selected)
    router.push('/onboarding/vocab-test-intro')
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-4">
        Please select your native language
      </h1>

      <p className="text-center text-muted-foreground mb-8">
        (You will be able to change this language at anytime)
      </p>

      <RadioGroup
        value={selected}
        onValueChange={setSelected}
        className="w-full max-w-md space-y-2 max-h-96 overflow-y-auto"
      >
        {NATIVE_LANGUAGES.map((lang) => (
          <div
            key={lang.code}
            className="flex items-center space-x-2 border rounded-lg p-3 hover:bg-accent cursor-pointer"
          >
            <RadioGroupItem value={lang.code} id={lang.code} />
            <Label htmlFor={lang.code} className="flex-1 cursor-pointer">
              {lang.name}
            </Label>
          </div>
        ))}
      </RadioGroup>

      <Button
        onClick={handleContinue}
        disabled={!selected}
        size="lg"
        className="w-full max-w-md mt-8"
      >
        Continue
      </Button>
    </div>
  )
}
