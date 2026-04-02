---
name: cdn-r2
description: "Configure AWS R2 buckets, image optimization, and CDN delivery"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /cdn-r2
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins: ["curl"]
      env: ["R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_ACCOUNT_ID"]
      os: ["darwin"]
---

# CDN & R2

Configure Cloudflare R2 object storage for image and asset hosting, implement image optimization pipelines, and manage CDN delivery for Lumina OS tenant websites. R2 provides S3-compatible storage with zero egress fees.

## When to Use

- Setting up a new R2 bucket for a tenant's media assets
- Configuring image optimization (resizing, format conversion, compression)
- Setting up CDN custom domains for asset delivery
- Implementing upload flows (direct upload, presigned URLs, server-side upload)
- Managing bucket policies, CORS, and lifecycle rules
- Troubleshooting slow asset loading or broken images

## Context Loading

Before any CDN/R2 work:
1. Read `tenants/<tenant>/config.yaml` for the tenant's R2 bucket name and custom domain
2. Verify R2 credentials are set: `$R2_ACCESS_KEY_ID`, `$R2_SECRET_ACCESS_KEY`, `$R2_ACCOUNT_ID`
3. Read existing asset handling code in `web/src/lib/storage/` or `web/src/lib/images/`
4. If credentials are missing, stop and prompt: "Set R2 credentials before proceeding."

## R2 Bucket Setup

### Bucket Naming Convention

Each tenant gets its own bucket: `lumina-<tenant-slug>-assets`
- Example: `lumina-tenant-a-assets`, `lumina-tenant-b-assets`
- Bucket names must be globally unique, lowercase, and 3-63 characters

### Bucket Configuration

Via the Cloudflare dashboard or API:
1. Create the bucket in the appropriate region (auto or specific)
2. Enable public access via custom domain (not the default R2 URL)
3. Configure CORS for the web application domain
4. Set lifecycle rules for temporary uploads (delete after 24 hours)

### CORS Configuration

```json
[
  {
    "AllowedOrigins": ["https://<tenant-domain>", "https://<tenant-domain>.vercel.app"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["Content-Type", "Content-Disposition"],
    "MaxAgeSeconds": 86400
  }
]
```

## Upload Patterns

### Presigned URL Upload (Preferred for Large Files)

1. Client requests an upload URL from `/api/upload/presign`
2. Backend generates a presigned PUT URL with a 15-minute expiry
3. Client uploads directly to R2 using the presigned URL
4. Client notifies the backend that the upload is complete
5. Backend verifies the object exists and records the asset in the database

```typescript
// Backend: generate presigned URL
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

const client = new S3Client({
  region: 'auto',
  endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: R2_ACCESS_KEY_ID,
    secretAccessKey: R2_SECRET_ACCESS_KEY,
  },
})

const key = `uploads/${tenantId}/${Date.now()}-${sanitizedFilename}`
const command = new PutObjectCommand({
  Bucket: bucketName,
  Key: key,
  ContentType: contentType,
})

const uploadUrl = await getSignedUrl(client, command, { expiresIn: 900 })
```

### Server-Side Upload (Small Files)

For small files (under 5 MB) like avatars and logos:
1. Client uploads to `/api/upload` as multipart form data
2. Backend validates file type and size
3. Backend uploads to R2 using the S3 SDK
4. Backend returns the public URL

### File Validation

Before any upload:
- **File type**: allow only expected types (image/jpeg, image/png, image/webp, image/svg+xml, application/pdf)
- **File size**: enforce limits per type (images: 10 MB, documents: 25 MB)
- **Filename**: sanitize (remove special characters, limit length, lowercase)
- **Content-Type**: validate that the Content-Type header matches the actual file content

Reject disallowed file types at the API route level, not just in the frontend.

## Image Optimization

### On-Upload Processing

After an image is uploaded to R2:
1. Generate optimized variants using Cloudflare Image Transformations or a processing pipeline:
   - Thumbnail: 150x150, WebP, quality 75
   - Medium: 800px wide, WebP, quality 80
   - Large: 1600px wide, WebP, quality 85
   - Original: preserved as-is
2. Store variants with predictable key patterns: `images/<id>/thumb.webp`, `images/<id>/medium.webp`
3. Record all variant URLs in the database asset record

### On-Demand Transformation (Cloudflare Images)

If Cloudflare Image Transformations are enabled:
```
https://cdn.<domain>/cdn-cgi/image/width=800,quality=80,format=webp/<original-path>
```

This avoids storing variants -- transformations happen at the CDN edge on request and are cached.

### Image Format Strategy

| Format | Use Case |
|---|---|
| WebP | Default for all raster images (93%+ browser support) |
| AVIF | Progressive enhancement where supported (smaller than WebP) |
| JPEG | Fallback for legacy clients |
| SVG | Logos, icons, illustrations (never rasterize SVGs) |
| PNG | Screenshots, images requiring transparency (prefer WebP with alpha when possible) |

Serve WebP by default with JPEG fallback via the `<picture>` element or `Accept` header negotiation.

## CDN Custom Domain

### Setup

1. Add a custom domain in the Cloudflare R2 bucket settings: `cdn.<tenant-domain>`
2. Create a CNAME DNS record pointing `cdn.<tenant-domain>` to the R2 bucket's public URL
3. Cloudflare provides SSL automatically
4. Configure cache rules: static assets cached for 1 year with content-hash filenames

### Cache Strategy

| Asset Type | Cache-Control | Rationale |
|---|---|---|
| Images with content hash | `public, max-age=31536000, immutable` | Content-addressed: URL changes when content changes |
| Images without hash | `public, max-age=86400, stale-while-revalidate=3600` | Daily revalidation |
| User uploads | `public, max-age=3600` | May be replaced; short cache |
| Private assets | `private, no-cache` | Auth-gated; never cached at CDN |

### Cache Invalidation

- Content-hashed URLs: no invalidation needed (new hash = new URL)
- Non-hashed URLs: use Cloudflare API to purge specific URLs
- Bulk purge: only as last resort (impacts cache hit rate)

## Directory Structure in R2

```
<bucket>/
  images/
    <tenant>/
      <asset-id>/
        original.<ext>
        thumb.webp
        medium.webp
        large.webp
  documents/
    <tenant>/
      <asset-id>.<ext>
  uploads/
    <tenant>/
      <temp-id>.<ext>    # Lifecycle: deleted after 24h
```

## Error Handling

- Upload fails (network): retry up to 3 times with exponential backoff. Show "Upload failed. Retrying..." to the user.
- File too large: reject before upload with a clear message ("File exceeds 10 MB limit")
- Invalid file type: reject with allowed types listed ("Allowed: JPEG, PNG, WebP, SVG")
- R2 credentials invalid: log the error, show "Storage service unavailable" to the user, alert the operator
- Bucket not found: verify bucket name in tenant config, check R2 dashboard
- CORS error: verify the origin is in the bucket's CORS allowlist

## Boundaries

- Never serve private or authenticated content through the public CDN
- Never delete bucket contents without operator approval
- Never disable CORS restrictions -- configure them correctly for each tenant
- Never store credentials or API keys in R2 buckets
- Never serve user-uploaded files without type validation (SVGs can contain scripts)

## Dependencies

- `domain-management` -- custom domain DNS configuration for CDN
- `env-management` -- R2 credential management
- `frontend` -- image components that consume CDN URLs

## State Tracking

- `buckets` -- keyed by tenant: bucket name, custom domain, region, total size
- `assets` -- keyed by asset ID: bucket key, variants, size, content type, upload date
- `cdnDomains` -- keyed by domain: bucket, SSL status, cache configuration
