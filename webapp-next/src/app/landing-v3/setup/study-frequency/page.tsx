'use client'

import { useRouter } from 'next/navigation'
import { useLandingV3 } from '@/contexts/LandingV3Context'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export default function StudyFrequencyPage() {
  const router = useRouter()
  const { targetLanguage, setStudyFrequency } = useLandingV3()

  const handleChoice = (frequency: string) => {
    setStudyFrequency(frequency)
    router.push('/landing-v3/setup/comparison')
  }

  const options = [
    { value: 'more-than-5', label: 'more than 5 times per week' },
    { value: '3-5', label: '3-5 times per week' },
    { value: '1-2', label: '1-2 times per week' },
    { value: 'less-than-1', label: 'less than 1 time per week' }
  ]

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          Currently, how often do you study/practice/learn {targetLanguage}?
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
