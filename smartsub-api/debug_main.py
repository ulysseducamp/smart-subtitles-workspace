#!/usr/bin/env python3
"""
Debug Main - Minimal FastAPI test to isolate startup issues
Tests if basic FastAPI works without external dependencies
"""

import time
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def main():
    print("🚀 Starting FastAPI debug test...")
    
    # Create minimal FastAPI app
    print("📝 Creating FastAPI app...")
    app = FastAPI(
        title="Debug FastAPI Test",
        description="Minimal test to isolate startup issues",
        version="0.1.0"
    )
    
    # Add CORS middleware
    print("🔧 Adding CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Define minimal endpoints
    print("📍 Defining endpoints...")
    
    @app.get("/")
    async def root():
        return {
            "message": "Debug FastAPI is working!",
            "status": "healthy",
            "timestamp": time.time()
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "ok", 
            "service": "debug-fastapi",
            "timestamp": time.time()
        }
    
    print("✅ FastAPI app configured successfully")
    print("🌐 Starting server on http://127.0.0.1:3002...")
    
    # Start server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=3002, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
