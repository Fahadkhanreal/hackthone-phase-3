'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../components/AuthProvider';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (isAuthenticated) {
    return null; // Redirect effect will handle this
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Navigation */}
      <nav className="px-4 py-4 sm:py-6 sm:px-6 lg:px-8 flex-shrink-0">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center max-w-7xl mx-auto gap-4">
          <div className="text-xl sm:text-2xl font-bold text-white text-center sm:text-left">
            Todo App
          </div>
          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 items-center">
            <Link
              href="/signin"
              className="px-3 py-2 sm:px-4 sm:py-2 text-sm font-medium text-white bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors duration-200 w-full sm:w-auto text-center"
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="px-3 py-2 sm:px-4 sm:py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors duration-200 w-full sm:w-auto text-center"
            >
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow flex flex-col">
        {/* Hero Section */}
        <section className="flex-grow flex flex-col items-center justify-center px-4 py-6 sm:py-8 md:py-16 sm:px-6 lg:px-8">
          <div className="max-w-4xl w-full text-center">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4 sm:mb-6 leading-tight">
              Organize Your Life
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                Stay Productive
              </span>
            </h1>

            <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-6 sm:mb-8 leading-relaxed max-w-2xl mx-auto">
              A beautiful and intuitive task management application designed to help you stay organized,
              focused, and productive. Track your tasks, manage your time, and achieve your goals.
            </p>

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center">
              <Link
                href="/signup"
                className="px-6 py-3 sm:px-8 sm:py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl w-full sm:w-auto text-center min-w-[200px] sm:min-w-[220px]"
              >
                Get Started - It's Free
              </Link>

              <Link
                href="/signin"
                className="px-6 py-3 sm:px-8 sm:py-4 bg-gray-800 hover:bg-gray-700 text-white font-semibold rounded-lg transition-all duration-200 border border-gray-600 w-full sm:w-auto text-center min-w-[200px] sm:min-w-[220px]"
              >
                Sign In to Your Account
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-12 px-4 sm:py-16 sm:px-6 lg:px-8 flex-shrink-0">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-8 sm:mb-12">
              <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white mb-3 sm:mb-4">
                Powerful Features for Your Productivity
              </h2>
              <p className="text-gray-400 max-w-xl mx-auto text-xs sm:text-sm md:text-base">
                Everything you need to manage your tasks efficiently and effectively
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
              {/* Feature 1 */}
              <div className="bg-gray-800/50 backdrop-blur-sm p-4 sm:p-6 rounded-xl border border-gray-700 hover:border-indigo-500 transition-all duration-300">
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-3 sm:mb-4 mx-auto">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-base sm:text-lg md:text-xl font-semibold text-white mb-1 sm:mb-2 text-center">Task Management</h3>
                <p className="text-gray-400 text-xs sm:text-sm md:text-base text-center">
                  Create, organize, and manage your tasks with ease. Set priorities and deadlines to stay on track.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-gray-800/50 backdrop-blur-sm p-4 sm:p-6 rounded-xl border border-gray-700 hover:border-indigo-500 transition-all duration-300">
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-3 sm:mb-4 mx-auto">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-base sm:text-lg md:text-xl font-semibold text-white mb-1 sm:mb-2 text-center">Secure & Private</h3>
                <p className="text-gray-400 text-xs sm:text-sm md:text-base text-center">
                  Your data is protected with enterprise-grade security. We respect your privacy and keep your information safe.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-gray-800/50 backdrop-blur-sm p-4 sm:p-6 rounded-xl border border-gray-700 hover:border-indigo-500 transition-all duration-300">
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-3 sm:mb-4 mx-auto">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h3 className="text-base sm:text-lg md:text-xl font-semibold text-white mb-1 sm:mb-2 text-center">Free Forever</h3>
                <p className="text-gray-400 text-xs sm:text-sm md:text-base text-center">
                  Enjoy all features completely free. No hidden charges, no premium tiers, just a great experience.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-12 px-4 sm:py-16 sm:px-6 lg:px-8 flex-shrink-0">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white mb-3 sm:mb-4">
              Ready to boost your productivity?
            </h2>
            <p className="text-gray-400 mb-6 sm:mb-8 text-sm sm:text-base md:text-lg max-w-xl mx-auto">
              Join thousands of users who have transformed the way they manage their tasks
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center">
              <Link
                href="/signup"
                className="px-6 py-3 sm:px-8 sm:py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl w-full sm:w-auto text-center min-w-[180px] sm:min-w-[220px]"
              >
                Create Free Account
              </Link>
              <Link
                href="/signin"
                className="px-6 py-3 sm:px-8 sm:py-4 bg-gray-800 hover:bg-gray-700 text-white font-semibold rounded-lg transition-all duration-200 border border-gray-600 w-full sm:w-auto text-center min-w-[180px] sm:min-w-[220px]"
              >
                Sign In
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-6 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center text-center sm:text-left">
            <div className="text-white font-semibold text-sm sm:text-base md:text-lg mb-2 sm:mb-0">
              Todo App
            </div>
            <div className="text-gray-400 text-xs sm:text-sm">
              © {new Date().getFullYear()} Todo App. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}