import { Button } from '@/components/ui/button'
import { simulateStripePortal } from '@/utils/mockups'

export function ManageSubscriptionButton() {
  return (
    <Button variant="ghost" onClick={simulateStripePortal}>
      Manage Subscription
    </Button>
  )
}
