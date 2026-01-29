'use client';

/**
 * ReminderPicker - Task reminder configuration
 * Phase V: User Story 8 - Task Reminders (T098)
 */

import { Bell, BellOff } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { cn } from '@/lib/utils';

// Preset reminder options (in minutes)
const REMINDER_PRESETS = [
  { value: '15', label: '15 minutes before', minutes: 15 },
  { value: '30', label: '30 minutes before', minutes: 30 },
  { value: '60', label: '1 hour before', minutes: 60 },
  { value: '120', label: '2 hours before', minutes: 120 },
  { value: '1440', label: '1 day before', minutes: 1440 },
  { value: '2880', label: '2 days before', minutes: 2880 },
] as const;

interface ReminderPickerProps {
  /** Minutes before due date (null if no reminder) */
  value: number | null;
  /** Called when reminder changes */
  onChange: (minutes: number | null) => void;
  /** Whether a due date is set (required for reminders) */
  hasDueDate: boolean;
  /** Optional label */
  label?: string;
  /** Additional CSS classes */
  className?: string;
  /** Disabled state */
  disabled?: boolean;
}

/**
 * ReminderPicker - Allows users to set reminders for tasks with due dates
 * Shows a toggle and preset options (1h before, 1d before, etc.)
 */
export function ReminderPicker({
  value,
  onChange,
  hasDueDate,
  label = 'Reminder',
  className,
  disabled = false,
}: ReminderPickerProps) {
  const isEnabled = value !== null && value > 0;

  const handleToggle = (checked: boolean) => {
    if (checked) {
      // Default to 1 hour before
      onChange(60);
    } else {
      onChange(null);
    }
  };

  const handlePresetChange = (preset: string) => {
    onChange(parseInt(preset, 10));
  };

  // If no due date, show disabled state with message
  if (!hasDueDate) {
    return (
      <div className={cn('space-y-2', className)}>
        <div className="flex items-center gap-2">
          <BellOff className="h-4 w-4 text-muted-foreground" />
          <Label className="text-sm font-medium text-muted-foreground">
            {label}
          </Label>
        </div>
        <p className="text-xs text-muted-foreground pl-6">
          Set a due date to enable reminders
        </p>
      </div>
    );
  }

  return (
    <div className={cn('space-y-3', className)}>
      {/* Reminder Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell className={cn(
            'h-4 w-4',
            isEnabled ? 'text-amber-500' : 'text-muted-foreground'
          )} />
          <Label htmlFor="reminder-toggle" className="text-sm font-medium">
            {label}
          </Label>
        </div>
        <Switch
          id="reminder-toggle"
          checked={isEnabled}
          onCheckedChange={handleToggle}
          disabled={disabled}
        />
      </div>

      {/* Preset Selector (only shown when enabled) */}
      {isEnabled && (
        <div className="pl-6">
          <Label htmlFor="reminder-preset" className="text-sm text-muted-foreground mb-1.5 block">
            Remind me
          </Label>
          <Select
            value={value?.toString() || '60'}
            onValueChange={handlePresetChange}
            disabled={disabled}
          >
            <SelectTrigger id="reminder-preset" className="w-full">
              <SelectValue placeholder="Select when to remind" />
            </SelectTrigger>
            <SelectContent>
              {REMINDER_PRESETS.map((preset) => (
                <SelectItem key={preset.value} value={preset.value}>
                  {preset.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}
    </div>
  );
}

/**
 * ReminderBadge - Small indicator showing reminder is set
 */
interface ReminderBadgeProps {
  /** Minutes before due date */
  minutesBefore: number;
  /** Additional CSS classes */
  className?: string;
}

export function ReminderBadge({ minutesBefore, className }: ReminderBadgeProps) {
  // Format the reminder time
  const formatReminder = (minutes: number): string => {
    if (minutes < 60) return `${minutes}m`;
    if (minutes < 1440) return `${Math.round(minutes / 60)}h`;
    return `${Math.round(minutes / 1440)}d`;
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium',
        'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
        className
      )}
      title={`Reminder set ${formatReminder(minutesBefore)} before due date`}
    >
      <Bell className="h-3 w-3" />
      <span>{formatReminder(minutesBefore)}</span>
    </span>
  );
}
