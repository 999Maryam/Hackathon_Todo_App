/**
 * useTags Hook - Tag data fetching and management with SWR
 * Provides optimistic updates and cache management for tags
 *
 * Phase V: User Story 3 - Tag Management (T051)
 */

'use client';

import useSWR, { mutate } from 'swr';
import { tagsApi } from '@/lib/api';
import type { Tag, TagCreate, TagWithCount, TagListResponse } from '@/lib/types';
import { toast } from 'sonner';

interface UseTagsReturn {
  tags: TagWithCount[];
  isLoading: boolean;
  isError: boolean;
  error: Error | undefined;
  refresh: () => void;
  createTag: (data: TagCreate) => Promise<Tag | null>;
  updateTag: (tagId: number, data: TagCreate) => Promise<Tag | null>;
  deleteTag: (tagId: number) => Promise<boolean>;
  addTagToTask: (taskId: string, tagId: number) => Promise<boolean>;
  removeTagFromTask: (taskId: string, tagId: number) => Promise<boolean>;
}

/**
 * Hook for managing tags with SWR caching and optimistic updates
 */
export function useTags(userId: string | null): UseTagsReturn {
  // Create unique SWR key
  const swrKey = userId ? `/api/${userId}/tags` : null;

  // Fetcher function
  const fetcher = async (): Promise<TagListResponse> => {
    if (!userId) return { tags: [] };
    return tagsApi.list(userId);
  };

  // SWR hook for data fetching
  const { data, error, isLoading } = useSWR(swrKey, fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: true,
    dedupingInterval: 2000,
  });

  const tags = data?.tags || [];

  // Refresh function
  const refresh = () => {
    if (swrKey) {
      mutate(swrKey);
    }
  };

  // Create tag with optimistic update
  const createTag = async (tagData: TagCreate): Promise<Tag | null> => {
    if (!userId) {
      toast.error('User not authenticated');
      return null;
    }

    try {
      // Optimistic update - add temporary tag
      const tempTag: TagWithCount = {
        id: Date.now(), // Temporary ID
        user_id: userId,
        name: tagData.name,
        created_at: new Date().toISOString(),
        task_count: 0,
      };

      // Update cache optimistically
      mutate(swrKey, { tags: [...tags, tempTag] }, false);

      // Make API call
      const newTag = await tagsApi.create(userId, tagData);

      // Update cache with real data
      const updatedTags = tags.filter((t) => t.id !== tempTag.id);
      mutate(
        swrKey,
        { tags: [...updatedTags, { ...newTag, task_count: 0 }] },
        false
      );

      toast.success('Tag created successfully');
      return newTag;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to create tag';
      toast.error(message);
      return null;
    }
  };

  // Update tag with optimistic update
  const updateTag = async (
    tagId: number,
    tagData: TagCreate
  ): Promise<Tag | null> => {
    if (!userId) {
      toast.error('User not authenticated');
      return null;
    }

    try {
      // Find existing tag
      const existingTag = tags.find((t) => t.id === tagId);
      if (!existingTag) {
        toast.error('Tag not found');
        return null;
      }

      // Optimistic update
      const updatedTag: TagWithCount = {
        ...existingTag,
        name: tagData.name,
      };

      const updatedTags = tags.map((t) => (t.id === tagId ? updatedTag : t));
      mutate(swrKey, { tags: updatedTags }, false);

      // Make API call
      const result = await tagsApi.update(userId, tagId, tagData);

      // Update cache with real data
      const finalTags = tags.map((t) =>
        t.id === tagId ? { ...result, task_count: existingTag.task_count } : t
      );
      mutate(swrKey, { tags: finalTags }, false);

      toast.success('Tag updated successfully');
      return result;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to update tag';
      toast.error(message);
      return null;
    }
  };

  // Delete tag with optimistic update
  const deleteTag = async (tagId: number): Promise<boolean> => {
    if (!userId) {
      toast.error('User not authenticated');
      return false;
    }

    try {
      // Optimistic update
      const filteredTags = tags.filter((t) => t.id !== tagId);
      mutate(swrKey, { tags: filteredTags }, false);

      // Make API call
      await tagsApi.delete(userId, tagId);

      // Confirm cache update
      mutate(swrKey);

      toast.success('Tag deleted successfully');
      return true;
    } catch (error: unknown) {
      // Revert optimistic update on error
      mutate(swrKey);
      const message = error instanceof Error ? error.message : 'Failed to delete tag';
      toast.error(message);
      return false;
    }
  };

  // Add tag to task
  const addTagToTask = async (taskId: string, tagId: number): Promise<boolean> => {
    if (!userId) {
      toast.error('User not authenticated');
      return false;
    }

    try {
      await tagsApi.addTagToTask(userId, taskId, tagId);

      // Update tag counts
      const updatedTags = tags.map((t) =>
        t.id === tagId ? { ...t, task_count: t.task_count + 1 } : t
      );
      mutate(swrKey, { tags: updatedTags }, false);

      return true;
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to add tag to task';
      toast.error(message);
      return false;
    }
  };

  // Remove tag from task
  const removeTagFromTask = async (taskId: string, tagId: number): Promise<boolean> => {
    if (!userId) {
      toast.error('User not authenticated');
      return false;
    }

    try {
      await tagsApi.removeTagFromTask(userId, taskId, tagId);

      // Update tag counts
      const updatedTags = tags.map((t) =>
        t.id === tagId ? { ...t, task_count: Math.max(0, t.task_count - 1) } : t
      );
      mutate(swrKey, { tags: updatedTags }, false);

      return true;
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to remove tag from task';
      toast.error(message);
      return false;
    }
  };

  return {
    tags,
    isLoading,
    isError: !!error,
    error,
    refresh,
    createTag,
    updateTag,
    deleteTag,
    addTagToTask,
    removeTagFromTask,
  };
}
