'use client';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

interface TaskItemProps {
  task: Task;
  onToggleTask: (id: string) => void;
  onDeleteTask: (id: string) => void;
}

export default function TaskItem({ task, onToggleTask, onDeleteTask }: TaskItemProps) {
  return (
    <div
      className={`flex items-center justify-between p-3 sm:p-4 bg-gradient-to-r ${
        task.completed
          ? 'from-gray-800/40 to-gray-900/40 opacity-70 border border-gray-700/50'
          : 'from-gray-800/50 to-gray-900/50 border border-gray-700/50'
      } rounded-xl transition-all duration-200 hover:from-gray-800/60 hover:to-gray-900/60 shadow-sm`}
    >
      <div className="flex items-center flex-1 min-w-0">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleTask(task.id)}
          className="h-4 w-4 sm:h-5 sm:w-5 text-blue-500 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer flex-shrink-0"
        />
        <span
          className={`ml-2 sm:ml-3 flex-1 min-w-0 truncate ${task.completed ? 'line-through text-gray-400' : 'text-gray-200 font-medium'}`}
        >
          {task.title}
        </span>
      </div>
      <button
        onClick={() => onDeleteTask(task.id)}
        className="ml-2 sm:ml-4 p-1.5 sm:p-2 text-red-400 hover:text-red-300 hover:bg-red-900/30 rounded-lg transition-colors duration-200 hover:scale-110 flex-shrink-0"
        aria-label="Delete task"
      >
        <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}