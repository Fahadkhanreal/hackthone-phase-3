<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: Correctness, Security, Maintainability, Agentic Workflow Adherence
- Added sections: Natural Language Accuracy, Statelessness, Cohere API Usage
- Removed sections: None
- Templates requiring updates: ✅ Updated .specify/templates/plan-template.md
- Templates requiring updates: ✅ Updated .specify/templates/spec-template.md
- Templates requiring updates: ✅ Updated .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Todo AI Chatbot (Phase 3) – Natural Language Task Management with Cohere Constitution

## Core Principles

### Correctness
All functionality must work as specified, including MCP tool calls, user isolation, authentication, and natural language intent detection.
<!-- Rationale: The AI chatbot must reliably perform all required operations without errors or data corruption -->

### Security
Enforce strict user-task ownership and proper JWT validation on every protected endpoint; every MCP tool call must enforce user_id from JWT with no cross-user data access.
<!-- Rationale: Multi-user applications require robust security measures to prevent unauthorized access and data breaches -->

### Maintainability
Clean, modular, well-documented code following best practices for Next.js + FastAPI + Cohere integration.
<!-- Rationale: Code must be easy to understand, modify, and extend by current and future team members -->

### Reproducibility
All setup steps, environment variables, and deployment instructions must be clear and repeatable.
<!-- Rationale: Team members and external users must be able to consistently reproduce the development and production environments -->

### Agentic Workflow Adherence
No manual coding allowed; every file must be generated via Claude Code using Spec-Kit Plus.
<!-- Rationale: Following the agentic workflow ensures consistency, automation, and proper documentation of all development activities -->

### Natural Language Accuracy
Agent must correctly detect intent and call exact MCP tool based on user input.
<!-- Rationale: The AI chatbot must accurately interpret user requests and execute appropriate task operations -->

### Statelessness
Server holds zero memory; all conversation state in DB (conversations + messages tables).
<!-- Rationale: The system must be resilient and scalable by maintaining no server-side session state -->

### Cohere API Usage
Use Cohere API (not OpenAI) for all AI logic and tool calling.
<!-- Rationale: The project requires Cohere integration for consistent AI behavior and tool calling capabilities -->

## Key Standards
- Authentication: Use Better Auth (frontend) + JWT issuance/verification (backend) with shared secret
- API design: RESTful, fully documented, consistent naming, proper HTTP status codes
- Data persistence: Use Neon Serverless PostgreSQL with SQLModel ORM; all tables must have proper relationships and constraints
- AI Framework: Cohere API (chat completions with tool calling / function calling)
- MCP Server: Official MCP SDK (FastMCP or equivalent) exposing exactly 5 stateless tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Chat endpoint: POST /api/{user_id}/chat (JWT protected, returns conversation_id, response, tool_calls)
- Frontend: Responsive design (mobile-first), modern UI components, clear loading/error states
- Code quality: Type-safe (TypeScript + Python type hints), linting (ESLint + Ruff), consistent formatting (Prettier + Black)
- Security: Never expose sensitive data, validate all inputs, protect against common vulnerabilities (XSS, CSRF, etc.)
- Documentation: Every endpoint, model, and major component must have clear comments and README instructions

## Constraints
- Technology stack: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Cohere API
- No OpenAI anywhere — use Cohere for agent + tool calling
- MCP tools must be stateless and DB-injected
- Frontend: OpenAI ChatKit (or equivalent embeddable chat UI) with JWT attachment
- Environment variables: COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL
- No real-time (WebSocket) functionality
- No manual coding: All implementation must be done through the Agentic Dev Stack (spec → plan → tasks → Claude Code)
- Final deliverable: Fully working web application deployable to Vercel (frontend) + Render/Fly.io/Railway (backend) with Neon DB
- JWT secret must be managed via environment variable (BETTER_AUTH_SECRET) shared between frontend and backend

## Success Criteria
- All 5 MCP tools work correctly (add_task, list_tasks, complete_task, delete_task, update_task)
- Proper user authentication and session management
- Secure JWT token handling between frontend and backend
- Accurate natural language intent detection and tool calling
- Responsive UI that works across device sizes
- Proper data isolation between users
- Complete API documentation
- Successful deployment to target platforms
- Comprehensive error handling and validation
- Statelessness maintained (no server-side session memory)

## Governance
- All code must be generated through Claude Code using the Spec-Kit Plus workflow
- Any deviations from the established technology stack require explicit approval
- Changes to core principles require updating this constitution document
- Regular compliance reviews must verify adherence to all principles
- All development activities must be documented as Prompt History Records (PHRs)
- MCP tools must be stateless and DB-injected with user_id enforcement

**Version**: 2.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-02-03