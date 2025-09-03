#!/usr/bin/env python3
"""
DeepL API Connection Test
Tests DeepL API connectivity with timeouts and error handling
"""

import os
import time
import httpx
from typing import Optional

def check_env_var(var_name: str) -> Optional[str]:
    """Check if environment variable exists and return its value"""
    value = os.getenv(var_name)
    if value:
        print(f"✅ {var_name}: {value[:20]}{'...' if len(value) > 20 else ''}")
        return value
    else:
        print(f"❌ {var_name}: NOT SET")
        return None

def test_deepl_api(api_key: str, timeout: int = 10) -> bool:
    """Test DeepL API connectivity with timeout"""
    print("🔗 Testing DeepL API connection...")
    
    try:
        with httpx.Client(timeout=timeout) as client:
            # Test usage endpoint
            print("📊 Testing usage endpoint...")
            response = client.get(
                "https://api-free.deepl.com/v2/usage",
                headers={"Authorization": f"DeepL-Auth-Key {api_key}"}
            )
            
            if response.status_code == 200:
                print("✅ DeepL API connection successful!")
                usage_data = response.json()
                print(f"📈 Character count: {usage_data.get('character_count', 'N/A')}")
                print(f"📊 Character limit: {usage_data.get('character_limit', 'N/A')}")
                return True
            elif response.status_code == 403:
                print("❌ DeepL API key invalid or expired")
                return False
            else:
                print(f"⚠️  DeepL API responded with status: {response.status_code}")
                return False
                
    except httpx.TimeoutException:
        print(f"⏰ Connection timeout after {timeout}s")
        return False
    except httpx.ConnectError as e:
        print(f"🔌 Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_deepl_translation(api_key: str, timeout: int = 10) -> bool:
    """Test DeepL translation with timeout"""
    print("🔄 Testing DeepL translation...")
    
    try:
        with httpx.Client(timeout=timeout) as client:
            # Test simple translation
            test_text = "Hello, world!"
            response = client.post(
                "https://api-free.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
                data={
                    "text": test_text,
                    "target_lang": "FR"
                }
            )
            
            if response.status_code == 200:
                print("✅ DeepL translation test successful!")
                translation_data = response.json()
                translations = translation_data.get('translations', [])
                if translations:
                    translated_text = translations[0].get('text', 'N/A')
                    print(f"📝 '{test_text}' → '{translated_text}'")
                return True
            else:
                print(f"⚠️  Translation test failed with status: {response.status_code}")
                return False
                
    except httpx.TimeoutException:
        print(f"⏰ Translation timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return False

def main():
    print("🔍 Starting DeepL API diagnostics...")
    print("=" * 50)
    
    # Check environment variables
    print("\n🌍 Checking environment variables:")
    deepl_key = check_env_var("DEEPL_API_KEY")
    
    if not deepl_key:
        print("\n❌ Missing DEEPL_API_KEY environment variable!")
        print("Please set DEEPL_API_KEY")
        return
    
    # Test API connection
    print(f"\n🚀 Testing DeepL API connection...")
    start_time = time.time()
    
    connection_success = test_deepl_api(deepl_key, timeout=10)
    connection_elapsed = time.time() - start_time
    
    if connection_success:
        # Test translation
        print(f"\n🔄 Testing DeepL translation...")
        translation_start = time.time()
        
        translation_success = test_deepl_translation(deepl_key, timeout=10)
        translation_elapsed = time.time() - translation_start
        
        print(f"\n⏱️  Connection test: {connection_elapsed:.3f}s")
        print(f"⏱️  Translation test: {translation_elapsed:.3f}s")
        
        if translation_success:
            print("\n🎉 DeepL API is working correctly!")
        else:
            print("\n⚠️  DeepL API connects but translation fails")
    else:
        print(f"\n⏱️  Connection test took: {connection_elapsed:.3f}s")
        print("\n💥 DeepL API connection failed!")
        print("Check your API key and network connectivity")

if __name__ == "__main__":
    main()
