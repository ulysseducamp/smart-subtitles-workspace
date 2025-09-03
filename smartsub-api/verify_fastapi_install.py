#!/usr/bin/env python3
"""
FastAPI/Uvicorn Installation Verification
Test imports individually with try/catch
Show package versions
Test different installation methods if needed
"""

import sys
import subprocess

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def test_import(module_name):
    """Test importing a module"""
    try:
        __import__(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"

print("=== FASTAPI INSTALLATION VERIFICATION ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print("=" * 50)

# Test package versions
print("\n1. PACKAGE VERSIONS:")
print("-" * 20)
stdout, stderr, code = run_command("pip list | grep -E '(fastapi|uvicorn)'")
if code == 0:
    print("Installed packages:")
    print(stdout)
else:
    print(f"Error checking packages: {stderr}")
    print("Trying alternative method...")
    stdout, stderr, code = run_command("pip3 list | grep -E '(fastapi|uvicorn)'")
    if code == 0:
        print("Installed packages (pip3):")
        print(stdout)
    else:
        print(f"pip3 also failed: {stderr}")

# Test individual imports
print("\n2. IMPORT TESTS:")
print("-" * 20)

modules_to_test = [
    "fastapi",
    "uvicorn",
    "uvicorn.server",
    "fastapi.applications",
    "pydantic"
]

for module in modules_to_test:
    success, error = test_import(module)
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{module:20} {status}")
    if not success:
        print(f"           Error: {error}")

# Test uvicorn command
print("\n3. UVICORN COMMAND TEST:")
print("-" * 20)
stdout, stderr, code = run_command("uvicorn --version")
if code == 0:
    print(f"uvicorn command works: {stdout.strip()}")
else:
    print(f"uvicorn command failed: {stderr}")
    print("Trying uvicorn3...")
    stdout, stderr, code = run_command("uvicorn3 --version")
    if code == 0:
        print(f"uvicorn3 command works: {stdout.strip()}")
    else:
        print(f"uvicorn3 also failed: {stderr}")

# Test fastapi command
print("\n4. FASTAPI COMMAND TEST:")
print("-" * 20)
stdout, stderr, code = run_command("fastapi --version")
if code == 0:
    print(f"fastapi command works: {stdout.strip()}")
else:
    print(f"fastapi command failed: {stderr}")

print("\n" + "=" * 50)
print("VERIFICATION COMPLETE")

