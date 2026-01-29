/**
 * Task Modal Component
 * Dialog for creating and editing tasks with React Hook Form + Zod validation
 *
 * Phase V: Extended with Priority, Due Date, Tags, and Recurring fields
 */

'use client';

import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/Input';
import { taskFormSchema, type TaskFormData } from '@/lib/validations';
import type { Task, Priority, Tag, TagWithCount } from '@/lib/types';
import { PrioritySelect } from './PrioritySelect';
import { DueDatePicker } from './DueDatePicker';
import { TagPicker } from './TagPicker';
import { RecurringSelect, type RecurringFrequency } from './RecurringSelect';
import { ReminderPicker } from './ReminderPicker';

interface TaskModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: TaskFormData) => Promise<void>;
  initialData?: Task | null;
  mode: 'create' | 'edit';
  // Phase V: Tag support
  availableTags?: TagWithCount[];
  onCreateTag?: (name: string) => Promise<Tag | null>;
}

/**
 * Modal for creating and editing tasks
 * - Uses shadcn/ui Dialog component
 * - React Hook Form with Zod validation
 * - Support for both create and edit modes
 * - Pre-fills data in edit mode
 * - Shows validation errors
 * - Loading state during submission
 *
 * Phase V: Extended with Priority, Due Date, and Tags fields
 */
export function TaskModal({
  open,
  onOpenChange,
  onSubmit,
  initialData,
  mode,
  availableTags = [],
  onCreateTag,
}: TaskModalProps) {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskFormSchema),
    defaultValues: {
      title: '',
      description: '',
      priority: 'medium',
      due_date: null,
      tag_ids: [],
      is_recurring: false,
      recurring_frequency: null,
      reminder_minutes_before: null,
    },
  });

  // Reset form when modal opens/closes or mode changes
  useEffect(() => {
    if (open) {
      if (mode === 'edit' && initialData) {
        reset({
          title: initialData.title,
          description: initialData.description || '',
          priority: initialData.priority || 'medium',
          due_date: initialData.due_date || null,
          tag_ids: initialData.tags?.map((t) => t.id) || [],
          is_recurring: initialData.is_recurring || false,
          recurring_frequency: initialData.recurring_config?.frequency || null,
          reminder_minutes_before: initialData.reminder?.minutes_before || null,
        });
      } else {
        reset({
          title: '',
          description: '',
          priority: 'medium',
          due_date: null,
          tag_ids: [],
          is_recurring: false,
          recurring_frequency: null,
          reminder_minutes_before: null,
        });
      }
    }
  }, [open, mode, initialData, reset]);

  // Handle form submission
  const handleFormSubmit = async (data: TaskFormData) => {
    await onSubmit(data);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="w-[calc(100vw-2rem)] max-w-[525px] mx-auto max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {mode === 'create' ? 'Create New Task' : 'Edit Task'}
          </DialogTitle>
          <DialogDescription>
            {mode === 'create'
              ? 'Add a new task to your list. Fill in the details below.'
              : 'Update your task details below.'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
          {/* Title Field */}
          <div className="space-y-2">
            <label
              htmlFor="title"
              className="text-sm font-medium text-slate-900 dark:text-slate-100"
            >
              Title <span className="text-red-600">*</span>
            </label>
            <Input
              id="title"
              {...register('title')}
              placeholder="Enter task title..."
              className={errors.title ? 'border-red-500' : ''}
              autoFocus
            />
            {errors.title && (
              <p className="text-sm text-red-600 dark:text-red-400">
                {errors.title.message}
              </p>
            )}
          </div>

          {/* Description Field */}
          <div className="space-y-2">
            <label
              htmlFor="description"
              className="text-sm font-medium text-slate-900 dark:text-slate-100"
            >
              Description <span className="text-slate-500 dark:text-slate-400">(optional)</span>
            </label>
            <textarea
              id="description"
              {...register('description')}
              placeholder="Add details about this task..."
              rows={3}
              className={`flex w-full rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 px-3 py-2 text-sm placeholder:text-slate-400 dark:placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:bg-slate-50 dark:disabled:bg-slate-900 disabled:text-slate-500 resize-none ${
                errors.description ? 'border-red-500 focus-visible:ring-red-500' : ''
              }`}
            />
            {errors.description && (
              <p className="text-sm text-red-600 dark:text-red-400">
                {errors.description.message}
              </p>
            )}
          </div>

          {/* Phase V: Priority and Due Date Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Priority Field (US1) */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-900 dark:text-slate-100">
                Priority
              </label>
              <Controller
                name="priority"
                control={control}
                render={({ field }) => (
                  <PrioritySelect
                    value={field.value as Priority}
                    onChange={field.onChange}
                    className="w-full"
                  />
                )}
              />
            </div>

            {/* Due Date Field (US2) */}
            <Controller
              name="due_date"
              control={control}
              render={({ field }) => (
                <DueDatePicker
                  value={field.value}
                  onChange={field.onChange}
                  label="Due Date"
                />
              )}
            />
          </div>

          {/* Phase V: Tags Field (US3) */}
          {availableTags.length > 0 || onCreateTag ? (
            <Controller
              name="tag_ids"
              control={control}
              render={({ field }) => (
                <TagPicker
                  availableTags={availableTags}
                  selectedTagIds={field.value || []}
                  onChange={field.onChange}
                  onCreateTag={onCreateTag}
                  label="Tags"
                  placeholder="Select or create tags..."
                />
              )}
            />
          ) : null}

          {/* Phase V: Recurring Field (US7 - T091) */}
          <Controller
            name="is_recurring"
            control={control}
            render={({ field: recurringField }) => (
              <Controller
                name="recurring_frequency"
                control={control}
                render={({ field: frequencyField }) => (
                  <RecurringSelect
                    isRecurring={recurringField.value || false}
                    frequency={frequencyField.value as RecurringFrequency}
                    onRecurringChange={recurringField.onChange}
                    onFrequencyChange={frequencyField.onChange}
                  />
                )}
              />
            )}
          />

          {/* Phase V: Reminder Field (US8 - T099) */}
          <Controller
            name="due_date"
            control={control}
            render={({ field: dueDateField }) => (
              <Controller
                name="reminder_minutes_before"
                control={control}
                render={({ field: reminderField }) => (
                  <ReminderPicker
                    value={reminderField.value ?? null}
                    onChange={reminderField.onChange}
                    hasDueDate={!!dueDateField.value}
                    label="Reminder"
                  />
                )}
              />
            )}
          />

          {/* Footer Actions */}
          <DialogFooter className="flex-col-reverse sm:flex-row gap-2 sm:gap-0">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isSubmitting}
              className="w-full sm:w-auto"
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting} className="w-full sm:w-auto">
              {isSubmitting
                ? mode === 'create'
                  ? 'Creating...'
                  : 'Updating...'
                : mode === 'create'
                ? 'Create Task'
                : 'Update Task'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
