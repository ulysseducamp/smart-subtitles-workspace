import { createClient } from '@supabase/supabase-js'

/**
 * Service Role Client - BYPASSES RLS
 *
 * ⚠️ CRITICAL SECURITY NOTES:
 * - This client has FULL admin access to the database
 * - Bypasses ALL Row Level Security (RLS) policies
 * - Should ONLY be used in secure server-side contexts
 * - NEVER expose this client or the service role key to the client
 *
 * Use cases:
 * - Stripe webhooks (no user session available)
 * - Background jobs and cron tasks
 * - Admin operations with prior authorization checks
 *
 * Security checklist before using:
 * ✅ Is this running server-side only? (API routes, not client components)
 * ✅ Have you verified the request is authenticated/authorized?
 * ✅ Are you validating all input data?
 * ✅ Is the service role key stored only in .env and never committed?
 */
export function createServiceClient() {
  if (!process.env.SUPABASE_SERVICE_ROLE_KEY) {
    throw new Error(
      'SUPABASE_SERVICE_ROLE_KEY is not set. This is required for service operations.'
    )
  }

  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  )
}
