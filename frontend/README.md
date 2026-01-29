# Todo AI Chatbot - Frontend

Next.js 16+ frontend for the Todo AI Chatbot application.

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **State Management**: SWR for server state
- **Forms**: React Hook Form + Zod validation
- **Notifications**: react-hot-toast

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

## Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
```

---

## Phase V Components

### Dashboard Components

Located in `src/components/dashboard/`:

#### PriorityBadge
Displays task priority with color-coded badges.

```tsx
import { PriorityBadge } from '@/components/dashboard/PriorityBadge';

<PriorityBadge priority="high" />  // Red badge
<PriorityBadge priority="medium" />  // Yellow badge
<PriorityBadge priority="low" />  // Green badge
```

#### PrioritySelect
Priority dropdown for task forms.

```tsx
import { PrioritySelect } from '@/components/dashboard/PrioritySelect';

<PrioritySelect
  value="medium"
  onChange={(priority) => console.log(priority)}
/>
```

#### DueDateBadge
Displays due date with overdue/upcoming indicators.

```tsx
import { DueDateBadge } from '@/components/dashboard/DueDateBadge';

<DueDateBadge dueDate="2025-01-20T10:00:00" />
// Displays: "Jan 20" with color based on urgency
```

#### DueDatePicker
Calendar picker for selecting due dates.

```tsx
import { DueDatePicker } from '@/components/dashboard/DueDatePicker';

<DueDatePicker
  value={dueDate}
  onChange={(date) => setDueDate(date)}
/>
```

#### TagPicker
Multi-select tag picker with tag management.

```tsx
import { TagPicker } from '@/components/dashboard/TagPicker';

<TagPicker
  selectedTags={[1, 2]}
  onChange={(tagIds) => setSelectedTags(tagIds)}
/>
```

#### RecurringSelect
Toggle and frequency selector for recurring tasks.

```tsx
import { RecurringSelect } from '@/components/dashboard/RecurringSelect';

<RecurringSelect
  isRecurring={true}
  frequency="weekly"
  onIsRecurringChange={(value) => setIsRecurring(value)}
  onFrequencyChange={(freq) => setFrequency(freq)}
/>
```

#### RecurringBadge
Badge displaying recurrence pattern.

```tsx
import { RecurringBadge } from '@/components/dashboard/RecurringBadge';

<RecurringBadge frequency="daily" />  // Shows: "Daily" with repeat icon
```

#### ReminderPicker
Preset dropdown for setting reminders.

```tsx
import { ReminderPicker } from '@/components/dashboard/ReminderPicker';

<ReminderPicker
  value={60}  // 60 minutes before
  hasDueDate={true}
  onChange={(minutes) => setReminderMinutes(minutes)}
/>
```

#### SearchBar
Search input for filtering tasks.

```tsx
import { SearchBar } from '@/components/dashboard/SearchBar';

<SearchBar
  value={searchTerm}
  onChange={(term) => setSearchTerm(term)}
/>
```

#### FilterPanel
Combined filter controls for priority, status, tags, and dates.

```tsx
import { FilterPanel } from '@/components/dashboard/FilterPanel';

<FilterPanel
  filters={filters}
  tags={availableTags}
  onFilterChange={(newFilters) => setFilters(newFilters)}
/>
```

#### SortDropdown
Sort field and order selector.

```tsx
import { SortDropdown } from '@/components/dashboard/SortDropdown';

<SortDropdown
  sortBy="due_date"
  sortOrder="asc"
  onChange={(field, order) => handleSort(field, order)}
/>
```

---

### Hooks

#### useTasks
Fetch and manage tasks with filtering, sorting, and search.

```tsx
import { useTasks } from '@/hooks/useTasks';

const { tasks, isLoading, error, mutate } = useTasks({
  search: 'meeting',
  priority: ['high', 'medium'],
  completed: false,
  tag_ids: [1, 2],
  due_from: '2025-01-01',
  due_to: '2025-01-31',
  sort_by: 'due_date',
  sort_order: 'asc'
});
```

#### useTags
Fetch and manage user tags.

```tsx
import { useTags } from '@/hooks/useTags';

const { tags, isLoading, createTag, deleteTag } = useTags();

// Create a new tag
await createTag('Work');
```

---

### Types

Located in `src/lib/types.ts`:

```tsx
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  is_recurring: boolean;
  recurring_config_id?: number;
  tags: Tag[];
  reminder?: Reminder;
  created_at: string;
  updated_at: string;
}

interface Tag {
  id: number;
  name: string;
  task_count?: number;
}

interface Reminder {
  id: number;
  remind_at: string;
  sent: boolean;
}

type Priority = 'low' | 'medium' | 'high';
type RecurringFrequency = 'daily' | 'weekly' | 'monthly';
```

---

### Validation Schemas

Located in `src/lib/validations.ts`:

```tsx
import { taskFormSchema } from '@/lib/validations';

// Schema includes:
// - title: required, max 200 chars
// - description: optional, max 1000 chars
// - priority: 'low' | 'medium' | 'high'
// - due_date: ISO string, optional
// - tag_ids: number[], optional
// - is_recurring: boolean, optional
// - recurring_frequency: 'daily' | 'weekly' | 'monthly', optional
// - reminder_minutes_before: positive number, optional
```

---

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/page.tsx    # Main dashboard
│   │   ├── chat/page.tsx         # AI chat interface
│   │   ├── auth/                 # Auth pages
│   │   └── layout.tsx
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskModal.tsx
│   │   │   ├── PriorityBadge.tsx
│   │   │   ├── PrioritySelect.tsx
│   │   │   ├── DueDateBadge.tsx
│   │   │   ├── DueDatePicker.tsx
│   │   │   ├── TagPicker.tsx
│   │   │   ├── RecurringSelect.tsx
│   │   │   ├── RecurringBadge.tsx
│   │   │   ├── ReminderPicker.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── FilterPanel.tsx
│   │   │   └── SortDropdown.tsx
│   │   ├── tags/
│   │   │   └── TagManager.tsx
│   │   └── ui/
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       ├── calendar.tsx
│   │       ├── popover.tsx
│   │       └── ...
│   ├── hooks/
│   │   ├── useTasks.ts
│   │   └── useTags.ts
│   └── lib/
│       ├── api.ts
│       ├── types.ts
│       ├── validations.ts
│       └── date-utils.ts
├── tailwind.config.ts
├── next.config.ts
└── package.json
```

---

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Type checking
npx tsc --noEmit
```

---

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [SWR](https://swr.vercel.app/)
