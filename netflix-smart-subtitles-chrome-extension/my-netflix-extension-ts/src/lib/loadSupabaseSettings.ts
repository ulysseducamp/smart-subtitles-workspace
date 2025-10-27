import { supabase } from './supabase'

export interface UserSettings {
  targetLanguage: string
  nativeLanguage: string
  vocabularyLevel: number
}

/**
 * Load user settings from Supabase
 * Returns null if user not authenticated or settings don't exist
 */
export async function loadSupabaseSettings(): Promise<UserSettings | null> {
  try {
    // Check if user is authenticated
    const { data: { session } } = await supabase.auth.getSession()

    if (!session?.user) {
      console.log('Smart Netflix Subtitles: No active session, user not logged in')
      return null
    }

    console.log('Smart Netflix Subtitles: User authenticated:', session.user.email)

    // Load user_settings
    const { data: settings, error: settingsError } = await supabase
      .from('user_settings')
      .select('target_lang, native_lang')
      .eq('user_id', session.user.id)
      .single()

    if (settingsError || !settings) {
      console.log('Smart Netflix Subtitles: No settings found in Supabase')
      return null
    }

    // Load vocab_levels for target language
    const { data: vocabData, error: vocabError } = await supabase
      .from('vocab_levels')
      .select('level')
      .eq('user_id', session.user.id)
      .eq('language', settings.target_lang)
      .single()

    if (vocabError || !vocabData) {
      console.log('Smart Netflix Subtitles: No vocab level found for', settings.target_lang)
      return null
    }

    console.log('Smart Netflix Subtitles: Loaded settings from Supabase:', {
      targetLanguage: settings.target_lang,
      nativeLanguage: settings.native_lang,
      vocabularyLevel: vocabData.level
    })

    return {
      targetLanguage: settings.target_lang,
      nativeLanguage: settings.native_lang,
      vocabularyLevel: vocabData.level
    }
  } catch (error) {
    console.error('Smart Netflix Subtitles: Error loading settings from Supabase:', error)
    return null
  }
}
