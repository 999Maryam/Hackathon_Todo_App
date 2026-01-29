/**
 * Task Item Component
 * Individual task card with checkbox, title, description, and action buttons
 *
 * Phase V: Extended with Priority Badge, Due Date Badge, Tags, and Recurring Badge
 */

'use client';

import { Card } from '@/components/ui/Card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Edit, Trash2 } from 'lucide-react';
import type { Task } from '@/lib/types';
import { triggerTaskCompletionConfetti } from '@/lib/confetti';
import { PriorityBadge } from './PriorityBadge';
import { DueDateBadge } from './DueDateBadge';
import { TagList } from '@/components/tags/TagBadge';
import { RecurringBadge } from './RecurringBadge';
import type { RecurringFrequency } from './RecurringSelect';
import { ReminderBadge } from './ReminderPicker';

interface TaskItemProps {
  task: Task;
  onToggleComplete?: (taskId: string | number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string | number) => void;
}

export function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const isCompleted = task.is_completed || task.completed;

  const handleToggle = () => {
    // Trigger confetti when marking as complete
    if (!isCompleted) {
      triggerTaskCompletionConfetti();
    }
    onToggleComplete?.(task.id);
  };

  return (
    <Card className="group p-3 sm:p-4 transition-all duration-200 hover:shadow-lg hover:border-primary/50 hover:-translate-y-1 cursor-default">
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Checkbox */}
        <Checkbox
          checked={isCompleted}
          onCheckedChange={handleToggle}
          className="mt-1 flex-shrink-0 h-5 w-5 sm:h-4 sm:w-4"
          aria-label={`Mark task "${task.title}" as ${isCompleted ? 'incomplete' : 'complete'}`}
        />

        {/* Content */}
        <div className="flex-1 min-w-0 space-y-1">
          {/* Title Row with Priority Badge */}
          <div className="flex items-center gap-2 flex-wrap">
            <h3
              className={`text-base sm:text-lg font-semibold transition-all duration-200 ${
                isCompleted
                  ? 'line-through text-muted-foreground'
                  : 'text-gray-900 dark:text-gray-100'
              }`}
            >
              {task.title}
            </h3>
            {/* Phase V: Priority Badge (US1) */}
            {task.priority && (
              <PriorityBadge priority={task.priority} size="sm" />
            )}
          </div>

          {/* Description */}
          {task.description && (
            <p
              className={`text-sm transition-all duration-200 ${
                isCompleted
                  ? 'line-through text-muted-foreground/70'
                  : 'text-gray-600 dark:text-gray-400'
              } line-clamp-2`}
            >
              {task.description}
            </p>
          )}

          {/* Metadata Row */}
          <div className="flex items-center gap-2 flex-wrap">
            {/* Phase V: Due Date Badge (US2) */}
            {task.due_date && (
              <DueDateBadge
                dueDate={task.due_date}
                completed={isCompleted}
                size="sm"
              />
            )}
            {/* Phase V: Recurring Badge (US7 - T092) */}
            {task.is_recurring && task.recurring_config?.frequency && (
              <RecurringBadge
                frequency={task.recurring_config.frequency as RecurringFrequency}
              />
            )}
            {/* Phase V: Reminder Badge (US8 - T100) */}
            {task.reminder && !task.reminder.sent && task.due_date && (
              <ReminderBadge
                minutesBefore={Math.round(
                  (new Date(task.due_date).getTime() - new Date(task.reminder.remind_at).getTime()) / 60000
                )}
              />
            )}
            {/* Phase V: Tags (US3) */}
            {task.tags && task.tags.length > 0 && (
              <TagList tags={task.tags} maxVisible={3} size="sm" />
            )}
            {/* Created date */}
            <p className="text-xs text-muted-foreground">
              {new Date(task.created_at).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
              })}
            </p>
          </div>
        </div>

        {/* Action Buttons - Always visible */}
        <div className="flex gap-1 sm:gap-2 flex-shrink-0 transition-opacity duration-200">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit?.(task)}
            className="h-9 w-9 sm:h-8 sm:w-8 min-w-[2.25rem] sm:min-w-[2rem] min-h-[2.25rem] sm:min-h-[2rem] hover:bg-blue-50 dark:hover:bg-blue-950 hover:text-blue-600 dark:hover:text-blue-400 hover:scale-110 active:scale-95 transition-all duration-200"
            aria-label="Edit task"
            title="Edit task"
          >
            <Edit className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete?.(task.id)}
            className="h-9 w-9 sm:h-8 sm:w-8 min-w-[2.25rem] sm:min-w-[2rem] min-h-[2.25rem] sm:min-h-[2rem] hover:bg-red-50 dark:hover:bg-red-950 hover:text-red-600 dark:hover:text-red-400 hover:scale-110 active:scale-95 transition-all duration-200"
            aria-label="Delete task"
            title="Delete task"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
}
