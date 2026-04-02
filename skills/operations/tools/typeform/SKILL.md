---
name: typeform
description: |
  Typeform API integration. List forms, retrieve responses, create/update/delete forms, and access insights. Connects directly to api.typeform.com using a Personal Access Token — no third-party proxy.
---

# Typeform

Interact with Typeform directly via the v1 REST API using a Personal Access Token.

## Required environment variable

| Variable | Description |
|---|---|
| `TYPEFORM_API_KEY` | Typeform Personal Access Token (`tfp_...`) |

## Base URL

```
https://api.typeform.com
```

## Authentication

All requests use a Bearer token:

```
Authorization: Bearer $TYPEFORM_API_KEY
```

## Quick Start

```javascript
// Who am I?
const r = await fetch('https://api.typeform.com/me', {
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});
console.log(await r.json());
```

## API Reference

### User

```javascript
GET /me
```

### Forms

#### List forms
```javascript
const r = await fetch('https://api.typeform.com/forms?page_size=25', {
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});
```

#### Get a form
```javascript
const r = await fetch(`https://api.typeform.com/forms/${formId}`, {
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});
```

#### Create a form
```javascript
const r = await fetch('https://api.typeform.com/forms', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Customer Survey',
    fields: [
      { type: 'short_text', title: 'What is your name?' },
      { type: 'email', title: 'What is your email?' }
    ]
  })
});
```

#### Update a form
```javascript
const r = await fetch(`https://api.typeform.com/forms/${formId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ title: 'Updated Title', fields: [...] })
});
```

#### Delete a form
```javascript
// Returns 204 on success
const r = await fetch(`https://api.typeform.com/forms/${formId}`, {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});
```

### Responses

#### List responses
```javascript
const r = await fetch(
  `https://api.typeform.com/forms/${formId}/responses?page_size=25`,
  { headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` } }
);
```

With filters:
```javascript
const params = new URLSearchParams({
  page_size: '25',
  since: '2024-01-01T00:00:00Z',
  until: '2024-12-31T23:59:59Z',
  completed: 'true'
});
const r = await fetch(
  `https://api.typeform.com/forms/${formId}/responses?${params}`,
  { headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` } }
);
```

### Insights

```javascript
const r = await fetch(
  `https://api.typeform.com/insights/${formId}/summary`,
  { headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` } }
);
```

### Workspaces

```javascript
// List
const r = await fetch('https://api.typeform.com/workspaces', {
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});

// Get one
const r = await fetch(`https://api.typeform.com/workspaces/${workspaceId}`, {
  headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` }
});
```

## Field Types

| Type | Description |
|---|---|
| `short_text` | Single line text |
| `long_text` | Multi-line text |
| `email` | Email address |
| `number` | Numeric input |
| `rating` | Star rating |
| `opinion_scale` | 0–10 scale |
| `multiple_choice` | Single or multiple selection |
| `yes_no` | Boolean |
| `date` | Date picker |
| `dropdown` | Dropdown selection |

## Pagination

Responses use cursor-based pagination via the `before` token:

```javascript
// Get next page using the token from the last item
const r = await fetch(
  `https://api.typeform.com/forms/${formId}/responses?before=${token}`,
  { headers: { 'Authorization': `Bearer ${process.env.TYPEFORM_API_KEY}` } }
);
```

## Error Handling

| Status | Meaning |
|---|---|
| 401 | Invalid or missing TYPEFORM_API_KEY |
| 404 | Form or resource not found |
| 429 | Rate limited — Typeform allows 10 req/sec |
| 204 | Success with no body (DELETE operations) |

## Resources

- [Typeform API Overview](https://www.typeform.com/developers/get-started)
- [Forms API](https://www.typeform.com/developers/create/reference/retrieve-forms)
- [Responses API](https://www.typeform.com/developers/responses/reference/retrieve-responses)
- [Workspaces API](https://www.typeform.com/developers/create/reference/retrieve-workspaces)
