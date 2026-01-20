---
name: docker-build-skill
description: Containerize applications with optimized Docker images for Phase IV Kubernetes deployment.
version: 1.0.0
---

# Docker Build Skill

This skill containerizes the Todo Chatbot frontend (Next.js) and backend (FastAPI) applications with production-ready Docker images.

## Input Requirements

- **Application Type**: frontend (Next.js) or backend (FastAPI)
- **Target Environment**: Minikube local Kubernetes
- **Build Options**: Multi-stage build, cache optimization, security hardening

## Workflow Overview

```
1. Analyze Application Structure
   ↓
2. Create .dockerignore
   ↓
3. Write Optimized Dockerfile
   ↓
4. Build Docker Image
   ↓
5. Verify Image
   ↓
6. Tag for Registry (optional)
```

## Instructions

### Step 1: Analyze Application Structure

**Frontend (Next.js) - Check for:**
- `package.json` and `package-lock.json`
- `next.config.js` or `next.config.mjs`
- `src/` or `app/` directory
- Build output configuration (standalone)

**Backend (FastAPI) - Check for:**
- `requirements.txt` or `pyproject.toml`
- `app/` directory with `main.py`
- Entry point configuration

### Step 2: Create .dockerignore

**Frontend .dockerignore:**
```
# Dependencies
node_modules
.pnpm-store

# Build outputs
.next
out
dist
build

# Development
.env.local
.env.development.local
.env.test.local

# Version control
.git
.gitignore

# IDE
.vscode
.idea
*.swp

# Testing
coverage
.nyc_output

# Misc
README.md
*.log
Dockerfile*
docker-compose*
```

**Backend .dockerignore:**
```
# Python
__pycache__
*.py[cod]
*$py.class
.Python
venv
.venv
env

# Testing
.pytest_cache
.coverage
htmlcov
.tox

# Development
.env
.env.local
*.log

# Version control
.git
.gitignore

# IDE
.vscode
.idea

# Misc
README.md
Dockerfile*
docker-compose*
```

### Step 3: Write Optimized Dockerfile

**Frontend Dockerfile (Next.js with Standalone Output):**

```dockerfile
# ============================================
# Todo Frontend - Next.js Production Dockerfile
# ============================================

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build application
RUN npm run build

# Stage 3: Production Runner
FROM node:20-alpine AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Set hostname
ENV HOSTNAME="0.0.0.0"

# Start application
CMD ["node", "server.js"]
```

**Backend Dockerfile (FastAPI):**

```dockerfile
# ============================================
# Todo Backend - FastAPI Production Dockerfile
# ============================================

# Stage 1: Dependencies
FROM python:3.13-slim AS deps

WORKDIR /app

# Install dependencies with cache mount
COPY requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim AS production

WORKDIR /app

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy dependencies from deps stage
COPY --from=deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 4: Build Docker Image

**For Minikube (use Minikube's Docker daemon):**
```bash
# Set Docker environment to Minikube
eval $(minikube docker-env)

# Build frontend
docker build -t todo-frontend:latest ./frontend

# Build backend
docker build -t todo-backend:latest ./backend
```

**Standard Build:**
```bash
# Build with tag
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend
docker build -t todo-backend:latest -f backend/Dockerfile ./backend

# Build specific stage
docker build --target production -t todo-frontend:prod ./frontend

# Build with build args
docker build --build-arg NODE_VERSION=20-alpine -t todo-frontend:latest ./frontend

# Build with no cache
docker build --no-cache -t todo-frontend:latest ./frontend
```

### Step 5: Verify Image

```bash
# List images
docker images | grep todo

# Check image size
docker images todo-frontend:latest --format "{{.Size}}"
docker images todo-backend:latest --format "{{.Size}}"

# Test run container
docker run -d -p 3000:3000 --name test-frontend todo-frontend:latest
docker run -d -p 8000:8000 --name test-backend todo-backend:latest

# Check container logs
docker logs test-frontend
docker logs test-backend

# Test endpoint
curl http://localhost:3000
curl http://localhost:8000/health

# Cleanup test containers
docker stop test-frontend test-backend
docker rm test-frontend test-backend
```

### Step 6: Tag for Registry (Optional)

```bash
# Tag for Minikube registry
docker tag todo-frontend:latest localhost:5000/todo-frontend:latest
docker tag todo-backend:latest localhost:5000/todo-backend:latest

# Push to Minikube registry
docker push localhost:5000/todo-frontend:latest
docker push localhost:5000/todo-backend:latest

# Verify in Minikube
minikube image ls | grep todo
```

## Next.js Standalone Configuration

For optimal Next.js containerization, ensure `next.config.js` has:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // ... other config
}

module.exports = nextConfig
```

## Image Optimization Tips

1. **Use Alpine Base Images**: `node:20-alpine` instead of `node:20`
2. **Multi-Stage Builds**: Separate build and production stages
3. **Cache Mounts**: Use BuildKit cache for npm/pip
4. **Non-Root User**: Always run as non-root in production
5. **.dockerignore**: Exclude unnecessary files
6. **Layer Ordering**: Put rarely-changing layers first

## Expected Image Sizes

| Image | Expected Size |
|-------|--------------|
| todo-frontend (Next.js standalone) | ~150-200MB |
| todo-backend (FastAPI slim) | ~200-250MB |

## Troubleshooting

### Build Fails at npm install

```bash
# Clear npm cache
docker builder prune

# Build without cache
docker build --no-cache -t todo-frontend:latest ./frontend
```

### Image Not Found in Minikube

```bash
# Ensure docker-env is set
eval $(minikube docker-env)

# Rebuild image
docker build -t todo-frontend:latest ./frontend

# Verify
minikube image ls | grep todo
```

### Container Exits Immediately

```bash
# Check logs
docker logs <container-id>

# Run interactively
docker run -it todo-frontend:latest /bin/sh
```

## Agent Coordination

This skill coordinates with:

| Task | Agent |
|------|-------|
| Dockerfile optimization | `docker-containerizer` |
| Minikube integration | `minikube-cluster-ops` |
| Deployment | `kubectl-resource-manager` |

## Output

Upon completion, provide:
1. Built image names and tags
2. Image sizes
3. Verification test results
4. Next steps for deployment
