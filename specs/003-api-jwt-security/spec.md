# Feature Specification: RESTful API Endpoints and JWT Security for Multi-User Todo Application

**Feature Branch**: `003-api-jwt-security`
**Created**: 2026-01-26
**Status**: Draft
**Input**: User description: "RESTful API Endpoints and JWT Security for Multi-User Todo Application - Build secure RESTful API endpoints in FastAPI for task CRUD operations, integrate JWT verification (using shared secret or JWKS from Better Auth), enforce strict user-task ownership on every request, and ensure no user can access or modify another user's tasks."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Listing (Priority: P1)

Authenticated users need to retrieve their own tasks securely through a protected API endpoint, with assurance that they cannot access other users' tasks.

**Why this priority**: This is the foundational read operation that users perform frequently to view their tasks.

**Independent Test**: The system can be tested by verifying that a user can only retrieve their own tasks and receives appropriate access errors when attempting to access others' tasks.

**Acceptance Scenarios**:

1. **Given** a user has valid JWT credentials, **When** they request GET /api/{their_user_id}/tasks, **Then** they receive only their own tasks with 200 OK status
2. **Given** a user has valid JWT credentials but tries to access another user's tasks, **When** they request GET /api/{other_user_id}/tasks, **Then** they receive a 403 Forbidden error

---
### User Story 2 - Secure Task Creation (Priority: P2)

Authenticated users need to create new tasks for themselves through a protected API endpoint, with assurance that they cannot create tasks for other users.

**Why this priority**: After viewing tasks, users need to create new ones, which is a core functionality.

**Independent Test**: The system can be tested by verifying that a user can only create tasks for themselves and receives appropriate access errors when attempting to create for others.

**Acceptance Scenarios**:

1. **Given** a user has valid JWT credentials, **When** they request POST /api/{their_user_id}/tasks with task data, **Then** a new task is created for their user ID with 201 Created status
2. **Given** a user has valid JWT credentials but tries to create a task for another user, **When** they request POST /api/{other_user_id}/tasks, **Then** they receive a 403 Forbidden error

---
### User Story 3 - Secure Task Retrieval and Modification (Priority: P3)

Authenticated users need to retrieve, update, and delete their own tasks securely, with assurance that they cannot access other users' tasks.

**Why this priority**: Users need full CRUD operations on their own tasks for complete task management functionality.

**Independent Test**: The system can be tested by verifying that a user can only perform operations on their own tasks and receives appropriate access errors when attempting operations on others' tasks.

**Acceptance Scenarios**:

1. **Given** a user has valid JWT credentials, **When** they request GET /api/{their_user_id}/tasks/{their_task_id}, **Then** they receive the task details with 200 OK status
2. **Given** a user has valid JWT credentials, **When** they request PUT /api/{their_user_id}/tasks/{their_task_id}, **Then** the task is updated with 200 OK status
3. **Given** a user has valid JWT credentials, **When** they request DELETE /api/{their_user_id}/tasks/{their_task_id}, **Then** the task is deleted with 200 OK status
4. **Given** a user has valid JWT credentials but tries to access another user's task, **When** they request any operation on /api/{other_user_id}/tasks/{any_task_id}, **Then** they receive a 403 Forbidden error

---

### Edge Cases

- What happens when a JWT token is expired or invalid?
- How does the system handle malformed user_id or task_id parameters?
- What occurs when a user attempts to access a non-existent task?
- How does the system behave when the JWT token's user_id doesn't match the URL's user_id?
- What happens when the authorization header is missing or malformed?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement GET /api/{user_id}/tasks endpoint to list a user's tasks
- **FR-002**: System MUST implement POST /api/{user_id}/tasks endpoint to create a new task for the user
- **FR-003**: System MUST implement GET /api/{user_id}/tasks/{task_id} endpoint to retrieve a single task
- **FR-004**: System MUST implement PUT /api/{user_id}/tasks/{task_id} endpoint to update a task
- **FR-005**: System MUST implement DELETE /api/{user_id}/tasks/{task_id} endpoint to delete a task
- **FR-006**: System MUST implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint to toggle completed status
- **FR-007**: System MUST require a valid JWT token in Authorization: Bearer <token> header for all protected endpoints
- **FR-008**: System MUST verify JWT token using HS256 algorithm with shared secret from BETTER_AUTH_SECRET environment variable
- **FR-009**: System MUST extract user_id from JWT token and verify it matches the {user_id} in the URL path
- **FR-010**: System MUST filter all database queries by the authenticated user's ID to enforce strict ownership
- **FR-011**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404) and JSON error messages
- **FR-012**: System MUST use Pydantic/SQLModel for request/response validation and serialization
- **FR-013**: System MUST ensure no cross-user data leakage is possible through any endpoint
- **FR-014**: System MUST accept UUID strings for both {user_id} and {task_id} path parameters

### Key Entities

- **Task**: Represents a user's todo item with properties for title, completion status, and timestamps, secured by user ownership
- **User**: Represents an authenticated user identified by UUID, whose identity is verified through JWT token
- **JWT Token**: Represents a secure authentication token containing user identity information for authorization

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 required endpoints are implemented and return correct HTTP status codes with 95% success rate during testing
- **SC-002**: JWT verification works correctly with 99% success rate for valid tokens and 100% rejection of invalid tokens
- **SC-003**: User-task ownership enforcement prevents cross-user data access with 100% effectiveness
- **SC-004**: Database queries are properly filtered by authenticated user ID in 100% of requests
- **SC-005**: Error responses follow consistent JSON format with appropriate HTTP status codes
- **SC-006**: API endpoints handle edge cases (invalid tokens, wrong user IDs, etc.) gracefully with proper error messages
- **SC-007**: No cross-user data leakage is detected during security testing
- **SC-008**: All request/response models use proper validation and serialization