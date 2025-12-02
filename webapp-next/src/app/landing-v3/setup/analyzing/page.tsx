'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Progress } from '@/components/ui/progress'

export default function AnalyzingPage() {
  const router = useRouter()

  useEffect(() => {
    // Simulate analysis for 2 seconds, then navigate to results
    const timer = setTimeout(() => {
      router.push('/landing-v3/setup/results')
    }, 2000)

    return () => clearTimeout(timer)
  }, [router])

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-md w-full space-y-6 text-center">
        <h2 className="text-2xl font-semibold">Analyzing your level...</h2>
        <Progress value={66} className="w-full" />
      </div>
    </div>
  )
}
