# Implementation Tasks: Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)

**Feature**: Todo AI Chatbot (Integrated into Existing Full-Stack Todo Application)
**Created**: 2026-02-03
**Status**: Draft
**Dependencies**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Cohere API

## Phase 1: Setup Tasks

- [X] T001 Create backend/mcp_server directory structure
- [X] T002 Create backend/mcp_tools directory structure
- [X] T003 Create backend/agents directory structure
- [X] T004 Update backend requirements.txt with cohere and mcp dependencies
- [X] T005 Create frontend/components directory if not exists
- [X] T006 Update frontend package.json with any needed chat dependencies

## Phase 2: Foundational Tasks

- [X] T010 Extend models.py with Conversation model per data-model.md
- [X] T011 Extend models.py with Message model per data-model.md
- [X] T012 Create database helper functions for conversation management in backend/utils/conversation_helpers.py
- [X] T013 [P] Create JWT utility function to extract user email in backend/auth/jwt_utils.py
- [X] T014 [P] Update database.py to include new models in table creation

## Phase 3: User Story 1 - Chatbot Interface Access (Priority: P1)

**Goal**: Enable logged-in users to access the AI chatbot interface through a floating icon in the bottom-right corner of the dashboard.

**Independent Test**: Can be fully tested by logging in and clicking the floating chatbot icon, which should open the conversation window with the chat interface visible and responsive.

- [X] T020 [US1] Create ChatbotIcon.tsx component with floating design in frontend/components/ChatbotIcon.tsx
- [X] T021 [US1] Add ChatbotIcon to dashboard layout in frontend/app/dashboard/page.tsx
- [X] T022 [US1] Create basic chat window component in frontend/components/ChatWindow.tsx
- [X] T023 [US1] Style chat interface with Tailwind CSS following existing design patterns

**Acceptance**:
- [ ] Floating icon appears in bottom-right corner after login
- [ ] Clicking icon opens chat window
- [ ] Chat window is responsive and user-friendly
- [ ] Icon and window follow existing design patterns

## Phase 4: User Story 2 - Natural Language Task Management (Priority: P1)

**Goal**: Enable users to interact with the AI chatbot using natural language commands to manage their tasks using exactly 5 MCP tools.

**Independent Test**: Can be fully tested by sending various natural language commands to the chatbot and verifying that the appropriate task operations are performed with confirmation messages.

- [X] T030 [P] [US2] Create add_task MCP tool in backend/mcp_tools/add_task.py
- [X] T031 [P] [US2] Create list_tasks MCP tool in backend/mcp_tools/list_tasks.py
- [X] T032 [P] [US2] Create complete_task MCP tool in backend/mcp_tools/complete_task.py
- [X] T033 [P] [US2] Create delete_task MCP tool in backend/mcp_tools/delete_task.py
- [X] T034 [P] [US2] Create update_task MCP tool in backend/mcp_tools/update_task.py
- [X] T035 [US2] Create MCP server in backend/mcp_server/server.py
- [X] T036 [US2] Register all 5 tools with MCP server
- [X] T037 [US2] Create Cohere agent in backend/agents/todo_agent.py
- [X] T038 [US2] Connect Cohere agent to MCP tools
- [X] T039 [US2] Create chat endpoint POST /api/{user_id}/chat in backend/routers/chat.py
- [X] T040 [US2] Implement JWT validation for chat endpoint
- [X] T041 [US2] Implement conversation history management in chat endpoint
- [X] T042 [US2] Implement tool call execution and response formatting
- [X] T043 [US2] Create system prompt for task management in backend/agents/prompts.py
- [X] T044 [US2] Connect frontend chat interface to backend chat endpoint
- [X] T045 [US2] Implement JWT token attachment to chat requests

**Acceptance**:
- [ ] Natural language commands are interpreted correctly
- [ ] All 5 MCP tools are called appropriately based on user input
- [ ] Task operations return proper confirmation messages
- [ ] JWT validation works for all requests
- [ ] Conversation history is maintained properly

## Phase 5: User Story 3 - User Identity Recognition (Priority: P2)

**Goal**: Enable the chatbot to respond to user identity queries (e.g. "Who am I?" or "What is my email?") with the logged-in user's email from JWT token.

**Independent Test**: Can be fully tested by asking identity-related questions to the chatbot and verifying that it responds with the correct email from the JWT token.

- [X] T050 [US3] Update system prompt to handle identity queries in backend/agents/todo_agent.py
- [X] T051 [US3] Modify chat endpoint to extract and provide user email context in backend/routers/chat.py
- [ ] T052 [US3] Test identity query responses in chat interface

**Acceptance**:
- [ ] Identity queries ("Who am I?", "What is my email?") return the correct email
- [ ] Email comes directly from JWT token without additional database queries
- [ ] Responses are immediate and accurate

## Phase 6: User Story 4 - Persistent Conversations (Priority: P2)

**Goal**: Ensure conversation history is stored in the database and persists across page refreshes and server restarts.

**Independent Test**: Can be fully tested by starting a conversation, refreshing the page, and verifying that the conversation history is preserved.

- [X] T060 [US4] Implement conversation creation in chat endpoint
- [X] T061 [US4] Implement message storage for user messages in chat endpoint
- [X] T062 [US4] Implement message storage for assistant responses in chat endpoint
- [X] T063 [US4] Implement conversation history retrieval in chat endpoint
- [ ] T064 [US4] Test conversation persistence across page refreshes
- [ ] T065 [US4] Test conversation persistence across server restarts

**Acceptance**:
- [ ] Conversation history persists after page refresh
- [ ] Conversation history persists after server restart
- [ ] Messages are properly saved and retrieved from database
- [ ] No data loss occurs during normal usage

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T070 Add loading and error states to chat interface
- [ ] T071 [P] Add environment variable validation for Cohere API
- [ ] T072 [P] Add comprehensive error handling for tool calls
- [ ] T073 [P] Add logging for debugging chat interactions
- [ ] T074 [P] Add rate limiting to chat endpoint
- [ ] T075 [P] Update README with Cohere setup instructions
- [ ] T076 [P] Update README with ChatKit domain allowlist steps
- [ ] T077 [P] Add security headers to chat endpoint
- [ ] T078 [P] Add input validation for chat messages
- [ ] T079 [P] Add tests for new models and endpoints
- [ ] T080 [P] Perform end-to-end testing of complete flow

## Dependencies

- **User Story 1** (P1 - Chatbot Interface Access) depends on: Phase 1 (Setup Tasks), Phase 2 (Foundational Tasks)
- **User Story 2** (P1 - Natural Language Task Management) depends on: User Story 1, Phase 1, Phase 2
- **User Story 3** (P2 - User Identity Recognition) depends on: User Story 2
- **User Story 4** (P2 - Persistent Conversations) depends on: User Story 2

## Parallel Execution Opportunities

- **Parallel Tasks**: T030-T034 (MCP tools) can be developed in parallel as they are independent of each other
- **Parallel Tasks**: T013-T014 (Helper functions and database updates) can be developed in parallel
- **UI and Backend**: Chat interface components (T020-T023) can be developed in parallel with backend API development (T035-T045)

## Implementation Strategy

**MVP Scope**: Focus on User Story 1 and User Story 2 for initial working version:
- Basic chat interface with floating icon
- Natural language task management with add_task and list_tasks tools
- JWT validation and basic conversation flow

**Incremental Delivery**:
1. MVP: Chat interface + add/list tasks
2. Complete tool set: Add complete/delete/update tools
3. Identity recognition: Email response functionality
4. Persistence: Conversation history across sessions
5. Polish: Error handling, loading states, documentation