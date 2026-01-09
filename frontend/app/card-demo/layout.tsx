import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Card Component Demo',
  description: 'Demo of the Card component for the todo app',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}