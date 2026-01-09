# Todo Frontend Application

A responsive, authenticated todo application built with Next.js 16+, TypeScript, and Tailwind CSS. This application provides core task management functionality with JWT-based authentication integration via Better Auth.

## Features

- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop devices
- **Authentication**: Secure login and registration with Better Auth and JWT tokens
- **Task Management**: Create, read, update, delete, and toggle completion status of tasks
- **Real-time Feedback**: Loading states, success toasts, and error messages
- **Type Safety**: Full TypeScript support with comprehensive type definitions
- **Modern UI**: Clean, minimalist interface with intuitive user experience

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **Data Fetching**: SWR for server-side rendering and caching
- **Forms**: React Hook Form with Zod validation
- **Notifications**: React Hot Toast
- **UI Components**: Custom built with accessibility in mind

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (with the 6 required endpoints)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Configure environment variables:
   ```bash
   cp .env.local.example .env.local
   ```

   Update the values in `.env.local`:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   ```

### Running the Application

1. Development mode:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

2. Production build:
   ```bash
   npm run build
   npm run start
   # or
   yarn build
   yarn start
   ```

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── (auth)/          # Authentication-related pages
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/       # Main dashboard with task list
│   ├── layout.tsx       # Root layout with auth protection
│   ├── page.tsx         # Home page (redirects to dashboard if authenticated)
│   └── globals.css      # Global styles
├── components/          # Reusable UI components
│   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   ├── auth/            # Authentication components
│   ├── tasks/           # Task-related components (TaskItem, TaskModal, etc.)
│   └── layout/          # Layout components (Header, Sidebar, etc.)
├── lib/                 # Utility functions and constants
│   ├── api.ts           # Centralized API client utility
│   ├── auth.ts          # Authentication helpers
│   └── types.ts         # TypeScript type definitions
├── hooks/               # Custom React hooks
│   ├── useTasks.ts      # Task management hooks
│   └── useAuth.ts       # Authentication state hooks
├── public/              # Static assets
└── styles/              # Additional style files if needed
```

## API Integration

The application consumes the following 6 REST API endpoints from the backend:

- `GET /api/{user_id}/tasks` - List all tasks for authenticated user
- `POST /api/{user_id}/tasks` - Create a new task for authenticated user
- `GET /api/{user_id}/tasks/{id}` - Get a single task (verify ownership)
- `PUT /api/{user_id}/tasks/{id}` - Update a task (verify ownership)
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task (verify ownership)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

All API requests automatically include the JWT token in the `Authorization: Bearer <token>` header.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.