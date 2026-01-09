'use client';

import React from 'react';
import { Modal } from '../../src/components/ui/Modal';
import { TaskForm, TaskFormValues } from './TaskForm';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: TaskFormValues) => void;
  initialData?: {
    id?: string | number;
    title: string;
    description?: string;
    dueDate?: string | null;
  };
  isSubmitting?: boolean;
}

export const TaskModal: React.FC<TaskModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  isSubmitting = false,
}) => {
  const handleSubmit = (formData: TaskFormValues) => {
    onSubmit(formData);
  };

  // Prepare default values for the form
  const defaultValues = {
    title: initialData?.title || '',
    description: initialData?.description || '',
    dueDate: initialData?.dueDate || '',
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="md"
      header={initialData ? 'Edit Task' : 'Create New Task'}
    >
      <div className="p-4">
        <TaskForm
          defaultValues={defaultValues}
          onSubmit={handleSubmit}
          isSubmitting={isSubmitting}
          submitButtonText={initialData ? 'Update Task' : 'Create Task'}
        />
      </div>
    </Modal>
  );
};