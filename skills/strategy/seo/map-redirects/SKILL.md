---
name: map-redirects
description: "Generate redirect map for site migration / map old URLs to new URLs"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      os: ["darwin"]
---

# Redirect Map Skill

Generates a redirect map for site migrations. Reads old URL lists, maps to new URL structure, and produces redirect rules in Next.js or Vercel format.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `domain`, `site_dir`, and `website.blueprint` from site context.

---

## Steps

### 1. Collect old URLs

Accept source URL list from one of:
- An old sitemap XML file (user provides path).
- A plain text file with one URL per line.
- A CSV with at minimum a `url` column.
- Manual list from the user.

Parse and deduplicate. Remove query strings and fragments unless user specifies otherwise.

### 2. Collect new URL structure

Read the new site's URL structure from:
- The sitemap in `<site_dir>` (if it exists).
- The blueprint at `website.blueprint` (page hierarchy section).
- Or accept a manual new URL list from the user.

### 3. Generate mappings

For each old URL:
1. Attempt exact slug match to a new URL.
2. If no exact match, attempt fuzzy match by page title or content topic.
3. If no match, flag as "needs manual mapping" with suggested candidates.

Classify each redirect:
- **301** (permanent): default for all page moves.
- **308** (permanent, preserves method): for API endpoints.
- **No redirect needed**: URL is unchanged.

### 4. Output redirect rules

Generate in the format requested by the user (default: Next.js):

**Next.js `next.config.ts` format:**
```typescript
async redirects() {
  return [
    { source: '/old-path', destination: '/new-path', permanent: true },
  ];
}
```

**Vercel `vercel.json` format:**
```json
{
  "redirects": [
    { "source": "/old-path", "destination": "/new-path", "permanent": true }
  ]
}
```

---

## Output

```markdown
## Redirect Map — <domain>
Date: YYYY-MM-DD | Old URLs: N | Mapped: N | Unresolved: N

### Mapped Redirects
| Old URL | New URL | Type | Confidence |
|---|---|---|---|
| /old | /new | 301 | exact/fuzzy |

### Unchanged URLs
| URL | Status |
|---|---|
| /stays-same | no redirect needed |

### Needs Manual Mapping
| Old URL | Suggested candidates | Reason |
|---|---|---|
| /orphan | /candidate-a, /candidate-b | no exact match |

### Generated Config
[Next.js or Vercel format code block]
```

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If old URL source file does not exist: report the expected path and stop.
- If new URL structure cannot be determined: ask user to provide the new sitemap or URL list.
