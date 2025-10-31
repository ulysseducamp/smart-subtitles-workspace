'use client'

export function simulateStripeCheckout(onSuccess: () => void) {
  const confirmed = window.confirm(
    '🎨 MOCKUP: Stripe Checkout\n\n' +
    'Simulate successful payment?\n' +
    '(Real Stripe integration in Phase 2B)'
  )

  if (confirmed) {
    // Simulate processing delay
    setTimeout(() => {
      alert('✅ Payment successful (mockup)')
      onSuccess()
    }, 1000)
  }
}

export function simulateStripePortal() {
  const action = window.confirm(
    '🎨 MOCKUP: Stripe Customer Portal\n\n' +
    'Simulate subscription cancellation?\n' +
    '(Real Portal opens in Phase 2B)'
  )

  if (action) {
    alert('✅ Subscription canceled (mockup)')
    // In Phase 2B, webhook will update Supabase
  }
}
