-- Add separate email tracking flags for Scenario 2 and 3
-- Fixes bug: had_subscription mixed cancellation and payment states

-- Add cancellation_email_sent_at for Scenario 2
ALTER TABLE public.user_email_tracking
ADD COLUMN IF NOT EXISTS cancellation_email_sent_at TIMESTAMPTZ;

COMMENT ON COLUMN public.user_email_tracking.cancellation_email_sent_at IS
'Timestamp when cancellation email (Scenario 2: user cancelled during trial) was sent. NULL = not sent yet.';

-- Add first_payment_email_sent_at for Scenario 3
ALTER TABLE public.user_email_tracking
ADD COLUMN IF NOT EXISTS first_payment_email_sent_at TIMESTAMPTZ;

COMMENT ON COLUMN public.user_email_tracking.first_payment_email_sent_at IS
'Timestamp when first payment email (Scenario 3: first payment after trial) was sent. NULL = not sent yet.';

-- Update comment on had_subscription to clarify its purpose
COMMENT ON COLUMN public.user_email_tracking.had_subscription IS
'Flag indicating user has had a subscription at any point. Used ONLY for Scenario 1 (trial reminder) to prevent sending to former customers who cancelled.';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_email_tracking_cancellation
ON public.user_email_tracking(cancellation_email_sent_at)
WHERE cancellation_email_sent_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_user_email_tracking_first_payment
ON public.user_email_tracking(first_payment_email_sent_at)
WHERE first_payment_email_sent_at IS NULL;
