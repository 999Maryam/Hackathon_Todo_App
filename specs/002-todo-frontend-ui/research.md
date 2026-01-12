# Research: Premium Todo Frontend UI

**Feature**: 002-todo-frontend-ui
**Date**: 2026-01-11
**Status**: Complete

## Technology Stack Decisions

### 1. UI Component Library

**Decision**: shadcn/ui with Tailwind CSS

**Rationale**:
- High-quality, accessible components built on Radix UI primitives
- Copy-paste model allows full customization without dependency lock-in
- Native Tailwind CSS integration matches our styling system
- Includes all needed components: Button, Card, Dialog, Input, Toast (via Sonner)
- Strong TypeScript support
- 1000+ code snippets available for reference

**Alternatives Considered**:
- **Radix UI directly**: More control but requires more styling effort
- **Chakra UI**: Good but different styling paradigm (not Tailwind-native)
- **Headless UI**: Lighter but fewer components

**Implementation Pattern**:
```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { toast } from "sonner"
```

---

### 2. Authentication UI

**Decision**: Better Auth UI (@daveyplate/better-auth-ui)

**Rationale**:
- Pre-built shadcn/ui styled components for authentication
- Seamless integration with Better Auth backend
- Handles sign-in, sign-up, forgot password flows automatically
- Customizable via className props and theming
- Reduces development time significantly

**Alternatives Considered**:
- **Custom auth forms**: More control but significant development effort
- **NextAuth UI**: Different auth system, not compatible with Better Auth

**Implementation Pattern**:
```tsx
// app/auth/[path]/page.tsx
import { AuthView } from "@daveyplate/better-auth-ui"

export default function AuthPage({ params }: { params: { path: string } }) {
  return (
    <main className="container mx-auto flex grow flex-col items-center justify-center">
      <AuthView pathname={params.path} />
    </main>
  )
}
```

**Provider Setup**:
```tsx
// providers.tsx
"use client"
import { AuthUIProvider } from '@daveyplate/better-auth-ui'
import { authClient } from '@/lib/auth-client'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export function Providers({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  return (
    <AuthUIProvider
      authClient={authClient}
      navigate={router.push}
      replace={router.replace}
      onSessionChange={() => router.refresh()}
      Link={Link}
    >
      {children}
    </AuthUIProvider>
  )
}
```

---

### 3. Animation Library

**Decision**: Motion (framer-motion successor) with minimal usage

**Rationale**:
- Production-grade animation library from Framer Motion creators
- Excellent stagger and list animation support
- Small bundle impact when used sparingly
- Native React integration with declarative API
- Variants system for orchestrating complex animations

**Alternatives Considered**:
- **CSS animations only**: Simpler but harder to orchestrate staggered effects
- **React Spring**: Good physics-based animations but steeper learning curve
- **GSAP**: Powerful but larger bundle and imperative API

**Implementation Patterns**:

Staggered list animation:
```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {tasks.map(task => (
    <motion.li key={task.id} variants={item} />
  ))}
</motion.ul>
```

Fade in on mount:
```tsx
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
/>
```

---

### 4. Route Protection Strategy

**Decision**: Next.js Middleware + Layout Wrapper

**Rationale**:
- Middleware handles redirects at edge (fast, before page loads)
- Layout wrapper provides loading states for protected content
- Server-side session check in layouts for additional security
- Clean separation of concerns

**Alternatives Considered**:
- **Client-side only checks**: Slower, flash of unauthorized content
- **Middleware only**: No loading states, harder to debug

**Implementation Pattern**:

Middleware (middleware.ts):
```typescript
import { NextRequest, NextResponse } from "next/server"
import { getSessionCookie } from "better-auth/cookies"

export async function middleware(request: NextRequest) {
  const sessionCookie = getSessionCookie(request)
  const { pathname } = request.nextUrl

  // Redirect authenticated users away from auth pages
  if (sessionCookie && ["/auth/sign-in", "/auth/sign-up"].includes(pathname)) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  // Redirect unauthenticated users to login
  if (!sessionCookie && pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/auth/sign-in", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"]
}
```

Server-side layout check:
```typescript
import { auth } from "@/lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"

export default async function DashboardLayout({ children }) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) redirect("/auth/sign-in")
  return <>{children}</>
}
```

---

### 5. Design System

**Decision**: Clean minimalism with glass-morphism accents

**Rationale**:
- Modern 2025-2026 aesthetic aligned with premium SaaS products
- Glass-morphism adds depth without overwhelming
- Clean base ensures readability and accessibility
- Generous whitespace creates premium feel

**Color Palette**:
```css
/* Primary accent */
--primary: 220 90% 56%;        /* Vibrant blue */
--primary-foreground: 0 0% 100%;

/* Neutrals */
--background: 0 0% 100%;
--foreground: 222 47% 11%;
--muted: 210 40% 96%;
--muted-foreground: 215 16% 47%;

/* Semantic */
--success: 142 76% 36%;
--destructive: 0 84% 60%;

/* Glass effect */
--glass-bg: rgba(255, 255, 255, 0.7);
--glass-border: rgba(255, 255, 255, 0.3);
--glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
```

**Typography**:
- Font: Inter (or system-ui fallback)
- Headings: 600-700 weight, tracking-tight
- Body: 400 weight, leading-relaxed for readability
- Touch targets: minimum 44px

**Spacing**:
- Base unit: 4px (Tailwind default)
- Component padding: 16-24px
- Section gaps: 32-48px
- Container max-width: 1280px

---

### 6. Toast Notifications

**Decision**: Sonner (via shadcn/ui)

**Rationale**:
- Already included in shadcn/ui ecosystem
- Beautiful default styling
- Supports actions, descriptions, and custom content
- Accessible with proper announcements
- Easy promise/async integration

**Implementation**:
```tsx
import { toast } from "sonner"

// Success
toast.success("Task created successfully")

// Error
toast.error("Failed to delete task")

// With action
toast("Task completed", {
  action: {
    label: "Undo",
    onClick: () => undoComplete(taskId)
  }
})

// Promise-based
toast.promise(createTask(data), {
  loading: "Creating task...",
  success: "Task created!",
  error: "Failed to create task"
})
```

---

### 7. Form Handling

**Decision**: React Hook Form + Zod validation

**Rationale**:
- Minimal re-renders for form state
- Type-safe validation with Zod
- Easy integration with shadcn/ui form components
- Native error handling

**Implementation**:
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(200),
  description: z.string().optional()
})

const form = useForm({
  resolver: zodResolver(taskSchema),
  defaultValues: { title: "", description: "" }
})
```

---

### 8. API Communication

**Decision**: Centralized typed fetcher with automatic JWT attachment

**Rationale**:
- Single source of truth for API calls
- Automatic token management via Better Auth client
- Type-safe request/response handling
- Consistent error handling

**Implementation**:
```typescript
// lib/api.ts
import { authClient } from "./auth-client"

const API_BASE = process.env.NEXT_PUBLIC_API_URL

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const session = await authClient.getSession()

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(session?.token && { Authorization: `Bearer ${session.token}` }),
      ...options.headers
    }
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new ApiError(response.status, error.message || "Request failed")
  }

  return response.json()
}
```

---

## Component Architecture

### Page Structure

```
app/
├── page.tsx                    # Welcome/Landing page
├── layout.tsx                  # Root layout with Providers
├── globals.css                 # Tailwind + custom styles
├── auth/
│   └── [path]/
│       └── page.tsx            # Dynamic auth views (sign-in, sign-up, etc.)
├── dashboard/
│   ├── layout.tsx              # Protected layout with session check
│   └── page.tsx                # Task dashboard
└── middleware.ts               # Route protection
```

### Component Hierarchy

```
Providers (AuthUIProvider, Toaster)
├── WelcomePage
│   ├── HeroSection
│   └── CTAButton → /auth/sign-up
├── AuthView (from better-auth-ui)
│   ├── SignInCard
│   └── SignUpCard
└── DashboardLayout (protected)
    └── Dashboard
        ├── Header (user info, logout)
        ├── TaskList
        │   ├── TaskItem (animated)
        │   │   ├── Checkbox (completion toggle)
        │   │   ├── TaskTitle
        │   │   └── TaskActions (edit, delete)
        │   └── EmptyState
        ├── AddTaskButton (FAB)
        └── TaskModal (create/edit)
```

---

## Performance Considerations

1. **Server Components by default**: Only use "use client" when interactivity is required
2. **Skeleton loaders**: Match final layout structure to prevent layout shift
3. **Optimistic updates**: Update UI immediately, rollback on error
4. **Staggered animations**: Use CSS `will-change` sparingly, prefer `transform` and `opacity`
5. **Bundle optimization**: Dynamic imports for modals and non-critical components

---

## Accessibility Checklist

- [ ] All interactive elements have visible focus states
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for normal text)
- [ ] All form inputs have associated labels
- [ ] Error messages are announced to screen readers
- [ ] Modal focus is trapped and managed
- [ ] Keyboard navigation follows logical tab order
- [ ] Touch targets are minimum 44px
- [ ] Loading states are announced with aria-live regions
