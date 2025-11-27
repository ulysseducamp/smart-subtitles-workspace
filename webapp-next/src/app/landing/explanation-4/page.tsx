'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { ArrowDown } from 'lucide-react'

export default function Explanation4Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          If a subtitle contains exactly one word that you don't know
        </h1>

        {/* Arrow */}
        <div className="flex justify-center">
          <ArrowDown className="h-12 w-12 text-muted-foreground" />
        </div>

        {/* Subtitle */}
        <h2 className="text-3xl font-bold">
          Subly displays it with the translation of the unknown word
        </h2>

        {/* Inline translation example */}
        <div className="flex flex-col items-center gap-4">
          <p className="text-lg">(like this 👇)</p>
          <img
            src="/landing/explanation-inline-translation.png"
            alt="Example of inline translation in subtitle"
            className="w-full max-w-md"
          />
        </div>

        {/* Explanation text */}
        <p className="text-lg">
          (So you can learn new words on the go)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/explanation-5')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
