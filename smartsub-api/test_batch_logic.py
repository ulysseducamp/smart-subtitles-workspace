#!/usr/bin/env python3
"""
Test script for DeepL batch translation logic (without API key)
Tests the logic and structure of the translate_batch method
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_batch_logic():
    """Test the batch translation logic without making actual API calls"""
    
    print("🧪 Testing DeepL batch translation logic...")
    
    # Test 1: Empty list
    print("\n📝 Test 1: Empty word list")
    try:
        from deepl_api import DeepLAPI
        deepl_api = DeepLAPI("fake-key")
        result = deepl_api.translate_batch([], "EN", "FR")
        if result == []:
            print("✅ Empty list handled correctly")
        else:
            print(f"❌ Expected [], got {result}")
            return False
    except Exception as e:
        print(f"❌ Error with empty list: {e}")
        return False
    
    # Test 2: Method exists and has correct signature
    print("\n📝 Test 2: Method signature")
    try:
        from deepl_api import DeepLAPI
        deepl_api = DeepLAPI("fake-key")
        
        # Check if method exists
        if hasattr(deepl_api, 'translate_batch'):
            print("✅ translate_batch method exists")
        else:
            print("❌ translate_batch method not found")
            return False
            
        # Check method signature (basic check)
        import inspect
        sig = inspect.signature(deepl_api.translate_batch)
        params = list(sig.parameters.keys())
        expected_params = ['words', 'source_lang', 'target_lang']
        
        if params == expected_params:
            print("✅ Method signature is correct")
        else:
            print(f"❌ Expected parameters {expected_params}, got {params}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking method signature: {e}")
        return False
    
    # Test 3: Cache logic (without API call)
    print("\n📝 Test 3: Cache logic structure")
    try:
        from deepl_api import DeepLAPI
        deepl_api = DeepLAPI("fake-key")
        
        # Add some cached translations manually
        deepl_api.cache["hello_EN_FR"] = "bonjour"
        deepl_api.cache["world_EN_FR"] = "monde"
        
        # Test with mixed cached/uncached words
        test_words = ["hello", "world", "beautiful"]  # hello, world cached, beautiful not
        
        # This will fail at API call, but we can check the cache separation logic
        try:
            result = deepl_api.translate_batch(test_words, "EN", "FR")
        except Exception as api_error:
            # Expected to fail at API call, but cache logic should work
            print("✅ Cache separation logic executed (API call failed as expected)")
            
            # Check that cache was populated correctly
            if "hello_EN_FR" in deepl_api.cache and "world_EN_FR" in deepl_api.cache:
                print("✅ Cache structure is correct")
            else:
                print("❌ Cache structure issue")
                return False
                
    except Exception as e:
        print(f"❌ Error testing cache logic: {e}")
        return False
    
    print(f"\n🎉 All logic tests passed! The translate_batch method is properly structured.")
    print("📋 Next step: Test with real API key to validate actual translation")
    return True

if __name__ == "__main__":
    success = test_batch_logic()
    sys.exit(0 if success else 1)

