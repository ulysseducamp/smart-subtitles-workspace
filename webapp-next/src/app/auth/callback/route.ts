import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')
  const redirectParam = requestUrl.searchParams.get('redirect')
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

    // If redirect parameter is present, validate and use it (for landing flow)
    if (redirectParam) {
      // Validate redirect URL (whitelist - security against open redirect attacks)
      const isValidRedirect = (url: string) => {
        return url.startsWith('/landing/') || url.startsWith('/landing-v3/') || url.startsWith('/onboarding/')
      }

      if (!isValidRedirect(redirectParam)) {
        console.error(`🚨 Security: Invalid redirect attempted - ${redirectParam}`)
        return NextResponse.redirect(`${origin}/welcome?error=Invalid redirect URL`)
      }

      console.log(`🔀 Custom redirect detected - redirecting to ${redirectParam}`)
      return NextResponse.redirect(`${origin}${redirectParam}`)
    }

    // Otherwise, use existing onboarding logic
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

    // New user - redirect to pricing-intro (nouveau flow 20 écrans)
    console.log('🆕 New user detected - redirecting to /onboarding/pricing-intro')
    return NextResponse.redirect(`${origin}/onboarding/pricing-intro`)
  }

  // No code - redirect to welcome
  return NextResponse.redirect(`${origin}/welcome`)
}
