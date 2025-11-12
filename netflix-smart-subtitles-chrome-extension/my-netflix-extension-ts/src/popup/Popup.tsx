/*
 * Smart Netflix Subtitles
 * Copyright (C) 2025 Based on Subadub by Russel Simmons
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { loadSupabaseSettings } from '@/lib/loadSupabaseSettings';
import { supabase } from '@/lib/supabase';
import { ChromeMessage, ChromeResponse, ChromeTab } from '@/types/netflix';

// Webapp URL - set via webpack environment variable (production vs development)
const WEBAPP_URL = process.env.WEBAPP_URL || 'http://localhost:5173';

// Interface for Smart Subtitles settings
interface SmartSubtitlesSettings {
  enabled: boolean;
  targetLanguage: string;
  nativeLanguage: string;
  vocabularyLevel: number;
  isSubscribed: boolean;
}

// Storage keys for chrome.storage.local
const STORAGE_KEYS = {
  TARGET_LANGUAGE: 'targetLanguage',
  NATIVE_LANGUAGE: 'nativeLanguage',
  VOCABULARY_LEVEL: 'vocabularyLevel',
  IS_SUBSCRIBED: 'isSubscribed',
} as const;

// Supported languages mapping (Netflix code -> DeepL code)
const SUPPORTED_NATIVE_LANGUAGES: Record<string, string> = {
  'en': 'English',
  'fr': 'French',
  'es': 'Spanish',
  'de': 'German',
  'it': 'Italian',
  'pt': 'Portuguese',
  'pt-BR': 'Portuguese (Brazil)',
  'pl': 'Polish',
  'nl': 'Dutch',
  'sv': 'Swedish',
  'da': 'Danish',
  'cs': 'Czech',
  'ja': 'Japanese',
  'ko': 'Korean',
};

export function Popup() {
  const [settings, setSettings] = useState<SmartSubtitlesSettings>({
    enabled: true,
    targetLanguage: '',
    nativeLanguage: '',
    vocabularyLevel: 0,
    isSubscribed: false,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [statusType, setStatusType] = useState<'info' | 'error' | 'success'>('info');
  const [availableNativeLanguages, setAvailableNativeLanguages] = useState<string[]>([]);
  const [isOnNetflix, setIsOnNetflix] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);

  // Load settings on mount
  useEffect(() => {
    loadSettings();
    loadAvailableNativeLanguages();
    checkNetflixPage();
  }, []);

  // Load settings from Supabase (with chrome.storage.local fallback)
  async function loadSettings(): Promise<void> {
    try {
      // Try loading from Supabase first
      const supabaseSettings = await loadSupabaseSettings();

      if (supabaseSettings) {
        setSettings({
          enabled: true,
          targetLanguage: supabaseSettings.targetLanguage,
          nativeLanguage: supabaseSettings.nativeLanguage,
          vocabularyLevel: supabaseSettings.vocabularyLevel,
          isSubscribed: supabaseSettings.isSubscribed,
        });

        // If vocabulary level is 0, show Welcome popup
        if (!supabaseSettings.vocabularyLevel || supabaseSettings.vocabularyLevel === 0) {
          setShowWelcome(true);
        }

        console.log('Smart Netflix Subtitles: Loaded settings from Supabase:', supabaseSettings);
      } else {
        // Fallback to chrome.storage.local (legacy or no auth)
        const result = await chrome.storage.local.get([
          STORAGE_KEYS.TARGET_LANGUAGE,
          STORAGE_KEYS.NATIVE_LANGUAGE,
          STORAGE_KEYS.VOCABULARY_LEVEL,
        ]);

        const localSettings = {
          enabled: true,
          targetLanguage: result[STORAGE_KEYS.TARGET_LANGUAGE] || '',
          nativeLanguage: result[STORAGE_KEYS.NATIVE_LANGUAGE] || '',
          vocabularyLevel: result[STORAGE_KEYS.VOCABULARY_LEVEL] || 0,
          isSubscribed: false,
        };

        setSettings(localSettings);

        // If no vocabulary level, show Welcome popup
        if (!localSettings.vocabularyLevel || localSettings.vocabularyLevel === 0) {
          setShowWelcome(true);
        }

        console.log('Smart Netflix Subtitles: No Supabase settings, using local storage or defaults');
      }
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error loading settings:', error);
    }
  }

  // Save settings to chrome.storage.local
  async function saveSettings(newSettings: SmartSubtitlesSettings): Promise<void> {
    try {
      const settingsToSave = {
        [STORAGE_KEYS.TARGET_LANGUAGE]: newSettings.targetLanguage,
        [STORAGE_KEYS.NATIVE_LANGUAGE]: newSettings.nativeLanguage,
        [STORAGE_KEYS.VOCABULARY_LEVEL]: newSettings.vocabularyLevel,
      };

      await chrome.storage.local.set(settingsToSave);
      console.log('Smart Netflix Subtitles: Settings saved to storage:', settingsToSave);
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error saving settings:', error);
    }
  }

  // Load available native languages from Netflix
  async function loadAvailableNativeLanguages(): Promise<void> {
    try {
      const [tab] = (await chrome.tabs.query({
        active: true,
        currentWindow: true,
      })) as ChromeTab[];

      if (!tab || !tab.url?.includes('netflix.com')) {
        console.log('Smart Netflix Subtitles: Not on Netflix page, using default languages');
        return;
      }

      const response = (await chrome.tabs.sendMessage(tab.id!, {
        action: 'getAvailableSubtitleTracks',
      } as ChromeMessage)) as ChromeResponse;

      if (response && response.success && response.availableLanguages) {
        setAvailableNativeLanguages(response.availableLanguages);
      }
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error loading available languages:', error);
    }
  }

  // Check if on Netflix page
  async function checkNetflixPage(): Promise<void> {
    try {
      const [tab] = (await chrome.tabs.query({
        active: true,
        currentWindow: true,
      })) as ChromeTab[];

      if (!tab || !tab.url?.includes('netflix.com')) {
        showStatus('Please navigate to Netflix to use Smart Subtitles', 'error');
        setIsOnNetflix(false);
        return;
      }

      const response = (await chrome.tabs.sendMessage(tab.id!, {
        action: 'checkNetflixPage',
      } as ChromeMessage)) as ChromeResponse;

      if (response && response.success && response.isNetflixEpisode) {
        showStatus(`Ready: ${response.title}`, 'success');
        setIsOnNetflix(true);
      } else {
        showStatus('Please navigate to a Netflix episode or movie', 'error');
        setIsOnNetflix(false);
      }
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error checking Netflix page:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      if (errorMessage.includes('Could not establish connection')) {
        showStatus('Please refresh the Netflix page and try again', 'error');
      } else {
        showStatus('Error: ' + errorMessage, 'error');
      }
      setIsOnNetflix(false);
    }
  }

  // Show status message
  function showStatus(message: string, type: 'info' | 'error' | 'success' = 'info'): void {
    setStatusMessage(message);
    setStatusType(type);
  }

  // Process subtitles
  async function processSubtitles(): Promise<void> {
    // Check subscription status first
    if (!settings.isSubscribed) {
      console.log('Smart Netflix Subtitles: User not subscribed, redirecting to subscribe page');
      chrome.tabs.create({ url: `${WEBAPP_URL}/subscribe` });
      return;
    }

    if (!settings.targetLanguage || !settings.nativeLanguage || !settings.vocabularyLevel) {
      showStatus('Please complete all fields', 'error');
      return;
    }

    if (settings.targetLanguage === settings.nativeLanguage) {
      showStatus('Target and native languages must be different', 'error');
      return;
    }

    setIsProcessing(true);
    setIsLoading(true);
    setStatusMessage('');

    try {
      const [tab] = (await chrome.tabs.query({
        active: true,
        currentWindow: true,
      })) as ChromeTab[];

      if (!tab || !tab.url?.includes('netflix.com')) {
        throw new Error('Please navigate to Netflix first');
      }

      const response = (await chrome.tabs.sendMessage(tab.id!, {
        action: 'processSmartSubtitles',
        settings: settings,
      } as ChromeMessage)) as ChromeResponse;

      if (response && response.success) {
        showStatus('Smart subtitles processed successfully!', 'success');
      } else {
        throw new Error(response?.error || 'Failed to process subtitles');
      }
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error processing subtitles:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      showStatus(`Error: ${errorMessage}`, 'error');
    } finally {
      setIsProcessing(false);
      setIsLoading(false);
    }
  }

  // Handle language change
  async function handleTargetLanguageChange(value: string): Promise<void> {
    // Update Supabase (sync across devices)
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.user) {
      const { error } = await supabase
        .from('user_settings')
        .update({ target_lang: value })
        .eq('user_id', session.user.id);

      if (error) {
        console.error('Smart Netflix Subtitles: Supabase sync failed (target_lang):', error);
      } else {
        console.log('Smart Netflix Subtitles: Supabase synced (target_lang):', value);
        // Reload settings to get correct vocab level for new language
        await loadSettings();
      }
    }
  }

  async function handleNativeLanguageChange(value: string): Promise<void> {
    const newSettings = { ...settings, nativeLanguage: value };
    setSettings(newSettings);

    // Save to chrome.storage.local (instant, local)
    await saveSettings(newSettings);

    // Update Supabase (sync across devices)
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.user) {
      const { error } = await supabase
        .from('user_settings')
        .update({ native_lang: value })
        .eq('user_id', session.user.id);

      if (error) {
        console.error('Smart Netflix Subtitles: Supabase sync failed (native_lang):', error);
      } else {
        console.log('Smart Netflix Subtitles: Supabase synced (native_lang):', value);
      }
    }
  }

  // Open webapp for onboarding
  function handleSetupExtension(): void {
    chrome.tabs.create({ url: `${WEBAPP_URL}/welcome` });
  }

  // Open vocab test page with current target language
  function handleTestLevel(): void {
    const targetLang = settings.targetLanguage || '';
    const url = targetLang
      ? `${WEBAPP_URL}/onboarding/vocab-test?targetLanguage=${targetLang}`
      : `${WEBAPP_URL}/onboarding/vocab-test`;
    chrome.tabs.create({ url });
  }

  // Open Stripe Customer Portal
  async function handleManageSubscription(): Promise<void> {
    try {
      const { data: { session } } = await supabase.auth.getSession();

      if (!session?.user) {
        console.log('Smart Netflix Subtitles: No user session, redirecting to login');
        chrome.tabs.create({ url: `${WEBAPP_URL}/welcome` });
        return;
      }

      // Send message to background script (avoids CORS issues)
      chrome.runtime.sendMessage(
        {
          type: 'OPEN_STRIPE_PORTAL',
          userId: session.user.id,
        },
        (response) => {
          if (!response || !response.success) {
            console.error('Smart Netflix Subtitles: Failed to open portal:', response?.error);
            showStatus('Failed to open subscription portal', 'error');
          }
        }
      );
    } catch (error) {
      console.error('Smart Netflix Subtitles: Error opening portal:', error);
      showStatus('Failed to open subscription portal', 'error');
    }
  }

  // Get language name from code
  function getLanguageName(code: string): string {
    const languageNames: Record<string, string> = {
      'pt-BR': 'Portuguese',
      'fr': 'French',
      'en': 'English',
    };
    return languageNames[code] || code;
  }

  // Render Welcome popup for first-time users
  if (showWelcome) {
    return (
      <div className="w-[400px] p-6">
        <Card>
          <CardContent className="pt-6 text-center space-y-4">
            <div className="flex justify-center">
              <img
                src="images/ulysse-photo.jpg"
                alt="Ulysse"
                className="w-20 h-20 rounded-full object-cover"
              />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-semibold">Thanks for downloading my extension!</h2>
              <p className="text-sm text-muted-foreground">
                To get started, please complete the onboarding process to set up your learning preferences and vocabulary level.
              </p>
            </div>
            <Button onClick={handleSetupExtension} className="w-full">
              Set up the extension
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Render Normal popup for returning users
  const canProcess =
    settings.targetLanguage &&
    settings.nativeLanguage &&
    settings.vocabularyLevel &&
    settings.targetLanguage !== settings.nativeLanguage &&
    !isProcessing &&
    isOnNetflix;

  return (
    <div className="w-[400px] p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Subly</h2>
        <button
          onClick={handleManageSubscription}
          className="text-sm underline hover:no-underline"
        >
          manage subscription
        </button>
      </div>

      {/* Target Language */}
      <div className="space-y-2">
        <Label htmlFor="target-language">Target Language (Learning):</Label>
        <Select
          value={settings.targetLanguage}
          onValueChange={handleTargetLanguageChange}
          disabled={!isOnNetflix}
        >
          <SelectTrigger id="target-language">
            <SelectValue placeholder="Select a language" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="fr">French</SelectItem>
            <SelectItem value="pt-BR">Brazilian Portuguese</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Native Language */}
      <div className="space-y-2">
        <Label htmlFor="native-language">Native Language:</Label>
        <Select
          value={settings.nativeLanguage}
          onValueChange={handleNativeLanguageChange}
          disabled={!isOnNetflix}
        >
          <SelectTrigger id="native-language">
            <SelectValue placeholder="Select a language" />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(SUPPORTED_NATIVE_LANGUAGES)
              .sort(([, a], [, b]) => a.localeCompare(b))
              .map(([code, name]) => {
                const isAvailable = availableNativeLanguages.includes(code);
                return (
                  <SelectItem key={code} value={code} disabled={!isAvailable}>
                    {isAvailable ? name : `${name} (Undetected)`}
                  </SelectItem>
                );
              })}
          </SelectContent>
        </Select>
        <p className="text-xs text-muted-foreground">
          If your language appears as Undetected, try turning on the Netflix subtitles in that language so it can be detected.
        </p>
      </div>

      {/* Vocabulary Level */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label>Vocabulary Level</Label>
          <Button variant="outline" size="sm" onClick={handleTestLevel}>
            Test my level
          </Button>
        </div>
        <Card>
          <CardContent className="pt-4 text-sm">
            {!settings.targetLanguage ? (
              <p>Please select a target language above</p>
            ) : !settings.vocabularyLevel || settings.vocabularyLevel === 0 ? (
              <p>
                Your vocabulary level in {getLanguageName(settings.targetLanguage)} is not defined yet, please click on the button "test my level" above
              </p>
            ) : (
              <p>
                You know <strong>{settings.vocabularyLevel}</strong> of the most used words in{' '}
                <strong>{getLanguageName(settings.targetLanguage)}</strong>
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Process Button */}
      <Button onClick={processSubtitles} disabled={!canProcess} className="w-full">
        {isProcessing ? 'Processing...' : 'Process Subtitles'}
      </Button>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="flex items-center gap-2 text-sm">
          <div className="animate-spin h-4 w-4 border-2 border-primary border-t-transparent rounded-full" />
          <span>Subtitles loading... (this may take up to 20 seconds)</span>
        </div>
      )}

      {/* Status Message */}
      {statusMessage && (
        <div
          className={`text-sm p-2 rounded ${
            statusType === 'success'
              ? 'bg-green-100 text-green-800'
              : statusType === 'error'
              ? 'bg-red-100 text-red-800'
              : 'bg-blue-100 text-blue-800'
          }`}
        >
          {statusMessage}
        </div>
      )}

      {/* Feedback Banner */}
      <div className="text-xs text-center text-muted-foreground border-t pt-4">
        Any feedback? Please, send me an email at{' '}
        <a href="mailto:unducamp.pro@gmail.com" className="underline">
          unducamp.pro@gmail.com
        </a>
      </div>
    </div>
  );
}
