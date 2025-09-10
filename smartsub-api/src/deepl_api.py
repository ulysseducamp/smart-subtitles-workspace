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
        import time
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{text}_{source_lang}_{target_lang}"
        if cache_key in self.cache:
            print(f"TIMING: DeepL cache hit for '{text}' in {time.time() - start_time:.3f}s")
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
            
            translation_time = time.time() - start_time
            print(f"TIMING: DeepL translation '{text}' -> '{translation}' completed in {translation_time:.3f}s")
            
            return translation
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"TIMING: DeepL translation error for '{text}' after {error_time:.3f}s: {e}")
            return text  # Fallback to original text
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get API usage statistics
        Migrated from TypeScript getStats method
        """
        return {
            "requestCount": self.request_count,
            "cacheSize": len(self.cache)
        }
