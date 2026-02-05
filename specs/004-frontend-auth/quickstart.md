# Quickstart Guide: Frontend Interface and Authentication for Multi-User Todo Web Application

**Feature**: 004-frontend-auth
**Date**: 2026-01-26

## Setup Instructions

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   - Copy `.env.local.example` to `.env.local`
   - Update `NEXT_PUBLIC_API_URL` with your backend URL (e.g., http://localhost:8000)
   - Ensure `BETTER_AUTH_SECRET` matches the one used in the backend

4. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open the application**
   - Visit `http://localhost:3000` in your browser
   - You should be redirected to the signin page if not authenticated

## Authentication Flow

1. **New users**: Navigate to `/signup` to create an account
2. **Existing users**: Navigate to `/signin` to log in
3. **After successful authentication**: Users are redirected to `/dashboard`
4. **Protected routes**: All routes under `/dashboard/*` require authentication

## Task Management Features

1. **View tasks**: On the dashboard, your tasks will be listed automatically
2. **Create task**: Use the "Add Task" form to create a new task
3. **Update task**: Click the edit icon next to a task to update its details
4. **Complete task**: Click the checkbox next to a task to toggle its completion status
5. **Delete task**: Click the delete icon to remove a task

## API Integration

- All API calls automatically include the Authorization: Bearer `<token>` header
- The token is retrieved from the current session via Better Auth
- Protected routes on the backend validate the JWT token for each request
- User isolation is enforced by using the authenticated user's ID in API paths

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API base URL (required)
- `BETTER_AUTH_SECRET` - Shared secret for JWT validation (must match backend)

## Verification Steps

1. After starting the application, verify the home page redirects to signin for unauthenticated users
2. Create a new account via `/signup` and verify you're redirected to `/dashboard`
3. On the dashboard, verify you can create, update, and delete tasks
4. Test that unauthenticated users cannot access `/dashboard` directly
5. Verify the logout function works and redirects to signin page

## Troubleshooting

- If you get authentication errors, verify your `BETTER_AUTH_SECRET` matches the backend
- If API calls fail, check that `NEXT_PUBLIC_API_URL` is correctly set
- If routes don't redirect properly, verify the middleware configuration
- For styling issues, ensure Tailwind CSS is properly configured