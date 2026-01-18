# Premium Todo Frontend UI Tasks (Hackathon Optimized – Spec 2)
Date: January 11, 2026
Goal: Beautiful welcome page → smooth auth → polished dashboard → full CRUD
Total Tasks: 34
MVP ready around Task 20

# Tasks: Premium Todo Frontend UI (Hackathon-Optimized Version)

**Goal**: Build a visually stunning, modern, responsive Todo app that looks premium and feels delightful  
**MVP Target**: Welcome → Signup/Login → Dashboard + Create/View tasks (ready by ~task 20)  
**Total Tasks**: 34  
**Parallel opportunities**: Marked with [P]  
**Tests**: Manual only (visual + flow testing)

## Phase 1: Setup & Foundation (8 tasks)

- [X] T001 Create Next.js 16+ (App Router) project with TypeScript in frontend/
- [X] T002 Configure tsconfig.json: strict mode + path alias @/* → src/*
- [X] T003 [P] Setup Tailwind CSS + custom theme (primary accent + neutral palette)
- [X] T004 [P] Install & init shadcn/ui (button, card, input, dialog, sonner, skeleton, checkbox, dropdown-menu, avatar)
- [X] T005 [P] Install core dependencies: better-auth, @daveyplate/better-auth-ui, lucide-react, swr, react-hook-form, @hookform/resolvers, zod, motion
- [X] T006 Create root layout with font, Toaster, and global providers in src/app/layout.tsx
- [X] T007 Setup .env.example with BETTER_AUTH_SECRET
- [X] T008 Create basic global styles & CSS variables in src/app/globals.css

**Checkpoint**: Project runs, shadcn components work, Tailwind styles apply

## Phase 2: Beautiful Welcome + Auth Flow (7 tasks)

- [X] T009 Create attractive Welcome / Landing page (/) with hero section, gradient, headline, subtext, strong CTA button in src/app/page.tsx
- [X] T010 Add subtle fade-in / scale animation to welcome hero using motion (framer-motion successor)
- [X] T011 Create elegant Auth wrapper component with glass-morphism / card style (src/components/auth/AuthWrapper.tsx)
- [X] T012 Implement /sign-in page using custom auth + AuthWrapper
- [X] T013 Implement /sign-up page using custom auth + AuthWrapper + link to sign-in
- [X] T014 [P] Add loading states + error toasts during auth actions
- [X] T015 Create protected layout with session check + redirect to /sign-in (src/app/dashboard/layout.tsx)

**Checkpoint**: Welcome page looks premium → can signup/login → redirects to /dashboard (empty for now)

## Phase 3: Dashboard Structure & Task List (9 tasks)

- [X] T016 Create Dashboard Header: app name, user avatar/initials, logout button (src/components/dashboard/DashboardHeader.tsx)
- [X] T017 Create elegant Empty State component (beautiful illustration/message) (src/components/dashboard/EmptyState.tsx)
- [X] T018 Create Loading Skeleton matching task list layout (src/components/shared/TaskListSkeleton.tsx)
- [X] T019 Create typed Task interface & API types (src/lib/types.ts)
- [X] T020 Create Zod schema for task form (src/lib/validations.ts)
- [X] T021 Create centralized typed API client with JWT attachment + error handling (src/lib/api.ts)
- [X] T022 Create useTasks hook with SWR for fetching user tasks (src/hooks/useTasks.ts)
- [X] T023 Create TaskList component with staggered fade-in animation (src/components/dashboard/TaskList.tsx)
- [X] T024 Create simple TaskItem component (title, description preview, checkbox, edit/delete icons) (src/components/dashboard/TaskItem.tsx)

**Checkpoint**: After login → see beautiful dashboard header + empty state or skeleton → real tasks load with stagger animation

## Phase 4: Quick Add + Basic CRUD (7 tasks)

- [X] T025 Create Floating Action Button (+ icon) for new task (src/components/dashboard/AddTaskButton.tsx)
- [X] T026 Create Task Modal (Dialog) with React Hook Form + Zod (src/components/dashboard/TaskModal.tsx)
- [X] T027 Implement task create form + optimistic update + success toast
- [X] T028 Add edit functionality to same modal (pre-fill existing task data)
- [X] T029 Add delete button + confirmation dialog with optimistic delete + toast
- [X] T030 Implement toggle complete with animated checkbox + strikethrough on complete
- [X] T031 Integrate modal + FAB into Dashboard page

**Checkpoint**: MVP complete! Can create, view, complete, edit, delete tasks with nice feedback

## Phase 5: Final Polish & Demo Quality (3–5 tasks – do as time allows)

- [X] T032 Add subtle hover states & button scale micro-interactions
- [X] T033 Fix responsive design across mobile/tablet/desktop (test 320–1920px)
- [X] T034 Add 2–3 extra delight touches (e.g., confetti on first task complete – optional)
- [X] T035 Handle session expiry gracefully (redirect + toast)
- [X] T036 Final visual QA: typography, spacing, colors, mobile touch targets

**Execution Strategy**

1. Complete Phase 1 → 2 (Welcome + Auth) → demo early to judges
2. Phase 3 → get dashboard showing tasks (core value)
3. Phase 4 → full CRUD with delight (what makes it premium)
4. Use remaining time for Phase 5 polish

**Parallel Opportunities**
- T003, T004, T005 can run in parallel
- T012 & T013 (sign-in + sign-up pages) parallel
- T017 & T018 (empty state + skeleton) parallel

**Design Direction for Judges**
- First impression: "Wow" on welcome page (gradient + clean hero)
- Feel: Modern SaaS / productivity app (clean, spacious, subtle animations)
- Polish: Consistent colors, good spacing, responsive everywhere
- Demo flow: Welcome → Sign up (30s) → Dashboard → Add task → Complete → Delete

This version is realistic for 1–2 focused days, gives a **very strong first impression**, and still looks significantly better than most hackathon UIs.