---
id: 1
title: Create Neon Connection Spec
stage: spec
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: neon-table-creation
branch: 002-neon-table-creation
user: user
command: /sp.specify
labels: [database, neon, sqlmodel, fastapi, table-creation]
links:
  spec: specs/002-neon-table-creation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-neon-table-creation/spec.md
  - specs/002-neon-table-creation/checklists/requirements.md
tests:
  - null
---

## Prompt

```
/sp.specify Backend Database and ORM Setup – Neon Table Creation & Connection Test

Target audience: Hackathon judges checking if the agentic process can connect to a real cloud database and automatically create tables

Focus: Connect FastAPI to Neon Serverless PostgreSQL using DATABASE_URL, define a simple Task model, automatically create the Task table in the real Neon database when the app starts, and test the connection with a /health endpoint.

Success criteria:
- FastAPI connects successfully to Neon PostgreSQL using the DATABASE_URL environment variable
- When the app starts, the Task table is automatically created in the Neon database (visible in Neon dashboard → Tables section)
- GET /health endpoint returns 200 OK and confirms the database connection is working
- Table creation is safe to run multiple times (no errors on app restart)
- No manual SQL or dashboard actions needed – everything happens from code

Constraints:
- Technologies: FastAPI, SQLModel (latest), asyncpg driver for Neon
- Environment variable: DATABASE_URL = postgresql+asyncpg://... (full Neon connection string)
- Only one model: Task
  - id: UUID primary key (server_default=uuid.uuid4())
  - title: str (required)
  - completed: bool = False
  - created_at: datetime (default_factory=datetime.utcnow)
- Table creation: Use SQLModel.metadata.create_all() inside a startup event (sync version is acceptable for simplicity)
- Only one endpoint: GET /health
- No authentication, no JWT, no user model, no task CRUD endpoints yet

Not building:
- Extra models or fields
- Any task API endpoints
- Authentication logic
- Frontend code
- Tests
- Migrations (Alembic)

Timeline: Very quick – prove database connection and table creation in one session

Deliverable:
- backend/main.py
- backend/models.py (only Task model)
- backend/database.py (engine and session setup)
- .env.example (with DATABASE_URL)
- README with instructions: how to set DATABASE_URL and check the table in Neon console
```

## Response snapshot

Created a comprehensive specification for the Backend Database and ORM Setup – Neon Table Creation & Connection Test feature. The specification includes:

1. Three prioritized user stories focusing on:
   - Database connection verification (P1)
   - Automatic table creation (P2)
   - Task model definition (P3)

2. Functional requirements covering:
   - Database connection using DATABASE_URL
   - Automatic Task table creation on startup
   - Health endpoint for connection verification
   - Proper Task model definition
   - Safe table creation (idempotent)
   - Technology stack compliance

3. Success criteria with measurable outcomes:
   - Connection success rate
   - Table creation timing
   - Health endpoint response
   - Restart safety
   - Automation completeness

4. Edge cases for error handling scenarios

The specification follows the template structure and maintains focus on business requirements rather than implementation details, while staying within the defined constraints.

## Outcome

- ✅ Impact: Created complete feature specification for Neon database connection
- 🧪 Tests: N/A (specification phase)
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready to proceed with /sp.plan for implementation planning
- 🧠 Reflection: Specification properly defines the database connection and table creation without implementation details, adhering to the agentic workflow.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase