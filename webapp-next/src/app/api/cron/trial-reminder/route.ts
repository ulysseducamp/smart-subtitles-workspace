import { NextRequest, NextResponse } from 'next/server'
import { createServiceClient } from '@/lib/supabase/service'
import { sendEmailFromTemplate } from '@/lib/emails/sendEmail'
import { getEmail1_NoCreditCard } from '@/lib/emails/templates'

/**
 * Vercel Cron Job: Send trial reminder emails
 *
 * Runs daily to check for users who:
 * 1. Signed up 24-25 hours ago
 * 2. Have NOT entered a credit card (no stripe_customer_id)
 * 3. Have NOT received the trial reminder email yet
 * 4. Have NEVER had a subscription (had_subscription = false)
 *
 * Schedule: Daily at midnight UTC (configured in vercel.json)
 */
export async function GET(req: NextRequest) {
  console.log('⏰ Cron: Trial reminder check started')

  // ⚠️ SECURITY: Using service client to bypass RLS
  // This is safe because:
  // 1. Cron endpoints are server-side only
  // 2. We need to query across auth.users and public tables
  // 3. Service key is server-side only (never exposed to client)
  const supabase = createServiceClient()

  try {
    // Calculate time window: 24-25 hours ago
    const now = new Date()
    const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000)
    const twentyFiveHoursAgo = new Date(now.getTime() - 25 * 60 * 60 * 1000)

    console.log('🔍 Looking for users created between:', {
      start: twentyFiveHoursAgo.toISOString(),
      end: twentyFourHoursAgo.toISOString(),
    })

    // Step 1: Fetch last 100 users via Admin API (auth.users is protected)
    // 100 users = sufficient for finding those created 24-25h ago
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

    // Sort by created_at desc to get most recent first, then filter users who signed up 2-3 hours ago
    const sortedUsers = [...allUsersData.users].sort(
      (a, b) => new Date(b.created_at!).getTime() - new Date(a.created_at!).getTime()
    )

    const recentUsers = sortedUsers
      .filter((user) => {
        if (!user.created_at || !user.email) return false
        const createdAt = new Date(user.created_at)
        return createdAt >= twentyFiveHoursAgo && createdAt <= twentyFourHoursAgo
      })
      .map((user) => ({
        id: user.id,
        email: user.email!,
        created_at: user.created_at,
      }))

    console.log(`📋 Found ${recentUsers.length} users in time window (out of ${allUsersData.users.length} total)`)

    if (recentUsers.length === 0) {
      return NextResponse.json({
        success: true,
        message: 'No users in 24-25h window',
        processed: 0,
      })
    }

    // Step 2: Filter out users who have a subscription (stripe_customer_id exists)
    const { data: subscriptions } = await supabase
      .from('subscriptions')
      .select('user_id, stripe_customer_id')
      .in(
        'user_id',
        recentUsers.map((u) => u.id)
      )
      .not('stripe_customer_id', 'is', null)

    const usersWithCard = new Set(subscriptions?.map((s) => s.user_id) || [])

    // Step 3: Filter out users who already received the email or had a subscription
    const { data: emailTracking } = await supabase
      .from('user_email_tracking')
      .select('user_id, trial_reminder_sent_at, had_subscription')
      .in(
        'user_id',
        recentUsers.map((u) => u.id)
      )

    const usersAlreadySent = new Set(
      emailTracking
        ?.filter(
          (t) => t.trial_reminder_sent_at !== null || t.had_subscription === true
        )
        .map((t) => t.user_id) || []
    )

    // Step 4: Find eligible users
    const eligibleUsers = recentUsers.filter(
      (user) => !usersWithCard.has(user.id) && !usersAlreadySent.has(user.id)
    )

    console.log(`✅ Found ${eligibleUsers.length} eligible users for reminder email`)

    if (eligibleUsers.length === 0) {
      return NextResponse.json({
        success: true,
        message: 'No eligible users found',
        processed: 0,
      })
    }

    // Step 5: Send emails and update tracking
    const results = []
    for (const user of eligibleUsers) {
      console.log(`📧 Sending reminder to ${user.email} (user_id: ${user.id})`)

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
      `✅ Cron completed: ${successCount}/${eligibleUsers.length} emails sent successfully`
    )

    return NextResponse.json({
      success: true,
      message: `Processed ${eligibleUsers.length} users`,
      successCount,
      results,
    })
  } catch (err) {
    console.error('❌ Cron exception:', err)
    return NextResponse.json(
      {
        success: false,
        error: String(err),
      },
      { status: 500 }
    )
  }
}
