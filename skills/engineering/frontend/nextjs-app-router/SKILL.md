---
name: nextjs-app-router
description: "Build Next.js App Router features with Server Components, streaming, and Server Actions"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /nextjs-app-router
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: []
      env: []
---

# Next.js App Router Patterns

Build production Next.js 14+ applications using App Router with Server Components, streaming, parallel routes, intercepting routes, and Server Actions. Use when building new Next.js features, implementing data fetching patterns, or optimizing rendering strategy.

## When to Use

- Building new Next.js pages or features with App Router
- Implementing Server Components and streaming patterns
- Setting up parallel routes or intercepting routes
- Optimizing data fetching, caching, and revalidation
- Building full-stack features with Server Actions
- Migrating from Pages Router to App Router

## Rendering Modes

| Mode | Where | When to Use |
|---|---|---|
| Server Components | Server only | Data fetching, heavy computation, secrets access |
| Client Components | Browser | Interactivity, hooks, browser APIs |
| Static | Build time | Content that rarely changes |
| Dynamic | Request time | Personalized or real-time data |
| Streaming | Progressive | Large pages, slow data sources (Suspense boundaries) |

## File Conventions

```
app/
├── layout.tsx       # Shared UI wrapper (persists across navigation)
├── page.tsx         # Route UI (unique per route)
├── loading.tsx      # Suspense loading UI
├── error.tsx        # Error boundary
├── not-found.tsx    # 404 UI
├── route.ts         # API endpoint (Route Handler)
├── template.tsx     # Re-mounted layout
├── default.tsx      # Parallel route fallback
└── opengraph-image.tsx  # OG image generation
```

## Key Patterns

### 1. Server Components with Data Fetching
- Default: components are Server Components (no 'use client' directive)
- Fetch data directly in components with `async/await`
- Use `<Suspense>` boundaries for streaming with `fallback` loading UI
- Key searchParams with `JSON.stringify` for Suspense invalidation

### 2. Client Components
- Add `'use client'` directive at the top of the file
- Use for interactivity: `useState`, `useEffect`, event handlers, browser APIs
- Use `useTransition` for non-blocking updates with Server Actions
- Keep client boundary as low in the component tree as possible

### 3. Server Actions
- Mark with `"use server"` directive
- Use `revalidateTag` and `revalidatePath` for cache invalidation after mutations
- Access `cookies()` and `headers()` for server-side context
- Return structured results `{ success: true }` or `{ error: "message" }`
- Use `redirect()` for navigation after successful mutations

### 4. Parallel Routes
- Use `@slot` convention in layout for independent loading states
- Each slot loads independently with its own `loading.tsx` and `error.tsx`
- Use `default.tsx` for fallback when slot has no matching content

### 5. Intercepting Routes
- `(.)` for same level, `(..)` for one level up, `(...)` for root
- Common pattern: modal overlay on navigation, full page on direct URL access

### 6. Caching Strategy
```typescript
fetch(url, { cache: 'no-store' })           // Always fresh
fetch(url, { cache: 'force-cache' })        // Static (default)
fetch(url, { next: { revalidate: 60 } })    // ISR - revalidate after 60s
fetch(url, { next: { tags: ['products'] } }) // Tag-based invalidation
```

### 7. Metadata and SEO
- Export `metadata` object or `generateMetadata` async function
- Use `generateStaticParams` for static page generation
- Include OpenGraph and Twitter Card metadata

## Best Practices

**Do:**
- Start with Server Components, add `'use client'` only when needed
- Colocate data fetching where data is used
- Use Suspense boundaries for progressive rendering
- Leverage Server Actions for mutations with progressive enhancement
- Use tag-based cache invalidation for precise control

**Do Not:**
- Pass non-serializable data across Server/Client boundary
- Use React hooks in Server Components
- Fetch data in Client Components when Server Components suffice
- Over-nest layouts (each adds to component tree)
- Skip loading states (always provide `loading.tsx` or Suspense fallback)
