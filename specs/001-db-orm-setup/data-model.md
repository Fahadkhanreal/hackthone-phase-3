# Data Model: Backend Database and ORM Setup for Multi-User Todo Web Application

**Feature**: 001-db-orm-setup
**Date**: 2026-01-26

## Task Entity

**Description**: Represents a todo item with properties for title, description, completion status, timestamps, and user association

**Fields**:
- `id`: UUID primary key, auto-generated with uuid_generate_v4()
- `title`: String, required, with index for performance
- `description`: String, optional (nullable)
- `completed`: Boolean, default False
- `created_at`: DateTime, default current timestamp
- `updated_at`: DateTime, auto-updates when record changes
- `user_id`: UUID, foreign key reference to user (placeholder for future auth integration)

**Relationships**:
- Many Tasks belong to One User (via user_id foreign key)
- Future: Will connect to actual User table managed by Better Auth

**Validation Rules**:
- `title` must not be empty
- `completed` defaults to False
- `created_at` and `updated_at` are automatically managed by the database

**State Transitions**:
- `completed` field can transition from False to True (marking task as complete)
- `completed` field can transition from True to False (reopening task)
- `title` and `description` can be updated anytime
- `updated_at` automatically updates on any modification

## Database Schema Requirements

**Indexes**:
- Primary key index on `id`
- Index on `user_id` for efficient user-based queries
- Index on `title` for search functionality (future use)

**Constraints**:
- `title` field cannot be NULL
- `completed` field defaults to False
- `created_at` and `updated_at` are automatically populated
- `user_id` references a valid user (foreign key constraint)

**Table Creation**:
- Table name: `task`
- Engine: PostgreSQL (via Neon)
- Character set: UTF-8
- Collation: Default for PostgreSQL