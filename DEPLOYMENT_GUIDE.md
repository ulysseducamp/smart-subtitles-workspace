# SmartSub API Docker Deployment Guide

## 🎯 Overview
This guide will help you deploy your SmartSub API to Railway using Docker, supporting both Python (FastAPI) and Node.js (CLI) runtimes.

## 📋 Prerequisites
- Docker installed locally
- Git repository with your code
- Railway account
- Your existing Railway project: https://smartsub-api-production.up.railway.app

## 🚀 Step-by-Step Deployment

### Step 1: Local Testing (Recommended)

Before deploying to Railway, test your Docker setup locally:

```bash
# Navigate to your project root
cd /Users/ulysse/Documents/01\ PROJECTS/smart-subs/smart-subtitles-workspace

# Run the Docker build test
./test-docker-build.sh
```

**Expected Output:**
```
🐳 SmartSub API Docker Build Test
==================================
[SUCCESS] Docker is installed
[INFO] Building Docker image...
[SUCCESS] Docker image built successfully
[SUCCESS] Both Python and Node.js are available in the container
[SUCCESS] Node.js CLI is accessible and working
[SUCCESS] FastAPI is running and health endpoint is accessible
[SUCCESS] File structure looks correct

🎉 Docker build test completed successfully!
```

### Step 2: Test API Functionality Locally

```bash
# Start the container locally
docker run -d -p 3000:3000 --name smartsub-test smartsub-api:test

# Wait a moment for startup
sleep 5

# Test the API
python test-api-functionality.py http://localhost:3000

# Clean up
docker stop smartsub-test
docker rm smartsub-test
```

### Step 3: Commit and Push Changes

```bash
# Add all new files
git add Dockerfile .dockerignore railway.toml test-docker-build.sh test-api-functionality.py

# Commit changes
git commit -m "Add Docker support for Python + Node.js deployment"

# Push to your repository
git push origin main
```

### Step 4: Deploy to Railway

#### Option A: Automatic Deployment (if connected to Git)
1. Go to your Railway project: https://railway.app/dashboard
2. Navigate to your `smartsub-api-production` project
3. Railway will automatically detect the new `Dockerfile` and start building
4. Monitor the build logs in the Railway dashboard

#### Option B: Manual Deployment
1. Go to Railway dashboard
2. Select your project
3. Go to "Settings" → "Build"
4. Ensure "Builder" is set to "Dockerfile"
5. Click "Deploy" to trigger a new build

### Step 5: Monitor Deployment

**What to expect in Railway build logs:**

```
Building Docker image...
Step 1/15 : FROM node:18-alpine AS node-builder
Step 2/15 : WORKDIR /app/node-cli
Step 3/15 : COPY subtitles-fusion-algorithm-public/package*.json ./
Step 4/15 : RUN npm ci --only=production
...
Step 15/15 : CMD ["python", "main.py"]
Successfully built [image-id]
Successfully tagged [tag]

Starting container...
[INFO] Starting FastAPI server on port 3000
```

**Success indicators:**
- ✅ Build completes without errors
- ✅ Container starts successfully
- ✅ Health check passes
- ✅ No "node: command not found" errors

### Step 6: Test Deployed API

```bash
# Test the deployed API
python test-api-functionality.py https://smartsub-api-production.up.railway.app
```

**Expected successful output:**
```
🧪 SmartSub API Functionality Test
========================================
Testing API at: https://smartsub-api-production.up.railway.app

🔍 Testing health endpoint...
✅ Health endpoint working
🔍 Testing root endpoint...
✅ Root endpoint working: Smart Netflix Subtitles API is running!
🔍 Testing fuse-subtitles endpoint...
✅ Fuse-subtitles endpoint working
   Output length: 1234 characters

📊 Test Results Summary:
------------------------------
Health Endpoint: ✅ PASS
Root Endpoint: ✅ PASS
Fuse Subtitles Endpoint: ✅ PASS

Results: 3/3 tests passed
🎉 All tests passed! Your API is working correctly.
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Build Fails with "node: command not found"
**Problem:** Railway is still using auto-detection instead of Dockerfile
**Solution:** 
- Check that `railway.toml` has `builder = "DOCKERFILE"`
- Ensure `Dockerfile` is in the project root
- Redeploy the project

#### 2. Docker Build Fails Locally
**Problem:** Missing dependencies or incorrect paths
**Solution:**
```bash
# Check if all required files exist
ls -la subtitles-fusion-algorithm-public/package.json
ls -la smartsub-api/requirements.txt
ls -la subtitles-fusion-algorithm-public/dist/

# Rebuild with verbose output
docker build -t smartsub-api:test . --no-cache --progress=plain
```

#### 3. API Returns 500 Error on /fuse-subtitles
**Problem:** Node.js CLI not found or not working
**Solution:**
```bash
# Test Node.js CLI directly in container
docker run --rm smartsub-api:test node --version
docker run --rm smartsub-api:test ls -la /app/dist/
docker run --rm smartsub-api:test node dist/main.js --help
```

#### 4. Railway Build Times Out
**Problem:** Build process is too slow
**Solution:**
- Check `.dockerignore` is excluding unnecessary files
- Consider using smaller base images
- Monitor Railway build logs for specific timeout points

#### 5. Environment Variables Not Working
**Problem:** API key or other env vars not accessible
**Solution:**
- Check Railway environment variables in dashboard
- Ensure variables are set for the correct service
- Restart the service after adding new variables

### Debug Commands

```bash
# Check container logs
docker logs [container-id]

# Inspect running container
docker exec -it [container-id] /bin/bash

# Test specific components
docker run --rm smartsub-api:test python -c "import subprocess; print(subprocess.run(['node', '--version'], capture_output=True, text=True).stdout)"
```

## 📊 Expected Performance

- **Build time:** 3-5 minutes (first build), 1-2 minutes (subsequent builds)
- **Startup time:** 10-30 seconds
- **Memory usage:** ~200-400MB
- **Response time:** <2 seconds for health checks, 5-30 seconds for subtitle processing

## 🔄 Rollback Plan

If deployment fails:

1. **Quick rollback:** Revert `railway.toml` to previous configuration
2. **Git rollback:** `git revert [commit-hash]` and push
3. **Railway rollback:** Use Railway's deployment history to rollback to previous version

## 📞 Support

If you encounter issues:
1. Check Railway build logs first
2. Run local tests to isolate the problem
3. Check this guide's troubleshooting section
4. Verify all files are in the correct locations

## ✅ Success Checklist

- [ ] Docker build completes successfully locally
- [ ] Both Python and Node.js are available in container
- [ ] FastAPI starts without errors
- [ ] Health endpoint responds correctly
- [ ] Fuse-subtitles endpoint processes files successfully
- [ ] Railway deployment completes
- [ ] Deployed API passes all tests
- [ ] No "node: command not found" errors

---

**🎉 Congratulations!** Your SmartSub API is now successfully deployed with both Python and Node.js support!
