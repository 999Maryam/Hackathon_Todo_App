import Link from 'next/link';

export default function DemoLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      <nav className="bg-gray-100 dark:bg-gray-800 p-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Component Demos</h1>
          <ul className="flex space-x-4">
            <li>
              <Link href="/demo/button" className="text-blue-600 hover:underline dark:text-blue-400">
                Button
              </Link>
            </li>
          </ul>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
}