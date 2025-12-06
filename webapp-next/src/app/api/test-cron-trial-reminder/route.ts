import { NextRequest, NextResponse } from 'next/server'
import { createServiceClient } from '@/lib/supabase/service'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import { getEmail1_NoCreditCard } from '@/lib/emails/templates'

/**
 * TEST ENDPOINT: Trial reminder cron with email whitelist
 *
 * Same logic as /api/cron/trial-reminder but ONLY processes whitelisted emails.
 * This allows safe testing in staging without sending emails to real users.
 *
 * ⚠️ FOR TESTING ONLY - Whitelist: unducamp@gmail.com
 *
 * To test:
 * 1. Create user with unducamp@gmail.com in staging
 * 2. Manually update created_at in Supabase to simulate "2h30 ago"
 * 3. Call: GET https://staging-subly-extension.vercel.app/api/test-cron-trial-reminder
 * 4. Verify email received
 */
export async function GET(req: NextRequest) {
  console.log('🧪 TEST: Trial reminder check started (with email whitelist)')

  // ⚠️ WHITELIST: Only process these emails (prevents sending to real users)
  const TEST_EMAIL_WHITELIST = ['unducamp@gmail.com']

  // ⚠️ SECURITY: Using service client to bypass RLS
  // This is safe because:
  // 1. Test endpoint with email whitelist
  // 2. We need to query across auth.users and public tables
  // 3. Service key is server-side only (never exposed to client)
  const supabase = createServiceClient()

  try {
    // Calculate time window: 2-27 hours ago
    // Min 2h: Give users time to add their credit card
    // Max 27h: Avoid processing old users + reduce DB load
    const now = new Date()
    const twoHoursAgo = new Date(now.getTime() - 2 * 60 * 60 * 1000)
    const twentySevenHoursAgo = new Date(now.getTime() - 27 * 60 * 60 * 1000)

    console.log('🔍 Looking for users created between:', {
      start: twentySevenHoursAgo.toISOString(),
      end: twoHoursAgo.toISOString(),
      whitelist: TEST_EMAIL_WHITELIST,
    })

    // Step 1: Fetch last 100 users via Admin API (auth.users is protected)
    const { data: allUsersData, error: usersError } =
      await supabase.auth.admin.listUsers({
        page: 1,
        perPage: 100,
      })

    if (usersError) {
      console.error('❌ Error fetching users:', usersError)
      return NextResponse.json(
        { error: 'Failed to fetch users', details: usersError },
        { status: 500 }
      )
    }

    // Sort by created_at desc to get most recent first
    const sortedUsers = [...allUsersData.users].sort(
      (a, b) => new Date(b.created_at!).getTime() - new Date(a.created_at!).getTime()
    )

    const recentUsers = sortedUsers
      .filter((user) => {
        if (!user.created_at || !user.email) return false
        const createdAt = new Date(user.created_at)
        return createdAt >= twentySevenHoursAgo && createdAt <= twoHoursAgo
      })
      .map((user) => ({
        id: user.id,
        email: user.email!,
        created_at: user.created_at,
      }))

    console.log(`📋 Found ${recentUsers.length} users in time window (out of ${allUsersData.users.length} total)`)

    // WHITELIST FILTER: Only process whitelisted emails
    const whitelistedUsers = recentUsers.filter((user) =>
      TEST_EMAIL_WHITELIST.includes(user.email)
    )

    console.log(`🔐 Whitelisted users: ${whitelistedUsers.length} (filtered from ${recentUsers.length})`)

    if (whitelistedUsers.length === 0) {
      return NextResponse.json({
        success: true,
        message: 'No whitelisted users in 2-27h window',
        processed: 0,
        whitelist: TEST_EMAIL_WHITELIST,
      })
    }

    // Step 2: Filter out users who have a subscription (stripe_customer_id exists)
    const { data: subscriptions } = await supabase
      .from('subscriptions')
      .select('user_id, stripe_customer_id')
      .in(
        'user_id',
        whitelistedUsers.map((u) => u.id)
      )
      .not('stripe_customer_id', 'is', null)

    const usersWithCard = new Set(subscriptions?.map((s) => s.user_id) || [])

    // Step 3: Filter out users who already received the email or had a subscription
    const { data: emailTracking } = await supabase
      .from('user_email_tracking')
      .select('user_id, trial_reminder_sent_at, had_subscription')
      .in(
        'user_id',
        whitelistedUsers.map((u) => u.id)
      )

    const usersAlreadySent = new Set(
      emailTracking
        ?.filter(
          (t) => t.trial_reminder_sent_at !== null || t.had_subscription === true
        )
        .map((t) => t.user_id) || []
    )

    // Step 4: Find eligible users
    const eligibleUsers = whitelistedUsers.filter(
      (user) => !usersWithCard.has(user.id) && !usersAlreadySent.has(user.id)
    )

    console.log(`✅ Eligible users: ${eligibleUsers.length}`)
    console.log(`   - With card: ${usersWithCard.size}`)
    console.log(`   - Already sent: ${usersAlreadySent.size}`)

    if (eligibleUsers.length === 0) {
      return NextResponse.json({
        success: true,
        message: 'No eligible whitelisted users',
        processed: 0,
        stats: {
          inTimeWindow: whitelistedUsers.length,
          withCard: usersWithCard.size,
          alreadySent: usersAlreadySent.size,
        },
      })
    }

    // Step 5: Send emails and update tracking
    const results = []
    for (const user of eligibleUsers) {
      console.log(`📧 Sending TEST reminder to ${user.email} (user_id: ${user.id})`)

      // Send email
      const emailResult = await sendEmailFromTemplate(
        user.email!,
        getEmail1_NoCreditCard()
      )

      if (emailResult.success) {
        // UPSERT tracking record
        const { error: upsertError } = await supabase
          .from('user_email_tracking')
          .upsert(
            {
              user_id: user.id,
              trial_reminder_sent_at: new Date().toISOString(),
              had_subscription: false,
            },
            {
              onConflict: 'user_id',
            }
          )

        if (upsertError) {
          console.error(
            `❌ Failed to update tracking for ${user.email}:`,
            upsertError
          )
          results.push({
            userId: user.id,
            email: user.email,
            success: false,
            error: 'Failed to update tracking',
          })
        } else {
          console.log(`✅ Email sent and tracked for ${user.email}`)
          results.push({
            userId: user.id,
            email: user.email,
            success: true,
            emailId: emailResult.emailId,
          })
        }
      } else {
        console.error(`❌ Failed to send email to ${user.email}:`, emailResult.error)
        // Silent fail: Mark as sent anyway to avoid retry loops
        await supabase.from('user_email_tracking').upsert(
          {
            user_id: user.id,
            trial_reminder_sent_at: new Date().toISOString(),
            had_subscription: false,
          },
          {
            onConflict: 'user_id',
          }
        )
        results.push({
          userId: user.id,
          email: user.email,
          success: false,
          error: emailResult.error,
        })
      }

      // Rate limiting: Wait 500ms between emails
      await new Promise((resolve) => setTimeout(resolve, 500))
    }

    const successCount = results.filter((r) => r.success).length

    console.log(
      `🎉 TEST Cron completed: ${successCount}/${eligibleUsers.length} emails sent successfully`
    )

    return NextResponse.json({
      success: true,
      message: `Processed ${eligibleUsers.length} whitelisted users`,
      successCount,
      whitelist: TEST_EMAIL_WHITELIST,
      results,
    })
  } catch (err) {
    console.error('❌ TEST Cron exception:', err)
    return NextResponse.json(
      {
        success: false,
        error: String(err),
      },
      { status: 500 }
    )
  }
}
