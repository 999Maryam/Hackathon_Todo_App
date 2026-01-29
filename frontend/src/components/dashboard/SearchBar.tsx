'use client';

/**
 * SearchBar - Debounced search input for filtering tasks.
 *
 * Phase V: User Story 4 - Search Tasks (T057)
 */

import { useState, useEffect, useCallback } from 'react';
import { Search, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/button';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  debounceMs?: number;
  className?: string;
}

/**
 * SearchBar with debounced input for efficient API calls.
 *
 * Features:
 * - Debounced onChange to prevent excessive API calls
 * - Clear button when search has value
 * - Search icon for visual clarity
 * - Responsive design
 */
export function SearchBar({
  value,
  onChange,
  placeholder = 'Search tasks...',
  debounceMs = 300,
  className,
}: SearchBarProps) {
  const [localValue, setLocalValue] = useState(value);

  // Sync local value with prop value
  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  // Debounced onChange
  useEffect(() => {
    const timer = setTimeout(() => {
      if (localValue !== value) {
        onChange(localValue);
      }
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [localValue, debounceMs, onChange, value]);

  // Clear search
  const handleClear = useCallback(() => {
    setLocalValue('');
    onChange('');
  }, [onChange]);

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalValue(e.target.value);
  };

  // Handle key press (Enter to search immediately, Escape to clear)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onChange(localValue);
    } else if (e.key === 'Escape') {
      handleClear();
    }
  };

  return (
    <div className={cn('relative', className)}>
      {/* Search Icon */}
      <Search
        className={cn(
          'absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4',
          'text-slate-400 dark:text-slate-500',
          'pointer-events-none'
        )}
      />

      {/* Input */}
      <Input
        type="text"
        value={localValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className={cn(
          'pl-10 pr-10',
          'w-full sm:w-64 md:w-80',
          'transition-all duration-200',
          'focus:w-full sm:focus:w-80 md:focus:w-96'
        )}
        aria-label="Search tasks"
      />

      {/* Clear Button */}
      {localValue && (
        <Button
          type="button"
          variant="ghost"
          size="sm"
          onClick={handleClear}
          className={cn(
            'absolute right-1 top-1/2 -translate-y-1/2',
            'h-7 w-7 p-0',
            'text-slate-400 hover:text-slate-600',
            'dark:text-slate-500 dark:hover:text-slate-300'
          )}
          aria-label="Clear search"
        >
          <X className="w-4 h-4" />
        </Button>
      )}
    </div>
  );
}

/**
 * SearchBarCompact - Smaller version for mobile/toolbar use.
 */
export function SearchBarCompact({
  value,
  onChange,
  placeholder = 'Search...',
  className,
}: Omit<SearchBarProps, 'debounceMs'>) {
  return (
    <SearchBar
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      debounceMs={200}
      className={cn('w-full', className)}
    />
  );
}
