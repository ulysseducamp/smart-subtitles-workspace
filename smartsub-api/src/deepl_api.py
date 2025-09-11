"""
DeepL API integration - Python implementation
Migrated from TypeScript deepl-api.ts
"""

from typing import Dict, Any, Optional
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
            lang_mapping = {
                'EN': 'EN-US',  # Use US English instead of deprecated EN
                'FR': 'FR',
                'PT': 'PT', 
                'ES': 'ES'
            }
            
            mapped_source_lang = lang_mapping.get(source_lang.upper(), source_lang.upper())
            mapped_target_lang = lang_mapping.get(target_lang.upper(), target_lang.upper())
            
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
    
    def translate_with_context(self, word: str, context: str, source_lang: str, target_lang: str) -> str:
        """
        Translate a word with context for better accuracy
        Uses the context to provide more precise translations
        """
        # Create a context-aware translation request
        # Format: "Translate 'word' in this context: context"
        context_text = f"Translate '{word}' in this context: {context}"
        
        # Check cache first
        cache_key = f"{context_text}_{source_lang}_{target_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            import deepl
            
            # Initialize DeepL translator
            translator = deepl.Translator(self.api_key)
            
            # Map language codes for DeepL compatibility
            lang_mapping = {
                'EN': 'EN-US',  # Use US English instead of deprecated EN
                'FR': 'FR',
                'PT': 'PT', 
                'ES': 'ES'
            }
            
            mapped_source_lang = lang_mapping.get(source_lang.upper(), source_lang.upper())
            mapped_target_lang = lang_mapping.get(target_lang.upper(), target_lang.upper())
            
            # Translate with context
            result = translator.translate_text(
                context_text, 
                source_lang=mapped_source_lang, 
                target_lang=mapped_target_lang
            )
            
            # Extract just the translated word from the result
            # The result should be something like "Translate 'emeralds' in this context: ..."
            # We need to extract just the word part
            translation = result.text
            
            # Try to extract the word from the translation
            # Look for the word in quotes or after "Translate"
            import re
            word_match = re.search(r"Translate\s+'([^']+)'", translation)
            if word_match:
                translation = word_match.group(1)
            else:
                # Fallback: try to find the word in the translation
                # This is a simple heuristic - might need refinement
                words = translation.split()
                if words:
                    translation = words[0]  # Take the first word as fallback
            
            self.cache[cache_key] = translation
            self.request_count += 1
            
            return translation
            
        except Exception as e:
            print(f"DeepL context translation error: {e}")
            # Fallback to regular translation without context
            return self.translate(word, source_lang, target_lang)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get API usage statistics
        Migrated from TypeScript getStats method
        """
        return {
            "requestCount": self.request_count,
            "cacheSize": len(self.cache)
        }
