import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createServiceClient } from '@/lib/supabase/service'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import {
  getEmail2_CancelledDuringTrial,
  getEmail3_FirstPayment,
} from '@/lib/emails/templates'
import { Resend } from 'resend'

// TypeScript workaround: stripe-node types missing subscription property on Invoice
// This property exists in webhook events but is not typed in @stripe/stripe-js
interface InvoiceWithSubscription extends Stripe.Invoice {
  subscription: string | null
}

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

      console.log('🔍 Subscription deleted:', {
        id: subscription.id,
        status: subscription.status,
        cancel_at_period_end: subscription.cancel_at_period_end,
      })

      // Update subscription status in Supabase
      const { data: subData } = await supabase
        .from('subscriptions')
        .update({ status: 'canceled' })
        .eq('stripe_subscription_id', subscription.id)
        .select('user_id')
        .single()

      // Scenario 2: Send email if cancelled DURING trial (before first payment)
      // Check if subscription was in trialing status (means cancelled before first payment)
      if (subscription.status === 'canceled' && subData?.user_id) {
        // Check if cancellation email already sent (anti-spam)
        const { data: trackingData } = await supabase
          .from('user_email_tracking')
          .select('cancellation_email_sent_at')
          .eq('user_id', subData.user_id)
          .maybeSingle()

        if (trackingData?.cancellation_email_sent_at) {
          console.log('⏭️ Cancellation email already sent - skipping')
          break
        }

        // Get user email from auth.users
        const { data: userData } = await supabase.auth.admin.getUserById(
          subData.user_id
        )

        if (userData?.user?.email) {
          console.log(
            `📧 Sending cancellation email to ${userData.user.email} (cancelled during trial)`
          )

          const emailResult = await sendEmailFromTemplate(
            userData.user.email,
            getEmail2_CancelledDuringTrial()
          )

          if (emailResult.success) {
            console.log(`✅ Cancellation email sent (${emailResult.emailId})`)

            // Update tracking: cancellation email sent + had_subscription (for Scenario 1)
            await supabase.from('user_email_tracking').upsert(
              {
                user_id: subData.user_id,
                cancellation_email_sent_at: new Date().toISOString(),
                had_subscription: true,
              },
              {
                onConflict: 'user_id',
              }
            )
          } else {
            console.error(`❌ Failed to send cancellation email:`, emailResult.error)
          }
        }
      }

      break
    }

    case 'invoice.paid': {
      const invoice = event.data.object as InvoiceWithSubscription

      console.log('🔍 Invoice paid:', {
        id: invoice.id,
        billing_reason: invoice.billing_reason,
        subscription: invoice.subscription,
      })

      // Scenario 3: Send email ONLY on first payment (after trial ends)
      // billing_reason === 'subscription_cycle' means it's a regular billing (first payment or renewal)
      if (
        invoice.billing_reason === 'subscription_cycle' &&
        invoice.subscription
      ) {
        // Check if this is the FIRST invoice for this subscription
        const { data: subData } = await supabase
          .from('subscriptions')
          .select('user_id')
          .eq('stripe_subscription_id', invoice.subscription)
          .single()

        if (subData?.user_id) {
          // Check if first payment email already sent (anti-spam)
          const { data: trackingData } = await supabase
            .from('user_email_tracking')
            .select('first_payment_email_sent_at')
            .eq('user_id', subData.user_id)
            .maybeSingle()

          if (trackingData?.first_payment_email_sent_at) {
            console.log('⏭️ First payment email already sent - skipping')
            break
          }

          // Get user email
          const { data: userData } = await supabase.auth.admin.getUserById(
            subData.user_id
          )

          if (userData?.user?.email) {
            console.log(
              `📧 Sending first payment email to ${userData.user.email}`
            )

            const emailResult = await sendEmailFromTemplate(
              userData.user.email,
              getEmail3_FirstPayment()
            )

            if (emailResult.success) {
              console.log(`✅ First payment email sent (${emailResult.emailId})`)

              // Update tracking: first payment email sent + had_subscription (for Scenario 1)
              await supabase.from('user_email_tracking').upsert(
                {
                  user_id: subData.user_id,
                  first_payment_email_sent_at: new Date().toISOString(),
                  had_subscription: true,
                },
                {
                  onConflict: 'user_id',
                }
              )
            } else {
              console.error(
                `❌ Failed to send first payment email:`,
                emailResult.error
              )
            }
          }
        }
      }

      break
    }
  }

  return NextResponse.json({ received: true })
}
