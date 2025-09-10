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
            
            # Translate text
            result = translator.translate_text(
                text, 
                source_lang=source_lang.upper(), 
                target_lang=target_lang.upper()
            )
            
            translation = result.text
            self.cache[cache_key] = translation
            self.request_count += 1
            
            return translation
            
        except Exception as e:
            print(f"DeepL translation error: {e}")
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
