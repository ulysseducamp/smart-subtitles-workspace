-- Migration: Create user_email_tracking table
-- Date: 2025-12-05
-- Purpose: Track email automation states for trial reminders and subscription tracking
-- Separate table for clean semantics and 100% user coverage

-- Create the table
CREATE TABLE IF NOT EXISTS public.user_email_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  trial_reminder_sent_at TIMESTAMPTZ,
  had_subscription BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Add indexes for performance (cron job will query these columns frequently)
CREATE INDEX IF NOT EXISTS idx_user_email_tracking_user_id
ON public.user_email_tracking(user_id);

CREATE INDEX IF NOT EXISTS idx_user_email_tracking_trial_reminder
ON public.user_email_tracking(trial_reminder_sent_at)
WHERE trial_reminder_sent_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_user_email_tracking_had_subscription
ON public.user_email_tracking(had_subscription);

-- Enable Row Level Security
ALTER TABLE public.user_email_tracking ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only read their own tracking data
CREATE POLICY "Users can view their own email tracking"
ON public.user_email_tracking
FOR SELECT
USING (auth.uid() = user_id);

-- RLS Policy: Service role can do everything (for cron jobs and webhooks)
CREATE POLICY "Service role has full access"
ON public.user_email_tracking
FOR ALL
USING (auth.role() = 'service_role');

-- Add comments for documentation
COMMENT ON TABLE public.user_email_tracking IS
'Tracks email automation state for each user. Used by cron jobs and webhooks to prevent duplicate emails.';

COMMENT ON COLUMN public.user_email_tracking.trial_reminder_sent_at IS
'Timestamp when trial reminder email (scenario 1: no credit card after 2h) was sent. NULL = not sent yet.';

COMMENT ON COLUMN public.user_email_tracking.had_subscription IS
'Flag indicating user has had a subscription at any point. Used to prevent trial reminder emails for users who started then quickly cancelled.';
