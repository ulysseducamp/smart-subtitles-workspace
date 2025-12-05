import { NextRequest, NextResponse } from 'next/server'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import {
  getEmail1_NoCreditCard,
  getEmail2_CancelledDuringTrial,
  getEmail3_FirstPayment,
} from '@/lib/emails/templates'

/**
 * Test route to send all 3 email templates to unducamp.pro@gmail.com
 * Use this to verify email rendering and reply-to functionality
 *
 * Usage: GET http://localhost:3000/api/test-email-templates
 */
export async function GET(req: NextRequest) {
  const testEmail = 'unducamp.pro@gmail.com'

  console.log('📧 Testing all 3 email templates...')

  try {
    // Send email 1: No credit card after 2h
    const result1 = await sendEmailFromTemplate(testEmail, getEmail1_NoCreditCard())

    // Wait 1 second between emails to avoid rate limiting
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Send email 2: Cancelled during trial
    const result2 = await sendEmailFromTemplate(
      testEmail,
      getEmail2_CancelledDuringTrial()
    )

    // Wait 1 second between emails
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Send email 3: First payment
    const result3 = await sendEmailFromTemplate(testEmail, getEmail3_FirstPayment())

    // Check results
    const allSuccess = result1.success && result2.success && result3.success

    if (!allSuccess) {
      console.error('❌ Some emails failed:', {
        email1: result1,
        email2: result2,
        email3: result3,
      })
      return NextResponse.json(
        {
          success: false,
          message: 'Some emails failed to send',
          results: { email1: result1, email2: result2, email3: result3 },
        },
        { status: 500 }
      )
    }

    console.log('✅ All 3 emails sent successfully!')
    return NextResponse.json({
      success: true,
      message: `3 test emails sent to ${testEmail}`,
      results: {
        email1: result1,
        email2: result2,
        email3: result3,
      },
    })
  } catch (err) {
    console.error('❌ Exception testing email templates:', err)
    return NextResponse.json(
      {
        success: false,
        error: String(err),
      },
      { status: 500 }
    )
  }
}
