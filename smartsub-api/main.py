from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import uvicorn
import os

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


# Endpoint for subtitle fusion using Python engine
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
        # Import Python engine
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from subtitle_fusion import SubtitleFusionEngine
        from srt_parser import parse_srt, generate_srt
        
        # Read uploaded files
        target_content = await target_srt.read()
        native_content = await native_srt.read()
        freq_content = await frequency_list.read()
        
        # Parse SRT files
        target_subs = parse_srt(target_content.decode('utf-8'))
        native_subs = parse_srt(native_content.decode('utf-8'))
        
        # Parse frequency list
        freq_lines = freq_content.decode('utf-8').split('\n')
        known_words = set(freq_lines[:top_n_words])
        
        # Initialize fusion engine
        engine = SubtitleFusionEngine()
        
        # Process fusion
        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang=target_language,
            enable_inline_translation=enable_inline_translation,
            deepl_api=None,  # TODO: Implement DeepL API integration
            native_lang=native_language
        )
        
        # Generate output SRT
        output_srt = generate_srt(result['hybrid'])
        
        # Prepare stats
        stats = {
            "processing_time": "calculated_from_python_engine",
            "words_processed": len(known_words),
            "subtitles_processed": len(target_subs),
            "subtitles_replaced": result['replacedCount'],
            "replacement_rate": f"{(result['replacedCount'] / len(target_subs) * 100):.1f}%"
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
