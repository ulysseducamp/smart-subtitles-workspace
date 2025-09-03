from fastapi import FastAPI
import uvicorn
import os
import time

print(f"POST-REBOOT TEST STARTING")
print(f"PID: {os.getpid()}")
print(f"Time: {time.strftime('%H:%M:%S')}")

app = FastAPI()

@app.get("/")
def root():
    print("Root endpoint called!")
    return {"status": "working", "message": "FastAPI is alive after reboot"}

@app.get("/health")  
def health():
    print("Health endpoint called!")
    return {"status": "ok", "reboot": "success"}

if __name__ == "__main__":
    print("Starting uvicorn server...")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=3000,
        log_level="info"
    )


