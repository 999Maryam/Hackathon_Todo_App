'use client';

import React, { useState } from 'react';
import Button from '@/components/ui/Button';

const ButtonDemoPage = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    setIsLoading(true);
    // Simulate async operation
    setTimeout(() => {
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Button Component Demo</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Variants */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Variants</h2>
            <div className="space-y-4">
              <div className="flex flex-wrap gap-4 items-center">
                <Button variant="primary">Primary</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="destructive">Destructive</Button>
              </div>
            </div>
          </div>

          {/* Sizes */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Sizes</h2>
            <div className="space-y-4">
              <div className="flex flex-wrap gap-4 items-center">
                <Button size="sm">Small</Button>
                <Button size="md">Medium</Button>
                <Button size="lg">Large</Button>
              </div>
            </div>
          </div>

          {/* Loading State */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Loading State</h2>
            <div className="space-y-4">
              <div className="flex flex-wrap gap-4 items-center">
                <Button isLoading={isLoading} onClick={handleClick}>
                  {isLoading ? 'Loading...' : 'Click to Load'}
                </Button>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Click the button to see the loading state in action
              </p>
            </div>
          </div>

          {/* Disabled State */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Disabled State</h2>
            <div className="space-y-4">
              <div className="flex flex-wrap gap-4 items-center">
                <Button disabled>Disabled Primary</Button>
                <Button variant="secondary" disabled>
                  Disabled Secondary
                </Button>
                <Button variant="destructive" disabled>
                  Disabled Destructive
                </Button>
              </div>
            </div>
          </div>

          {/* Combined Examples */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg md:col-span-2">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Combined Examples</h2>
            <div className="flex flex-wrap gap-4 items-center">
              <Button variant="primary" size="lg">
                Large Primary
              </Button>
              <Button variant="secondary" size="sm">
                Small Secondary
              </Button>
              <Button variant="destructive" size="lg" isLoading>
                Loading Destructive
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ButtonDemoPage;