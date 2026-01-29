/**
 * Date utility functions for Phase V task features.
 *
 * Uses date-fns for date manipulation and formatting.
 */

import {
  format,
  formatDistanceToNow,
  isToday,
  isTomorrow,
  isPast,
  isWithinInterval,
  addDays,
  differenceInMinutes,
  parseISO,
} from 'date-fns';

/**
 * Check if a date is overdue (past the current time).
 */
export function isOverdue(date: string | Date | null): boolean {
  if (!date) return false;
  const d = typeof date === 'string' ? parseISO(date) : date;
  return isPast(d);
}

/**
 * Check if a date is today.
 */
export function isDueToday(date: string | Date | null): boolean {
  if (!date) return false;
  const d = typeof date === 'string' ? parseISO(date) : date;
  return isToday(d);
}

/**
 * Check if a date is within the next N days.
 */
export function isDueSoon(date: string | Date | null, days: number = 3): boolean {
  if (!date) return false;
  const d = typeof date === 'string' ? parseISO(date) : date;
  const now = new Date();
  return isWithinInterval(d, { start: now, end: addDays(now, days) });
}

/**
 * Get due status for a task.
 */
export type DueStatus = 'overdue' | 'today' | 'tomorrow' | 'soon' | 'upcoming' | 'none';

export function getDueStatus(date: string | Date | null): DueStatus {
  if (!date) return 'none';
  const d = typeof date === 'string' ? parseISO(date) : date;

  if (isPast(d) && !isToday(d)) return 'overdue';
  if (isToday(d)) return 'today';
  if (isTomorrow(d)) return 'tomorrow';
  if (isDueSoon(d, 3)) return 'soon';
  return 'upcoming';
}

/**
 * Format a due date for display.
 *
 * Returns human-friendly strings like "Today", "Tomorrow", "In 3 days", "Jan 15".
 */
export function formatDueDate(date: string | Date | null): string {
  if (!date) return '';
  const d = typeof date === 'string' ? parseISO(date) : date;

  if (isToday(d)) return 'Today';
  if (isTomorrow(d)) return 'Tomorrow';

  // If within a week, show relative time
  const now = new Date();
  if (isWithinInterval(d, { start: now, end: addDays(now, 7) })) {
    return formatDistanceToNow(d, { addSuffix: true });
  }

  // For overdue, show how long ago
  if (isPast(d)) {
    return formatDistanceToNow(d, { addSuffix: true });
  }

  // Otherwise, show the date
  return format(d, 'MMM d');
}

/**
 * Format a due date with time for display.
 */
export function formatDueDateWithTime(date: string | Date | null): string {
  if (!date) return '';
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'MMM d, yyyy h:mm a');
}

/**
 * Format a date for input fields (ISO format without time).
 */
export function formatDateForInput(date: string | Date | null): string {
  if (!date) return '';
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'yyyy-MM-dd');
}

/**
 * Format a datetime for input fields.
 */
export function formatDateTimeForInput(date: string | Date | null): string {
  if (!date) return '';
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, "yyyy-MM-dd'T'HH:mm");
}

/**
 * Calculate reminder time based on due date and offset.
 */
export function calculateReminderTime(dueDate: Date, minutesBefore: number): Date {
  return new Date(dueDate.getTime() - minutesBefore * 60 * 1000);
}

/**
 * Get minutes until a date.
 */
export function getMinutesUntil(date: string | Date): number {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return differenceInMinutes(d, new Date());
}
