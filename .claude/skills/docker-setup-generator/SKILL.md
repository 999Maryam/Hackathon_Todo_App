# SKILL: docker-setup-generator

## 1. Purpose
Generate multi-stage Dockerfiles and docker-compose configurations for development and production.

## 2. Input Parameters
- `ServiceStack`: (e.g., FastAPI + Postgres + React).
- `Context`: dev/prod.

## 3. Code Template

### Backend Multi-Stage Dockerfile
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
services:
  api:
    build: ./backend
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db]
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app
```

## 4. Output
Dockerfile, .dockerignore, and docker-compose.yml files.

## 5. Usage Example
Input: `ServiceStack="Fullstack"`
Output: A setup where the entire app can be started with `docker-compose up`.

## 6. Quality Standards
- Multi-stage builds for smaller images.
- Least privilege (non-root users where possible).
- Health checks for database and API services.
