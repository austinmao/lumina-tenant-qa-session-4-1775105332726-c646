---
name: stripe-checkout
description: "Add Stripe checkout session and webhook to a Next.js route"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /stripe-checkout
metadata:
  openclaw:
    emoji: "💳"
    requires:
      bins: ["stripe", "node"]
      env: ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"]
---

## Overview

Adds Stripe-powered checkout to a Next.js App Router project. Creates a checkout session API route, a Stripe webhook handler for `payment_intent.succeeded` and subscription events, and success/cancel redirect pages.

## Steps

### 1. Gather Requirements

Ask the user for:
- Product name and price (one-time or recurring/subscription)
- Currency (default: USD)
- Success redirect path (e.g., `/thank-you`)
- Cancel redirect path (e.g., `/`)
- Whether to collect billing address

### 2. Create Checkout Session Route

Write `app/api/checkout/session/route.ts`:

```ts
import Stripe from 'stripe'
import { NextRequest, NextResponse } from 'next/server'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: NextRequest) {
  const { priceId, quantity = 1, customerEmail } = await request.json()

  if (!priceId) {
    return NextResponse.json({ error: 'priceId is required' }, { status: 400 })
  }

  const session = await stripe.checkout.sessions.create({
    mode: 'payment', // or 'subscription' — update based on user's requirement
    line_items: [{ price: priceId, quantity }],
    customer_email: customerEmail,
    billing_address_collection: 'auto',
    success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/thank-you?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_SITE_URL}/`,
  })

  return NextResponse.json({ url: session.url })
}
```

### 3. Create Webhook Handler

Write `app/api/webhooks/stripe/route.ts`:

```ts
import Stripe from 'stripe'
import { NextRequest, NextResponse } from 'next/server'
import { headers } from 'next/headers'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: NextRequest) {
  const body = await request.text()
  const headersList = await headers()
  const sig = headersList.get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    return NextResponse.json({ error: 'Webhook signature verification failed' }, { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      // TODO: provision access, send receipt email, update CRM
      console.log('Payment succeeded for session:', session.id, 'customer:', session.customer_email)
      break
    }
    case 'customer.subscription.created':
    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription
      // TODO: update subscription status in database
      console.log('Subscription event:', event.type, subscription.id, subscription.status)
      break
    }
    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription
      // TODO: revoke access
      console.log('Subscription cancelled:', subscription.id)
      break
    }
    default:
      console.log('Unhandled event type:', event.type)
  }

  return NextResponse.json({ received: true })
}
```

Add a comment reminding the user to replace `TODO` sections with their business logic.

### 4. Create Success and Cancel Pages

Write `app/thank-you/page.tsx`:
```tsx
import { redirect } from 'next/navigation'
import Stripe from 'stripe'

export default async function ThankYouPage({ searchParams }: { searchParams: { session_id?: string } }) {
  if (!searchParams.session_id) redirect('/')
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
  const session = await stripe.checkout.sessions.retrieve(searchParams.session_id)
  return (
    <main>
      <h1>Thank you for your purchase!</h1>
      <p>A receipt has been sent to {session.customer_details?.email}.</p>
    </main>
  )
}
```

### 5. Update `.env.local`

Append the following (do not overwrite existing keys):
```
STRIPE_SECRET_KEY=sk_test_<your key>
STRIPE_WEBHOOK_SECRET=whsec_<your secret>
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### 6. List npm Dependencies and Webhook Testing

Print:
```
npm install stripe

# Test webhooks locally:
stripe listen --forward-to localhost:3000/api/webhooks/stripe
stripe trigger checkout.session.completed
```

## Output

- `app/api/checkout/session/route.ts` — checkout session creator
- `app/api/webhooks/stripe/route.ts` — webhook handler
- `app/thank-you/page.tsx` — success page
- `.env.local` additions

## Error Handling

- Missing `STRIPE_SECRET_KEY` → route throws at startup; remind user to set env var
- Webhook signature mismatch → return 400; log raw body length for debugging
- Stripe API error → catch and return 500 with sanitized error message (never expose raw Stripe error to client)
- Missing `session_id` on success page → redirect to home
