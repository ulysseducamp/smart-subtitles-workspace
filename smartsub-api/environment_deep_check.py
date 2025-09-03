#!/usr/bin/env python3
"""
Environment Deep Check - Test Python installation integrity
Check for conflicting packages, versions, and environment issues
"""

import sys
import subprocess
import os
import platform
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

def check_python_installation() -> Dict[str, str]:
    """Check Python installation details"""
    print("🐍 Checking Python installation...")
    
    info = {}
    
    # Python version
    info['version'] = sys.version
    info['version_info'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Python executable
    info['executable'] = sys.executable
    info['executable_path'] = str(Path(sys.executable).resolve())
    
    # Platform info
    info['platform'] = platform.platform()
    info['machine'] = platform.machine()
    info['processor'] = platform.processor()
    
    # Python path
    info['python_path'] = sys.path
    
    print(f"✅ Python {info['version_info']} on {info['platform']}")
    print(f"📍 Executable: {info['executable_path']}")
    
    return info

def check_python_alternatives() -> List[str]:
    """Check for alternative Python installations"""
    print("\n🔍 Checking for alternative Python installations...")
    
    alternatives = []
    
    # Check common Python locations
    python_locations = [
        "/usr/bin/python3",
        "/usr/local/bin/python3",
        "/opt/homebrew/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3"
    ]
    
    for location in python_locations:
        if Path(location).exists():
            try:
                result = subprocess.run([location, "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"✅ Found: {location} - {version}")
                    alternatives.append(location)
                else:
                    print(f"⚠️  Found but broken: {location}")
            except Exception as e:
                print(f"❌ Error testing {location}: {e}")
        else:
            print(f"❌ Not found: {location}")
    
    return alternatives

def check_virtual_environment() -> Dict[str, str]:
    """Check virtual environment status"""
    print("\n🌍 Checking virtual environment...")
    
    env_info = {}
    
    # Check if we're in a virtual environment
    env_info['in_venv'] = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    env_info['venv_path'] = sys.prefix
    env_info['base_prefix'] = getattr(sys, 'base_prefix', 'N/A')
    
    if env_info['in_venv']:
        print(f"✅ In virtual environment: {env_info['venv_path']}")
        print(f"📍 Base Python: {env_info['base_prefix']}")
    else:
        print("❌ Not in virtual environment")
    
    # Check environment variables
    env_vars = ['VIRTUAL_ENV', 'PYTHONPATH', 'PATH']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:50]}{'...' if len(value) > 50 else ''}")
            env_info[var] = value
        else:
            print(f"❌ {var}: NOT SET")
            env_info[var] = None
    
    return env_info

def check_package_conflicts() -> Dict[str, bool]:
    """Check for package conflicts"""
    print("\n📦 Checking for package conflicts...")
    
    conflicts = {}
    
    # Check pip list for conflicts
    success, stdout, stderr = run_command("pip list")
    if success:
        print("✅ pip list successful")
        
        # Look for common conflict indicators
        lines = stdout.strip().split('\n')
        for line in lines:
            if 'WARNING' in line or 'ERROR' in line or 'conflict' in line.lower():
                print(f"⚠️  Potential conflict: {line}")
                conflicts['pip_warnings'] = True
        
        if not conflicts.get('pip_warnings'):
            print("✅ No pip warnings found")
            conflicts['pip_warnings'] = False
    else:
        print(f"❌ pip list failed: {stderr}")
        conflicts['pip_list_failed'] = True
    
    # Check for multiple versions of same package
    success, stdout, stderr = run_command("pip list | grep -E 'fastapi|uvicorn'")
    if success and stdout.strip():
        print("📋 FastAPI/Uvicorn packages:")
        for line in stdout.strip().split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    
    return conflicts

def test_fresh_environment() -> bool:
    """Test with completely fresh virtual environment"""
    print("\n🆕 Testing fresh virtual environment...")
    
    # Create new venv
    venv_name = "test_fresh_venv"
    print(f"📁 Creating {venv_name}...")
    
    success, stdout, stderr = run_command(f"python3 -m venv {venv_name}")
    if not success:
        print(f"❌ Failed to create venv: {stderr}")
        return False
    
    print("✅ Fresh venv created")
    
    # Activate and install minimal packages
    activate_cmd = f"source {venv_name}/bin/activate && pip install fastapi uvicorn"
    success, stdout, stderr = run_command(activate_cmd)
    
    if success:
        print("✅ FastAPI/Uvicorn installed in fresh venv")
        
        # Test minimal app
        test_code = '''
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test")
async def test():
    return {"message": "Fresh venv test"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
'''
        
        test_file = f"{venv_name}/test_app.py"
        with open(test_file, 'w') as f:
            f.write(test_code)
        
        print("✅ Test app created")
        
        # Clean up
        run_command(f"rm -rf {venv_name}")
        print("✅ Fresh venv cleaned up")
        
        return True
    else:
        print(f"❌ Failed to install packages: {stderr}")
        run_command(f"rm -rf {venv_name}")
        return False

def compare_python_installations() -> Dict[str, bool]:
    """Compare system Python vs venv Python"""
    print("\n🔍 Comparing Python installations...")
    
    results = {}
    
    # Test current Python
    print("📝 Testing current Python...")
    try:
        import fastapi
        import uvicorn
        print("✅ Current Python: FastAPI/Uvicorn import successfully")
        results['current_imports'] = True
    except ImportError as e:
        print(f"❌ Current Python: Import failed - {e}")
        results['current_imports'] = False
    
    # Test system Python (if different)
    if not os.getenv('VIRTUAL_ENV'):
        print("📝 Testing system Python...")
        success, stdout, stderr = run_command("python3 -c 'import fastapi; import uvicorn; print(\"System Python OK\")'")
        if success:
            print("✅ System Python: FastAPI/Uvicorn import successfully")
            results['system_imports'] = True
        else:
            print(f"❌ System Python: Import failed - {stderr}")
            results['system_imports'] = False
    
    return results

def main():
    print("🔍 Starting Environment Deep Check...")
    print("=" * 60)
    
    # Check Python installation
    python_info = check_python_installation()
    
    # Check alternatives
    alternatives = check_python_alternatives()
    
    # Check virtual environment
    venv_info = check_virtual_environment()
    
    # Check package conflicts
    conflicts = check_package_conflicts()
    
    # Test fresh environment
    fresh_works = test_fresh_environment()
    
    # Compare installations
    comparison = compare_python_installations()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Environment Deep Check Summary:")
    
    print(f"🐍 Python: {python_info['version_info']} on {python_info['platform']}")
    print(f"🌍 Virtual Environment: {'✅' if venv_info['in_venv'] else '❌'}")
    print(f"📦 Package Conflicts: {'❌' if conflicts.get('pip_warnings') else '✅'}")
    print(f"🆕 Fresh Environment: {'✅' if fresh_works else '❌'}")
    
    if alternatives:
        print(f"🔄 Alternative Pythons: {len(alternatives)} found")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not fresh_works:
        print("- Fresh environment creation failed - system issue")
    elif conflicts.get('pip_warnings'):
        print("- Package conflicts detected - resolve with pip")
    elif not venv_info['in_venv']:
        print("- Not in virtual environment - consider using one")
    else:
        print("- Environment appears healthy - issue elsewhere")
    
    print("\n🎯 Environment deep check complete!")

if __name__ == "__main__":
    main()




