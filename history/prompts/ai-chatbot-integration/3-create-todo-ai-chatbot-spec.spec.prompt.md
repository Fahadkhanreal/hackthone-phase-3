---
id: 3
title: create-todo-ai-chatbot-spec
stage: spec
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-chatbot-integration
branch: 1-ai-chatbot-integration
user: Governor Sindh It Initiative
command: /sp.specify
labels: ["spec", "ai-chatbot", "todo-app", "cohere"]
links:
  spec: specs/1-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-ai-chatbot-integration/spec.md
 - specs/1-ai-chatbot-integration/checklists/requirements.md
tests:
 - none
---

## Prompt

```
/sp.specify Phase III – Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)
Target audience: Hackathon judges evaluating the agentic development process, secure multi-user architecture, LLM integration with Cohere, MCP tool implementation, stateless design, and seamless full-stack integration.
Focus: Extend the existing multi-user Todo web application (Next.js frontend + FastAPI backend + Better Auth + Neon PostgreSQL) by adding an AI-powered chatbot that manages tasks through natural language. The chatbot must be fully integrated into the existing app, use Cohere as the LLM provider, adapt OpenAI Agents SDK style code to work with Cohere, expose exactly 5 MCP tools, and display a floating chatbot icon in the UI that opens a conversation window.
Success criteria:

After login, a floating chatbot icon appears in the bottom-right corner of the dashboard (clickable, responsive, modern design)
Clicking the icon opens the OpenAI ChatKit chat interface (conversation window)
The chatbot understands natural language commands to add, list, complete, delete, and update tasks
All operations use exactly 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
Every action is confirmed with a friendly message (example: "Task added: Buy groceries ✅")
When the user asks about their identity or email (e.g. "Who am I?" or "What is my email?"), the bot correctly responds with the logged-in user's email from JWT
Conversations are persistent — history loads from the database even after page refresh or server restart
All chat requests are protected by JWT (user_id in path must match token)
The existing task CRUD REST endpoints and UI remain fully functional and unaffected
Cohere API is used successfully for agent reasoning and tool calling

Constraints:

LLM: Must use Cohere API (COHERE_API_KEY) — no OpenAI, Gemini, DeepSeek, or other providers
Agent style: Adapt the OpenAI Agents SDK pattern (Agent + Runner + tool calling) to work with Cohere (using langchain-cohere or direct Cohere client)
MCP: Use official MCP Python SDK (FastMCP recommended) to expose exactly 5 stateless tools
Frontend: Next.js 16+ App Router + OpenAI ChatKit (embeddable or custom mode)
Backend: FastAPI, SQLModel, Neon PostgreSQL, Better Auth (JWT)
Required environment variables: COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_OPENAI_DOMAIN_KEY
Chat endpoint: POST /api/{user_id}/chat (JWT protected, stateless)
Chat history must be stored in new Conversation and Message tables
No additional task fields (only title, description, completed)
Domain allowlist configuration required for production ChatKit usage
No real-time features (WebSockets, live updates)

Not building:

Advanced authentication (social login, MFA, password reset)
Extra task features (due dates, priorities, categories, reminders, search)
Voice input/output
Complex multi-step workflows beyond basic task CRUD
Separate mobile application
Automated unit/integration tests (manual demo is sufficient)

Timeline: Complete within Pha
```

## Response snapshot

Created the feature specification for the Todo AI Chatbot integration. The specification includes:
- User scenarios with priorities (P1-P2) for chatbot interface access, natural language task management, user identity recognition, and persistent conversations
- Functional requirements covering all 13 required capabilities including JWT validation, MCP tools, conversation persistence, and Cohere API integration
- Success criteria with measurable outcomes for performance, accuracy, and user experience
- Key entities for Conversation, Message, and Task
- Edge cases for error handling and security considerations
- A quality checklist to validate the specification completeness

## Outcome

- ✅ Impact: Created comprehensive feature specification for AI chatbot integration with existing Todo app
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements.md in specs/1-ai-chatbot-integration/
- 🔁 Next prompts: Ready to proceed with planning using /sp.plan
- 🧠 Reflection: Specification covers all required functionality while maintaining focus on user value

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard spec creation
- Next experiment (smallest change to try): Generate implementation plan for the AI chatbot feature