/**
 * Type definitions for the Premium Todo App
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

// Task types
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean; // Updated to match backend field name
  completed: boolean; // Keep for backwards compatibility
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

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
