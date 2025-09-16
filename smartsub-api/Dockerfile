# Python-only Dockerfile for SmartSub API with Rate Limiting
FROM python:3.11-slim

# Force cache bust - Railway cache issue fix
ARG CACHE_BUST=2025-09-16-09-45

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI application files
COPY main.py ./
COPY env.example ./
COPY test_api_key.py ./
COPY src/ ./src/

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port (Railway will override this)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start the FastAPI application
CMD ["python", "main.py"]