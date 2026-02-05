# Feature Specification: Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)

**Feature Branch**: `1-ai-chatbot-integration`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "Phase III – Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)
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
Automated unit/integration tests (manual demo is sufficient)"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Chatbot Interface Access (Priority: P1)

Logged-in users can access the AI chatbot interface through a floating icon in the bottom-right corner of the dashboard. When clicked, the OpenAI ChatKit interface opens in a conversation window.

**Why this priority**: Essential for users to access the primary feature of the application. Without this interface, users cannot interact with the AI chatbot functionality.

**Independent Test**: Can be fully tested by logging in and clicking the floating chatbot icon, which should open the conversation window with the chat interface visible and responsive.

**Acceptance Scenarios**:

1. **Given** user is logged in and on the dashboard page, **When** user clicks the floating chatbot icon, **Then** the OpenAI ChatKit conversation window opens
2. **Given** user has opened the chat window, **When** user closes the chat window, **Then** the chat window disappears but the floating icon remains visible

---

### User Story 2 - Natural Language Task Management (Priority: P1)

Users can interact with the AI chatbot using natural language commands to manage their tasks. The chatbot correctly interprets commands to add, list, complete, delete, and update tasks using exactly 5 MCP tools.

**Why this priority**: Core functionality that delivers the main value proposition of the AI chatbot. Without this, users cannot manage tasks through the chat interface.

**Independent Test**: Can be fully tested by sending various natural language commands to the chatbot and verifying that the appropriate task operations are performed with confirmation messages.

**Acceptance Scenarios**:

1. **Given** user types "Add a task: Buy groceries", **When** chatbot processes the command, **Then** a new task "Buy groceries" is created and confirmed with "Task added: Buy groceries ✅"
2. **Given** user types "List my tasks", **When** chatbot processes the command, **Then** the chatbot displays all current tasks
3. **Given** user types "Complete task 1", **When** chatbot processes the command, **Then** task 1 is marked as completed and confirmed
4. **Given** user types "Update task 1 to say 'Buy organic groceries'", **When** chatbot processes the command, **Then** task 1 is updated with the new text and confirmed

---

### User Story 3 - User Identity Recognition (Priority: P2)

When users ask the chatbot about their identity (e.g. "Who am I?" or "What is my email?"), the bot correctly responds with the logged-in user's email from JWT token without requiring additional tool calls.

**Why this priority**: Enhances user experience by providing contextual awareness of the user's identity within the conversation.

**Independent Test**: Can be fully tested by asking identity-related questions to the chatbot and verifying that it responds with the correct email from the JWT token.

**Acceptance Scenarios**:

1. **Given** user asks "Who am I?", **When** chatbot processes the query, **Then** the chatbot responds with the user's email address from JWT
2. **Given** user asks "What is my email?", **When** chatbot processes the query, **Then** the chatbot responds with the user's email address from JWT

---

### User Story 4 - Persistent Conversations (Priority: P2)

Conversation history is stored in the database and persists across page refreshes and server restarts. Users can continue conversations where they left off.

**Why this priority**: Critical for maintaining user experience and ensuring that conversation context is not lost during normal usage patterns.

**Independent Test**: Can be fully tested by starting a conversation, refreshing the page, and verifying that the conversation history is preserved.

**Acceptance Scenarios**:

1. **Given** user has an ongoing conversation with the chatbot, **When** user refreshes the page, **Then** the conversation history remains visible in the chat window
2. **Given** server restarts, **When** user accesses the chat again, **Then** previous conversation history is still accessible

---

### Edge Cases

- What happens when the JWT token is invalid or expired?
- How does the system handle network failures during chat requests?
- What occurs when the Cohere API is temporarily unavailable?
- How does the system handle malformed natural language commands?
- What happens when a user attempts to access another user's conversation history?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST display a floating chatbot icon in the bottom-right corner of the dashboard after successful login
- **FR-002**: System MUST open the OpenAI ChatKit conversation window when the floating icon is clicked
- **FR-003**: System MUST integrate with Cohere API for natural language processing and tool calling
- **FR-004**: System MUST expose exactly 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- **FR-005**: System MUST validate JWT tokens on all chat requests and ensure user_id in path matches token
- **FR-006**: System MUST store conversation history in Conversation and Message database tables
- **FR-007**: System MUST confirm every task operation with a friendly message (e.g., "Task added: Buy groceries ✅")
- **FR-008**: System MUST respond to identity queries with the logged-in user's email from JWT without tool calls
- **FR-009**: System MUST maintain existing task CRUD REST endpoints and UI functionality unchanged
- **FR-010**: System MUST persist conversation history across page refreshes and server restarts
- **FR-011**: System MUST implement stateless design with no server-side session memory
- **FR-012**: System MUST use MCP Python SDK to expose stateless tools
- **FR-013**: System MUST support natural language interpretation for task management commands

### Key Entities *(include if feature involves data)*

- **Conversation**: Represents a user's chat session with the AI chatbot, containing metadata about the conversation
- **Message**: Represents individual messages exchanged between user and chatbot, including role (user/assistant) and content
- **Task**: Represents user tasks with title, description, and completion status, managed through MCP tools

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: After login, users can access the AI chatbot interface within 2 seconds of page load
- **SC-002**: The chatbot correctly interprets and executes at least 90% of natural language task commands
- **SC-003**: All chat requests are processed with valid JWT authentication at a success rate of 99.5%
- **SC-004**: Conversation history persists across page refreshes with 100% data integrity
- **SC-005**: Users receive immediate confirmation for all task operations (within 2 seconds)
- **SC-006**: Identity queries are answered directly from JWT token without additional processing delays
- **SC-007**: The existing task CRUD functionality remains fully operational with no performance degradation
- **SC-008**: All 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) function correctly with natural language interpretation