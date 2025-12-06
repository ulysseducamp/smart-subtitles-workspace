import { NextRequest, NextResponse } from 'next/server'
import { createServiceClient } from '@/lib/supabase/service'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import { getEmail2_CancelledDuringTrial } from '@/lib/emails/templates'

/**
 * TEST ENDPOINT: Simulate customer.subscription.deleted webhook event
 *
 * Simulates Stripe subscription cancellation for testing Scenario 2 (cancellation email).
 * Bypasses Stripe signature verification - FOR STAGING TESTING ONLY.
 *
 * ⚠️ DO NOT DEPLOY TO PRODUCTION
 *
 * To test:
 * 1. Ensure test subscription exists (sub_test_scenario3_12345)
 * 2. Call: GET https://staging-subly-extension.vercel.app/api/test-webhook-subscription-deleted
 * 3. Verify email received at unducamp@gmail.com
 * 4. Call again to test anti-spam (should NOT send email twice)
 */
export async function GET(req: NextRequest) {
  console.log('🧪 TEST: Simulating customer.subscription.deleted webhook event')

  const supabase = createServiceClient()

  try {
    // Simulate subscription.deleted event
    const fakeSubscription = {
      id: 'sub_test_scenario3_12345', // Our test subscription
      status: 'canceled',
      customer: 'cus_test_scenario3',
    }

    console.log('🗑️ Simulated subscription cancellation:', {
      id: fakeSubscription.id,
      status: fakeSubscription.status,
    })

    // Execute same logic as real webhook (customer.subscription.deleted case)

    // Update subscription status to canceled
    const { data: subData, error: subError } = await supabase
      .from('subscriptions')
      .update({ status: 'canceled' })
      .eq('stripe_subscription_id', fakeSubscription.id)
      .select('user_id')
      .single()

    if (subError) {
      console.error('❌ Subscription not found:', subError)
      return NextResponse.json(
        { error: 'Subscription not found', details: subError },
        { status: 404 }
      )
    }

    // Scenario 2: Send email if cancelled DURING trial (before first payment)
    if (fakeSubscription.status === 'canceled' && subData?.user_id) {
      console.log(`👤 Found user for subscription: ${subData.user_id}`)

      // Check if cancellation email already sent (anti-spam)
      const { data: trackingData } = await supabase
        .from('user_email_tracking')
        .select('cancellation_email_sent_at')
        .eq('user_id', subData.user_id)
        .maybeSingle()

      console.log('📊 Email tracking:', trackingData)

      if (trackingData?.cancellation_email_sent_at) {
        console.log('⏭️ Cancellation email already sent - skipping')
        return NextResponse.json({
          success: true,
          message: 'Cancellation email already sent (anti-spam working)',
          alreadySent: true,
        })
      }

      // Get user email from auth.users
      const { data: userData, error: userError } =
        await supabase.auth.admin.getUserById(subData.user_id)

      if (userError || !userData?.user?.email) {
        console.error('❌ User not found:', userError)
        return NextResponse.json(
          { error: 'User not found', details: userError },
          { status: 404 }
        )
      }

      console.log(
        `📧 Sending cancellation email to ${userData.user.email} (cancelled during trial)`
      )

      // Send email
      const emailResult = await sendEmailFromTemplate(
        userData.user.email,
        getEmail2_CancelledDuringTrial()
      )

      if (emailResult.success) {
        console.log(`✅ Cancellation email sent (${emailResult.emailId})`)

        // Update tracking: cancellation email sent + had_subscription (for Scenario 1)
        const { error: upsertError } = await supabase
          .from('user_email_tracking')
          .upsert(
            {
              user_id: subData.user_id,
              cancellation_email_sent_at: new Date().toISOString(),
              had_subscription: true,
            },
            {
              onConflict: 'user_id',
            }
          )

        if (upsertError) {
          console.error('❌ Failed to update tracking:', upsertError)
        }

        return NextResponse.json({
          success: true,
          message: 'Cancellation email sent successfully',
          emailId: emailResult.emailId,
          recipient: userData.user.email,
        })
      } else {
        console.error(`❌ Failed to send email:`, emailResult.error)
        return NextResponse.json(
          { error: 'Failed to send email', details: emailResult.error },
          { status: 500 }
        )
      }
    }

    return NextResponse.json({
      success: false,
      message: 'No action taken (subscription not canceled)',
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
