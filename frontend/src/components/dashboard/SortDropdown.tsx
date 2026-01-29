'use client';

/**
 * SortDropdown - Task sorting controls
 * Phase V: User Story 6 - Sort Tasks (T077-T079)
 */

import { ArrowUpDown, ArrowUp, ArrowDown, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import type { SortParams } from '@/lib/types';

// T078: Sort options
export const SORT_OPTIONS = [
  { value: 'created_at', label: 'Created Date' },
  { value: 'due_date', label: 'Due Date' },
  { value: 'priority', label: 'Priority' },
  { value: 'title', label: 'Title (A-Z)' },
] as const;

export type SortField = (typeof SORT_OPTIONS)[number]['value'];

interface SortDropdownProps {
  sortBy: SortField;
  sortOrder: 'asc' | 'desc';
  onSortChange: (params: SortParams) => void;
  className?: string;
}

/**
 * SortDropdown - Dropdown for selecting sort field and order
 */
export function SortDropdown({
  sortBy,
  sortOrder,
  onSortChange,
  className,
}: SortDropdownProps) {
  const currentOption = SORT_OPTIONS.find((opt) => opt.value === sortBy);

  // Handle sort field change
  const handleSortFieldChange = (field: SortField) => {
    onSortChange({
      sort_by: field,
      sort_order: sortOrder,
    });
  };

  // T079: Toggle ascending/descending
  const handleToggleOrder = () => {
    onSortChange({
      sort_by: sortBy,
      sort_order: sortOrder === 'asc' ? 'desc' : 'asc',
    });
  };

  return (
    <div className={cn('flex items-center gap-1', className)}>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <ArrowUpDown className="h-4 w-4" />
            <span className="hidden sm:inline">Sort by:</span>
            <span className="font-medium">{currentOption?.label || 'Created Date'}</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-48">
          {SORT_OPTIONS.map((option) => (
            <DropdownMenuItem
              key={option.value}
              onClick={() => handleSortFieldChange(option.value)}
              className="flex items-center justify-between"
            >
              <span>{option.label}</span>
              {sortBy === option.value && (
                <Check className="h-4 w-4 text-primary" />
              )}
            </DropdownMenuItem>
          ))}
          <DropdownMenuSeparator />
          <DropdownMenuItem
            onClick={handleToggleOrder}
            className="flex items-center justify-between"
          >
            <span>Order</span>
            <span className="flex items-center gap-1 text-muted-foreground">
              {sortOrder === 'asc' ? (
                <>
                  <ArrowUp className="h-3 w-3" />
                  Ascending
                </>
              ) : (
                <>
                  <ArrowDown className="h-3 w-3" />
                  Descending
                </>
              )}
            </span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Quick toggle button for order */}
      <Button
        variant="ghost"
        size="sm"
        onClick={handleToggleOrder}
        className="px-2"
        title={sortOrder === 'asc' ? 'Switch to Descending' : 'Switch to Ascending'}
      >
        {sortOrder === 'asc' ? (
          <ArrowUp className="h-4 w-4" />
        ) : (
          <ArrowDown className="h-4 w-4" />
        )}
      </Button>
    </div>
  );
}
