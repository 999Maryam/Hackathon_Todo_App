# API Contract: Frontend ↔ Backend

**Feature**: 002-todo-frontend-ui
**Date**: 2026-01-11

## Overview

This document defines the API contract between the frontend and backend for the Todo application. The frontend consumes the 6 RESTful endpoints defined in the constitution.

---

## Base Configuration

```typescript
// Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000  // Backend API URL
BETTER_AUTH_SECRET=<shared-secret>          // JWT signing secret
```

---

## Authentication

All protected endpoints require JWT authentication:

```http
Authorization: Bearer <jwt-token>
```

The JWT token is obtained from Better Auth after successful sign-in and contains:
- `sub`: User ID
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

---

## Endpoints

### 1. List Tasks

**Request**:
```http
GET /api/{user_id}/tasks
Authorization: Bearer <token>
```

**Success Response** (200):
```json
[
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Task title",
    "description": "Optional description",
    "is_completed": false,
    "created_at": "2026-01-11T10:30:00Z",
    "updated_at": "2026-01-11T10:30:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Token user_id doesn't match path user_id

---

### 2. Create Task

**Request**:
```http
POST /api/{user_id}/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "New task title",
  "description": "Optional description"
}
```

**Success Response** (201):
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "New task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2026-01-11T10:30:00Z",
  "updated_at": "2026-01-11T10:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body (missing title, title too long)
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Token user_id doesn't match path user_id

---

### 3. Get Single Task

**Request**:
```http
GET /api/{user_id}/tasks/{task_id}
Authorization: Bearer <token>
```

**Success Response** (200):
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "created_at": "2026-01-11T10:30:00Z",
  "updated_at": "2026-01-11T10:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Task belongs to different user
- `404 Not Found`: Task with given ID doesn't exist

---

### 4. Update Task

**Request**:
```http
PUT /api/{user_id}/tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Success Response** (200):
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "is_completed": false,
  "created_at": "2026-01-11T10:30:00Z",
  "updated_at": "2026-01-11T10:35:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Task belongs to different user
- `404 Not Found`: Task with given ID doesn't exist

---

### 5. Delete Task

**Request**:
```http
DELETE /api/{user_id}/tasks/{task_id}
Authorization: Bearer <token>
```

**Success Response** (200 or 204):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Task belongs to different user
- `404 Not Found`: Task with given ID doesn't exist

---

### 6. Toggle Task Completion

**Request**:
```http
PATCH /api/{user_id}/tasks/{task_id}/complete
Authorization: Bearer <token>
```

**Success Response** (200):
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": true,
  "created_at": "2026-01-11T10:30:00Z",
  "updated_at": "2026-01-11T10:40:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Task belongs to different user
- `404 Not Found`: Task with given ID doesn't exist

---

## TypeScript Client Implementation

```typescript
// lib/api.ts
import { authClient } from './auth-client'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

async function getAuthHeaders(): Promise<HeadersInit> {
  const session = await authClient.getSession()
  if (!session?.session?.token) {
    throw new ApiError(401, 'Not authenticated')
  }
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.session.token}`
  }
}

export const tasksApi = {
  async list(userId: string): Promise<Task[]> {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/${userId}/tasks`, { headers })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  },

  async create(userId: string, data: CreateTaskRequest): Promise<Task> {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/${userId}/tasks`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data)
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  },

  async update(userId: string, taskId: string, data: UpdateTaskRequest): Promise<Task> {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data)
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  },

  async delete(userId: string, taskId: string): Promise<void> {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
      headers
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
  },

  async toggleComplete(userId: string, taskId: string): Promise<Task> {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  }
}
```

---

## SWR Integration

```typescript
// hooks/useTasks.ts
import useSWR from 'swr'
import { tasksApi } from '@/lib/api'
import { useSession } from '@/lib/auth-client'

export function useTasks() {
  const { data: session } = useSession()
  const userId = session?.user?.id

  const { data, error, isLoading, mutate } = useSWR(
    userId ? ['tasks', userId] : null,
    () => tasksApi.list(userId!)
  )

  return {
    tasks: data ?? [],
    isLoading,
    error,
    mutate,

    async createTask(data: CreateTaskRequest) {
      // Optimistic update
      const tempTask = { ...data, id: `temp-${Date.now()}`, is_completed: false }
      mutate([...tasks, tempTask], false)

      try {
        const newTask = await tasksApi.create(userId!, data)
        mutate()
        return newTask
      } catch (e) {
        mutate() // Rollback
        throw e
      }
    },

    async toggleComplete(taskId: string) {
      // Optimistic update
      mutate(
        tasks.map(t => t.id === taskId ? { ...t, is_completed: !t.is_completed } : t),
        false
      )

      try {
        const updated = await tasksApi.toggleComplete(userId!, taskId)
        mutate()
        return updated
      } catch (e) {
        mutate() // Rollback
        throw e
      }
    },

    async deleteTask(taskId: string) {
      // Optimistic update
      mutate(tasks.filter(t => t.id !== taskId), false)

      try {
        await tasksApi.delete(userId!, taskId)
        mutate()
      } catch (e) {
        mutate() // Rollback
        throw e
      }
    }
  }
}
```

---

## Error Handling Strategy

| Status | Meaning | Frontend Action |
|--------|---------|-----------------|
| 400 | Bad Request | Show validation error in form |
| 401 | Unauthorized | Redirect to sign-in |
| 403 | Forbidden | Show "Access denied" toast, refresh |
| 404 | Not Found | Show "Task not found" toast, refresh list |
| 500 | Server Error | Show "Server error" toast with retry option |

---

## CORS Configuration

Backend must allow:
```
Access-Control-Allow-Origin: http://localhost:3000 (or frontend URL)
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```
