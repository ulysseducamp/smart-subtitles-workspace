#!/usr/bin/env python3
"""
Test script for DeepL batch translation functionality
Tests the new translate_batch() method
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from deepl_api import DeepLAPI

def test_batch_translation():
    """Test the new translate_batch method"""
    
    # Get API key from environment or .env.test file
    api_key = os.getenv("DEEPL_API_KEY")
    
    # Try to load from .env.test file if not in environment
    if not api_key:
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env.test')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DEEPL_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
    
    if not api_key:
        print("❌ DEEPL_API_KEY not found in environment variables or .env.test file")
        print("Please set your DeepL API key: export DEEPL_API_KEY='your-key-here'")
        return False
    
    print("🧪 Testing DeepL batch translation...")
    
    # Initialize DeepL API
    deepl_api = DeepLAPI(api_key)
    
    # Test words to translate
    test_words = ["hello", "world", "beautiful", "day", "sunshine"]
    source_lang = "EN"
    target_lang = "FR"
    
    print(f"📝 Testing with words: {test_words}")
    print(f"🌐 Translation: {source_lang} → {target_lang}")
    
    try:
        # Test batch translation
        print("\n🔄 Testing batch translation...")
        translations = deepl_api.translate_batch(test_words, source_lang, target_lang)
        
        print(f"✅ Batch translation successful!")
        print(f"📊 Results:")
        for i, (original, translation) in enumerate(zip(test_words, translations)):
            print(f"  {i+1}. '{original}' → '{translation}'")
        
        # Test cache functionality
        print(f"\n🔄 Testing cache (should be instant)...")
        cached_translations = deepl_api.translate_batch(test_words, source_lang, target_lang)
        
        if cached_translations == translations:
            print("✅ Cache working correctly!")
        else:
            print("❌ Cache not working properly")
            return False
        
        # Test API stats
        stats = deepl_api.get_stats()
        print(f"\n📈 API Statistics:")
        print(f"  - Total requests: {stats['requestCount']}")
        print(f"  - Cache size: {stats['cacheSize']}")
        
        # Verify we only made 1 API request for the batch
        if stats['requestCount'] == 1:
            print("✅ Only 1 API request made (batch working correctly)")
        else:
            print(f"❌ Expected 1 API request, got {stats['requestCount']}")
            return False
        
        print(f"\n🎉 All tests passed! Batch translation is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_batch_translation()
    sys.exit(0 if success else 1)
