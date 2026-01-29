/**
 * useTasks Hook - Task data fetching and management with SWR
 * Provides optimistic updates and cache management for tasks
 *
 * Phase V: Extended with search, filter, and sort parameters
 */

'use client';

import useSWR, { mutate } from 'swr';
import { tasksApi } from '@/lib/api';
import type { Task, TaskCreate, TaskUpdate } from '@/lib/types';
import { toast } from 'sonner';

/**
 * Options for the useTasks hook
 * Phase V: Added search, filter, and sort support
 */
interface UseTasksOptions {
  search?: string;
  priority?: string[];
  completed?: boolean;
  due_from?: string;
  due_to?: string;
  tag_ids?: number[];
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  isError: boolean;
  error: Error | undefined;
  refresh: () => void;
  createTask: (data: TaskCreate) => Promise<Task | undefined>;
  updateTask: (taskId: string | number, data: TaskUpdate) => Promise<Task | undefined>;
  deleteTask: (taskId: string | number) => Promise<boolean>;
  toggleComplete: (taskId: string | number) => Promise<Task | undefined>;
}

/**
 * Hook for managing tasks with SWR caching and optimistic updates
 *
 * Phase V: Extended with search, filter, and sort support
 */
export function useTasks(
  userId: string | null,
  options?: UseTasksOptions
): UseTasksReturn {
  // Create unique SWR key including options for proper caching
  const optionsKey = options
    ? JSON.stringify({
        search: options.search || '',
        priority: options.priority || [],
        completed: options.completed,
        sort_by: options.sort_by || '',
        sort_order: options.sort_order || 'desc',
      })
    : '';
  const swrKey = userId ? `/api/${userId}/tasks?${optionsKey}` : null;

  // Fetcher function
  const fetcher = async () => {
    if (!userId) return { tasks: [], total: 0 };
    const response = await tasksApi.list(userId, options);
    return response;
  };

  // SWR hook for data fetching
  const { data, error, isLoading } = useSWR(swrKey, fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: true,
    dedupingInterval: 2000,
  });

  const tasks = data?.tasks || [];

  // Refresh function
  const refresh = () => {
    if (swrKey) {
      mutate(swrKey);
    }
  };

  // Create task with optimistic update
  const createTask = async (taskData: TaskCreate): Promise<Task | undefined> => {
    if (!userId) {
      toast.error('User not authenticated');
      return;
    }

    try {
      // Optimistic update - add temporary task with Phase V fields
      const tempTask: Task = {
        id: String(Date.now()), // Temporary ID as string
        user_id: userId,
        title: taskData.title,
        description: taskData.description || null,
        is_completed: false,
        completed: false,
        // Phase V fields
        priority: taskData.priority || 'medium',
        due_date: taskData.due_date || null,
        is_recurring: taskData.is_recurring || false,
        recurring_config: null,
        tags: [],
        reminder: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      // Update cache optimistically
      mutate(
        swrKey,
        { tasks: [tempTask, ...tasks], total: tasks.length + 1 },
        false
      );

      // Make API call
      const newTask = await tasksApi.create(userId, taskData);

      // Update cache with real data
      mutate(
        swrKey,
        { tasks: [newTask, ...tasks], total: tasks.length + 1 },
        false
      );

      toast.success('Task created successfully');
      return newTask;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to create task';
      toast.error(message);
      throw error;
    }
  };

  // Update task with optimistic update
  const updateTask = async (
    taskId: string | number,
    taskData: TaskUpdate
  ): Promise<Task | undefined> => {
    if (!userId) {
      toast.error('User not authenticated');
      return;
    }

    try {
      // Find existing task
      const existingTask = tasks.find((t) => t.id === taskId);
      if (!existingTask) {
        toast.error('Task not found');
        return;
      }

      // Optimistic update
      const updatedTask = {
        ...existingTask,
        ...taskData,
        updated_at: new Date().toISOString(),
      };

      const updatedTasks = tasks.map((t) => (t.id === taskId ? updatedTask : t));

      mutate(swrKey, { tasks: updatedTasks, total: tasks.length }, false);

      // Make API call
      const result = await tasksApi.update(userId, taskId, taskData);

      // Update cache with real data
      const finalTasks = tasks.map((t) => (t.id === taskId ? result : t));
      mutate(swrKey, { tasks: finalTasks, total: tasks.length }, false);

      toast.success('Task updated successfully');
      return result;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to update task';
      toast.error(message);
      throw error;
    }
  };

  // Delete task with optimistic update
  const deleteTask = async (taskId: string | number): Promise<boolean> => {
    if (!userId) {
      toast.error('User not authenticated');
      return false;
    }

    try {
      // Optimistic update
      const filteredTasks = tasks.filter((t) => t.id !== taskId);
      mutate(swrKey, { tasks: filteredTasks, total: tasks.length - 1 }, false);

      // Make API call
      await tasksApi.delete(userId, taskId);

      // Confirm cache update
      mutate(swrKey);

      toast.success('Task deleted successfully');
      return true;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to delete task';
      toast.error(message);
      return false;
    }
  };

  // Toggle task completion with optimistic update
  const toggleComplete = async (taskId: string | number): Promise<Task | undefined> => {
    if (!userId) {
      toast.error('User not authenticated');
      return;
    }

    try {
      // Find existing task
      const existingTask = tasks.find((t) => t.id === taskId);
      if (!existingTask) {
        toast.error('Task not found');
        return;
      }

      // Optimistic update
      const updatedTask = {
        ...existingTask,
        is_completed: !existingTask.is_completed,
        completed: !existingTask.completed,
        updated_at: new Date().toISOString(),
      };

      const updatedTasks = tasks.map((t) => (t.id === taskId ? updatedTask : t));

      mutate(swrKey, { tasks: updatedTasks, total: tasks.length }, false);

      // Make API call
      const result = await tasksApi.toggleComplete(userId, taskId);

      // Update cache with real data
      const finalTasks = tasks.map((t) => (t.id === taskId ? result : t));
      mutate(swrKey, { tasks: finalTasks, total: tasks.length }, false);

      const message = result.is_completed ? 'Task completed!' : 'Task reopened';
      toast.success(message);

      return result;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to toggle task';
      toast.error(message);
      throw error;
    }
  };

  return {
    tasks,
    isLoading,
    isError: !!error,
    error,
    refresh,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
  };
}
