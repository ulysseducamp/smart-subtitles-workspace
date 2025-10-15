import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'

function OnboardingPage() {
  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Onboarding</h1>
      <p className="mb-4 text-muted-foreground">
        This is where the 5-step onboarding flow will go
      </p>
      <div className="space-y-2 text-sm">
        <p>✅ Step 1: Welcome screen</p>
        <p>✅ Step 2: Language selection (target + native)</p>
        <p>✅ Step 3: Vocabulary test</p>
        <p>✅ Step 4: Pin extension reminder</p>
        <p>✅ Step 5: Congratulations</p>
      </div>
    </div>
  )
}

function DashboardPage() {
  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <p className="mb-4 text-muted-foreground">
        This is where word management and statistics will go
      </p>
      <div className="space-y-2 text-sm">
        <p>📚 Known words list</p>
        <p>📈 Learning statistics</p>
        <p>⚙️ Settings management</p>
      </div>
      <div className="mt-6">
        <Button onClick={() => window.location.href = '/onboarding'}>
          Go to Onboarding
        </Button>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/" element={<Navigate to="/onboarding" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
