import Link from 'next/link';
import React from 'react';

const ModalDemoIndex = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">Modal Component Demos</h1>

        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <div className="p-4 border border-gray-200 rounded-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Basic Modal Demo</h2>
            <p className="text-gray-600 mb-4">
              Demonstrates the core features of the Modal component with different sizes.
            </p>
            <Link
              href="/modal-demo"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              View Basic Demo →
            </Link>
          </div>

          <div className="p-4 border border-gray-200 rounded-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Todo App Modal Demo</h2>
            <p className="text-gray-600 mb-4">
              Shows how the Modal component can be used in a practical todo application.
            </p>
            <Link
              href="/modal-demo/todo-modal-demo"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              View Todo Demo →
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModalDemoIndex;