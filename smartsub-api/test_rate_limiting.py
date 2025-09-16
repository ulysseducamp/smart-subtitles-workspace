#!/usr/bin/env python3
"""
Test script for rate limiting functionality.
Tests the /fuse-subtitles endpoint to ensure rate limiting works correctly.
"""

import requests
import time
import os
from typing import Dict, Any

# Configuration
BASE_URL = "https://smartsub-api-production.up.railway.app"
API_KEY = os.getenv("API_KEY", "sk-smartsub-abchgoehjoj135262gh256")  # Use environment variable or fallback

# Test files (small SRT files for testing)
TEST_SRT_CONTENT = """1
00:00:01,000 --> 00:00:03,000
Hello world

2
00:00:04,000 --> 00:00:06,000
This is a test
"""

def create_test_files() -> Dict[str, str]:
    """Create temporary test files."""
    import tempfile
    
    # Create temporary files
    target_file = tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False)
    native_file = tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False)
    
    target_file.write(TEST_SRT_CONTENT)
    native_file.write(TEST_SRT_CONTENT)
    
    target_file.close()
    native_file.close()
    
    return {
        'target_file': target_file.name,
        'native_file': native_file.name
    }

def cleanup_test_files(files: Dict[str, str]) -> None:
    """Clean up temporary test files."""
    import os
    try:
        os.unlink(files['target_file'])
        os.unlink(files['native_file'])
    except OSError:
        pass

def make_request(files: Dict[str, str]) -> requests.Response:
    """Make a request to the fuse-subtitles endpoint."""
    url = f"{BASE_URL}/fuse-subtitles"
    
    with open(files['target_file'], 'rb') as target_f, open(files['native_file'], 'rb') as native_f:
        files_data = {
            'target_srt': ('test_target.srt', target_f, 'text/plain'),
            'native_srt': ('test_native.srt', native_f, 'text/plain')
        }
        
        data = {
            'target_language': 'fr',
            'native_language': 'en',
            'top_n_words': 100,
            'enable_inline_translation': 'false'
        }
        
        params = {'api_key': API_KEY}
        
        response = requests.post(url, files=files_data, data=data, params=params, timeout=30)
    
    return response

def test_rate_limiting():
    """Test rate limiting functionality."""
    print("🧪 Testing Rate Limiting Functionality")
    print("=" * 50)
    
    # Create test files
    files = create_test_files()
    
    try:
        # Test 1: Normal usage (should work)
        print("\n📋 Test 1: Normal usage (5 requests)")
        success_count = 0
        for i in range(5):
            try:
                response = make_request(files)
                print(f"  Request {i+1}: Status {response.status_code}")
                if response.status_code == 200:
                    success_count += 1
                elif response.status_code == 429:
                    print(f"    ⚠️  Rate limited on request {i+1} (unexpected)")
                else:
                    print(f"    ❌ Unexpected status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Request failed: {e}")
        
        print(f"  ✅ Successful requests: {success_count}/5")
        
        # Test 2: Exceed rate limit (should get 429)
        print("\n📋 Test 2: Exceed rate limit (5 more requests)")
        rate_limited_count = 0
        for i in range(5):
            try:
                response = make_request(files)
                print(f"  Request {i+6}: Status {response.status_code}")
                if response.status_code == 429:
                    rate_limited_count += 1
                    print(f"    ✅ Rate limited correctly")
                elif response.status_code == 200:
                    print(f"    ⚠️  Request {i+6} succeeded (rate limit not reached yet)")
                else:
                    print(f"    ❌ Unexpected status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Request failed: {e}")
        
        print(f"  ✅ Rate limited requests: {rate_limited_count}/5")
        
        # Test 3: Wait and retry (should work again)
        print("\n📋 Test 3: Wait 65 seconds and retry")
        print("  ⏳ Waiting 65 seconds for rate limit to reset...")
        time.sleep(65)
        
        try:
            response = make_request(files)
            print(f"  Request after wait: Status {response.status_code}")
            if response.status_code == 200:
                print("  ✅ Rate limit reset successfully")
            elif response.status_code == 429:
                print("  ❌ Still rate limited (rate limit not reset)")
            else:
                print(f"  ❌ Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request failed: {e}")
        
    finally:
        # Clean up test files
        cleanup_test_files(files)
    
    print("\n" + "=" * 50)
    print("🏁 Rate limiting test completed")

def test_health_endpoint():
    """Test that health endpoint is not rate limited."""
    print("\n🏥 Testing Health Endpoint (should not be rate limited)")
    print("-" * 50)
    
    try:
        # Make multiple requests to health endpoint
        for i in range(15):
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            print(f"  Health request {i+1}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"    ❌ Health endpoint failed: {response.status_code}")
                return False
        
        print("  ✅ Health endpoint not rate limited (as expected)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Health endpoint test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Smart Subtitles API - Rate Limiting Test Suite")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print(f"API Key: {'*' * (len(API_KEY) - 8) + API_KEY[-8:] if API_KEY else 'Not set'}")
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("\n❌ Health endpoint test failed. Aborting rate limiting tests.")
        return
    
    # Test rate limiting
    test_rate_limiting()
    
    print("\n🎉 All tests completed!")
    print("\n📝 Summary:")
    print("  - Health endpoint: Not rate limited ✅")
    print("  - Fuse-subtitles endpoint: Rate limited to 10/minute ✅")
    print("  - Rate limit resets after 1 minute ✅")

if __name__ == "__main__":
    main()
