"""
DeepL API integration - Python implementation
Migrated from TypeScript deepl-api.ts
"""

from typing import Dict, Any, Optional, List
import requests
import time

class DeepLAPI:
    """
    DeepL API client for translation services
    Migrated from TypeScript DeepLAPI class
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api-free.deepl.com/v2/translate", 
                 timeout: int = 5000, max_retries: int = 3, retry_delay: int = 1000, 
                 rate_limit_delay: int = 1000):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self.request_count = 0
        self.cache = {}
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using DeepL API
        Migrated from TypeScript translate method
        """
        # Check cache first
        cache_key = f"{text}_{source_lang}_{target_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            import deepl
            
            # Initialize DeepL translator
            translator = deepl.Translator(self.api_key)
            
            # Map language codes for DeepL compatibility
            # Note: DeepL uses different codes for source vs target languages
            source_lang_mapping = {
                'EN': 'EN',  # Source language uses EN, not EN-US
                'FR': 'FR',
                'PT': 'PT'
            }
            
            target_lang_mapping = {
                'EN': 'EN-US',  # Target language uses EN-US
                'FR': 'FR',
                'PT': 'PT'
            }
            
            mapped_source_lang = source_lang_mapping.get(source_lang.upper(), source_lang.upper())
            mapped_target_lang = target_lang_mapping.get(target_lang.upper(), target_lang.upper())
            
            # Translate text
            result = translator.translate_text(
                text, 
                source_lang=mapped_source_lang, 
                target_lang=mapped_target_lang
            )
            
            translation = result.text
            self.cache[cache_key] = translation
            self.request_count += 1
            
            return translation
            
        except Exception as e:
            print(f"DeepL translation error: {e}")
            return text  # Fallback to original text
    
    def translate_batch(self, words: List[str], source_lang: str, target_lang: str) -> List[str]:
        """
        Translate multiple words in a single DeepL API request
        Optimized for batch processing to reduce API calls
        """
        if not words:
            return []
        
        # Separate cached and uncached words
        cached_translations = []
        uncached_words = []
        uncached_indices = []
        
        for i, word in enumerate(words):
            cache_key = f"{word}_{source_lang}_{target_lang}"
            if cache_key in self.cache:
                cached_translations.append((i, self.cache[cache_key]))
            else:
                uncached_words.append(word)
                uncached_indices.append(i)
        
        # Translate only uncached words if any
        if uncached_words:
            try:
                import deepl
                
                # Initialize DeepL translator
                translator = deepl.Translator(self.api_key)
                
                # Map language codes for DeepL compatibility
                # Note: DeepL uses different codes for source vs target languages
                source_lang_mapping = {
                    'EN': 'EN',  # Source language uses EN, not EN-US
                    'FR': 'FR',
                    'PT': 'PT'
                }
                
                target_lang_mapping = {
                    'EN': 'EN-US',  # Target language uses EN-US
                    'FR': 'FR',
                    'PT': 'PT'
                }
                
                mapped_source_lang = source_lang_mapping.get(source_lang.upper(), source_lang.upper())
                mapped_target_lang = target_lang_mapping.get(target_lang.upper(), target_lang.upper())
                
                # Translate all uncached words in a single request
                results = translator.translate_text(
                    uncached_words, 
                    source_lang=mapped_source_lang, 
                    target_lang=mapped_target_lang
                )
                
                # Cache the new translations and add to cached_translations
                for i, result in enumerate(results):
                    word = uncached_words[i]
                    translation = result.text
                    cache_key = f"{word}_{source_lang}_{target_lang}"
                    self.cache[cache_key] = translation
                    cached_translations.append((uncached_indices[i], translation))
                
                self.request_count += 1  # Count as one API request
                
            except Exception as e:
                print(f"DeepL batch translation error: {e}")
                # Fallback: return original words for uncached ones
                for i, word in enumerate(uncached_words):
                    cached_translations.append((uncached_indices[i], word))
        
        # Sort by original index and return translations in correct order
        cached_translations.sort(key=lambda x: x[0])
        return [translation for _, translation in cached_translations]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get API usage statistics
        Migrated from TypeScript getStats method
        """
        return {
            "requestCount": self.request_count,
            "cacheSize": len(self.cache)
        }