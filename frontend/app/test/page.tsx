'use client';

import React from 'react';

export default function TestPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Test Page</h1>
        <p className="text-gray-600">Frontend server is running!</p>
        <p className="text-sm text-gray-500 mt-4">Backend connection: {process.env.NEXT_PUBLIC_API_BASE_URL}</p>
      </div>
    </div>
  );
}