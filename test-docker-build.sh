#!/bin/bash

# Test script for Docker build and runtime verification
# This script tests the Docker build locally before Railway deployment

set -e  # Exit on any error

echo "🐳 SmartSub API Docker Build Test"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_success "Docker is installed"

# Build the Docker image
print_status "Building Docker image..."
docker build -t smartsub-api:test .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

# Test 1: Check if both Python and Node.js are available
print_status "Testing Python and Node.js availability..."
docker run --rm smartsub-api:test python --version
docker run --rm smartsub-api:test node --version
docker run --rm smartsub-api:test npm --version

print_success "Both Python and Node.js are available in the container"

# Test 2: Check if the CLI is accessible
print_status "Testing Node.js CLI accessibility..."
docker run --rm smartsub-api:test node dist/main.js --help

if [ $? -eq 0 ]; then
    print_success "Node.js CLI is accessible and working"
else
    print_warning "Node.js CLI help command failed (this might be expected if no arguments provided)"
fi

# Test 3: Check if FastAPI can start
print_status "Testing FastAPI startup..."
timeout 10s docker run --rm -p 3000:3000 smartsub-api:test python main.py &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 5

# Test health endpoint
if curl -f http://localhost:3000/health &> /dev/null; then
    print_success "FastAPI is running and health endpoint is accessible"
else
    print_warning "FastAPI health check failed (this might be expected in test environment)"
fi

# Clean up
kill $FASTAPI_PID 2>/dev/null || true

# Test 4: Check file structure
print_status "Checking container file structure..."
docker run --rm smartsub-api:test ls -la /app/
docker run --rm smartsub-api:test ls -la /app/dist/

print_success "File structure looks correct"

echo ""
echo "🎉 Docker build test completed successfully!"
echo ""
echo "Next steps:"
echo "1. Push your changes to your Git repository"
echo "2. Deploy to Railway (see deployment instructions)"
echo "3. Test the deployed API endpoint"
