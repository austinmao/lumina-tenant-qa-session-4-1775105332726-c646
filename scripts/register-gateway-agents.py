#!/usr/bin/env python3
"""Register catalog agents with the OpenClaw gateway.

Reads catalog/agents/**/*.yaml and registers each agent with the gateway
via `openclaw agents add`. Purely OSS — no Paperclip dependency.

Idempotent: skips agents that are already registered.

The agent ID used for gateway registration is derived from the catalog
spec's `id` field (e.g., "executive/cmo" → gateway agent id "cmo").
The workspace path points to the agent's directory in the repo.

Usage:
    python3 scripts/register-gateway-agents.py [--dry-run] [--filter <pattern>]

Gateway agent ID convention:
    catalog id "executive/cmo"  → gateway id "cmo",  workspace "agents/executive/cmo"
    catalog id "campaigns/campaign-orchestrator" → gateway id "conductor", workspace "agents/campaigns/campaign-orchestrator"

The gateway ID is the agent's short name (last segment of catalog id),
unless a display_name override exists in the catalog spec.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog" / "agents"
AGENTS_DIR = REPO_ROOT / "agents"

# Map catalog IDs to short gateway IDs where the default (last segment) is ambiguous
GATEWAY_ID_OVERRIDES = {
    "campaigns/campaign-orchestrator": "conductor",
    "operations/coordinator": "ops-coordinator",
    "operations/knowledge-sync": "meridian",
    "operations/transcript-curator": "curator",
    "website/orchestrator": "construct",
    "website/visual-designer": "canvas",
    "website/frontend-engineer": "nova",
    "marketing/brand-guardian": "brand-guardian",
    "marketing/brand-designer": "brand-designer",
    "content/copywriter": "quill",
    "engineering/email-engineer": "forge",
    "engineering/frontend-engineer": "nova-eng",
    "engineering/backend-engineer": "backend-eng",
    "engineering/devops-engineer": "devops-eng",
    "creative/creative-director": "creative-director",
    "strategy/seo-geo-strategist": "seo-strategist",
    "strategy/analytics-engineer": "analytics-eng",
    "quality/qa-engineer": "qa-engineer",
    "sales/director": "sales-director",
    "sales/lumina": "lumina",
    "sales/enrollment": "enrollment",
    "sales/lead-nurture": "lead-nurture",
    "sales/coach": "sales-coach",
    "sales/concierge": "concierge",
    "sales/pricing-analyst": "pricing-analyst",
}


def catalog_id_to_gateway_id(catalog_id: str) -> str:
    """Convert catalog ID to gateway agent ID."""
    if catalog_id in GATEWAY_ID_OVERRIDES:
        return GATEWAY_ID_OVERRIDES[catalog_id]
    # Default: use last segment
    return catalog_id.rsplit("/", 1)[-1]


def catalog_id_to_workspace(catalog_id: str) -> Path:
    """Convert catalog ID to workspace path."""
    return AGENTS_DIR / catalog_id


def catalog_id_to_agent_dir(catalog_id: str) -> Path:
    """Convert catalog ID to agent dir (where SOUL.md lives)."""
    return AGENTS_DIR / catalog_id


def list_registered_agents() -> set[str]:
    """Get currently registered gateway agent IDs."""
    try:
        result = subprocess.run(
            ["openclaw", "agents", "list", "--json"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return {a.get("id", "") for a in data}
            if isinstance(data, dict) and "agents" in data:
                return {a.get("id", "") for a in data["agents"]}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    # Fallback: parse text output
    try:
        result = subprocess.run(
            ["openclaw", "agents", "list"],
            capture_output=True, text=True, timeout=15,
        )
        ids = set()
        for line in result.stdout.splitlines():
            # Lines like "- main (default)" or "- cmo"
            match = re.match(r"^-\s+(\S+)", line.strip())
            if match:
                ids.add(match.group(1))
        return ids
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return set()


def discover_catalog_agents() -> list[dict]:
    """Read all catalog agent specs."""
    agents = []
    for yaml_path in sorted(CATALOG_DIR.rglob("*.yaml")):
        try:
            with open(yaml_path) as f:
                spec = yaml.safe_load(f)
            if not spec or spec.get("kind") != "agent":
                continue
            catalog_id = spec.get("id", "")
            if not catalog_id:
                continue
            workspace = catalog_id_to_workspace(catalog_id)
            if not workspace.is_dir():
                continue  # Skip agents without a workspace directory
            agents.append({
                "catalog_id": catalog_id,
                "gateway_id": catalog_id_to_gateway_id(catalog_id),
                "title": spec.get("title", catalog_id),
                "workspace": str(workspace),
                "agent_dir": str(catalog_id_to_agent_dir(catalog_id)),
                "spec_path": str(yaml_path.relative_to(REPO_ROOT)),
            })
        except (yaml.YAMLError, OSError) as e:
            print(f"  WARN: Failed to read {yaml_path}: {e}", file=sys.stderr)
    return agents


def register_agent(agent: dict, dry_run: bool = False) -> bool:
    """Register a single agent with the gateway."""
    gw_id = agent["gateway_id"]
    workspace = agent["workspace"]
    agent_dir = agent["agent_dir"]

    cmd = [
        "openclaw", "agents", "add", gw_id,
        "--workspace", workspace,
    ]

    if dry_run:
        print(f"  DRY-RUN: {' '.join(cmd)}")
        return True

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return True
        # Check if already exists
        if "already exists" in result.stderr.lower() or "already exists" in result.stdout.lower():
            return True
        print(f"  ERROR: {result.stderr.strip() or result.stdout.strip()}", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print(f"  ERROR: Timeout registering {gw_id}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Register catalog agents with OpenClaw gateway")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    parser.add_argument("--filter", type=str, default="", help="Only register agents matching pattern")
    parser.add_argument("--list", action="store_true", help="List what would be registered")
    args = parser.parse_args()

    print("=== OpenClaw Gateway Agent Registration ===\n")

    # Discover catalog agents
    agents = discover_catalog_agents()
    if args.filter:
        agents = [a for a in agents if args.filter in a["catalog_id"] or args.filter in a["gateway_id"]]

    if not agents:
        print("No catalog agents found with workspaces.")
        return 0

    if args.list:
        print(f"Found {len(agents)} agents with workspaces:\n")
        for a in agents:
            print(f"  {a['gateway_id']:25s} ← {a['catalog_id']:40s} workspace={a['workspace']}")
        return 0

    # Get currently registered agents
    registered = list_registered_agents()
    print(f"Currently registered: {registered or '{none}'}")
    print(f"Catalog agents with workspaces: {len(agents)}\n")

    registered_count = 0
    skipped_count = 0
    failed_count = 0

    for agent in agents:
        gw_id = agent["gateway_id"]
        if gw_id in registered:
            print(f"  SKIP: {gw_id:25s} (already registered)")
            skipped_count += 1
            continue

        ok = register_agent(agent, dry_run=args.dry_run)
        if ok:
            print(f"  OK:   {gw_id:25s} ← {agent['catalog_id']}")
            registered_count += 1
        else:
            print(f"  FAIL: {gw_id:25s} ← {agent['catalog_id']}")
            failed_count += 1

    print(f"\n=== Summary ===")
    print(f"Registered: {registered_count}")
    print(f"Skipped:    {skipped_count}")
    print(f"Failed:     {failed_count}")
    print(f"Total:      {len(agents)}")

    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
