#!/usr/bin/env python3
"""
Test script for CORS configuration validation in production
Tests both allowed and blocked origins on Railway deployment
"""

import requests
import sys
import time

def test_cors_origin(base_url, origin, should_allow=True):
    """Test CORS preflight request for a specific origin"""
    try:
        headers = {
            'Origin': origin,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{base_url}/fuse-subtitles", headers=headers, timeout=10)
        
        # Check if CORS headers are present
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')
        cors_headers = response.headers.get('Access-Control-Allow-Headers')
        
        if should_allow:
            if cors_origin == origin or cors_origin == '*':
                print(f"✅ ALLOWED: {origin} - CORS headers present")
                print(f"   - Allow-Origin: {cors_origin}")
                print(f"   - Allow-Methods: {cors_methods}")
                print(f"   - Allow-Headers: {cors_headers}")
                return True
            else:
                print(f"❌ BLOCKED: {origin} - Expected to be allowed but was blocked")
                print(f"   - Allow-Origin: {cors_origin}")
                return False
        else:
            if cors_origin is None or cors_origin != origin:
                print(f"✅ BLOCKED: {origin} - Correctly blocked (no CORS headers)")
                return True
            else:
                print(f"❌ ALLOWED: {origin} - Expected to be blocked but was allowed")
                print(f"   - Allow-Origin: {cors_origin}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR testing {origin}: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Testing CORS Configuration in Production")
    print("=" * 60)
    
    # Test against Railway production server
    base_url = "https://smartsub-api-production.up.railway.app"
    
    # Test allowed origins
    print("\n📋 Testing ALLOWED Origins:")
    allowed_origins = [
        "https://www.netflix.com",
        "https://netflix.com"
    ]
    
    allowed_results = []
    for origin in allowed_origins:
        result = test_cors_origin(base_url, origin, should_allow=True)
        allowed_results.append(result)
    
    # Test blocked origins
    print("\n🚫 Testing BLOCKED Origins:")
    blocked_origins = [
        "https://malicious-site.com",
        "https://evil.com",
        "https://google.com",
        "https://facebook.com"
    ]
    
    blocked_results = []
    for origin in blocked_origins:
        result = test_cors_origin(base_url, origin, should_allow=False)
        blocked_results.append(result)
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 60)
    
    allowed_passed = sum(allowed_results)
    blocked_passed = sum(blocked_results)
    
    print(f"Allowed origins: {allowed_passed}/{len(allowed_origins)} passed")
    print(f"Blocked origins: {blocked_passed}/{len(blocked_origins)} passed")
    
    if allowed_passed == len(allowed_origins) and blocked_passed == len(blocked_origins):
        print("🎉 All CORS tests PASSED! Configuration is secure.")
        return 0
    else:
        print("⚠️  Some CORS tests FAILED! Check configuration.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

