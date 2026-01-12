# Data Model: Premium Todo Frontend UI

**Feature**: 002-todo-frontend-ui
**Date**: 2026-01-11

## Overview

This document defines the frontend data models for the Todo application. These models represent the client-side state and API response/request types.

---

## Core Entities

### Task

Represents a user's todo item as received from and sent to the backend API.

```typescript
interface Task {
  id: string
  user_id: string
  title: string
  description?: string | null
  is_completed: boolean
  created_at: string  // ISO 8601 datetime
  updated_at: string  // ISO 8601 datetime
}
```

**Visual States**:
- `idle`: Normal display state
- `loading`: Operation in progress (show loading indicator)
- `editing`: User is modifying the task
- `deleting`: Task is being removed (exit animation)

**Frontend Extension**:
```typescript
interface TaskWithUIState extends Task {
  _uiState: 'idle' | 'loading' | 'editing' | 'deleting'
  _optimistic?: boolean  // True if awaiting server confirmation
}
```

---

### User Session

Represents the authenticated user's session data from Better Auth.

```typescript
interface UserSession {
  user: {
    id: string
    email: string
    name?: string
    image?: string
  }
  token: string  // JWT for API authorization
}
```

---

### Toast Notification

Represents feedback messages shown to users.

```typescript
interface ToastNotification {
  id: string
  type: 'success' | 'error' | 'info' | 'warning'
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
  duration?: number  // Auto-dismiss time in ms (default: 4000)
}
```

---

### UI State

Application-wide UI state for managing modals, loading, and navigation.

```typescript
interface UIState {
  isTaskModalOpen: boolean
  taskModalMode: 'create' | 'edit'
  editingTaskId: string | null
  isConfirmDialogOpen: boolean
  confirmDialogAction: (() => void) | null
  globalLoading: boolean
}
```

---

## API Request/Response Types

### Create Task

**Request**:
```typescript
interface CreateTaskRequest {
  title: string
  description?: string
}
```

**Response**: `Task`

---

### Update Task

**Request**:
```typescript
interface UpdateTaskRequest {
  title?: string
  description?: string
}
```

**Response**: `Task`

---

### Toggle Complete

**Request**: None (PATCH to endpoint)

**Response**: `Task`

---

### List Tasks

**Request**: None (GET to endpoint)

**Response**:
```typescript
interface TaskListResponse {
  tasks: Task[]
}
```

---

### Error Response

```typescript
interface ApiError {
  status: number
  message: string
  detail?: string
}
```

---

## Form Schemas (Zod Validation)

### Task Form Schema

```typescript
import { z } from 'zod'

export const taskFormSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters'),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
})

export type TaskFormData = z.infer<typeof taskFormSchema>
```

---

## State Management

### Tasks State (React Context or SWR)

```typescript
interface TasksState {
  tasks: TaskWithUIState[]
  isLoading: boolean
  error: string | null

  // Actions
  fetchTasks: () => Promise<void>
  createTask: (data: CreateTaskRequest) => Promise<Task>
  updateTask: (id: string, data: UpdateTaskRequest) => Promise<Task>
  deleteTask: (id: string) => Promise<void>
  toggleComplete: (id: string) => Promise<Task>

  // Optimistic updates
  optimisticCreate: (data: CreateTaskRequest) => string  // Returns temp ID
  optimisticUpdate: (id: string, data: Partial<Task>) => void
  optimisticDelete: (id: string) => void
  rollbackOptimistic: (id: string) => void
}
```

---

## Component Props Interfaces

### TaskItem Props

```typescript
interface TaskItemProps {
  task: Task
  onToggleComplete: (id: string) => void
  onEdit: (task: Task) => void
  onDelete: (id: string) => void
  isLoading?: boolean
}
```

### TaskModal Props

```typescript
interface TaskModalProps {
  isOpen: boolean
  onClose: () => void
  mode: 'create' | 'edit'
  task?: Task  // Required when mode is 'edit'
  onSubmit: (data: TaskFormData) => Promise<void>
}
```

### EmptyState Props

```typescript
interface EmptyStateProps {
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
}
```

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Browser Client                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐       ┌──────────────────┐                │
│  │ UserSession  │──────▶│ API Authorization │                │
│  │ (JWT Token)  │       │ (Bearer Header)   │                │
│  └──────────────┘       └──────────────────┘                │
│         │                        │                          │
│         ▼                        ▼                          │
│  ┌──────────────┐       ┌──────────────────┐                │
│  │  UI State    │       │    Tasks[]       │                │
│  │ (modals,     │       │ (from API)       │                │
│  │  loading)    │       └──────────────────┘                │
│  └──────────────┘                │                          │
│         │                        │                          │
│         └────────────┬───────────┘                          │
│                      ▼                                       │
│              ┌──────────────┐                               │
│              │  Components  │                               │
│              │ (TaskList,   │                               │
│              │  TaskModal)  │                               │
│              └──────────────┘                               │
│                      │                                       │
│                      ▼                                       │
│              ┌──────────────┐                               │
│              │    Toasts    │                               │
│              │ (Feedback)   │                               │
│              └──────────────┘                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

1. **Authentication Flow**:
   - User visits app → Middleware checks session cookie
   - No session → Redirect to `/auth/sign-in`
   - Has session → Allow access, inject JWT into API client

2. **Task CRUD Flow**:
   - User action triggers mutation (create/update/delete)
   - Optimistic update applied immediately
   - API request sent with JWT
   - Success → Confirm optimistic state, show success toast
   - Failure → Rollback optimistic state, show error toast

3. **Real-time State Updates**:
   - SWR handles cache and revalidation
   - `mutate()` for optimistic updates
   - `revalidate()` after mutations for consistency
