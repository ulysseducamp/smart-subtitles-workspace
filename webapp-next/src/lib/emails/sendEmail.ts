import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY!)

/**
 * Email configuration constants
 */
const EMAIL_CONFIG = {
  from: 'Ulysse from Subly <ulysse@sublyy.com>',
  replyTo: 'unducamp.pro@gmail.com',
} as const

/**
 * Send an email using Resend with tracking enabled
 *
 * @param to - Recipient email address
 * @param subject - Email subject
 * @param html - Email HTML content
 * @returns Resend response with email ID
 */
export async function sendEmail(
  to: string,
  subject: string,
  html: string
): Promise<{ success: boolean; emailId?: string; error?: string }> {
  try {
    const { data, error } = await resend.emails.send({
      from: EMAIL_CONFIG.from,
      replyTo: EMAIL_CONFIG.replyTo,
      to: [to],
      subject,
      html,
    })

    if (error) {
      console.error('❌ Resend error:', error)
      return {
        success: false,
        error: JSON.stringify(error),
      }
    }

    console.log('✅ Email sent successfully:', {
      to,
      subject,
      emailId: data?.id,
    })

    return {
      success: true,
      emailId: data?.id,
    }
  } catch (err) {
    console.error('❌ Exception sending email:', err)
    return {
      success: false,
      error: String(err),
    }
  }
}

/**
 * Type-safe email sender with template validation
 */
export type EmailTemplate = {
  subject: string
  html: string
}

/**
 * Send an email using a template
 *
 * @param to - Recipient email address
 * @param template - Email template (from templates.ts)
 * @returns Resend response with email ID
 */
export async function sendEmailFromTemplate(
  to: string,
  template: EmailTemplate
): Promise<{ success: boolean; emailId?: string; error?: string }> {
  return sendEmail(to, template.subject, template.html)
}
