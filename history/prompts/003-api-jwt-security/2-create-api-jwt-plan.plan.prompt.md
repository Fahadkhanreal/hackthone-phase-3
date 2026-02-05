---
id: 2
title: Create API JWT Plan
stage: plan
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: api-jwt-security
branch: 003-api-jwt-security
user: user
command: /sp.plan
labels: [api, jwt, security, fastapi, todo-app, plan]
links:
  spec: specs/003-api-jwt-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-api-jwt-security/plan.md
  - specs/003-api-jwt-security/research.md
  - specs/003-api-jwt-security/data-model.md
  - specs/003-api-jwt-security/quickstart.md
  - specs/003-api-jwt-security/contracts/task-api.yaml
tests:
  - null
---

## Prompt

```
/sp.plan

Goal: Add secure REST API for tasks with JWT authentication and ownership enforcement on top of Spec 1 database

High-level phases:

1. Install & setup JWT dependencies
   - Add to requirements: pyjwt or python-jose[cryptography]
   - Create config / settings to load BETTER_AUTH_SECRET

2. Create JWT verification logic
   - Function: decode_and_validate_jwt(token: str) → dict (payload) or raise HTTPException(401)
   - Use jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
   - Extract user_id from payload["sub"] or payload["user_id"]
   - Handle expired/invalid/signature errors → 401

3. Create authentication dependency
   - async def get_current_user(token: str = Header(...)):
       - payload = decode_and_validate_jwt(token)
       - return payload["user_id"]  # or full user dict
   - Raise 401 if missing or invalid token

4. Create Pydantic schemas
   - TaskCreate: title: str, description: Optional[str]
   - TaskRead: id, title, completed, created_at, updated_at, user_id
   - TaskUpdate: title: Optional[str], description: Optional[str], completed: Optional[bool]

5. Build task router (APIRouter(prefix="/api/{user_id}/tasks"))
   - GET "/" : list tasks → db.query(Task).where(Task.user_id == current_user_id).all()
   - POST "/" : create → new_task = Task(**data.dict(), user_id=current_user_id), db.add, commit
   - GET "/{task_id}" : get one → query with user_id AND id, else 404
   - PUT "/{task_id}" : update → find task (user_id + id), update fields, commit
   - DELETE "/{task_id}" : delete → find + delete
   - PATCH "/{task_id}/complete" : toggle completed → find, flip bool, commit

6. Ownership enforcement in every endpoint
   - Use Depends(get_current_user) → current_user_id
   - In path: user_id: str
   - If user_id != current_user_id → raise HTTPException(403, "Not authorized for this user")
   - Always filter queries by user_id == current_user_id

7. Integrate with main app
   - app.include_router(tasks_router, prefix="/api")
   - Keep /health from Spec 1

8. Testing
```

## Response snapshot

Created a comprehensive implementation plan for the RESTful API Endpoints and JWT Security feature. The plan includes:

1. Implementation Plan (plan.md): Outlined the technical context, constitution compliance, and project structure with a modular backend organization.

2. Research (research.md): Researched and documented key technology decisions including JWT implementation choice (PyJWT vs python-jose), HS256 algorithm selection, JWT payload structure, authentication dependency pattern, user ID matching enforcement, and error response format.

3. Data Model (data-model.md): Extended the Task entity from Spec 1 with API request/response schemas (TaskCreate, TaskRead, TaskUpdate), JWT token structure, and detailed API endpoint specifications with authorization requirements.

4. Quickstart Guide (quickstart.md): Created a step-by-step guide for setting up, configuring, and testing the secure API endpoints with example curl commands and security validation procedures.

5. API Contract (contracts/task-api.yaml): Defined the OpenAPI specification for all six task endpoints with proper security schemes, request/response schemas, and error handling.

All artifacts align with the feature specification and constitutional requirements, ensuring security, proper authentication, and clean code structure.

## Outcome

- ✅ Impact: Created complete planning artifacts for secure API endpoints
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and task API contract
- 🔁 Next prompts: Ready to proceed with /sp.tasks for implementation task breakdown
- 🧠 Reflection: Plan comprehensively covers all requirements from the specification while maintaining focus on security and authentication.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task breakdown and implementation