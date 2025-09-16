#!/usr/bin/env python3
"""
Quick test script for rate limiting functionality.
Tests the /fuse-subtitles endpoint without waiting for rate limit reset.
"""

import requests
import time
import os
from typing import Dict, Any

# Configuration
BASE_URL = "https://smartsub-api-production.up.railway.app"
API_KEY = os.getenv("API_KEY", "sk-smartsub-abchgoehjoj135262gh256")

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

def test_rate_limiting_quick():
    """Quick test of rate limiting functionality."""
    print("🧪 Quick Rate Limiting Test")
    print("=" * 40)
    
    # Create test files
    files = create_test_files()
    
    try:
        # Test: Make 12 requests quickly to trigger rate limiting
        print("\n📋 Making 12 requests to trigger rate limiting...")
        success_count = 0
        rate_limited_count = 0
        
        for i in range(12):
            try:
                response = make_request(files)
                print(f"  Request {i+1:2d}: Status {response.status_code}", end="")
                
                if response.status_code == 200:
                    success_count += 1
                    print(" ✅")
                elif response.status_code == 429:
                    rate_limited_count += 1
                    print(" 🚫 (Rate Limited)")
                else:
                    print(f" ❌ (Unexpected: {response.status_code})")
                
                # Small delay to avoid overwhelming the server
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"  Request {i+1:2d}: ❌ Failed - {e}")
        
        print(f"\n📊 Results:")
        print(f"  ✅ Successful requests: {success_count}")
        print(f"  🚫 Rate limited requests: {rate_limited_count}")
        print(f"  📈 Total requests: {success_count + rate_limited_count}")
        
        # Analysis
        if rate_limited_count > 0:
            print(f"\n🎉 Rate limiting is working!")
            print(f"   - First {success_count} requests succeeded")
            print(f"   - Next {rate_limited_count} requests were rate limited")
        else:
            print(f"\n⚠️  Rate limiting may not be working")
            print(f"   - All {success_count} requests succeeded")
            print(f"   - Expected some requests to be rate limited")
        
    finally:
        # Clean up test files
        cleanup_test_files(files)

def test_health_endpoint():
    """Test that health endpoint is not rate limited."""
    print("\n🏥 Testing Health Endpoint")
    print("-" * 30)
    
    try:
        # Make multiple requests to health endpoint
        for i in range(5):
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            print(f"  Health request {i+1}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"    ❌ Health endpoint failed")
                return False
        
        print("  ✅ Health endpoint working (not rate limited)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Health endpoint test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Smart Subtitles API - Quick Rate Limiting Test")
    print("=" * 55)
    print(f"Testing against: {BASE_URL}")
    print(f"API Key: {'*' * (len(API_KEY) - 8) + API_KEY[-8:] if API_KEY else 'Not set'}")
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("\n❌ Health endpoint test failed. Aborting.")
        return
    
    # Test rate limiting
    test_rate_limiting_quick()
    
    print("\n🎉 Quick test completed!")
    print("\n💡 To test rate limit reset, run the full test:")
    print("   python test_rate_limiting.py")

if __name__ == "__main__":
    main()
