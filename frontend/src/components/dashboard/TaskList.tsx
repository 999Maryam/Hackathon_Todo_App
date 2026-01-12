/**
 * Task List Component
 * Displays list of tasks - always visible
 */

'use client';

import { TaskItem } from './TaskItem';
import { EmptyState } from './EmptyState';
import type { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
  onCreateClick?: () => void;
}

export function TaskList({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  onCreateClick,
}: TaskListProps) {
  // Show empty state if no tasks
  if (tasks.length === 0) {
    return <EmptyState onCreateClick={onCreateClick} />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div key={task.id}>
          <TaskItem
            task={task}
            onToggleComplete={onToggleComplete}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  );
}
