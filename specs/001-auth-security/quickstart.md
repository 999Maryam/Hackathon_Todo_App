# Quickstart Guide: Authentication & Security Implementation

## Overview
This guide provides a step-by-step approach to implementing the JWT-based authentication system using Better Auth for the todo application.

## Prerequisites
- Node.js 18+ and npm/yarn for frontend
- Python 3.11+ with pip for backend
- Neon Serverless PostgreSQL database
- BETTER_AUTH_SECRET environment variable (same for both services)

## Phase 1: Frontend Authentication Setup

### Step 1: Install Better Auth
```bash
npm install better-auth @better-auth/react
```

### Step 2: Configure Better Auth with JWT Plugin
```typescript
// frontend/src/lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d",
    }),
  ],
});
```

### Step 3: Create Authentication Context
```typescript
// frontend/src/hooks/useAuth.ts
import { useSession } from "@better-auth/react";

export const useAuth = () => {
  const { session, signIn, signOut } = useSession();

  return {
    user: session?.user,
    isAuthenticated: !!session,
    isLoading: session === undefined,
    signIn,
    signOut,
    getToken: () => session?.accessToken,
  };
};
```

### Step 4: Create API Client with JWT Attachment
```typescript
// frontend/src/utils/apiClient.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('better-auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
```

## Phase 2: Backend JWT Verification Setup

### Step 1: Install PyJWT and Dependencies
```bash
pip install pyjwt[crypto] python-dotenv
```

### Step 2: Create JWT Handler
```python
# backend/src/auth/jwt_handler.py
import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token and return payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def verify_user_id_from_token(token: str, expected_user_id: str) -> bool:
    """Verify that the token's user_id matches the expected user_id"""
    payload = decode_token(token)
    token_user_id = payload.get("sub")
    return token_user_id == expected_user_id
```

### Step 3: Create FastAPI Dependency
```python
# backend/src/api/deps.py
from fastapi import Depends, HTTPException, status, Request
from typing import Dict, Optional
from auth.jwt_handler import decode_token

async def get_current_user(request: Request) -> Dict:
    """Dependency to get current user from JWT token"""
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return {"user_id": user_id}
```

## Phase 3: Protected Endpoints with Ownership Enforcement

### Step 1: Update Task Endpoints
```python
# backend/src/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from api.deps import get_current_user
from models.task import Task
from services.task_service import (
    get_user_tasks,
    create_task_for_user,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)

router = APIRouter()

@router.get("/{user_id}/tasks")
def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other users' tasks"
        )

    return get_user_tasks(db, user_id)

@router.post("/{user_id}/tasks")
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other users' tasks"
        )

    return create_task_for_user(db, user_id, task_data)
```

## Phase 4: Environment Variables Setup

### Backend (.env)
```env
BETTER_AUTH_SECRET=your-super-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-super-secret-key-here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Important**: Use the same BETTER_AUTH_SECRET value in both services.

## Phase 5: Protected Route Component

### Create Protected Route Component
```tsx
// frontend/src/components/auth/ProtectedRoute.tsx
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { ReactNode, useEffect } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return <>{children}</>;
}
```

## Phase 6: Testing the Implementation

### Test Authentication Flow
1. Register a new user
2. Verify JWT token is received and stored
3. Call protected API endpoints with token
4. Verify 401 responses for missing/invalid tokens
5. Test cross-user access attempts (should return 403/404)

### Test Multi-User Isolation
1. Create two different user accounts
2. Each user creates tasks
3. Verify each user only sees their own tasks
4. Attempt to access other user's tasks (should fail)

## Troubleshooting

### Common Issues:
- **401 Unauthorized**: Check BETTER_AUTH_SECRET matches between frontend and backend
- **403 Forbidden**: Verify user_id in JWT matches the requested resource
- **Token Expiry**: Implement proper token refresh handling if needed
- **Database Connection**: Ensure Neon PostgreSQL connection is properly configured

### Debugging Steps:
1. Verify environment variables are set correctly
2. Check that JWT tokens are properly attached to requests
3. Confirm user_id in token matches the requested resource
4. Validate that BETTER_AUTH_SECRET is identical in both services