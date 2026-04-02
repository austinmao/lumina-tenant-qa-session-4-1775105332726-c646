---
name: faq-lookup
description: "Look up approved FAQ answers for common retreat questions"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "❓"
---

# faq-lookup

Retrieve approved answers to common questions about retreats and the ritual experience. Always use this skill before composing answers to factual questions — never fabricate or estimate.

## FAQ Content

Load FAQ content from `config/faqs.yaml`.

The config defines Q&A pairs organized by topic (safety, what_to_expect, who_its_for, medical_medications, pricing, application), along with escalation flags and a fallback response for uncovered topics.

## Rules (generic)
- If the topic is not covered in the loaded FAQ config, use the `fallback_response` field from the config.
- For any FAQ entry where `escalate: true`, follow the `escalate_to` directive in the config.
- Never fabricate answers — only use content from the loaded config.
