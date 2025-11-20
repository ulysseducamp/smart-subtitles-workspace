'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'

export default function VocabTestExplanationPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <div className="space-y-6 mb-8">
        <p className="text-lg text-center">
          We'll show you words selected from this list and you'll tell us if you know them or not.
        </p>

        <p className="text-lg text-center">
          This will allow us to evaluate, approximately, how many of the most used words you know, which will be your 'vocabulary level' in Subly.
        </p>

        <p className="text-center text-muted-foreground">
          (You'll be able to redo the test at anytime)
        </p>
      </div>

      <Button onClick={() => router.push('/vocab-test/test?level=100')} size="lg">
        Start
      </Button>
    </div>
  )
}
