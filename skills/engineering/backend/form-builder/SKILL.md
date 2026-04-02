---
name: form-builder
description: "Build multi-step forms with validation wired to Attio CRM and Resend email"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /form-builder
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["node"]
      env: ["ATTIO_API_KEY", "RESEND_API_KEY"]
---

## Overview

Creates a fully wired multi-step form: Zod validation schema, React form component with progress indicator, API route handler, Attio CRM contact creation/update, and Resend confirmation email. Includes a honeypot field for bot protection.

## Steps

### 1. Gather Requirements

Ask the user for:
- Form name and purpose (e.g., "retreat application", "newsletter signup")
- Steps and their fields (e.g., Step 1: name + email, Step 2: goals + questions)
- Redirect URL after successful submission
- Confirmation email subject and body template
- Attio list or attribute to tag submitted contacts with

### 2. Generate Zod Validation Schema

Write `lib/forms/<form-name>/schema.ts`:

```ts
import { z } from 'zod'

export const step1Schema = z.object({
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Valid email required'),
  honeypot: z.string().max(0), // must be empty — bot protection
})

export const step2Schema = z.object({
  goals: z.string().min(10, 'Please describe your goals (10+ chars)'),
  questions: z.string().optional(),
})

export const fullFormSchema = step1Schema.merge(step2Schema)
export type FormData = z.infer<typeof fullFormSchema>
```

Adjust field names and validation rules to match the user's requirements.

### 3. Generate API Route

Write `app/api/forms/<form-name>/route.ts`:

```ts
import { NextRequest, NextResponse } from 'next/server'
import { fullFormSchema } from '@/lib/forms/<form-name>/schema'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  const body = await request.json()
  const parsed = fullFormSchema.safeParse(body)

  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const data = parsed.data

  // Honeypot check
  if (data.honeypot) {
    return NextResponse.json({ ok: true }) // silent discard
  }

  // Attio CRM upsert
  await fetch('https://api.attio.com/v2/objects/people/records', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.ATTIO_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      data: {
        values: {
          email_addresses: [{ email_address: data.email }],
          name: [{ first_name: data.firstName, last_name: data.lastName }],
        },
      },
    }),
  })

  // Resend confirmation
  await resend.emails.send({
    from: process.env.FROM_EMAIL ?? 'hello@example.com',
    to: data.email,
    subject: 'We received your application',
    text: `Hi ${data.firstName}, thank you for applying. We'll be in touch soon.`,
  })

  return NextResponse.json({ ok: true })
}
```

### 4. Generate React Form Component

Write `components/forms/<FormName>.tsx` with:
- `useState` for current step index and form data accumulation
- Progress bar: `<div style={{ width: `${(step / totalSteps) * 100}%` }} />`
- Each step rendered conditionally; Back/Next/Submit buttons
- Client-side Zod validation on Next click (`step1Schema.safeParse(...)`)
- Hidden honeypot input: `<input name="honeypot" style={{ display: 'none' }} tabIndex={-1} />`
- `fetch('/api/forms/<form-name>', { method: 'POST', body: JSON.stringify(formData) })` on final submit
- Loading state and error message display on API failure

### 5. List npm Dependencies

Print the install command: `npm install zod resend`

## Output

- `lib/forms/<form-name>/schema.ts` — Zod schemas
- `app/api/forms/<form-name>/route.ts` — API route with Attio + Resend integration
- `components/forms/<FormName>.tsx` — multi-step React form component

## Error Handling

- Missing `ATTIO_API_KEY` or `RESEND_API_KEY` → route returns 500 with descriptive message; add explicit check at top of route
- Attio API failure → log error, continue with Resend send; return 200 to user (do not expose CRM errors)
- Resend failure → log error; return 200 (form submission still recorded)
- Validation failure → return 400 with field-level errors for client-side display
