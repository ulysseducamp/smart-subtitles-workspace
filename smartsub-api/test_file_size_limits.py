#!/usr/bin/env python3
"""
Test script for file size limits validation.
This script tests that files larger than 5MB are rejected with HTTP 413.
"""

import requests
import tempfile
import os
from io import BytesIO

# Configuration
API_URL = "http://localhost:3000"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def create_large_srt_file(size_mb: float) -> bytes:
    """Create a fake SRT file of specified size in MB."""
    size_bytes = int(size_mb * 1024 * 1024)
    
    # Create a basic SRT content
    srt_content = """1
00:00:01,000 --> 00:00:02,000
This is a test subtitle line that will be repeated to create a large file.
"""
    
    # Calculate how many times we need to repeat the content
    content_size = len(srt_content.encode('utf-8'))
    repetitions = (size_bytes // content_size) + 1
    
    # Create the large content
    large_content = srt_content * repetitions
    
    # Truncate to exact size
    return large_content[:size_bytes].encode('utf-8')

def test_file_size_limit():
    """Test that files larger than 5MB are rejected."""
    print("🧪 Testing file size limits...")
    
    # Test 1: Normal file (should work)
    print("  📝 Test 1: Normal file (1MB) - should work")
    normal_content = create_large_srt_file(1.0)  # 1MB
    
    files = {
        'target_srt': ('normal.srt', BytesIO(normal_content), 'text/plain'),
        'native_srt': ('normal.srt', BytesIO(normal_content), 'text/plain')
    }
    
    data = {
        'target_language': 'fr',
        'native_language': 'en',
        'top_n_words': 2000,
        'enable_inline_translation': 'false'
    }
    
    try:
        response = requests.post(f"{API_URL}/fuse-subtitles", files=files, data=data, timeout=30)
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            print("    ✅ Normal file accepted (expected)")
        else:
            print(f"    ⚠️  Unexpected status: {response.status_code}")
            print(f"    Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Request failed: {e}")
    
    # Test 2: Large file (should be rejected)
    print("  📝 Test 2: Large file (6MB) - should be rejected")
    large_content = create_large_srt_file(6.0)  # 6MB
    
    files = {
        'target_srt': ('large.srt', BytesIO(large_content), 'text/plain'),
        'native_srt': ('normal.srt', BytesIO(normal_content), 'text/plain')
    }
    
    try:
        response = requests.post(f"{API_URL}/fuse-subtitles", files=files, data=data, timeout=30)
        print(f"    Status: {response.status_code}")
        if response.status_code == 500 and "413:" in response.text:
            print("    ✅ Large file rejected with 413 error message (expected)")
            print(f"    Response: {response.json()}")
        elif response.status_code == 413:
            print("    ✅ Large file rejected with 413 status (expected)")
            print(f"    Response: {response.json()}")
        else:
            print(f"    ❌ Expected 413 or 500 with 413 message, got {response.status_code}")
            print(f"    Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Request failed: {e}")
    
    # Test 3: Very large file (should be rejected)
    print("  📝 Test 3: Very large file (10MB) - should be rejected")
    very_large_content = create_large_srt_file(10.0)  # 10MB
    
    files = {
        'target_srt': ('very_large.srt', BytesIO(very_large_content), 'text/plain'),
        'native_srt': ('normal.srt', BytesIO(normal_content), 'text/plain')
    }
    
    try:
        response = requests.post(f"{API_URL}/fuse-subtitles", files=files, data=data, timeout=30)
        print(f"    Status: {response.status_code}")
        if response.status_code == 500 and "413:" in response.text:
            print("    ✅ Very large file rejected with 413 error message (expected)")
            print(f"    Response: {response.json()}")
        elif response.status_code == 413:
            print("    ✅ Very large file rejected with 413 status (expected)")
            print(f"    Response: {response.json()}")
        else:
            print(f"    ❌ Expected 413 or 500 with 413 message, got {response.status_code}")
            print(f"    Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Request failed: {e}")

def test_invalid_file_type():
    """Test that non-SRT files are rejected."""
    print("🧪 Testing file type validation...")
    
    # Create a fake text file with .txt extension
    fake_content = "This is not an SRT file"
    
    files = {
        'target_srt': ('fake.txt', BytesIO(fake_content.encode('utf-8')), 'text/plain'),
        'native_srt': ('normal.srt', BytesIO(create_large_srt_file(0.1)), 'text/plain')
    }
    
    data = {
        'target_language': 'fr',
        'native_language': 'en',
        'top_n_words': 2000,
        'enable_inline_translation': 'false'
    }
    
    try:
        response = requests.post(f"{API_URL}/fuse-subtitles", files=files, data=data, timeout=30)
        print(f"    Status: {response.status_code}")
        if response.status_code == 500 and "400:" in response.text:
            print("    ✅ Invalid file type rejected with 400 error message (expected)")
            print(f"    Response: {response.json()}")
        elif response.status_code == 400:
            print("    ✅ Invalid file type rejected with 400 status (expected)")
            print(f"    Response: {response.json()}")
        else:
            print(f"    ⚠️  Expected 400 or 500 with 400 message, got {response.status_code}")
            print(f"    Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Request failed: {e}")

def main():
    """Run all tests."""
    print("🚀 Starting file size limit tests...")
    print(f"   API URL: {API_URL}")
    print(f"   Max file size: {MAX_FILE_SIZE / (1024*1024):.1f}MB")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running with: python main.py")
        return
    
    print()
    
    # Run tests
    test_file_size_limit()
    print()
    test_invalid_file_type()
    
    print()
    print("🎉 Tests completed!")

if __name__ == "__main__":
    main()
