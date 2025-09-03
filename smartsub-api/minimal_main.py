#!/usr/bin/env python3
"""
Minimal Main - Emergency fallback version of main.py
Same endpoints as original but no external dependencies
Helps isolate if issue is in endpoints vs dependencies
"""

import time
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import subprocess
import tempfile

# Create FastAPI app with CLI integration
app = FastAPI(
    title="Smart Netflix Subtitles API",
    description="FastAPI backend with TypeScript CLI integration for subtitle fusion",
    version="1.0.0"
)

# CORS middleware for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API data validation
class SubtitleRequest(BaseModel):
    target_language: str
    native_language: str
    top_n_words: int = 2000
    enable_inline_translation: bool = False
    deepl_api_key: Optional[str] = None

class SubtitleResponse(BaseModel):
    success: bool
    output_srt: str
    stats: dict
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Smart Netflix Subtitles API (Minimal) is running!",
        "status": "healthy",
        "version": "0.1.0",
        "note": "This is the emergency fallback version"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "service": "smartsub-api-minimal",
        "timestamp": time.time()
    }

# Endpoint for subtitle fusion (stub implementation)
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
    start_time = time.time()
    
    try:
        # Stub implementation - no external dependencies
        print(f"📝 Received request: {target_language} -> {native_language}")
        print(f"📊 Top N words: {top_n_words}")
        print(f"🔄 Inline translation: {enable_inline_translation}")
        
        # Create temporary files for CLI processing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_target, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_native, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_freq, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as temp_output:
            
            # Write uploaded files to temporary files
            target_content = await target_srt.read()
            native_content = await native_srt.read()
            freq_content = await frequency_list.read()
            
            temp_target.write(target_content.decode())
            temp_native.write(native_content.decode())
            temp_freq.write(freq_content.decode())
            
            # Flush to ensure all data is written
            temp_target.flush()
            temp_native.flush()
            temp_freq.flush()
            
            print(f"📁 Files written to temp: {temp_target.name}, {temp_native.name}, {temp_freq.name}")
            
            # Build CLI command
            cli_path = os.path.join(os.path.dirname(__file__), "..", "subtitles-fusion-algorithm-public", "dist", "main.js")
            cmd = [
                "node",
                cli_path,
                "--target", temp_target.name,
                "--native", temp_native.name,
                "--freq", temp_freq.name,
                "--out", temp_output.name,
                "--topN", str(top_n_words),
                "--lang", target_language,
                "--native-lang", native_language
            ]
            
            # Add inline translation options if enabled
            if enable_inline_translation:
                cmd.append("--inline-translation")
                if deepl_api_key:
                    cmd.extend(["--deepl-key", deepl_api_key])
            
            print(f"🔧 CLI command: {' '.join(cmd)}")
            
            # Execute CLI
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )
            
            # Check CLI execution result
            if result.returncode != 0:
                print(f"❌ CLI failed with return code {result.returncode}")
                print(f"❌ CLI stderr: {result.stderr}")
                raise HTTPException(
                    status_code=500,
                    detail=f"CLI processing failed: {result.stderr}"
                )
            
            print(f"✅ CLI executed successfully")
            print(f"📝 CLI stdout: {result.stdout}")
            
            # Read output file
            with open(temp_output.name, 'r') as f:
                output_srt = f.read()
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Build statistics
            stats = {
                "processing_time": f"{processing_time:.2f}s",
                "cli_return_code": result.returncode,
                "files_processed": {
                    "target_srt": len(target_content),
                    "native_srt": len(native_content),
                    "frequency_list": len(freq_content),
                    "output_srt": len(output_srt)
                }
            }
            
            return SubtitleResponse(
                success=True,
                output_srt=output_srt,
                stats=stats
            )
        
    except subprocess.TimeoutExpired:
        print("⏰ CLI processing timeout")
        raise HTTPException(status_code=408, detail="Processing timeout - CLI took too long")
        
    except Exception as e:
        print(f"❌ Error in subtitle fusion: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Subtitle fusion error: {str(e)}")
        
    finally:
        # Clean up temporary files
        temp_files = []
        try:
            if 'temp_target' in locals():
                temp_files.append(temp_target.name)
            if 'temp_native' in locals():
                temp_files.append(temp_native.name)
            if 'temp_freq' in locals():
                temp_files.append(temp_freq.name)
            if 'temp_output' in locals():
                temp_files.append(temp_output.name)
                
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    print(f"🧹 Cleaned up: {temp_file}")
        except Exception as cleanup_error:
            print(f"⚠️ Warning: Could not clean up temp file: {cleanup_error}")

if __name__ == "__main__":
    print("🚀 Starting Smart Netflix Subtitles API...")
    print("📝 FastAPI backend with TypeScript CLI integration")
    print("🔧 Ready to process subtitle fusion requests")
    
    port = int(os.environ.get("PORT", 3000))  # Use standard port now
    print(f"🌐 Server will start on port {port}")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=port,
        log_level="info"
    )
