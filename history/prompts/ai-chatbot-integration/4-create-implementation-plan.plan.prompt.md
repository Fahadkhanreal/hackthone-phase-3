---
id: 4
title: create-implementation-plan
stage: plan
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-chatbot-integration
branch: 1-ai-chatbot-integration
user: Governor Sindh It Initiative
command: /sp.plan
labels: ["plan", "ai-chatbot", "architecture", "todo-app"]
links:
  spec: specs/1-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-ai-chatbot-integration/impl/plan.md
 - specs/1-ai-chatbot-integration/impl/research.md
 - specs/1-ai-chatbot-integration/impl/data-model.md
 - specs/1-ai-chatbot-integration/impl/contracts/mcp-tools.json
 - specs/1-ai-chatbot-integration/impl/contracts/chat-api.json
 - specs/1-ai-chatbot-integration/impl/quickstart.md
tests:
 - none
---

## Prompt

```
before planning first you can review the frontend and backend folder after that generate plan here is plan : /sp.plan

Project phase: Phase III – Todo AI Chatbot (full integration into existing Todo app)

Goal: Extend the existing full-stack Todo application with a natural-language AI chatbot that uses Cohere as the LLM provider, exposes 5 MCP tools, persists conversation state in Neon DB, and displays a floating chatbot icon in the Next.js dashboard that opens the OpenAI ChatKit conversation window. Everything must remain stateless on the server, secured with JWT, and generated via Claude Code.

High-level phases & execution order:

Phase 1 – Database & Model Extensions
- Add Conversation model (user_id: UUID, id: UUID, created_at, updated_at)
- Add Message model (user_id: UUID, id: UUID, conversation_id: UUID, role: str ("user"|"assistant"), content: str, created_at)
- Update database.py / startup event to create these new tables automatically
- Reuse existing Task model and SQLModel engine/session
- Create simple helper functions to fetch/save conversation history by user_id

Phase 2 – MCP Server & Tools Implementation
- Create /backend/mcp_server/ folder
- Use official MCP Python SDK (FastMCP preferred)
- Define exactly 5 stateless tools in /backend/mcp_tools/ (one file per tool):
  1. add_task(user_id, title, description=None) → {"task_id": str, "status": "created", "title": str}
  2. list_tasks(user_id, status="all") → list of {"id": str, "title": str, "completed": bool}
  3. complete_task(user_id, task_id) → {"task_id": str, "status": "completed", "title": str}
  4. delete_task(user_id, task_id) → {"task_id": str, "status": "deleted", "title": str}
  5. update_task(user_id, task_id, title=None, description=None) → {"task_id": str, "status": "updated", "title": str}
- Each tool must:
  - Inject SQLModel AsyncSession
  - Strictly filter by user_id
  - Raise clear exceptions on not found / ownership violation
- Register all 5 tools in MCP server with proper JSON schemas
- Expose MCP server (e.g., via FastAPI sub-app or separate process)

Phase 3 – Cohere Agent & Chat Endpoint
- Adapt OpenAI Agents SDK style to Cohere (use langchain-cohere or direct Cohere tool calling)
- Create /backend/agents/todo_agent.py
  - Define Agent with Cohere model (command-r-plus or command-r recommended)
  - Bind the 5 MCP tools
  - System prompt: detailed instructions for task CRUD detection + email response + confirmation + error handling + tool chaining
- Create /backend/routers/chat.py
  - POST /api/{user_id}/chat (protected by JWT dependency)
  - Extract user_id and email from JWT payload
  - If no conversation_id → create new Conversation
  - Fetch history from DB
  - Store incoming user message
  - Run Cohere agent with history + new message + user context
  - Store assistant response + any tool_calls
  - Return: {"conversation_id": str, "response": str, "tool_calls": list}

Phase 4 – Frontend Chatbot Integration
- Create floating chatbot icon component (ChatbotIcon.tsx) – fixed bottom-right, clickable, responsive
- Add icon to dashboard layout (/app/dashboard/layout.tsx or page.tsx)
- On click → open ChatKit conversation window
- Configure OpenAI ChatKit (custom/embeddable mode)
  - Connect to backend /api/{user_id}/chat endpoint
  - Attach JWT Bearer token to every request (use auth session from Better Auth)
  - Handle conversation_id persistence (store in localStorage or session)
- Add loading/error states in chat UI
- Display tool confirmations naturally in responses

Phase 5 – Cross-cutting Standards & Polish
- Environment variables: COHERE_API_KEY, NEXT_PUBLIC_OPENAI_DOMAIN_KEY, etc.
- Security: every DB query and tool call filtered by user_id from JWT
- Error handling: 401/403 on auth mismatch, 404 on task not found, graceful agent errors
- README updates: Cohere setup, domain allowlist steps, full run instructions
- Test flow: login → open chat icon → "add task buy milk" → see confirmation → "show pending" → restart server → resume chat

Execution notes:
- All code must be generated via Claude Code tasks – no manual writing
- Use existing JWT dependency for auth
- Prefer async SQLMod
```

## Response snapshot

Created a comprehensive implementation plan for the Todo AI Chatbot integration, including:
- Technical context analysis of existing frontend/backend structure
- Research summary addressing all unknowns (Cohere integration, MCP server, ChatKit, etc.)
- Data model documentation for Conversation and Message entities
- API contracts for MCP tools and chat endpoint
- Quickstart guide for developers
- Detailed phased approach covering all required functionality

The plan addresses all constitutional principles including security, statelessness, Cohere API usage, and agentic workflow adherence.

## Outcome

- ✅ Impact: Complete implementation plan with all necessary design artifacts
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/*.json, quickstart.md
- 🔁 Next prompts: Ready to proceed with task generation using /sp.tasks
- 🧠 Reflection: Plan comprehensively covers all aspects of AI chatbot integration while maintaining security and architectural consistency

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard plan creation
- Next experiment (smallest change to try): Generate implementation tasks for the AI chatbot feature