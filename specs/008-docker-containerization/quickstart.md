# Quickstart: Docker Containerization

**Feature**: 008-docker-containerization
**Date**: 2026-01-20

## Prerequisites

- Docker 24+ installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose v2+ (included with Docker Desktop)
- Phase III application code complete and functional
- Environment variables configured in `.env` files

## Quick Start (5 minutes)

### 1. Build Images

```bash
# Build backend image
docker build -t todo-backend -f backend/Dockerfile backend/

# Build frontend image
docker build -t todo-frontend -f frontend/Dockerfile frontend/
```

### 2. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Verify

```bash
# Backend health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Frontend
open http://localhost:3000
```

### 4. Stop Services

```bash
docker-compose down
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key
GEMINI_API_KEY=your-api-key
```

### Frontend (.env)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
```

## Development Mode (Hot Reload)

```bash
# Start with dev profile (mounts source code)
docker-compose --profile dev up

# Changes to source files are reflected immediately
```

## Useful Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start services in background |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f` | Follow logs |
| `docker-compose ps` | List running containers |
| `docker-compose build` | Rebuild images |
| `docker exec -it todo-backend sh` | Shell into backend |
| `docker exec -it todo-frontend sh` | Shell into frontend |

## Image Sizes (Expected)

| Image | Expected Size |
|-------|---------------|
| todo-backend | < 500MB |
| todo-frontend | < 300MB |

Verify with: `docker images | grep todo`

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000 or 3000
lsof -i :8000
lsof -i :3000

# Kill the process or use different ports in docker-compose.yml
```

### Build Failures

```bash
# Clean rebuild
docker-compose build --no-cache

# Check build logs
docker build -t todo-backend -f backend/Dockerfile backend/ 2>&1
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Common issues:
# - Missing environment variables
# - Database connection refused (check DATABASE_URL)
# - Port conflicts
```

## Next Steps

After verifying Docker containers work locally:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement Dockerfiles and docker-compose.yml
3. Test with `docker-compose up`
4. Proceed to Helm chart creation (next Phase IV spec)
