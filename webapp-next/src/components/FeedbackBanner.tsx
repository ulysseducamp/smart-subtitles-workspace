export function FeedbackBanner() {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
      Any feedback? Please, send me an email at{' '}
      <a
        href="mailto:unducamp.pro@gmail.com"
        className="underline hover:text-primary"
      >
        unducamp.pro@gmail.com
      </a>
    </div>
  )
}
