---
name: api-design
description: "Design REST and GraphQL APIs with pagination, error handling, and versioning"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /api-design
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: []
      env: []
---

# API Design Principles

Design intuitive, scalable REST and GraphQL APIs with proper resource modeling, pagination, error handling, versioning, and documentation. Use when designing new APIs, reviewing API specifications, or establishing API design standards.

## When to Use

- Designing new REST or GraphQL APIs
- Refactoring existing APIs for better usability
- Establishing API design standards for a team
- Reviewing API specifications before implementation

## REST Design Principles

### Resource-Oriented Architecture
- Resources are nouns (users, orders, products), not verbs
- HTTP methods for actions: GET (retrieve), POST (create), PUT (replace), PATCH (update), DELETE (remove)
- URLs represent resource hierarchies: `/api/users/{id}/orders`
- Consistent naming: plural nouns for collections (`/users`, not `/user`)

### Pagination and Filtering
- Page-based: `?page=1&page_size=20` with total count in response
- Cursor-based: `?after=cursor&first=20` (Relay spec) for large datasets
- Filter parameters: `?status=active&created_after=2024-01-01&search=term`
- Always paginate collections — never return unbounded result sets

### Error Handling
- Consistent error response format: `{ error, message, details, timestamp, path }`
- Correct HTTP status codes: 2xx success, 4xx client errors, 5xx server errors
- Validation errors with field-level detail: `{ field, message, value }`
- Never expose internal error details in production responses

### Versioning
- URL versioning preferred: `/api/v1/users`
- Plan for breaking changes from day one
- Support two versions concurrently during migration

## GraphQL Design Principles

### Schema-First Development
- Types define domain model; Queries for reading; Mutations for modifying
- Cursor-based pagination (Relay spec) with `Connection`, `Edge`, `PageInfo`
- Input types for mutations; Payload types with `user` and `errors` fields
- Use `@deprecated` directive for gradual migration

### DataLoader Pattern (N+1 Prevention)
- Batch load functions group multiple individual fetches into single queries
- Map results back to input order for correct resolution
- Create per-request DataLoader instances to prevent cross-request caching

## Best Practices

**REST:** Stateless requests, always paginate, rate limit, use OpenAPI/Swagger docs, version APIs.
**GraphQL:** Schema first, use DataLoaders, validate at schema and resolver levels, track query complexity.
**Both:** Never expose database schema in API structure, consistent error formats, monitor performance.
