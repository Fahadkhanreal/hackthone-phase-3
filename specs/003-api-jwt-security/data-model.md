# Data Model: RESTful API Endpoints and JWT Security for Multi-User Todo Application

**Feature**: 003-api-jwt-security
**Date**: 2026-01-26

## Task Entity (Extended from Spec 1)

**Description**: Represents a user's todo item with properties for title, completion status, and timestamps, secured by user ownership

**Fields** (existing from Spec 1):
- `id`: UUID primary key, auto-generated with uuid4()
- `title`: String, required, with index for performance
- `description`: Optional[String], max length 1000
- `completed`: Boolean, default False
- `created_at`: DateTime, default current timestamp
- `updated_at`: DateTime, auto-updates when record changes
- `user_id`: UUID, foreign key reference to user (enforced by ownership validation)

**Validation Rules**:
- `title` field cannot be empty (min length 1)
- `completed` field defaults to False
- `created_at` and `updated_at` are automatically managed by the database
- `user_id` must match the authenticated user's ID for all operations

**State Transitions**:
- `completed` field can transition from False to True (marking task as complete)
- `completed` field can transition from True to False (reopening task)
- `title` and `description` can be updated anytime
- `updated_at` automatically updates on any modification

## API Request/Response Schemas

### TaskCreate Schema
**Purpose**: Schema for creating new tasks
- `title`: String (required, min length 1, max length 255)
- `description`: Optional[String] (max length 1000)
- `completed`: Optional[Boolean] (defaults to False)

### TaskRead Schema
**Purpose**: Schema for returning task data
- `id`: UUID (read-only)
- `title`: String
- `description`: Optional[String]
- `completed`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime
- `user_id`: UUID (read-only, validated against authenticated user)

### TaskUpdate Schema
**Purpose**: Schema for updating existing tasks
- `title`: Optional[String] (min length 1, max length 255)
- `description`: Optional[String] (max length 1000)
- `completed`: Optional[Boolean]

## JWT Token Structure

### JWT Payload Claims
- `user_id`: UUID string (primary identifier for authorization)
- `exp`: Expiration timestamp (for automatic token invalidation)
- `iat`: Issued-at timestamp (for audit trails)
- `sub`: Subject identifier (alternative to user_id, for compatibility)

### JWT Validation Requirements
- Algorithm: HS256 (symmetric key)
- Secret: Retrieved from BETTER_AUTH_SECRET environment variable
- Expiration: Checked to prevent use of expired tokens
- Signature: Verified using shared secret

## API Endpoint Specifications

### GET /api/{user_id}/tasks
**Purpose**: List all tasks for a specific user
**Authorization**: JWT token required, user_id must match token's user_id
**Response**: Array of TaskRead objects
**Validation**: User ownership enforcement on all returned tasks

### POST /api/{user_id}/tasks
**Purpose**: Create a new task for a specific user
**Authorization**: JWT token required, user_id must match token's user_id
**Request Body**: TaskCreate object
**Response**: Created TaskRead object
**Validation**: New task's user_id set to authenticated user's ID

### GET /api/{user_id}/tasks/{task_id}
**Purpose**: Retrieve a single task
**Authorization**: JWT token required, user_id must match token's user_id, task must belong to user
**Response**: TaskRead object
**Validation**: Both user_id and task_id must match an existing task

### PUT /api/{user_id}/tasks/{task_id}
**Purpose**: Update an existing task
**Authorization**: JWT token required, user_id must match token's user_id, task must belong to user
**Request Body**: TaskUpdate object
**Response**: Updated TaskRead object
**Validation**: Task must exist and belong to authenticated user

### DELETE /api/{user_id}/tasks/{task_id}
**Purpose**: Delete an existing task
**Authorization**: JWT token required, user_id must match token's user_id, task must belong to user
**Response**: Empty or success confirmation
**Validation**: Task must exist and belong to authenticated user

### PATCH /api/{user_id}/tasks/{task_id}/complete
**Purpose**: Toggle the completion status of a task
**Authorization**: JWT token required, user_id must match token's user_id, task must belong to user
**Response**: Updated TaskRead object
**Validation**: Task must exist and belong to authenticated user