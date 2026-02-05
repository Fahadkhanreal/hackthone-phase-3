---
id: 1
title: "Create Project Constitution"
stage: constitution
date_iso: "2026-02-03"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels:
  - "constitution"
  - "todo-chatbot"
  - "cohere"
  - "mcp"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
prompt_text: |
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
response_text: |
  Created the project constitution file at .specify/memory/constitution.md with all the specified principles, standards, and constraints for the Todo AI Chatbot project. The constitution includes governance procedures, core principles (full integration, security first, stateless architecture, natural language accuracy, agentic workflow, Cohere API priority), key standards (AI framework, MCP server, chat endpoint, database, agent behavior), and constraints (technology stack, vendor, MCP tools, frontend, environment variables).
outcome: "Successfully created the project constitution file with all specified principles and guidelines."
evaluation: "The constitution file was created with all required sections and follows the expected structure."
---

# PHR: Create Project Constitution

## Summary
Created the initial project constitution for the Todo AI Chatbot project with all specified principles, standards, and constraints.

## Action Taken
Generated .specify/memory/constitution.md with comprehensive governance, core principles, standards, and constraints as specified by the user.

## Files Created/Modified
- .specify/memory/constitution.md