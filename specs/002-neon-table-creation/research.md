# Research: Neon Database Connection and Table Creation

**Feature**: 002-neon-table-creation
**Date**: 2026-01-26

## Decision: FastAPI with SQLModel for Database Connection

**Rationale**: FastAPI provides excellent async support and automatic API documentation. SQLModel combines Pydantic and SQLAlchemy, offering type safety with database functionality. Together they provide the ideal combination for connecting to Neon PostgreSQL with proper async support.

**Alternatives considered**:
- Flask + SQLAlchemy: Less async support and modern typing
- Django: Overkill for this simple database connection task
- Raw SQLAlchemy: Missing Pydantic integration and type safety

## Decision: Async Engine with Neon PostgreSQL

**Rationale**: Using asyncpg driver with create_async_engine provides native async support for PostgreSQL operations, which aligns with the requirement for async operations and Neon's serverless capabilities.

**Alternatives considered**:
- Synchronous engine: Would block operations and not meet async requirements
- Other drivers: asyncpg is the most mature and performant PostgreSQL async driver

## Decision: UUID Primary Key with Factory Function

**Rationale**: Using UUID primary keys with uuid4() factory provides globally unique identifiers without coordination, which is important for potential distributed systems. The lambda approach ensures proper string conversion for the database.

**Alternatives considered**:
- Auto-increment integers: Potential issues with distributed systems
- String-based IDs: Less standardized approach

## Decision: Lifespan Event Handler for Table Creation

**Rationale**: Using FastAPI's lifespan context manager is the modern and recommended approach for startup/shutdown events, replacing the deprecated on_event("startup") method.

**Alternatives considered**:
- Startup event: Deprecated in newer FastAPI versions
- Manual creation: Would require manual intervention for deployments

## Decision: Environment Variable Loading with python-dotenv

**Rationale**: python-dotenv provides simple and reliable environment variable loading from .env files, which is essential for securely managing the DATABASE_URL without hardcoding.

**Alternatives considered**:
- Manual os.getenv: More verbose and error-prone
- pydantic-settings: More complex for simple environment loading

## Decision: Health Check with Database Query

**Rationale**: Executing a simple "SELECT 1" query through the database session is the most reliable way to verify that the database connection is not only established but functional.

**Alternatives considered**:
- Simple ping: May not catch connection issues that only appear during actual queries
- Connection object check: Less definitive than actual query execution