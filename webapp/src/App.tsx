import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/contexts/AuthContext'
import { Toaster } from '@/components/ui/sonner'

// Pages
import Welcome from '@/pages/Welcome'
import Languages from '@/pages/Languages'
import VocabTest from '@/pages/VocabTest'
import Results from '@/pages/Results'
import Pricing from '@/pages/onboarding/Pricing'
import PinExtension from '@/pages/PinExtension'
import Complete from '@/pages/Complete'
import WelcomeBack from '@/pages/WelcomeBack'
import Subscribe from '@/pages/Subscribe'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster position="top-center" />
        <Routes>
          {/* Welcome */}
          <Route path="/welcome" element={<Welcome />} />

          {/* Onboarding Flow */}
          <Route path="/onboarding/languages" element={<Languages />} />
          <Route path="/onboarding/vocab-test" element={<VocabTest />} />
          <Route path="/onboarding/results" element={<Results />} />
          <Route path="/onboarding/pricing" element={<Pricing />} />
          <Route path="/onboarding/pin-extension" element={<PinExtension />} />
          <Route path="/onboarding/complete" element={<Complete />} />

          {/* Subscription */}
          <Route path="/subscribe" element={<Subscribe />} />

          {/* Returning Users */}
          <Route path="/welcome-back" element={<WelcomeBack />} />

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/welcome" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
