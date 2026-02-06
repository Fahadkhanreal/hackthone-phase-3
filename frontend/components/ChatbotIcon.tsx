'use client';

import { useState } from 'react';
import { FaRobot } from 'react-icons/fa';

interface ChatbotIconProps {
  onClick: () => void;
}

export default function ChatbotIcon({ onClick }: ChatbotIconProps) {
  const [isVisible, setIsVisible] = useState(true);

  const handleClick = () => {
    onClick();
    // Hide the icon when chat is opened, let chat window handle visibility
    setIsVisible(false);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <button
      onClick={handleClick}
      className="fixed bottom-6 right-6 sm:bottom-6 sm:right-6 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white p-4 rounded-full shadow-xl z-50 transition-all duration-300 transform hover:scale-110 hover:rotate-12 focus:outline-none focus:ring-4 focus:ring-blue-500/50 animate-pulse"
      aria-label="Open chatbot"
    >
      <div className="relative">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        <span className="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center animate-ping">
          ●
        </span>
      </div>
    </button>
  );
}