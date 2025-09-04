from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Netflix Subtitles API",
    description="FastAPI backend for bilingual adaptive subtitles",
    version="0.1.0"
)

# CORS middleware for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En V0, on accepte toutes les origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment at startup
API_KEY = os.getenv("API_KEY")

# Debug environment variables at startup
logger.info("=== STARTUP DEBUG INFO ===")
logger.info(f"RAILWAY_ENVIRONMENT_NAME: {os.getenv('RAILWAY_ENVIRONMENT_NAME', 'NOT_SET')}")
logger.info(f"RAILWAY_PROJECT_ID: {os.getenv('RAILWAY_PROJECT_ID', 'NOT_SET')}")
logger.info(f"API_KEY configured: {bool(API_KEY)}")
if API_KEY:
    logger.info(f"API_KEY length: {len(API_KEY)}")
    logger.info(f"API_KEY first 10 chars: {API_KEY[:10]}...")
else:
    logger.warning("API_KEY is None or empty!")
logger.info("=== END STARTUP DEBUG ===")

# API Key validation middleware
@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    # Skip validation for health check and debug endpoints
    if request.url.path in ["/health", "/debug-env"]:
        return await call_next(request)
    
    # Get API key from query parameters or headers
    api_key_from_request = request.query_params.get("api_key") or request.headers.get("x-api-key")
    
    # Debug each request
    logger.info(f"=== REQUEST DEBUG: {request.url.path} ===")
    logger.info(f"API_KEY from env: {bool(API_KEY)}")
    logger.info(f"API_KEY from request: {bool(api_key_from_request)}")
    if api_key_from_request:
        logger.info(f"Request API key length: {len(api_key_from_request)}")
        logger.info(f"Request API key first 10 chars: {api_key_from_request[:10]}...")
    
    if not API_KEY:
        logger.error("API_KEY not configured in environment!")
        return JSONResponse(
            status_code=500,
            content={"error": "Server API key not configured"}
        )
    
    if not api_key_from_request:
        logger.warning("No API key provided in request")
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or missing API key"}
        )
    
    # Compare API keys
    if api_key_from_request != API_KEY:
        logger.error(f"API key mismatch! Expected length: {len(API_KEY)}, Got length: {len(api_key_from_request)}")
        logger.error(f"Expected starts with: {API_KEY[:10]}..., Got starts with: {api_key_from_request[:10]}...")
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or missing API key"}
        )
    
    logger.info("API key validation successful")
    return await call_next(request)

# Pydantic models for API data validation
class SubtitleRequest(BaseModel):
    target_language: str  # ex: "fr", "en"
    native_language: str  # ex: "en", "fr"
    top_n_words: int = 2000  # niveau vocabulaire
    enable_inline_translation: bool = False
    deepl_api_key: Optional[str] = None

class SubtitleResponse(BaseModel):
    success: bool
    output_srt: str  # contenu du fichier SRT hybride
    stats: dict  # statistiques de traitement
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Smart Netflix Subtitles API is running!",
        "status": "healthy",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "smartsub-api"}

@app.get("/debug-env")
async def debug_environment():
    """Debug endpoint to check environment variables - REMOVE AFTER DEBUGGING"""
    return {
        "api_key_configured": bool(API_KEY),
        "api_key_length": len(API_KEY) if API_KEY else 0,
        "railway_environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "NOT_SET"),
        "railway_project_id": os.getenv("RAILWAY_PROJECT_ID", "NOT_SET"),
        "port": os.getenv("PORT", "NOT_SET"),
        "python_version": os.getenv("PYTHON_VERSION", "NOT_SET")
    }

# Endpoint for subtitle fusion using CLI wrapper
@app.post("/fuse-subtitles", response_model=SubtitleResponse)
async def fuse_subtitles(
    target_language: str = Form(...),
    native_language: str = Form(...),
    top_n_words: int = Form(2000),
    enable_inline_translation: bool = Form(False),
    deepl_api_key: Optional[str] = Form(None),
    target_srt: UploadFile = File(...),
    native_srt: UploadFile = File(...),
    frequency_list: UploadFile = File(...)
):
    try:
        # Create temporary files for CLI processing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_target, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_native, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_freq, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_output:
            
            # Write uploaded files to temp files
            temp_target.write(target_srt.file.read().decode())
            temp_native.write(native_srt.file.read().decode())
            temp_freq.write(frequency_list.file.read().decode())
            
            # Close files to ensure writing is complete
            temp_target.close()
            temp_native.close()
            temp_freq.close()
            temp_output.close()
            
            # Build CLI command
            cmd = [
                "node", 
                "../subtitles-fusion-algorithm-public/dist/main.js",  # Fixed path to CLI
                "--target", temp_target.name,
                "--native", temp_native.name,
                "--freq", temp_freq.name,
                "--out", temp_output.name,
                "--topN", str(top_n_words),
                "--lang", target_language,
                "--native-lang", native_language
            ]
            
            if enable_inline_translation:
                cmd.append("--inline-translation")
                if deepl_api_key:
                    cmd.extend(["--deepl-key", deepl_api_key])
            
            # Execute CLI
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"CLI processing failed: {result.stderr}"
                )
            
            # Read output and return
            with open(temp_output.name, 'r') as f:
                output_srt = f.read()
            
            # Parse CLI output for stats (you can enhance this)
            stats = {
                "processing_time": "calculated_from_cli_output",
                "words_processed": "extracted_from_cli_output"
            }
            
            return SubtitleResponse(
                success=True,
                output_srt=output_srt,
                stats=stats
            )
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Processing timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files
        for temp_file in [temp_target.name, temp_native.name, temp_freq.name, temp_output.name]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Changed from 8001 to 3000 due to port blocking
    uvicorn.run(app, host="0.0.0.0", port=port)
