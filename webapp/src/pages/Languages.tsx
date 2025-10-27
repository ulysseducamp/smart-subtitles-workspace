import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useNavigate } from 'react-router-dom'
import { supabase } from '@/lib/supabase'

const TARGET_LANGUAGES = [
  { value: 'pt-BR', label: 'Portuguese 🇧🇷' },
  { value: 'fr', label: 'French 🇫🇷' },
]

const NATIVE_LANGUAGES = [
  { value: 'en', label: 'English 🇬🇧🇺🇸' },
  { value: 'fr', label: 'French 🇫🇷' },
  { value: 'es', label: 'Spanish 🇪🇸' },
  { value: 'de', label: 'German 🇩🇪' },
  { value: 'it', label: 'Italian 🇮🇹' },
  { value: 'pt', label: 'Portuguese 🇵🇹' },
  { value: 'pl', label: 'Polish 🇵🇱' },
  { value: 'nl', label: 'Dutch 🇳🇱' },
  { value: 'sv', label: 'Swedish 🇸🇪' },
  { value: 'da', label: 'Danish 🇩🇰' },
  { value: 'cs', label: 'Czech 🇨🇿' },
  { value: 'ja', label: 'Japanese 🇯🇵' },
  { value: 'ko', label: 'Korean 🇰🇷' },
]

export default function Languages() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const [targetLang, setTargetLang] = useState<string>('')
  const [nativeLang, setNativeLang] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [saving, setSaving] = useState(false)

  const handleNext = async () => {
    // Validation
    if (!targetLang || !nativeLang) {
      setError('Please select both languages')
      return
    }
    if (targetLang === nativeLang) {
      setError('Target and native languages must be different')
      return
    }

    setSaving(true)
    try {
      // Save to Supabase user_settings
      const { error: dbError } = await supabase
        .from('user_settings')
        .upsert({
          user_id: user?.id,
          target_lang: targetLang,
          native_lang: nativeLang,
          updated_at: new Date().toISOString(),
        }, {
          onConflict: 'user_id'
        })

      if (dbError) throw dbError

      navigate('/onboarding/vocab-test')
    } catch (err) {
      console.error('Error saving settings:', err)
      setError('Failed to save settings. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Logout button */}
      <div className="absolute top-4 right-4">
        <Button variant="ghost" onClick={signOut}>
          Log out
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 max-w-md mx-auto w-full">
        <h1 className="text-3xl font-bold text-center mb-8">
          Select your languages
        </h1>

        <div className="w-full space-y-6">
          {/* Target Language */}
          <div className="space-y-2">
            <Label htmlFor="target-lang">Target language (language you want to learn)</Label>
            <Select value={targetLang} onValueChange={setTargetLang}>
              <SelectTrigger id="target-lang">
                <SelectValue placeholder="Select target language" />
              </SelectTrigger>
              <SelectContent>
                {TARGET_LANGUAGES.map((lang) => (
                  <SelectItem key={lang.value} value={lang.value}>
                    {lang.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Native Language */}
          <div className="space-y-2">
            <Label htmlFor="native-lang">Native language (your native language)</Label>
            <Select value={nativeLang} onValueChange={setNativeLang}>
              <SelectTrigger id="native-lang">
                <SelectValue placeholder="Select native language" />
              </SelectTrigger>
              <SelectContent>
                {NATIVE_LANGUAGES.map((lang) => (
                  <SelectItem key={lang.value} value={lang.value}>
                    {lang.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Error message */}
          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <Button
            onClick={handleNext}
            disabled={!targetLang || !nativeLang || targetLang === nativeLang || saving}
            className="w-full"
          >
            {saving ? 'Saving...' : 'Next'}
          </Button>
        </div>
      </div>

      {/* Fixed feedback banner */}
      <div className="fixed bottom-0 left-0 right-0 bg-muted p-4 text-center text-sm">
        Any feedback? Please, send me an email at unducamp.pro@gmail.com
      </div>
    </div>
  )
}
