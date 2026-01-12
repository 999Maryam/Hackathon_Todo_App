/**
 * Task List Skeleton Component
 * Loading skeleton that matches the task list layout
 */

'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { Card } from '@/components/ui/Card';

interface TaskListSkeletonProps {
  count?: number;
}

export function TaskListSkeleton({ count = 5 }: TaskListSkeletonProps) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, index) => (
        <Card
          key={index}
          className="p-4 animate-pulse"
        >
          <div className="flex items-start gap-3">
            {/* Checkbox skeleton */}
            <Skeleton className="h-5 w-5 rounded mt-0.5 flex-shrink-0" />

            {/* Content skeleton */}
            <div className="flex-1 space-y-2">
              {/* Title skeleton */}
              <Skeleton className="h-5 w-3/4" />
              {/* Description skeleton - random width for variety */}
              <Skeleton
                className="h-4"
                style={{ width: `${60 + Math.random() * 30}%` }}
              />
            </div>

            {/* Action buttons skeleton */}
            <div className="flex gap-2 flex-shrink-0">
              <Skeleton className="h-8 w-8 rounded" />
              <Skeleton className="h-8 w-8 rounded" />
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
