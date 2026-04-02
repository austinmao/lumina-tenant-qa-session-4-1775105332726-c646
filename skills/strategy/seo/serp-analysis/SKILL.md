---
name: serp-analysis
description: "Analyze SERP features and format content for featured snippets"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /serp-analysis
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: []
      env: []
---

# SERP Analysis

Format content to be eligible for featured snippets and SERP features. Create snippet-optimized content blocks based on best practices for paragraph, list, and table snippet types. Use when optimizing question-based content for position zero or People Also Ask dominance.

## When to Use

- Optimizing content for featured snippets
- Creating FAQ content for People Also Ask
- Formatting comparison content for table snippets
- Structuring how-to content for list snippets
- Analyzing current SERP landscape for target queries

## Snippet Types and Formatting

### Paragraph Snippets (40-60 words)
- Direct answer in opening sentence
- Question-based H2/H3 headers
- Clear, concise definitions
- No unnecessary filler words
- First sentence is a standalone citation candidate

### List Snippets
- Numbered steps for processes (5-8 items optimal)
- Bullet points for features or options
- Clear heading immediately before the list
- Concise item descriptions
- Complete, actionable list items

### Table Snippets
- Comparison data with clear column headers
- Specifications and pricing
- Structured information with consistent formatting
- Use HTML `<table>` elements (not Markdown-only)

## Content Optimization Strategy

1. Identify question-based queries for target topic
2. Determine best snippet format for each question type
3. Create snippet-optimized content blocks
4. Format answers concisely (40-60 word direct answer)
5. Structure surrounding context for depth
6. Add FAQ schema markup where applicable

## Output

**Snippet Package per target query:**

```markdown
## [Exact Question from SERP]

[40-60 word direct answer paragraph with keyword in first sentence.
Clear, definitive response that fully answers the query.]

### Supporting Details:
- Point 1 (enriching context)
- Point 2 (related data point)
- Point 3 (additional value)
```

**Deliverables:**
- Snippet-optimized content blocks
- PAA (People Also Ask) question/answer pairs
- Format recommendations (paragraph/list/table per query)
- Schema markup code (FAQPage, HowTo) for AI readability
- Voice search optimization recommendations
