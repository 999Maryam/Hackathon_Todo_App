'use client';

import { useState } from 'react';
import Button from '@/components/ui/Button';
import { TaskModal } from '@/components/tasks/TaskModal';

export const AddTaskButton = () => {
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = async (taskData: any) => {
    // This would typically call a mutation function from a hook
    // For now, we'll just close the modal
    console.log('Creating task:', taskData);
    setShowModal(false);
  };

  return (
    <>
      <Button onClick={() => setShowModal(true)}>
        <svg className="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Add Task
      </Button>

      {showModal && (
        <TaskModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onSubmit={handleSubmit}
        />
      )}
    </>
  );
};