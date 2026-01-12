# Component Tree - Premium Todo App (Phase 3)

## Visual Component Hierarchy

```
app/
└── dashboard/
    └── page.tsx (DashboardPage)
        ├── DashboardHeader
        │   ├── CheckSquare (icon)
        │   ├── h1 (TaskFlow branding)
        │   └── DropdownMenu
        │       ├── DropdownMenuTrigger
        │       │   └── Avatar
        │       │       └── AvatarFallback (user initials)
        │       └── DropdownMenuContent
        │           ├── DropdownMenuLabel (user info)
        │           ├── DropdownMenuItem (Profile)
        │           └── DropdownMenuItem (Logout)
        │
        └── main
            ├── h2 (Page title)
            ├── p (Task count)
            ├── [Error State] (conditional)
            │
            └── [Loading State]
                └── TaskListSkeleton
                    └── Card × 5
                        ├── Skeleton (checkbox)
                        ├── Skeleton (title)
                        ├── Skeleton (description)
                        └── Skeleton (actions)
            │
            └── [OR Loaded State]
                └── TaskList
                    ├── EmptyState (if no tasks)
                    │   ├── CheckCircle2 (icon)
                    │   ├── Sparkles (accent)
                    │   ├── h2 (heading)
                    │   ├── p (message)
                    │   └── button (CTA - optional)
                    │
                    └── [OR] TaskItem × N (with motion)
                        ├── Card
                        │   ├── Checkbox (completion toggle)
                        │   ├── div (content)
                        │   │   ├── h3 (title)
                        │   │   ├── p (description)
                        │   │   └── p (metadata)
                        │   └── div (actions)
                        │       ├── Button (Edit icon)
                        │       └── Button (Delete icon)
                        └── motion.div (animation wrapper)
```

---

## Component Relationships

### Data Flow

```
Dashboard Page
│
├── useAuth() ──────────────> user
│
└── useTasks(user.id) ─────> tasks, isLoading, isError
                             │
                             ├── SWR cache
                             ├── API client
                             └── Optimistic updates
                                 │
                                 ├── createTask()
                                 ├── updateTask()
                                 ├── deleteTask()
                                 └── toggleComplete()
```

### Event Flow

```
User Interactions
│
├── Toggle Checkbox ────> handleToggleComplete() ────> useTasks.toggleComplete()
│                                                       │
│                                                       ├── Optimistic update
│                                                       ├── API call
│                                                       └── Toast notification
│
├── Click Edit ─────────> handleEdit() ──────────────> Console log (Phase 4: Modal)
│
├── Click Delete ───────> handleDelete() ─────────────> useTasks.deleteTask()
│                                                       │
│                                                       ├── Optimistic remove
│                                                       ├── API call
│                                                       └── Toast notification
│
└── Click Logout ───────> DashboardHeader.handleLogout()
                          │
                          ├── useAuth.logout()
                          ├── Clear localStorage
                          └── Navigate to '/'
```

---

## State Management

### Local Component State
- **DashboardHeader**: None (stateless, uses hooks)
- **EmptyState**: None (stateless presentation)
- **TaskListSkeleton**: None (stateless presentation)
- **TaskList**: None (receives props, manages animation state)
- **TaskItem**: None (controlled by parent)

### Hook State (useTasks)
```javascript
{
  tasks: Task[],           // From SWR cache
  isLoading: boolean,      // SWR loading state
  isError: boolean,        // SWR error state
  error: any,              // Error object
  // Methods for mutations
  refresh(),
  createTask(),
  updateTask(),
  deleteTask(),
  toggleComplete()
}
```

### Hook State (useAuth)
```javascript
{
  user: User | null,       // From localStorage + server
  isLoading: boolean,      // Auth check loading
  isAuthenticated: boolean,// Computed from user
  // Methods
  login(),
  register(),
  logout(),
  refreshUser()
}
```

---

## Props Interface

### DashboardHeader
```typescript
// No props - uses hooks internally
```

### EmptyState
```typescript
interface EmptyStateProps {
  onCreateClick?: () => void; // Optional CTA handler
}
```

### TaskListSkeleton
```typescript
interface TaskListSkeletonProps {
  count?: number; // Default: 5
}
```

### TaskList
```typescript
interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
  onCreateClick?: () => void;
}
```

### TaskItem
```typescript
interface TaskItemProps {
  task: Task;
  onToggleComplete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}
```

---

## Animation Flow

### TaskList Stagger Animation

```
TaskList Container
│
├── Initial State: hidden (opacity: 0)
│
└── Animate to: visible (opacity: 1)
    │
    └── Stagger children (0.1s delay each)
        │
        ├── Task 1 ──> hidden: {opacity: 0, y: 20}
        │              visible: {opacity: 1, y: 0, duration: 0.4s}
        │
        ├── Task 2 ──> (100ms delay) same animation
        │
        ├── Task 3 ──> (200ms delay) same animation
        │
        └── Task N ──> ((N-1)*100ms delay) same animation
```

### Loading to Content Transition

```
Page Load
│
├── Show TaskListSkeleton (pulse animation)
│   └── Skeleton pulse: opacity 0.5 → 1 → 0.5 (repeat)
│
└── Data arrives
    │
    ├── Unmount TaskListSkeleton
    │
    └── Mount TaskList
        └── Trigger stagger animation
```

---

## Responsive Breakpoints

### Mobile (< 640px)
- Single column layout
- Smaller text sizes (text-base → text-lg)
- Reduced padding (p-4)
- Action buttons always visible (no hover needed)
- Hamburger menu for user dropdown

### Tablet (640px - 1024px)
- Optimized spacing (p-6)
- Medium text sizes (text-lg → text-xl)
- Hover states enabled
- Full dropdown menu

### Desktop (> 1024px)
- Maximum content width (max-w-4xl)
- Large text sizes (text-xl → text-2xl)
- Full hover interactions
- Optimal line lengths for readability

---

## Accessibility Features

### Keyboard Navigation
```
Tab Order:
1. Dashboard Header → Avatar button
2. Task 1 → Checkbox
3. Task 1 → Edit button
4. Task 1 → Delete button
5. Task 2 → Checkbox
   ... (repeat for each task)
```

### Screen Reader Announcements
- Checkbox: "Mark task '[title]' as complete/incomplete"
- Edit button: "Edit task"
- Delete button: "Delete task"
- User avatar: Accessible via dropdown trigger
- Empty state: Announced with heading hierarchy

### Focus Management
- Focus rings on all interactive elements
- Skip links (future enhancement)
- Modal focus trap (Phase 4)

---

## Performance Characteristics

### Initial Load
1. Server renders dashboard layout
2. Client hydrates with user data
3. Show TaskListSkeleton
4. Fetch tasks via SWR
5. Animate in TaskList

### Subsequent Loads
1. SWR serves from cache immediately
2. Background revalidation
3. No loading skeleton (instant display)

### Optimistic Updates
1. User action triggers handler
2. Local state updates instantly
3. API call happens in background
4. On success: Update with server data
5. On error: Rollback + show error toast

---

## Future Extensions (Phase 4+)

### Planned Components
- TaskModal (create/edit form)
- ConfirmationDialog (delete confirmation)
- FloatingActionButton (quick add)
- TaskFilters (all/pending/completed)
- TaskSearch (filter by title)

### Planned Hooks
- useTaskModal (modal state management)
- useTaskFilters (filter state)
- useDebounce (search optimization)

### Planned Animations
- Modal slide-in from bottom (mobile)
- Modal fade + scale (desktop)
- Confetti on first task completion
- Checkbox bounce on toggle

---

This component tree provides a complete map of the Phase 3 implementation, showing how all pieces fit together to create a cohesive, performant dashboard experience.
