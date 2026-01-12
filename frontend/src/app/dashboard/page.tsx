/**
 * Dashboard Page
 * Main task management interface with header, task list, and CRUD operations
 */

'use client';

import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { TaskList } from '@/components/dashboard/TaskList';
import { TaskListSkeleton } from '@/components/shared/TaskListSkeleton';
import { AddTaskButton } from '@/components/dashboard/AddTaskButton';
import { TaskModal } from '@/components/dashboard/TaskModal';
import { ConfirmationDialog } from '@/components/shared/ConfirmationDialog';
import type { Task } from '@/lib/types';
import type { TaskFormData } from '@/lib/validations';

export default function DashboardPage() {
  const { user } = useAuth();
  const {
    tasks,
    isLoading,
    isError,
    createTask,
    updateTask,
    toggleComplete,
    deleteTask,
  } = useTasks(user?.id || null);

  // Modal state management
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Delete confirmation state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<number | null>(null);

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
  const handleToggleComplete = async (taskId: number) => {
    await toggleComplete(taskId);
  };

  // Handle delete button click - show confirmation
  const handleDeleteClick = (taskId: number) => {
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
          {/* Page Title */}
          <div className="mb-8">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100">
              My Tasks
            </h2>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              {isLoading
                ? 'Loading your tasks...'
                : `${tasks.length} ${tasks.length === 1 ? 'task' : 'tasks'}`}
            </p>
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
            />
          )}
        </div>
      </main>

      {/* Floating Action Button */}
      <AddTaskButton onClick={handleOpenCreate} />

      {/* Task Modal (Create/Edit) */}
      <TaskModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        onSubmit={handleSubmit}
        initialData={selectedTask}
        mode={modalMode}
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
