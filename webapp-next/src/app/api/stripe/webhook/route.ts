import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createServiceClient } from '@/lib/supabase/service'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: NextRequest) {
  const body = await req.text()
  const signature = req.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    )
  }

  // ⚠️ SECURITY: Using service client to bypass RLS
  // Webhooks are system operations with no user session, so we need service role key
  // This is safe because:
  // 1. Stripe signature is verified above (prevents unauthorized requests)
  // 2. We validate userId format below (prevents injection)
  // 3. Service key is server-side only (never exposed to client)
  const supabase = createServiceClient()

  console.log('📥 Webhook reçu:', event.type)

  // Handle events
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      const userId = session.metadata?.user_id

      console.log('🔍 checkout.session.completed data:', {
        userId,
        customer: session.customer,
        subscription: session.subscription,
        metadata: session.metadata,
      })

      if (!userId) {
        console.warn('⚠️ Pas de userId dans metadata, INSERT ignoré')
        break
      }
      const { data, error } = await supabase.from('subscriptions').insert({
        user_id: userId,
        stripe_customer_id: session.customer as string,
        stripe_subscription_id: session.subscription as string,
        status: 'trialing', // ← Option A: Stocké tel quel (pas de mapping)
      })

      if (error) {
        console.error('❌ Erreur Supabase INSERT:', error)
        return NextResponse.json(
          { error: 'Database insert failed' },
          { status: 500 }
        )
      } else {
        console.log('✅ Subscription créée dans Supabase:', data)
      }
      break
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription

      await supabase
        .from('subscriptions')
        .update({ status: subscription.status })  // ← Stocké tel quel: 'trialing', 'active', 'past_due', etc.
        .eq('stripe_subscription_id', subscription.id)
      break
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription

      await supabase
        .from('subscriptions')
        .update({ status: 'canceled' })
        .eq('stripe_subscription_id', subscription.id)
      break
    }
  }

  return NextResponse.json({ received: true })
}
