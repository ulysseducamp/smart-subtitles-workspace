'use client'

import { useRouter } from 'next/navigation'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface ProgressBarWithBackProps {
  progress: number           // 0-100
  label?: string             // Optional label above progress bar
  showBackButton?: boolean   // Default true
  onBack?: () => void        // Custom back logic
}

export function ProgressBarWithBack({
  progress,
  label,
  showBackButton = true,
  onBack
}: ProgressBarWithBackProps) {
  const router = useRouter()

  const handleBack = () => {
    if (onBack) {
      onBack()  // Custom logic
    } else {
      router.back()  // Default: browser back
    }
  }

  return (
    <div className="w-full">
      {/* Label with no spacing - progress bar has natural spacing */}
      {label && (
        <p className="text-sm text-muted-foreground text-center">
          {label}
        </p>
      )}

      {/* Progress bar with back button */}
      <div className="flex items-center gap-2 w-full">
        {showBackButton && (
          <Button
            variant="ghost"
            size="icon"
            onClick={handleBack}
            className="shrink-0"
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
        )}
        <Progress value={progress} className="flex-1" />
      </div>
    </div>
  )
}
