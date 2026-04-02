---
name: design-motion
description: "Define animation specs for a component / specify micro-interactions and transitions"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      os: ["darwin"]
---

# Design Motion Skill

Produces motion specifications for web components: easing curves, durations, triggers, stagger timing. References the Motion library (Framer Motion). Covers page transitions, scroll animations, hover states, and loading states.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` for existing motion tokens (if defined).

---

## Steps

### 1. Identify the component

Accept from the user:
- Component name or page section (e.g., "hero section", "card grid", "navigation menu").
- Interaction type: entrance, exit, hover, scroll-triggered, page transition, loading state.

### 2. Define motion properties

For each animation, specify:

| Property | Description | Example |
|---|---|---|
| **Trigger** | What starts the animation | `on:viewport-enter`, `on:hover`, `on:mount`, `on:route-change` |
| **Duration** | How long it takes | `0.3s`, `0.5s`, `0.8s` |
| **Easing** | Acceleration curve | `ease-out`, `[0.16, 1, 0.3, 1]` (spring) |
| **Delay** | Wait before starting | `0s`, `0.1s` |
| **Stagger** | Delay between children | `0.05s` per child |
| **Properties** | What animates | `opacity`, `transform`, `height` |
| **From** | Starting state | `opacity: 0, y: 20px` |
| **To** | Ending state | `opacity: 1, y: 0` |

### 3. Apply motion principles

- **Entrance**: Elements enter from below or fade in. Duration: 0.3-0.6s. Easing: ease-out.
- **Exit**: Elements fade out or scale down. Duration: 0.2-0.3s. Easing: ease-in.
- **Hover**: Subtle scale (1.02-1.05) or color shift. Duration: 0.15-0.2s.
- **Scroll**: Triggered at 20% viewport visibility. Stagger children 0.05-0.1s apart.
- **Page transitions**: Crossfade or slide. Duration: 0.3-0.5s.
- **Loading**: Skeleton shimmer or pulse. Loop until content loads.
- **Reduced motion**: Always provide `prefers-reduced-motion` fallback (instant state, no animation).

### 4. Generate Motion library code

Produce a Framer Motion (Motion) code snippet:

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
>
```

For scroll-triggered animations:
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.2 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
>
```

---

## Output

```markdown
## Motion Spec — <component_name>
Site: <site_id> | Date: YYYY-MM-DD

### Animation Table
| Element | Trigger | From | To | Duration | Easing | Delay |
|---|---|---|---|---|---|---|

### Stagger
- Children stagger: Xs per child
- Direction: top-to-bottom / left-to-right

### Reduced Motion Fallback
- All animations: instant transition (duration: 0)

### Code
[Framer Motion code snippet]
```

---

## Guidelines

- Keep total animation time under 1s per interaction. Users perceive delays over 1s as sluggish.
- Never animate `width`, `height`, or `top`/`left` -- use `transform` and `opacity` for GPU-accelerated performance.
- Scroll animations should fire once (`viewport.once: true`) unless explicitly looping.
- Match motion style to the brand -- energetic brands use faster, bouncier curves; calm brands use slower, smoother curves.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If design tokens have no motion section: use the default principles above.
- If component type is unclear: ask user to specify before generating.
