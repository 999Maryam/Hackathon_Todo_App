# Quickstart Guide: Todo Frontend UI

## Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (with the 6 required endpoints)
- `BETTER_AUTH_SECRET` environment variable set up

## Project Setup

1. **Clone and Initialize**
   ```bash
   # If this is part of a monorepo, navigate to the frontend directory
   cd frontend

   # Install dependencies
   npm install
   # or
   yarn install
   ```

2. **Environment Configuration**
   ```bash
   # Copy the environment template
   cp .env.example .env.local

   # Edit environment variables
   nano .env.local
   ```

   Required environment variables:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # Backend API base URL
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000  # Better Auth URL
   ```

3. **Better Auth Configuration**
   ```typescript
   // lib/auth.ts
   import { BetterAuthClient } from "@better-auth/react";

   export const authClient = new BetterAuthClient({
     baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL!,
     fetch: globalThis.fetch,
   });
   ```

## Development Server

```bash
# Start the development server
npm run dev
# or
yarn dev

# The application will be available at http://localhost:3000
```

## Key Features Setup

### 1. Protected Routes
All routes except login/register are protected by default:
```typescript
// app/layout.tsx
import { auth } from "@/lib/auth";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth.api.getSession({
    headers: new Headers(),
  });

  if (!session) {
    redirect("/login");
  }

  return <>{children}</>;
}
```

### 2. API Client Configuration
Centralized API client with JWT token attachment:
```typescript
// lib/api.ts
const apiClient = {
  get: async (url: string) => {
    const token = await getAuthToken();
    return fetch(`${API_BASE_URL}${url}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
  },
  // ... other methods
};
```

### 3. Task Management Hooks
SWR-based hooks for data management:
```typescript
// hooks/useTasks.ts
export function useTasks() {
  const { data, error, mutate } = useSWR('/api/tasks', fetcher);

  return {
    tasks: data?.tasks || [],
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
}
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests (if configured)

## Next Steps

1. Implement the authentication flow using Better Auth
2. Create the task list page with SWR integration
3. Build the task creation/editing modal
4. Add responsive design with Tailwind CSS
5. Implement toast notifications for user feedback