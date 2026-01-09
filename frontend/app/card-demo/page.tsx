'use client';

import React from 'react';
import { Card } from '@/components/ui/Card';

const CardDemoPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">Card Component Demo</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Default Card */}
          <Card
            header={
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Default Card</h2>
                <p className="text-sm text-gray-500">Standard card variant</p>
              </div>
            }
            footer={
              <div className="flex justify-between">
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  Cancel
                </button>
                <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm font-medium hover:bg-blue-700">
                  Save
                </button>
              </div>
            }
            className="w-full"
          >
            <p className="text-gray-700">
              This is the default card variant with subtle styling and minimal elevation.
            </p>
            <div className="mt-4 p-3 bg-gray-100 rounded text-sm">
              <p>Body content goes here</p>
            </div>
          </Card>

          {/* Elevated Card */}
          <Card
            variant="elevated"
            header={
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Elevated Card</h2>
                <p className="text-sm text-gray-500">With more visual prominence</p>
              </div>
            }
            footer={
              <div className="flex justify-between">
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  Back
                </button>
                <button className="bg-green-600 text-white px-3 py-1 rounded text-sm font-medium hover:bg-green-700">
                  Continue
                </button>
              </div>
            }
            className="w-full"
          >
            <p className="text-gray-700">
              This is the elevated card variant with more prominent shadow and visual presence.
            </p>
            <div className="mt-4 p-3 bg-gray-100 rounded text-sm">
              <p>Elevated card content</p>
            </div>
          </Card>

          {/* Card with Custom Styling */}
          <Card
            header={<h3 className="font-medium text-gray-900">Custom Styled Card</h3>}
            className="border-blue-300 bg-blue-50 w-full"
          >
            <p className="text-gray-700">
              This card demonstrates custom styling through the className prop.
            </p>
            <ul className="mt-2 space-y-1 text-sm text-gray-600">
              <li>• Custom border color</li>
              <li>• Custom background color</li>
              <li>• Additional padding</li>
            </ul>
          </Card>

          {/* Minimal Card */}
          <Card className="w-full">
            <div className="text-center py-6">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Minimal Card</h3>
              <p className="text-gray-600">
                This card has no header or footer, just body content.
              </p>
              <div className="mt-4 flex justify-center">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                  Status: Active
                </span>
              </div>
            </div>
          </Card>
        </div>

        {/* Full-width card */}
        <div className="mt-8">
          <Card
            header={
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-900">Full Width Card</h2>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  Featured
                </span>
              </div>
            }
          >
            <div className="prose prose-gray max-w-none">
              <p>
                This card spans the full width of its container. It demonstrates how the Card component
                can adapt to different layout requirements while maintaining consistent styling.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
                <div className="bg-gray-50 p-4 rounded">
                  <h4 className="font-medium text-gray-900">Feature 1</h4>
                  <p className="text-sm text-gray-600 mt-1">Description of feature 1</p>
                </div>
                <div className="bg-gray-50 p-4 rounded">
                  <h4 className="font-medium text-gray-900">Feature 2</h4>
                  <p className="text-sm text-gray-600 mt-1">Description of feature 2</p>
                </div>
                <div className="bg-gray-50 p-4 rounded">
                  <h4 className="font-medium text-gray-900">Feature 3</h4>
                  <p className="text-sm text-gray-600 mt-1">Description of feature 3</p>
                </div>
              </div>

              <div className="mt-6 flex justify-end">
                <button className="bg-indigo-600 text-white px-4 py-2 rounded font-medium hover:bg-indigo-700">
                  Take Action
                </button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CardDemoPage;