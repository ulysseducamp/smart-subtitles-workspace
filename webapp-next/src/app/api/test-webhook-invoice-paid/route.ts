import { NextRequest, NextResponse } from 'next/server'
import { createServiceClient } from '@/lib/supabase/service'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import { getEmail3_FirstPayment } from '@/lib/emails/templates'

/**
 * TEST ENDPOINT: Simulate invoice.paid webhook event
 *
 * Simulates Stripe invoice.paid event for testing Scenario 3 (first payment email).
 * Bypasses signature verification - FOR STAGING TESTING ONLY.
 *
 * ⚠️ DO NOT DEPLOY TO PRODUCTION
 *
 * To test:
 * 1. Ensure test subscription exists (sub_test_scenario3_12345)
 * 2. Call: GET https://staging-subly-extension.vercel.app/api/test-webhook-invoice-paid
 * 3. Verify email received at unducamp@gmail.com
 * 4. Call again to test anti-spam (should NOT send email twice)
 */
export async function GET(req: NextRequest) {
  console.log('🧪 TEST: Simulating invoice.paid webhook event')

  const supabase = createServiceClient()

  try {
    // Simulate invoice.paid event with billing_reason = subscription_cycle
    const fakeInvoice = {
      id: 'in_test_' + Date.now(),
      subscription: 'sub_test_scenario3_12345', // Our test subscription
      billing_reason: 'subscription_cycle', // First payment after trial
      amount_paid: 900, // $9.00
      currency: 'usd',
    }

    console.log('📄 Simulated invoice:', {
      id: fakeInvoice.id,
      subscription: fakeInvoice.subscription,
      billing_reason: fakeInvoice.billing_reason,
    })

    // Execute same logic as real webhook (invoice.paid case)
    if (
      fakeInvoice.billing_reason === 'subscription_cycle' &&
      fakeInvoice.subscription
    ) {
      // Check if this is the FIRST invoice for this subscription
      const { data: subData, error: subError } = await supabase
        .from('subscriptions')
        .select('user_id')
        .eq('stripe_subscription_id', fakeInvoice.subscription)
        .single()

      if (subError) {
        console.error('❌ Subscription not found:', subError)
        return NextResponse.json(
          { error: 'Subscription not found', details: subError },
          { status: 404 }
        )
      }

      if (subData?.user_id) {
        console.log(`👤 Found user for subscription: ${subData.user_id}`)

        // Check if first payment email already sent
        const { data: trackingData } = await supabase
          .from('user_email_tracking')
          .select('user_id, had_subscription')
          .eq('user_id', subData.user_id)
          .maybeSingle()

        console.log('📊 Email tracking:', trackingData)

        if (trackingData?.had_subscription === true) {
          console.log('⏭️ First payment email already sent - skipping')
          return NextResponse.json({
            success: true,
            message: 'First payment email already sent (anti-spam working)',
            alreadySent: true,
          })
        }

        // Fetch user email
        const { data: userData, error: userError } =
          await supabase.auth.admin.getUserById(subData.user_id)

        if (userError || !userData?.user?.email) {
          console.error('❌ User not found:', userError)
          return NextResponse.json(
            { error: 'User not found', details: userError },
            { status: 404 }
          )
        }

        console.log(`📧 Sending first payment email to ${userData.user.email}`)

        // Send email
        const emailResult = await sendEmailFromTemplate(
          userData.user.email,
          getEmail3_FirstPayment()
        )

        if (emailResult.success) {
          console.log(`✅ Email sent (ID: ${emailResult.emailId})`)

          // Update tracking
          const { error: upsertError } = await supabase
            .from('user_email_tracking')
            .upsert(
              {
                user_id: subData.user_id,
                had_subscription: true,
              },
              { onConflict: 'user_id' }
            )

          if (upsertError) {
            console.error('❌ Failed to update tracking:', upsertError)
          }

          return NextResponse.json({
            success: true,
            message: 'First payment email sent successfully',
            emailId: emailResult.emailId,
            recipient: userData.user.email,
          })
        } else {
          console.error('❌ Failed to send email:', emailResult.error)
          return NextResponse.json(
            { error: 'Failed to send email', details: emailResult.error },
            { status: 500 }
          )
        }
      }
    }

    return NextResponse.json({
      success: false,
      message: 'No action taken (billing_reason not subscription_cycle)',
    })
  } catch (err) {
    console.error('❌ TEST webhook exception:', err)
    return NextResponse.json(
      {
        success: false,
        error: String(err),
      },
      { status: 500 }
    )
  }
}
