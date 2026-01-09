'use client';

import { useState, useEffect, createContext, useContext } from 'react';
import { getAuthToken, setAuthToken, removeAuthToken } from '../lib/auth';
import axios from 'axios';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  getToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in on component mount
    const checkSession = async () => {
      try {
        const token = getAuthToken();
        if (token) {
          // Verify token and get user info from API
          const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/me`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.data) {
            setUser({
              id: response.data.id,
              email: response.data.email,
            });
          }
        }
      } catch (error) {
        console.error('Error checking session:', error);
        // Clear invalid token
        removeAuthToken();
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/login`, {
        email,
        password,
      });

      if (response.data && response.data.access_token) {
        setAuthToken(response.data.access_token);
        setUser({
          id: response.data.user.id,
          email: response.data.user.email,
        });
      } else {
        throw new Error('Sign in failed');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw new Error('Sign in failed');
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/register`, {
        email,
        password,
      });

      if (response.data && response.data.access_token) {
        setAuthToken(response.data.access_token);
        setUser({
          id: response.data.user.id,
          email: response.data.user.email,
        });
      } else {
        throw new Error('Sign up failed');
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw new Error('Sign up failed');
    }
  };

  const signOut = async () => {
    try {
      const token = getAuthToken();
      if (token) {
        await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/logout`, {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }
      // Clear tokens
      removeAuthToken();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const getToken = (): string | null => {
    return getAuthToken();
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    signIn,
    signUp,
    signOut,
    getToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;