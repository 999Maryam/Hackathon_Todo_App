'use client';

import { useState, useEffect, useCallback } from 'react';
import { getCurrentUser, isAuthenticated as checkIsAuthenticated, login as authLogin, logout as authLogout, register as authRegister } from '@/lib/auth';

interface UserSession {
  userId: string;
  email: string;
  expiresAt: string;
  accessToken: string;
}

export const useAuth = () => {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check authentication status on mount and when needed
  const checkAuthStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const authenticated = await checkIsAuthenticated();
      if (authenticated) {
        const currentUser = await getCurrentUser();
        if (currentUser) {
          setUser({
            userId: currentUser.id,
            email: currentUser.email,
            expiresAt: currentUser.expiresAt || '',
            accessToken: '' // We don't expose the actual token for security
          });
        } else {
          setUser(null);
        }
      } else {
        setUser(null);
      }
    } catch (err) {
      console.error('Auth status check error:', err);
      setError('Failed to check authentication status');
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const result = await authLogin({
        email,
        password,
      });

      if (result?.user) {
        setUser({
          userId: result.user.id,
          email: result.user.email,
          expiresAt: result.user.expiresAt || '',
          accessToken: '' // We don't expose the actual token for security
        });
      }

      return result;
    } catch (err) {
      console.error('Login error:', err);
      setError(err instanceof Error ? err.message : 'Login failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // Register function
  const register = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const result = await authRegister({
        email,
        password,
      });

      if (result?.user) {
        setUser({
          userId: result.user.id,
          email: result.user.email,
          expiresAt: result.user.expiresAt || '',
          accessToken: '' // We don't expose the actual token for security
        });
      }

      return result;
    } catch (err) {
      console.error('Registration error:', err);
      setError(err instanceof Error ? err.message : 'Registration failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      setIsLoading(true);
      setError(null);

      await authLogout();
      setUser(null);
    } catch (err) {
      console.error('Logout error:', err);
      setError(err instanceof Error ? err.message : 'Logout failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // Check if user is authenticated
  const isAuthenticated = (): boolean => {
    return user !== null;
  };

  // Effect to check auth status on mount
  useEffect(() => {
    // Delay the auth check to prevent blocking initial render
    const timer = setTimeout(() => {
      checkAuthStatus();
    }, 500); // Small delay to allow initial render

    return () => clearTimeout(timer);
  }, [checkAuthStatus]);

  return {
    user,
    isLoading,
    error,
    isAuthenticated: !!user && !isLoading, // Determine based on user state instead of async call
    login,
    register,
    logout,
    checkAuthStatus,
  };
};

export default useAuth;