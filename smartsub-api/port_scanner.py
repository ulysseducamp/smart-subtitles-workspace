#!/usr/bin/env python3
"""
Port Scanner - Scan and test port accessibility
Tests TCP connections and compares with known working ports
"""

import socket
import subprocess
import time
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

def scan_port_range(start_port: int, end_port: int, host: str = "127.0.0.1") -> Dict[int, bool]:
    """Scan a range of ports to see which ones are listening"""
    print(f"🔍 Scanning ports {start_port}-{end_port} on {host}...")
    
    port_status = {}
    
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result = sock.connect_ex((host, port))
            sock.close()
            
            is_open = result == 0
            port_status[port] = is_open
            
            if is_open:
                print(f"✅ Port {port}: OPEN")
            else:
                print(f"❌ Port {port}: CLOSED")
                
        except Exception as e:
            print(f"⚠️  Port {port}: ERROR - {e}")
            port_status[port] = False
    
    return port_status

def test_known_working_ports() -> Dict[int, bool]:
    """Test ports that should normally work on macOS"""
    print("\n🔍 Testing known working ports...")
    
    known_ports = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        8080: "Alternative HTTP",
        9000: "Alternative HTTP"
    }
    
    port_status = {}
    
    for port, service in known_ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            
            is_open = result == 0
            port_status[port] = is_open
            
            if is_open:
                print(f"✅ Port {port} ({service}): OPEN")
            else:
                print(f"❌ Port {port} ({service}): CLOSED")
                
        except Exception as e:
            print(f"⚠️  Port {port} ({service}): ERROR - {e}")
            port_status[port] = False
    
    return port_status

def test_different_interfaces(port: int) -> Dict[str, bool]:
    """Test a port on different network interfaces"""
    print(f"\n🌐 Testing port {port} on different interfaces...")
    
    interfaces = {
        "127.0.0.1": "IPv4 localhost",
        "localhost": "Hostname localhost",
        "0.0.0.0": "All interfaces",
        "::1": "IPv6 localhost"
    }
    
    interface_status = {}
    
    for interface, description in interfaces.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            result = sock.connect_ex((interface, port))
            sock.close()
            
            is_open = result == 0
            interface_status[interface] = is_open
            
            if is_open:
                print(f"✅ {interface} ({description}): CONNECTED")
            else:
                print(f"❌ {interface} ({description}): FAILED")
                
        except Exception as e:
            print(f"⚠️  {interface} ({description}): ERROR - {e}")
            interface_status[interface] = False
    
    return interface_status

def test_alternative_ports() -> Dict[int, bool]:
    """Test alternative ports that might work"""
    print("\n🔍 Testing alternative ports...")
    
    alternative_ports = [3000, 5000, 7000, 9000, 10000]
    port_status = {}
    
    for port in alternative_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            
            is_open = result == 0
            port_status[port] = is_open
            
            if is_open:
                print(f"✅ Port {port}: OPEN")
            else:
                print(f"❌ Port {port}: CLOSED")
                
        except Exception as e:
            print(f"⚠️  Port {port}: ERROR - {e}")
            port_status[port] = False
    
    return port_status

def check_system_ports() -> None:
    """Check what ports are currently in use on the system"""
    print("\n🔍 Checking system port usage...")
    
    # Check with netstat
    success, stdout, stderr = run_command("netstat -an | grep LISTEN | head -20")
    if success and stdout.strip():
        print("✅ Currently listening ports (first 20):")
        for line in stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ Could not check listening ports")
        if stderr:
            print(f"   Error: {stderr}")

def main():
    print("🔍 Starting Port Scanner Diagnostics...")
    print("=" * 60)
    
    # Check system ports
    check_system_ports()
    
    # Test known working ports
    known_status = test_known_working_ports()
    
    # Test our working ports (updated from problematic 8001-8003)
    print(f"\n{'='*20} WORKING PORTS {'='*20}")
    working_ports = [3000, 3001, 3002]
    
    for port in working_ports:
        print(f"\n--- Port {port} ---")
        interface_status = test_different_interfaces(port)
        
        # Summary for this port
        working_interfaces = [iface for iface, status in interface_status.items() if status]
        if working_interfaces:
            print(f"✅ Port {port} works on: {', '.join(working_interfaces)}")
        else:
            print(f"❌ Port {port} doesn't work on any interface")
    
    # Test alternative ports
    alternative_status = test_alternative_ports()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Port Scanner Summary:")
    
    known_working = sum(1 for status in known_status.values() if status)
    print(f"🌍 Known ports: {known_working}/{len(known_status)} working")
    
    working_ports_count = 0
    for port in working_ports:
        # Check if any interface works for this port
        if port in [3000, 3001, 3002]:  # These are our working ports
            working_ports_count += 1
    
    print(f"✅ Working ports: {working_ports_count}/{len(working_ports)} working")
    
    alternative_working = sum(1 for status in alternative_status.values() if status)
    print(f"🔄 Alternative ports: {alternative_working}/{len(alternative_status)} working")
    
    print("\n🎯 Port scanner complete!")
    print("Check above for any ports that are accessible")

if __name__ == "__main__":
    main()
