'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Lightbulb } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export default function PricingPage() {
  const router = useRouter()
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!user) {
      alert('Please sign in first')
      router.push('/landing/setup/auth')
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
          successUrl: '/landing/setup/complete',
          cancelUrl: '/landing/setup/pricing',
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
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold">
          Start your 3-day FREE trial to continue
        </h1>

        {/* Timeline */}
        <div className="flex flex-col items-start max-w-xl mx-auto text-left">
          {/* Today */}
          <div className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="h-6 w-6 rounded-full bg-foreground flex-shrink-0"></div>
              <div className="w-0.5 flex-1 bg-foreground"></div>
            </div>
            <div className="flex-1 space-y-1 pb-6">
              <h3 className="text-xl font-semibold">Today</h3>
              <p className="text-sm text-muted-foreground">
                Receive an email to download the extension already set up for you
              </p>
            </div>
          </div>

          {/* In 3 days */}
          <div className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="h-6 w-6 rounded-full bg-foreground flex-shrink-0"></div>
            </div>
            <div className="flex-1 space-y-1">
              <h3 className="text-xl font-semibold">In 3 days - Billing</h3>
              <p className="text-sm text-muted-foreground">
                You'll be charged, unless you cancel before.
              </p>
            </div>
          </div>
        </div>

        {/* CTA section with 16px spacing */}
        <div className="space-y-4">
          {/* Good to know */}
          <div className="flex items-start gap-3 text-left bg-muted p-4 rounded-lg max-w-xl mx-auto">
            <Lightbulb className="h-5 w-5 mt-1 flex-shrink-0" />
            <p className="text-sm">
              <strong>Good to know:</strong> You'll be able to cancel your trial at any time through the "manage subscription" button
            </p>
          </div>

          {/* Button */}
          <Button
            size="lg"
            onClick={handleCheckout}
            className="w-full md:w-auto"
            disabled={loading || !user}
          >
            {loading ? 'Loading...' : 'Start My 3-Day Free Trial'}
          </Button>

          {/* Pricing info */}
          <p className="text-base text-muted-foreground">
            3 days free, then just 19,99$ per year (1,67$/mo)
          </p>
        </div>
      </div>
    </div>
  )
}
