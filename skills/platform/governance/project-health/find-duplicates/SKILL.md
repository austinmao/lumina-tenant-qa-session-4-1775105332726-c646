---
name: find-duplicates
description: "Find duplicate or overlapping files, skills, and agents in the project"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /find-duplicates
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["md5", "bd"]
---

# Find Duplicates

Two-pass duplicate detection: content hash (exact copies) then semantic (overlapping purpose).

## Pass 1: Content Hash Scan

### Step 1: Hash all SKILL.md files

```bash
find skills/ -name "SKILL.md" -exec md5 {} \;
```

Group by hash. Any hash appearing 2+ times = exact duplicate.

### Step 2: Hash all SOUL.md files

```bash
find agents/ -name "SOUL.md" -exec md5 {} \;
```

### Step 3: Hash scripts

```bash
find scripts/ -name "*.sh" -o -name "*.py" | xargs md5
```

### Step 4: Report exact duplicates

For each group of identical files:
- List file paths
- Report content hash
- Recommend: keep one canonical copy, delete others (or merge if slightly different)

## Pass 2: Semantic Scan

### Step 1: Extract skill descriptions

Read the `description` field from every `skills/**/SKILL.md` frontmatter.
Build a table: skill name | description | permissions | directory.

### Step 2: Identify overlapping descriptions

Flag pairs where:
- Two skills mention the same verb + noun (e.g., both say "send email")
- Two skills reference the same external service (e.g., both call Resend API)
- Two skills have >60% word overlap in their descriptions

### Step 3: Extract agent purposes

Read the first `# Who I Am` paragraph from every `agents/**/SOUL.md`.
Build a table: agent path | purpose summary | skills list.

### Step 4: Identify overlapping agents

Flag pairs where:
- Two agents claim the same domain responsibility
- Two agents list the same skills but in different directories
- An agent's stated purpose is a subset of another agent's purpose

## Output Format

### Exact Duplicates

| File A | File B | Hash | Action |
|---|---|---|---|
| path/a | path/b | abc123 | Delete B (identical content) |

### Semantic Overlaps

| Item A | Item B | Overlap Type | Recommendation |
|---|---|---|---|
| skill-a | skill-b | Both send email via Resend | Merge into single skill |
| agent-x | agent-y | Both handle medical screening | Consolidate or clarify boundaries |

## Beads Integration

Create one beads issue per duplicate group:
```bash
bd create "Duplicate: [item-a] and [item-b] overlap" \
  --type chore --priority 2 \
  --description "Overlap type: [exact|semantic]. Details: [specifics]. Recommendation: [action]" \
  --labels "duplicates,project-health"
```
