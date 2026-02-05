// Custom auth client that works with the existing backend JWT system
class CustomAuthClient {
  private baseUrl: string;

  constructor() {
this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'https://localhost:8000';
  }

  // Method to get current session (check if user is authenticated)
  async getSession(): Promise<{ user: any } | null> {
    try {
      // Check if we have a token in localStorage
      const token = localStorage.getItem('better-auth-token');

      if (!token) {
        return null;
      }

      // For now, we'll just return a mock session based on the stored token
      // In a real implementation, you'd validate the token with your backend
      return {
        user: {
          id: localStorage.getItem('user_id') || '',
          email: localStorage.getItem('user_email') || ''
        }
      };
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  }

  // Internal implementations of sign in and sign up
  private signInImpl = async (email: string, password: string): Promise<any> => {
    try {
      const response = await fetch(`${this.baseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();

      // Store the token and user info
      if (data.access_token) {
        localStorage.setItem('better-auth-token', data.access_token);
        localStorage.setItem('user_id', data.user_id || '');
        localStorage.setItem('user_email', data.user_email || '');
      }

      return data;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  }

  private signUpImpl = async (email: string, password: string): Promise<any> => {
    try {
      const response = await fetch(`${this.baseUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const data = await response.json();

      // Store the token and user info
      if (data.access_token) {
        localStorage.setItem('better-auth-token', data.access_token);
        localStorage.setItem('user_id', data.user_id || '');
        localStorage.setItem('user_email', data.user_email || '');
      }

      return data;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  }

  // Method for signing out
  async signOut(): Promise<void> {
    // Clear the stored token and user info
    localStorage.removeItem('better-auth-token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_email');
  }

  // Methods to match Better Auth API structure
  signIn = {
    email: (credentials: { email: string; password: string; callbackURL?: string }) => {
      return this.signInImpl(credentials.email, credentials.password);
    }
  }

  signUp = {
    email: (credentials: { email: string; password: string; callbackURL?: string }) => {
      return this.signUpImpl(credentials.email, credentials.password);
    }
  }
}

// Export the custom auth client instance
export const authClient = new CustomAuthClient();