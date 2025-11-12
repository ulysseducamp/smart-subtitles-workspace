'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

export default function ComparisonPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        Subly vs traditional apps
      </h1>

      <Image
        src="/onboarding/graph_comparison.png"
        alt="Graph comparing Subly vs traditional apps: Time vs New vocabulary acquired. Red curve (traditional apps) peaks then drops, Black curve (Subly) rises steadily"
        width={700}
        height={394}
        className="w-full max-w-xl mb-6 rounded-lg"
      />

      <p className="text-lg text-center mb-8">
        With Subly, learners stay consistent (because they learn through Netflix shows, the most engaging content in the world)
      </p>

      <Button onClick={() => router.push('/onboarding/target-language')} size="lg">
        Continue
      </Button>
    </div>
  )
}
