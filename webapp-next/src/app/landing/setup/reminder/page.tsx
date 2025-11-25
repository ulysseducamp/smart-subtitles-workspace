'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Check, Mail } from 'lucide-react'

export default function ReminderPage() {
  const router = useRouter()

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center">
        {/* Title */}
        <h1 className="text-4xl font-bold mb-8">
          We'll send you a reminder before your trial ends
        </h1>

        {/* Mail icon with notification badge */}
        <div className="flex justify-center mb-8">
          <div className="relative">
            <Mail className="h-32 w-32" strokeWidth={1.5} />
            <div className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full h-12 w-12 flex items-center justify-center text-xl font-bold">
              1
            </div>
          </div>
        </div>

        {/* CTA section with 16px spacing */}
        <div className="space-y-4">
          {/* No Payment Due Now */}
          <div className="flex items-center justify-center gap-2 text-base">
            <Check className="h-5 w-5" />
            <span>No Payment Due Now</span>
          </div>

          {/* Button */}
          <Button
            size="lg"
            onClick={() => router.push('/landing/setup/pricing')}
            className="w-full md:w-auto"
          >
            Continue for FREE
          </Button>

          {/* Pricing info */}
          <p className="text-base text-muted-foreground">
            After, Just 9$ per year (0,75$/mo)
          </p>
        </div>
      </div>
    </div>
  )
}
