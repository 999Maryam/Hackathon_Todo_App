# Implementation Plan: Docker Containerization

**Branch**: `008-docker-containerization` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/008-docker-containerization/spec.md`

## Summary

Containerize the Todo AI Chatbot application (Phase III) for local Kubernetes deployment. Create optimized multi-stage Dockerfiles for both frontend (Next.js) and backend (FastAPI), docker-compose.yml for local orchestration, and .dockerignore files to minimize build context. This enables the transition from local development to Minikube/Helm deployment in Phase IV.

## Technical Context

**Language/Version**: Python 3.13+ (backend), Node.js 20 (frontend), Docker 24+
**Primary Dependencies**: FastAPI, uvicorn (backend); Next.js 16+, React 19 (frontend); Docker, docker-compose
**Storage**: N/A (containerization layer - app connects to external Neon PostgreSQL)
**Testing**: Manual docker build/run verification, docker-compose up smoke tests
**Target Platform**: Linux containers (amd64), local development on Linux/WSL2/macOS
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Backend image <500MB, Frontend image <300MB, Services start in <60s
**Constraints**: No secrets in images, non-root execution, reuse Phase III code unchanged
**Scale/Scope**: Single developer local testing, preparation for Minikube deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Spec-Driven Development | Follow /specify → /plan → /tasks → /implement | PASS | Following SDD workflow |
| II. Progressive Evolution | Build on Phase III without breaking changes | PASS | Containerization adds layer, no app changes |
| IV. Security First | No secrets in images, non-root users | PASS | Env vars via .env, USER directive in Dockerfile |
| V. Stateless Design | Containers must be stateless | PASS | No local storage, external DB connection |
| VI. Cloud-Native Mindset | Multi-stage Dockerfiles, .dockerignore, health endpoints | PASS | All requirements addressed |
| VIII. Maintainability | Task ID + spec references in files | PASS | Will include in Dockerfile comments |

**Gate Result**: PASS - All constitutional requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/008-docker-containerization/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A - no data models)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - no APIs)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── Dockerfile           # Multi-stage FastAPI container (to be created/updated)
├── .dockerignore        # Build context exclusions (to be created)
├── app/                 # Existing application code (unchanged)
├── requirements.txt     # Existing dependencies (unchanged)
└── ...

frontend/
├── Dockerfile           # Multi-stage Next.js container (to be created)
├── .dockerignore        # Build context exclusions (to be created)
├── src/                 # Existing application code (unchanged)
├── package.json         # Existing dependencies (unchanged)
└── ...

docker-compose.yml       # Root-level orchestration (to be created)
README.md                # Updated with Docker commands
```

**Structure Decision**: Web application structure with separate frontend/backend directories. Docker artifacts placed directly in each service directory (Dockerfiles, .dockerignore) with root-level docker-compose.yml for orchestration.

## Architecture Decisions

### AD-001: Multi-Stage Dockerfile Pattern

**Decision**: Use multi-stage builds for both frontend and backend Dockerfiles.

**Rationale**:
- Separates build dependencies from runtime
- Reduces final image size significantly
- Enables caching of dependency installation layer
- Follows Docker best practices

**Alternatives Considered**:
- Single-stage build: Rejected due to larger image size (includes build tools)
- External build scripts: Rejected due to added complexity

### AD-002: Base Image Selection

**Decision**:
- Backend: `python:3.13-slim` (Debian-based slim variant)
- Frontend: `node:20-alpine` (Alpine Linux minimal)

**Rationale**:
- python:3.13-slim: Balances size (~150MB) with glibc compatibility for Python packages
- node:20-alpine: Minimal footprint (~50MB), sufficient for Node.js runtime
- Both are official images with security updates

**Alternatives Considered**:
- python:3.13-alpine: Rejected due to musl libc compatibility issues with some Python packages
- node:20-slim: Viable but Alpine is smaller and sufficient

### AD-003: Next.js Standalone Output

**Decision**: Configure Next.js for standalone output mode.

**Rationale**:
- Produces self-contained build without node_modules
- Dramatically reduces image size (from ~500MB to ~150MB)
- Includes only necessary dependencies in output
- Official Next.js recommendation for Docker deployments

**Configuration Required**:
```javascript
// next.config.ts
output: 'standalone'
```

### AD-004: Non-Root User Execution

**Decision**: Create and use non-root user in all containers.

**Rationale**:
- Security best practice (defense in depth)
- Required by Kubernetes security policies
- Prevents container escape privilege escalation
- Constitution requirement (Security First principle)

**Implementation**:
```dockerfile
RUN adduser --system --uid 1001 appuser
USER appuser
```

### AD-005: Docker Compose for Local Development

**Decision**: Use docker-compose.yml for local multi-container orchestration.

**Rationale**:
- Simple local testing before Kubernetes
- Defines service dependencies and networking
- Environment variable management via .env files
- Supports development profile with volume mounts

**Alternatives Considered**:
- Direct docker run commands: Rejected due to complexity with multiple services
- Kubernetes locally (Minikube): Reserved for next Phase IV spec

## Implementation Approach

### Backend Dockerfile Strategy

```text
Stage 1: Builder
- FROM python:3.13-slim AS builder
- Install build dependencies
- Create virtual environment
- Copy requirements.txt
- pip install dependencies

Stage 2: Runtime
- FROM python:3.13-slim
- Copy virtual environment from builder
- Copy application code
- Create non-root user
- Set environment variables
- Expose port 8000
- CMD uvicorn
```

### Frontend Dockerfile Strategy

```text
Stage 1: Dependencies
- FROM node:20-alpine AS deps
- Copy package.json, package-lock.json
- npm ci (clean install)

Stage 2: Builder
- FROM node:20-alpine AS builder
- Copy node_modules from deps
- Copy source code
- npm run build (with standalone output)

Stage 3: Runner
- FROM node:20-alpine AS runner
- Copy standalone output only
- Create non-root user
- Set environment variables
- Expose port 3000
- CMD node server.js
```

### Docker Compose Configuration

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    env_file: ./backend/.env
    healthcheck: curl localhost:8000/health

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    env_file: ./frontend/.env
    depends_on: [backend]
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000
```

## Testing Strategy

### Build Verification

```bash
# Backend build
docker build -t todo-backend -f backend/Dockerfile backend/
docker images todo-backend  # Verify size <500MB

# Frontend build
docker build -t todo-frontend -f frontend/Dockerfile frontend/
docker images todo-frontend  # Verify size <300MB
```

### Runtime Verification

```bash
# Start services
docker-compose up -d

# Health check
curl http://localhost:8000/health  # → {"status": "healthy"}

# Frontend accessible
curl -I http://localhost:3000  # → HTTP 200

# Logs inspection
docker-compose logs backend
docker-compose logs frontend
```

### Security Verification

```bash
# Non-root user check
docker exec todo-backend whoami  # → appuser (not root)
docker exec todo-frontend whoami  # → nextjs (not root)
```

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Next.js standalone mode not configured | Build fails or large images | Verify next.config.ts has `output: 'standalone'` |
| Python package incompatibility with slim | Build fails | Test locally, fallback to full python image if needed |
| Port conflicts on local machine | Services fail to start | Document port requirements, use different ports if needed |
| Missing environment variables | Runtime crashes | Document required vars, fail-fast validation in apps |

## Deliverables Summary

| File | Purpose | Location |
|------|---------|----------|
| Dockerfile (backend) | Multi-stage FastAPI container | backend/Dockerfile |
| Dockerfile (frontend) | Multi-stage Next.js container | frontend/Dockerfile |
| .dockerignore (backend) | Exclude __pycache__, venv, .env | backend/.dockerignore |
| .dockerignore (frontend) | Exclude node_modules, .next, .env | frontend/.dockerignore |
| docker-compose.yml | Local orchestration | ./docker-compose.yml |
| README.md update | Docker build/run commands | ./README.md |
