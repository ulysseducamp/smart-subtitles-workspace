'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

export default function Explanation2Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">
        If a subtitle contains only words that you know
      </h1>

      <Image
        src="/onboarding/known_words-before.png"
        alt="Subtitle analysis: Je le souhaite vraiment with green annotations showing all known words"
        width={500}
        height={125}
        className="w-full max-w-md mb-6 rounded-lg"
      />

      <p className="text-lg mb-6">
        → Subly displays it in your target language
      </p>

      <Image
        src="/onboarding/known_words-after.png"
        alt="Displayed subtitle: Je le souhaite vraiment in French"
        width={500}
        height={125}
        className="w-full max-w-md mb-4 rounded-lg"
      />

      <p className="text-sm text-muted-foreground mb-8">
        (Since you know all the necessary words to understand it)
      </p>

      <Button onClick={() => router.push('/onboarding/explanation-3')} size="lg" className="self-start">
        Ok
      </Button>
    </div>
  )
}
