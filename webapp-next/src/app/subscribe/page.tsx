'use client'

import { PricingCard } from '@/components/PricingCard'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export default function Subscribe() {
  const { user } = useAuth()
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
    <div className="min-h-screen flex items-center justify-center p-8">
      <PricingCard context="expired" onCheckout={handleCheckout} />
    </div>
  )
}
