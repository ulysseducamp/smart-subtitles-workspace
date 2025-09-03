#!/usr/bin/env python3
"""
FastAPI with Maximum Logging
Capture all uvicorn startup logs
Use --log-level debug
Show exactly what happens during startup
Document any exceptions with full tracebacks
"""

import uvicorn
import logging
from fastapi import FastAPI

# Configure maximum logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger for this script
logger = logging.getLogger(__name__)

# Create minimal app
app = FastAPI()

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "FastAPI with logging is working!"}

@app.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("=== STARTING FASTAPI WITH MAXIMUM LOGGING ===")
    logger.info("Port: 3000")
    logger.info("Host: 127.0.0.1")
    logger.info("Log level: DEBUG")
    logger.info("=" * 50)
    
    try:
        logger.info("Attempting to start uvicorn...")
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=3000, 
            log_level="debug",
            access_log=True
        )
    except Exception as e:
        logger.error(f"CRITICAL ERROR starting uvicorn: {e}")
        import traceback
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        
        # Also print to stdout for immediate visibility
        print(f"\n🚨 CRITICAL ERROR: {e}")
        print("Full traceback:")
        traceback.print_exc()

