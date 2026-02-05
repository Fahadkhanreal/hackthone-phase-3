---
id: 1
title: Create API JWT Spec
stage: spec
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: api-jwt-security
branch: 003-api-jwt-security
user: user
command: /sp.specify
labels: [api, jwt, security, fastapi, todo-app]
links:
  spec: specs/003-api-jwt-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-api-jwt-security/spec.md
  - specs/003-api-jwt-security/checklists/requirements.md
tests:
  - null
---

## Prompt

```
/sp.specify RESTful API Endpoints and JWT Security for Multi-User Todo Application

Target audience: Hackathon judges evaluating secure backend API design, proper authentication integration, and data isolation in a full-stack agentic project

Focus: Build secure RESTful API endpoints in FastAPI for task CRUD operations, integrate JWT verification (using shared secret or JWKS from Better Auth), enforce strict user-task ownership on every request, and ensure no user can access or modify another user's tasks.

Success criteria:
- All 6 required endpoints are implemented and work correctly:
  - GET    /api/{user_id}/tasks           → list user's tasks
  - POST   /api/{user_id}/tasks           → create new task for the user
  - GET    /api/{user_id}/tasks/{task_id} → get single task
  - PUT    /api/{user_id}/tasks/{task_id} → update task
  - DELETE /api/{user_id}/tasks/{task_id} → delete task
  - PATCH  /api/{user_id}/tasks/{task_id}/complete → toggle completed status
- Every protected endpoint requires a valid JWT in Authorization: Bearer <token> header
- Backend verifies JWT and extracts user_id → must match the {user_id} in the URL path (return 403 if mismatch)
- All database queries are filtered by authenticated user's ID (strict ownership)
- Returns correct HTTP status codes (200, 201, 401, 403, 404) and JSON error messages
- Uses the Task table and database connection created in Spec 1
- No cross-user data leakage is possible

Constraints:
- Backend only: FastAPI + SQLModel + Neon PostgreSQL (reuse Spec 1 setup)
- JWT verification:
  - Use PyJWT or python-jose[cryptography]
  - Prefer shared secret method: read BETTER_AUTH_SECRET from env var
  - Algorithm: HS256 (standard for symmetric secret)
  - Token payload must contain at least "sub" or "user_id"
- Environment variables: BETTER_AUTH_SECRET (shared with frontend in Spec 3), DATABASE_URL (from Spec 1)
- Request/response models: Use Pydantic / SQLModel for input validation and output serialization
- Path parameter {user_id} must be UUID string
- No frontend code in this spec
- No signup/signin logic (handled by Better Auth in frontend)
- No real-time features, pagination, or advanced filtering

Not building:
- Frontend integration or token attachment (that's Spec 3)
- Better Auth installation or user registration endpoints
- Role-based access beyond basic user ownership
- Rate limiting, CORS (add minimal CORS if needed for local testing)
- Unit tests

Timeline: Complete in 1–2 hackathon sessions after Spec 1 is working

Deliverable format:
- Extend backend/ folder:
  - Add routers/tasks.py (APIRouter)
  - schemas.py (Pydantic models: TaskCreate, TaskRead, TaskUpdate)
  - dependencies.py (updated with get_current_user dependency)
  - auth.py or jwt_utils.py (JWT decode + validation logic)
- Update main.py to include task router with prefix "/api"
- README update: how to test endpoints with curl + JWT token (example tokens can be mocked)
```

## Response snapshot

Created a comprehensive specification for the RESTful API Endpoints and JWT Security feature. The specification includes:

1. Three prioritized user stories focusing on:
   - Secure task listing (P1)
   - Secure task creation (P2)
   - Secure task retrieval and modification (P3)

2. Functional requirements covering:
   - All 6 required endpoints (GET, POST, PUT, DELETE, PATCH)
   - JWT token verification and user ID matching
   - Database query filtering by user ID
   - Proper HTTP status codes and error messages
   - Request/response validation

3. Success criteria with measurable outcomes:
   - Endpoint implementation success rate
   - JWT verification effectiveness
   - User-task ownership enforcement
   - Error handling consistency

4. Edge cases for security and error handling scenarios

The specification follows the template structure and maintains focus on business requirements rather than implementation details, while staying within the defined constraints.

## Outcome

- ✅ Impact: Created complete feature specification for secure API endpoints
- 🧪 Tests: N/A (specification phase)
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready to proceed with /sp.plan for implementation planning
- 🧠 Reflection: Specification properly defines the secure API requirements without implementation details, adhering to the agentic workflow.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase