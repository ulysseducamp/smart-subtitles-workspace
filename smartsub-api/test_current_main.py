#!/usr/bin/env python3
"""
Test Current Main - Test your actual main.py on port 3000
Tests if the port migration fixed the issue
"""

import time
import uvicorn
from main import app

def main():
    print("🚀 Testing CURRENT main.py on port 3000...")
    print("📝 This tests your actual application after port migration")
    
    print("✅ Imported app from main.py successfully")
    print("🌐 Starting server on http://127.0.0.1:3000...")
    print("📋 Test endpoints with:")
    print("   curl http://localhost:3000/")
    print("   curl http://localhost:3000/health")
    
    # Start server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=3000, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
