'use client';

/**
 * RecurringBadge - Visual indicator for recurring tasks
 * Phase V: User Story 7 - Recurring Tasks (T090)
 */

import { Repeat } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { RecurringFrequency } from './RecurringSelect';

interface RecurringBadgeProps {
  frequency: RecurringFrequency;
  className?: string;
  showLabel?: boolean;
}

const FREQUENCY_LABELS: Record<string, string> = {
  daily: 'Daily',
  weekly: 'Weekly',
  monthly: 'Monthly',
};

const FREQUENCY_SHORT_LABELS: Record<string, string> = {
  daily: 'D',
  weekly: 'W',
  monthly: 'M',
};

/**
 * RecurringBadge - Shows recurrence pattern for recurring tasks
 */
export function RecurringBadge({
  frequency,
  className,
  showLabel = true,
}: RecurringBadgeProps) {
  if (!frequency) return null;

  const label = FREQUENCY_LABELS[frequency] || frequency;
  const shortLabel = FREQUENCY_SHORT_LABELS[frequency] || frequency;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium',
        'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
        className
      )}
      title={`Repeats ${label.toLowerCase()}`}
    >
      <Repeat className="h-3 w-3" />
      {showLabel ? (
        <span className="hidden sm:inline">{label}</span>
      ) : null}
      {showLabel ? (
        <span className="sm:hidden">{shortLabel}</span>
      ) : null}
    </span>
  );
}
