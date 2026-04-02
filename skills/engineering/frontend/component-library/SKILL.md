---
name: component-library
description: "Generate component documentation with props, variants, and usage examples"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /component-library
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Component Library Documentation

Generate Storybook-style component documentation from source code. Extracts props, variants, default values, and usage patterns. Produces a structured documentation file per component suitable for developer reference and design handoff. Use when documenting a component library, generating API docs for a design system, or onboarding new developers.

## Usage

```
/component-library <path-to-component>
```

Example:

```
/component-library web/src/components/Button.tsx
/component-library web/src/components/ui/
```

When a directory is provided, generate documentation for all components in the directory.

---

## Props Extraction

For each component, extract:

- **Prop name** — the property identifier
- **Type** — TypeScript type (string, number, boolean, union, enum, custom interface)
- **Required/Optional** — whether the prop has a `?` modifier or default value
- **Default value** — if a default is specified in destructuring or defaultProps
- **Description** — from JSDoc comments, inline comments, or inferred from usage context

Output format per prop:
```
| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| variant | "primary" \| "secondary" \| "ghost" | No | "primary" | Visual style variant |
| size | "sm" \| "md" \| "lg" | No | "md" | Button size |
| disabled | boolean | No | false | Disables interaction |
| onClick | () => void | Yes | — | Click handler |
```

---

## Variant Documentation

Identify and document all visual variants of the component:

- **Variant prop values** — enumerate all accepted values for variant-like props (variant, size, color, etc.)
- **Compound variants** — combinations of props that produce distinct visual states (e.g., `variant="primary" + size="lg"`)
- **State variants** — hover, focus, active, disabled, loading, error states
- **Responsive variants** — breakpoint-specific behavior if implemented

For each variant, provide:
```
### Variant: primary
- Props: variant="primary"
- Description: Default brand-colored button with filled background
- States: hover (darker bg), focus (ring), disabled (opacity 50%)
```

---

## Usage Examples

Generate practical code examples:

- **Basic usage** — minimal props required to render the component
- **With all props** — example showing every prop populated
- **Common patterns** — 2-3 real-world usage patterns (e.g., button in a form, button with icon, button group)
- **Composition** — how the component composes with other components in the library
- **Anti-patterns** — common misuses to avoid (e.g., nesting interactive elements, missing required props)

Example output:
```tsx
// Basic usage
<Button onClick={handleClick}>Submit</Button>

// With variant and size
<Button variant="secondary" size="lg" disabled>
  Processing...
</Button>

// With icon
<Button variant="ghost" size="sm">
  <ArrowIcon className="mr-2" />
  Back
</Button>
```

---

## Accessibility Notes

For each component, document:

- **ARIA role** — the implicit or explicit role
- **Keyboard interaction** — expected keyboard behavior (Enter, Space, Escape, Arrow keys)
- **Screen reader behavior** — how the component is announced
- **Focus management** — focus behavior on interaction
- **Required ARIA attributes** — any ARIA props the consumer must provide

---

## Import and Dependencies

- **Import path** — the canonical import for the component
- **Peer dependencies** — other components or packages required
- **CSS/token dependencies** — design tokens or stylesheets the component expects

---

## Output Format

For each component, produce:

```markdown
# <ComponentName>

<one-line description>

## Import

\`\`\`tsx
import { <ComponentName> } from '@/components/<path>';
\`\`\`

## Props

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Variants

### <variant-name>
...

## Usage Examples

### Basic
\`\`\`tsx
...
\`\`\`

### Common Patterns
\`\`\`tsx
...
\`\`\`

## Accessibility

- Role: ...
- Keyboard: ...
- Screen reader: ...

## Dependencies

- ...
```

Save the documentation to `memory/reports/component-docs/<ComponentName>.md`.

When generating for a directory, also produce an index file at `memory/reports/component-docs/index.md` listing all documented components.

---

## Error Handling

- If the component file does not export a React component: report "No React component export found in <path>" and skip
- If the component has no typed props (e.g., no interface or type declaration): document with "Props: None (component accepts no props)" and continue with variant and usage sections
- If the file is empty or unparseable: report "Cannot parse <path>" and skip

## Issue Routing

Documentation gaps and undocumented components are reported to **Nova** (frontend engineer, `agents/engineering/frontend-engineer`) for prop type additions or JSDoc comments.
