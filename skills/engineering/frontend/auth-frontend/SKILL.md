---
name: auth-frontend
description: "Implement frontend authentication flows — OAuth2, session management, and protected routes"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /auth-frontend
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: []
      env: []
---

# Frontend Authentication Patterns

Implement client-side authentication flows including OAuth2/social login, session management, protected routes, and secure token handling. Use when building login/signup flows, implementing route guards, or integrating with auth providers.

## When to Use

- Building login/signup pages with form validation
- Implementing OAuth2/social login (Google, GitHub)
- Creating protected routes and role-based route guards
- Managing JWT tokens or sessions on the client
- Implementing secure token refresh flows

## Core Concepts

**Session-Based Auth (Frontend):**
- Session ID stored in httpOnly cookie (set by server)
- No client-side token management needed
- Automatic CSRF token handling

**Token-Based Auth (Frontend):**
- Store tokens in httpOnly cookies (NOT localStorage — XSS vulnerable)
- Implement silent token refresh before expiration
- Use `useTransition` for non-blocking auth state updates

**OAuth2 Flow (Frontend):**
- Redirect to provider authorization URL
- Handle callback with authorization code
- Exchange code for tokens (server-side)
- Store session, redirect to protected route

## Key Patterns

### Protected Route Component
Check auth state before rendering. Redirect to login if unauthenticated. Show loading state during auth check. Preserve intended destination for post-login redirect.

### Role-Based Access Control
`requireRole()` wrapper component checking user role against allowed roles. Return 403 component for unauthorized access. Role hierarchy: admin > moderator > user.

### Auth Context Provider
Provide auth state (user, isAuthenticated, isLoading) to component tree. Login/logout functions. Token refresh on app mount. Persist auth state across page reloads.

### Form Validation
Zod schemas for email/password validation. Password requirements: 12+ characters, uppercase, lowercase, number, special character. Real-time validation feedback. Rate limiting awareness (show retry messages).

## Security Best Practices

1. Never store tokens in localStorage (XSS vulnerable)
2. Use httpOnly, secure, sameSite cookies
3. Implement CSRF protection for session-based auth
4. Short-lived access tokens (15-30 minutes)
5. Validate all auth state server-side (never trust client)
6. Rate limit login attempts client-side (disable button, show countdown)
7. Clear sensitive data from memory on logout
