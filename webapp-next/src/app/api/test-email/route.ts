import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY!)

export async function GET(req: NextRequest) {
  try {
    console.log('📧 Test email - Envoi depuis ulysse@sublyy.com...')

    const { data, error } = await resend.emails.send({
      from: 'Ulysse from Subly <ulysse@sublyy.com>',
      replyTo: 'unducamp.pro@gmail.com',
      to: ['unducamp.pro@gmail.com'], // Ton email pour le test
      subject: '🧪 Test - Email depuis ulysse@sublyy.com',
      html: `
        <h1>Test d'envoi Resend</h1>
        <p>Salut Ulysse,</p>
        <p>Cet email est envoyé depuis <strong>ulysse@sublyy.com</strong>.</p>
        <p>Si tu reçois cet email, ça veut dire que :</p>
        <ul>
          <li>✅ Resend peut envoyer depuis <code>ulysse@sublyy.com</code></li>
          <li>✅ Le domaine <code>sublyy.com</code> est bien vérifié</li>
        </ul>
        <p><strong>Test du reply-to :</strong></p>
        <p>Clique sur "Reply" dans ton client email. L'adresse de réponse devrait être automatiquement <code>unducamp.pro@gmail.com</code> (pas <code>ulysse@sublyy.com</code>).</p>
        <hr />
        <p style="color: #666; font-size: 12px;">Email de test - Tu peux supprimer ce message</p>
      `,
    })

    if (error) {
      console.error('❌ Erreur envoi test:', error)
      return NextResponse.json(
        { error: 'Failed to send test email', details: error },
        { status: 500 }
      )
    }

    console.log('✅ Email test envoyé avec succès:', data)
    return NextResponse.json({
      success: true,
      message: 'Email de test envoyé vers unducamp.pro@gmail.com',
      emailId: data?.id,
    })
  } catch (err) {
    console.error('❌ Exception envoi test:', err)
    return NextResponse.json(
      { error: 'Exception occurred', details: String(err) },
      { status: 500 }
    )
  }
}
