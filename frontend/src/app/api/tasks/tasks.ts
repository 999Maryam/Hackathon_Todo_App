import apiClient from '../../../utils/apiClient';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export const taskApi = {
  // Get all tasks for a user
  getUserTasks: async (userId: string): Promise<{ tasks: Task[]; total: number }> => {
    const response = await apiClient.get(`/${userId}/tasks`);
    return response.data;
  },

  // Create a new task
  createTask: async (userId: string, taskData: TaskCreate): Promise<Task> => {
    const response = await apiClient.post(`/${userId}/tasks`, taskData);
    return response.data;
  },

  // Get a specific task
  getTask: async (userId: string, taskId: string): Promise<Task> => {
    const response = await apiClient.get(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update a task
  updateTask: async (userId: string, taskId: string, taskData: TaskUpdate): Promise<Task> => {
    const response = await apiClient.put(`/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId: string, taskId: string): Promise<Task> => {
    const response = await apiClient.patch(`/${userId}/tasks/${taskId}/complete`);
    return response.data;
  },
};