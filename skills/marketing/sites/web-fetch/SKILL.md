---
name: web-fetch
description: Fetch a website URL and return raw HTML for brand analysis. First stage
  of the brand-preview pipeline.
version: 0.1.0
permissions:
  filesystem: none
  network: true
triggers:
- command: /web-fetch
metadata:
  openclaw:
    emoji: ':wrench:'
---

# Overview

<!-- oc:section id="overview" source="authored" checksum="9561036081bf" generated="2026-03-19" -->
Fetch a website URL and return raw HTML for brand analysis. This is a Lobster pipeline step — it runs as the first stage of the demo-brand-preview workflow, outputting truncated HTML to stdout for the brand-extract stage.
<!-- /oc:section id="overview" -->

## Usage

<!-- oc:section id="usage" source="authored" checksum="9d8bebc2f58b" generated="2026-03-19" -->
## Steps

1. Receive the target URL from the pipeline message
2. Perform HTTP GET with User-Agent header and 10-second timeout
3. If fetch fails, return a minimal fallback HTML stub
4. Truncate HTML to 8000 characters to fit downstream context windows
5. Extract and prepend key meta signals: title, meta description, theme-color, og:image
6. Output the extracted signals + truncated HTML as structured text to stdout

## Output

Plain text to stdout containing:
- Line 1: brand signals summary (title, description, theme-color, og:image)
- Remaining: truncated raw HTML

## Error Handling

- Timeout after 10s: return fallback HTML stub with generic metadata
- Non-200 status: return fallback HTML stub
- Invalid URL: return error message to stdout
<!-- /oc:section id="usage" -->

## Requirements

<!-- oc:section id="requirements" source="authored" checksum="6feff7f5b99a" generated="2026-03-19" -->
- Filesystem: `none`
- Network: `true` (HTTP GET to external URLs)
- Dependencies: `curl` binary
- No env vars required
<!-- /oc:section id="requirements" -->
