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
import httpx
from collections import defaultdict
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File size validation configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))  # 5MB default
ALLOWED_EXTENSIONS = {".srt"}

# Simple rate limiter
rate_limit_storage = defaultdict(list)
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60  # seconds

def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit."""
    now = datetime.now()
    # Clean old requests
    rate_limit_storage[client_ip] = [
        req_time for req_time in rate_limit_storage[client_ip]
        if now - req_time < timedelta(seconds=RATE_LIMIT_WINDOW)
    ]
    
    # Check if limit exceeded
    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    
    # Add current request
    rate_limit_storage[client_ip].append(now)
    return True

def validate_file_size(file: UploadFile, file_type: str) -> None:
    """Validate file size and type."""
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"{file_type} file too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )
    
    # Validate file extension
    if file.filename:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Only {', '.join(ALLOWED_EXTENSIONS)} files allowed"
            )

app = FastAPI(
    title="Smart Netflix Subtitles API",
    description="FastAPI backend for bilingual adaptive subtitles with rate limiting",
    version="0.1.1"
)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Only apply rate limiting to /fuse-subtitles endpoint
    if request.url.path == "/fuse-subtitles" and request.method == "POST":
        client_ip = request.client.host
        if not check_rate_limit(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Maximum 10 requests per minute."}
            )
    
    response = await call_next(request)
    return response

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
    # Skip validation for health check and proxy endpoints
    if request.url.path in ["/health", "/proxy-railway"]:
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
    request: Request,
    target_language: str = Form(...),
    native_language: str = Form(...),
    top_n_words: int = Form(2000),
    enable_inline_translation: bool = Form(True),
    deepl_api_key: Optional[str] = Form(None),
    target_srt: UploadFile = File(...),
    native_srt: UploadFile = File(...)
):
    try:
        # Import Python engine
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from subtitle_fusion import SubtitleFusionEngine
        from srt_parser import parse_srt, generate_srt
        from frequency_loader import get_frequency_loader
        
        # SECURITY: Validate file sizes
        validate_file_size(target_srt, "Target SRT")
        validate_file_size(native_srt, "Native SRT")
        
        # Read uploaded files
        target_content = await target_srt.read()
        native_content = await native_srt.read()
        
        # Parse SRT files
        target_subs = parse_srt(target_content.decode('utf-8'))
        native_subs = parse_srt(native_content.decode('utf-8'))
        
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
        
        # Process fusion with timing
        import time
        start_time = time.time()
        
        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang=target_language,
            enable_inline_translation=enable_inline_translation,
            deepl_api=deepl_api,
            native_lang=native_language
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Subtitle processing completed in {processing_time:.2f} seconds")
        
        # Generate output SRT
        output_srt = generate_srt(result['hybrid'])
        
        # Log detailed statistics AFTER all subtitle processing logs are complete
        logger.info("=== SUBTITLE PROCESSING STATISTICS ===")
        logger.info(f"Total target subtitles: {len(target_subs)}")
        logger.info(f"Total native subtitles: {len(native_subs)}")
        
        # Calculate kept subtitles (total - replaced)
        kept_subtitles = len(target_subs) - result['replacedCount']
        logger.info(f"Subtitles kept in target language: {kept_subtitles}/{len(target_subs)}")
        
        # Calculate percentages
        percent_kept = (kept_subtitles / len(target_subs) * 100) if len(target_subs) > 0 else 0
        percent_replaced = (result['replacedCount'] / len(target_subs) * 100) if len(target_subs) > 0 else 0
        percent_inline = (result['inlineTranslationCount'] / len(target_subs) * 100) if len(target_subs) > 0 else 0
        percent_inline_vs_kept = (result['inlineTranslationCount'] / kept_subtitles * 100) if kept_subtitles > 0 else 0
        
        logger.info(f"Subtitles replaced with native: {result['replacedCount']}/{len(target_subs)} ({percent_replaced:.1f}%)")
        logger.info(f"Subtitles with inline translation: {result['inlineTranslationCount']}/{len(target_subs)} ({percent_inline:.1f}%)")
        logger.info(f"Subs with inline translation vs kept in target language: {result['inlineTranslationCount']}/{kept_subtitles} ({percent_inline_vs_kept:.1f}%)")
        logger.info("—")
        
        # DeepL statistics
        if enable_inline_translation and deepl_api:
            logger.info(f"Number of translation errors: {result['errorCount']}")
            deepl_stats = deepl_api.get_stats()
            logger.info(f"DeepL API requests made: {deepl_stats['requestCount']}")
            logger.info(f"Translation cache size: {deepl_stats['cacheSize']}")
            logger.info("—")
        
        # Translated words statistics
        translated_words = result.get('translatedWords', {})
        if translated_words:
            # Get words translated multiple times
            multiple_translated_words = [
                f"{word} (translated {count} times)" 
                for word, count in translated_words.items() 
                if count > 1
            ]
            
            if multiple_translated_words:
                logger.info(f"Same word translated several times: {', '.join(multiple_translated_words)}")
                logger.info("—")
            
            # Get unique words translated
            unique_words_translated = len(translated_words)
            unique_words_list = sorted(translated_words.keys())
            
            logger.info(f"Number of new words translated: {unique_words_translated}")
            logger.info(f"New words: {', '.join(unique_words_list)}")
            logger.info("—")
        
        # Processing time
        logger.info(f"Operation duration: {processing_time:.2f} seconds")
        
        # Prepare stats
        stats = {
            "processing_time": "calculated_from_python_engine",
            "words_processed": len(known_words),
            "frequency_list_size": len(known_words),
            "subtitles_processed": len(target_subs),
            "subtitles_replaced": result['replacedCount'],
            "replacement_rate": f"{(result['replacedCount'] / len(target_subs) * 100):.1f}%",
            "target_language": target_language,
            "native_language": native_language
        }
        
        return SubtitleResponse(
            success=True,
            output_srt=output_srt,
            stats=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Proxy endpoint for Chrome extension to securely access Railway API
@app.post("/proxy-railway")
async def proxy_railway(request: Request):
    """
    Proxy endpoint that receives requests from Chrome extension and forwards them
    to the Railway API with the API key securely stored on the server.
    """
    try:
        # Get the request body
        body = await request.body()
        
        # Get the Railway API key from environment
        railway_api_key = os.getenv("RAILWAY_API_KEY")
        if not railway_api_key:
            raise HTTPException(
                status_code=500, 
                detail="Railway API key not configured on server"
            )
        
        # Get the target URL from query parameters or use default
        target_url = request.query_params.get("url", "https://smartsub-api-production.up.railway.app/fuse-subtitles")
        
        # Add the API key to the target URL
        separator = "&" if "?" in target_url else "?"
        target_url_with_key = f"{target_url}{separator}api_key={railway_api_key}"
        
        # Forward the request to Railway API
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                target_url_with_key,
                content=body,
                headers={
                    "Content-Type": request.headers.get("content-type", "application/json"),
                    "User-Agent": "SmartSubtitles-Proxy/1.0"
                }
            )
            
            # Return the response from Railway API
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
                status_code=response.status_code
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout to Railway API")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to Railway API: {str(e)}")
    except Exception as e:
        logger.error(f"Proxy error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal proxy error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Changed from 8001 to 3000 due to port blocking
    uvicorn.run(app, host="0.0.0.0", port=port)
