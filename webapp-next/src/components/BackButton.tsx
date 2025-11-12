'use client'

import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

export function BackButton() {
  const router = useRouter()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => router.back()}
      className="mr-2"
      aria-label="Go back"
    >
      <ArrowLeft className="h-5 w-5" />
    </Button>
  )
}
