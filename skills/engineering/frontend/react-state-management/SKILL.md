---
name: react-state-management
description: "Set up React state management with Zustand, Jotai, Redux Toolkit, or React Query"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /react-state-management
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: []
      env: []
---

# React State Management

Implement modern React state management using Redux Toolkit, Zustand, Jotai, and React Query. Choose the right solution based on app complexity, and combine client and server state management correctly. Use when setting up state management, choosing between libraries, or implementing optimistic updates.

## When to Use

- Setting up global state management in a React application
- Choosing between Redux Toolkit, Zustand, or Jotai
- Managing server state with React Query or SWR
- Implementing optimistic updates for responsive UX
- Migrating from legacy Redux to modern patterns

## State Categories

| Type | Description | Recommended Solutions |
|---|---|---|
| Local State | Component-specific, UI state | `useState`, `useReducer` |
| Global State | Shared across components | Redux Toolkit, Zustand, Jotai |
| Server State | Remote data, caching | React Query, SWR, RTK Query |
| URL State | Route parameters, search | React Router, nuqs |
| Form State | Input values, validation | React Hook Form, Formik |

## Selection Criteria

```
Small app, simple state       → Zustand or Jotai
Large app, complex state      → Redux Toolkit
Heavy server interaction      → React Query + light client state
Atomic/granular updates       → Jotai
```

## Key Patterns

### Zustand (Simplest Global State)
- `create` store with typed interface
- Slice pattern for scalable stores: `createUserSlice`, `createCartSlice`
- Middleware: `devtools` (debugging), `persist` (localStorage)
- Selective subscriptions to prevent unnecessary re-renders

### Redux Toolkit (Complex State)
- `configureStore` with typed hooks (`useAppDispatch`, `useAppSelector`)
- `createSlice` with Immer-powered immutable updates
- `createAsyncThunk` for async operations with loading/error states
- RTK Query for API caching layer

### Jotai (Atomic State)
- Bottom-up atomic model: `atom` for state, derived atoms for computed values
- `atomWithStorage` for persistence
- Async atoms with Suspense integration
- Write-only atoms for actions (`logoutAtom`)

### React Query (Server State)
- Query key factories for organized cache management
- `useQuery` with `staleTime` and `gcTime` configuration
- `useMutation` with optimistic updates: `onMutate` → `onError` rollback → `onSettled` refetch
- Selective query invalidation with `invalidateQueries`

### Combined Pattern
- Zustand for client/UI state (sidebar, modals, theme)
- React Query for all server data (users, products, analytics)
- Never duplicate server state in client stores

## Best Practices

**Do:** Colocate state near usage, use selectors for render optimization, normalize data, full TypeScript coverage, separate server from client state concerns.

**Do Not:** Over-globalize state, duplicate server state in stores, mutate state directly, store derived/computed data, mix paradigms unnecessarily.
