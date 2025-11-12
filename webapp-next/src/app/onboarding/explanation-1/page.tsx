'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

export default function Explanation1Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        Subly's magic
      </h1>

      <Image
        src="/onboarding/S+N=wand.png"
        alt="Subly magic formula: S + N = wand"
        width={700}
        height={394}
        className="w-full max-w-xl mb-8 rounded-lg"
      />

      <p className="text-lg text-center mb-8">
        When watching Netflix, based on your level, Subly choose if a subtitle should be displayed in your target language or in your native language
      </p>

      <Button onClick={() => router.push('/onboarding/explanation-2')} size="lg">
        Ok
      </Button>
    </div>
  )
}
