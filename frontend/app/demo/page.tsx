import Link from 'next/link';

export default function DemoHomePage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Component Demos</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link
            href="/demo/button"
            className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          >
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Button</h2>
            <p className="text-gray-600 dark:text-gray-400">Professional, responsive button component with variants, sizes, and loading states</p>
          </Link>
        </div>
      </div>
    </div>
  );
}