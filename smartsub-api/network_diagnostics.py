#!/usr/bin/env python3
"""
Network Diagnostics - Check actual port binding and network connectivity
Tests if ports are actually listening and accessible
"""

import socket
import subprocess
import time
import os
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

def check_port_listening(port: int) -> bool:
    """Check if a port is actually listening using netstat"""
    print(f"🔍 Checking if port {port} is listening...")
    
    # Check with netstat
    success, stdout, stderr = run_command(f"netstat -an | grep :{port}")
    if success and stdout.strip():
        print(f"✅ Port {port} found in netstat:")
        for line in stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        return True
    else:
        print(f"❌ Port {port} not found in netstat")
        if stderr:
            print(f"   Error: {stderr}")
        return False

def check_port_usage(port: int) -> bool:
    """Check what's using a port with lsof"""
    print(f"🔍 Checking what's using port {port}...")
    
    success, stdout, stderr = run_command(f"lsof -i :{port}")
    if success and stdout.strip():
        print(f"✅ Port {port} usage found:")
        for line in stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        return True
    else:
        print(f"❌ Nothing found using port {port}")
        if stderr:
            print(f"   Error: {stderr}")
        return False

def test_socket_connection(host: str, port: int, timeout: int = 5) -> bool:
    """Test raw socket connection to a port"""
    print(f"🔌 Testing socket connection to {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Socket connection successful to {host}:{port}")
            return True
        else:
            print(f"❌ Socket connection failed to {host}:{port} (error code: {result})")
            return False
            
    except socket.timeout:
        print(f"⏰ Socket connection timeout to {host}:{port}")
        return False
    except Exception as e:
        print(f"❌ Socket connection error to {host}:{port}: {e}")
        return False

def test_curl_connection(host: str, port: int, timeout: int = 10) -> bool:
    """Test HTTP connection with curl"""
    print(f"🌐 Testing HTTP connection to {host}:{port}...")
    
    url = f"http://{host}:{port}/health"
    success, stdout, stderr = run_command(f"curl -v --connect-timeout {timeout} {url}")
    
    if success:
        print(f"✅ HTTP connection successful to {url}")
        return True
    else:
        print(f"❌ HTTP connection failed to {url}")
        if stderr:
            print(f"   Error: {stderr}")
        return False

def test_netcat_connection(host: str, port: int, timeout: int = 5) -> bool:
    """Test raw TCP connection with netcat"""
    print(f"🔌 Testing TCP connection with netcat to {host}:{port}...")
    
    success, stdout, stderr = run_command(f"nc -zv -w {timeout} {host} {port}")
    
    if success:
        print(f"✅ Netcat connection successful to {host}:{port}")
        return True
    else:
        print(f"❌ Netcat connection failed to {host}:{port}")
        if stderr:
            print(f"   Error: {stderr}")
        return False

def check_network_interfaces() -> None:
    """Check network interface status"""
    print("\n🌐 Checking network interfaces...")
    
    success, stdout, stderr = run_command("ifconfig | grep -E 'inet |status'")
    if success:
        print("✅ Network interfaces:")
        for line in stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ Could not check network interfaces")
        if stderr:
            print(f"   Error: {stderr}")

def main():
    print("🔍 Starting Network Diagnostics...")
    print("=" * 60)
    
    # Test ports 3000, 3001, 3002 (updated from 8001-8003 due to blocking)
    test_ports = [3000, 3001, 3002]
    test_hosts = ["127.0.0.1", "localhost", "0.0.0.0"]
    
    # Check network interfaces
    check_network_interfaces()
    
    # Test each port
    for port in test_ports:
        print(f"\n{'='*20} PORT {port} {'='*20}")
        
        # Check if port is listening
        listening = check_port_listening(port)
        
        # Check what's using the port
        usage = check_port_usage(port)
        
        # Test different connection methods
        for host in test_hosts:
            print(f"\n--- Testing {host}:{port} ---")
            
            # Test socket connection
            socket_ok = test_socket_connection(host, port)
            
            # Test HTTP connection
            http_ok = test_curl_connection(host, port)
            
            # Test TCP connection
            tcp_ok = test_netcat_connection(host, port)
            
            # Summary for this host:port combination
            if socket_ok or http_ok or tcp_ok:
                print(f"✅ {host}:{port} - At least one connection method works")
            else:
                print(f"❌ {host}:{port} - All connection methods failed")
    
    print("\n" + "=" * 60)
    print("🎯 Network diagnostics complete!")
    print("Check above for any ports that are listening and accessible")

if __name__ == "__main__":
    main()
