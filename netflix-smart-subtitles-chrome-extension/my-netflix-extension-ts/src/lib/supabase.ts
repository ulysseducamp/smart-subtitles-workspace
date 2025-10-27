import { createClient } from '@supabase/supabase-js'
import { chromeStorageAdapter } from './supabase-storage-adapter'

const supabaseUrl = 'https://dqjbkbdgvtewrgxrfqil.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxamJrYmRndnRld3JneHJmcWlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3MDQwMjYsImV4cCI6MjA3NjI4MDAyNn0.hoZflFK2abrRi8-KCizAi2mtw8Pb6z0KNSLzf6R8bRA'

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: chromeStorageAdapter,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false, // CRITICAL: Extensions don't have URL hash
  },
})
