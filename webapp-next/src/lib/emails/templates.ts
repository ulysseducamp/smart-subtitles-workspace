/**
 * Email templates for automated user outreach
 *
 * All emails:
 * - From: Ulysse from Subly <ulysse@sublyy.com>
 * - Reply-To: unducamp.pro@gmail.com
 */

/**
 * Email 1: No credit card after 2 hours
 * Offer lifetime access in exchange for 30min feedback call
 */
export function getEmail1_NoCreditCard(): { subject: string; html: string } {
  return {
    subject: "You're officially the 49th person who signed up for Subly",
    html: `
      <p>Hello, It's Ulysse, the developer behind the Subly Netflix extension</p>

      <p>I saw you registered for Subly, thanks a lot for your interest in our tool! It's the very beginning of our extension and you are officially the 49th person who signed up.</p>

      <p>I noticed that you didn't start the free trial, I totally understand you, since you have to enter your credit card to start it.</p>

      <p>Even though you didn't start the free trial, I would really like to hear your thoughts about the extension. Things like what motivated you to download it and register, what were your expectations from it, things like that. I would also like to learn about your language learning journey to understand better who can be interested by Subly and what pain points we could solve.</p>

      <p>I believe that a call is worth a thousand emails, I'd like to propose you something:</p>

      <p><strong>→ I offer you a totally free subscription, lifetime, for Subly and in exchange you give 30mn of your time to talk through a video call about your language learning journey and your thoughts about the extension.</strong></p>

      <p>I've already had 8 calls like that and the conversations are always very interesting, it's such a pleasure to exchange with other language learners and getting feedback about Subly is extremely valuable for us. Having calls with potential users like you is very important at this stage because it allows us to really understand your needs and how we can address them.</p>

      <p>I believe that a free lifetime subscription to Subly is a very good gift since we plan to add a lot of features to Subly to turn it into a very complete language learning solution. We really want to make language learning easier and smoother.</p>

      <p>During our call, I'll also do my best to help you as much as I can in your learning process by giving you tips and tools to try, depending on your constraints and goals (I know a lot about language learning tools, that's why we decided to create our own)</p>

      <p>I know from experience that just one tip can often change a whole language learning trajectory and make the difference between a habit that you give up early and one that you maintain over the long-term. Language learning shouldn't be hard.</p>

      <p>It's only because it's the very beginning of Subly that I am offering this kind of deal, I don't know for how long I'll propose calls like that.</p>

      <p>If you're ok to give 30mn of your time to help us and play a role in the development of Subly, you can book a call with me directly through this link at the most convenient moment for you: <a href="https://calendly.com/ulysse-i/30min">https://calendly.com/ulysse-i/30min</a> (It will automatically create a google meet link for us to have the call at the time you picked)</p>

      <p>Thanks a lot for your time,</p>
      <p>Ulysse Ducamp</p>
    `,
  }
}

/**
 * Email 2: Cancelled subscription during trial (before first payment)
 * Ask for quick feedback
 */
export function getEmail2_CancelledDuringTrial(): { subject: string; html: string } {
  return {
    subject: "You canceled your subscription and that's ok",
    html: `
      <p>Hello, it's Ulysse, the developer behind Subly!</p>

      <p>I saw that you tested Subly and canceled your subscription (which is totally ok). I am very sorry that Subly didn't match your expectations. I just launched this extension (you are actually the 9th person who entered their credit card) and I'd love to hear your feedback about Subly to know what I should improve/add/correct first.</p>

      <p>I'd be extremely grateful if you could answer to this email with a quick feedback 🙏</p>

      <p>Thanks a lot for your precious time,</p>

      <p>Ulysse Ducamp</p>
    `,
  }
}

/**
 * Email 3: First payment successful (after 3-day trial)
 * Thank + offer French tutoring in exchange for feedback call
 */
export function getEmail3_FirstPayment(): { subject: string; html: string } {
  return {
    subject: "You're officially Subly's 8th customer!",
    html: `
      <p>Hello, it's Ulysse, the developer behind Subly.</p>

      <p>Thank you so much for your interest in our extension. It's far from being perfect but it's a beginning and you are officially our 8th customer which is very important to us.</p>

      <p>I would really like to hear your thoughts about the extension. Things like what motivated you to register, what were your expectations from it, things like that. I would also like to learn about your language learning journey to understand better who can be interested by Subly and what pain points we could solve.</p>

      <p>I believe that a call is worth a thousand emails, I'd like to propose you something, as a french native (born and raised in Paris), <strong>I offer you a free 30mn French tutoring call and in exchange you give 30mn of your time to talk about your language learning journey and your thoughts about the extension through a video call.</strong></p>

      <p>I've already had 4 calls like that and the conversations are always very interesting, it's such a pleasure to exchange with other language learners and getting feedback about Subly is extremely valuable for us. Having calls with users like you is very important at this stage because it allows us to really understand your needs.</p>

      <p>This call will have a real impact on how Subly is shaped, you'll be able to propose ideas that we will really listen to. We plan to add a lot of innovative features to Subly. We really want to make language learning easier and smoother and we need your help (30mn of your time) for that.</p>

      <p>During our call, I'll also do my best to help you as much as I can in your learning process by giving you tips and tools to try, depending on your constraints and goals (I know a lot about language learning tools, that's why we decided to create our own).</p>

      <p>I know from experience that just one tip can often change a whole language learning trajectory and make the difference between a habit that you give up early and one that you maintain over the long-term. Language learning shouldn't be hard.</p>

      <p>It's only because it's the very beginning of Subly that I am offering this kind of "deal", I don't know for how long I'll propose calls like that.</p>

      <p>If you're ok to give 30mn of your time to help us, you can book a call with me directly through this link at the most convenient moment for you: <a href="https://calendly.com/ulysse-i/30min">https://calendly.com/ulysse-i/30min</a></p>

      <p>(After the call, you'll be able to book another call for our 30min French tutoring call as promised)</p>

      <p>Thanks a lot for your time,</p>
      <p>Ulysse Ducamp</p>
    `,
  }
}
