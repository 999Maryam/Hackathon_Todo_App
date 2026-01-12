/**
 * useTasks Hook - Task data fetching and management with SWR
 * Provides optimistic updates and cache management for tasks
 */

'use client';

import useSWR, { mutate } from 'swr';
import { tasksApi } from '@/lib/api';
import type { Task, TaskCreate, TaskUpdate } from '@/lib/types';
import { toast } from 'sonner';

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  isError: boolean;
  error: any;
  refresh: () => void;
  createTask: (data: TaskCreate) => Promise<Task | undefined>;
  updateTask: (taskId: number, data: TaskUpdate) => Promise<Task | undefined>;
  deleteTask: (taskId: number) => Promise<boolean>;
  toggleComplete: (taskId: number) => Promise<Task | undefined>;
}

/**
 * Hook for managing tasks with SWR caching and optimistic updates
 */
export function useTasks(userId: string | null): UseTasksReturn {
  // Create unique SWR key
  const swrKey = userId ? `/api/${userId}/tasks` : null;

  // Fetcher function
  const fetcher = async () => {
    if (!userId) return { tasks: [], total: 0 };
    const response = await tasksApi.list(userId);
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
      // Optimistic update - add temporary task
      const tempTask: Task = {
        id: Date.now(), // Temporary ID
        user_id: userId,
        title: taskData.title,
        description: taskData.description || null,
        is_completed: false,
        completed: false,
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
    } catch (error: any) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error.response?.detail || error.message || 'Failed to create task';
      toast.error(message);
      throw error;
    }
  };

  // Update task with optimistic update
  const updateTask = async (
    taskId: number,
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
    } catch (error: any) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error.response?.detail || error.message || 'Failed to update task';
      toast.error(message);
      throw error;
    }
  };

  // Delete task with optimistic update
  const deleteTask = async (taskId: number): Promise<boolean> => {
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
    } catch (error: any) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error.response?.detail || error.message || 'Failed to delete task';
      toast.error(message);
      return false;
    }
  };

  // Toggle task completion with optimistic update
  const toggleComplete = async (taskId: number): Promise<Task | undefined> => {
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
    } catch (error: any) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error.response?.detail || error.message || 'Failed to toggle task';
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
