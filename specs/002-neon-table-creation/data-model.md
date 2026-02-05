# Data Model: Neon Database Connection and Table Creation

**Feature**: 002-neon-table-creation
**Date**: 2026-01-26

## Task Entity

**Description**: Represents a todo item with properties for id, title, completion status, and creation timestamp

**Fields**:
- `id`: UUID primary key, auto-generated with uuid4() factory function
- `title`: String, required, no maximum length specified
- `completed`: Boolean, default False
- `created_at`: DateTime, default current UTC time

**Validation Rules**:
- `title` field cannot be empty
- `completed` field defaults to False
- `created_at` is automatically set to current time when record is created

**Relationships**:
- No relationships in this initial version (no user association yet)

**State Transitions**:
- `completed` field can transition from False to True (marking task as complete)
- `completed` field can transition from True to False (reopening task)

## Database Schema Requirements

**Indexes**:
- Primary key index on `id`

**Constraints**:
- `title` field cannot be NULL
- `completed` field defaults to False
- `created_at` is automatically populated with current UTC time

**Table Creation**:
- Table name: `task`
- Engine: PostgreSQL (via Neon)
- Character set: UTF-8
- Collation: Default for PostgreSQL
- The table should be created automatically when the application starts up