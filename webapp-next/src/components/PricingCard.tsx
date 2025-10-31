'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface PricingCardProps {
  context: 'onboarding' | 'expired'
  onCheckout: () => void
}

export function PricingCard({ context, onCheckout }: PricingCardProps) {
  const title = context === 'onboarding'
    ? 'Start Your 14-Day Free Trial'
    : 'Subscribe to continue'

  const subtitle = context === 'expired'
    ? 'Get unlimited access to Subly for $1/month'
    : null

  const buttonText = context === 'onboarding'
    ? 'Start Free Trial'
    : 'Subscribe Now'

  const trialEndDate = new Date()
  trialEndDate.setDate(trialEndDate.getDate() + 14)

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {subtitle && (
          <p className="text-sm text-muted-foreground mt-2">
            {subtitle}
          </p>
        )}
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="text-center">
          <p className="text-4xl font-bold">$1/month</p>
          {context === 'onboarding' && (
            <p className="text-sm text-muted-foreground">
              Special price for first 10 users
            </p>
          )}
        </div>

        <ul className="space-y-2">
          <li>✅ Adapt subtitles to your level</li>
          <li>✅ AI inline translations</li>
          <li>✅ Works on any device</li>
          <li>✅ Cancel anytime</li>
        </ul>

        {context === 'onboarding' && (
          <p className="text-sm text-muted-foreground">
            Trial ends: {trialEndDate.toLocaleDateString()}
            <br />
            You won't be charged until then
          </p>
        )}

        <Button onClick={onCheckout} size="lg" className="w-full">
          {buttonText}
        </Button>
      </CardContent>
    </Card>
  )
}
