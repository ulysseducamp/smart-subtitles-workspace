'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function Explanation2Page() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Explanation text */}
        <p className="text-lg">
          This will allow us to evaluate, approximately, how many of the most used words you know which will be your "vocabulary level" in Subly.
        </p>

        <p className="text-lg">
          (You'll be able to redo the test at anytime)
        </p>

        <Button
          size="lg"
          onClick={() => router.push('/landing/setup/vocab-test')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
