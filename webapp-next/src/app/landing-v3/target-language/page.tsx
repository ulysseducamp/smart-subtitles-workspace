'use client'

import { useRouter } from 'next/navigation'
import { useLandingV3 } from '@/contexts/LandingV3Context'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const TARGET_LANGUAGES = [
  { code: 'fr', name: 'French' },
  { code: 'pt-BR', name: 'Brazilian Portuguese' },
]

export default function TargetLanguagePage() {
  const router = useRouter()
  const { setTargetLanguage } = useLandingV3()

  const handleLanguageSelect = (languageName: string) => {
    setTargetLanguage(languageName)
    // Auto-navigation: go to next screen immediately
    router.push('/landing-v3/native-language')
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Header text */}
        <p className="text-lg text-muted-foreground">
          Quick question to adapt our explanations
        </p>

        {/* Title */}
        <h1 className="text-4xl font-bold">
          What is your target language?
        </h1>

        {/* Subtitle */}
        <p className="text-base text-muted-foreground">
          (the language you are learning)
        </p>

        {/* Language selection */}
        <RadioGroup onValueChange={handleLanguageSelect} className="space-y-4">
          {TARGET_LANGUAGES.map((lang) => (
            <div
              key={lang.code}
              className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-accent cursor-pointer transition-colors"
              onClick={() => handleLanguageSelect(lang.name)}
            >
              <RadioGroupItem value={lang.name} id={lang.code} />
              <Label
                htmlFor={lang.code}
                className="flex-1 cursor-pointer text-lg font-medium"
              >
                {lang.name}
              </Label>
            </div>
          ))}
        </RadioGroup>
      </div>
    </div>
  )
}
