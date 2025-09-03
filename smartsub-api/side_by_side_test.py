#!/usr/bin/env python3
"""
Side by Side Test - Run both versions simultaneously
Compare working minimal FastAPI vs your main.py
"""

import time
import uvicorn
import subprocess
import threading
from fastapi import FastAPI

# Create minimal working FastAPI app
def create_minimal_app():
    app = FastAPI(title="MINIMAL FastAPI")
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "MINIMAL FastAPI working!", "timestamp": time.time()}
    
    return app

# Import your actual app
def import_actual_app():
    try:
        from main import app
        print("✅ Successfully imported app from main.py")
        return app
    except Exception as e:
        print(f"❌ Failed to import app from main.py: {e}")
        return None

def run_server(app, port, name):
    """Run a server in a separate thread"""
    print(f"🚀 Starting {name} on port {port}...")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")

def test_endpoint(port, name):
    """Test an endpoint with curl"""
    import subprocess
    import time
    
    # Wait for server to start
    time.sleep(3)
    
    print(f"\n🔍 Testing {name} on port {port}...")
    
    # Test with curl
    try:
        result = subprocess.run(
            f"curl -s http://localhost:{port}/test" if "MINIMAL" in name else f"curl -s http://localhost:{port}/health",
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ {name} responded: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {name} failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {name} test error: {e}")
        return False

def main():
    print("🔍 Starting Side by Side FastAPI Test...")
    print("=" * 60)
    
    # Create minimal app
    print("📝 Creating minimal working FastAPI app...")
    minimal_app = create_minimal_app()
    
    # Import actual app
    print("📝 Importing your actual main.py app...")
    actual_app = import_actual_app()
    
    if not actual_app:
        print("❌ Cannot proceed without importing actual app")
        return
    
    # Start both servers
    print("\n🚀 Starting both servers...")
    
    # Start minimal app on port 3000
    minimal_thread = threading.Thread(
        target=run_server, 
        args=(minimal_app, 3000, "MINIMAL FastAPI")
    )
    minimal_thread.daemon = True
    minimal_thread.start()
    
    # Start actual app on port 3001
    actual_thread = threading.Thread(
        target=run_server, 
        args=(actual_app, 3001, "YOUR main.py")
    )
    actual_thread.daemon = True
    actual_thread.start()
    
    # Wait for servers to start
    print("⏳ Waiting for servers to start...")
    time.sleep(5)
    
    # Test both endpoints
    print("\n🧪 Testing both endpoints...")
    
    minimal_works = test_endpoint(3000, "MINIMAL FastAPI")
    actual_works = test_endpoint(3001, "YOUR main.py")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Side by Side Test Results:")
    print(f"   MINIMAL FastAPI (port 3000): {'✅' if minimal_works else '❌'}")
    print(f"   YOUR main.py (port 3001): {'✅' if actual_works else '❌'}")
    
    # Analysis
    print("\n🎯 Analysis:")
    if minimal_works and actual_works:
        print("✅ Both work - FastAPI is functional on your system")
    elif minimal_works and not actual_works:
        print("❌ Minimal works, yours doesn't - issue in your main.py")
    elif not minimal_works and actual_works:
        print("❌ Yours works, minimal doesn't - unexpected result")
    else:
        print("❌ Neither works - system-level FastAPI issue")
    
    print("\n🎯 Side by side test complete!")

if __name__ == "__main__":
    main()
