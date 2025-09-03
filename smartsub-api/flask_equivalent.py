#!/usr/bin/env python3
"""
Flask Equivalent Test
Equivalent Flask app with same endpoints
Prove Flask actually works as claimed
Same port (3000), same functionality
Compare behavior side by side
"""

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "message": "Flask is working!",
        "framework": "Flask",
        "status": "healthy"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "framework": "Flask",
        "timestamp": time.time()
    })

@app.route("/test")
def test():
    return jsonify({
        "message": "Flask test endpoint",
        "method": request.method,
        "headers": dict(request.headers)
    })

if __name__ == "__main__":
    print("=== STARTING FLASK EQUIVALENT TEST ===")
    print("Port: 3000")
    print("Host: 127.0.0.1")
    print("Framework: Flask")
    print("=" * 40)
    
    try:
        app.run(
            host="127.0.0.1",
            port=3000,
            debug=True
        )
    except Exception as e:
        print(f"ERROR starting Flask: {e}")
        import traceback
        traceback.print_exc()

