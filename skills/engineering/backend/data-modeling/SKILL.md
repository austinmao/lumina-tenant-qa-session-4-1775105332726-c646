---
name: data-modeling
description: "Design database schemas, entity relationships, and migration strategies"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Design relational and document database schemas. Define entities, relationships, indexes, and migration paths.

## When to Use
- New feature requiring database tables
- Refactoring existing schema
- Planning data migration

## Principles
- Normalize to 3NF, denormalize for read performance
- Every table has created_at, updated_at timestamps
- Foreign keys with appropriate ON DELETE behavior
- Indexes on all foreign keys and common query predicates
- Migration files are sequential, idempotent, and reversible
