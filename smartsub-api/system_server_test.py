#!/usr/bin/env python3
"""
System Server Test - Test other Python web servers for comparison
Tests if the issue is specific to Uvicorn/FastAPI
"""

import socket
import subprocess
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Tuple

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler for testing"""
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = '{"status": "ok", "service": "simple-http"}'
            self.wfile.write(response.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = '<html><body><h1>Simple HTTP Server Working!</h1></body></html>'
            self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        # Suppress logging for cleaner output
        pass

def run_command(cmd: str, timeout: int = 10) -> Tuple[bool, str, str]:
    """Run a shell command and return success, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Command timeout after {timeout}s"
    except Exception as e:
        return False, "", str(e)

def test_simple_http_server(port: int = 9000) -> bool:
    """Test a simple Python HTTP server"""
    print(f"🌐 Testing simple HTTP server on port {port}...")
    
    try:
        # Start server in background thread
        server = HTTPServer(('127.0.0.1', port), SimpleHTTPHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Test connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Simple HTTP server started successfully on port {port}")
                
                # Test HTTP request
                success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/health")
                if success:
                    print(f"✅ HTTP request successful: {stdout.strip()}")
                else:
                    print(f"⚠️  HTTP request failed: {stderr}")
                
                # Stop server
                server.shutdown()
                server.server_close()
                return True
            else:
                print(f"❌ Simple HTTP server failed to start on port {port}")
                server.shutdown()
                server.server_close()
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            server.shutdown()
            server.server_close()
            return False
            
    except Exception as e:
        print(f"❌ Simple HTTP server error: {e}")
        return False

def test_socket_server(port: int = 9001) -> bool:
    """Test a simple socket server"""
    print(f"🔌 Testing socket server on port {port}...")
    
    try:
        # Start server in background thread
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(1)
        
        def socket_server():
            try:
                while True:
                    client, addr = server_socket.accept()
                    client.send(b"Socket server working!\n")
                    client.close()
            except:
                pass
        
        server_thread = threading.Thread(target=socket_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Test connection
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect(('127.0.0.1', port))
            
            response = client_socket.recv(1024)
            client_socket.close()
            
            if response:
                print(f"✅ Socket server working on port {port}: {response.decode().strip()}")
                
                # Stop server
                server_socket.close()
                return True
            else:
                print(f"❌ Socket server no response on port {port}")
                server_socket.close()
                return False
                
        except Exception as e:
            print(f"❌ Socket server connection failed: {e}")
            server_socket.close()
            return False
            
    except Exception as e:
        print(f"❌ Socket server error: {e}")
        return False

def test_python_http_server_module(port: int = 9002) -> bool:
    """Test Python's built-in HTTP server module"""
    print(f"🐍 Testing Python HTTP server module on port {port}...")
    
    try:
        # Start server using Python module
        cmd = f"python3 -m http.server {port} --bind 127.0.0.1"
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Python HTTP server module working on port {port}")
                
                # Test HTTP request
                success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}")
                if success:
                    print(f"✅ HTTP request successful (length: {len(stdout)} chars)")
                else:
                    print(f"⚠️  HTTP request failed: {stderr}")
                
                # Stop server
                process.terminate()
                process.wait()
                return True
            else:
                print(f"❌ Python HTTP server module failed on port {port}")
                process.terminate()
                process.wait()
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            process.terminate()
            process.wait()
            return False
            
    except Exception as e:
        print(f"❌ Python HTTP server module error: {e}")
        return False

def test_different_bindings() -> Dict[str, bool]:
    """Test different binding approaches"""
    print("\n🌐 Testing different binding approaches...")
    
    bindings = {
        "127.0.0.1": "IPv4 localhost only",
        "0.0.0.0": "All interfaces",
        "localhost": "Hostname localhost"
    }
    
    binding_results = {}
    
    for binding, description in bindings.items():
        print(f"\n--- Testing binding: {binding} ---")
        
        try:
            # Test with simple socket server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                server_socket.bind((binding, 9003))
                server_socket.listen(1)
                
                print(f"✅ Binding successful to {binding}:9003")
                
                # Test connection
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5)
                client_socket.connect(('127.0.0.1', 9003))
                client_socket.close()
                
                print(f"✅ Connection successful to {binding}:9003")
                binding_results[binding] = True
                
            except Exception as e:
                print(f"❌ Binding failed to {binding}:9003: {e}")
                binding_results[binding] = False
            finally:
                server_socket.close()
                
        except Exception as e:
            print(f"❌ Test failed for {binding}: {e}")
            binding_results[binding] = False
    
    return binding_results

def main():
    print("🔍 Starting System Server Tests...")
    print("=" * 60)
    
    # Test simple HTTP server
    http_success = test_simple_http_server(9000)
    
    # Test socket server
    socket_success = test_socket_server(9001)
    
    # Test Python HTTP server module
    module_success = test_python_http_server_module(9002)
    
    # Test different bindings
    binding_results = test_different_bindings()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 System Server Test Summary:")
    
    print(f"🌐 Simple HTTP server: {'✅' if http_success else '❌'}")
    print(f"🔌 Socket server: {'✅' if socket_success else '❌'}")
    print(f"🐍 Python HTTP module: {'✅' if module_success else '❌'}")
    
    print("\n🌐 Binding test results:")
    for binding, success in binding_results.items():
        status = "✅" if success else "❌"
        print(f"   {binding}: {status}")
    
    # Analysis
    print("\n🎯 Analysis:")
    if http_success and socket_success and module_success:
        print("✅ All basic Python servers work - issue is specific to FastAPI/Uvicorn")
    elif not http_success and not socket_success and not module_success:
        print("❌ No Python servers work - system-level networking issue")
    else:
        print("⚠️  Mixed results - some servers work, others don't")
    
    print("\n🎯 System server tests complete!")

if __name__ == "__main__":
    main()
