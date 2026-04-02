---
name: replay-page
description: "Build a webinar replay page from Zoom recording with countdown timer and CTA"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /replay-page
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - node
---

## Overview

Generates a Next.js App Router page at `web/src/app/replay/[slug]/page.tsx` from a `replay-config.json` file written by the zoom-recording skill. For v1, embeds Zoom recording via iframe (`share_url`). Future v2 adds Mux/YouTube providers.

## Input

Reads `web/data/replay-config.json` with the following schema:

```json
{
  "url": "https://zoom.us/rec/share/...",
  "expiresAt": "2026-04-03T17:00:00Z",
  "meetingId": "85162340877",
  "status": "active",
  "transcript_vtt_path": "web/data/replay-transcript.vtt",
  "summary": { "key_points": ["..."], "action_items": ["..."] }
}
```

| Field | Required | Description |
|---|---|---|
| `url` | Yes | Zoom share URL for iframe embed |
| `expiresAt` | Yes | ISO 8601 timestamp; replay page becomes unavailable after this |
| `meetingId` | Yes | Zoom meeting ID; used as the `[slug]` in the route |
| `status` | Yes | Must be `"active"` for page generation to proceed |
| `transcript_vtt_path` | No | Path to VTT transcript file for download link |
| `summary` | No | Object with `key_points` and `action_items` arrays |

## Page Components

1. **Zoom iframe embed**: `<iframe src={url} width="100%" height="500" />` wrapped in a responsive container (`aspect-video` or equivalent) that scales on mobile. Include `allowfullscreen` and `allow="autoplay"` attributes.

2. **Countdown timer**: Client Component (`"use client"`) showing `days:hours:minutes:seconds` until `expiresAt`. Updates every second via `setInterval`. When the timer reaches zero, replace the video iframe with a styled "This replay has expired" message and hide the CTA.

3. **Server-side expiry check**: In the Server Component (page.tsx), compare `new Date()` against `expiresAt`. If expired, return a 410 Gone response using Next.js App Router conventions:
   ```tsx
   import { notFound } from "next/navigation";
   // For expired replays, render an explicit 410 page
   ```
   Use `generateMetadata` to set appropriate meta tags including `robots: noindex` for expired pages.

4. **CTA section**: Rendered below the video embed. Contains a "Book a Connection Call" button linking to a configurable Calendly URL. The Calendly URL defaults to the value in `config/org.yaml` under `calendly.booking_url` if not overridden. Style the button prominently with the brand primary color.

5. **Key takeaways** (optional): If `summary.key_points` exists in the config, render as a bulleted list in a card below the CTA. If `transcript_vtt_path` exists, render a "Download Transcript" link pointing to the VTT file served from `/public/` or a static route.

## Steps

1. **Read config**: Load `web/data/replay-config.json`. If the file does not exist, abort with a clear error message: "replay-config.json not found. Run /zoom-recording first."

2. **Validate required fields**: Confirm `url`, `expiresAt`, `meetingId`, and `status` are all present and non-empty. If any are missing, abort with a message listing the missing fields.

3. **Check status**: If `status` is not `"active"`, abort with message: "Replay status is '{status}'. Only active replays can be built."

4. **Generate page**: Create or overwrite `web/src/app/replay/[slug]/page.tsx` using the React Server Component pattern:
   - Server Component (`page.tsx`) reads config at build/request time, checks expiry, and passes props to the client countdown component.
   - Client Component (`ReplayCountdown.tsx`) in the same directory handles the live countdown timer and iframe rendering.
   - Use `generateStaticParams` to pre-render the route for the current `meetingId` slug.

5. **Log completion**: Report to operator: "Replay page generated at /replay/{meetingId}. Expires: {expiresAt}."

## File Structure

After generation, the following files exist:

```
web/src/app/replay/[slug]/
  page.tsx              # Server Component — expiry check, metadata, layout
  ReplayCountdown.tsx   # Client Component — countdown timer + iframe embed
  ReplayCTA.tsx         # CTA button section
  ReplayTakeaways.tsx   # Optional key points + transcript download
```

## Error Handling

- **Missing config file**: Abort with actionable message pointing to the zoom-recording skill.
- **Invalid JSON**: Abort with parse error details.
- **Missing required fields**: List all missing fields in a single error message.
- **Inactive status**: Abort with current status value in the message.
- **Past expiresAt at generation time**: Warn operator but still generate the page (server-side 410 will handle runtime).

## Future Upgrade Path

v2 adds a `provider` field to `replay-config.json`. The embed strategy switches based on provider value:

| Provider | Embed Strategy |
|---|---|
| `"zoom"` | iframe with `share_url` (current v1 behavior) |
| `"mux"` | `@mux/mux-player-react` component with `playbackId` |
| `"youtube"` | YouTube embed iframe with `videoId` |

The `ReplayCountdown.tsx` component will accept a `provider` prop and render the appropriate embed. The countdown and CTA logic remain unchanged across providers.
