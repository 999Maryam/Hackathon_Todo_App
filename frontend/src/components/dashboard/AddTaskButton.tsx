/**
 * Floating Action Button (FAB) - Add Task Button
 * Fixed position button in bottom-right corner for creating new tasks
 */

'use client';

import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface AddTaskButtonProps {
  onClick: () => void;
}

/**
 * Floating Action Button for adding new tasks
 * - Fixed bottom-right position
 * - Large circular button with Plus icon
 * - Primary vibrant blue background
 * - Scale animation on hover
 * - Mobile-friendly with large touch target (56x56px minimum)
 */
export function AddTaskButton({ onClick }: AddTaskButtonProps) {
  return (
    <Button
      onClick={onClick}
      size="lg"
      className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 lg:bottom-8 lg:right-8 h-14 w-14 sm:h-16 sm:w-16 min-w-[3.5rem] min-h-[3.5rem] sm:min-w-[4rem] sm:min-h-[4rem] rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110 active:scale-95 z-50"
      aria-label="Add new task"
    >
      <Plus className="h-6 w-6 sm:h-7 sm:w-7" />
    </Button>
  );
}
