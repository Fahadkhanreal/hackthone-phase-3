---
description: "Task list for RESTful API Endpoints and JWT Security feature"
---

# Tasks: 003-api-jwt-security

**Input**: Design documents from `/specs/003-api-jwt-security/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Simple backend**: `backend/`, `backend/main.py`, `backend/routers/tasks.py`
- **Paths shown below** follow the planned structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Update backend/requirements.txt with JWT dependencies (PyJWT or python-jose[cryptography])
- [x] T002 Create backend/config/ directory structure per implementation plan
- [x] T003 Create backend/routers/ directory structure per implementation plan
- [x] T004 Create backend/auth/ directory structure per implementation plan
- [x] T005 Create backend/schemas/ directory structure per implementation plan

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create config/settings.py to load BETTER_AUTH_SECRET environment variable
- [x] T007 [P] Create auth/jwt_utils.py with decode_and_validate_jwt function
- [x] T008 [P] Create auth/dependencies.py with get_current_user dependency
- [x] T009 Create schemas/task_schemas.py with TaskCreate, TaskRead, TaskUpdate models
- [x] T010 Update main.py to include task router with prefix "/api"

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Listing (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to retrieve their own tasks securely through a protected API endpoint, with assurance that they cannot access other users' tasks

**Independent Test**: The system can be tested by verifying that a user can only retrieve their own tasks and receives appropriate access errors when attempting to access others' tasks

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T011 [P] [US1] Contract test for GET /api/{user_id}/tasks endpoint in backend/tests/contract/test_tasks_list.py
- [ ] T012 [P] [US1] Integration test for task listing functionality in backend/tests/integration/test_task_listing.py

### Implementation for User Story 1

- [x] T013 [P] [US1] Create tasks router in backend/routers/tasks.py with GET /api/{user_id}/tasks endpoint
- [x] T014 [US1] Implement task listing with user_id validation and ownership enforcement
- [x] T015 [US1] Add authentication dependency to task listing endpoint
- [x] T016 [US1] Test task listing functionality with JWT token validation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Task Creation (Priority: P2)

**Goal**: Allow authenticated users to create new tasks for themselves through a protected API endpoint, with assurance that they cannot create tasks for other users

**Independent Test**: The system can be tested by verifying that a user can only create tasks for themselves and receives appropriate access errors when attempting to create for others

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Contract test for POST /api/{user_id}/tasks endpoint in backend/tests/contract/test_tasks_create.py
- [ ] T018 [P] [US2] Integration test for task creation functionality in backend/tests/integration/test_task_creation.py

### Implementation for User Story 2

- [x] T019 [P] [US2] Add POST /api/{user_id}/tasks endpoint to tasks router
- [x] T020 [US2] Implement task creation with user_id validation and ownership enforcement
- [x] T021 [US2] Add authentication dependency to task creation endpoint
- [x] T022 [US2] Test task creation functionality with JWT token validation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Task Retrieval and Modification (Priority: P3)

**Goal**: Allow authenticated users to retrieve, update, and delete their own tasks securely, with assurance that they cannot access other users' tasks

**Independent Test**: The system can be tested by verifying that a user can only perform operations on their own tasks and receives appropriate access errors when attempting operations on others' tasks

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for GET /api/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_tasks_get.py
- [ ] T024 [P] [US3] Contract test for PUT /api/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_tasks_update.py
- [ ] T025 [P] [US3] Contract test for DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/tests/contract/test_tasks_delete.py
- [ ] T026 [P] [US3] Contract test for PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/tests/contract/test_tasks_complete.py

### Implementation for User Story 3

- [x] T027 [P] [US3] Add GET /api/{user_id}/tasks/{task_id} endpoint to tasks router
- [x] T028 [P] [US3] Add PUT /api/{user_id}/tasks/{task_id} endpoint to tasks router
- [x] T029 [P] [US3] Add DELETE /api/{user_id}/tasks/{task_id} endpoint to tasks router
- [x] T030 [P] [US3] Add PATCH /api/{user_id}/tasks/{task_id}/complete endpoint to tasks router
- [x] T031 [US3] Implement all endpoints with user_id validation and ownership enforcement
- [x] T032 [US3] Add authentication dependencies to all new endpoints
- [x] T033 [US3] Test all endpoint functionalities with JWT token validation

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T034 [P] Update quickstart documentation in specs/003-api-jwt-security/quickstart.md based on implementation
- [x] T035 Code cleanup and refactoring
- [x] T036 Add type hints and improve code documentation
- [x] T037 [P] Update API contracts in specs/003-api-jwt-security/contracts/ if needed
- [x] T038 Security hardening for JWT validation
- [x] T039 Run validation against quickstart.md procedures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May depend on authentication setup (foundational)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May depend on authentication setup (foundational)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/{user_id}/tasks endpoint in backend/tests/contract/test_tasks_list.py"
Task: "Integration test for task listing functionality in backend/tests/integration/test_task_listing.py"

# Launch tasks router and endpoint implementation together:
Task: "Create tasks router in backend/routers/tasks.py with GET /api/{user_id}/tasks endpoint"
Task: "Implement task listing with user_id validation and ownership enforcement"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence