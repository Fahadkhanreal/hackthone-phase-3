# Research: RESTful API Endpoints and JWT Security for Multi-User Todo Application

**Feature**: 003-api-jwt-security
**Date**: 2026-01-26

## Decision: JWT Implementation Choice (PyJWT vs python-jose)

**Rationale**: PyJWT is the most widely adopted and maintained library for JWT handling in Python. It has better documentation, community support, and is actively maintained. While python-jose offers additional cryptographic features, PyJWT is sufficient for our symmetric key (HS256) approach.

**Alternatives considered**:
- python-jose[cryptography]: More complex but provides additional cryptographic algorithms
- Manual JWT implementation: Would require significant security-sensitive code maintenance

## Decision: HS256 Algorithm for JWT

**Rationale**: HS256 (HMAC with SHA-256) is the standard algorithm for symmetric key JWT signing. It's secure when using a strong secret key and is the most commonly used algorithm for server-side token verification. It fits perfectly with the shared secret approach from Better Auth.

**Alternatives considered**:
- RS256 (RSA): Requires public/private key pairs which are more complex to manage
- ES256 (ECDSA): Elliptic curve cryptography, more complex but offers smaller signatures

## Decision: JWT Payload Structure

**Rationale**: Using "user_id" as the primary identifier in JWT payload is clear and explicit for our use case. While "sub" is the standard JWT claim for subject, using "user_id" makes the code more readable and self-documenting in our context.

**Alternatives considered**:
- Using "sub" claim: Standard but less explicit for our use case
- Multiple claims: Would add complexity without clear benefit

## Decision: Authentication Dependency Pattern

**Rationale**: FastAPI's dependency injection system with Depends() is the idiomatic way to handle authentication. Creating a get_current_user dependency that extracts and validates the JWT token is the recommended pattern for securing endpoints.

**Alternatives considered**:
- Manual token validation in each endpoint: Repetitive and error-prone
- Decorator-based approach: Less flexible than FastAPI's dependency system

## Decision: User ID Matching Enforcement

**Rationale**: Comparing the user_id extracted from the JWT token with the user_id in the URL path is the most secure way to prevent cross-user data access. This ensures users can only operate on their own data regardless of the task_id.

**Alternatives considered**:
- Only checking ownership in database queries: Could miss validation in some scenarios
- Additional role-based checks: Not needed for basic user ownership model

## Decision: Error Response Format

**Rationale**: Using consistent JSON error responses with appropriate HTTP status codes (401, 403, 404) follows REST API best practices and makes client-side error handling predictable.

**Alternatives considered**:
- Plain text error messages: Less structured for client consumption
- Custom error formats: Would require additional client-side parsing logic