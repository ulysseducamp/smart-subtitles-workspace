#!/usr/bin/env python3
"""
Framework Comparison - Test alternative web frameworks
Test Flask, built-in HTTP server, raw socket, and other ASGI servers
"""

import subprocess
import time
import socket
import threading
from pathlib import Path
from typing import Dict, List, Tuple

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

def test_builtin_http_server(port: int = 8080) -> bool:
    """Test Python's built-in HTTP server"""
    print(f"🐍 Testing built-in HTTP server on port {port}...")
    
    try:
        # Start server using Python module
        cmd = f"python3 -m http.server {port} --bind 127.0.0.1"
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Built-in HTTP server connection successful on port {port}")
                
                # Test HTTP request
                success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}")
                if success:
                    print(f"✅ HTTP request successful (length: {len(stdout)} chars)")
                    
                    # Stop server
                    process.terminate()
                    process.wait()
                    return True
                else:
                    print(f"⚠️  HTTP request failed: {stderr}")
                    process.terminate()
                    process.wait()
                    return False
            else:
                print(f"❌ Built-in HTTP server connection failed on port {port}")
                process.terminate()
                process.wait()
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            process.terminate()
            process.wait()
            return False
            
    except Exception as e:
        print(f"❌ Built-in HTTP server error: {e}")
        return False

def test_flask_app(port: int = 8081) -> bool:
    """Test Flask web framework"""
    print(f"🌿 Testing Flask on port {port}...")
    
    # Check if Flask is available
    success, stdout, stderr = run_command("python3 -c 'import flask'")
    if not success:
        print("❌ Flask not available - install with: pip install flask")
        return False
    
    print("✅ Flask is available")
    
    # Create minimal Flask app
    flask_code = '''
from flask import Flask
import time

app = Flask(__name__)

@app.route('/test')
def test():
    return {"message": "Flask is working!", "timestamp": time.time()}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=False)
'''
    
    # Write Flask app to file
    flask_file = "test_flask.py"
    with open(flask_file, 'w') as f:
        f.write(flask_code)
    
    try:
        # Start Flask server
        process = subprocess.Popen(
            ["python3", flask_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Flask connection successful on port {port}")
                
                # Test HTTP request
                success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/test")
                if success:
                    print(f"✅ Flask HTTP request successful: {stdout.strip()}")
                    
                    # Stop server
                    process.terminate()
                    process.wait()
                    
                    # Clean up
                    Path(flask_file).unlink()
                    return True
                else:
                    print(f"⚠️  Flask HTTP request failed: {stderr}")
                    process.terminate()
                    process.wait()
                    Path(flask_file).unlink()
                    return False
            else:
                print(f"❌ Flask connection failed on port {port}")
                process.terminate()
                process.wait()
                Path(flask_file).unlink()
                return False
                
        except Exception as e:
            print(f"❌ Flask connection test error: {e}")
            process.terminate()
            process.wait()
            Path(flask_file).unlink()
            return False
            
    except Exception as e:
        print(f"❌ Flask error: {e}")
        if Path(flask_file).exists():
            Path(flask_file).unlink()
        return False

def test_raw_socket_server(port: int = 8082) -> bool:
    """Test raw socket server"""
    print(f"🔌 Testing raw socket server on port {port}...")
    
    try:
        # Create and start socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(1)
        
        def socket_server():
            try:
                while True:
                    client, addr = server_socket.accept()
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSocket server working!"
                    client.send(response)
                    client.close()
            except:
                pass
        
        server_thread = threading.Thread(target=socket_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
        
        # Test connection
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect(('127.0.0.1', port))
            
            response = client_socket.recv(1024)
            client_socket.close()
            
            if response:
                print(f"✅ Raw socket server working on port {port}: {response.decode().strip()}")
                
                # Stop server
                server_socket.close()
                return True
            else:
                print(f"❌ Raw socket server no response on port {port}")
                server_socket.close()
                return False
                
        except Exception as e:
            print(f"❌ Raw socket server connection failed: {e}")
            server_socket.close()
            return False
            
    except Exception as e:
        print(f"❌ Raw socket server error: {e}")
        return False

def test_alternative_asgi_servers() -> Dict[str, bool]:
    """Test alternative ASGI servers"""
    print(f"\n🔄 Testing alternative ASGI servers...")
    
    servers = {
        "hypercorn": "pip install hypercorn",
        "daphne": "pip install daphne",
        "gunicorn": "pip install gunicorn[uvicorn]"
    }
    
    results = {}
    
    for server, install_cmd in servers.items():
        print(f"\n--- Testing {server} ---")
        
        # Check if server is available
        success, stdout, stderr = run_command(f"python3 -c 'import {server}'")
        
        if not success:
            print(f"❌ {server} not available - install with: {install_cmd}")
            results[server] = False
            continue
        
        print(f"✅ {server} is available")
        
        # Create minimal ASGI app
        asgi_code = '''
async def app(scope, receive, send):
    if scope["type"] == "http":
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"ASGI app working!",
        })
'''
        
        asgi_file = f"test_{server}.py"
        with open(asgi_file, 'w') as f:
            f.write(asgi_code)
        
        # Try to start server
        process = None
        try:
            if server == "hypercorn":
                cmd = f"hypercorn test_{server}:app --bind 127.0.0.1:8083"
            elif server == "daphne":
                cmd = f"daphne -b 127.0.0.1 -p 8083 test_{server}:app"
            elif server == "gunicorn":
                cmd = f"gunicorn test_{server}:app --bind 127.0.0.1:8083 --worker-class uvicorn.workers.UvicornWorker"
            else:
                cmd = f"{server} test_{server}:app --bind 127.0.0.1:8083"
            
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Test connection
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', 8083))
                sock.close()
                
                if result == 0:
                    print(f"✅ {server} connection successful")
                    
                    # Test HTTP request
                    success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:8083")
                    if success:
                        print(f"✅ {server} HTTP request successful: {stdout.strip()}")
                        results[server] = True
                    else:
                        print(f"⚠️  {server} HTTP request failed: {stderr}")
                        results[server] = False
                else:
                    print(f"❌ {server} connection failed")
                    results[server] = False
                    
            except Exception as e:
                print(f"❌ {server} connection test error: {e}")
                results[server] = False
                
        except Exception as e:
            print(f"❌ {server} server start error: {e}")
            results[server] = False
        finally:
            # Stop server if it was started
            if process:
                process.terminate()
                process.wait()
            
            # Clean up
            if Path(asgi_file).exists():
                Path(asgi_file).unlink()
    
    return results

def test_bottle_framework(port: int = 8084) -> bool:
    """Test Bottle web framework"""
    print(f"🍾 Testing Bottle on port {port}...")
    
    # Check if Bottle is available
    success, stdout, stderr = run_command("python3 -c 'import bottle'")
    if not success:
        print("❌ Bottle not available - install with: pip install bottle")
        return False
    
    print("✅ Bottle is available")
    
    # Create minimal Bottle app
    bottle_code = '''
from bottle import route, run
import time

@route('/test')
def test():
    return {"message": "Bottle is working!", "timestamp": time.time()}

if __name__ == '__main__':
    run(host='127.0.0.1', port=8084, debug=False)
'''
    
    # Write Bottle app to file
    bottle_file = "test_bottle.py"
    with open(bottle_file, 'w') as f:
        f.write(bottle_code)
    
    try:
        # Start Bottle server
        process = subprocess.Popen(
            ["python3", bottle_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Bottle connection successful on port {port}")
                
                # Test HTTP request
                success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/test")
                if success:
                    print(f"✅ Bottle HTTP request successful: {stdout.strip()}")
                    
                    # Stop server
                    process.terminate()
                    process.wait()
                    
                    # Clean up
                    Path(bottle_file).unlink()
                    return True
                else:
                    print(f"⚠️  Bottle HTTP request failed: {stderr}")
                    process.terminate()
                    process.wait()
                    Path(bottle_file).unlink()
                    return False
            else:
                print(f"❌ Bottle connection failed on port {port}")
                process.terminate()
                process.wait()
                Path(bottle_file).unlink()
                return False
                
        except Exception as e:
            print(f"❌ Bottle connection test error: {e}")
            process.terminate()
            process.wait()
            Path(bottle_file).unlink()
            return False
            
    except Exception as e:
        print(f"❌ Bottle error: {e}")
        if Path(bottle_file).exists():
            Path(bottle_file).unlink()
        return False

def main():
    print("🔍 Starting Framework Comparison Tests...")
    print("=" * 60)
    
    # Test built-in HTTP server
    builtin_works = test_builtin_http_server(8080)
    
    # Test Flask
    flask_works = test_flask_app(8081)
    
    # Test raw socket server
    socket_works = test_raw_socket_server(8082)
    
    # Test alternative ASGI servers
    asgi_results = test_alternative_asgi_servers()
    
    # Test Bottle
    bottle_works = test_bottle_framework(8084)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Framework Comparison Results:")
    
    print(f"🐍 Built-in HTTP server: {'✅' if builtin_works else '❌'}")
    print(f"🌿 Flask: {'✅' if flask_works else '❌'}")
    print(f"🔌 Raw socket server: {'✅' if socket_works else '❌'}")
    print(f"🍾 Bottle: {'✅' if bottle_works else '❌'}")
    
    print(f"\n🔄 Alternative ASGI servers:")
    for server, success in asgi_results.items():
        status = "✅" if success else "❌"
        print(f"   {server}: {status}")
    
    # Analysis
    print("\n🎯 Analysis:")
    working_frameworks = []
    if builtin_works: working_frameworks.append("Built-in HTTP")
    if flask_works: working_frameworks.append("Flask")
    if socket_works: working_frameworks.append("Raw Socket")
    if bottle_works: working_frameworks.append("Bottle")
    
    working_asgi = [server for server, success in asgi_results.items() if success]
    working_frameworks.extend(working_asgi)
    
    if working_frameworks:
        print(f"✅ Working frameworks: {', '.join(working_frameworks)}")
        print("💡 FastAPI issue is framework-specific, not system-wide")
    else:
        print("❌ No frameworks work - system-level networking issue")
        print("💡 Problem affects all Python web servers")
    
    print("\n🎯 Framework comparison complete!")

if __name__ == "__main__":
    main()
