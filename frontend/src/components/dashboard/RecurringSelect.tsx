'use client';

/**
 * RecurringSelect - Recurring task frequency selector
 * Phase V: User Story 7 - Recurring Tasks (T089)
 */

import { Repeat } from 'lucide-react';
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

export type RecurringFrequency = 'daily' | 'weekly' | 'monthly' | null;

const FREQUENCY_OPTIONS: { value: RecurringFrequency; label: string }[] = [
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
];

interface RecurringSelectProps {
  isRecurring: boolean;
  frequency: RecurringFrequency;
  onRecurringChange: (isRecurring: boolean) => void;
  onFrequencyChange: (frequency: RecurringFrequency) => void;
  className?: string;
  disabled?: boolean;
}

/**
 * RecurringSelect - Combined toggle and frequency selector for recurring tasks
 */
export function RecurringSelect({
  isRecurring,
  frequency,
  onRecurringChange,
  onFrequencyChange,
  className,
  disabled = false,
}: RecurringSelectProps) {
  const handleToggle = (checked: boolean) => {
    onRecurringChange(checked);
    // Reset frequency when disabling recurring
    if (!checked) {
      onFrequencyChange(null);
    } else if (!frequency) {
      // Default to weekly when enabling
      onFrequencyChange('weekly');
    }
  };

  return (
    <div className={cn('space-y-3', className)}>
      {/* Recurring Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Repeat className="h-4 w-4 text-muted-foreground" />
          <Label htmlFor="recurring-toggle" className="text-sm font-medium">
            Repeat Task
          </Label>
        </div>
        <Switch
          id="recurring-toggle"
          checked={isRecurring}
          onCheckedChange={handleToggle}
          disabled={disabled}
        />
      </div>

      {/* Frequency Selector (only shown when recurring is enabled) */}
      {isRecurring && (
        <div className="pl-6">
          <Label htmlFor="frequency-select" className="text-sm text-muted-foreground mb-1.5 block">
            Repeat every
          </Label>
          <Select
            value={frequency || 'weekly'}
            onValueChange={(value) => onFrequencyChange(value as RecurringFrequency)}
            disabled={disabled}
          >
            <SelectTrigger id="frequency-select" className="w-full">
              <SelectValue placeholder="Select frequency" />
            </SelectTrigger>
            <SelectContent>
              {FREQUENCY_OPTIONS.map((option) => (
                <SelectItem key={option.value} value={option.value!}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}
    </div>
  );
}
