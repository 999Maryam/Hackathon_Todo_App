'use client';

import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { TodoTask, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { taskApi } from '@/lib/api';
import { useAuth } from './useAuth';
import toast from 'react-hot-toast';

// Define the fetcher function for SWR
const fetcher = (url: string) => {
  // We'll use taskApi methods which handle auth automatically
  return taskApi.getTasks(url.split('/')[2]); // Extract userId from URL
};

export const useTasks = () => {
  const { user } = useAuth();
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // The SWR key depends on the user ID, so tasks are fetched when user is available
  const userId = user?.userId;
  const { data, error: swrError, mutate, isLoading } = useSWR(
    userId ? `/api/${userId}/tasks` : null,
    () => userId ? taskApi.getTasks(userId) : Promise.resolve({ tasks: [], totalCount: 0 }),
    {
      onError: (err) => {
        toast.error(err.message || 'Failed to fetch tasks');
      },
      refreshInterval: 0, // Disable auto-refresh, we'll handle it manually
      revalidateOnFocus: false, // Don't revalidate on window focus
    }
  );

  // Combine SWR error with local error state
  const combinedError = swrError?.message;

  // Apply filter to tasks
  const filteredTasks = data?.tasks?.filter((task: TodoTask) => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all' filter
  }) || [];

  // Function to create a new task
  const createTask = async (taskData: CreateTaskRequest) => {
    if (!userId) {
      toast.error('User not authenticated');
      throw new Error('User not authenticated');
    }

    try {
      const loadingToast = toast.loading('Creating task...');
      const response = await taskApi.createTask(userId, taskData);
      toast.dismiss(loadingToast);
      toast.success('Task created successfully!');

      // Update the cache optimistically
      await mutate(
        (currentData: any) => {
          if (!currentData) return currentData;
          return {
            ...currentData,
            tasks: [...currentData.tasks, response.task],
            totalCount: currentData.totalCount + 1,
          };
        },
        false // Don't revalidate immediately
      );
      return response.task;
    } catch (err: any) {
      toast.error(err.message || 'Failed to create task');
      throw err;
    }
  };

  // Function to update an existing task
  const updateTask = async (taskId: string, taskData: UpdateTaskRequest) => {
    if (!userId) {
      toast.error('User not authenticated');
      throw new Error('User not authenticated');
    }

    try {
      const loadingToast = toast.loading('Updating task...');
      const response = await taskApi.updateTask(userId, taskId, taskData);
      toast.dismiss(loadingToast);
      toast.success('Task updated successfully!');

      // Update the cache
      await mutate(
        (currentData: any) => {
          if (!currentData) return currentData;
          return {
            ...currentData,
            tasks: currentData.tasks.map((task: TodoTask) =>
              task.id === taskId ? response.task : task
            ),
          };
        },
        false // Don't revalidate immediately
      );
      return response.task;
    } catch (err: any) {
      toast.error(err.message || 'Failed to update task');
      throw err;
    }
  };

  // Function to delete a task
  const deleteTask = async (taskId: string) => {
    if (!userId) {
      toast.error('User not authenticated');
      throw new Error('User not authenticated');
    }

    try {
      const loadingToast = toast.loading('Deleting task...');
      await taskApi.deleteTask(userId, taskId);
      toast.dismiss(loadingToast);
      toast.success('Task deleted successfully!');

      // Update the cache
      await mutate(
        (currentData: any) => {
          if (!currentData) return currentData;
          return {
            ...currentData,
            tasks: currentData.tasks.filter((task: TodoTask) => task.id !== taskId),
            totalCount: Math.max(0, currentData.totalCount - 1),
          };
        },
        false // Don't revalidate immediately
      );
    } catch (err: any) {
      toast.error(err.message || 'Failed to delete task');
      throw err;
    }
  };

  // Function to toggle task completion
  const toggleTaskCompletion = async (taskId: string) => {
    if (!userId) {
      toast.error('User not authenticated');
      throw new Error('User not authenticated');
    }

    try {
      const loadingToast = toast.loading('Updating task status...');
      const response = await taskApi.toggleTaskCompletion(userId, taskId);
      toast.dismiss(loadingToast);

      // Show appropriate message based on new status
      const status = response.task.completed ? 'completed' : 'marked as active';
      toast.success(`Task ${status}!`);

      // Update the cache
      await mutate(
        (currentData: any) => {
          if (!currentData) return currentData;
          return {
            ...currentData,
            tasks: currentData.tasks.map((task: TodoTask) =>
              task.id === taskId ? response.task : task
            ),
          };
        },
        false // Don't revalidate immediately
      );
      return response.task;
    } catch (err: any) {
      toast.error(err.message || 'Failed to toggle task completion');
      throw err;
    }
  };

  // Function to refresh tasks
  const refreshTasks = async () => {
    await mutate();
  };

  // Function to set the filter
  const setTaskFilter = (newFilter: 'all' | 'active' | 'completed') => {
    setFilter(newFilter);
  };

  return {
    tasks: filteredTasks,
    allTasks: data?.tasks || [],
    isLoading,
    error: combinedError,
    filter,
    setFilter: setTaskFilter,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    refreshTasks,
  };
};