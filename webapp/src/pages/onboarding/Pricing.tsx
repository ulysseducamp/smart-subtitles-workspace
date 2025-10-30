import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { PricingCard } from '@/components/PricingCard'
import { simulateStripeCheckout } from '@/utils/mockups'

export default function Pricing() {
  const navigate = useNavigate()
  const { user, signOut } = useAuth()

  const handleCheckout = () => {
    simulateStripeCheckout(() => {
      navigate('/onboarding/pin-extension')
    })
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button */}
      {user && (
        <div className="absolute top-4 right-4">
          <Button variant="ghost" onClick={signOut}>
            Log out
          </Button>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex items-center justify-center p-8">
        <PricingCard context="onboarding" onCheckout={handleCheckout} />
      </div>
    </div>
  )
}
