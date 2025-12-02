'use client'

import { useRouter } from 'next/navigation'
import { useLandingV3 } from '@/contexts/LandingV3Context'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

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
  const { setNativeLanguage } = useLandingV3()

  const handleLanguageSelect = (languageName: string) => {
    setNativeLanguage(languageName)
    // Auto-navigation: go to next screen immediately
    router.push('/landing-v3/magic')
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8">
        {/* Title */}
        <h1 className="text-4xl font-bold text-center">
          What is your native language?
        </h1>

        {/* Language selection */}
        <RadioGroup onValueChange={handleLanguageSelect} className="space-y-4">
          {NATIVE_LANGUAGES.map((lang) => (
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
