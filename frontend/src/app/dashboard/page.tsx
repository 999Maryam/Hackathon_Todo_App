/**
 * Dashboard Page
 * Main task management interface with header, task list, and CRUD operations
 *
 * Phase V: Extended with search, filter, and sort functionality
 */

'use client';

import { useState, useCallback } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { useTags } from '@/hooks/useTags';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { TaskList } from '@/components/dashboard/TaskList';
import { TaskListSkeleton } from '@/components/shared/TaskListSkeleton';
import { AddTaskButton } from '@/components/dashboard/AddTaskButton';
import { FloatingChatButton } from '@/components/dashboard/FloatingChatButton';
import { TaskModal } from '@/components/dashboard/TaskModal';
import { ConfirmationDialog } from '@/components/shared/ConfirmationDialog';
import { SearchBar } from '@/components/dashboard/SearchBar';
import { FilterPanel } from '@/components/dashboard/FilterPanel';
import { SortDropdown, type SortField } from '@/components/dashboard/SortDropdown';
import type { Task, Tag, FilterParams, SortParams } from '@/lib/types';
import type { TaskFormData } from '@/lib/validations';

export default function DashboardPage() {
  const { user } = useAuth();

  // Phase V: Search state (US4)
  const [searchQuery, setSearchQuery] = useState('');

  // Phase V: Filter state (US5)
  const [filters, setFilters] = useState<FilterParams>({});

  // Phase V: Sort state (US6)
  const [sortBy, setSortBy] = useState<SortField>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Use tasks with search, filter, and sort parameters
  const {
    tasks,
    isLoading,
    isError,
    createTask,
    updateTask,
    toggleComplete,
    deleteTask,
  } = useTasks(user?.id || null, {
    search: searchQuery || undefined,
    priority: filters.priority,
    completed: filters.completed ?? undefined,
    due_from: filters.due_from,
    due_to: filters.due_to,
    tag_ids: filters.tag_ids,
    sort_by: sortBy,
    sort_order: sortOrder,
  });

  // Phase V: Use tags for the modal
  const { tags, createTag } = useTags(user?.id || null);

  // Handle tag creation from modal
  const handleCreateTag = useCallback(async (name: string): Promise<Tag | null> => {
    return createTag({ name });
  }, [createTag]);

  // Phase V: Handle sort changes (US6 - T081)
  const handleSortChange = useCallback((params: SortParams) => {
    setSortBy(params.sort_by as SortField);
    setSortOrder(params.sort_order);
  }, []);

  // Modal state management
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Delete confirmation state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<string | number | null>(null);

  // Handle opening modal in create mode
  const handleOpenCreate = () => {
    setModalMode('create');
    setSelectedTask(null);
    setModalOpen(true);
  };

  // Handle opening modal in edit mode
  const handleEdit = (task: Task) => {
    setModalMode('edit');
    setSelectedTask(task);
    setModalOpen(true);
  };

  // Handle form submission (create or edit)
  const handleSubmit = async (data: TaskFormData) => {
    if (modalMode === 'create') {
      await createTask(data);
    } else if (selectedTask) {
      await updateTask(selectedTask.id, data);
    }
    setModalOpen(false);
  };

  // Handle task completion toggle
  const handleToggleComplete = async (taskId: string | number) => {
    await toggleComplete(taskId);
  };

  // Handle delete button click - show confirmation
  const handleDeleteClick = (taskId: string | number) => {
    setTaskToDelete(taskId);
    setDeleteConfirmOpen(true);
  };

  // Handle confirmed delete
  const handleDeleteConfirm = async () => {
    if (taskToDelete !== null) {
      await deleteTask(taskToDelete);
      setDeleteConfirmOpen(false);
      setTaskToDelete(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <DashboardHeader />

      {/* Main Content */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Page Title and Search Bar */}
          <div className="mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100">
                  My Tasks
                </h2>
                <p className="mt-2 text-gray-600 dark:text-gray-400">
                  {isLoading
                    ? 'Loading your tasks...'
                    : searchQuery
                    ? `${tasks.length} result${tasks.length !== 1 ? 's' : ''} for "${searchQuery}"`
                    : `${tasks.length} ${tasks.length === 1 ? 'task' : 'tasks'}`}
                </p>
              </div>
              {/* Phase V: Search Bar (US4) */}
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder="Search tasks..."
              />
            </div>
          </div>

          {/* Phase V: Filter Panel (US5) and Sort Dropdown (US6) */}
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6">
            <FilterPanel
              filters={filters}
              onFiltersChange={setFilters}
              availableTags={tags}
              className="flex-1"
            />
            {/* Phase V: Sort Dropdown (US6 - T081) */}
            <SortDropdown
              sortBy={sortBy}
              sortOrder={sortOrder}
              onSortChange={handleSortChange}
              className="shrink-0"
            />
          </div>

          {/* Error State */}
          {isError && (
            <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
              <p className="text-red-800 dark:text-red-200 text-sm">
                Failed to load tasks. Please try again later.
              </p>
            </div>
          )}

          {/* Task List or Loading Skeleton */}
          {isLoading ? (
            <TaskListSkeleton count={5} />
          ) : (
            <TaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEdit}
              onDelete={handleDeleteClick}
              onCreateClick={handleOpenCreate}
              searchQuery={searchQuery}
              onClearSearch={() => setSearchQuery('')}
            />
          )}
        </div>
      </main>

      {/* Floating Action Buttons */}
      <FloatingChatButton />
      <AddTaskButton onClick={handleOpenCreate} />

      {/* Task Modal (Create/Edit) */}
      <TaskModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        onSubmit={handleSubmit}
        initialData={selectedTask}
        mode={modalMode}
        availableTags={tags}
        onCreateTag={handleCreateTag}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmationDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        onConfirm={handleDeleteConfirm}
        title="Delete Task"
        description="Are you sure you want to delete this task? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
}
