---
name: schema-markup
description: "Add JSON-LD structured data to pages for rich results and GEO citation accuracy"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /schema-markup
metadata:
  openclaw:
    emoji: "label"
---

# Schema Markup

## Overview

Add JSON-LD structured data to Next.js App Router pages to enable Google rich results and improve GEO (Generative Engine Optimization) citation accuracy. Use this skill whenever a page needs schema markup added, fixed, or optimized.

## Core Principles

1. **Accuracy first** -- Schema must reflect actual visible page content. Never mark up content that does not exist on the page.
2. **JSON-LD format only** -- Google recommends JSON-LD. Place it inside a `<script type="application/ld+json">` tag.
3. **Follow Google structured data guidelines** -- Only use markup types and properties Google actively supports for rich results. Check eligibility before implementing.
4. **Always validate** -- Test every implementation with Google Rich Results Test before deploying.
5. **GEO priority** -- Structured data is how AI models understand and trust entities. A complete entity graph in structured data dramatically increases citation probability across all AI search platforms.

---

## GEO-Specific Schema Guidance (Merged from geo-schema)

### sameAs Strategy (Critical for AI Entity Recognition)

The `sameAs` property is the single most important structured data property for GEO. It tells AI systems: "This entity on my website is the SAME entity as these profiles elsewhere." This creates the entity graph AI platforms use to verify, trust, and cite sources.

**Recommended sameAs links (priority order):**
1. Wikipedia article (highest authority entity link)
2. Wikidata item (machine-readable identifier, e.g., `https://www.wikidata.org/wiki/Q12345`)
3. LinkedIn (company page or personal profile)
4. YouTube (channel URL)
5. Twitter/X (profile URL)
6. Facebook (page URL)
7. Crunchbase (company profile, for startups/tech)
8. GitHub (organization profile, for tech companies)
9. Google Scholar / ORCID (for researchers/academics)

### knowsAbout Property

Add `knowsAbout` to Organization and Person schemas to signal topic expertise to AI models:
```json
"knowsAbout": ["Topic 1", "Topic 2", "Topic 3"]
```

### speakable Property (Voice/AI Assistants)

Mark passages suitable for voice and AI assistant citation:
```json
{
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-takeaway"]
  }
}
```

### Deprecated/Changed Schemas (2023-2024)

| Schema | Status | Note |
|---|---|---|
| HowTo | Rich results deprecated Aug 2023 | Still useful for AI parsing |
| FAQPage | Restricted to govt/health Aug 2023 | Still useful for AI parsing |
| SpecialAnnouncement | Deprecated 2023 | Remove if present |
| VideoObject contentUrl | Changed 2024 | Must point to actual video file |

### JSON-LD Templates for GEO

**SoftwareApplication (for SaaS):**
```json
{
  "@type": "SoftwareApplication",
  "name": "App Name",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
  "featureList": ["Feature 1", "Feature 2"],
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "150"}
}
```

**LocalBusiness (for physical locations):**
```json
{
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {"@type": "PostalAddress", "streetAddress": "...", "addressLocality": "..."},
  "geo": {"@type": "GeoCoordinates", "latitude": 0.0, "longitude": 0.0},
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday"], "opens": "09:00", "closes": "17:00"}],
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "50"}
}
```

### GEO Schema Scoring Criteria

| Criterion | Points |
|---|---|
| Organization/Person schema with sameAs (5+ platforms) | 30 |
| Article schema with full author details | 10 |
| Business-type-specific schema present | 10 |
| JSON-LD format (not Microdata/RDFa) | 5 |
| Server-rendered (not JS-injected) | 10 |
| speakable property on articles | 5 |
| knowsAbout on Organization/Person | 5 |

---

## the organization Schema Types

### Organization

Use on: homepage, about page.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Organization name]",
  "url": "https://[the organization's domain]",
  "logo": "https://[the organization's domain]/logo.png",
  "description": "the organization facilitates psychedelic healing retreats and educational programs for personal transformation.",
  "nonprofitStatus": "https://schema.org/Nonprofit501c3",
  "sameAs": [
    "https://www.instagram.com/[organization_handle]",
    "https://www.facebook.com/[organization_handle]",
    "https://www.youtube.com/@[organization_handle]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "info@[the organization's domain]",
    "contactType": "customer service"
  }
}
```

### Person (Founder -- GEO Entity Recognition)

Use on: about page, author bylines, speaker bios. Critical for GEO -- helps AI engines correctly attribute expertise.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Austin Mao",
  "jobTitle": "Founder",
  "affiliation": {
    "@type": "Organization",
    "name": "[Organization name]",
    "url": "https://[the organization's domain]"
  },
  "sameAs": [
    "https://www.linkedin.com/in/your-profile"
  ]
}
```

### Event -- Online (Webinars)

Use on: webinar landing pages, event registration pages.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "[Webinar Title]",
  "description": "[One-sentence description of the webinar topic]",
  "startDate": "2026-04-15T19:00:00-04:00",
  "endDate": "2026-04-15T20:30:00-04:00",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://[the organization's domain]/webinar/[slug]"
  },
  "image": "https://[the organization's domain]/images/[webinar-image].jpg",
  "organizer": {
    "@type": "Organization",
    "name": "[Organization name]",
    "url": "https://[the organization's domain]"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://[the organization's domain]/webinar/[slug]",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

### Event -- In-Person (Retreats)

Use on: retreat detail pages. Populate dates and location from live data (use airtable-retreats skill -- never hardcode dates).

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "[Retreat Name]",
  "description": "[Brief description of the retreat experience]",
  "startDate": "2026-05-10",
  "endDate": "2026-05-17",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "[Venue Name]",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "[City]",
      "addressRegion": "[State/Region]",
      "addressCountry": "[Country Code]"
    }
  },
  "image": "https://[the organization's domain]/images/[retreat-image].jpg",
  "organizer": {
    "@type": "Organization",
    "name": "[Organization name]",
    "url": "https://[the organization's domain]"
  },
  "performer": {
    "@type": "Person",
    "name": "Austin Mao"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://[the organization's domain]/retreats/[slug]",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

### Course

Use on: any paid educational program page (workshops, training programs, certification tracks).

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "[Program Name]",
  "description": "[One-sentence description of what participants learn]",
  "provider": {
    "@type": "Organization",
    "name": "[Organization name]",
    "url": "https://[the organization's domain]"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "Blended",
    "startDate": "2026-06-01",
    "endDate": "2026-08-01",
    "instructor": {
      "@type": "Person",
      "name": "Austin Mao"
    }
  }
}
```

### EducationalOrganization

Use on: homepage or about page as a secondary type when emphasizing the organization's educational mission.

```json
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "[Organization name]",
  "url": "https://[the organization's domain]",
  "description": "Educational organization offering psychedelic healing retreats and integration programs.",
  "sameAs": [
    "https://www.instagram.com/[organization_handle]"
  ]
}
```

### FAQPage

Use on: any page with a visible FAQ section. Critical for GEO -- AI engines heavily cite FAQ structured data when generating answers.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What happens during a the organization retreat?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Each retreat includes guided ceremonies, integration circles, one-on-one support, and group workshops over the course of several days in a safe, supported setting."
      }
    },
    {
      "@type": "Question",
      "name": "Who is a good candidate for a retreat?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Our retreats are designed for individuals seeking personal transformation and healing. All participants go through a screening process to ensure safety and readiness."
      }
    },
    {
      "@type": "Question",
      "name": "How do I prepare for my first retreat?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "After enrollment, you receive a preparation guide covering dietary guidelines, intention-setting practices, and what to expect during the experience."
      }
    }
  ]
}
```

### HowTo

Use on: preparation guides, integration guides, step-by-step instructional content. Important for GEO -- step-by-step markup is frequently cited by AI engines.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[Guide Title, e.g., How to Prepare for Your First Retreat]",
  "description": "[Brief summary of what this guide covers]",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Review the preparation guide",
      "text": "Read the full preparation document sent to your email after enrollment. It covers dietary recommendations, substances to avoid, and mental preparation practices.",
      "image": "https://[the organization's domain]/images/[step-image].jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Set your intention",
      "text": "Reflect on what you want to explore or heal. Write down your intention and revisit it in the days leading up to the retreat."
    },
    {
      "@type": "HowToStep",
      "name": "Prepare your body",
      "text": "Follow the dietary guidelines for at least two weeks before the retreat. Avoid alcohol, processed foods, and any contraindicated substances."
    }
  ]
}
```

### Article / BlogPosting

Use on: blog posts, educational articles, resource pages.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Article Title]",
  "image": "https://[the organization's domain]/images/[article-image].jpg",
  "datePublished": "2026-03-01T08:00:00-05:00",
  "dateModified": "2026-03-05T10:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Austin Mao",
    "url": "https://[the organization's domain]/about"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Organization name]",
    "logo": {
      "@type": "ImageObject",
      "url": "https://[the organization's domain]/logo.png"
    }
  },
  "description": "[One-sentence summary of the article]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://[the organization's domain]/blog/[slug]"
  }
}
```

Use `BlogPosting` instead of `Article` for blog-format posts. The schema is identical except `"@type": "BlogPosting"`.

### BreadcrumbList

Use on: every page except the homepage.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://[the organization's domain]"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Retreats",
      "item": "https://[the organization's domain]/retreats"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[Retreat Name]",
      "item": "https://[the organization's domain]/retreats/[slug]"
    }
  ]
}
```

### LocalBusiness

Use on: retreat detail pages where the retreat has a fixed, publicly known location.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Venue Name]",
  "image": "https://[the organization's domain]/images/[venue-image].jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street Address]",
    "addressLocality": "[City]",
    "addressRegion": "[State/Region]",
    "postalCode": "[Postal Code]",
    "addressCountry": "[Country Code]"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Latitude]",
    "longitude": "[Longitude]"
  }
}
```

### Review / AggregateRating

Use on: pages displaying participant testimonials. Reviews must be from real participants -- never fabricate reviews. Fetch testimonials from Senja (use senja skill) for accurate data.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Organization name]",
  "url": "https://[the organization's domain]",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[Average Rating]",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "[Total Review Count]"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "[Participant Name]"
      },
      "datePublished": "[YYYY-MM-DD]",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "[1-5]"
      },
      "reviewBody": "[Actual testimonial text from Senja]"
    }
  ]
}
```

### Multi-Type @graph Pattern

Use on: homepage and key landing pages to combine multiple schema types in a single JSON-LD block with cross-references via `@id`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://[the organization's domain]/#organization",
      "name": "[Organization name]",
      "url": "https://[the organization's domain]",
      "logo": "https://[the organization's domain]/logo.png",
      "nonprofitStatus": "https://schema.org/Nonprofit501c3",
      "sameAs": [
        "https://www.instagram.com/[organization_handle]",
        "https://www.facebook.com/[organization_handle]",
        "https://www.youtube.com/@[organization_handle]"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://[the organization's domain]/#website",
      "url": "https://[the organization's domain]",
      "name": "[Organization name]",
      "publisher": {
        "@id": "https://[the organization's domain]/#organization"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://[the organization's domain]"
        }
      ]
    }
  ]
}
```

---

## GEO (Generative Engine Optimization)

Structured data helps AI engines (ChatGPT, Perplexity, Google AI Overviews) correctly attribute content to the organization and cite it accurately. Key points:

- **FAQPage** and **HowTo** schemas are the most frequently cited by AI engines when generating answers. Prioritize these on content-heavy pages.
- **Person** schema for Austin Mao establishes entity recognition -- AI engines associate expertise with the correct person and organization.
- **Organization** with `nonprofitStatus` helps AI engines classify the organization correctly in health/wellness contexts.
- Every page with substantive content should have at least one schema type. Pages with only navigation or redirects do not need schema.

---

## Validation and Testing

### Before deploying any schema:

1. Copy the JSON-LD block.
2. Paste into **Google Rich Results Test**: https://search.google.com/test/rich-results
3. Confirm zero errors and zero warnings.
4. Paste into **Schema Markup Validator**: https://validator.schema.org/
5. Confirm all required properties are present.
6. Visually compare schema content against actual page content -- every claim in the schema must be visible on the page.

### After deploying:

- Check **Google Search Console > Enhancements** for indexing errors within 7 days.
- If errors appear, fix immediately and request re-validation.

---

## Next.js App Router Implementation

### In page.tsx or layout.tsx (App Router)

```tsx
// app/retreats/[slug]/page.tsx
import { Metadata } from "next";

export async function generateMetadata({ params }): Promise<Metadata> {
  // Fetch retreat data for meta tags
  return {
    title: "[Retreat Name] | the organization",
    description: "[Retreat description]",
  };
}

export default function RetreatPage({ params }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Event",
    name: "[Retreat Name]",
    // ... populate from props or fetched data
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />
      {/* Page content */}
    </>
  );
}
```

### Key rules for Next.js App Router:

- Place the `<script type="application/ld+json">` tag inside the component return, not in `<Head>` (App Router does not use `next/head`).
- Use `dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}` to serialize.
- For shared schemas (Organization, WebSite), place in `app/layout.tsx` so they appear on every page.
- For page-specific schemas (Event, Article, FAQPage), place in the individual `page.tsx`.
- Use `generateMetadata` for `<title>` and `<meta>` tags -- keep schema in the component body.
- Never duplicate schema types: if Organization is in layout.tsx, do not repeat it in page.tsx.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| Missing required property | Omitted a field Google requires (e.g., `startDate` on Event) | Check Google's docs for the specific type and add the missing field |
| Invalid date format | Date not in ISO 8601 (e.g., "March 5, 2026" instead of "2026-03-05") | Use `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS+TZ` format |
| Content mismatch | Schema says one thing, page shows another | Ensure every schema value matches visible page content exactly |
| Invalid URL | Relative URL or malformed href | Use fully qualified URLs starting with `https://` |
| Duplicate types | Same schema type appears in both layout.tsx and page.tsx | Place shared types in layout only; page-specific types in page only |
| Self-serving reviews | Marking up your own testimonials without real review data | Only use Review schema with verified participant testimonials from Senja |

---

## Steps

1. Identify the page type and determine which schema types apply from the list above.
2. Check if the page already has existing JSON-LD -- inspect source for `<script type="application/ld+json">`.
   - If existing schema is present: audit it for errors and missing properties before adding new types.
   - If no existing schema: proceed with implementation.
3. Select the appropriate template(s) from above and populate with real page data.
   - For retreat dates: fetch from airtable-retreats skill -- never hardcode.
   - For testimonials: fetch from senja skill -- never fabricate.
4. For pages needing multiple types, use the `@graph` pattern with `@id` cross-references.
5. Place schema in the correct file:
   - Shared (Organization, WebSite): `app/layout.tsx`
   - Page-specific (Event, Article, FAQPage, HowTo, Course): individual `page.tsx`
6. Validate with Google Rich Results Test -- zero errors required.
7. Validate with Schema Markup Validator -- all required properties present.
8. Deploy and monitor Search Console Enhancements within 7 days.

## Output

Provide:
1. The complete JSON-LD code block(s), ready to paste.
2. The exact file path where each block should be placed (e.g., `app/retreats/[slug]/page.tsx`).
3. The validation checklist result (pass/fail for Rich Results Test and Schema Validator).

## Error Handling

- If page content is insufficient to populate required schema properties: notify the user which properties are missing and what content needs to be added to the page before schema can be implemented.
- If a schema type is requested but not applicable to the page (e.g., LocalBusiness on a blog post): explain why it does not apply and suggest the correct type.
- If retreat dates or testimonial data is needed: instruct the user to run the airtable-retreats or senja skill first, then return to add schema with real data.
