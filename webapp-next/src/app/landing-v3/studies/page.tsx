'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function StudiesPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Text content - "studies" is normal text (not a link, not bold) */}
        <div className="space-y-6 text-lg">
          <p>
            Studies have shown that you only need to know:
          </p>

          <div className="space-y-2">
            <p>
              - 1000 of the most used words to cover 72% of any conversation
            </p>
            <p>
              - 2800 of the most used words to cover 93% of any conversation
            </p>
          </div>
        </div>

        <Button
          size="lg"
          onClick={() => router.push('/landing-v3/belief')}
          className="w-full md:w-auto"
        >
          Continue
        </Button>
      </div>
    </div>
  )
}
