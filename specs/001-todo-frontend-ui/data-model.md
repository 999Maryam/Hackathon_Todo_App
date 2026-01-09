# Frontend Data Model: Todo Frontend UI

## Core Entities

### Todo Task
**Definition**: Represents a user's task with properties for managing daily activities

**Fields**:
- `id`: string | number (unique identifier from backend)
- `title`: string (task title, required)
- `description`: string (optional task details)
- `completed`: boolean (completion status, default: false)
- `createdAt`: Date | string (timestamp when task was created)
- `updatedAt`: Date | string (timestamp when task was last updated)
- `dueDate`: Date | string | null (optional deadline for the task)

**Validation Rules**:
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- Completed must be boolean
- createdAt and updatedAt must be valid ISO date strings
- dueDate must be a valid date if provided

**State Transitions**:
- Pending → Completed (when user marks as complete)
- Completed → Pending (when user unmarks completion)

### User Session
**Definition**: Represents the authenticated user state with JWT token for API authentication

**Fields**:
- `userId`: string (user identifier from JWT payload)
- `email`: string (user's email address)
- `expiresAt`: Date (token expiration timestamp)
- `accessToken`: string (JWT token for API authentication)

**Validation Rules**:
- userId must exist and be non-empty
- email must be a valid email format
- expiresAt must be in the future
- accessToken must be a valid JWT format

## API Response Structures

### Task List Response
**Endpoint**: GET /api/{user_id}/tasks
```typescript
{
  tasks: TodoTask[],
  totalCount: number,
  page?: number,
  pageSize?: number
}
```

### Single Task Response
**Endpoint**: GET /api/{user_id}/tasks/{id}
```typescript
{
  task: TodoTask
}
```

### Create Task Request/Response
**Endpoint**: POST /api/{user_id}/tasks
```typescript
// Request
{
  title: string,
  description?: string,
  dueDate?: string
}

// Response
{
  task: TodoTask
}
```

### Update Task Request/Response
**Endpoint**: PUT /api/{user_id}/tasks/{id}
```typescript
// Request
{
  title: string,
  description?: string,
  completed?: boolean,
  dueDate?: string
}

// Response
{
  task: TodoTask
}
```

### Toggle Completion Response
**Endpoint**: PATCH /api/{user_id}/tasks/{id}/complete
```typescript
{
  task: TodoTask
}
```

## UI State Models

### Task Form State
```typescript
{
  title: string,
  description: string,
  dueDate: string | null,
  isSubmitting: boolean,
  errors: {
    title?: string,
    description?: string
  }
}
```

### Task List State
```typescript
{
  tasks: TodoTask[],
  isLoading: boolean,
  isError: boolean,
  errorMessage: string | null,
  filter: 'all' | 'active' | 'completed'
}
```

### Authentication State
```typescript
{
  isAuthenticated: boolean,
  user: UserSession | null,
  isLoading: boolean,
  error: string | null
}
```