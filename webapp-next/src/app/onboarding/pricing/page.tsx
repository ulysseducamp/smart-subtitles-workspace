'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { PricingCard } from '@/components/PricingCard'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function Pricing() {
  const { user, signOut } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!user) return

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
