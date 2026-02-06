'use client';

import { useState, useRef, useEffect } from 'react';
import { FaTimes, FaPaperPlane } from 'react-icons/fa';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant'; // 'user' or 'assistant'
  timestamp: Date;
}

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
}

export default function ChatWindow({ isOpen, onClose, userId }: ChatWindowProps) {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the same authentication method as the existing API calls
      let authToken = '';
      let baseUrl = typeof window !== 'undefined'
        ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
        : 'http://localhost:8000';

      // Ensure no trailing slash in base URL
      baseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;

      if (typeof window !== 'undefined') {
        authToken = localStorage.getItem('better-auth-token') || '';
      }

      const response = await fetch(`${baseUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          message: inputValue,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(), // Simple ID generation
        content: data.response,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-x-0 bottom-0 sm:inset-auto sm:bottom-24 sm:right-6 w-full sm:w-full sm:max-w-md h-[70vh] sm:h-[500px] sm:h-[600px] bg-gradient-to-b from-gray-800 to-gray-900 rounded-t-xl sm:rounded-xl shadow-2xl border border-gray-700 flex flex-col z-50 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 rounded-t-xl flex justify-between items-center">
        <h3 className="font-semibold text-lg flex items-center">
          <span className="mr-2">🤖</span> AI Task Assistant
        </h3>
        <button
          onClick={onClose}
          className="text-white hover:text-gray-200 focus:outline-none transition-colors duration-200"
          aria-label="Close chat"
        >
          <FaTimes className="text-xl" />
        </button>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-gray-900 to-gray-800 chat-messages-container">
        {messages.length === 0 ? (
          <div className="text-center text-gray-300 mt-4 sm:mt-8">
            <div className="text-4xl mb-4">👋</div>
            <p className="text-lg font-medium mb-2">Hello! I'm your AI task assistant.</p>
            <p className="mb-4">How can I help you today?</p>
            <div className="bg-gray-800/50 p-3 sm:p-4 rounded-lg border border-gray-700">
              <p className="font-medium mb-2 text-blue-300 text-sm sm:text-base">Try these commands:</p>
              <ul className="text-xs sm:text-sm space-y-1 text-left">
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>Add tasks: "Add a task: Buy groceries"</li>
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>List tasks: "Show my tasks"</li>
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>Complete tasks: "Complete task 1"</li>
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>Update tasks: "Update task 1"</li>
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>Delete tasks: "Delete task 1"</li>
                <li className="flex items-start"><span className="text-green-400 mr-2 text-xs">•</span>Ask: "Who am I?"</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`p-3 rounded-2xl max-w-[80%] ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-blue-600/30 to-blue-700/30 ml-auto border border-blue-500/30 backdrop-blur-sm'
                    : 'bg-gradient-to-r from-gray-700/50 to-gray-800/50 mr-auto border border-gray-600/30 backdrop-blur-sm'
                }`}
              >
                <div className="text-gray-100 text-sm sm:text-base">{message.content}</div>
                <div className="text-xs text-gray-400 mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="p-3 rounded-2xl bg-gradient-to-r from-gray-700/50 to-gray-800/50 mr-auto max-w-[80%] border border-gray-600/30 backdrop-blur-sm">
                <div className="flex items-center text-gray-300 text-sm">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-75"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150"></div>
                  </div>
                  <span className="ml-2">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="p-3 border-t border-gray-700 bg-gradient-to-b from-gray-800 to-gray-900">
        <div className="flex">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me to manage your tasks..."
            className="flex-1 bg-gray-700 text-white border border-gray-600 rounded-l-lg p-3 resize-none h-12 min-h-[48px] max-h-32 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400"
            disabled={isLoading}
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !inputValue.trim()}
            className={`bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-4 rounded-r-lg transition-all duration-200 ${
              isLoading || !inputValue.trim()
                ? 'opacity-50 cursor-not-allowed'
                : 'hover:from-blue-700 hover:to-indigo-800 active:scale-95'
            }`}
            aria-label="Send message"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
}