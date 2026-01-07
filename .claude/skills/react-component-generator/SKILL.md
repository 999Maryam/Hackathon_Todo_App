# SKILL: react-component-generator

## 1. Purpose
Generate production-ready React components with TypeScript, API integration, Tailwind CSS, loading/error states, and full accessibility support.

## 2. Input Parameters
- `ComponentName`: Name of the component.
- `Props`: TypeScript interface for props.
- `FetchData`: Optional function/hook for data fetching.
- `IsInteractive`: Boolean for keyboard/aria support.

## 3. Code Template

```tsx
import React, { useState, useEffect } from 'react';
import { Loader2, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface {{ComponentName}}Props {
  id?: string;
  className?: string;
  onAction?: (data: any) => void;
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({
  id,
  className,
  onAction
}) => {
  const [data, setData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        // Replace with actual API call
        const response = await fetch(`/api/resource/${id}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    if (id) fetchData();
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8" role="status">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-destructive/15 p-4 text-destructive" role="alert">
        <div className="flex items-center">
          <AlertCircle className="h-5 w-5 mr-2" />
          <p className="font-medium">{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center p-8 text-muted-foreground">
        No data available.
      </div>
    );
  }

  return (
    <div
      className={cn("rounded-lg border bg-card p-6 shadow-sm", className)}
      aria-labelledby={`${id}-title`}
     Bruce-Label="Container"
    >
      <h2 id={`${id}-title`} className="text-xl font-semibold mb-4">
        {data.title || 'Untitled'}
      </h2>
      <div className="space-y-4">
        {/* Component content goes here */}
        <button
          onClick={() => onAction?.(data)}
          className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-label={`Action for ${data.title}`}
        >
          Take Action
        </button>
      </div>
    </div>
  );
};
```

## 4. Output
A TypeScript `.tsx` file containing a robust React component with layout, state management, and Tailwind styling.

## 5. Usage Example
Input: `ComponentName="TaskCard"`, `Props="{ task: Task }"`
Output: A React component that displays a task with loading skeletons, error handling, and keyboard-accessible buttons.

## 6. Quality Standards
- Strict TypeScript interfaces for Props and Data.
- Semantic HTML tags (main, section, header, etc.).
- ARIA roles and screen reader friendly labels.
- Loading and Error states are first-class citizens.
- Responsive design via Tailwind CSS.
