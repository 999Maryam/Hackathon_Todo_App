# SKILL: error-handler-generator

## 1. Purpose
Implement a consistent error handling and logging strategy across backend and frontend.

## 2. Input Parameters
- `Environment`: dev/prod.
- `LogTarget`: console/external-service.

## 3. Code Template

### Backend: Global Exception Handler
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )
```

### Frontend: Fetch Wrapper Error Handling
```typescript
export async function handleError(response: Response) {
  const errorData = await response.json().catch(() => ({}));
  const message = errorData.detail || response.statusText;

  if (response.status === 401) {
    // Handle unauthorized (redirect/logout)
  }

  throw new Error(message);
}
```

## 4. Output
Error handling utilities for both Python/FastAPI and TypeScript/React.

## 5. Usage Example
Input: `LogTarget="Sentry"`
Output: Configured error boundaries and middleware that log to Sentry while showing user-friendly messages.

## 6. Quality Standards
- Never leak stack traces to the client in production.
- Use appropriate HTTP status codes (400, 401, 403, 404, 500).
- Log significant errors with context (user ID, request path).
