'use client'

import Image from 'next/image'

export default function Complete() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">
        Congrats you're all set!
      </h1>

      <p className="text-lg text-center mb-8">
        You can start using the extension: when watching Netflix, click on the Subly icon to make this pop-up appear, then click on the button 'Process subtitles' to adapt the Netflix subtitles to your level.
      </p>

      <Image
        src="/onboarding/extension_popup.png"
        alt="Screenshot: Extension popup on Netflix with Process subtitles button visible"
        width={400}
        height={500}
        className="w-full max-w-sm mb-8 rounded-lg shadow-lg"
      />

      <p className="text-center text-muted-foreground">
        As you can see, through this pop-up you can change your languages and your level at any time.
      </p>
    </div>
  )
}
