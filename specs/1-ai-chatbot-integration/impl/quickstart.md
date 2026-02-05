# Quickstart Guide: Todo AI Chatbot Integration

## Prerequisites
- Python 3.9+
- Node.js 18+
- Next.js 16+
- PostgreSQL (or Neon Serverless PostgreSQL)
- Cohere API key
- Better Auth configured

## Environment Setup

### Backend Environment Variables
Create or update `backend/.env`:
```env
COHERE_API_KEY=your_cohere_api_key_here
BETTER_AUTH_SECRET=your_better_auth_secret
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_app
```

### Frontend Environment Variables
Create or update `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_verification_key
```

## Installation Steps

### 1. Install Backend Dependencies
```bash
cd backend
pip install cohere-toolkit  # For MCP server
pip install cohere  # For AI integration
pip install python-jose[cryptography]  # Already installed for JWT
```

### 2. Update Database Schema
The new models (Conversation and Message) will be automatically created when the application starts, following the existing pattern in `backend/database.py`.

### 3. Start Backend Services
```bash
cd backend
uvicorn main:app --reload
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

## Key Components Overview

### Backend Structure
```
backend/
├── mcp_server/          # MCP server implementation
├── mcp_tools/           # 5 stateless tools implementation
├── agents/             # Cohere AI agent
│   └── todo_agent.py
├── routers/
│   └── chat.py         # Chat API endpoint
├── models.py           # Updated with Conversation/Message models
└── database.py         # Database connection (unchanged)
```

### Frontend Structure
```
frontend/
├── components/
│   └── ChatbotIcon.tsx # Floating chatbot icon
└── app/
    └── dashboard/      # ChatKit integration in dashboard
```

## Usage Flow

1. **Login**: User logs in through existing authentication
2. **Chat Icon Appears**: Floating chatbot icon appears in bottom-right of dashboard
3. **Open Chat**: Click icon to open OpenAI ChatKit interface
4. **Natural Language Commands**:
   - "Add a task: Buy groceries" → Creates new task
   - "Show my tasks" → Lists all tasks
   - "Complete task 1" → Marks task as completed
   - "Delete task 1" → Removes task
   - "Update task 1 to 'Buy organic groceries'" → Updates task
   - "Who am I?" → Responds with user's email from JWT

## Security Notes
- All API requests are JWT-protected
- Every database query filters by user_id from JWT
- MCP tools enforce user_id validation
- Conversation history is isolated by user

## Testing the Integration
1. Login to the application
2. Navigate to the dashboard
3. Click the floating chatbot icon
4. Try natural language commands like "Add task: Learn AI"
5. Verify the task appears in the main task list
6. Test conversation persistence by refreshing the page