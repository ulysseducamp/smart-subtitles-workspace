'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

export default function Explanation3Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">
        If a subtitle contains exactly one word that you don't know
      </h1>

      <Image
        src="/onboarding/one_unknown-before.png"
        alt="Subtitle analysis: Je le souhaite vraiment with one unknown word marked in red"
        width={500}
        height={125}
        className="w-full max-w-md mb-6 rounded-lg"
      />

      <p className="text-lg mb-6">
        → Subly displays it in your target language with the translation of the unknown word
      </p>

      <Image
        src="/onboarding/one_unknown-after.png"
        alt="Displayed subtitle: Je le souhaite vraiment (really) with inline translation"
        width={500}
        height={125}
        className="w-full max-w-md mb-4 rounded-lg"
      />

      <p className="text-sm text-muted-foreground mb-8">
        (so you can learn new words without needing to click)
      </p>

      <Button onClick={() => router.push('/onboarding/explanation-4')} size="lg" className="self-start">
        Ok
      </Button>
    </div>
  )
}
