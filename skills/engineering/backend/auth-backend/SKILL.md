---
name: auth-backend
description: "Implement backend authentication — JWT, OAuth2, RBAC, and session security"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /auth-backend
metadata:
  openclaw:
    emoji: "🔑"
    requires:
      bins: []
      env: []
---

# Backend Authentication & Authorization

Implement secure server-side authentication and authorization including JWT token management, OAuth2 provider integration, session security, RBAC, and permission-based access control. Use when building auth systems, securing APIs, or implementing access control.

## When to Use

- Implementing user authentication on the server
- Securing REST or GraphQL API endpoints
- Adding OAuth2/social login provider integration
- Implementing role-based access control (RBAC)
- Designing session management and token rotation
- Building rate limiting for auth endpoints

## JWT Authentication

### Token Generation
- Short-lived access tokens (15 minutes): `jwt.sign({ userId, email, role }, secret, { expiresIn: '15m' })`
- Long-lived refresh tokens (7 days) stored hashed in database
- Always hash refresh tokens before database storage

### Token Refresh Flow
1. Client sends expired access token + refresh token
2. Server verifies refresh token against hashed database entry
3. Server issues new access token
4. Optional: rotate refresh token (revoke old, issue new)

### Authentication Middleware
Extract Bearer token from Authorization header. Verify signature and expiration. Attach decoded user payload to request context. Return 401 for missing/invalid tokens.

## Session-Based Authentication

- Redis-backed session store for horizontal scaling
- Cookie configuration: `httpOnly: true`, `secure: true` (HTTPS), `sameSite: 'strict'`, `maxAge: 24h`
- Session ID regeneration on login (prevent fixation)
- Explicit session destruction on logout with cookie clearing

## OAuth2 / Social Login

- Google, GitHub strategies via Passport.js
- Find-or-create user pattern on OAuth callback
- Map provider profile (id, email, name, avatar) to local user record
- Generate JWT after successful OAuth, redirect to frontend with token

## Authorization Patterns

### Role-Based Access Control (RBAC)
Role hierarchy: `admin > moderator > user`. `requireRole(...roles)` middleware checks user role against allowed roles.

### Permission-Based Access Control
Fine-grained permissions: `read:users`, `write:users`, `delete:users`. Role-to-permission mapping. `requirePermission(...permissions)` middleware.

### Resource Ownership
Check resource ownership before allowing mutations. Admin bypass for all resources. Return 403 for unauthorized, 404 for not found.

## Security Best Practices

1. Hash passwords with bcrypt (saltRounds=12) or argon2
2. Validate password strength with Zod: 12+ chars, mixed case, number, special char
3. Rate limit auth endpoints: 5 attempts per 15 minutes per IP
4. Log all security events: login attempts, failed auth, token refresh
5. Use HTTPS exclusively — HSTS header with `max-age=31536000`
6. Rotate JWT secrets regularly
7. Implement CSRF protection for session-based auth
8. Never expose password hashes or internal errors in API responses
