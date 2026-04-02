---
name: generate-wireframe
description: "Generate a wireframe for a page / create ASCII layout from spec"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "📐"
    requires:
      os: ["darwin"]
---

# Wireframe Generator Skill

Generates ASCII wireframes showing layout blocks, content hierarchy, CTA placement, and responsive breakpoints from a page spec or blueprint.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `site_dir`, `brand_root`, and `website.blueprint` from site context.
3. Read the blueprint at `website.blueprint` for page specs (if generating from blueprint).

---

## Steps

### 1. Determine page spec

Accept input from one of:
- A page name that exists in the blueprint (reads the spec from the blueprint file).
- A verbal description from the user ("homepage with hero, features, testimonials, CTA").
- A reference URL (reads the page structure conceptually -- does not fetch).

### 2. Define content blocks

Break the page into vertical sections. For each section, define:
- Section name (e.g., Hero, Features, Testimonials, CTA).
- Content elements: heading, body text, image, button, form, list, grid.
- Layout: full-width, two-column, three-column, sidebar.
- Priority: above-fold vs below-fold.

### 3. Generate desktop wireframe (1280px)

Produce an ASCII wireframe using box-drawing characters:

```
+--------------------------------------------------+
|  [Logo]              [Nav] [Nav] [Nav]   [CTA]   |
+--------------------------------------------------+
|                                                    |
|           [H1: Hero Headline]                      |
|           [Subheadline text]                       |
|           [====Primary CTA====]                    |
|                                                    |
+--------------------------------------------------+
|  [Feature 1]    [Feature 2]    [Feature 3]        |
|  [icon]         [icon]         [icon]              |
|  [text]         [text]         [text]              |
+--------------------------------------------------+
```

### 4. Generate mobile wireframe (375px)

Show how blocks restack on mobile:
- Multi-column layouts collapse to single column.
- Navigation collapses to hamburger menu.
- Images resize or are replaced with smaller variants.
- CTAs remain prominent and full-width.

### 5. Annotate

Add notes below the wireframe:
- CTA button text (from brand guide's primary CTA if available).
- Approximate section heights.
- Scroll depth markers (above fold / below fold).
- Interactive elements (hover states, expandable sections).

---

## Output

```markdown
## Wireframe — <page_name>
Site: <site_id> | Date: YYYY-MM-DD

### Desktop (1280px)
[ASCII wireframe]

### Mobile (375px)
[ASCII wireframe]

### Annotations
- Hero: above fold, H1 + subhead + primary CTA
- [additional section notes]

### Content Requirements
| Section | Heading | Body words | Images | CTA |
|---|---|---|---|---|
```

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If blueprint does not exist and no page spec is provided: ask user to describe the page structure.
- If a referenced section type is ambiguous: ask user to clarify before generating.
