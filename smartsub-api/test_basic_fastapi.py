#!/usr/bin/env python3
"""
ABSOLUTE MINIMAL FastAPI Test
Single file, minimal dependencies
Capture ALL output (stdout, stderr)
Show exact error messages if any
"""

import uvicorn
from fastapi import FastAPI

# Create minimal app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI is working!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("=== STARTING MINIMAL FASTAPI TEST ===")
    print("Port: 3000")
    print("Host: 127.0.0.1")
    print("=" * 40)
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=3000, 
            log_level="info"
        )
    except Exception as e:
        print(f"ERROR starting uvicorn: {e}")
        import traceback
        traceback.print_exc()

