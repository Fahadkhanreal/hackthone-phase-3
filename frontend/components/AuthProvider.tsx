'use client';

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { authClient } from '@/lib/auth';

// Define the shape of our auth context
interface AuthContextType {
  user: any | null;
  token: string | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  isAuthenticated: boolean;
}

// Create the auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Check session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        // Attempt to get session from auth client
        const session = await authClient.getSession();
        if (session) {
          setUser(session.user);
        } else {
          // If no session from auth client, try to reconstruct from localStorage
          const userId = localStorage.getItem('user_id');
          const userEmail = localStorage.getItem('user_email');
          if (userId || userEmail) {
            setUser({
              id: userId || '',
              email: userEmail || ''
            });
          }
        }
        // In a real implementation, you would get the JWT token
        // For now, we'll use a placeholder approach
        setToken(localStorage.getItem('better-auth-token'));
      } catch (error) {
        console.error('Error checking session:', error);
        // Clear any invalid session data
        setUser(null);
        setToken(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  // Sign in function
  const signIn = async (email: string, password: string) => {
    try {
      // Call auth client sign in
      const result = await authClient.signIn.email({
        email,
        password,
        callbackURL: '/dashboard',
      });

      if (result) {
        // Update user and token state
        setUser(result.user || { id: localStorage.getItem('user_id'), email: localStorage.getItem('user_email') });
        // Get the JWT token from localStorage where our auth client stores it
        const token = localStorage.getItem('better-auth-token');
        setToken(token);
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  // Sign up function
  const signUp = async (email: string, password: string) => {
    try {
      // Call auth client sign up
      const result = await authClient.signUp.email({
        email,
        password,
        callbackURL: '/dashboard',
      });

      if (result) {
        // Update user and token state
        setUser(result.user || { id: localStorage.getItem('user_id'), email: localStorage.getItem('user_email') });
        // Get the JWT token from localStorage where our auth client stores it
        const token = localStorage.getItem('better-auth-token');
        setToken(token);
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  // Sign out function
  const signOut = async () => {
    try {
      // Call auth client sign out
      await authClient.signOut();

      // Clear local state
      setUser(null);
      setToken(null);
      localStorage.removeItem('better-auth-token');
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  };

  // Check if user is authenticated
  const isAuthenticated = !!user && !!token;

  // Provide the auth context to children
  const value: AuthContextType = {
    user,
    token,
    isLoading,
    signIn,
    signUp,
    signOut,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook to use the auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}