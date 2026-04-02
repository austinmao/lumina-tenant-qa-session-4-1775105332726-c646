---
name: interaction-design
description: "Design microinteractions, motion, transitions, and user feedback patterns"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /interaction-design
metadata:
  openclaw:
    emoji: "✨"
    requires:
      bins: []
      env: []
---

# Interaction Design

Design and implement microinteractions, motion design, transitions, loading states, and user feedback patterns that enhance usability. Use when adding polish to UI interactions, implementing skeleton screens, or creating gesture-based interfaces.

## When to Use

- Adding microinteractions for user feedback
- Implementing page and component transitions
- Designing loading states and skeleton screens
- Creating gesture-based interactions (swipe, drag)
- Building notification and toast systems
- Adding scroll-triggered animations

## Core Principles

### Purposeful Motion
Motion should communicate, not decorate:
- **Feedback:** Confirm user actions occurred
- **Orientation:** Show where elements come from/go to
- **Focus:** Direct attention to important changes
- **Continuity:** Maintain context during transitions

### Timing Guidelines

| Duration | Use Case |
|---|---|
| 100-150ms | Micro-feedback (hovers, clicks) |
| 200-300ms | Small transitions (toggles, dropdowns) |
| 300-500ms | Medium transitions (modals, page changes) |
| 500ms+ | Complex choreographed animations |

### Easing Functions
- `ease-out` (decelerate): entering elements
- `ease-in` (accelerate): exiting elements
- `ease-in-out`: moving between positions
- `spring` (cubic-bezier overshoot): playful interactions

## Key Patterns

1. **Skeleton screens:** Preserve layout while loading with `animate-pulse` placeholder blocks
2. **Progress indicators:** Determinate progress bars with smooth width animation
3. **State transitions:** Toggle switches with spring physics (`stiffness: 500, damping: 30`)
4. **Page transitions:** `AnimatePresence` + `motion.div` for enter/exit animations
5. **Feedback patterns:** Ripple effect on click, scale on tap (`whileTap={{ scale: 0.98 }}`)
6. **Gesture interactions:** Swipe-to-dismiss with drag constraints and velocity thresholds

## Accessibility

Always respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Performance Rules

1. Animate only `transform` and `opacity` for 60fps
2. Use `will-change` sparingly for GPU acceleration
3. Prefer spring animations over linear for natural feel
4. Clean up animation listeners on component unmount
5. Never prevent user input during animations
