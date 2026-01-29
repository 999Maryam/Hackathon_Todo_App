/**
 * Task List Component
 * Displays list of tasks - always visible
 *
 * Phase V: Extended with search results handling
 */

'use client';

import { Search } from 'lucide-react';
import { TaskItem } from './TaskItem';
import { EmptyState } from './EmptyState';
import type { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (taskId: string | number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string | number) => void;
  onCreateClick?: () => void;
  // Phase V: Search state
  searchQuery?: string;
  onClearSearch?: () => void;
}

export function TaskList({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  onCreateClick,
  searchQuery,
  onClearSearch,
}: TaskListProps) {
  // Phase V: Show "no results found" when searching with empty results
  if (tasks.length === 0 && searchQuery) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4">
        <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center mb-4">
          <Search className="w-8 h-8 text-slate-400 dark:text-slate-500" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">
          No tasks found
        </h3>
        <p className="text-sm text-slate-600 dark:text-slate-400 text-center max-w-sm mb-4">
          No tasks match &ldquo;{searchQuery}&rdquo;. Try a different search term or clear the search.
        </p>
        {onClearSearch && (
          <button
            onClick={onClearSearch}
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            Clear search
          </button>
        )}
      </div>
    );
  }

  // Show empty state if no tasks (and not searching)
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
