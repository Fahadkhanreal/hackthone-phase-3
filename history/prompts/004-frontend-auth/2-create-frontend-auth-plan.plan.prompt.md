---
id: 2
title: Create Frontend Auth Plan
stage: plan
date: 2026-01-26
surface: agent
model: Claude Sonnet 4.5
feature: frontend-auth
branch: 004-frontend-auth
user: user
command: /sp.plan
labels: [frontend, auth, nextjs, better-auth, todo-app, plan]
links:
  spec: specs/004-frontend-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-frontend-auth/plan.md
  - specs/004-frontend-auth/research.md
  - specs/004-frontend-auth/data-model.md
  - specs/004-frontend-auth/quickstart.md
  - specs/004-frontend-auth/contracts/
tests:
  - null
---

## Prompt

```
/sp.plan

Goal: Create responsive Next.js frontend with Better Auth (JWT-enabled), connect to secured FastAPI backend, and implement full task management UI

High-level phases:

1. Initialize Next.js project
   - npx create-next-app@latest frontend --typescript --tailwind --eslint
   - Install Better Auth: npm install better-auth
   - Install any helpers (axios/fetch wrapper if needed)

2. Configure Better Auth with JWT plugin
   - Create auth.ts or lib/auth.ts
   - Import { betterAuth } from "better-auth"
   - Enable jwt() plugin: plugins: [jwt()]
   - Set secret: process.env.BETTER_AUTH_SECRET (same as backend)
   - Export auth client for server/client use

3. Set up authentication pages
   - app/signin/page.tsx: signin form using authClient.signIn.email()
   - app/signup/page.tsx: signup form using authClient.signUp.email()
   - app/signout or button: authClient.signOut()
   - Handle redirects after success (e.g. to /dashboard)

4. Protect routes / middleware
   - middleware.ts: check session with authClient.getSession(); redirect to /signin if unauthenticated for protected paths
   - Or client-side: use useSession() hook → loading/redirect logic

5. Create API client with JWT attachment
   - lib/api.ts: export async function apiFetch(endpoint, options)
     - Get token: const { token } = await authClient.token() or from session
     - Add headers: { Authorization: `Bearer ${token}` }
     - Use fetch or axios to call backend (NEXT_PUBLIC_API_URL + endpoint)
     - Handle 401/403 → logout or show error

6. Build dashboard / task UI
   - app/dashboard/page.tsx (protected)
     - Use useSession() or server component to get user_id
     - Fetch tasks: apiFetch(`/api/${user_id}/tasks`)
     - Display TaskList component
   - Components:
     - TaskList: map tasks → show title, completed checkbox, edit/delete buttons
     - TaskForm: input for title, submit → POST to /api/${user_id}/tasks
     - Edit/Delete/Toggle: PUT/DELETE/PATCH requests with apiFetch

7. Handle states & UX
   - Loading spinner during fet
```

## Response snapshot

Created a comprehensive implementation plan for the Frontend Interface and Authentication feature. The plan includes:

1. Implementation Plan (plan.md): Outlined the technical context, constitution compliance, and project structure with a modular Next.js App Router organization.

2. Research (research.md): Researched and documented key technology decisions including Next.js with App Router, Better Auth with JWT plugin, Tailwind CSS, TypeScript, Fetch API, and middleware for route protection.

3. Data Model (data-model.md): Defined the frontend entities including User Session, Task representation, Authentication Form Data, API Response Structures, and Component State Structures.

4. Quickstart Guide (quickstart.md): Created a step-by-step guide for setting up, configuring, and running the frontend application with authentication and task management features.

5. API Contract (contracts/): Directory created for future API specification files.

All artifacts align with the feature specification and constitutional requirements, ensuring proper authentication, responsive design, type safety, and secure API integration. The plan provides a clear roadmap for implementing the responsive Next.js frontend with Better Auth and full task management capabilities.

## Outcome

- ✅ Impact: Created complete planning artifacts for frontend authentication and task management
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts directory
- 🔁 Next prompts: Ready to proceed with /sp.tasks for implementation task breakdown
- 🧠 Reflection: Plan comprehensively covers all requirements from the specification while maintaining focus on the frontend authentication and task management.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task breakdown and implementation