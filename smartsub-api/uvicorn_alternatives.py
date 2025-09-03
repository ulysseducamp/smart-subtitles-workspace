#!/usr/bin/env python3
"""
Uvicorn Alternatives - Test FastAPI with different ASGI servers
Tests different uvicorn configurations and alternative servers
"""

import subprocess
import time
import socket
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

def test_uvicorn_different_hosts(port: int = 8004) -> Dict[str, bool]:
    """Test uvicorn with different host bindings"""
    print(f"🌐 Testing uvicorn with different host bindings on port {port}...")
    
    host_configs = {
        "127.0.0.1": "IPv4 localhost only",
        "0.0.0.0": "All interfaces",
        "localhost": "Hostname localhost"
    }
    
    results = {}
    
    for host, description in host_configs.items():
        print(f"\n--- Testing host: {host} ({description}) ---")
        
        try:
            # Start uvicorn with specific host
            cmd = f"uvicorn main:app --host {host} --port {port} --log-level error"
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
                    print(f"✅ Connection successful to {host}:{port}")
                    
                    # Test HTTP request
                    success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/health")
                    if success:
                        print(f"✅ HTTP request successful: {stdout.strip()}")
                        results[host] = True
                    else:
                        print(f"⚠️  HTTP request failed: {stderr}")
                        results[host] = False
                else:
                    print(f"❌ Connection failed to {host}:{port}")
                    results[host] = False
                    
            except Exception as e:
                print(f"❌ Connection test error: {e}")
                results[host] = False
            finally:
                # Stop server
                process.terminate()
                process.wait()
                
        except Exception as e:
            print(f"❌ Server start error: {e}")
            results[host] = False
    
    return results

def test_uvicorn_different_ports() -> Dict[int, bool]:
    """Test uvicorn on different ports"""
    print(f"\n🔌 Testing uvicorn on different ports...")
    
    test_ports = [3000, 5000, 7000, 9000, 10000]
    results = {}
    
    for port in test_ports:
        print(f"\n--- Testing port: {port} ---")
        
        try:
            # Start uvicorn on specific port
            cmd = f"uvicorn main:app --host 127.0.0.1 --port {port} --log-level error"
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
                    print(f"✅ Connection successful to port {port}")
                    
                    # Test HTTP request
                    success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/health")
                    if success:
                        print(f"✅ HTTP request successful: {stdout.strip()}")
                        results[port] = True
                    else:
                        print(f"⚠️  HTTP request failed: {stderr}")
                        results[port] = False
                else:
                    print(f"❌ Connection failed to port {port}")
                    results[port] = False
                    
            except Exception as e:
                print(f"❌ Connection test error: {e}")
                results[port] = False
            finally:
                # Stop server
                process.terminate()
                process.wait()
                
        except Exception as e:
            print(f"❌ Server start error: {e}")
            results[port] = False
    
    return results

def test_uvicorn_different_workers(port: int = 8005) -> Dict[str, bool]:
    """Test uvicorn with different worker configurations"""
    print(f"\n👥 Testing uvicorn with different worker configurations on port {port}...")
    
    worker_configs = {
        "1": "Single worker",
        "2": "Two workers",
        "4": "Four workers"
    }
    
    results = {}
    
    for workers, description in worker_configs.items():
        print(f"\n--- Testing workers: {workers} ({description}) ---")
        
        try:
            # Start uvicorn with specific workers
            cmd = f"uvicorn main:app --host 127.0.0.1 --port {port} --workers {workers} --log-level error"
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(5)  # More time for multiple workers
            
            # Test connection
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:
                    print(f"✅ Connection successful with {workers} workers")
                    
                    # Test HTTP request
                    success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:{port}/health")
                    if success:
                        print(f"✅ HTTP request successful: {stdout.strip()}")
                        results[workers] = True
                    else:
                        print(f"⚠️  HTTP request failed: {stderr}")
                        results[workers] = False
                else:
                    print(f"❌ Connection failed with {workers} workers")
                    results[workers] = False
                    
            except Exception as e:
                print(f"❌ Connection test error: {e}")
                results[workers] = False
            finally:
                # Stop server
                process.terminate()
                process.wait()
                
        except Exception as e:
            print(f"❌ Server start error: {e}")
            results[workers] = False
    
    return results

def test_alternative_asgi_servers() -> Dict[str, bool]:
    """Test alternative ASGI servers"""
    print(f"\n🔄 Testing alternative ASGI servers...")
    
    # Test if alternative servers are available
    servers = {
        "gunicorn": "pip install gunicorn[uvicorn]",
        "hypercorn": "pip install hypercorn",
        "daphne": "pip install daphne"
    }
    
    results = {}
    
    for server, install_cmd in servers.items():
        print(f"\n--- Testing {server} ---")
        
        # Check if server is available
        success, stdout, stderr = run_command(f"python3 -c 'import {server}'")
        
        if success:
            print(f"✅ {server} is available")
            
            # Try to start server
            try:
                if server == "gunicorn":
                    cmd = f"gunicorn main:app --bind 127.0.0.1:3006 --worker-class uvicorn.workers.UvicornWorker"
                elif server == "hypercorn":
                    cmd = f"hypercorn main:app --bind 127.0.0.1:3006"
                elif server == "daphne":
                    cmd = f"daphne -b 127.0.0.1 -p 3006 main:app"
                else:
                    cmd = f"{server} main:app --bind 127.0.0.1:3006"
                
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
                    result = sock.connect_ex(('127.0.0.1', 3006))
                    sock.close()
                    
                    if result == 0:
                        print(f"✅ {server} connection successful")
                        
                        # Test HTTP request
                        success, stdout, stderr = run_command(f"curl -s http://127.0.0.1:3006/health")
                        if success:
                            print(f"✅ HTTP request successful: {stdout.strip()}")
                            results[server] = True
                        else:
                            print(f"⚠️  HTTP request failed: {stderr}")
                            results[server] = False
                    else:
                        print(f"❌ {server} connection failed")
                        results[server] = False
                        
                except Exception as e:
                    print(f"❌ Connection test error: {e}")
                    results[server] = False
                finally:
                    # Stop server
                    process.terminate()
                    process.wait()
                    
            except Exception as e:
                print(f"❌ {server} start error: {e}")
                results[server] = False
        else:
            print(f"❌ {server} not available - install with: {install_cmd}")
            results[server] = False
    
    return results

def main():
    print("🔍 Starting Uvicorn Alternatives Tests...")
    print("=" * 60)
    
    # Test different host bindings
    host_results = test_uvicorn_different_hosts(3004)
    
    # Test different ports
    port_results = test_uvicorn_different_ports()
    
    # Test different worker configurations
    worker_results = test_uvicorn_different_workers(3005)
    
    # Test alternative ASGI servers
    server_results = test_alternative_asgi_servers()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Uvicorn Alternatives Test Summary:")
    
    print(f"\n🌐 Host binding results:")
    for host, success in host_results.items():
        status = "✅" if success else "❌"
        print(f"   {host}: {status}")
    
    print(f"\n🔌 Port results:")
    working_ports = [port for port, success in port_results.items() if success]
    if working_ports:
        print(f"   Working ports: {', '.join(map(str, working_ports))}")
    else:
        print("   No working ports found")
    
    print(f"\n👥 Worker configuration results:")
    for workers, success in worker_results.items():
        status = "✅" if success else "❌"
        print(f"   {workers} workers: {status}")
    
    print(f"\n🔄 Alternative ASGI server results:")
    for server, success in server_results.items():
        status = "✅" if success else "❌"
        print(f"   {server}: {status}")
    
    # Analysis
    print("\n🎯 Analysis:")
    if any(host_results.values()):
        print("✅ Some host bindings work - issue might be specific to certain configurations")
    else:
        print("❌ No host bindings work - fundamental uvicorn issue")
    
    if working_ports:
        print(f"✅ Some ports work - issue might be port-specific")
    else:
        print("❌ No ports work - system-level issue")
    
    if any(server_results.values()):
        print("✅ Alternative ASGI servers work - issue specific to uvicorn")
    else:
        print("❌ No alternative ASGI servers work - broader system issue")
    
    print("\n🎯 Uvicorn alternatives tests complete!")

if __name__ == "__main__":
    main()
