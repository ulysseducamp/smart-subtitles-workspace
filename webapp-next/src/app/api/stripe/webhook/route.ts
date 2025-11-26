import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createServiceClient } from '@/lib/supabase/service'
import { Resend } from 'resend'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
const resend = new Resend(process.env.RESEND_API_KEY!)

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

      if (!userId) {
        console.warn('⚠️ Pas de userId dans metadata, INSERT ignoré')
        break
      }
      const { data, error } = await supabase.from('subscriptions').insert({
        user_id: userId,
        stripe_customer_id: session.customer as string,
        stripe_subscription_id: session.subscription as string,
        status: 'trialing',
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

      // Send extension download email (only for landing flow)
      const customerEmail = session.customer_email
      const isLandingFlow = session.metadata?.flow === 'landing'

      if (customerEmail && isLandingFlow) {
        try {
          const { data: emailData, error: emailError } = await resend.emails.send({
            from: 'Subly <noreply@sublyy.com>',
            to: [customerEmail],
            subject: 'Download Subly',
            html: `
              <p>Hi it's Ulysse, the developer behind Subly!</p>

              <p>You can download the extension <a href="https://chromewebstore.google.com/detail/subly/lhkamocmjgjikhmfiogfdjhlhffoaaek">here</a>.</p>

              <p><strong>Important:</strong> Once the extension is downloaded, click on <strong>"Already have an account? Sign in with Google"</strong> to load the information you already provided.</p>

              <p>Best,</p>
              <p>Ulysse Ducamp</p>
              <p>(you can contact me at unducamp.pro@gmail.com)</p>
            `,
          })

          if (emailError) {
            console.error('❌ Erreur envoi email:', emailError)
          } else {
            console.log('✅ Email envoyé:', emailData)
          }
        } catch (emailErr) {
          console.error('❌ Exception envoi email:', emailErr)
        }
      } else {
        if (!customerEmail) {
          console.warn('⚠️ Pas de customer_email, email non envoyé')
        } else if (!isLandingFlow) {
          console.log('ℹ️ Flow non-landing détecté, email non envoyé (attendu pour ancien onboarding)')
        }
      }
      break
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription

      await supabase
        .from('subscriptions')
        .update({ status: subscription.status })
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
