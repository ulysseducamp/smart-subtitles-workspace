#!/usr/bin/env python3
"""
Import Test - Test each import individually with timing
Finds which module import causes the hang
"""

import time
import sys
import traceback

def test_import(module_name, import_statement):
    """Test importing a module and return timing info"""
    start_time = time.time()
    try:
        print(f"📦 Testing import: {module_name}")
        exec(import_statement)
        elapsed = time.time() - start_time
        print(f"✅ {module_name}: {elapsed:.3f}s")
        return True, elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ {module_name}: {elapsed:.3f}s - ERROR: {str(e)}")
        return False, elapsed

def main():
    print("🔍 Starting import diagnostics...")
    print("=" * 50)
    
    # Test basic Python imports
    print("\n🐍 Testing basic Python imports:")
    basic_imports = [
        ("os", "import os"),
        ("sys", "import sys"),
        ("time", "import time"),
        ("tempfile", "import tempfile"),
        ("subprocess", "import subprocess"),
    ]
    
    for name, stmt in basic_imports:
        test_import(name, stmt)
    
    # Test FastAPI ecosystem
    print("\n⚡ Testing FastAPI ecosystem:")
    fastapi_imports = [
        ("fastapi", "import fastapi"),
        ("uvicorn", "import uvicorn"),
        ("pydantic", "import pydantic"),
        ("python-multipart", "from fastapi import File, UploadFile"),
    ]
    
    for name, stmt in fastapi_imports:
        test_import(name, stmt)
    
    # Test custom modules from src/
    print("\n📁 Testing custom modules from src/:")
    try:
        test_import("deepl_client", "from src.deepl_client import *")
    except:
        print("⚠️  src.deepl_client not found or failed")
    
    try:
        test_import("fusion_algorithm", "from src.fusion_algorithm import *")
    except:
        print("⚠️  src.fusion_algorithm not found or failed")
    
    try:
        test_import("lemmatizer_service", "from src.lemmatizer_service import *")
    except:
        print("⚠️  src.lemmatizer_service not found or failed")
    
    try:
        test_import("supabase_client", "from src.supabase_client import *")
    except:
        print("⚠️  src.supabase_client not found or failed")
    
    # Test utils modules
    print("\n🔧 Testing utils modules:")
    try:
        test_import("srt_parser", "from utils.srt_parser import *")
    except:
        print("⚠️  utils.srt_parser not found or failed")
    
    try:
        test_import("vocabulary_analyzer", "from utils.vocabulary_analyzer import *")
    except:
        print("⚠️  utils.vocabulary_analyzer not found or failed")
    
    print("\n" + "=" * 50)
    print("🎯 Import diagnostics complete!")
    print("Check above for any imports that took too long or failed")

if __name__ == "__main__":
    main()
