---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, todo-app, fullstack]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/tasks-template.md
tests:
  - null
---

## Prompt

```
/sp.constitution
Project: Todo Full-Stack Web Application (Multi-user Todo App with REST API, JWT Authentication, and Responsive Frontend)

Core principles:
- Correctness: All functionality must work as specified (CRUD operations, user isolation, authentication)
- Security: Enforce strict user-task ownership and proper JWT validation on every protected endpoint
- Maintainability: Clean, modular, well-documented code following best practices for Next.js + FastAPI
- Reproducibility: All setup steps, environment variables, and deployment instructions must be clear and repeatable
- Agentic workflow adherence: No manual coding allowed; every file must be generated via Claude Code using Spec-Kit Plus

Key standards:
- Authentication: Use Better Auth (frontend) + JWT issuance/verification (backend) with shared secret
- API design: RESTful, fully documented, consistent naming, proper HTTP status codes
- Data persistence: Use Neon Serverless PostgreSQL with SQLModel ORM; all tables must have proper relationships and constraints
- Frontend: Responsive design (mobile-first), modern UI components, clear loading/error states
- Code quality: Type-safe (TypeScript + Python type hints), linting (ESLint + Ruff), consistent formatting (Prettier + Black)
- Security: Never expose sensitive data, validate all inputs, protect against common vulnerabilities (XSS, CSRF, etc.)
- Documentation: Every endpoint, model, and major component must have clear comments and README instructions

Constraints:
- Technology stack: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- No manual coding: All implementation must be done through the Agentic Dev Stack (spec → plan → tasks → Claude Code)
- Project must be split into exactly three specs (as defined earlier)
- Final deliverable: Fully working web application deployable to Vercel (frontend) + Render/Fly.io/Railway (backend) with Neon DB
- JWT secret must be managed via environment variable (BETTER_AUTH_SECRET) shared between frontend and backend

Success criteria:
- All CRUD operations work correctly for individual users
- Proper user authentication and session management
- Secure JWT token handling between frontend and backend
- Responsive UI that works across device sizes
- Proper data isolation between users
- Complete API documentation
- Successful deployment to target platforms
- Comprehensive error handling and validation
```

## Response snapshot

Updated the project constitution file at `.specify/memory/constitution.md` with the specific requirements for the Todo Full-Stack Web Application. The new constitution includes:

1. Five core principles: Correctness, Security, Maintainability, Reproducibility, and Agentic Workflow Adherence
2. Key standards covering authentication, API design, data persistence, frontend, code quality, security, and documentation
3. Constraints related to technology stack, workflow, and deployment
4. Success criteria for measuring project completion
5. Governance rules for maintaining consistency

Also updated the plan and tasks templates to align with the new constitution, ensuring the templates include checks and guidelines that match the project requirements.

## Outcome

- ✅ Impact: Created comprehensive project constitution and aligned templates
- 🧪 Tests: N/A
- 📁 Files: Updated constitution.md, plan-template.md, tasks-template.md
- 🔁 Next prompts: Ready to proceed with feature specification using /sp.specify
- 🧠 Reflection: The constitution now clearly defines the project goals and constraints, which will guide all subsequent development decisions.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification