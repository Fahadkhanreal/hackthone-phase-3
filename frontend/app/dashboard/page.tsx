'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../components/AuthProvider';
import TaskList from '../../components/TaskList';
import ChatbotIcon from '../../components/ChatbotIcon';
import ChatWindow from '../../components/ChatWindow';
import { apiGet, apiPost, apiPut, apiDelete, apiPatch } from '../../lib/api';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);

  const router = useRouter();
  const { user, isLoading: authLoading, isAuthenticated, signOut } = useAuth();

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/');
    }
  }, [authLoading, isAuthenticated, router]);

  // Fetch tasks when component mounts
  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    if (!user?.id) return;

    try {
      setLoading(true);
      // Fetch tasks from the backend API
      const tasksData = await apiGet<Task[]>(`/api/${user.id}/tasks`);
      setTasks(tasksData);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      console.error('Fetch tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTaskSubmit = async (title: string) => {
    try {
      // Call the API to create a task
      const newTask = await apiPost<Task>(`/api/${user.id}/tasks/`, {
        title: title,
        completed: false,
      });

      setTasks([...tasks, newTask]);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Create task error:', err);
    }
  };

  const toggleTaskCompletion = async (taskId: string) => {
    try {
      // Call the API to update the task
      const updatedTask = await apiPatch<Task>(`/api/${user.id}/tasks/${taskId}/complete`, {});

      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Update task error:', err);
    }
  };

  const deleteTask = async (taskId: string) => {
    try {
      // Call the API to delete the task
      await apiDelete(`/api/${user.id}/tasks/${taskId}`);

      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      console.error('Delete task error:', err);
    }
  };

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <div className="w-12 h-12 border-t-2 border-b-2 border-indigo-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect effect will handle this
  }

  const handleChatIconClick = () => {
    setIsChatOpen(true);
  };

  const handleCloseChat = () => {
    setIsChatOpen(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <div className="border-b border-gray-700 bg-gray-800/30 backdrop-blur-sm">
        <div className="max-w-6xl px-4 mx-auto sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div>
              <h1 className="text-3xl font-bold text-white">Dashboard</h1>
              <p className="mt-1 text-gray-300">
                Welcome back, {user?.email || 'User'}! Here's your task overview.
              </p>
            </div>
            <button
              onClick={() => {
                signOut();
                router.push('/');
              }}
              className="px-6 py-2 font-medium text-white transition-all duration-200 transform rounded-lg bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl px-4 py-8 mx-auto sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-6 mb-8 md:grid-cols-3">
          <div className="p-6 border shadow-lg bg-gradient-to-br from-gray-800/70 to-gray-900/70 backdrop-blur-sm rounded-xl border-gray-700/50">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-gradient-to-r from-blue-600/30 to-indigo-700/30">
                <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-400">Total Tasks</p>
                <p className="text-2xl font-bold text-white">{tasks.length}</p>
              </div>
            </div>
          </div>

          <div className="p-6 border shadow-lg bg-gradient-to-br from-gray-800/70 to-gray-900/70 backdrop-blur-sm rounded-xl border-gray-700/50">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-gradient-to-r from-green-600/30 to-emerald-700/30">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-400">Completed</p>
                <p className="text-2xl font-bold text-white">{tasks.filter(task => task.completed).length}</p>
              </div>
            </div>
          </div>

          <div className="p-6 border shadow-lg bg-gradient-to-br from-gray-800/70 to-gray-900/70 backdrop-blur-sm rounded-xl border-gray-700/50">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-gradient-to-r from-amber-600/30 to-orange-700/30">
                <svg className="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-400">Pending</p>
                <p className="text-2xl font-bold text-white">{tasks.filter(task => !task.completed).length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 mb-6 text-red-200 border bg-gradient-to-br from-red-900/50 to-red-800/50 border-red-700/50 rounded-xl backdrop-blur-sm">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Task List Section */}
        <div className="overflow-hidden border shadow-xl bg-gradient-to-br from-gray-800/70 to-gray-900/70 backdrop-blur-sm rounded-xl border-gray-700/50">
          <div className="p-6 border-b border-gray-700/50">
            <h2 className="text-xl font-semibold text-white">Your Tasks</h2>
            <p className="mt-1 text-gray-400">Manage and track your daily activities</p>
          </div>
          <TaskList
            tasks={tasks}
            onCreateTask={handleCreateTaskSubmit}
            onToggleTask={toggleTaskCompletion}
            onDeleteTask={deleteTask}
            loading={loading}
          />
        </div>
      </div>

      {/* Chatbot components */}
      {!isChatOpen && user && (
        <ChatbotIcon onClick={handleChatIconClick} />
      )}
      {user && (
        <ChatWindow
          isOpen={isChatOpen}
          onClose={handleCloseChat}
          userId={user.id}
        />
      )}
    </div>
  );
}