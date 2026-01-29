'use client';

import { Calendar, X } from 'lucide-react';
import { formatDateTimeForInput, formatDueDateWithTime } from '@/lib/date-utils';
import { cn } from '@/lib/utils';

interface DueDatePickerProps {
  value: string | null | undefined;
  onChange: (value: string | null) => void;
  minDate?: Date;
  disabled?: boolean;
  className?: string;
  label?: string;
}

/**
 * DueDatePicker - Date/time picker for task due dates.
 *
 * Phase V: User Story 2 - Due Dates for Tasks
 *
 * @param value - Current due date (ISO string)
 * @param onChange - Callback when date changes
 * @param minDate - Minimum selectable date (default: now)
 * @param disabled - Whether the picker is disabled
 * @param className - Additional CSS classes
 * @param label - Optional label text
 */
export function DueDatePicker({
  value,
  onChange,
  minDate = new Date(),
  disabled = false,
  className,
  label = 'Due Date',
}: DueDatePickerProps) {
  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (newValue) {
      // Convert local datetime to ISO string
      onChange(new Date(newValue).toISOString());
    } else {
      onChange(null);
    }
  };

  const handleClear = () => {
    onChange(null);
  };

  const minDateStr = formatDateTimeForInput(minDate);

  return (
    <div className={cn('flex flex-col gap-1', className)}>
      {label && (
        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
        </label>
      )}

      <div className="relative">
        {/* Date/Time Input */}
        <div className="relative">
          <input
            type="datetime-local"
            value={value ? formatDateTimeForInput(value) : ''}
            onChange={handleDateChange}
            min={minDateStr}
            disabled={disabled}
            className={cn(
              'w-full rounded-md border px-3 py-2 pl-10 text-sm',
              'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600',
              'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              value && 'pr-10'
            )}
          />
          <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />

          {/* Clear button */}
          {value && !disabled && (
            <button
              type="button"
              onClick={handleClear}
              className={cn(
                'absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded',
                'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300',
                'hover:bg-gray-100 dark:hover:bg-gray-700'
              )}
              aria-label="Clear due date"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Display formatted date below */}
        {value && (
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            {formatDueDateWithTime(value)}
          </p>
        )}
      </div>
    </div>
  );
}

/**
 * Quick date presets for common due dates.
 */
export function DueDatePresets({
  onSelect,
  className,
}: {
  onSelect: (date: Date) => void;
  className?: string;
}) {
  const presets = [
    { label: 'Today', getDate: () => endOfDay(new Date()) },
    { label: 'Tomorrow', getDate: () => endOfDay(addDays(new Date(), 1)) },
    { label: 'Next Week', getDate: () => endOfDay(addDays(new Date(), 7)) },
    { label: 'Next Month', getDate: () => endOfDay(addDays(new Date(), 30)) },
  ];

  return (
    <div className={cn('flex flex-wrap gap-2', className)}>
      {presets.map((preset) => (
        <button
          key={preset.label}
          type="button"
          onClick={() => onSelect(preset.getDate())}
          className={cn(
            'px-2 py-1 text-xs rounded-full border',
            'bg-gray-100 dark:bg-gray-800 border-gray-200 dark:border-gray-700',
            'hover:bg-gray-200 dark:hover:bg-gray-700',
            'text-gray-700 dark:text-gray-300'
          )}
        >
          {preset.label}
        </button>
      ))}
    </div>
  );
}

// Helper functions for presets
function endOfDay(date: Date): Date {
  const d = new Date(date);
  d.setHours(23, 59, 59, 999);
  return d;
}

function addDays(date: Date, days: number): Date {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}
