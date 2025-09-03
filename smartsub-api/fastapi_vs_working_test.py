#!/usr/bin/env python3
"""
FastAPI vs Working Server Test - Direct comparison
Test FastAPI against the working built-in HTTP server
"""

import subprocess
import time
import socket
import threading
from pathlib import Path

def test_working_server(port: int = 8080) -> bool:
    """Test the working built-in HTTP server"""
    print(f"✅ Testing WORKING built-in HTTP server on port {port}...")
    
    try:
        # Start working server
        cmd = f"python3 -m http.server {port} --bind 127.0.0.1"
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test HTTP request
        try:
            import urllib.request
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}", timeout=5)
            content = response.read()
            response.close()
            
            print(f"✅ Working server HTTP request successful (length: {len(content)} chars)")
            print(f"📄 First 100 chars: {content[:100].decode()}")
            
            # Stop server
            process.terminate()
            process.wait()
            return True
            
        except Exception as e:
            print(f"❌ Working server HTTP request failed: {e}")
            process.terminate()
            process.wait()
            return False
            
    except Exception as e:
        print(f"❌ Working server error: {e}")
        return False

def test_fastapi_server(port: int = 8081) -> bool:
    """Test FastAPI server"""
    print(f"🚀 Testing FastAPI server on port {port}...")
    
    # Create minimal FastAPI app
    fastapi_code = '''
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="TEST FastAPI")

@app.get("/test")
async def test():
    return {"message": "FastAPI is working!", "timestamp": time.time()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="info")
'''
    
    # Write FastAPI app to file
    fastapi_file = "test_fastapi.py"
    with open(fastapi_file, 'w') as f:
        f.write(fastapi_code)
    
    try:
        # Start FastAPI server
        process = subprocess.Popen(
            ["python3", fastapi_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test HTTP request
        try:
            import urllib.request
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/test", timeout=5)
            content = response.read()
            response.close()
            
            print(f"✅ FastAPI HTTP request successful: {content.decode()}")
            
            # Stop server
            process.terminate()
            process.wait()
            
            # Clean up
            Path(fastapi_file).unlink()
            return True
            
        except Exception as e:
            print(f"❌ FastAPI HTTP request failed: {e}")
            process.terminate()
            process.wait()
            Path(fastapi_file).unlink()
            return False
            
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        if Path(fastapi_file).exists():
            Path(fastapi_file).unlink()
        return False

def test_socket_connection(port: int) -> bool:
    """Test raw socket connection to port"""
    print(f"🔌 Testing socket connection to port {port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"✅ Socket connection successful to port {port}")
            return True
        else:
            print(f"❌ Socket connection failed to port {port}")
            return False
            
    except Exception as e:
        print(f"❌ Socket test error: {e}")
        return False

def test_curl_request(port: int, endpoint: str = "") -> bool:
    """Test HTTP request with curl"""
    print(f"🌐 Testing curl request to port {port}{endpoint}...")
    
    try:
        result = subprocess.run(
            f"curl -s -w 'HTTP_STATUS:%{{http_code}}' http://127.0.0.1:{port}{endpoint}",
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            output = result.stdout
            if 'HTTP_STATUS:' in output:
                response, status = output.split('HTTP_STATUS:')
                status = status.strip()
                response = response.strip()
                
                print(f"✅ Curl successful - Status: {status}, Length: {len(response)}")
                if response:
                    print(f"📄 Response preview: {response[:100]}{'...' if len(response) > 100 else ''}")
                return True
            else:
                print(f"✅ Curl successful - Length: {len(output)}")
                return True
        else:
            print(f"❌ Curl failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Curl test error: {e}")
        return False

def main():
    print("🔍 Starting FastAPI vs Working Server Test...")
    print("=" * 60)
    
    # Test 1: Working server (baseline)
    print("\n🧪 TEST 1: Working Server Baseline")
    working_works = test_working_server(8080)
    
    # Test 2: FastAPI server
    print("\n🧪 TEST 2: FastAPI Server")
    fastapi_works = test_fastapi_server(8081)
    
    # Test 3: Socket connections
    print("\n🧪 TEST 3: Socket Connections")
    working_socket = test_socket_connection(8080)
    fastapi_socket = test_socket_connection(8081)
    
    # Test 4: Curl requests
    print("\n🧪 TEST 4: Curl Requests")
    working_curl = test_curl_request(8080)
    fastapi_curl = test_curl_request(8081, "/test")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FastAPI vs Working Server Results:")
    
    print(f"✅ Working Server:")
    print(f"   - Server start: {'✅' if working_works else '❌'}")
    print(f"   - Socket connection: {'✅' if working_socket else '❌'}")
    print(f"   - HTTP request: {'✅' if working_curl else '❌'}")
    
    print(f"\n🚀 FastAPI Server:")
    print(f"   - Server start: {'✅' if fastapi_works else '❌'}")
    print(f"   - Socket connection: {'✅' if fastapi_socket else '❌'}")
    print(f"   - HTTP request: {'✅' if fastapi_curl else '❌'}")
    
    # Analysis
    print("\n🎯 Analysis:")
    if working_works and not fastapi_works:
        print("❌ FastAPI server fails to start - FastAPI/Uvicorn issue")
    elif working_socket and not fastapi_socket:
        print("❌ FastAPI server doesn't bind to port - binding issue")
    elif working_curl and not fastapi_curl:
        print("❌ FastAPI server doesn't respond to HTTP - response issue")
    elif working_works and fastapi_works:
        print("✅ Both servers work - issue resolved!")
    else:
        print("❌ Both servers fail - deeper system issue")
    
    print("\n🎯 FastAPI vs Working Server test complete!")

if __name__ == "__main__":
    main()




