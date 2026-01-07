# SKILL: auth-flow-generator

## 1. Purpose
Generate a complete authentication flow integrating Better Auth on the frontend with FastAPI JWT middleware on the backend, secured by protected routes.

## 2. Input Parameters
- `AuthProvider`: Strategy (e.g., "password", "github").
- `ProtectedRoutes`: List of frontend paths requiring auth.
- `TokenExpiry`: Minutes for JWT validity.

## 3. Code Template

### Backend: FastAPI Middleware
```python
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings

async def verify_jwt(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid authentication token required"
        )

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")
```

### Frontend: Better Auth Setup
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    plugins: [
        // JWT plugin configuration
    ]
});

export const { signIn, signUp, useSession, signOut } = authClient;
```

## 4. Output
Two files: a FastAPI security dependency and a TypeScript auth configuration file for Better Auth.

## 5. Usage Example
Input: `ProtectedRoutes=["/dashboard", "/profile"]`
Output: Middleware to lock down backend endpoints and a frontend provider to redirect unauthenticated users to `/login`.

## 6. Quality Standards
- Use secure `HS256` or `RS256` algorithms.
- Token validation must occur on every protected request.
- Frontend must handle "expired session" events gracefully by clearing local state.
- Rate limiting should be applied to `signIn` and `signUp` routes.
