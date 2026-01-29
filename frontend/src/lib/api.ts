/**
 * API Client - Centralized typed API client with JWT attachment and error handling
 * All API calls go through this client for consistent error handling and auth
 */

import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
  Task,
  TaskCreate,
  TaskUpdate,
  TaskListResponse,
  DashboardStats,
  ApiError,
  Tag,
  TagCreate,
  TagWithCount,
  TagListResponse,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Session expiry handler - called when 401 is received
 * This will be set by the auth hook
 */
let onSessionExpired: (() => void) | null = null;

export function setSessionExpiredHandler(handler: () => void) {
  onSessionExpired = handler;
}

/**
 * Custom error class for API errors
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: ApiError
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

/**
 * Get auth token from localStorage
 */
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

/**
 * Set auth token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_token', token);
}

/**
 * Remove auth token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user');
}

/**
 * Get stored user from localStorage
 */
export function getStoredUser(): User | null {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

/**
 * Store user in localStorage
 */
export function setStoredUser(user: User): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('user', JSON.stringify(user));
}

/**
 * Generic fetch wrapper with auth and error handling
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Add authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Merge with existing headers
  if (options.headers) {
    Object.assign(headers, options.headers);
  }

  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }

    const data = await response.json();

    // Handle error responses
    if (!response.ok) {
      // Handle session expiry (401 Unauthorized)
      if (response.status === 401 && onSessionExpired) {
        onSessionExpired();
      }

      const errorMessage = data?.detail || `HTTP ${response.status}: ${response.statusText}`;
      throw new ApiClientError(errorMessage, response.status, data);
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    // Network or other errors
    throw new ApiClientError(
      error instanceof Error ? error.message : 'An unknown error occurred'
    );
  }
}

/**
 * Auth API
 */
export const authApi = {
  /**
   * Register a new user
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiFetch<AuthResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    // Store token and user
    setAuthToken(response.access_token);
    setStoredUser(response.user);

    return response;
  },

  /**
   * Login user
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiFetch<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    // Store token and user
    setAuthToken(response.access_token);
    setStoredUser(response.user);

    return response;
  },

  /**
   * Get current user from server
   */
  async me(): Promise<User> {
    return apiFetch<User>('/api/auth/me');
  },

  /**
   * Logout user (client-side only)
   */
  logout(): void {
    clearAuthToken();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!getAuthToken();
  },
};

/**
 * Tasks API - Phase V: Extended with search, filter, sort parameters
 */
export const tasksApi = {
  /**
   * List all tasks for a user with optional search, filter, and sort
   */
  async list(
    userId: string,
    options?: {
      search?: string;
      priority?: string[];
      completed?: boolean;
      due_from?: string;
      due_to?: string;
      tag_ids?: number[];
      sort_by?: string;
      sort_order?: 'asc' | 'desc';
    }
  ): Promise<TaskListResponse> {
    const params = new URLSearchParams();

    if (options?.search) {
      params.append('search', options.search);
    }
    if (options?.priority && options.priority.length > 0) {
      params.append('priority', options.priority.join(','));
    }
    if (options?.completed !== undefined) {
      params.append('completed', String(options.completed));
    }
    if (options?.due_from) {
      params.append('due_from', options.due_from);
    }
    if (options?.due_to) {
      params.append('due_to', options.due_to);
    }
    if (options?.tag_ids && options.tag_ids.length > 0) {
      params.append('tag_ids', options.tag_ids.join(','));
    }
    if (options?.sort_by) {
      params.append('sort_by', options.sort_by);
    }
    if (options?.sort_order) {
      params.append('sort_order', options.sort_order);
    }

    const queryString = params.toString();
    const url = `/api/${userId}/tasks${queryString ? `?${queryString}` : ''}`;
    return apiFetch<TaskListResponse>(url);
  },

  /**
   * Get a single task
   */
  async get(userId: string, taskId: string | number): Promise<Task> {
    return apiFetch<Task>(`/api/${userId}/tasks/${taskId}`);
  },

  /**
   * Create a new task
   */
  async create(userId: string, data: TaskCreate): Promise<Task> {
    return apiFetch<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a task
   */
  async update(userId: string, taskId: string | number, data: TaskUpdate): Promise<Task> {
    return apiFetch<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a task
   */
  async delete(userId: string, taskId: string | number): Promise<void> {
    return apiFetch<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },

  /**
   * Toggle task completion
   */
  async toggleComplete(userId: string, taskId: string | number): Promise<Task> {
    return apiFetch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  },
};

/**
 * Dashboard API
 */
export const dashboardApi = {
  /**
   * Get dashboard statistics
   */
  async getStats(userId: string): Promise<DashboardStats> {
    return apiFetch<DashboardStats>(`/api/${userId}/dashboard`);
  },
};

/**
 * Chat API
 */
export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ToolCallRecord {
  name: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCallRecord[];
}

export const chatApi = {
  /**
   * Send a message to the chat endpoint
   */
  async sendMessage(userId: string, data: ChatRequest): Promise<ChatResponse> {
    return apiFetch<ChatResponse>(`/api/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

/**
 * Tags API - Phase V US3: Tag Management
 */
export const tagsApi = {
  /**
   * List all tags for a user with task counts
   */
  async list(userId: string): Promise<TagListResponse> {
    return apiFetch<TagListResponse>(`/api/${userId}/tags`);
  },

  /**
   * Get a single tag with task count
   */
  async get(userId: string, tagId: number): Promise<TagWithCount> {
    return apiFetch<TagWithCount>(`/api/${userId}/tags/${tagId}`);
  },

  /**
   * Create a new tag
   */
  async create(userId: string, data: TagCreate): Promise<Tag> {
    return apiFetch<Tag>(`/api/${userId}/tags`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a tag
   */
  async update(userId: string, tagId: number, data: TagCreate): Promise<Tag> {
    return apiFetch<Tag>(`/api/${userId}/tags/${tagId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a tag
   */
  async delete(userId: string, tagId: number): Promise<void> {
    return apiFetch<void>(`/api/${userId}/tags/${tagId}`, {
      method: 'DELETE',
    });
  },

  /**
   * Get tags for a specific task
   */
  async getTaskTags(userId: string, taskId: string): Promise<Tag[]> {
    return apiFetch<Tag[]>(`/api/${userId}/tasks/${taskId}/tags`);
  },

  /**
   * Add a tag to a task
   */
  async addTagToTask(userId: string, taskId: string, tagId: number): Promise<void> {
    return apiFetch<void>(`/api/${userId}/tasks/${taskId}/tags/${tagId}`, {
      method: 'POST',
    });
  },

  /**
   * Remove a tag from a task
   */
  async removeTagFromTask(userId: string, taskId: string, tagId: number): Promise<void> {
    return apiFetch<void>(`/api/${userId}/tasks/${taskId}/tags/${tagId}`, {
      method: 'DELETE',
    });
  },
};
