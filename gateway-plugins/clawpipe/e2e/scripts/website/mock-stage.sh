#!/bin/bash
# Mock website stage — writes stub output matching contract requirements
set -euo pipefail
STAGE="${1:-unknown}"

# Write YAML output to stdout (clawpipe captures it)
case "$STAGE" in
  strategy-interview)
    echo "interview_summary: completed"
    echo "site: acme-corp"
    echo "word_count: 250"
    ;;
  competitor-research)
    echo "competitors:"
    echo "  - name: competitor1"
    echo "    positioning: wellness retreats"
    ;;
  synthesize-brief)
    echo "personas:"
    echo "  - name: seeker"
    echo "    jobs_to_be_done: find safe retreat"
    echo "kpis:"
    echo "  - metric: conversion_rate"
    echo "    target: 3%"
    echo "  - metric: bounce_rate"
    echo "    target: 40%"
    echo "  - metric: time_on_page"
    echo "    target: 120s"
    echo "page_priorities:"
    echo "  - slug: home"
    echo "    rank: 1"
    echo "scope: 1 page (homepage POC)"
    ;;
  extract-brand-signals)
    echo "colors:"
    echo "  primary: '#14B8A6'"
    echo "fonts:"
    echo "  heading: Cormorant Garant"
    ;;
  generate-design-tokens)
    echo "tokens:"
    echo "  accent: '#14B8A6'"
    ;;
  build-brand-profile)
    echo "identity:"
    echo "  name: AcmeCo"
    echo "voice:"
    echo "  tone: warm, grounded"
    ;;
  build-sitemap)
    echo "pages:"
    echo "  - slug: home"
    echo "    url: /"
    ;;
  build-content-model)
    echo "types:"
    echo "  - name: page"
    echo "    fields: [title, body, cta]"
    ;;
  generate-page-spec)
    echo "sections:"
    echo "  - hero"
    echo "  - features"
    echo "cta: Book a call"
    echo "depends_on: []"
    ;;
  seo-keyword-injection)
    echo "primary_keyword: psychedelic retreat"
    echo "secondary:"
    echo "  - healing ceremony"
    ;;
  wireframe)
    echo "wireframe: ASCII layout for homepage with hero, features, CTA sections"
    echo "word_count: 100"
    ;;
  copy-draft)
    echo "hero: Transform Your Life"
    echo "cta: Begin Your Journey"
    echo "body: Experience profound healing in a safe, guided setting."
    ;;
  copy-review)
    echo "approved: true"
    echo "voice_score: 0.9"
    ;;
  visual-design)
    echo "tokens:"
    echo "  primary: '#14B8A6'"
    echo "breakpoints:"
    echo "  mobile: 375px"
    echo "  tablet: 768px"
    echo "  desktop: 1440px"
    echo "states:"
    echo "  - default"
    echo "  - hover"
    ;;
  design-handoff)
    echo "specs:"
    echo "  hero_height: 100vh"
    echo "assets:"
    echo "  - logo.svg"
    ;;
  implement-page)
    echo "page_tsx: generated"
    echo "aria-labels: present"
    echo "typescript: strict"
    ;;
  write-tests)
    echo "coverage: 85%"
    echo "pass: true"
    echo "tests: 12"
    ;;
  *)
    echo "stage: $STAGE"
    echo "status: completed"
    ;;
esac
exit 0
