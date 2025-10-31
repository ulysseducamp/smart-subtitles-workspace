'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { PricingCard } from '@/components/PricingCard'
import { simulateStripeCheckout } from '@/utils/mockups'
import { useRouter } from 'next/navigation'

export default function Pricing() {
  const { signOut } = useAuth()
  const router = useRouter()

  const handleCheckout = () => {
    simulateStripeCheckout(() => {
      router.push('/onboarding/pin-extension')
    })
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button */}
      <div className="absolute top-4 right-4">
        <Button variant="ghost" onClick={signOut}>
          Log out
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <PricingCard context="onboarding" onCheckout={handleCheckout} />
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
