# Data Model: Frontend Interface and Authentication for Multi-User Todo Web Application

**Feature**: 004-frontend-auth
**Date**: 2026-01-26

## User Session Entity

**Description**: Represents an authenticated user's session with JWT token and user identity

**Fields**:
- `userId`: UUID string (from JWT payload or session)
- `token`: JWT string (for API authentication)
- `expiresAt`: DateTime (token expiration time)
- `email`: String (user's email address)
- `isLoggedIn`: Boolean (current authentication status)

**Validation Rules**:
- `userId` must be a valid UUID format
- `token` must be a valid JWT string
- `expiresAt` must be in the future
- `email` must be a valid email format
- `isLoggedIn` reflects actual session status

**State Transitions**:
- From unauthenticated → authenticated (login)
- From authenticated → unauthenticated (logout)
- From valid session → expired session (token expiry)

## Task Entity (Frontend Representation)

**Description**: Represents a user's todo item with properties for title, description, completion status, and timestamps

**Fields**:
- `id`: UUID string (unique identifier)
- `title`: String (required, max 255 characters)
- `description`: String | null (optional, max 1000 characters)
- `completed`: Boolean (default false)
- `createdAt`: DateTime (timestamp when created)
- `updatedAt`: DateTime (timestamp when last updated)
- `userId`: UUID string (owner of the task)

**Validation Rules**:
- `title` must be 1-255 characters
- `description` can be null or 1-1000 characters
- `completed` must be a boolean value
- `createdAt` and `updatedAt` are read-only from API
- `userId` must match authenticated user

**State Transitions**:
- `completed` field can transition from false to true (marking task as complete)
- `completed` field can transition from true to false (reopening task)
- `title` and `description` can be updated while maintaining user ownership

## Authentication Form Data

**Description**: Represents the data structure for authentication forms

**Fields**:
- `email`: String (valid email format)
- `password`: String (min 8 characters, with complexity requirements)
- `confirmPassword`: String (for signup, must match password)

**Validation Rules**:
- `email` must be valid email format
- `password` must be at least 8 characters with complexity requirements
- `confirmPassword` must match `password` field (for signup)

**State Transitions**:
- From empty → filled (user input)
- From filled → submitted (form submission)
- From submitted → validated (success or error response)

## API Response Structures

### Authentication Response
- `user`: Object with user details (id, email, etc.)
- `token`: JWT string for subsequent API calls
- `expiresIn`: Number of seconds until token expires

### Task List Response
- `tasks`: Array of Task objects (as defined above)

### Task Operation Response
- `task`: Single Task object reflecting the operation result
- `message`: String with operation status message

## Component State Structures

### Task Form State
- `title`: String (current title input value)
- `description`: String (current description input value)
- `isSubmitting`: Boolean (form submission in progress)
- `errors`: Object (field-specific error messages)

### Task List State
- `tasks`: Array of Task objects
- `loading`: Boolean (data loading in progress)
- `error`: String | null (error message if any)
- `filter`: String (filtering criteria, e.g., "all", "active", "completed")