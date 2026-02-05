---
id: 2
title: update-project-constitution-for-ai-chatbot
stage: constitution
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-chatbot
branch: main
user: Governor Sindh It Initiative
command: /sp.constitution
labels: ["constitution", "governance", "todo-chatbot", "cohere"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution
Project: Todo AI Chatbot (Phase 3) – Natural Language Task Management with Cohere

Core principles:
- Full integration with existing backend: FastAPI, SQLModel, Neon PostgreSQL, Better Auth (JWT), multi-user isolation
- Security first: Every MCP tool call must enforce user_id from JWT; no cross-user data access
- Stateless everywhere: Server holds zero memory; all conversation state in DB (conversations + messages tables)
- Natural language accuracy: Agent must correctly detect intent and call exact MCP tool
- Agentic workflow adherence: No manual coding; every file generated via Claude Code + Spec-Kit Plus
- Use Cohere API (not OpenAI) for all AI logic and tool calling

Key standards:
- AI Framework: Cohere API (chat completions with tool calling / function calling)
- MCP Server: Official MCP SDK (FastMCP or equivalent) exposing exactly 5 stateless tools:
  - add_task (user_id, title, description?)
  - list_tasks (user_id, status: all/pending/completed)
  - complete_task (user_id, task_id)
  - delete_task (user_id, task_id)
  - update_task (user_id, task_id, title?, description?)
- Chat endpoint: POST /api/{user_id}/chat (JWT protected, returns conversation_id, response, tool_calls)
- Database: Reuse Task model + add Conversation & Message models
- Agent behavior: Intent detection → tool call(s) → friendly confirmation → handle errors gracefully
- Extra: If user asks about their email → respond directly from JWT payload (no tool needed)
- Code quality: Type hints, clear error messages, consistent formatting (Ruff/Black)

Constraints:
- Technology stack fixed: FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Cohere API (COHERE_API_KEY env var)
- No OpenAI anywhere — use Cohere for agent + tool calling
- MCP tools must be stateless and DB-injected
- Frontend: OpenAI ChatKit (or equivalent embeddable chat UI) with JWT attachment
- Environment variables: COHERE_API_KEY=jtpSdGy2vzXBlTRGc5fOB2gRts41jlhtbDtEDUqs, BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL
- No real-time (WebSocke
```

## Response snapshot

Updated the project constitution to reflect the Todo AI Chatbot (Phase 3) requirements, including:
- Added new principles for Natural Language Accuracy, Statelessness, and Cohere API Usage
- Updated existing principles to incorporate MCP tool calls and JWT enforcement
- Added key standards for Cohere API integration and MCP server requirements
- Updated constraints to include Cohere API usage and MCP tools requirements
- Enhanced success criteria to include MCP tools functionality and statelessness

## Outcome

- ✅ Impact: Updated constitution to reflect Todo AI Chatbot (Phase 3) requirements with Cohere API integration
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with version 2.0.0
- 🔁 Next prompts: Continue with spec, plan, and tasks generation for the Todo AI Chatbot
- 🧠 Reflection: Constitution now properly reflects the new project direction with AI chatbot functionality

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard constitution update
- Next experiment (smallest change to try): Generate spec for Todo AI Chatbot