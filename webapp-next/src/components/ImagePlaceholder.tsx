interface ImagePlaceholderProps {
  label: string
  aspectRatio?: string // e.g., "16/9" or "1/1"
  className?: string
}

export function ImagePlaceholder({
  label,
  aspectRatio = '16/9',
  className = ''
}: ImagePlaceholderProps) {
  return (
    <div
      className={`bg-muted border-2 border-dashed border-muted-foreground/30 rounded-lg flex items-center justify-center ${className}`}
      style={{ aspectRatio }}
    >
      <p className="text-muted-foreground text-sm text-center px-4">
        {label}
      </p>
    </div>
  )
}
