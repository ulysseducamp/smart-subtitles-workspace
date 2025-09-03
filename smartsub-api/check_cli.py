#!/usr/bin/env python3
"""
CLI Integration Test
Tests CLI integration with timeouts and error handling
"""

import os
import time
import subprocess
from pathlib import Path
from typing import Optional, Tuple

def check_node_js() -> bool:
    """Check if Node.js is available"""
    print("🔍 Checking Node.js availability...")
    
    try:
        result = subprocess.run(
            ["node", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js available: {version}")
            return True
        else:
            print(f"❌ Node.js check failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Node.js version check timeout")
        return False
    except FileNotFoundError:
        print("❌ Node.js not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Node.js check error: {e}")
        return False

def find_cli_path() -> Optional[str]:
    """Find CLI executable path"""
    print("🔍 Finding CLI executable...")
    
    # Possible CLI paths
    possible_paths = [
        "../subtitles-fusion-algorithm-public/dist/main.js",
        "./subtitles-fusion-algorithm-public/dist/main.js",
        "/app/cli/dist/main.js",  # Original path that was wrong
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            print(f"✅ CLI found at: {path}")
            return path
    
    print("❌ CLI not found in expected locations")
    print("Searched in:")
    for path in possible_paths:
        print(f"  - {path}")
    
    return None

def test_cli_help(cli_path: str, timeout: int = 10) -> bool:
    """Test CLI help command with timeout"""
    print(f"🔄 Testing CLI help command...")
    
    try:
        result = subprocess.run(
            ["node", cli_path, "--help"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            print("✅ CLI help command successful!")
            help_output = result.stdout.strip()
            print(f"📖 Help output preview: {help_output[:100]}...")
            return True
        else:
            print(f"⚠️  CLI help failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ CLI help command timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"❌ CLI help command error: {e}")
        return False

def test_cli_version(cli_path: str, timeout: int = 10) -> bool:
    """Test CLI version command with timeout"""
    print(f"🏷️  Testing CLI version command...")
    
    try:
        result = subprocess.run(
            ["node", cli_path, "--version"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ CLI version: {version}")
            return True
        else:
            print(f"⚠️  CLI version command failed")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ CLI version command timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"❌ CLI version command error: {e}")
        return False

def main():
    print("🔍 Starting CLI integration diagnostics...")
    print("=" * 50)
    
    # Check Node.js
    print("\n🐍 Checking Node.js...")
    if not check_node_js():
        print("\n💥 Node.js is required but not available!")
        return
    
    # Find CLI path
    print("\n📁 Finding CLI executable...")
    cli_path = find_cli_path()
    
    if not cli_path:
        print("\n💥 CLI executable not found!")
        print("Please check the CLI path in your configuration")
        return
    
    # Test CLI functionality
    print(f"\n🚀 Testing CLI functionality...")
    start_time = time.time()
    
    help_success = test_cli_help(cli_path, timeout=10)
    version_success = test_cli_version(cli_path, timeout=10)
    
    elapsed = time.time() - start_time
    print(f"\n⏱️  CLI tests took: {elapsed:.3f}s")
    
    if help_success and version_success:
        print("\n🎉 CLI integration is working correctly!")
        print(f"CLI path: {cli_path}")
    else:
        print("\n⚠️  CLI integration has issues!")
        if not help_success:
            print("- Help command failed")
        if not version_success:
            print("- Version command failed")

if __name__ == "__main__":
    main()
