# SKILL: monorepo-integrator

## 1. Purpose
Orchestrate integration between frontend and backend in a monorepo setup, including CORS, proxies, and shared environment management.

## 2. Input Parameters
- `FrontendPort`: default 3000.
- `BackendPort`: default 8000.

## 3. Code Template

### CORS Configuration (FastAPI)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Next.js Proxy Config
```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}
```

## 4. Output
Configuration snippets and scripts for unified development workflow.

## 5. Usage Example
Input: `BackendPort=8001`
Output: Updated CORS settings and proxy rewrites to ensure frontend can communicate with the backend without browser blocks.

## 6. Quality Standards
- Strict origin checks in production.
- Unified environment variable prefixing (e.g., `NEXT_PUBLIC_`).
- Synchronized health checks.
