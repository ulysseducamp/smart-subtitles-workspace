'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function ReachFluencyPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Main text */}
        <div className="space-y-6 text-lg">
          <p>
            If you use Subly, you would reach the 2800 words magic treshold just by watching a few series 🤯
          </p>

          <p>
            Good news: Since you already tested your level, there are just a few steps left to set-up Subly entirely.
          </p>
        </div>

        <div className="space-y-4">
          <Button
            size="lg"
            onClick={() => router.push('/landing-v3/setup/main-struggles')}
            className="w-full md:w-auto"
          >
            Finish setting up Subly
          </Button>

          <p className="text-sm text-muted-foreground">
            (You can to that from your phone/tablet/computer)
          </p>
        </div>
      </div>
    </div>
  )
}
