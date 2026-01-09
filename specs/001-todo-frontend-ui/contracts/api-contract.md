# API Contract: Todo Frontend UI

## Overview
This contract defines the API interactions between the frontend Todo application and the backend service. The frontend will consume the 6 required REST endpoints with proper JWT authentication.

## Authentication
All API requests must include a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The JWT token is obtained through Better Auth's authentication flow and should be automatically refreshed when expired.

## API Endpoints

### 1. List Tasks
**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieve all tasks for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID

**Response**:
```json
{
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": true,
      "createdAt": "2023-01-01T00:00:00.000Z",
      "updatedAt": "2023-01-01T00:00:00.000Z",
      "dueDate": "2023-01-01T00:00:00.000Z"
    }
  ],
  "totalCount": 10
}
```

**Status Codes**:
- `200`: Success
- `401`: Unauthorized (invalid/expired token)
- `403`: Forbidden (attempting to access another user's tasks)
- `500`: Internal server error

### 2. Create Task
**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new task for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "dueDate": "2023-01-01T00:00:00.000Z"
}
```

**Response**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": false,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "dueDate": "2023-01-01T00:00:00.000Z"
  }
}
```

**Status Codes**:
- `201`: Created
- `400`: Bad request (validation error)
- `401`: Unauthorized
- `403`: Forbidden
- `500`: Internal server error

### 3. Get Single Task
**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieve a specific task for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID
- `id`: String - The task ID

**Response**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "dueDate": "2023-01-01T00:00:00.000Z"
  }
}
```

**Status Codes**:
- `200`: Success
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Task not found
- `500`: Internal server error

### 4. Update Task
**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update an existing task for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID
- `id`: String - The task ID

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "completed": true,
  "dueDate": "2023-01-01T00:00:00.000Z"
}
```

**Response**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "dueDate": "2023-01-01T00:00:00.000Z"
  }
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad request (validation error)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Task not found
- `500`: Internal server error

### 5. Delete Task
**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Delete a task for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID
- `id`: String - The task ID

**Response**: Empty body

**Status Codes**:
- `204`: Deleted successfully
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Task not found
- `500`: Internal server error

### 6. Toggle Task Completion
**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle the completion status of a task for the authenticated user

**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `user_id`: String - The authenticated user's ID
- `id`: String - The task ID

**Response**:
```json
{
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00.000Z",
    "updatedAt": "2023-01-01T00:00:00.000Z",
    "dueDate": "2023-01-01T00:00:00.000Z"
  }
}
```

**Status Codes**:
- `200`: Success
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Task not found
- `500`: Internal server error

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

## Frontend Integration Patterns

### Authentication Token Retrieval
```typescript
async function getAuthToken(): Promise<string> {
  // Get token from Better Auth session
  const session = await authClient.getSession();
  return session?.token || '';
}
```

### API Client Implementation
```typescript
const apiClient = {
  get: async (url: string) => {
    const token = await getAuthToken();
    const response = await fetch(`${API_BASE_URL}${url}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  post: async (url: string, data: any) => {
    const token = await getAuthToken();
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  // Similar implementations for put, delete, patch
};
```