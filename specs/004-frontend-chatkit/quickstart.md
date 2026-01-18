# Quickstart Guide: Premium Todo Frontend UI

**Feature**: 002-todo-frontend-ui
**Date**: 2026-01-11

## Prerequisites

- Node.js 18+ installed
- Backend API running at `http://localhost:8000`
- Better Auth configured with JWT plugin

---

## 1. Project Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install shadcn/ui CLI
npx shadcn@latest init
```

When prompted by shadcn init:
- Style: Default
- Base color: Slate
- CSS variables: Yes
- Tailwind config: tailwind.config.ts
- Components location: @/components
- Utils location: @/lib/utils

---

## 2. Install Required shadcn Components

```bash
# Core UI components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add dialog
npx shadcn@latest add checkbox
npx shadcn@latest add sonner
npx shadcn@latest add skeleton
npx shadcn@latest add avatar
npx shadcn@latest add dropdown-menu
```

---

## 3. Install Additional Dependencies

```bash
# Better Auth + Better Auth UI
npm install better-auth @daveyplate/better-auth-ui

# Animation
npm install motion

# Form handling
npm install react-hook-form @hookform/resolvers zod

# Data fetching
npm install swr

# Icons
npm install lucide-react
```

---

## 4. Environment Configuration

Create `.env.local`:
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-shared-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

---

## 5. File Structure Setup

```
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx                 # Welcome page
│   │   ├── auth/
│   │   │   └── [path]/
│   │   │       └── page.tsx         # Auth views
│   │   └── dashboard/
│   │       ├── layout.tsx           # Protected layout
│   │       └── page.tsx             # Dashboard
│   ├── components/
│   │   ├── ui/                      # shadcn components
│   │   ├── providers.tsx            # AuthUIProvider
│   │   ├── welcome/
│   │   │   └── hero-section.tsx
│   │   ├── dashboard/
│   │   │   ├── header.tsx
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   ├── task-modal.tsx
│   │   │   ├── empty-state.tsx
│   │   │   └── add-task-button.tsx
│   │   └── shared/
│   │       └── loading-skeleton.tsx
│   ├── hooks/
│   │   └── use-tasks.ts
│   ├── lib/
│   │   ├── auth.ts                  # Better Auth server config
│   │   ├── auth-client.ts           # Better Auth client
│   │   ├── api.ts                   # API client
│   │   ├── utils.ts                 # shadcn utils
│   │   └── types.ts                 # TypeScript types
│   └── middleware.ts                # Route protection
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 6. Core Configuration Files

### tsconfig.json (path aliases)
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### tailwind.config.ts (custom theme)
```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Glass effect colors
        glass: {
          bg: "rgba(255, 255, 255, 0.7)",
          border: "rgba(255, 255, 255, 0.3)"
        }
      },
      backdropBlur: {
        glass: "16px"
      },
      boxShadow: {
        glass: "0 8px 32px rgba(0, 0, 0, 0.1)"
      }
    }
  },
  plugins: [require("tailwindcss-animate")]
}

export default config
```

---

## 7. Development Workflow

```bash
# Start development server
npm run dev

# Open browser
open http://localhost:3000
```

---

## 8. Testing Checklist

### Visual Testing
- [ ] Welcome page renders with gradient hero
- [ ] Auth pages show beautiful card forms
- [ ] Dashboard displays task list or empty state
- [ ] Responsive layout works on mobile/tablet/desktop
- [ ] Animations are smooth and subtle

### Functional Testing
- [ ] Sign up creates new account
- [ ] Sign in redirects to dashboard
- [ ] Create task shows in list
- [ ] Toggle completion updates task
- [ ] Edit task saves changes
- [ ] Delete task removes from list
- [ ] Sign out redirects to welcome page

### UX Testing
- [ ] Loading states appear during operations
- [ ] Toast notifications show on success/error
- [ ] Confirmation dialog appears before delete
- [ ] Keyboard navigation works throughout
- [ ] Focus states are visible

---

## 9. Common Issues & Solutions

### Issue: "Module not found" for shadcn components
**Solution**: Ensure components are installed:
```bash
npx shadcn@latest add [component-name]
```

### Issue: Auth redirects not working
**Solution**: Check middleware.ts matcher configuration:
```typescript
export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"]
}
```

### Issue: API calls return 401
**Solution**: Verify BETTER_AUTH_SECRET matches backend:
```bash
# Check both .env files have same secret
cat frontend/.env.local | grep BETTER_AUTH_SECRET
cat backend/.env | grep BETTER_AUTH_SECRET
```

### Issue: CORS errors
**Solution**: Backend must allow frontend origin:
```python
# In FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 10. Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

## Key Files to Implement (Priority Order)

1. `lib/auth.ts` + `lib/auth-client.ts` - Better Auth setup
2. `middleware.ts` - Route protection
3. `components/providers.tsx` - AuthUIProvider wrapper
4. `app/layout.tsx` - Root layout with providers
5. `app/page.tsx` - Welcome/landing page
6. `app/auth/[path]/page.tsx` - Auth views
7. `app/dashboard/layout.tsx` - Protected layout
8. `app/dashboard/page.tsx` - Dashboard with task list
9. `components/dashboard/*` - Task components
10. `hooks/use-tasks.ts` - SWR-based task management
