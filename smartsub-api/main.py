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

# Initialize frequency loader at startup
@app.on_event("startup")
async def startup_event():
    """Initialize frequency loader on application startup."""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from frequency_loader import initialize_frequency_loader
        
        # Initialize the global frequency loader
        frequency_loader = initialize_frequency_loader()
        logger.info("Frequency loader initialized successfully")
        
        # Log supported languages
        supported_langs = frequency_loader.get_supported_languages()
        logger.info(f"Supported languages: {supported_langs}")
        
    except Exception as e:
        logger.error(f"Failed to initialize frequency loader: {e}")
        # Don't fail startup, but log the error

# CORS middleware for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En V0, on accepte toutes les origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key validation middleware
@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    # Skip validation for health check endpoint
    if request.url.path == "/health":
        return await call_next(request)
    
    # Get API key from query parameters or headers
    api_key = request.query_params.get("api_key") or request.headers.get("x-api-key")
    
    # Get expected API key from environment
    expected_api_key = os.getenv("API_KEY")
    
    if not expected_api_key:
        # If no API key is configured, allow all requests (for development)
        return await call_next(request)
    
    if not api_key or api_key != expected_api_key:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or missing API key"}
        )
    
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

@app.get("/frequency-lists")
async def get_frequency_lists():
    """Get information about available frequency lists."""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from frequency_loader import get_frequency_loader
        
        frequency_loader = get_frequency_loader()
        supported_languages = frequency_loader.get_supported_languages()
        
        return {
            "supported_languages": supported_languages,
            "status": "available"
        }
    except Exception as e:
        logger.error(f"Error getting frequency lists info: {e}")
        return {"error": str(e), "status": "error"}


# Endpoint for subtitle fusion using Python engine
@app.post("/fuse-subtitles", response_model=SubtitleResponse)
async def fuse_subtitles(
    target_language: str = Form(...),
    native_language: str = Form(...),
    top_n_words: int = Form(2000),
    enable_inline_translation: bool = Form(True),
    deepl_api_key: Optional[str] = Form(None),
    target_srt: UploadFile = File(...),
    native_srt: UploadFile = File(...)
):
    import time
    start_time = time.time()
    logger.info(f"TIMING: Starting subtitle processing at {start_time}")
    
    try:
        # Import Python engine
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from subtitle_fusion import SubtitleFusionEngine
        from srt_parser import parse_srt, generate_srt
        from frequency_loader import get_frequency_loader
        
        # Read uploaded files
        file_read_time = time.time()
        target_content = await target_srt.read()
        native_content = await native_srt.read()
        logger.info(f"TIMING: File reading completed in {time.time() - file_read_time:.2f}s")
        
        # Parse SRT files
        parse_time = time.time()
        target_subs = parse_srt(target_content.decode('utf-8'))
        native_subs = parse_srt(native_content.decode('utf-8'))
        logger.info(f"TIMING: SRT parsing completed in {time.time() - parse_time:.2f}s")
        
        # Get frequency list from in-memory loader
        frequency_loader = get_frequency_loader()
        
        # Get top N words in frequency order (most frequent first)
        known_words = frequency_loader.get_top_n_words(target_language, top_n_words)
        
        # Log received parameters for debugging
        logger.info(f"Received parameters - enable_inline_translation: {enable_inline_translation}, target_lang: {target_language}, native_lang: {native_language}")
        
        # Initialize fusion engine
        engine = SubtitleFusionEngine()
        
        # Initialize DeepL API (always try if key available)
        deepl_api = None
        from deepl_api import DeepLAPI
        # Use API key from request or environment
        api_key = deepl_api_key or os.getenv("DEEPL_API_KEY")
        if api_key:
            deepl_api = DeepLAPI(api_key)
            logger.info("DeepL API initialized for inline translations")
        else:
            logger.warning("DeepL API key not provided, inline translation disabled")
        
        # Process fusion
        fusion_time = time.time()
        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang=target_language,
            enable_inline_translation=enable_inline_translation,
            deepl_api=deepl_api,
            native_lang=native_language
        )
        logger.info(f"TIMING: Subtitle fusion completed in {time.time() - fusion_time:.2f}s")
        
        # Generate output SRT
        generate_time = time.time()
        output_srt = generate_srt(result['hybrid'])
        logger.info(f"TIMING: SRT generation completed in {time.time() - generate_time:.2f}s")
        
        # Calculate total processing time
        total_time = time.time() - start_time
        logger.info(f"TIMING: Total processing time: {total_time:.2f}s")
        
        # Prepare stats
        stats = {
            "processing_time": f"{total_time:.2f}s",
            "words_processed": len(known_words),
            "frequency_list_size": len(known_words),
            "subtitles_processed": len(target_subs),
            "subtitles_replaced": result['replacedCount'],
            "replacement_rate": f"{(result['replacedCount'] / len(target_subs) * 100):.1f}%",
            "target_language": target_language,
            "native_language": native_language,
            "inline_translations": result.get('inlineTranslationCount', 0)
        }
        
        return SubtitleResponse(
            success=True,
            output_srt=output_srt,
            stats=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Changed from 8001 to 3000 due to port blocking
    uvicorn.run(app, host="0.0.0.0", port=port)
