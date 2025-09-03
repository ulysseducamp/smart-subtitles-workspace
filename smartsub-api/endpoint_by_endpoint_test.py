#!/usr/bin/env python3
"""
Endpoint by Endpoint Test - Test each endpoint individually
Identify which specific endpoint fails
"""

import time
import uvicorn
import subprocess
from main import app

def test_endpoint(port: int, endpoint: str, expected_response: str = None):
    """Test a specific endpoint"""
    print(f"\n🔍 Testing endpoint: {endpoint}")
    
    url = f"http://localhost:{port}{endpoint}"
    print(f"📡 URL: {url}")
    
    try:
        # Test with curl
        result = subprocess.run(
            f"curl -s -w 'HTTP_STATUS:%{{http_code}}' {url}",
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse response
            output = result.stdout
            if 'HTTP_STATUS:' in output:
                response, status = output.split('HTTP_STATUS:')
                status = status.strip()
                response = response.strip()
                
                print(f"✅ HTTP Status: {status}")
                print(f"📄 Response: {response[:200]}{'...' if len(response) > 200 else ''}")
                
                if expected_response and expected_response in response:
                    print(f"✅ Expected content found: {expected_response}")
                return True
            else:
                print(f"✅ Response: {output[:200]}{'...' if len(output) > 200 else ''}")
                return True
        else:
            print(f"❌ Curl failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Request timeout")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    print("🔍 Starting Endpoint by Endpoint Test...")
    print("=" * 60)
    
    print("📝 Testing your main.py app on port 3000")
    print("🌐 Server will start on http://127.0.0.1:3000")
    
    # Start server in background
    print("\n🚀 Starting server...")
    
    import threading
    
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=3000, log_level="info")
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test each endpoint individually
    print("\n🧪 Testing endpoints individually...")
    
    endpoints = [
        ("/", "Smart Netflix Subtitles API"),
        ("/health", "smartsub-api"),
    ]
    
    results = {}
    
    for endpoint, expected in endpoints:
        success = test_endpoint(3000, endpoint, expected)
        results[endpoint] = success
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Endpoint Test Results:")
    
    for endpoint, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {endpoint}: {status}")
    
    # Analysis
    print("\n🎯 Analysis:")
    working_endpoints = [ep for ep, success in results.items() if success]
    failing_endpoints = [ep for ep, success in results.items() if not success]
    
    if working_endpoints:
        print(f"✅ Working endpoints: {', '.join(working_endpoints)}")
    
    if failing_endpoints:
        print(f"❌ Failing endpoints: {', '.join(failing_endpoints)}")
    
    if all(results.values()):
        print("🎉 All endpoints work - your API is fully functional!")
    elif any(results.values()):
        print("⚠️  Some endpoints work, others don't - partial functionality")
    else:
        print("💥 No endpoints work - fundamental API issue")
    
    print("\n🎯 Endpoint by endpoint test complete!")

if __name__ == "__main__":
    main()
