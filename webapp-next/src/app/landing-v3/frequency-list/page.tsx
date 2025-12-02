'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useLandingV3 } from '@/contexts/LandingV3Context'

export default function FrequencyListPage() {
  const router = useRouter()
  const { targetLanguage } = useLandingV3()

  // Get example words based on target language
  const getExampleWords = () => {
    if (targetLanguage === 'Brazilian Portuguese') {
      return ['que', 'não', 'o']
    } else if (targetLanguage === 'French') {
      return ['un', 'le', 'être']
    }
    // Default to French if language not recognized
    return ['un', 'le', 'être']
  }

  const exampleWords = getExampleWords()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Text content with dynamic target language */}
        <div className="space-y-6 text-lg">
          <p>
            A frequency list is a list of the most used words in a language, ordered by frequency.
          </p>

          <p>
            For example the first 3 words of the <strong>{targetLanguage || 'your target language'}</strong> frequency list are :
          </p>

          <div className="space-y-1">
            {exampleWords.map((word, index) => (
              <p key={index}>- {word}</p>
            ))}
          </div>

          <p>
            (Because they are the most used words in <strong>{targetLanguage || 'that language'}</strong>)
          </p>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/studies')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
