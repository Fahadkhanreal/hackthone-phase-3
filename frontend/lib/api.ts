import { authClient } from './auth';

/**
 * API client with JWT token attachment for authenticated requests
 */
class ApiClient {
  private baseUrl: string;

  constructor() {
    let base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Ensure no trailing slash in base
    this.baseUrl = base.endsWith('/') ? base.slice(0, -1) : base;

    console.log("API Base URL:", this.baseUrl);
  }

  /**
   * Generic API request method that automatically attaches JWT token
   */
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    // Get the current session to retrieve the JWT token
    const session = await this.getSession();

    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    if (session?.token) {
      headers.set('Authorization', `Bearer ${session.token}`);
    }

    // Construct the full URL (yahaan sahi jagah hai)
    const url = `${this.baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

    // Make the API request
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle 401 Unauthorized responses
    if (response.status === 401) {
      console.warn('Unauthorized request - token may be expired');
      throw new Error('Unauthorized: Please sign in again');
    }

    // Check if response is OK
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    // Return JSON response
    return response.json() as Promise<T>;
  }

  /**
   * Get current session with JWT token
   */
  private async getSession(): Promise<{ token: string } | null> {
    try {
      const token = localStorage.getItem('better-auth-token');
      if (token) {
        return { token };
      }
      return null;
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }
}

// Singleton instance
export const apiClient = new ApiClient();

// Export helpers
export const apiGet = <T>(endpoint: string) => apiClient.get<T>(endpoint);
export const apiPost = <T>(endpoint: string, data?: any) => apiClient.post<T>(endpoint, data);
export const apiPut = <T>(endpoint: string, data?: any) => apiClient.put<T>(endpoint, data);
export const apiDelete = <T>(endpoint: string) => apiClient.delete<T>(endpoint);
export const apiPatch = <T>(endpoint: string, data?: any) => apiClient.patch<T>(endpoint, data);




















































// import { authClient } from './auth';

// /**
//  * API client with JWT token attachment for authenticated requests
//  */
// class ApiClient {
//   private baseUrl: string;

//   // lib/api.ts mein constructor update karo
// constructor() {
//   let base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
//   // Ensure no trailing slash in base
//   this.baseUrl = base.endsWith('/') ? base.slice(0, -1) : base;
// }

// const url = `${this.baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

//   /**
//    * Generic API request method that automatically attaches JWT token
//    */
//   async request<T>(
//     endpoint: string,
//     options: RequestInit = {}
//   ): Promise<T> {
//     // Get the current session to retrieve the JWT token
//     const session = await this.getSession();

    
//    const headers = new Headers(options.headers);


// headers.set('Content-Type', 'application/json');


// if (session?.token) {
//   headers.set('Authorization', `Bearer ${session.token}`);
// }
//     // Construct the full URL
//     const url = `${this.baseUrl}${endpoint}`;

//     // Make the API request
//     const response = await fetch(url, {
//       ...options,
//       headers,
//     });

//     // Handle 401 Unauthorized responses
//     if (response.status === 401) {
//       // Optionally redirect to sign-in or clear session
//       console.warn('Unauthorized request - token may be expired');
//       throw new Error('Unauthorized: Please sign in again');
//     }

//     // Check if response is OK
//     if (!response.ok) {
//       throw new Error(`API request failed: ${response.status} ${response.statusText}`);
//     }

//     // Return JSON response
//     return response.json() as Promise<T>;
//   }

//   /**
//    * Get current session with JWT token
//    */
//   private async getSession(): Promise<{ token: string } | null> {
//     try {
//       // Get the token from localStorage where our auth client stores it
//       const token = localStorage.getItem('better-auth-token');

//       if (token) {
//         return { token };
//       }

//       return null;
//     } catch (error) {
//       console.error('Error getting session:', error);
//       return null;
//     }
//   }

//   /**
//    * GET request helper
//    */
//   async get<T>(endpoint: string): Promise<T> {
//     return this.request<T>(endpoint, {
//       method: 'GET',
//     });
//   }

//   /**
//    * POST request helper
//    */
//   async post<T>(endpoint: string, data?: any): Promise<T> {
//     return this.request<T>(endpoint, {
//       method: 'POST',
//       body: data ? JSON.stringify(data) : undefined,
//     });
//   }

//   /**
//    * PUT request helper
//    */
//   async put<T>(endpoint: string, data?: any): Promise<T> {
//     return this.request<T>(endpoint, {
//       method: 'PUT',
//       body: data ? JSON.stringify(data) : undefined,
//     });
//   }

//   /**
//    * DELETE request helper
//    */
//   async delete<T>(endpoint: string): Promise<T> {
//     return this.request<T>(endpoint, {
//       method: 'DELETE',
//     });
//   }

//   /**
//    * PATCH request helper
//    */
//   async patch<T>(endpoint: string, data?: any): Promise<T> {
//     return this.request<T>(endpoint, {
//       method: 'PATCH',
//       body: data ? JSON.stringify(data) : undefined,
//     });
//   }
// }

// // Create and export a singleton instance
// export const apiClient = new ApiClient();

// // Export individual helper functions
// export const apiGet = <T>(endpoint: string) => apiClient.get<T>(endpoint);
// export const apiPost = <T>(endpoint: string, data?: any) => apiClient.post<T>(endpoint, data);
// export const apiPut = <T>(endpoint: string, data?: any) => apiClient.put<T>(endpoint, data);
// export const apiDelete = <T>(endpoint: string) => apiClient.delete<T>(endpoint);
// export const apiPatch = <T>(endpoint: string, data?: any) => apiClient.patch<T>(endpoint, data);