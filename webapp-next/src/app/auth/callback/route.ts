import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')
  const origin = requestUrl.origin

  if (code) {
    const supabase = await createClient()

    // Exchange code for session
    const { error } = await supabase.auth.exchangeCodeForSession(code)

    if (error) {
      console.error('Auth callback error:', error)
      return NextResponse.redirect(`${origin}/welcome?error=${error.message}`)
    }

    // Get current user
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      return NextResponse.redirect(`${origin}/welcome`)
    }

    // Check if user has completed onboarding
    // 1. Check user_settings exists
    const { data: settings } = await supabase
      .from('user_settings')
      .select('target_lang, native_lang')
      .eq('user_id', user.id)
      .single()

    // 2. Check subscription exists
    const { data: subscription } = await supabase
      .from('subscriptions')
      .select('status')
      .eq('user_id', user.id)
      .single()

    // If user has settings AND subscription, they've completed onboarding
    if (settings && subscription) {
      console.log('✅ Existing user detected - redirecting to /welcome-back')
      return NextResponse.redirect(`${origin}/welcome-back`)
    }

    // New user - redirect to onboarding
    console.log('🆕 New user detected - redirecting to /onboarding/languages')
    return NextResponse.redirect(`${origin}/onboarding/languages`)
  }

  // No code - redirect to welcome
  return NextResponse.redirect(`${origin}/welcome`)
}
