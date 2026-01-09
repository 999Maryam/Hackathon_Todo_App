'use client';

import React from 'react';
import { TodoTask } from '@/lib/types';
import { TaskItem } from './TaskItem';
import { Card } from '../ui/Card';

interface TaskListProps {
  tasks: TodoTask[];
  loading?: boolean;
  error?: string | null;
  onToggleComplete: (task: TodoTask) => void;
  onDelete: (taskId: string | number) => void;
  filter?: 'all' | 'active' | 'completed';
  onFilterChange?: (filter: 'all' | 'active' | 'completed') => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  loading = false,
  error = null,
  onToggleComplete,
  onDelete,
  filter = 'all',
  onFilterChange,
}) => {
  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all' filter
  });

  // Count active tasks for display
  const activeTaskCount = tasks.filter(task => !task.completed).length;

  if (loading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse flex flex-col space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-200 dark:bg-gray-700 rounded"></div>
          ))}
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6">
        <div className="text-red-500 text-center py-4">
          <p>Error loading tasks: {error}</p>
        </div>
      </Card>
    );
  }

  if (filteredTasks.length === 0) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">
            {filter === 'completed'
              ? 'No completed tasks yet.'
              : filter === 'active'
                ? 'All caught up! No active tasks.'
                : 'No tasks yet. Create your first task!'}
          </p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden">
      {/* Filter Controls */}
      {onFilterChange && (
        <div className="border-b border-gray-200 dark:border-gray-700 px-6 py-4 bg-gray-50 dark:bg-gray-800">
          <div className="flex flex-wrap gap-2">
            {(['all', 'active', 'completed'] as const).map((f) => (
              <button
                key={f}
                onClick={() => onFilterChange(f)}
                className={`px-3 py-1 rounded-full text-sm capitalize ${
                  filter === f
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {f} ({f === 'all' ? tasks.length : f === 'active' ? activeTaskCount : tasks.length - activeTaskCount})
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Task List */}
      <ul className="divide-y divide-gray-200 dark:divide-gray-700">
        {filteredTasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleComplete={onToggleComplete}
            onDelete={onDelete}
          />
        ))}
      </ul>

      {/* Task Summary */}
      <div className="border-t border-gray-200 dark:border-gray-700 px-6 py-3 bg-gray-50 dark:bg-gray-800 text-sm text-gray-500 dark:text-gray-400">
        {activeTaskCount} {activeTaskCount === 1 ? 'task' : 'tasks'} left
      </div>
    </Card>
  );
};