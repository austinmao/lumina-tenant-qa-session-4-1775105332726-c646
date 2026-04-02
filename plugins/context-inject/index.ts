/**
 * context-inject — OpenClaw ContextEngine plugin (Phase 2, feature 002)
 *
 * Hooks into Gateway v2026.3.7 ContextEngine lifecycle:
 *   - prepareSubagentSpawn: injects SOUL.md + IDENTITY.md identity context
 *     and handoff-contract binding constraints into the sub-agent task.
 *   - onSubagentEnded: runs contract assertion verification via the Python
 *     contract_assertions module when a handoff contract was referenced.
 */

import { readFile } from "node:fs/promises";
import { execFileSync } from "node:child_process";

// ---------------------------------------------------------------------------
// Types — mirrors Gateway plugin hook signatures
// ---------------------------------------------------------------------------

interface SpawnContext {
  agentId: string;
  task: string;
  workspaceDir?: string;
}

interface SpawnResult {
  task: string;
}

interface EndedContext {
  agentId: string;
  task: string;
  result: unknown;
}

interface OpenClawConfig {
  agents?: {
    list?: Array<{ id: string; workspace?: string }>;
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Extract the `binding:` section from a contract YAML string using regex.
 * Avoids adding a js-yaml dependency to keep the plugin lightweight.
 *
 * Matches "binding:" at column 0 followed by indented lines until the next
 * top-level key (or end-of-string).
 */
function formatBinding(yamlContent: string): string {
  const bindingMatch = yamlContent.match(/^binding:\n((?:[ \t]+.+\n?)*)/m);
  if (!bindingMatch) return "";

  const lines = bindingMatch[1]
    .split("\n")
    .filter((l) => l.trim().length > 0);

  if (lines.length === 0) return "";

  const formatted = lines.map((l) => `- ${l.trim()}`).join("\n");
  return (
    "## Binding Constraints (from handoff contract — these override your defaults)\n\n" +
    formatted +
    "\n\n"
  );
}

/**
 * Extract a simple top-level scalar from YAML without adding a parser
 * dependency. Used for fields like artifact_path that are guaranteed by
 * contract validation to be single-line scalar values.
 */
function extractTopLevelScalar(yamlContent: string, key: string): string | null {
  const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = yamlContent.match(
    new RegExp(`^${escapedKey}:\\s*(.+?)\\s*$`, "m"),
  );
  if (!match) return null;

  const raw = match[1].trim();
  if (
    (raw.startsWith('"') && raw.endsWith('"')) ||
    (raw.startsWith("'") && raw.endsWith("'"))
  ) {
    return raw.slice(1, -1);
  }
  return raw;
}

/**
 * Safely read a text file, returning null on any error.
 */
async function safeReadFile(path: string): Promise<string | null> {
  try {
    return await readFile(path, "utf-8");
  } catch {
    return null;
  }
}

/**
 * Resolve the workspace directory for an agent by reading the OpenClaw
 * config at ~/.openclaw/openclaw.json and matching on agentId.
 */
async function resolveAgentWorkspace(agentId: string): Promise<string> {
  const homeDir = process.env.HOME || process.env.USERPROFILE || "";
  const configPath = `${homeDir}/.openclaw/openclaw.json`;

  try {
    const raw = await readFile(configPath, "utf-8");
    const config: OpenClawConfig = JSON.parse(raw);
    const agentEntry = (config.agents?.list || []).find(
      (a) => a.id === agentId,
    );
    return agentEntry?.workspace || "";
  } catch {
    return "";
  }
}

// ---------------------------------------------------------------------------
// Plugin export
// ---------------------------------------------------------------------------

export default {
  name: "context-inject",

  /**
   * Called before a sub-agent session starts.
   *
   * Reads SOUL.md and IDENTITY.md (but NOT USER.md — operator PII) from the
   * agent's workspace and prepends them to the task string. If the task
   * references a handoff contract (via "handoff-contract: <path>"), the
   * binding section is extracted and injected as override constraints.
   */
  async prepareSubagentSpawn(ctx: SpawnContext): Promise<SpawnResult> {
    const { agentId, task } = ctx;

    // --- Resolve agent workspace ---
    const agentWorkspace = await resolveAgentWorkspace(agentId);

    // --- Build identity block (SOUL.md + IDENTITY.md) ---
    let identityBlock = "";

    if (agentWorkspace) {
      const soul = await safeReadFile(`${agentWorkspace}/SOUL.md`);
      if (soul !== null) {
        identityBlock += `## Your Identity (from SOUL.md)\n\n${soul}\n\n`;
      } else {
        console.warn(`[context-inject] SOUL.md not found for ${agentId}`);
      }

      const identity = await safeReadFile(`${agentWorkspace}/IDENTITY.md`);
      if (identity !== null) {
        identityBlock += `## Your Profile (from IDENTITY.md)\n\n${identity}\n\n`;
      }
      // IDENTITY.md is optional — no warning if missing
    }

    // --- Build binding block from handoff contract (if referenced) ---
    let bindingBlock = "";
    const contractMatch = task.match(/handoff-contract:\s*(\S+)/);

    if (contractMatch) {
      const contractPath = contractMatch[1];
      const contractYaml = await safeReadFile(contractPath);

      if (contractYaml !== null) {
        bindingBlock = formatBinding(contractYaml);
      } else {
        console.warn(
          `[context-inject] Failed to read contract at ${contractPath}`,
        );
      }
    }

    // --- Preserve pipeline-state reference ---
    // Extract pipeline-state: reference from the original task so it survives
    // task restructuring and remains available to onSubagentEnded.
    const pipelineStateMatch = task.match(/pipeline-state:\s*(\S+)/);
    let pipelineStateRef = "";
    if (pipelineStateMatch) {
      pipelineStateRef = `\npipeline-state: ${pipelineStateMatch[1]}\n`;
    }

    // --- Assemble modified task ---
    const parts = [identityBlock, bindingBlock, "## Task\n\n", task].filter(
      Boolean,
    );

    return { task: parts.join("\n") + pipelineStateRef };
  },

  /**
   * Called after a sub-agent session ends.
   *
   * If the original task referenced a handoff contract, runs the Python
   * assertion engine (compiler/engine/contract_assertions.py) to verify
   * that output artifacts satisfy the contract's verification rules.
   */
  async onSubagentEnded(ctx: EndedContext): Promise<void> {
    const { agentId, task } = ctx;

    const contractMatch = task.match(/handoff-contract:\s*(\S+)/);
    if (!contractMatch) return; // No contract referenced — nothing to verify

    const contractPath = contractMatch[1];
    const workspaceRoot = process.env.OPENCLAW_WORKSPACE || ".";
    const agentWorkspace = await resolveAgentWorkspace(agentId);
    const verificationWorkspace = agentWorkspace || workspaceRoot;

    let artifactPath: string | null = null;
    const contractYaml =
      (await safeReadFile(`${verificationWorkspace}/${contractPath}`)) ??
      (await safeReadFile(`${workspaceRoot}/${contractPath}`)) ??
      (await safeReadFile(contractPath));
    if (contractYaml !== null) {
      artifactPath = extractTopLevelScalar(contractYaml, "artifact_path");
    }

    // --- Contract verification (existing) ---
    let contractPassed = true;
    let contractErrorDetail = "";

    try {
      const pythonSnippet = [
        "from compiler.engine.contract_assertions import run_assertions",
        "import json",
        `r = run_assertions(${JSON.stringify(contractPath)}, ${JSON.stringify(verificationWorkspace)})`,
        "print(json.dumps({",
        "  'passed': r.passed,",
        "  'total': r.total,",
        "  'failures': [{'type': f['type'], 'detail': f['detail']} for f in r.failures]",
        "}))",
      ].join("; ");

      const output = execFileSync("python3", ["-c", pythonSnippet], {
        cwd: verificationWorkspace,
        encoding: "utf-8",
        timeout: 30_000,
      });

      const result = JSON.parse(output.trim()) as {
        passed: boolean;
        total: number;
        failures: Array<{ type: string; detail: string }>;
      };

      if (result.passed) {
        console.log(
          `[context-inject] Contract verification PASSED for ${agentId} (${result.total} assertions)`,
        );
      } else {
        contractPassed = false;
        contractErrorDetail = result.failures
          .map((f) => `${f.type}: ${f.detail}`)
          .join("; ");
        console.error(
          `[context-inject] Contract verification FAILED for ${agentId}: ${result.failures.length}/${result.total} assertions failed`,
        );
        for (const f of result.failures) {
          console.error(`  - ${f.type}: ${f.detail}`);
        }
      }
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e);
      contractPassed = false;
      contractErrorDetail = `Assertion runner error: ${message}`;
      console.warn(
        `[context-inject] Assertion runner failed for ${agentId}: ${message}`,
      );
    }

    // --- Pipeline state write (T019) ---
    const stateMatch = task.match(/pipeline-state:\s*(\S+)/);
    if (!stateMatch) return; // No pipeline state referenced — skip

    const statePath = stateMatch[1];

    try {
      const stateSnippet = [
        "from compiler.engine.pipeline_state import update_stage_verdict",
        "from pathlib import Path",
        "updated = update_stage_verdict(",
        `    Path(${JSON.stringify(statePath)}),`,
        `    agent=${JSON.stringify(agentId)},`,
        `    contract=${JSON.stringify(contractPath)},`,
        "    actor='context-inject-plugin',",
        `    passed=${contractPassed ? "True" : "False"},`,
        `    artifact=${artifactPath === null ? "None" : JSON.stringify(artifactPath)},`,
        `    error_detail=${contractErrorDetail ? JSON.stringify(contractErrorDetail) : "None"},`,
        ")",
        "if not updated:",
        "    raise RuntimeError('matching stage not found in pipeline state')",
      ].join("\n");

      execFileSync("python3", ["-c", stateSnippet], {
        cwd: workspaceRoot,
        encoding: "utf-8",
        timeout: 10_000,
      });

      console.log(
        `[context-inject] Pipeline state updated for ${agentId} (${contractPassed ? "completed" : "failed"}) at ${statePath}`,
      );
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e);
      console.warn(
        `[context-inject] Pipeline state write failed for ${agentId}: ${message}`,
      );
    }
  },
};
