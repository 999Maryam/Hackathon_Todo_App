/**
 * Type definitions for the Premium Todo App
 * Phase V: Extended with priority, due dates, tags, recurring, and reminders
 */

// User types
export interface User {
  id: string;
  email: string;
  name: string;
  created_at?: string;
}

// Auth types
export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
}

// === Phase V: Priority Types ===
export type Priority = 'high' | 'medium' | 'low';

export const PRIORITY_OPTIONS: { value: Priority; label: string; color: string }[] = [
  { value: 'high', label: 'High', color: 'red' },
  { value: 'medium', label: 'Medium', color: 'yellow' },
  { value: 'low', label: 'Low', color: 'green' },
];

// === Phase V: Tag Types ===
export interface Tag {
  id: number;
  user_id: string;
  name: string;
  created_at: string;
}

export interface TagWithCount extends Tag {
  task_count: number;
}

export interface TagCreate {
  name: string;
}

export interface TagListResponse {
  tags: TagWithCount[];
}

// === Phase V: Recurring Types ===
export type RecurringFrequency = 'daily' | 'weekly' | 'monthly';

export interface RecurringConfig {
  id: number;
  frequency: RecurringFrequency;
  next_occurrence: string;
  created_at: string;
}

// === Phase V: Reminder Types ===
export interface Reminder {
  id: number;
  task_id: string;
  remind_at: string;
  minutes_before: number;
  sent: boolean;
  created_at: string;
}

export interface ReminderPreset {
  label: string;
  minutes_before: number;
}

export const REMINDER_PRESETS: ReminderPreset[] = [
  { label: '15 minutes before', minutes_before: 15 },
  { label: '1 hour before', minutes_before: 60 },
  { label: '1 day before', minutes_before: 1440 },
  { label: '1 week before', minutes_before: 10080 },
];

// === Task types (Extended for Phase V) ===
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean; // Updated to match backend field name
  completed: boolean; // Keep for backwards compatibility

  // Phase V: Advanced Features
  priority: Priority;
  due_date: string | null;
  is_recurring: boolean;
  recurring_config: RecurringConfig | null;
  tags: Tag[];
  reminder: Reminder | null;

  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;

  // Phase V: Advanced Features
  priority?: Priority;
  due_date?: string | null;
  is_recurring?: boolean;
  recurring_frequency?: RecurringFrequency | null;
  tag_ids?: number[];
  reminder_minutes_before?: number | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;

  // Phase V: Advanced Features
  priority?: Priority;
  due_date?: string | null;
  is_recurring?: boolean;
  recurring_frequency?: RecurringFrequency | null;
  tag_ids?: number[];
  reminder_minutes_before?: number | null;
}

export interface TaskListResponse {
  tasks: Task[];
  total?: number;
  page?: number;
  page_size?: number;
}

// === Phase V: Filter & Sort Types ===
export interface FilterParams {
  priority?: Priority[];
  tag_ids?: number[];
  completed?: boolean | null; // null = all, true = completed, false = pending
  due_from?: string;
  due_to?: string;
  search?: string;
}

export type SortField = 'due_date' | 'priority' | 'created_at' | 'title';
export type SortOrder = 'asc' | 'desc';

export interface SortParams {
  sort_by: SortField;
  sort_order: SortOrder;
}

export const SORT_OPTIONS: { value: SortField; label: string }[] = [
  { value: 'due_date', label: 'Due Date' },
  { value: 'priority', label: 'Priority' },
  { value: 'created_at', label: 'Created Date' },
  { value: 'title', label: 'Title (A-Z)' },
];

// Dashboard types
export interface DashboardStats {
  total_tasks: number;
  pending_tasks: number;
  completed_tasks: number;
  completion_rate: number;
  recent_activity: ActivityItem[];
}

export interface ActivityItem {
  task_id: number | null;
  task_title: string;
  action: 'created' | 'completed' | 'updated' | 'deleted';
  timestamp: string;
}

// API Error types
export interface ApiError {
  detail: string;
}
