import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: NextRequest) {
  try {
    const { userId, email } = await req.json()

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      customer_email: email,
      line_items: [
        {
          price: process.env.STRIPE_PRICE_ID, // $1/month
          quantity: 1,
        },
      ],
      subscription_data: {
        trial_period_days: 3,
        metadata: { user_id: userId },
      },
      metadata: { user_id: userId }, // ← Aussi au niveau session pour webhook checkout.session.completed
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/complete`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/onboarding/pricing-details`,
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('Stripe checkout error:', error)
    return NextResponse.json(
      { error: 'Failed to create checkout session' },
      { status: 500 }
    )
  }
}
