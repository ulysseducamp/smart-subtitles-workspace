'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import Image from 'next/image'

export default function ComparisonPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-3xl font-bold">
          Subly vs traditional apps
        </h1>

        {/* Comparison graph */}
        <div className="flex justify-center">
          <Image
            src="/landing/comparison-graph.png"
            alt="Subly vs traditional apps comparison"
            width={600}
            height={400}
            className="rounded-lg"
          />
        </div>

        {/* Explanation text */}
        <p className="text-lg">
          With Subly, learners stay consistent in the long run (because they learn through Netflix shows, the most engaging content in the world)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/setup/auth')}
          className="w-full md:w-auto"
        >
          Ok
        </Button>
      </div>
    </div>
  )
}
