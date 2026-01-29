/**
 * useAuth Hook - Authentication state management
 * Provides auth status, user data, and auth methods
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { authApi, getStoredUser, setSessionExpiredHandler } from '@/lib/api';
import type { User, LoginRequest, RegisterRequest } from '@/lib/types';
import { toast } from 'sonner';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Handle session expiry
  const handleSessionExpired = useCallback(() => {
    authApi.logout();
    setUser(null);
    toast.error('Session expired. Please sign in again.');
    router.push('/sign-in');
  }, [router]);

  // Set session expiry handler on mount
  useEffect(() => {
    setSessionExpiredHandler(handleSessionExpired);
  }, [handleSessionExpired]);

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
    }
    setIsLoading(false);
  }, []);

  // Refresh user data from server
  const refreshUser = useCallback(async () => {
    if (!authApi.isAuthenticated()) {
      setUser(null);
      return;
    }

    try {
      const userData = await authApi.me();
      setUser(userData);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      // Token might be expired, clear auth
      authApi.logout();
      setUser(null);
    }
  }, []);

  // Login
  const login = useCallback(async (data: LoginRequest) => {
    setIsLoading(true);
    try {
      const response = await authApi.login(data);
      setUser(response.user);
      toast.success('Welcome back!');
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Login failed';
      toast.error(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Register
  const register = useCallback(async (data: RegisterRequest) => {
    setIsLoading(true);
    try {
      const response = await authApi.register(data);
      setUser(response.user);
      toast.success('Account created successfully!');
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Registration failed';
      toast.error(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Logout
  const logout = useCallback(() => {
    authApi.logout();
    setUser(null);
    toast.success('Logged out successfully');
  }, []);

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    refreshUser,
  };
}
