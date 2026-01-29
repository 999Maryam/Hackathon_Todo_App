'use client';

/**
 * TagBadge - Display component for task tags.
 *
 * Phase V: User Story 3 - Tag Management (T048)
 */

import { X } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Tag } from '@/lib/types';

interface TagBadgeProps {
  tag: Tag;
  size?: 'sm' | 'md' | 'lg';
  removable?: boolean;
  onRemove?: (tagId: number) => void;
  className?: string;
}

// Color palette for tags (based on tag id for consistency)
const TAG_COLORS = [
  { bg: 'bg-blue-100 dark:bg-blue-900/30', text: 'text-blue-700 dark:text-blue-400', border: 'border-blue-200 dark:border-blue-800' },
  { bg: 'bg-purple-100 dark:bg-purple-900/30', text: 'text-purple-700 dark:text-purple-400', border: 'border-purple-200 dark:border-purple-800' },
  { bg: 'bg-pink-100 dark:bg-pink-900/30', text: 'text-pink-700 dark:text-pink-400', border: 'border-pink-200 dark:border-pink-800' },
  { bg: 'bg-indigo-100 dark:bg-indigo-900/30', text: 'text-indigo-700 dark:text-indigo-400', border: 'border-indigo-200 dark:border-indigo-800' },
  { bg: 'bg-cyan-100 dark:bg-cyan-900/30', text: 'text-cyan-700 dark:text-cyan-400', border: 'border-cyan-200 dark:border-cyan-800' },
  { bg: 'bg-teal-100 dark:bg-teal-900/30', text: 'text-teal-700 dark:text-teal-400', border: 'border-teal-200 dark:border-teal-800' },
  { bg: 'bg-orange-100 dark:bg-orange-900/30', text: 'text-orange-700 dark:text-orange-400', border: 'border-orange-200 dark:border-orange-800' },
  { bg: 'bg-rose-100 dark:bg-rose-900/30', text: 'text-rose-700 dark:text-rose-400', border: 'border-rose-200 dark:border-rose-800' },
];

const sizeConfig = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-0.5 text-sm',
  lg: 'px-2.5 py-1 text-base',
};

/**
 * Get consistent color for a tag based on its ID.
 */
function getTagColor(tagId: number) {
  return TAG_COLORS[tagId % TAG_COLORS.length];
}

/**
 * TagBadge - Displays a single tag with consistent color based on tag ID.
 */
export function TagBadge({
  tag,
  size = 'sm',
  removable = false,
  onRemove,
  className,
}: TagBadgeProps) {
  const colors = getTagColor(tag.id);

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full border font-medium',
        colors.bg,
        colors.text,
        colors.border,
        sizeConfig[size],
        className
      )}
    >
      <span className="truncate max-w-24">{tag.name}</span>
      {removable && onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove(tag.id);
          }}
          className={cn(
            'ml-0.5 hover:bg-black/10 dark:hover:bg-white/10 rounded-full p-0.5',
            'focus:outline-none focus:ring-1 focus:ring-offset-1'
          )}
          aria-label={`Remove ${tag.name} tag`}
        >
          <X className="w-3 h-3" />
        </button>
      )}
    </span>
  );
}

/**
 * TagList - Display a list of tags with optional "show more" functionality.
 */
interface TagListProps {
  tags: Tag[];
  maxVisible?: number;
  size?: 'sm' | 'md' | 'lg';
  removable?: boolean;
  onRemove?: (tagId: number) => void;
  className?: string;
}

export function TagList({
  tags,
  maxVisible = 3,
  size = 'sm',
  removable = false,
  onRemove,
  className,
}: TagListProps) {
  const visibleTags = tags.slice(0, maxVisible);
  const remainingCount = tags.length - maxVisible;

  return (
    <div className={cn('flex flex-wrap gap-1', className)}>
      {visibleTags.map((tag) => (
        <TagBadge
          key={tag.id}
          tag={tag}
          size={size}
          removable={removable}
          onRemove={onRemove}
        />
      ))}
      {remainingCount > 0 && (
        <span
          className={cn(
            'inline-flex items-center rounded-full border font-medium',
            'bg-slate-100 dark:bg-slate-800',
            'text-slate-600 dark:text-slate-400',
            'border-slate-200 dark:border-slate-700',
            sizeConfig[size]
          )}
          title={tags.slice(maxVisible).map((t) => t.name).join(', ')}
        >
          +{remainingCount}
        </span>
      )}
    </div>
  );
}
