# Implementation Plan: Premium Todo Frontend UI

**Branch**: `002-todo-frontend-ui` | **Date**: 2026-01-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-frontend-ui/spec.md`

## Summary

Build a visually stunning, production-grade Todo application frontend designed to impress hackathon judges. The implementation uses Next.js 16+ App Router with TypeScript, shadcn/ui components, Better Auth UI for authentication, and Motion for subtle animations. Key focus areas: premium design aesthetic (glass-morphism + clean minimalism), exceptional UX with optimistic updates, smooth animations, perfect responsiveness, and excellent accessibility.

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Next.js 16+ (App Router), React 19, Tailwind CSS 3.4+, shadcn/ui, Better Auth, Better Auth UI, Motion, SWR, React Hook Form, Zod, Lucide React
**Storage**: N/A (frontend only - consumes backend API)
**Testing**: Manual testing checklist, Lighthouse accessibility audit
**Target Platform**: Web (modern browsers: Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (frontend)
**Performance Goals**: <300ms animations, <5s task creation flow, Lighthouse accessibility 90+
**Constraints**: <100ms visual feedback for all actions, 44px minimum touch targets, WCAG 2.1 AA contrast
**Scale/Scope**: Single user per session, ~100 tasks display, 3 main routes (/, /auth/*, /dashboard)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec created first, plan follows spec |
| II. Separation of Concerns | PASS | Frontend-only, consumes backend API via REST |
| III. Security - Stateless JWT | PASS | JWT from Better Auth attached to all API requests |
| IV. Multi-User Data Isolation | PASS | API includes user_id, backend enforces isolation |
| V. Reliable Persistent Storage | N/A | Frontend only - no direct DB access |
| VI. Modern, Responsive, Maintainable | PASS | TypeScript, Tailwind, responsive design, ESLint |

**Constitution Gate**: PASSED

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-frontend-ui/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology research and decisions
├── data-model.md        # Frontend data models and types
├── quickstart.md        # Setup and development guide
├── contracts/
│   └── api-contract.md  # Frontend ↔ Backend API contract
└── checklists/
    └── requirements.md  # Spec validation checklist
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css              # Global styles + Tailwind
│   │   ├── layout.tsx               # Root layout with providers
│   │   ├── page.tsx                 # Welcome/landing page
│   │   ├── auth/
│   │   │   └── [path]/
│   │   │       └── page.tsx         # Dynamic auth views
│   │   └── dashboard/
│   │       ├── layout.tsx           # Protected layout
│   │       └── page.tsx             # Task dashboard
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components
│   │   ├── providers.tsx            # AuthUIProvider wrapper
│   │   ├── welcome/
│   │   │   └── hero-section.tsx     # Landing page hero
│   │   ├── dashboard/
│   │   │   ├── header.tsx           # Dashboard header (user, logout)
│   │   │   ├── task-list.tsx        # Task list container
│   │   │   ├── task-item.tsx        # Individual task with animations
│   │   │   ├── task-modal.tsx       # Create/edit modal
│   │   │   ├── empty-state.tsx      # No tasks state
│   │   │   └── add-task-button.tsx  # FAB for adding tasks
│   │   └── shared/
│   │       └── loading-skeleton.tsx # Skeleton loaders
│   ├── hooks/
│   │   └── use-tasks.ts             # SWR-based task management
│   ├── lib/
│   │   ├── auth.ts                  # Better Auth server config
│   │   ├── auth-client.ts           # Better Auth client
│   │   ├── api.ts                   # Typed API client
│   │   ├── utils.ts                 # shadcn utilities
│   │   └── types.ts                 # TypeScript interfaces
│   └── middleware.ts                # Route protection
├── public/                          # Static assets
├── tailwind.config.ts               # Tailwind + custom theme
├── tsconfig.json                    # TypeScript config
├── next.config.js                   # Next.js config
└── package.json
```

**Structure Decision**: Web application with Next.js App Router. Single `frontend/` directory containing all source code with `src/` subdirectory for organized file structure. Path alias `@/*` maps to `./src/*`.

## Architecture Overview

### Component Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  middleware.ts                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Session Cookie Check → Redirect Logic                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    RootLayout                            │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │              AuthUIProvider                        │  │   │
│  │  │  ┌─────────────────────────────────────────────┐  │  │   │
│  │  │  │                 Toaster                      │  │  │   │
│  │  │  └─────────────────────────────────────────────┘  │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│           │                                                      │
│           ├───────────────┬───────────────┬────────────────┐    │
│           ▼               ▼               ▼                │    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │    │
│  │   Welcome   │  │  AuthView   │  │  DashboardLayout    │ │    │
│  │   (/)      │  │ (/auth/*)   │  │  (/dashboard)       │ │    │
│  │             │  │             │  │  ┌───────────────┐  │ │    │
│  │ HeroSection │  │ SignIn/Up   │  │  │    Header     │  │ │    │
│  │ CTAButton   │  │ ForgotPwd   │  │  ├───────────────┤  │ │    │
│  └─────────────┘  └─────────────┘  │  │   TaskList    │  │ │    │
│                                     │  │  ┌─────────┐  │  │ │    │
│                                     │  │  │TaskItem │  │  │ │    │
│                                     │  │  └─────────┘  │  │ │    │
│                                     │  ├───────────────┤  │ │    │
│                                     │  │ AddTaskButton │  │ │    │
│                                     │  └───────────────┘  │ │    │
│                                     │       │             │ │    │
│                                     │       ▼             │ │    │
│                                     │  ┌───────────────┐  │ │    │
│                                     │  │  TaskModal    │  │ │    │
│                                     │  └───────────────┘  │ │    │
│                                     └─────────────────────┘ │    │
│                                                              │    │
└──────────────────────────────────────────────────────────────┘   │
```

### User Flow Diagram

```
┌──────────┐    No Session    ┌──────────────┐
│  User    │ ───────────────▶ │   Welcome    │
│  Visits  │                  │   Page (/)   │
└──────────┘                  └──────────────┘
     │                              │
     │ Has Session                  │ Click CTA
     ▼                              ▼
┌──────────────┐              ┌──────────────┐
│  Dashboard   │ ◀─ Success ─ │   Sign Up    │
│  (/dashboard)│              │  /auth/sign-up│
└──────────────┘              └──────────────┘
     │                              │
     │                              │ Existing User
     │                              ▼
     │                        ┌──────────────┐
     │                        │   Sign In    │
     │                        │ /auth/sign-in│
     │                        └──────────────┘
     │                              │
     │                              │ Success
     │◀─────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────┐
│           Dashboard Actions            │
│  • View tasks (with stagger animation) │
│  • Create task (modal + optimistic)    │
│  • Toggle complete (animated checkbox) │
│  • Edit task (modal + save)            │
│  • Delete task (confirm + animate out) │
│  • Sign out → Back to Welcome          │
└────────────────────────────────────────┘
```

## Design System

### Visual Aesthetic

**Primary Style**: Clean minimalism with glass-morphism accents
- White/light backgrounds with subtle gradients
- Glass effect on cards and modals (`backdrop-blur`, semi-transparent backgrounds)
- Soft shadows for depth (`shadow-lg`, `shadow-xl`)
- Rounded corners (`rounded-xl`, `rounded-2xl`)
- Generous whitespace and padding

### Color Palette

```css
/* Core Colors */
--primary: hsl(220, 90%, 56%);           /* Vibrant blue */
--primary-foreground: hsl(0, 0%, 100%);  /* White text on primary */

/* Backgrounds */
--background: hsl(0, 0%, 100%);          /* Pure white */
--card: hsl(0, 0%, 100%);                /* Card background */
--muted: hsl(210, 40%, 96%);             /* Muted sections */

/* Text */
--foreground: hsl(222, 47%, 11%);        /* Primary text */
--muted-foreground: hsl(215, 16%, 47%);  /* Secondary text */

/* Semantic */
--success: hsl(142, 76%, 36%);           /* Green */
--destructive: hsl(0, 84%, 60%);         /* Red */

/* Glass Effect */
--glass-bg: rgba(255, 255, 255, 0.7);
--glass-border: rgba(255, 255, 255, 0.3);
```

### Typography

- **Font Family**: Inter (with system fallback)
- **Headings**: 600-700 weight, tracking-tight
- **Body**: 400 weight, leading-relaxed
- **Small text**: 14px minimum for readability

### Spacing Scale

- Base: 4px (Tailwind default)
- Components: 16-24px padding
- Sections: 32-48px gap
- Container: max-w-4xl (896px) for dashboard

## Animation Strategy

### Principles

1. **Subtlety**: Animations enhance, not distract
2. **Performance**: Use `transform` and `opacity` only
3. **Duration**: 200-300ms for micro-interactions
4. **Easing**: `ease-out` for entries, `ease-in` for exits

### Animation Catalog

| Element | Animation | Duration | Trigger |
|---------|-----------|----------|---------|
| Page load | Fade in | 300ms | Mount |
| Task list | Stagger fade + slide up | 100ms per item | Load |
| Task item appear | Scale + fade | 200ms | Create |
| Task item exit | Fade + slide right | 200ms | Delete |
| Checkbox | Scale bounce | 150ms | Toggle |
| Modal | Scale + fade overlay | 200ms | Open/close |
| Button hover | Scale 1.02 | 100ms | Hover |
| Toast | Slide in from right | 200ms | Show |

### Motion Code Patterns

```tsx
// List stagger
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.2 } }
}

// Checkbox completion
const checkmark = {
  unchecked: { scale: 0, opacity: 0 },
  checked: { scale: 1, opacity: 1, transition: { type: "spring", stiffness: 300 } }
}
```

## Implementation Phases

### Phase 1: Foundation (Priority: P0)

1. Project setup with Next.js 16+ App Router
2. Tailwind CSS configuration with custom theme
3. shadcn/ui initialization and core components
4. Better Auth client and server configuration
5. Middleware for route protection
6. AuthUIProvider setup

### Phase 2: Welcome & Auth (Priority: P1)

1. Welcome/landing page with hero section
2. Gradient background with subtle animation
3. CTA button linking to sign-up
4. Auth dynamic route with AuthView component
5. Styled auth cards with glass effect

### Phase 3: Dashboard Core (Priority: P1)

1. Dashboard layout with session check
2. Header component (user info, logout)
3. Task list container with loading skeleton
4. Empty state component
5. Add task button (FAB style)

### Phase 4: Task Components (Priority: P1)

1. TaskItem with completion toggle
2. Animated checkbox with checkmark
3. TaskModal for create/edit
4. Confirmation dialog for delete
5. Form validation with Zod

### Phase 5: Data Layer (Priority: P1)

1. API client with JWT attachment
2. SWR hook for tasks (useTasks)
3. Optimistic updates for all operations
4. Error handling and rollback
5. Toast notifications integration

### Phase 6: Animations & Polish (Priority: P2)

1. Staggered list animations
2. Task appear/disappear animations
3. Page transition animations
4. Micro-interactions (hover, focus)
5. Skeleton loader animations

### Phase 7: Accessibility & Responsiveness (Priority: P2)

1. Keyboard navigation testing
2. ARIA labels on all interactive elements
3. Focus management in modals
4. Mobile responsive adjustments
5. Touch target verification (44px)

### Phase 8: Final Polish (Priority: P3)

1. Lighthouse audit and fixes
2. Performance optimization
3. Cross-browser testing
4. Visual QA on all breakpoints
5. Edge case handling

## Testing Strategy

### Manual Testing Checklist

**Authentication Flow**:
- [ ] Welcome page displays correctly
- [ ] Sign-up creates account and redirects to dashboard
- [ ] Sign-in authenticates and redirects to dashboard
- [ ] Invalid credentials show error message
- [ ] Sign-out returns to welcome page
- [ ] Protected routes redirect unauthenticated users

**Task Operations**:
- [ ] Task list loads with skeleton, then shows tasks
- [ ] Empty state shows when no tasks
- [ ] Create task adds to list immediately (optimistic)
- [ ] Edit task updates in place
- [ ] Delete task shows confirmation, then removes
- [ ] Toggle complete animates checkbox
- [ ] Error shows toast and rolls back

**Responsiveness**:
- [ ] Mobile layout (< 640px) works correctly
- [ ] Tablet layout (640-1024px) works correctly
- [ ] Desktop layout (> 1024px) works correctly
- [ ] Touch targets are 44px minimum on mobile

**Accessibility**:
- [ ] Tab navigation works throughout
- [ ] Focus states are visible
- [ ] Screen reader announces correctly
- [ ] Color contrast meets WCAG AA

**Performance**:
- [ ] Animations are smooth (60fps)
- [ ] No layout shifts during loading
- [ ] Page loads feel instant

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Better Auth UI compatibility issues | Low | Medium | Use custom auth forms as fallback |
| Animation performance on low-end devices | Medium | Low | Reduce motion for prefer-reduced-motion |
| API latency affecting UX | Medium | Medium | Aggressive optimistic updates |
| shadcn/ui version conflicts | Low | Low | Pin versions in package.json |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task creation time | < 5 seconds | Manual timing |
| Animation smoothness | 60 fps | Chrome DevTools |
| Accessibility score | 90+ | Lighthouse |
| Mobile usability | Full functionality | Manual testing |
| Judge impression | "Production-ready" | Visual quality review |

## Complexity Tracking

No constitutional violations. All design decisions align with established principles.

## Related Documents

- [Specification](./spec.md)
- [Research](./research.md)
- [Data Model](./data-model.md)
- [API Contract](./contracts/api-contract.md)
- [Quickstart Guide](./quickstart.md)
