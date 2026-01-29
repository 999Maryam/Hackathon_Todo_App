'use client';

/**
 * TagManager - CRUD UI for managing user tags.
 *
 * Phase V: User Story 3 - Tag Management (T050)
 */

import { useState } from 'react';
import { Plus, Pencil, Trash2, X, Check, Loader2, Tag as TagIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { TagWithCount, TagCreate } from '@/lib/types';
import { TagBadge } from './TagBadge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/Input';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

interface TagManagerProps {
  tags: TagWithCount[];
  isLoading?: boolean;
  onCreateTag: (data: TagCreate) => Promise<void>;
  onUpdateTag: (tagId: number, data: TagCreate) => Promise<void>;
  onDeleteTag: (tagId: number) => Promise<void>;
  className?: string;
}

/**
 * TagManager - Full tag management UI with create, edit, delete functionality.
 */
export function TagManager({
  tags,
  isLoading = false,
  onCreateTag,
  onUpdateTag,
  onDeleteTag,
  className,
}: TagManagerProps) {
  const [editingTagId, setEditingTagId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState('');
  const [newTagName, setNewTagName] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null);

  // Start editing a tag
  const startEditing = (tag: TagWithCount) => {
    setEditingTagId(tag.id);
    setEditValue(tag.name);
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingTagId(null);
    setEditValue('');
  };

  // Save edited tag
  const saveEdit = async () => {
    if (!editingTagId || !editValue.trim()) return;

    setIsSaving(true);
    try {
      await onUpdateTag(editingTagId, { name: editValue.trim() });
      cancelEditing();
    } finally {
      setIsSaving(false);
    }
  };

  // Create new tag
  const handleCreate = async () => {
    if (!newTagName.trim()) return;

    setIsSaving(true);
    try {
      await onCreateTag({ name: newTagName.trim() });
      setNewTagName('');
      setIsCreating(false);
    } finally {
      setIsSaving(false);
    }
  };

  // Delete tag
  const handleDelete = async (tagId: number) => {
    setIsSaving(true);
    try {
      await onDeleteTag(tagId);
      setDeleteConfirmId(null);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TagIcon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          <h3 className="font-medium text-slate-900 dark:text-slate-100">
            Manage Tags
          </h3>
          <span className="text-sm text-slate-500 dark:text-slate-400">
            ({tags.length})
          </span>
        </div>
        {!isCreating && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsCreating(true)}
          >
            <Plus className="w-4 h-4 mr-1" />
            New Tag
          </Button>
        )}
      </div>

      {/* Create New Tag Form */}
      {isCreating && (
        <div className="flex items-center gap-2 p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
          <Input
            value={newTagName}
            onChange={(e) => setNewTagName(e.target.value)}
            placeholder="Enter tag name..."
            className="flex-1"
            autoFocus
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleCreate();
              if (e.key === 'Escape') {
                setIsCreating(false);
                setNewTagName('');
              }
            }}
          />
          <Button
            size="sm"
            onClick={handleCreate}
            disabled={!newTagName.trim() || isSaving}
          >
            {isSaving ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Check className="w-4 h-4" />
            )}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setIsCreating(false);
              setNewTagName('');
            }}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      )}

      {/* Tags List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
        </div>
      ) : tags.length === 0 ? (
        <div className="text-center py-8 text-slate-500 dark:text-slate-400">
          <TagIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
          <p>No tags yet. Create your first tag to organize tasks.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {tags.map((tag) => (
            <div
              key={tag.id}
              className={cn(
                'flex items-center justify-between gap-2 p-3',
                'rounded-lg border border-slate-200 dark:border-slate-700',
                'hover:bg-slate-50 dark:hover:bg-slate-800/50',
                'transition-colors'
              )}
            >
              {editingTagId === tag.id ? (
                // Edit Mode
                <div className="flex items-center gap-2 flex-1">
                  <Input
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    className="flex-1"
                    autoFocus
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') saveEdit();
                      if (e.key === 'Escape') cancelEditing();
                    }}
                  />
                  <Button
                    size="sm"
                    onClick={saveEdit}
                    disabled={!editValue.trim() || isSaving}
                  >
                    {isSaving ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Check className="w-4 h-4" />
                    )}
                  </Button>
                  <Button variant="ghost" size="sm" onClick={cancelEditing}>
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ) : (
                // View Mode
                <>
                  <div className="flex items-center gap-3">
                    <TagBadge tag={tag} size="md" />
                    <span className="text-sm text-slate-500 dark:text-slate-400">
                      {tag.task_count} task{tag.task_count !== 1 ? 's' : ''}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => startEditing(tag)}
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setDeleteConfirmId(tag.id)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteConfirmId !== null}
        onOpenChange={(open) => !open && setDeleteConfirmId(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Tag</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this tag? It will be removed from
              all tasks. This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end gap-2 mt-4">
            <Button variant="outline" onClick={() => setDeleteConfirmId(null)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() => deleteConfirmId && handleDelete(deleteConfirmId)}
              disabled={isSaving}
            >
              {isSaving ? (
                <Loader2 className="w-4 h-4 animate-spin mr-2" />
              ) : null}
              Delete
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
