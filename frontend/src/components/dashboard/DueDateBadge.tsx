'use client';

import { Clock, AlertCircle, Calendar, CheckCircle } from 'lucide-react';
import { getDueStatus, formatDueDate, DueStatus } from '@/lib/date-utils';
import { cn } from '@/lib/utils';

interface DueDateBadgeProps {
  dueDate: string | null;
  completed?: boolean;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
  className?: string;
}

const statusConfig: Record<DueStatus, {
  bgColor: string;
  textColor: string;
  borderColor: string;
  icon: typeof Clock;
}> = {
  overdue: {
    bgColor: 'bg-red-100 dark:bg-red-900/30',
    textColor: 'text-red-700 dark:text-red-400',
    borderColor: 'border-red-200 dark:border-red-800',
    icon: AlertCircle,
  },
  today: {
    bgColor: 'bg-orange-100 dark:bg-orange-900/30',
    textColor: 'text-orange-700 dark:text-orange-400',
    borderColor: 'border-orange-200 dark:border-orange-800',
    icon: Clock,
  },
  tomorrow: {
    bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
    textColor: 'text-yellow-700 dark:text-yellow-400',
    borderColor: 'border-yellow-200 dark:border-yellow-800',
    icon: Calendar,
  },
  soon: {
    bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    textColor: 'text-blue-700 dark:text-blue-400',
    borderColor: 'border-blue-200 dark:border-blue-800',
    icon: Calendar,
  },
  upcoming: {
    bgColor: 'bg-gray-100 dark:bg-gray-800',
    textColor: 'text-gray-700 dark:text-gray-400',
    borderColor: 'border-gray-200 dark:border-gray-700',
    icon: Calendar,
  },
  none: {
    bgColor: 'bg-transparent',
    textColor: 'text-gray-500 dark:text-gray-500',
    borderColor: 'border-transparent',
    icon: Calendar,
  },
};

const sizeConfig = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base',
};

const iconSizeConfig = {
  sm: 'w-3 h-3',
  md: 'w-4 h-4',
  lg: 'w-5 h-5',
};

/**
 * DueDateBadge - Visual indicator for task due dates.
 *
 * Phase V: User Story 2 - Due Dates for Tasks
 * Shows color-coded status: overdue (red), today (orange), tomorrow (yellow), soon (blue), upcoming (gray).
 *
 * @param dueDate - Task due date (ISO string)
 * @param completed - Whether task is completed (hides urgency styling)
 * @param size - Badge size (sm, md, lg)
 * @param showIcon - Whether to show status icon
 * @param className - Additional CSS classes
 */
export function DueDateBadge({
  dueDate,
  completed = false,
  size = 'sm',
  showIcon = true,
  className,
}: DueDateBadgeProps) {
  if (!dueDate) return null;

  // If completed, show muted styling
  if (completed) {
    return (
      <span
        className={cn(
          'inline-flex items-center gap-1 rounded-full border',
          'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-500 border-gray-200 dark:border-gray-700',
          sizeConfig[size],
          className
        )}
      >
        {showIcon && <CheckCircle className={cn(iconSizeConfig[size], 'text-green-500')} />}
        <span className="line-through">{formatDueDate(dueDate)}</span>
      </span>
    );
  }

  const status = getDueStatus(dueDate);
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full border font-medium',
        config.bgColor,
        config.textColor,
        config.borderColor,
        sizeConfig[size],
        className
      )}
    >
      {showIcon && <Icon className={iconSizeConfig[size]} />}
      {formatDueDate(dueDate)}
    </span>
  );
}
