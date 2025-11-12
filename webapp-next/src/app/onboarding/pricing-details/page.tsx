'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export default function PricingDetailsPage() {
  const router = useRouter()
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!user) {
      alert('Please sign in first')
      router.push('/onboarding/auth')
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user.id,
          email: user.email,
        }),
      })

      const { url } = await response.json()

      if (url) {
        window.location.href = url  // Redirect to Stripe Checkout
      }
    } catch (error) {
      console.error('Checkout error:', error)
      alert('Failed to start checkout. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-12">
        Start your 3-day FREE trial to continue
      </h1>

      {/* Timeline verticale */}
      <div className="w-full max-w-md mb-8">
        <div className="relative pl-8 pb-8 border-l-2 border-border">
          <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-foreground" />
          <div className="mb-2">
            <h3 className="font-bold text-lg">Today</h3>
            <p className="text-muted-foreground">Unlock the full potential of Subly</p>
          </div>
        </div>

        <div className="relative pl-8">
          <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-foreground" />
          <div>
            <h3 className="font-bold text-lg">In 3 days - Billing</h3>
            <p className="text-muted-foreground">You'll be charged $9/year, unless you cancel before.</p>
          </div>
        </div>
      </div>

      {/* Good to know */}
      <div className="w-full max-w-md mb-12 p-4 bg-muted rounded-lg">
        <p className="text-sm">
          <strong>Good to know:</strong> You'll be able to cancel your trial at any time through the 'manage subscription' button
        </p>
      </div>

      <Button
        onClick={handleCheckout}
        size="lg"
        className="mb-4"
        disabled={loading || !user}
      >
        {loading ? 'Loading...' : 'Start My 3-Day Free Trial'}
      </Button>

      <p className="text-center text-muted-foreground">
        3 days free, then just <strong>$9/year</strong>
      </p>
    </div>
  )
}
