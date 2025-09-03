#!/usr/bin/env python3
"""
Verify Working FastAPI - Guaranteed minimal FastAPI app
Tests if FastAPI actually works on port 3000, not just port binding
"""

import time
import uvicorn
from fastapi import FastAPI

def main():
    print("🚀 Starting VERIFICATION FastAPI app...")
    print("📝 This is a guaranteed-working minimal FastAPI app")
    
    # Create absolute minimal FastAPI app
    print("📝 Creating minimal FastAPI app...")
    app = FastAPI(
        title="VERIFICATION FastAPI",
        description="Minimal app to verify FastAPI works on port 3000",
        version="0.1.0"
    )
    
    # Single endpoint only
    print("📍 Defining single test endpoint...")
    
    @app.get("/test")
    async def test_endpoint():
        print("✅ /test endpoint called - responding!")
        return {
            "message": "VERIFICATION FastAPI is working!",
            "timestamp": time.time(),
            "status": "success"
        }
    
    print("✅ FastAPI app configured successfully")
    print("🌐 Starting server on http://127.0.0.1:3000...")
    print("📋 Test with: curl http://localhost:3000/test")
    
    # Start server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=3000, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
