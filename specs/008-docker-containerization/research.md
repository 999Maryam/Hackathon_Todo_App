# Research: Docker Containerization

**Feature**: 008-docker-containerization
**Date**: 2026-01-20
**Status**: Complete

## Research Summary

This document consolidates research findings for containerizing the Todo AI Chatbot application. All technical decisions have been resolved with clear rationale.

---

## R-001: Python Base Image Selection

**Question**: Which Python base image provides the best balance of size and compatibility?

**Decision**: `python:3.13-slim`

**Rationale**:
- Debian-based slim variant (~150MB compressed)
- Full glibc support for all Python packages
- Regular security updates from official Python team
- Pre-installed pip and common build tools

**Alternatives Considered**:

| Image | Size | Pros | Cons |
|-------|------|------|------|
| python:3.13 | ~1GB | Full Debian, all tools | Too large for containers |
| python:3.13-slim | ~150MB | Good balance | Needs some build deps |
| python:3.13-alpine | ~50MB | Smallest | musl libc incompatibility with some packages |

**Research Source**: Docker Hub official Python images, FastAPI deployment docs

---

## R-002: Node.js Base Image Selection

**Question**: Which Node.js base image is optimal for Next.js standalone deployment?

**Decision**: `node:20-alpine`

**Rationale**:
- Alpine Linux is minimal (~50MB)
- Node.js 20 LTS provides long-term support
- Sufficient for Next.js standalone runtime (no native modules)
- Smallest official Node image

**Alternatives Considered**:

| Image | Size | Pros | Cons |
|-------|------|------|------|
| node:20 | ~1GB | Full Debian | Too large |
| node:20-slim | ~200MB | Smaller Debian | Still larger than needed |
| node:20-alpine | ~50MB | Minimal | Limited package manager |

**Research Source**: Next.js Docker deployment guide, Vercel examples

---

## R-003: Next.js Standalone Output Mode

**Question**: How to minimize Next.js container image size?

**Decision**: Use `output: 'standalone'` in next.config.ts

**Rationale**:
- Standalone mode produces self-contained build
- Includes only necessary dependencies (no full node_modules)
- Reduces image size from ~500MB to ~150MB
- Official Next.js recommendation for Docker

**Configuration**:
```typescript
// next.config.ts
const nextConfig = {
  output: 'standalone',
  // ... other config
}
```

**File Structure After Build**:
```
.next/standalone/
├── server.js          # Entry point
├── node_modules/      # Minimal runtime deps only
└── .next/
    └── static/        # Static assets
```

**Research Source**: Next.js documentation (nextjs.org/docs/app/building-your-application/deploying#docker-image)

---

## R-004: Multi-Stage Build Pattern

**Question**: What's the optimal Dockerfile structure for minimal images?

**Decision**: Multi-stage builds with separate builder and runtime stages

**Rationale**:
- Builder stage: Install dependencies, compile code
- Runtime stage: Copy only artifacts needed to run
- Excludes: source code, build tools, dev dependencies
- Docker layer caching improves rebuild speed

**Backend Pattern**:
```dockerfile
# Stage 1: Build
FROM python:3.13-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim
COPY --from=builder /root/.local /root/.local
COPY ./app ./app
CMD ["uvicorn", "app.main:app"]
```

**Frontend Pattern**:
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine AS runner
COPY --from=builder /app/.next/standalone ./
CMD ["node", "server.js"]
```

**Research Source**: Docker multi-stage build documentation

---

## R-005: Non-Root User Security

**Question**: How to implement container security best practices?

**Decision**: Create dedicated non-root user in each container

**Rationale**:
- Defense in depth (limits container escape impact)
- Required by Kubernetes PodSecurityPolicy/Standards
- Docker best practice
- Constitution requirement (Security First principle)

**Implementation**:
```dockerfile
# Backend
RUN adduser --system --uid 1001 appuser
USER appuser

# Frontend (Alpine syntax)
RUN adduser --system --uid 1001 nextjs
USER nextjs
```

**Research Source**: OWASP Container Security, Kubernetes Security Best Practices

---

## R-006: Docker Compose Configuration

**Question**: What docker-compose features are needed for local development?

**Decision**: Use docker-compose v3.8 with env_file, health checks, and dev profile

**Features Used**:
- `env_file`: Load environment variables from .env files
- `healthcheck`: Container health monitoring
- `depends_on`: Service startup ordering
- `profiles`: Separate dev/prod configurations
- `volumes`: Dev mode source mounting

**Network**: Default bridge network with service DNS (backend reachable as `backend:8000`)

**Research Source**: Docker Compose documentation, 12-factor app methodology

---

## R-007: .dockerignore Patterns

**Question**: What files should be excluded from Docker build context?

**Decision**: Exclude all non-essential files to minimize context size

**Backend .dockerignore**:
```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
venv/
.env
.env.*
*.egg-info/
dist/
build/
.git/
```

**Frontend .dockerignore**:
```
node_modules/
.next/
.env
.env.*
*.log
.git/
coverage/
.turbo/
```

**Impact**: Reduces build context from ~500MB to <10MB

**Research Source**: Docker documentation, gitignore patterns

---

## Unresolved Items

None. All technical decisions have been resolved.

---

## References

1. Docker Official Images: https://hub.docker.com/_/python, https://hub.docker.com/_/node
2. Next.js Docker Deployment: https://nextjs.org/docs/app/building-your-application/deploying#docker-image
3. FastAPI Docker Deployment: https://fastapi.tiangolo.com/deployment/docker/
4. Docker Multi-Stage Builds: https://docs.docker.com/build/building/multi-stage/
5. Container Security: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
