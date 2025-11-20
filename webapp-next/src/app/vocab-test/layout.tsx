import { VocabTestProvider } from '@/contexts/VocabTestContext'

export default function VocabTestLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <VocabTestProvider>
      <div className="min-h-screen flex flex-col">
        {children}
      </div>
    </VocabTestProvider>
  )
}
