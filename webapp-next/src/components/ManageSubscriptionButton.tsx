'use client'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

export function ManageSubscriptionButton() {
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)

  const handleManageSubscription = async () => {
    if (!user) return

    setLoading(true)
    try {
      const response = await fetch('/api/stripe/portal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: user.id }),
      })

      const { url } = await response.json()

      if (url) {
        window.open(url, '_blank')  // Open Stripe Portal in new tab
      }
    } catch (error) {
      console.error('Portal error:', error)
      alert('Failed to open customer portal. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Button
      variant="ghost"
      onClick={handleManageSubscription}
      disabled={loading}
    >
      {loading ? 'Loading...' : 'Manage Subscription'}
    </Button>
  )
}
