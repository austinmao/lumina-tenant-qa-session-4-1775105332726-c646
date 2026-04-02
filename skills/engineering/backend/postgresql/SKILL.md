---
name: postgresql
description: "Design PostgreSQL schemas with proper types, indexing, constraints, and performance patterns"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /postgresql
metadata:
  openclaw:
    emoji: "🐘"
    requires:
      bins: []
      env: []
---

# PostgreSQL Table Design

Design PostgreSQL schemas with best-practice data types, indexing strategies, constraints, partitioning, and performance patterns. Use when designing new database schemas, optimizing existing tables, or solving PostgreSQL-specific problems.

## Core Rules

- Define a PRIMARY KEY for reference tables. Prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness or opacity is needed.
- Normalize first (to 3NF); denormalize ONLY for measured, high-ROI reads where join performance is proven problematic.
- Add NOT NULL everywhere semantically required; use DEFAULTs for common values.
- Create indexes for access paths actually queried: PK/unique (auto), FK columns (manual), frequent filters/sorts.

## Data Type Rules

**Preferred types:**
- IDs: `BIGINT GENERATED ALWAYS AS IDENTITY` (or `UUID` with `gen_random_uuid()` for distributed)
- Strings: `TEXT` (never `VARCHAR(n)` or `CHAR(n)`)
- Money: `NUMERIC(p,s)` (never float, never `money` type)
- Time: `TIMESTAMPTZ` (never `TIMESTAMP` without timezone)
- Booleans: `BOOLEAN` with `NOT NULL`
- Enums: `CREATE TYPE ... AS ENUM` for stable sets; TEXT + CHECK for evolving values
- JSON: `JSONB` with GIN index (never `JSON` unless ordering must be preserved)

**Never use:** `timestamp` (without tz), `char(n)`, `varchar(n)`, `money`, `timetz`, `serial`

## PostgreSQL Gotchas

- Unquoted identifiers lowercased — use `snake_case`
- FK columns NOT auto-indexed — always add indexes manually
- `UNIQUE` allows multiple NULLs — use `NULLS NOT DISTINCT` (PG15+)
- Identity sequences have gaps (normal — do not "fix")
- Updates leave dead tuples — design to avoid hot wide-row churn

## Indexing Strategy

| Index Type | Use Case |
|---|---|
| B-tree (default) | Equality, range, ORDER BY |
| Composite | Multi-column filters (leftmost prefix rule) |
| Covering (INCLUDE) | Index-only scans without table access |
| Partial | Hot subsets (`WHERE status = 'active'`) |
| Expression | Computed keys (`LOWER(email)`) |
| GIN | JSONB, arrays, full-text search |
| GiST | Ranges, geometry, exclusion constraints |
| BRIN | Very large naturally-ordered data (time-series) |

## Special Patterns

**Update-heavy tables:** Separate hot/cold columns, `fillfactor=90` for HOT updates, avoid updating indexed columns.
**Insert-heavy workloads:** Minimize indexes, use `COPY` or multi-row INSERT, UNLOGGED for rebuildable staging, partition by time/hash.
**Upsert:** Requires UNIQUE index on conflict target, use `EXCLUDED.column`, `DO NOTHING` faster than `DO UPDATE` when no actual update needed.
**Safe schema evolution:** Transactional DDL, `CREATE INDEX CONCURRENTLY`, volatile defaults cause table rewrites.

## Row-Level Security

`ALTER TABLE tbl ENABLE ROW LEVEL SECURITY; CREATE POLICY user_access ON orders FOR SELECT TO app_users USING (user_id = current_user_id());`

## Essential Extensions

pgcrypto (hashing), pg_trgm (fuzzy search), timescaledb (time-series), postgis (geospatial), pgvector (embeddings), pgaudit (audit logging).
