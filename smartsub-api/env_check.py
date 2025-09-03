#!/usr/bin/env python3
"""
Environment Check
Checks all environment variables and paths systematically
"""

import os
import sys
from pathlib import Path
from typing import Dict, List

def check_env_vars() -> Dict[str, str]:
    """Check all expected environment variables"""
    print("🌍 Checking environment variables...")
    
    expected_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY", 
        "DEEPL_API_KEY",
        "PORT",
        "PYTHONPATH",
        "PATH"
    ]
    
    env_status = {}
    
    for var in expected_vars:
        value = os.getenv(var)
        if value:
            # Truncate long values for display
            display_value = value[:30] + "..." if len(value) > 30 else value
            print(f"✅ {var}: {display_value}")
            env_status[var] = value
        else:
            print(f"❌ {var}: NOT SET")
            env_status[var] = None
    
    return env_status

def check_paths() -> Dict[str, bool]:
    """Check important file paths"""
    print("\n📁 Checking important paths...")
    
    paths_to_check = [
        ("Current working directory", "."),
        ("Python executable", sys.executable),
        ("Python version", f"{sys.version_info.major}.{sys.version_info.minor}"),
        ("CLI directory", "../subtitles-fusion-algorithm-public/dist/"),
        ("Source directory", "./src/"),
        ("Utils directory", "./utils/"),
    ]
    
    path_status = {}
    
    for name, path in paths_to_check:
        if Path(path).exists():
            print(f"✅ {name}: {path}")
            path_status[name] = True
        else:
            print(f"❌ {name}: {path} (NOT FOUND)")
            path_status[name] = False
    
    return path_status

def check_python_modules() -> Dict[str, bool]:
    """Check Python module availability"""
    print("\n🐍 Checking Python module availability...")
    
    modules_to_check = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "httpx",
        "supabase",
        "simplemma"
    ]
    
    module_status = {}
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
            module_status[module] = True
        except ImportError:
            print(f"❌ {module}: NOT AVAILABLE")
            module_status[module] = False
        except Exception as e:
            print(f"⚠️  {module}: ERROR - {e}")
            module_status[module] = False
    
    return module_status

def check_file_permissions() -> Dict[str, bool]:
    """Check file permissions"""
    print("\n🔐 Checking file permissions...")
    
    files_to_check = [
        ("main.py", "./main.py"),
        ("CLI executable", "../subtitles-fusion-algorithm-public/dist/main.js"),
    ]
    
    permission_status = {}
    
    for name, file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            try:
                # Check if readable
                with open(path, 'r') as f:
                    f.read(1)
                print(f"✅ {name}: Readable")
                permission_status[name] = True
            except PermissionError:
                print(f"❌ {name}: Permission denied")
                permission_status[name] = False
            except Exception as e:
                print(f"⚠️  {name}: Error - {e}")
                permission_status[name] = False
        else:
            print(f"❌ {name}: File not found")
            permission_status[name] = False
    
    return permission_status

def main():
    print("🔍 Starting environment diagnostics...")
    print("=" * 50)
    
    # Check environment variables
    env_status = check_env_vars()
    
    # Check paths
    path_status = check_paths()
    
    # Check Python modules
    module_status = check_python_modules()
    
    # Check file permissions
    permission_status = check_file_permissions()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Environment Summary:")
    
    env_ok = sum(1 for v in env_status.values() if v is not None)
    env_total = len(env_status)
    print(f"🌍 Environment variables: {env_ok}/{env_total} set")
    
    path_ok = sum(1 for v in path_status.values() if v)
    path_total = len(path_status)
    print(f"📁 Paths: {path_ok}/{path_total} found")
    
    module_ok = sum(1 for v in module_status.values() if v)
    module_total = len(module_status)
    print(f"🐍 Python modules: {module_ok}/{module_total} available")
    
    perm_ok = sum(1 for v in permission_status.values() if v)
    perm_total = len(permission_status)
    print(f"🔐 File permissions: {perm_ok}/{perm_total} OK")
    
    print("\n🎯 Environment check complete!")
    
    # Recommendations
    if env_ok < env_total:
        print("💡 Consider setting missing environment variables")
    if path_ok < path_total:
        print("💡 Check file paths and directory structure")
    if module_ok < module_total:
        print("💡 Install missing Python packages")
    if perm_ok < perm_total:
        print("💡 Check file permissions and ownership")

if __name__ == "__main__":
    main()
