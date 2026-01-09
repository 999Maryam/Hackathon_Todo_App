'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'; // Assuming we have a loading component

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading, checkAuthStatus } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Check auth status on component mount
    checkAuthStatus();
  }, [checkAuthStatus]);

  // If still loading, show a loading indicator
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!user) {
    // Redirect to login page - in a real app you might use Next.js redirect
    // For now, we'll use router.push
    router.push('/auth/login');
    return null; // Render nothing while redirecting
  }

  // If authenticated, render the children
  return <>{children}</>;
}