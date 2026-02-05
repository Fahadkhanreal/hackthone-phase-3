
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Get the session to check if the user is authenticated
  const isAuthenticated = checkAuth(request);

  // Define protected routes that require authentication
  const protectedPaths = [
    /^\/dashboard(?:\/.*)?$/,  // Matches /dashboard and /dashboard/*
    /^\/profile(?:\/.*)?$/,    // Matches /profile and /profile/*
    // Add more protected routes as needed
  ];

  const isProtectedRoute = protectedPaths.some(pattern =>
    pattern.test(request.nextUrl.pathname)
  );

  // If user is not authenticated and tries to access a protected route
  if (isProtectedRoute && !isAuthenticated) {
    // Redirect to signin page
    const signInUrl = new URL('/signin', request.url);
    return NextResponse.redirect(signInUrl);
  }

  // If user is authenticated and tries to access auth pages, redirect to dashboard
  const authPaths = [/^\/signin(?:\/.*)?$/, /^\/signup(?:\/.*)?$/];
  const isAuthRoute = authPaths.some(pattern =>
    pattern.test(request.nextUrl.pathname)
  );

  if (isAuthenticated && isAuthRoute) {
    const dashboardUrl = new URL('/dashboard', request.url);
    return NextResponse.redirect(dashboardUrl);
  }

  // Continue with the request
  return NextResponse.next();
}

// Helper function to check if user is authenticated
function checkAuth(request: NextRequest): boolean {
  // This is a simplified check - in a real implementation,
  // you'd verify the JWT token from cookies or headers
  try {
    // Look for auth cookie or header
    const authCookie = request.cookies.get('better-auth-session');
    const authHeader = request.headers.get('authorization');

    // Return true if either auth cookie or header with bearer token exists
   return Boolean(authCookie) || Boolean(authHeader?.startsWith('Bearer '));
;
  } catch (error) {
    console.error('Auth check error:', error);
    return false;
  }
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};