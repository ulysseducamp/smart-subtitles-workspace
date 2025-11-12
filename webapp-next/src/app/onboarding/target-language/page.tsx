'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/contexts/OnboardingContext'

export default function TargetLanguagePage() {
  const router = useRouter()
  const { setTargetLang } = useOnboarding()
  const [selected, setSelected] = useState<string>('')

  const handleContinue = () => {
    setTargetLang(selected)
    router.push('/onboarding/native-language')
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-4">
        Please select your target language
      </h1>

      <p className="text-center text-muted-foreground mb-8">
        (the language you want to learn)
      </p>

      <RadioGroup
        value={selected}
        onValueChange={setSelected}
        className="w-full max-w-md space-y-3"
      >
        <div className="flex items-center space-x-2 border rounded-lg p-4 hover:bg-accent cursor-pointer">
          <RadioGroupItem value="fr" id="fr" />
          <Label htmlFor="fr" className="flex-1 cursor-pointer">
            French
          </Label>
        </div>

        <div className="flex items-center space-x-2 border rounded-lg p-4 hover:bg-accent cursor-pointer">
          <RadioGroupItem value="pt-BR" id="pt-BR" />
          <Label htmlFor="pt-BR" className="flex-1 cursor-pointer">
            Brazilian Portuguese
          </Label>
        </div>
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
