#!/usr/bin/env python3
"""
Test script to verify SmartSub API functionality
Tests both the FastAPI endpoints and the Node.js CLI integration
"""

import requests
import json
import tempfile
import os
import subprocess
import sys
from pathlib import Path

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def create_test_files():
    """Create test SRT and frequency files"""
    print("📝 Creating test files...")
    
    # Sample target SRT (English)
    target_srt = """1
00:00:01,000 --> 00:00:03,000
Hello world, this is a test.

2
00:00:04,000 --> 00:00:06,000
This is another subtitle line.

3
00:00:07,000 --> 00:00:09,000
Testing the subtitle fusion algorithm.
"""
    
    # Sample native SRT (French)
    native_srt = """1
00:00:01,000 --> 00:00:03,000
Bonjour le monde, ceci est un test.

2
00:00:04,000 --> 00:00:06,000
Ceci est une autre ligne de sous-titre.

3
00:00:07,000 --> 00:00:09,000
Test de l'algorithme de fusion de sous-titres.
"""
    
    # Sample frequency list
    frequency_list = """hello
world
test
subtitle
algorithm
fusion
another
line
this
is
"""
    
    return target_srt, native_srt, frequency_list

def test_fuse_subtitles_endpoint(base_url, api_key=None):
    """Test the fuse-subtitles endpoint"""
    print("🔍 Testing fuse-subtitles endpoint...")
    
    target_srt, native_srt, frequency_list = create_test_files()
    
    # Prepare form data
    data = {
        'target_language': 'en',
        'native_language': 'fr',
        'top_n_words': 1000,
        'enable_inline_translation': False
    }
    
    # Prepare files
    files = {
        'target_srt': ('target.srt', target_srt, 'text/plain'),
        'native_srt': ('native.srt', native_srt, 'text/plain'),
        'frequency_list': ('frequency.txt', frequency_list, 'text/plain')
    }
    
    # Add API key if provided
    params = {}
    if api_key:
        params['api_key'] = api_key
    
    try:
        response = requests.post(
            f"{base_url}/fuse-subtitles",
            data=data,
            files=files,
            params=params,
            timeout=60  # Longer timeout for processing
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Fuse-subtitles endpoint working")
                print(f"   Output length: {len(result.get('output_srt', ''))} characters")
                return True
            else:
                print(f"❌ Fuse-subtitles failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Fuse-subtitles endpoint failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Fuse-subtitles endpoint error: {e}")
        return False

def test_node_cli_directly():
    """Test the Node.js CLI directly (if running locally)"""
    print("🔍 Testing Node.js CLI directly...")
    
    try:
        # Check if we're in the right directory
        if not os.path.exists('dist/main.js'):
            print("⚠️  Node.js CLI not found (dist/main.js missing)")
            return False
        
        # Create test files
        target_srt, native_srt, frequency_list = create_test_files()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_target, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_native, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_freq, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_output:
            
            temp_target.write(target_srt)
            temp_native.write(native_srt)
            temp_freq.write(frequency_list)
            
            temp_target.close()
            temp_native.close()
            temp_freq.close()
            temp_output.close()
            
            # Run CLI
            cmd = [
                'node', 'dist/main.js',
                '--target', temp_target.name,
                '--native', temp_native.name,
                '--freq', temp_freq.name,
                '--out', temp_output.name,
                '--topN', '1000',
                '--lang', 'en',
                '--native-lang', 'fr'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Node.js CLI working directly")
                return True
            else:
                print(f"❌ Node.js CLI failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Node.js CLI test error: {e}")
        return False
    finally:
        # Cleanup temp files
        for temp_file in [temp_target.name, temp_native.name, temp_freq.name, temp_output.name]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

def main():
    """Main test function"""
    print("🧪 SmartSub API Functionality Test")
    print("=" * 40)
    
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:3000"
    
    print(f"Testing API at: {base_url}")
    print()
    
    # Test results
    results = []
    
    # Test endpoints
    results.append(("Health Endpoint", test_health_endpoint(base_url)))
    results.append(("Root Endpoint", test_root_endpoint(base_url)))
    
    # Test API key (if provided as environment variable)
    api_key = os.getenv('API_KEY')
    if api_key:
        print(f"Using API key: {api_key[:8]}...")
    else:
        print("No API key provided (testing without authentication)")
    
    results.append(("Fuse Subtitles Endpoint", test_fuse_subtitles_endpoint(base_url, api_key)))
    
    # Test Node.js CLI directly (only if running locally)
    if base_url == "http://localhost:3000":
        results.append(("Node.js CLI Direct", test_node_cli_directly()))
    
    # Summary
    print()
    print("📊 Test Results Summary:")
    print("-" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit(main())
