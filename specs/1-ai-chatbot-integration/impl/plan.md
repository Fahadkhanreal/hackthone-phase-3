# Implementation Plan: Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)

**Feature Branch**: `1-ai-chatbot-integration`
**Created**: 2026-02-03
**Status**: Draft
**Specification**: specs/1-ai-chatbot-integration/spec.md

## Technical Context

### Known Architecture Elements
- **Frontend**: Next.js 16+ with App Router, deployed on Vercel
- **Backend**: FastAPI with SQLModel ORM, deployed on Render/Fly.io/Railway
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Existing Models**: User and Task models with proper relationships
- **Database Connection**: Async engine with session factory in database.py
- **JWT Handling**: Utilities in backend/auth/jwt_utils.py for token validation
- **Frontend Structure**: App Router with dashboard, signin, signup pages

### Unknowns / Need Clarification
- **OpenAI ChatKit Integration**: How to configure and connect with Next.js frontend
- **Cohere API Integration**: Specific implementation patterns for tool calling with langchain-cohere
- **MCP Server Setup**: Exact configuration for FastMCP with 5 stateless tools
- **Floating Chat Icon**: Best practices for implementation in Next.js with Tailwind CSS
- **Environment Variables**: Complete list needed for Cohere and ChatKit integration

### Dependencies & Integrations
- **Cohere API**: For AI reasoning and tool calling (COHERE_API_KEY)
- **Better Auth**: For JWT token validation and user identification
- **SQLModel**: For database operations with async sessions
- **FastAPI**: For API endpoint creation with JWT protection
- **OpenAI ChatKit**: For frontend chat interface (NEXT_PUBLIC_OPENAI_DOMAIN_KEY)

## Constitution Check

### Applied Principles
- ✅ **Security**: All DB queries and tool calls will be filtered by user_id from JWT
- ✅ **Statelessness**: Server holds zero memory; all conversation state in DB (conversations + messages tables)
- ✅ **Cohere API Usage**: Will use Cohere API (not OpenAI) for all AI logic and tool calling
- ✅ **Natural Language Accuracy**: Agent must correctly detect intent and call exact MCP tool
- ✅ **Agentic Workflow Adherence**: No manual coding; every file must be generated via Claude Code
- ✅ **Reproducibility**: Clear setup steps and environment variables

### Potential Violations
- **None identified**: All planned implementations align with constitutional principles

## Gates & Validation

### Gate 1: Architecture Compatibility
- **Status**: PASSED
- **Validation**: Existing architecture supports the planned extensions (database models, JWT auth, FastAPI routes)

### Gate 2: Technology Stack Compliance
- **Status**: PASSED
- **Validation**: All planned technologies (Cohere, MCP, ChatKit) align with constitutional constraints

### Gate 3: Security Requirements
- **Status**: PASSED
- **Validation**: All planned implementations maintain user isolation and JWT protection

---

## Phase 0: Research & Discovery

### Research Task 1: Cohere API Integration
- **Objective**: Research best practices for Cohere tool calling in Python with langchain-cohere
- **Focus**: Understanding how to bind tools to Cohere models for task management
- **Deliverable**: research.md entry on Cohere integration patterns

### Research Task 2: MCP Server Configuration
- **Objective**: Research FastMCP setup for exposing exactly 5 stateless tools
- **Focus**: Understanding tool schema definitions and registration patterns
- **Deliverable**: research.md entry on MCP server implementation

### Research Task 3: OpenAI ChatKit Integration
- **Objective**: Research Next.js integration patterns for OpenAI ChatKit
- **Focus**: Connecting to custom backend endpoints with JWT authentication
- **Deliverable**: research.md entry on ChatKit configuration

### Research Task 4: Floating Chat Icon Component
- **Objective**: Research best practices for floating action buttons in Next.js with Tailwind
- **Focus**: Responsive design, positioning, and animation patterns
- **Deliverable**: research.md entry on UI implementation

## Phase 1: Data Model & API Design

### Task 1.1: Design Conversation and Message Models
- **Objective**: Define SQLModel models for conversation persistence
- **Requirements**:
  - Conversation: id (UUID), user_id (UUID), created_at, updated_at
  - Message: id (UUID), user_id (UUID), conversation_id (UUID), role (str), content (str), created_at
  - All queries must be filtered by user_id for security
- **Deliverable**: data-model.md with complete entity definitions

### Task 1.2: Design MCP Tool Contracts
- **Objective**: Define JSON schemas for 5 stateless tools
- **Requirements**:
  - add_task(user_id, title, description=None) → {"task_id": str, "status": "created", "title": str}
  - list_tasks(user_id, status="all") → [{"id": str, "title": str, "completed": bool}]
  - complete_task(user_id, task_id) → {"task_id": str, "status": "completed", "title": str}
  - delete_task(user_id, task_id) → {"task_id": str, "status": "deleted", "title": str}
  - update_task(user_id, task_id, title=None, description=None) → {"task_id": str, "status": "updated", "title": str}
- **Deliverable**: contracts/mcp-tools.json with OpenAPI schemas

### Task 1.3: Design Chat API Contract
- **Objective**: Define contract for POST /api/{user_id}/chat endpoint
- **Requirements**: JWT-protected, returns conversation_id, response, and tool_calls
- **Deliverable**: contracts/chat-api.json with OpenAPI schema

## Phase 2: Infrastructure Setup

### Task 2.1: Extend Database Models
- **Objective**: Add Conversation and Message models to existing database structure
- **Requirements**: Integrate with existing database.py, maintain async patterns
- **Deliverable**: Updated models.py with new entities

### Task 2.2: Create MCP Server Infrastructure
- **Objective**: Set up MCP server with 5 stateless tools
- **Requirements**: Use FastMCP, inject SQLModel sessions, enforce user_id filtering
- **Deliverable**: /backend/mcp_server/ and /backend/mcp_tools/ directories with complete implementation

### Task 2.3: Implement Cohere Agent
- **Objective**: Create agent that binds MCP tools to Cohere model
- **Requirements**: Proper system prompt, tool binding, error handling
- **Deliverable**: /backend/agents/todo_agent.py with complete implementation

## Phase 3: API Implementation

### Task 3.1: Create Chat Endpoint
- **Objective**: Implement POST /api/{user_id}/chat with JWT protection
- **Requirements**: Conversation management, history persistence, tool call handling
- **Deliverable**: /backend/routers/chat.py with complete implementation

### Task 3.2: Implement Helper Functions
- **Objective**: Create database helper functions for conversation management
- **Requirements**: Async functions to fetch/save conversation history by user_id
- **Deliverable**: Helper functions in appropriate backend module

## Phase 4: Frontend Integration

### Task 4.1: Create Floating Chat Icon
- **Objective**: Implement floating action button component
- **Requirements**: Fixed bottom-right, clickable, responsive, modern design
- **Deliverable**: /frontend/components/ChatbotIcon.tsx with complete implementation

### Task 4.2: Integrate ChatKit
- **Objective**: Connect OpenAI ChatKit to dashboard with JWT authentication
- **Requirements**: Attach JWT tokens, handle conversation_id persistence, error states
- **Deliverable**: Updated dashboard layout/page with ChatKit integration

## Phase 5: Testing & Integration

### Task 5.1: Security Validation
- **Objective**: Verify all endpoints properly validate JWT and filter by user_id
- **Requirements**: Test cross-user data access prevention
- **Deliverable**: Security validation report

### Task 5.2: End-to-End Testing
- **Objective**: Test complete user flow from login to chat interaction
- **Requirements**: Verify all 5 MCP tools work via natural language
- **Deliverable**: Test report with success criteria validation

### Task 5.3: Persistence Validation
- **Objective**: Verify conversation history persists across page refreshes
- **Requirements**: Test server restart resilience, data integrity
- **Deliverable**: Persistence validation report

## Success Criteria Validation

At completion, the implementation will satisfy these measurable outcomes:
- ✅ After login, users can access the AI chatbot interface within 2 seconds of page load
- ✅ The chatbot correctly interprets and executes at least 90% of natural language task commands
- ✅ All chat requests are processed with valid JWT authentication at a success rate of 99.5%
- ✅ Conversation history persists across page refreshes with 100% data integrity
- ✅ Users receive immediate confirmation for all task operations (within 2 seconds)
- ✅ Identity queries are answered directly from JWT token without additional processing delays
- ✅ The existing task CRUD functionality remains fully operational with no performance degradation
- ✅ All 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) function correctly with natural language interpretation