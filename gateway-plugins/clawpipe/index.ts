// @ts-nocheck
// ClawPipe — OpenClaw gateway bridge plugin
// Registers `clawpipe` tool and HTTP webhook routes, delegates to Python CLI via child_process.
// Uses @ts-nocheck to avoid openclaw/plugin-sdk import resolution bug (#53002)

import { execFile } from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const DEFAULT_TIMEOUT_MS = 60_000;

function resolveConfig(api) {
  const cfg = api?.pluginConfig ?? {};
  const repoRoot = (typeof cfg.repoRoot === "string" && cfg.repoRoot.trim()) ||
    process.env.OPENCLAW_WORKSPACE || process.cwd();
  const pythonBin = (typeof cfg.pythonBin === "string" && cfg.pythonBin.trim()) ||
    path.join(repoRoot, "clawpipe", ".venv", "bin", "python");
  const timeoutMs = (typeof cfg.timeoutMs === "number" && Number.isFinite(cfg.timeoutMs))
    ? cfg.timeoutMs : DEFAULT_TIMEOUT_MS;
  return { repoRoot, pythonBin, timeoutMs };
}

function textResult(payload) {
  return { content: [{ type: "text", text: JSON.stringify(payload) }] };
}

async function runCli(pythonBin, repoRoot, args, timeoutMs) {
  let stdout, stderr;
  try {
    const result = await execFileAsync(
      pythonBin, ["-m", "clawpipe", ...args, "--json"],
      {
        cwd: repoRoot, timeout: timeoutMs, maxBuffer: 2 * 1024 * 1024,
        env: { ...process.env, PYTHONPATH: path.join(repoRoot, "clawpipe", "src") },
      }
    );
    stdout = result.stdout;
    stderr = result.stderr;
  } catch (err) {
    // CLI exits non-zero for needs_dispatch/needs_approval — still parse stdout
    stdout = err.stdout ?? "";
    stderr = err.stderr ?? "";
    const raw = stdout.trim();
    if (raw) try { return JSON.parse(raw); } catch {}
    throw err;
  }
  const raw = stdout.trim();
  if (!raw) throw new Error(`clawpipe CLI empty stdout${stderr ? ` (${stderr.trim()})` : ""}`);
  try { return JSON.parse(raw); }
  catch { throw new Error(`clawpipe non-JSON: ${raw.slice(0, 500)}`); }
}

/** Collect request body chunks and JSON-parse them. */
function readBody(req): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("error", reject);
    req.on("end", () => {
      const raw = Buffer.concat(chunks).toString("utf-8").trim();
      if (!raw) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(raw));
      } catch (err) {
        reject(new Error(`Invalid JSON body: ${err.message}`));
      }
    });
  });
}

/** Build CLI args array from action name and parsed body params. */
function buildArgs(action: string, params: Record<string, unknown>): string[] {
  const args = [action];
  if (params.config_path) args.push("--config", String(params.config_path));
  if (params.pipeline_id) args.push("--pipeline-id", String(params.pipeline_id));

  switch (action) {
    case "run":
      if (params.reasoning_mode) args.push("--reasoning-mode", String(params.reasoning_mode));
      break;
    case "resume":
      if (params.approved === true) args.push("--approved");
      else if (params.approved === false) args.push("--rejected");
      if (params.option_value) args.push("--option-value", String(params.option_value));
      if (params.stage_result != null) args.push("--stage-result", String(params.stage_result));
      if (params.stage_error != null) args.push("--stage-error", String(params.stage_error));
      if (params.cost != null) args.push("--cost", String(params.cost));
      break;
    case "watch":
      if (params.runs_dir) args.push("--runs-dir", String(params.runs_dir));
      break;
    case "goals":
      if (params.last_n) args.push("--last-n", String(params.last_n));
      break;
    case "factory":
      if (params.intent) args.push("--intent", String(params.intent));
      if (params.modify) args.push("--modify", String(params.modify));
      break;
    case "trigger":
      if (params.trigger_action) args.push("--action", String(params.trigger_action));
      break;
    case "rubric-gen":
      if (params.stage) args.push("--stage", String(params.stage));
      break;
    case "heartbeat":
      if (params.stage) args.push("--stage", String(params.stage));
      if (params.progress) args.push("--progress", String(params.progress));
      break;
  }

  return args;
}

/** Send a JSON response on a raw Node ServerResponse. */
function sendJson(res, statusCode: number, payload: unknown) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(payload));
}

/** Known HTTP route actions and their path suffixes. */
const KNOWN_ACTIONS = [
  "run", "resume", "show", "lessons", "watch",
  "goals", "factory", "trigger", "rubric-gen", "heartbeat",
] as const;

export function register(api) {
  const { repoRoot, pythonBin, timeoutMs } = resolveConfig(api);

  // ─── Tool registration (existing) ───────────────────────────────────
  api.registerTool({
    name: "clawpipe",
    description: "Run, resume, show, or watch config-driven pipelines. Returns Envelope JSON.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        action: { type: "string", enum: ["run","resume","show","lessons","watch","goals","factory","trigger","rubric-gen","heartbeat"], description: "Action to perform" },
        config_path: { type: "string", description: "Path to pipeline YAML config" },
        pipeline_id: { type: "string", description: "Pipeline run identifier" },
        approved: { type: "boolean", description: "Resume: true=approve, false=reject" },
        runs_dir: { type: "string", description: "Watch: directory to scan" },
        reasoning_mode: { type: "string", enum: ["simple","standard","extended","auto"] },
        intent: { type: "string", description: "Factory: natural language intent" },
        modify: { type: "string", description: "Factory: modification to apply" },
        trigger_action: { type: "string", enum: ["list","enable","disable","fire"] },
        option_value: { type: "string", description: "Resume: selected approval option" },
        last_n: { type: "number", description: "Goals: number of recent runs" },
        stage: { type: "string", description: "Rubric-gen/heartbeat: stage name" },
        stage_result: { type: "string", description: "Resume: agent dispatch result" },
        stage_error: { type: "string", description: "Resume: agent dispatch error" },
        cost: { type: "number", description: "Resume: dispatch cost" },
        progress: { type: "string", description: "Heartbeat: progress text" },
      },
      required: ["action"],
    },
    async execute(_id, params) {
      const action = String(params.action);
      const args = buildArgs(action, params);

      try {
        return textResult(await runCli(pythonBin, repoRoot, args, timeoutMs));
      } catch (err) {
        return textResult({ status: "error", error: err.message || String(err), action });
      }
    },
  });

  // ─── HTTP webhook routes ────────────────────────────────────────────
  for (const action of KNOWN_ACTIONS) {
    api.registerHttpRoute({
      path: `/clawpipe/${action}`,
      auth: "gateway",
      match: "exact",
      handler: async (req, res) => {
        try {
          const body = await readBody(req);
          const args = buildArgs(action, body);
          const result = await runCli(pythonBin, repoRoot, args, timeoutMs);
          sendJson(res, 200, result);
        } catch (err) {
          sendJson(res, 200, { status: "error", error: err.message || String(err), action });
        }
      },
    });
  }

  // Catch-all for unknown /clawpipe/* paths
  api.registerHttpRoute({
    path: "/clawpipe/",
    auth: "gateway",
    match: "prefix",
    handler: async (_req, res) => {
      sendJson(res, 404, { error: "Unknown action" });
    },
  });

  console.log(`[clawpipe] tool registered, ${KNOWN_ACTIONS.length} HTTP routes registered`);
}

export function activate(api) { register(api); }
export default { register, activate };
