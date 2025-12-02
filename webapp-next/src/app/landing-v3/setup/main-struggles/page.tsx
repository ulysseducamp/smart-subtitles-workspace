'use client'

import { useRouter } from 'next/navigation'
import { useLandingV3 } from '@/contexts/LandingV3Context'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export default function MainStrugglesPage() {
  const router = useRouter()
  const { targetLanguage, setMainStruggle } = useLandingV3()

  const handleChoice = (struggle: string) => {
    setMainStruggle(struggle)
    router.push('/landing-v3/setup/you-are-in-good-hands')
  }

  const options = [
    { value: 'grammar', label: 'Grammar' },
    { value: 'writing', label: 'Writing' },
    { value: 'listening', label: 'Listening comprehension' },
    { value: 'speaking', label: 'Speaking' },
    { value: 'reading', label: 'Reading comprehension' }
  ]

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          What is your main struggle with learning {targetLanguage}?
        </h1>

        {/* Radio options */}
        <RadioGroup onValueChange={handleChoice} className="space-y-4">
          {options.map((option) => (
            <div
              key={option.value}
              className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-accent cursor-pointer transition-colors"
              onClick={() => handleChoice(option.value)}
            >
              <RadioGroupItem value={option.value} id={option.value} />
              <Label
                htmlFor={option.value}
                className="flex-1 cursor-pointer text-lg font-medium"
              >
                {option.label}
              </Label>
            </div>
          ))}
        </RadioGroup>
      </div>
    </div>
  )
}
