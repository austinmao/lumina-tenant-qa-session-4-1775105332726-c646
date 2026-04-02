---
name: chroma
description: "Query a Chroma vector database collection / search documents in Chroma / RAG lookup"
version: "1.0.0"
permissions:
  filesystem: none
  network: true
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - curl
        - jq
        - python3
---

# Chroma Vector Database Skill

## Overview

Chroma is the local vector database used by the organization agents for RAG (retrieval-augmented
generation). It runs as a persistent HTTP server on `localhost:8000` via launchd
(`org.example.chroma.app`). No authentication is required. Agents access it
directly via the Chroma v2 HTTP API — there is no MCP layer.

**Base URL:** `http://localhost:8000/api/v2`
**Tenant:** `default_tenant`
**Database:** `default_database`

---

## Available Collections (as of 2026-03-01)

| Collection | Dimension | Purpose |
|---|---|---|
| `psychedelic_safety` | 384 | Medical screening RAG — safety literature, drug interactions, contraindications |
| `programs` | 384 | Retreat program content |
| `marketing` | 384 | Marketing copy and campaign documents |
| `sales` | 384 | Sales collateral and deal context |
| `executive` | — | Executive documents |
| `finance` | — | Finance documents |
| `fundraising` | — | Fundraising documents |
| `legal_compliance` | — | Legal and compliance documents |
| `operations` | — | Operations documents |
| `people_hr` | — | HR documents |
| `public_relations` | — | PR documents |
| `research_education` | — | Research and education documents |
| `technology` | — | Technology documents |
| `austin_teachings` | 384 | Austin Mao corpus — talks, podcasts, retreat education, and other staged transcript material |
| `retreat-photos` | 3072 | Semantic photo retrieval — LLM-captioned photos with text-embedding-3-large |

---

## Operations Gate

**Safe to execute without the operator's approval:**
- Heartbeat check (read-only)
- List collections (read-only)
- Query any collection (read-only semantic search)
- Get document count for any collection (read-only)

**Requires the operator's explicit approval before executing:**
- Adding documents to any collection
- Deleting documents from any collection
- Deleting a collection
- Creating a new collection

---

## Quick Start — Verify Chroma is Running

```bash
curl -s http://localhost:8000/api/v2/heartbeat
# Expected: {"nanosecond heartbeat": <timestamp>}
```

---

## API Reference

All endpoints use the base path:
`http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database`

### List Collections

```bash
curl -s \
  "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections" \
  | jq '[.[] | {name: .name, id: .id}]'
```

### Get Collection Document Count

Replace `<collection-name>` with e.g. `psychedelic_safety`:

```bash
# Step 1: get collection ID
COLLECTION_ID=$(curl -s \
  "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections" \
  | jq -r '.[] | select(.name == "<collection-name>") | .id')

# Step 2: get count
curl -s \
  "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections/${COLLECTION_ID}/count"
```

### Query a Collection (Semantic Search)

The query endpoint performs a semantic vector search. OpenClaw agents call this when
doing RAG lookups (e.g. medical-screening querying `psychedelic_safety`).

Use the Python chromadb client from within a skill script:

```python
import chromadb

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "psychedelic_safety"

client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = client.get_collection(COLLECTION_NAME)

results = collection.query(
    query_texts=["SSRI serotonin syndrome washout timeline psilocybin"],
    n_results=3
)

# results["documents"][0] — list of matching text chunks
# results["metadatas"][0] — list of metadata dicts (source, page, filename, chunk)
# results["distances"][0] — similarity scores (lower = more similar for L2 space)

for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"Result {i+1}: {meta.get('source','?')} p.{meta.get('page','?')}")
    print(f"  {doc[:200]}")
```

Install chromadb if not present:
```bash
pip3 install chromadb
# or
uvx --from chromadb python -c "import chromadb; print('ok')"
```

### Query via Raw HTTP (no Python client)

```bash
# Step 1: get collection ID
COLLECTION_ID=$(curl -s \
  "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections" \
  | jq -r '.[] | select(.name == "psychedelic_safety") | .id')

# Step 2: query (embedding must be pre-computed; use Python client for text queries)
curl -s -X POST \
  "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections/${COLLECTION_ID}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embeddings": null,
    "query_texts": ["SSRI washout psilocybin"],
    "n_results": 3,
    "include": ["documents", "metadatas", "distances"]
  }' | jq '.'
```

---

## Error Handling

- **Chroma unavailable** (`Connection refused` or no heartbeat response): Note "RAG query
  failed — Chroma not reachable at localhost:8000" and continue without RAG context.
  Notify the operator via the relevant Slack channel.
- **Collection not found**: Note "Collection `<name>` not found in Chroma". Report to
  the operator — collection may need to be re-ingested.
- **Zero results returned**: Note "RAG query returned 0 results for query: `<text>`".
  Continue; flag low coverage in any brief or report.
- **chromadb module not found**: Install with `pip3 install chromadb` or use the raw
  HTTP endpoint above as a fallback.

---

## Infrastructure

Chroma runs as a launchd service:
- **Plist**: `~/Library/LaunchAgents/org.example.chroma.app.plist`
- **Data dir**: `~/.lumina-rag/chroma_data`
- **Logs**: `~/.lumina-rag/logs/chroma.log` and `chroma_err.log`
- **Start/restart**: `launchctl kickstart -k gui/$(id -u)/org.example.chroma.app`
- **Stop**: `launchctl bootout gui/$(id -u)/org.example.chroma.app`

Verify health:
```bash
/Users/luminamao/Documents/Github/openclaw/scripts/verify-chroma-mcp.sh
```
