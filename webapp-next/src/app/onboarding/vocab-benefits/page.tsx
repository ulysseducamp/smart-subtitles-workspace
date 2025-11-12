'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'

export default function VocabBenefitsPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <p className="text-lg text-center mb-6">
        On average, users with this level acquire <strong>30 new words per episode</strong>.
      </p>

      <p className="text-lg text-center mb-12">
        Which means you will double the number of words you know just by watching a few series with Subly 🥳
      </p>

      <Button onClick={() => router.push('/onboarding/auth')} size="lg">
        Ok
      </Button>
    </div>
  )
}
