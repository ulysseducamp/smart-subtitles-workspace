# Multi-stage Dockerfile for SmartSub API
# Stage 1: Build TypeScript CLI using Node.js
FROM node:18-alpine AS node-builder

# Set working directory for Node.js build
WORKDIR /app/node-cli

# Copy package files for Node.js dependencies
COPY subtitles-fusion-algorithm-public/package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production

# Copy TypeScript source code
COPY subtitles-fusion-algorithm-public/src ./src
COPY subtitles-fusion-algorithm-public/tsconfig.json ./

# Install TypeScript and build dependencies
RUN npm install typescript @types/node --save-dev

# Build TypeScript to JavaScript
RUN npm run build

# Stage 2: Final image with Python + Node.js runtime
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Verify Node.js installation
RUN node --version && npm --version

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built Node.js CLI from stage 1
COPY --from=node-builder /app/node-cli/dist ./dist
COPY --from=node-builder /app/node-cli/node_modules ./node_modules
COPY --from=node-builder /app/node-cli/package.json ./package.json

# Copy FastAPI application files individually
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
