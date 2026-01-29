/**
 * FilterPanel Component - Advanced task filtering UI
 * Phase V US5: Filter tasks by priority, completion status, due date, and tags
 */

'use client';

import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import {
  Filter,
  X,
  CalendarIcon,
  ChevronDown,
  Tag as TagIcon,
  CheckCircle2,
  Circle,
  ListFilter,
} from 'lucide-react';
import type { Priority, Tag, FilterParams } from '@/lib/types';
import { PRIORITY_OPTIONS } from '@/lib/types';

interface FilterPanelProps {
  filters: FilterParams;
  onFiltersChange: (filters: FilterParams) => void;
  availableTags?: Tag[];
  className?: string;
}

type CompletionFilter = 'all' | 'pending' | 'completed';

/**
 * Get completion filter value from FilterParams
 */
function getCompletionFilter(completed: boolean | null | undefined): CompletionFilter {
  if (completed === true) return 'completed';
  if (completed === false) return 'pending';
  return 'all';
}

/**
 * Convert CompletionFilter to boolean for API
 */
function completionFilterToBoolean(filter: CompletionFilter): boolean | undefined {
  if (filter === 'completed') return true;
  if (filter === 'pending') return false;
  return undefined;
}

/**
 * Priority color mapping for consistent styling
 */
const PRIORITY_COLORS = {
  high: {
    dot: 'bg-red-500',
    bg: 'bg-red-50 dark:bg-red-950/30',
    border: 'border-red-200 dark:border-red-800',
    text: 'text-red-700 dark:text-red-400',
  },
  medium: {
    dot: 'bg-amber-500',
    bg: 'bg-amber-50 dark:bg-amber-950/30',
    border: 'border-amber-200 dark:border-amber-800',
    text: 'text-amber-700 dark:text-amber-400',
  },
  low: {
    dot: 'bg-emerald-500',
    bg: 'bg-emerald-50 dark:bg-emerald-950/30',
    border: 'border-emerald-200 dark:border-emerald-800',
    text: 'text-emerald-700 dark:text-emerald-400',
  },
};

export function FilterPanel({
  filters,
  onFiltersChange,
  availableTags = [],
  className,
}: FilterPanelProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Count active filters
  const activeFilterCount = [
    filters.priority && filters.priority.length > 0,
    filters.completed !== undefined && filters.completed !== null,
    filters.due_from || filters.due_to,
    filters.tag_ids && filters.tag_ids.length > 0,
  ].filter(Boolean).length;

  // Handle priority checkbox change
  const handlePriorityChange = useCallback(
    (priority: Priority, checked: boolean) => {
      const currentPriorities = filters.priority || [];
      const newPriorities = checked
        ? [...currentPriorities, priority]
        : currentPriorities.filter((p) => p !== priority);

      onFiltersChange({
        ...filters,
        priority: newPriorities.length > 0 ? newPriorities : undefined,
      });
    },
    [filters, onFiltersChange]
  );

  // Handle completion status change
  const handleCompletionChange = useCallback(
    (status: CompletionFilter) => {
      onFiltersChange({
        ...filters,
        completed: completionFilterToBoolean(status),
      });
    },
    [filters, onFiltersChange]
  );

  // Handle due date range change
  const handleDueDateChange = useCallback(
    (type: 'from' | 'to', date: Date | undefined) => {
      onFiltersChange({
        ...filters,
        [type === 'from' ? 'due_from' : 'due_to']: date
          ? format(date, 'yyyy-MM-dd')
          : undefined,
      });
    },
    [filters, onFiltersChange]
  );

  // Handle tag selection
  const handleTagChange = useCallback(
    (tagId: number, checked: boolean) => {
      const currentTags = filters.tag_ids || [];
      const newTags = checked
        ? [...currentTags, tagId]
        : currentTags.filter((id) => id !== tagId);

      onFiltersChange({
        ...filters,
        tag_ids: newTags.length > 0 ? newTags : undefined,
      });
    },
    [filters, onFiltersChange]
  );

  // Clear all filters
  const handleClearAll = useCallback(() => {
    onFiltersChange({
      search: filters.search, // Keep search query
    });
  }, [filters.search, onFiltersChange]);

  const completionStatus = getCompletionFilter(filters.completed);

  return (
    <div className={cn('space-y-3', className)}>
      {/* Filter Toggle Button */}
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsExpanded(!isExpanded)}
          className={cn(
            'gap-2 border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800',
            isExpanded && 'bg-slate-50 dark:bg-slate-800'
          )}
        >
          <Filter className="h-4 w-4 text-slate-500" />
          <span className="font-medium">Filters</span>
          {activeFilterCount > 0 && (
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-600 text-[10px] font-semibold text-white">
              {activeFilterCount}
            </span>
          )}
          <ChevronDown
            className={cn(
              'h-4 w-4 text-slate-400 transition-transform duration-200',
              isExpanded && 'rotate-180'
            )}
          />
        </Button>

        {/* Clear All Button - shown when filters are active */}
        {activeFilterCount > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClearAll}
            className="gap-1.5 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
          >
            <X className="h-4 w-4" />
            Clear all
          </Button>
        )}
      </div>

      {/* Expanded Filter Panel */}
      {isExpanded && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {/* Status Filter Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <ListFilter className="h-4 w-4 text-slate-400" />
                <Label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Status
                </Label>
              </div>
              <div className="flex flex-col gap-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 p-1.5">
                {(['all', 'pending', 'completed'] as CompletionFilter[]).map(
                  (status) => {
                    const isActive = completionStatus === status;
                    const Icon = status === 'completed' ? CheckCircle2 : status === 'pending' ? Circle : ListFilter;
                    return (
                      <button
                        key={status}
                        onClick={() => handleCompletionChange(status)}
                        className={cn(
                          'flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-all duration-150',
                          isActive
                            ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 shadow-sm'
                            : 'text-slate-600 dark:text-slate-400 hover:bg-white/50 dark:hover:bg-slate-700/50 hover:text-slate-900 dark:hover:text-slate-200'
                        )}
                      >
                        <Icon className={cn(
                          'h-4 w-4',
                          isActive ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'
                        )} />
                        {status.charAt(0).toUpperCase() + status.slice(1)}
                      </button>
                    );
                  }
                )}
              </div>
            </div>

            {/* Priority Filter Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="flex -space-x-1">
                  <span className="h-3 w-3 rounded-full bg-red-500 ring-2 ring-white dark:ring-slate-900" />
                  <span className="h-3 w-3 rounded-full bg-amber-500 ring-2 ring-white dark:ring-slate-900" />
                  <span className="h-3 w-3 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-900" />
                </div>
                <Label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Priority
                </Label>
              </div>
              <div className="space-y-2">
                {PRIORITY_OPTIONS.map(({ value, label }) => {
                  const colors = PRIORITY_COLORS[value];
                  const isChecked = filters.priority?.includes(value) || false;
                  return (
                    <label
                      key={value}
                      className={cn(
                        'flex items-center gap-3 rounded-lg border px-3 py-2.5 cursor-pointer transition-all duration-150',
                        isChecked
                          ? cn(colors.bg, colors.border)
                          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      )}
                    >
                      <Checkbox
                        id={`priority-${value}`}
                        checked={isChecked}
                        onCheckedChange={(checked) =>
                          handlePriorityChange(value, checked === true)
                        }
                        className="border-slate-300 dark:border-slate-600"
                      />
                      <span className={cn('h-2.5 w-2.5 rounded-full', colors.dot)} />
                      <span className={cn(
                        'text-sm font-medium',
                        isChecked ? colors.text : 'text-slate-700 dark:text-slate-300'
                      )}>
                        {label}
                      </span>
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Due Date Range Filter Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <CalendarIcon className="h-4 w-4 text-slate-400" />
                <Label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Due Date
                </Label>
              </div>
              <div className="flex flex-col gap-2">
                {/* From Date */}
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      size="sm"
                      className={cn(
                        'w-full justify-start text-left font-normal h-10 border-slate-200 dark:border-slate-700',
                        filters.due_from
                          ? 'text-slate-900 dark:text-slate-100'
                          : 'text-slate-500 dark:text-slate-400'
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4 text-slate-400" />
                      {filters.due_from
                        ? format(new Date(filters.due_from), 'MMM d, yyyy')
                        : 'From date'}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={
                        filters.due_from
                          ? new Date(filters.due_from)
                          : undefined
                      }
                      onSelect={(date) => handleDueDateChange('from', date)}
                      initialFocus
                    />
                    {filters.due_from && (
                      <div className="border-t border-slate-200 dark:border-slate-700 p-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="w-full text-slate-600 dark:text-slate-400"
                          onClick={() => handleDueDateChange('from', undefined)}
                        >
                          Clear
                        </Button>
                      </div>
                    )}
                  </PopoverContent>
                </Popover>

                {/* To Date */}
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      size="sm"
                      className={cn(
                        'w-full justify-start text-left font-normal h-10 border-slate-200 dark:border-slate-700',
                        filters.due_to
                          ? 'text-slate-900 dark:text-slate-100'
                          : 'text-slate-500 dark:text-slate-400'
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4 text-slate-400" />
                      {filters.due_to
                        ? format(new Date(filters.due_to), 'MMM d, yyyy')
                        : 'To date'}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={
                        filters.due_to ? new Date(filters.due_to) : undefined
                      }
                      onSelect={(date) => handleDueDateChange('to', date)}
                      disabled={(date) =>
                        filters.due_from
                          ? date < new Date(filters.due_from)
                          : false
                      }
                      initialFocus
                    />
                    {filters.due_to && (
                      <div className="border-t border-slate-200 dark:border-slate-700 p-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="w-full text-slate-600 dark:text-slate-400"
                          onClick={() => handleDueDateChange('to', undefined)}
                        >
                          Clear
                        </Button>
                      </div>
                    )}
                  </PopoverContent>
                </Popover>
              </div>
            </div>

            {/* Tag Filter Section */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <TagIcon className="h-4 w-4 text-slate-400" />
                <Label className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Tags
                </Label>
              </div>
              {availableTags.length > 0 ? (
                <div className="max-h-[140px] space-y-2 overflow-y-auto pr-1">
                  {availableTags.map((tag) => {
                    const isChecked = filters.tag_ids?.includes(tag.id) || false;
                    return (
                      <label
                        key={tag.id}
                        className={cn(
                          'flex items-center gap-3 rounded-lg border px-3 py-2.5 cursor-pointer transition-all duration-150',
                          isChecked
                            ? 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-950/30'
                            : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                        )}
                      >
                        <Checkbox
                          id={`tag-${tag.id}`}
                          checked={isChecked}
                          onCheckedChange={(checked) =>
                            handleTagChange(tag.id, checked === true)
                          }
                          className="border-slate-300 dark:border-slate-600"
                        />
                        <TagIcon className={cn(
                          'h-3.5 w-3.5',
                          isChecked ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'
                        )} />
                        <span className={cn(
                          'text-sm font-medium',
                          isChecked ? 'text-blue-700 dark:text-blue-300' : 'text-slate-700 dark:text-slate-300'
                        )}>
                          {tag.name}
                        </span>
                      </label>
                    );
                  })}
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/30 px-4 py-6 text-center">
                  <TagIcon className="mx-auto h-6 w-6 text-slate-300 dark:text-slate-600 mb-2" />
                  <p className="text-sm text-slate-500 dark:text-slate-400">No tags created yet</p>
                </div>
              )}
            </div>
          </div>

          {/* Active Filters Summary */}
          {activeFilterCount > 0 && (
            <div className="mt-5 pt-4 border-t border-slate-200 dark:border-slate-700">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">
                  Active Filters
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {filters.priority?.map((p) => {
                  const colors = PRIORITY_COLORS[p];
                  return (
                    <span
                      key={p}
                      className={cn(
                        'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium border',
                        colors.bg, colors.border, colors.text
                      )}
                    >
                      <span className={cn('h-2 w-2 rounded-full', colors.dot)} />
                      {PRIORITY_OPTIONS.find((opt) => opt.value === p)?.label}
                      <button
                        onClick={() => handlePriorityChange(p, false)}
                        className="ml-0.5 hover:opacity-70 transition-opacity"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  );
                })}

                {filters.completed !== undefined && (
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-3 py-1 text-xs font-medium text-slate-700 dark:text-slate-300">
                    {filters.completed ? (
                      <CheckCircle2 className="h-3 w-3 text-emerald-500" />
                    ) : (
                      <Circle className="h-3 w-3 text-amber-500" />
                    )}
                    {filters.completed ? 'Completed' : 'Pending'}
                    <button
                      onClick={() => handleCompletionChange('all')}
                      className="ml-0.5 hover:opacity-70 transition-opacity"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                )}

                {(filters.due_from || filters.due_to) && (
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-800 px-3 py-1 text-xs font-medium text-purple-700 dark:text-purple-300">
                    <CalendarIcon className="h-3 w-3" />
                    {filters.due_from
                      ? format(new Date(filters.due_from), 'MMM d')
                      : '...'}
                    {' - '}
                    {filters.due_to
                      ? format(new Date(filters.due_to), 'MMM d')
                      : '...'}
                    <button
                      onClick={() => {
                        onFiltersChange({
                          ...filters,
                          due_from: undefined,
                          due_to: undefined,
                        });
                      }}
                      className="ml-0.5 hover:opacity-70 transition-opacity"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                )}

                {filters.tag_ids?.map((tagId) => {
                  const tag = availableTags.find((t) => t.id === tagId);
                  if (!tag) return null;
                  return (
                    <span
                      key={tagId}
                      className="inline-flex items-center gap-1.5 rounded-full bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 px-3 py-1 text-xs font-medium text-blue-700 dark:text-blue-300"
                    >
                      <TagIcon className="h-3 w-3" />
                      {tag.name}
                      <button
                        onClick={() => handleTagChange(tagId, false)}
                        className="ml-0.5 hover:opacity-70 transition-opacity"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
