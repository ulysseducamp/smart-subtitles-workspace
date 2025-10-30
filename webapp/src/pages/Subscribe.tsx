import { PricingCard } from '@/components/PricingCard'
import { simulateStripeCheckout } from '@/utils/mockups'

export default function Subscribe() {
  const handleCheckout = () => {
    simulateStripeCheckout(() => {
      window.close() // Close tab after subscription
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <PricingCard context="expired" onCheckout={handleCheckout} />
    </div>
  )
}
