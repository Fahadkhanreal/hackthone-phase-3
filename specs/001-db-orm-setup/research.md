# Research: Backend Database and ORM Setup for Multi-User Todo Web Application

**Feature**: 001-db-orm-setup
**Date**: 2026-01-26

## Decision: FastAPI with SQLModel for Backend

**Rationale**: FastAPI provides excellent async support, automatic API documentation, and strong typing capabilities. SQLModel combines Pydantic and SQLAlchemy, offering type safety with database functionality. Together they provide the ideal combination for our requirements of async operations, type safety, and clean code.

**Alternatives considered**:
- Flask + SQLAlchemy: Less async support and modern typing
- Django: Overkill for this simple backend API
- Starlette alone: Would require more boilerplate code

## Decision: Neon Serverless PostgreSQL with asyncpg

**Rationale**: Neon's serverless PostgreSQL provides automatic scaling, branching, and cost-effectiveness for development. The asyncpg driver provides native async support for PostgreSQL operations, which aligns with our requirement for async database operations.

**Alternatives considered**:
- Standard PostgreSQL: Requires more manual scaling and management
- SQLite: Not suitable for multi-user applications
- MongoDB: Would not leverage SQL expertise and relationships

## Decision: Environment Configuration with pydantic-settings

**Rationale**: pydantic-settings provides robust validation and type checking for environment variables, which is crucial for database connection strings and other configuration. It integrates seamlessly with FastAPI and Pydantic models.

**Alternatives considered**:
- python-dotenv alone: No validation or type safety
- Manual os.environ checks: More verbose and error-prone

## Decision: Async Session Dependency Injection

**Rationale**: Using FastAPI's dependency injection system with async sessions provides clean separation of concerns, automatic session management, and proper error handling. This pattern is recommended by FastAPI documentation and SQLModel examples.

**Alternatives considered**:
- Global session objects: Harder to manage lifecycle and prone to connection leaks
- Manual session creation in each endpoint: Repetitive and error-prone

## Decision: UUID Primary Keys with Automatic Generation

**Rationale**: UUIDs provide globally unique identifiers without coordination, which is important for a multi-user system. SQLModel's server_default=func.uuid_generate_v4() ensures uniqueness at the database level.

**Alternatives considered**:
- Auto-increment integers: Potential issues with distributed systems and user privacy
- String-based IDs: Less standardized and potentially collision-prone

## Decision: Startup Event for Table Creation

**Rationale**: Using FastAPI's lifespan events for table creation ensures tables are created when the application starts, which is simple and effective for this hackathon timeline. For production, Alembic migrations would be preferred.

**Alternatives considered**:
- Alembic migrations: More complex setup for hackathon speed
- Manual table creation: Would require manual intervention for deployments