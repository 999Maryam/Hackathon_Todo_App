'use client';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Priority, PRIORITY_OPTIONS } from '@/lib/types';
import { cn } from '@/lib/utils';

interface PrioritySelectProps {
  value: Priority;
  onChange: (value: Priority) => void;
  disabled?: boolean;
  className?: string;
}

const priorityColors = {
  high: {
    dot: 'bg-red-500',
    text: 'text-red-600 dark:text-red-400',
  },
  medium: {
    dot: 'bg-amber-500',
    text: 'text-amber-600 dark:text-amber-400',
  },
  low: {
    dot: 'bg-emerald-500',
    text: 'text-emerald-600 dark:text-emerald-400',
  },
};

/**
 * PrioritySelect - Dropdown selector for task priority.
 *
 * Phase V: User Story 1 - Task Priority Management
 * Uses shadcn/ui Select for accessible dropdown with proper styling.
 *
 * @param value - Current priority value
 * @param onChange - Callback when priority changes
 * @param disabled - Whether the select is disabled
 * @param className - Additional CSS classes
 */
export function PrioritySelect({
  value,
  onChange,
  disabled = false,
  className,
}: PrioritySelectProps) {
  const currentOption = PRIORITY_OPTIONS.find((opt) => opt.value === value);
  const colors = priorityColors[value];

  return (
    <Select
      value={value}
      onValueChange={(v) => onChange(v as Priority)}
      disabled={disabled}
    >
      <SelectTrigger className={cn('min-w-[140px]', className)}>
        <SelectValue>
          <span className="flex items-center gap-2">
            <span className={cn('h-2 w-2 rounded-full', colors.dot)} />
            <span className={cn('font-medium', colors.text)}>
              {currentOption?.label || 'Medium'}
            </span>
          </span>
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {PRIORITY_OPTIONS.map((option) => {
          const optionColors = priorityColors[option.value];
          return (
            <SelectItem
              key={option.value}
              value={option.value}
              className="cursor-pointer"
            >
              <span className="flex items-center gap-2">
                <span className={cn('h-2 w-2 rounded-full', optionColors.dot)} />
                <span className={cn('font-medium', optionColors.text)}>
                  {option.label}
                </span>
              </span>
            </SelectItem>
          );
        })}
      </SelectContent>
    </Select>
  );
}
