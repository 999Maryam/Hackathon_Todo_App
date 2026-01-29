'use client';

/**
 * TagPicker - Multi-select component for assigning tags to tasks.
 *
 * Phase V: User Story 3 - Tag Management (T049)
 */

import { useState, useRef, useEffect } from 'react';
import { Check, ChevronDown, Plus } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Tag, TagWithCount } from '@/lib/types';
import { TagBadge } from '@/components/tags/TagBadge';

interface TagPickerProps {
  availableTags: TagWithCount[];
  selectedTagIds: number[];
  onChange: (tagIds: number[]) => void;
  onCreateTag?: (name: string) => Promise<Tag | null>;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
}

/**
 * TagPicker - Multi-select dropdown for selecting and creating tags.
 */
export function TagPicker({
  availableTags,
  selectedTagIds,
  onChange,
  onCreateTag,
  label,
  placeholder = 'Select tags...',
  disabled = false,
  className,
}: TagPickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter tags based on search
  const filteredTags = availableTags.filter((tag) =>
    tag.name.toLowerCase().includes(search.toLowerCase())
  );

  // Check if search matches any existing tag exactly
  const exactMatch = availableTags.some(
    (tag) => tag.name.toLowerCase() === search.toLowerCase()
  );

  // Get selected tags
  const selectedTags = availableTags.filter((tag) => selectedTagIds.includes(tag.id));

  // Toggle tag selection
  const toggleTag = (tagId: number) => {
    if (selectedTagIds.includes(tagId)) {
      onChange(selectedTagIds.filter((id) => id !== tagId));
    } else {
      onChange([...selectedTagIds, tagId]);
    }
  };

  // Create new tag
  const handleCreateTag = async () => {
    if (!onCreateTag || !search.trim() || exactMatch) return;

    setIsCreating(true);
    try {
      const newTag = await onCreateTag(search.trim());
      if (newTag) {
        onChange([...selectedTagIds, newTag.id]);
        setSearch('');
      }
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className={cn('space-y-2', className)} ref={containerRef}>
      {label && (
        <label className="text-sm font-medium text-slate-900 dark:text-slate-100">
          {label}
        </label>
      )}

      <div className="relative">
        {/* Trigger - using div instead of button to allow nested remove buttons */}
        <div
          role="combobox"
          aria-expanded={isOpen}
          aria-haspopup="listbox"
          tabIndex={disabled ? -1 : 0}
          onClick={() => {
            if (disabled) return;
            setIsOpen(!isOpen);
            if (!isOpen) {
              setTimeout(() => inputRef.current?.focus(), 0);
            }
          }}
          onKeyDown={(e) => {
            if (disabled) return;
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              setIsOpen(!isOpen);
              if (!isOpen) {
                setTimeout(() => inputRef.current?.focus(), 0);
              }
            }
          }}
          className={cn(
            'w-full flex items-center justify-between gap-2 px-3 py-2 cursor-pointer',
            'rounded-md border border-slate-300 dark:border-slate-700',
            'bg-white dark:bg-slate-800',
            'text-slate-900 dark:text-slate-100',
            'hover:border-slate-400 dark:hover:border-slate-600',
            'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
            disabled && 'cursor-not-allowed opacity-50',
            'min-h-[42px]'
          )}
        >
          <div className="flex flex-wrap gap-1 flex-1">
            {selectedTags.length > 0 ? (
              selectedTags.map((tag) => (
                <TagBadge
                  key={tag.id}
                  tag={tag}
                  size="sm"
                  removable
                  onRemove={(id) => {
                    onChange(selectedTagIds.filter((tid) => tid !== id));
                  }}
                />
              ))
            ) : (
              <span className="text-slate-400 dark:text-slate-500">
                {placeholder}
              </span>
            )}
          </div>
          <ChevronDown
            className={cn(
              'w-4 h-4 text-slate-400 transition-transform shrink-0',
              isOpen && 'rotate-180'
            )}
          />
        </div>

        {/* Dropdown */}
        {isOpen && (
          <div className="absolute z-50 w-full mt-1 py-1 rounded-md border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-lg max-h-64 overflow-auto">
            {/* Search Input */}
            <div className="px-2 py-1.5 border-b border-slate-200 dark:border-slate-700">
              <input
                ref={inputRef}
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search or create tag..."
                className={cn(
                  'w-full px-2 py-1 text-sm rounded',
                  'border border-slate-200 dark:border-slate-600',
                  'bg-slate-50 dark:bg-slate-700',
                  'text-slate-900 dark:text-slate-100',
                  'placeholder:text-slate-400 dark:placeholder:text-slate-500',
                  'focus:outline-none focus:ring-1 focus:ring-blue-500'
                )}
              />
            </div>

            {/* Tag Options */}
            {filteredTags.length > 0 ? (
              <div className="py-1">
                {filteredTags.map((tag) => {
                  const isSelected = selectedTagIds.includes(tag.id);
                  return (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => toggleTag(tag.id)}
                      className={cn(
                        'w-full flex items-center justify-between gap-2 px-3 py-2 text-left',
                        'hover:bg-slate-100 dark:hover:bg-slate-700',
                        isSelected && 'bg-blue-50 dark:bg-blue-900/20'
                      )}
                    >
                      <div className="flex items-center gap-2">
                        <TagBadge tag={tag} size="sm" />
                        <span className="text-xs text-slate-500 dark:text-slate-400">
                          ({tag.task_count} task{tag.task_count !== 1 ? 's' : ''})
                        </span>
                      </div>
                      {isSelected && (
                        <Check className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      )}
                    </button>
                  );
                })}
              </div>
            ) : search && !exactMatch ? null : (
              <div className="px-3 py-2 text-sm text-slate-500 dark:text-slate-400">
                No tags found
              </div>
            )}

            {/* Create New Tag Option */}
            {search && !exactMatch && onCreateTag && (
              <div className="border-t border-slate-200 dark:border-slate-700 py-1">
                <button
                  type="button"
                  onClick={handleCreateTag}
                  disabled={isCreating}
                  className={cn(
                    'w-full flex items-center gap-2 px-3 py-2 text-left',
                    'hover:bg-slate-100 dark:hover:bg-slate-700',
                    'text-blue-600 dark:text-blue-400'
                  )}
                >
                  <Plus className="w-4 h-4" />
                  <span className="text-sm">
                    {isCreating ? 'Creating...' : `Create "${search}"`}
                  </span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
