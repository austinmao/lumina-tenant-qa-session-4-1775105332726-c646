---
name: domain-management
description: "Configure DNS records, SSL certificates, and domain provisioning for tenants"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /domain-management
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Domain Management

Configure DNS records, SSL certificates, and domain provisioning for Lumina OS tenant websites. This skill covers the full domain lifecycle from acquisition through production DNS setup, including subdomain management and multi-site configurations.

## When to Use

- Provisioning a new domain for a tenant website
- Configuring DNS records (A, AAAA, CNAME, MX, TXT)
- Setting up SSL certificates for custom domains
- Managing subdomains (www, cdn, api, staging)
- Configuring email sending domains (SPF, DKIM, DMARC)
- Migrating a domain between hosting providers
- Troubleshooting DNS propagation or SSL issues

## Context Loading

Before any domain work:
1. Read `tenants/<tenant>/config.yaml` for the tenant's domain configuration
2. Read `tenants/<tenant>/dns.yaml` if it exists (records the intended DNS state)
3. Identify the DNS provider (Cloudflare, Vercel, Route 53, etc.)
4. Identify the hosting provider (Vercel, custom server, etc.)

## Domain Provisioning Workflow

### Step 1: Domain Acquisition

If the tenant does not yet own the domain:
1. Verify domain availability via the registrar
2. Purchase through the tenant's preferred registrar (Cloudflare Registrar, Namecheap, Google Domains)
3. Enable registrar lock and WHOIS privacy
4. Set nameservers to the DNS provider (Cloudflare recommended for Lumina OS tenants)

Document the registrar, registration date, and renewal date in `tenants/<tenant>/config.yaml`.

### Step 2: DNS Provider Setup

If using Cloudflare (recommended):
1. Add the domain to the Cloudflare account
2. Update nameservers at the registrar to point to Cloudflare
3. Wait for nameserver propagation (typically 1-24 hours)
4. Verify the domain is active in Cloudflare

### Step 3: DNS Record Configuration

Configure records based on the hosting setup:

**For Vercel-hosted sites:**
```
Type    Name    Value                   TTL     Proxy
A       @       76.76.21.21             Auto    No (Vercel manages SSL)
CNAME   www     cname.vercel-dns.com    Auto    No
```

**For CDN subdomains (R2):**
```
Type    Name    Value                           TTL     Proxy
CNAME   cdn     <bucket>.r2.cloudflarestorage.com Auto  Yes (orange cloud)
```

**For API subdomains:**
```
Type    Name    Value                   TTL     Proxy
CNAME   api     cname.vercel-dns.com    Auto    No
```

### Step 4: SSL Certificate

SSL setup depends on the hosting provider:
- **Vercel**: automatic SSL via Let's Encrypt. Add the domain in Vercel dashboard and verify DNS.
- **Cloudflare proxied**: automatic SSL. Enable "Full (Strict)" mode if the origin also has SSL.
- **Custom server**: use Let's Encrypt with certbot or Caddy (automatic HTTPS).

Verify SSL is working: `curl -I https://<domain>` should return 200 with valid certificate.

## Email Domain Configuration

### SPF Record

Specify which mail servers can send on behalf of the domain:

```
Type    Name    Value                                       TTL
TXT     @       v=spf1 include:_spf.google.com              Auto
                include:amazonses.com ~all
```

Add `include:` entries for each sending service:
- Resend: `include:amazonses.com` (Resend uses SES)
- Google Workspace: `include:_spf.google.com`
- Mailchimp: `include:servers.mcsv.net`

Only one SPF record per domain. Combine all includes into a single TXT record.

### DKIM Record

Each email sending service provides its own DKIM public key:
```
Type    Name                            Value                   TTL
CNAME   resend._domainkey               <value from Resend>     Auto
CNAME   s1._domainkey                   <value from provider>   Auto
```

Follow the exact instructions from each provider. DKIM record names and types vary.

### DMARC Record

```
Type    Name        Value                                   TTL
TXT     _dmarc      v=DMARC1; p=quarantine;                 Auto
                    rua=mailto:dmarc@<domain>;
                    ruf=mailto:dmarc@<domain>;
                    pct=100
```

Start with `p=none` for monitoring, upgrade to `p=quarantine` after verifying all legitimate senders pass SPF and DKIM.

## Multi-Site Domain Strategy

Lumina OS supports multiple sites per tenant. Domain configuration patterns:

### Separate Domains
Each site gets its own domain:
- `[the organization's domain]` (primary site)
- `example.com` (product site)
- `example.com` (founder site)

Each domain is configured independently with its own DNS records.

### Subdomain Model
All sites under one domain:
- `www.example.com` (primary)
- `blog.example.com` (content)
- `app.example.com` (application)

Subdomains can point to different hosting targets (Vercel projects, separate servers).

## Staging and Preview Domains

### Staging
- Use a subdomain: `staging.<domain>` or a separate domain: `staging-<domain>.vercel.app`
- Configure DNS identically to production (same record types, different targets)
- Staging should not be indexed: add `X-Robots-Tag: noindex` header

### Vercel Preview Deployments
- Automatic preview URLs: `<branch>.<project>.vercel.app`
- No DNS configuration needed for preview deployments
- Optionally configure a wildcard subdomain for custom preview URLs

## DNS Propagation

After any DNS change:
1. Verify the change via `dig <domain> <record-type>` or online tools
2. Propagation typically takes 1-60 minutes for Cloudflare, up to 48 hours for other providers
3. TTL affects how quickly changes propagate -- lower TTL before planned changes, raise after
4. Clear local DNS cache if testing locally: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`

## Common Issues

### SSL Certificate Not Issuing
- Verify DNS records point to the correct target (Vercel, Cloudflare)
- Check for CAA records that restrict certificate authorities
- If using Cloudflare proxy (orange cloud): ensure SSL mode is "Full (Strict)"
- Wait 15 minutes after DNS changes before troubleshooting SSL

### Email Deliverability Issues
- Run SPF check: `dig TXT <domain>` -- verify the SPF record includes all senders
- Run DKIM check: `dig CNAME <selector>._domainkey.<domain>` -- verify DKIM records exist
- Check DMARC alignment: both SPF and DKIM must pass with the From domain
- Use mail-tester.com to score deliverability

### www vs Apex Domain
- Always configure both `www` and apex (`@`)
- Choose one as canonical and redirect the other (301)
- For Vercel: add both in the Vercel dashboard, set the redirect

## DNS Record Documentation

Document all DNS records in `tenants/<tenant>/dns.yaml`:
```yaml
domain: example.com
registrar: cloudflare
nameservers: [ns1.cloudflare.com, ns2.cloudflare.com]
records:
  - type: A
    name: "@"
    value: "76.76.21.21"
    ttl: auto
    purpose: "Vercel hosting"
  - type: CNAME
    name: www
    value: cname.vercel-dns.com
    ttl: auto
    purpose: "Vercel hosting (www redirect)"
  - type: TXT
    name: "@"
    value: "v=spf1 include:amazonses.com ~all"
    ttl: auto
    purpose: "SPF for Resend email sending"
```

## Error Handling

- Domain not resolving: check nameserver configuration at the registrar, verify DNS provider shows the domain as active
- SSL error: verify DNS points to the correct target, check for mixed content (HTTP resources on HTTPS pages)
- Email bouncing: verify SPF, DKIM, and DMARC records, check the sending service dashboard for errors
- DNS change not propagating: check TTL on the old record, try flushing local DNS cache, wait for TTL expiry

## Boundaries

- Never transfer domain ownership without explicit operator approval
- Never disable DNSSEC without documenting the reason
- Never set SPF to `+all` (allows any server to send as the domain)
- Never delete MX records without verifying email will not be disrupted
- Never expose internal infrastructure IPs in public DNS records

## Dependencies

- `cdn-r2` -- CDN subdomain configuration
- `env-management` -- API keys for DNS provider APIs
- `deployment` -- hosting target configuration

## State Tracking

- `domains` -- keyed by domain: registrar, nameservers, SSL status, expiry date
- `dnsRecords` -- keyed by record name + type: value, TTL, purpose, last verified
- `emailDomains` -- keyed by domain: SPF status, DKIM status, DMARC status, last tested
