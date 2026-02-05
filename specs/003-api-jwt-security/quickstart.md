# Quickstart Guide: RESTful API Endpoints and JWT Security

**Feature**: 003-api-jwt-security
**Date**: 2026-01-26

## Setup Instructions

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install updated dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Ensure PyJWT or python-jose[cryptography] is included in the requirements

3. **Configure environment variables**
   - Ensure `BETTER_AUTH_SECRET` is set in your .env file for JWT verification
   - Verify `DATABASE_URL` is properly configured (from Spec 1)

4. **Start the application**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## API Endpoint Testing

Once the application is running, you can test the secure endpoints:

### Getting a JWT Token
Since this spec doesn't implement signup/signin logic (handled by Better Auth in frontend), you can mock a JWT token for testing:

```bash
# Example JWT token structure (for testing purposes):
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNDU2NzgtMTIzNC0xMjM0LTEyMzQtMTIzNDU2Nzg5IiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Testing the Endpoints

1. **List User's Tasks**
   ```bash
   curl -X GET "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

2. **Create a Task**
   ```bash
   curl -X POST "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task description"}'
   ```

3. **Get a Single Task**
   ```bash
   curl -X GET "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks/TASK_UUID_HERE" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

4. **Update a Task**
   ```bash
   curl -X PUT "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks/TASK_UUID_HERE" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Task", "completed": true}'
   ```

5. **Delete a Task**
   ```bash
   curl -X DELETE "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks/TASK_UUID_HERE" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

6. **Toggle Task Completion**
   ```bash
   curl -X PATCH "http://localhost:8000/api/12345678-1234-1234-1234-123456789/tasks/TASK_UUID_HERE/complete" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

## Expected Responses

- **Successful operations**: 200 OK or 201 Created with JSON response
- **Unauthorized (invalid/missing token)**: 401 Unauthorized
- **Forbidden (user ID mismatch)**: 403 Forbidden
- **Not found (nonexistent task)**: 404 Not Found

## Security Validation

To verify the security implementation:

1. Test with a JWT token containing a different user_id than the one in the URL - should return 403 Forbidden
2. Test with an invalid/expired JWT token - should return 401 Unauthorized
3. Test with a non-existent task ID - should return 404 Not Found
4. Verify that users cannot access each other's tasks