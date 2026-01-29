'use client';

import { Priority } from '@/lib/types';
import { cn } from '@/lib/utils';

interface PriorityBadgeProps {
  priority: Priority;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const priorityConfig = {
  high: {
    label: 'High',
    bgColor: 'bg-red-100 dark:bg-red-900/30',
    textColor: 'text-red-700 dark:text-red-400',
    borderColor: 'border-red-200 dark:border-red-800',
    dotColor: 'bg-red-500',
  },
  medium: {
    label: 'Medium',
    bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
    textColor: 'text-yellow-700 dark:text-yellow-400',
    borderColor: 'border-yellow-200 dark:border-yellow-800',
    dotColor: 'bg-yellow-500',
  },
  low: {
    label: 'Low',
    bgColor: 'bg-green-100 dark:bg-green-900/30',
    textColor: 'text-green-700 dark:text-green-400',
    borderColor: 'border-green-200 dark:border-green-800',
    dotColor: 'bg-green-500',
  },
};

const sizeConfig = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base',
};

/**
 * PriorityBadge - Color-coded priority indicator for tasks.
 *
 * Phase V: User Story 1 - Task Priority Management
 *
 * @param priority - Task priority level (high, medium, low)
 * @param size - Badge size (sm, md, lg)
 * @param className - Additional CSS classes
 */
export function PriorityBadge({
  priority,
  size = 'sm',
  className
}: PriorityBadgeProps) {
  const config = priorityConfig[priority] || priorityConfig.medium;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border font-medium',
        config.bgColor,
        config.textColor,
        config.borderColor,
        sizeConfig[size],
        className
      )}
    >
      <span className={cn('w-1.5 h-1.5 rounded-full', config.dotColor)} />
      {config.label}
    </span>
  );
}

/**
 * PriorityDot - Minimal priority indicator (just the colored dot).
 */
export function PriorityDot({ priority, className }: { priority: Priority; className?: string }) {
  const config = priorityConfig[priority] || priorityConfig.medium;

  return (
    <span
      className={cn('w-2 h-2 rounded-full', config.dotColor, className)}
      title={`${config.label} priority`}
    />
  );
}
