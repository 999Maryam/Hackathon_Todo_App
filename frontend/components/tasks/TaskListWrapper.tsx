'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/useTasks';
import { TaskList as TaskListComponent } from './TaskList';

export const TaskList = () => {
  const {
    tasks,
    isLoading,
    error,
    filter,
    setFilter,
    toggleTaskCompletion,
    deleteTask
  } = useTasks();

  const handleToggleComplete = (task: any) => {
    toggleTaskCompletion(task.id.toString());
  };

  const handleDelete = (taskId: string | number) => {
    deleteTask(taskId.toString());
  };

  return (
    <TaskListComponent
      tasks={tasks}
      loading={isLoading}
      error={error}
      onToggleComplete={handleToggleComplete}
      onDelete={handleDelete}
      filter={filter}
      onFilterChange={setFilter}
    />
  );
};