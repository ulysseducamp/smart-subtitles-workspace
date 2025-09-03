#!/usr/bin/env python3
"""
Supabase Connection Test
Tests Supabase connectivity with timeouts and error handling
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

def test_supabase_connection(url: str, key: str, timeout: int = 10) -> bool:
    """Test Supabase connection with timeout"""
    print(f"🔗 Testing Supabase connection to: {url}")
    
    try:
        with httpx.Client(timeout=timeout) as client:
            # Test basic connectivity
            print("📡 Testing basic connectivity...")
            response = client.get(f"{url}/rest/v1/", headers={
                "apikey": key,
                "Authorization": f"Bearer {key}"
            })
            
            if response.status_code == 200:
                print("✅ Supabase connection successful!")
                return True
            else:
                print(f"⚠️  Supabase responded with status: {response.status_code}")
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

def main():
    print("🔍 Starting Supabase diagnostics...")
    print("=" * 50)
    
    # Check environment variables
    print("\n🌍 Checking environment variables:")
    supabase_url = check_env_var("SUPABASE_URL")
    supabase_key = check_env_var("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("\n❌ Missing required environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY")
        return
    
    # Test connection
    print(f"\n🚀 Testing Supabase connection...")
    start_time = time.time()
    
    success = test_supabase_connection(supabase_url, supabase_key, timeout=10)
    
    elapsed = time.time() - start_time
    print(f"⏱️  Connection test took: {elapsed:.3f}s")
    
    if success:
        print("\n🎉 Supabase is working correctly!")
    else:
        print("\n💥 Supabase connection failed!")
        print("Check your credentials and network connectivity")

if __name__ == "__main__":
    main()
