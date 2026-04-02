/**
 * paperclip-lifecycle-bridge — OpenClaw gateway plugin
 *
 * Translates Paperclip task assignments into clean specialist briefs for
 * restricted agents. Handles claim/checkout/status-update lifecycle in
 * infrastructure so agents never need HTTP tools for Paperclip protocol.
 *
 * Hooks:
 *   - message_received: detect Paperclip wake, claim issue, build brief
 *   - before_prompt_build: inject clean brief instead of raw procedure
 *   - agent_end: update Paperclip issue status from agent outcome
 */

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PluginConfig {
  paperclipApiUrl: string;
  supportedSpecialists: string[];
  defaultReviewPosture: "done" | "in_review";
  dedupeWindowMs: number;
}

interface PaperclipEnv {
  PAPERCLIP_RUN_ID?: string;
  PAPERCLIP_AGENT_ID?: string;
  PAPERCLIP_COMPANY_ID?: string;
  PAPERCLIP_API_URL?: string;
  PAPERCLIP_API_KEY?: string;
  PAPERCLIP_TASK_ID?: string;
  PAPERCLIP_WAKE_REASON?: string;
}

interface PaperclipIssue {
  id: string;
  identifier?: string;
  title: string;
  description?: string;
  status: string;
  priority?: string;
  assigneeAgentId?: string;
  kind?: "task" | "conversation";
}

interface AssignmentBrief {
  issue_id: string;
  specialist_agent_id: string;
  title: string;
  instructions: string;
  review_posture: "done" | "in_review";
  source_summary: string;
}

interface LifecycleOutcome {
  issue_id: string;
  result_state: "done" | "blocked" | "in_review" | "no_action";
  summary: string;
  blocker_owner?: string;
  duplicate_wake: boolean;
}

interface AuditRecord {
  run_id: string;
  issue_id: string;
  agent_id: string;
  action: string;
  success: boolean;
  detail?: string;
}

// ---------------------------------------------------------------------------
// State — per-run context shared across hooks
// ---------------------------------------------------------------------------

/** Active briefs keyed by run ID */
const activeBriefs = new Map<string, AssignmentBrief>();

/** Recent claims keyed by issue ID → timestamp for dedup */
const recentClaims = new Map<string, number>();

/** Audit log buffer */
const auditLog: AuditRecord[] = [];

// ---------------------------------------------------------------------------
// Paperclip API helpers
// ---------------------------------------------------------------------------

function paperclipHeaders(env: PaperclipEnv): Record<string, string> {
  const h: Record<string, string> = { "Content-Type": "application/json" };
  if (env.PAPERCLIP_API_KEY) {
    h["Authorization"] = `Bearer ${env.PAPERCLIP_API_KEY}`;
  }
  if (env.PAPERCLIP_RUN_ID) {
    h["X-Paperclip-Run-Id"] = env.PAPERCLIP_RUN_ID;
  }
  return h;
}

async function checkoutIssue(
  baseUrl: string,
  issueId: string,
  agentId: string,
  env: PaperclipEnv,
): Promise<PaperclipIssue | null> {
  try {
    const resp = await fetch(`${baseUrl}/api/issues/${issueId}/checkout`, {
      method: "POST",
      headers: paperclipHeaders(env),
      body: JSON.stringify({
        agentId,
        expectedStatuses: ["todo", "backlog", "blocked"],
      }),
    });
    if (resp.status === 409) return null; // owned by another agent
    if (!resp.ok) return null;
    return (await resp.json()) as PaperclipIssue;
  } catch {
    return null;
  }
}

async function fetchIssue(
  baseUrl: string,
  issueId: string,
  env: PaperclipEnv,
): Promise<PaperclipIssue | null> {
  try {
    const resp = await fetch(`${baseUrl}/api/issues/${issueId}`, {
      headers: paperclipHeaders(env),
    });
    if (!resp.ok) return null;
    return (await resp.json()) as PaperclipIssue;
  } catch {
    return null;
  }
}

async function updateIssueStatus(
  baseUrl: string,
  issueId: string,
  status: string,
  comment: string,
  env: PaperclipEnv,
): Promise<boolean> {
  try {
    const resp = await fetch(`${baseUrl}/api/issues/${issueId}`, {
      method: "PATCH",
      headers: paperclipHeaders(env),
      body: JSON.stringify({ status, comment }),
    });
    return resp.ok;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Wake detection and parsing
// ---------------------------------------------------------------------------

function parsePaperclipEnv(message: string): PaperclipEnv | null {
  const env: PaperclipEnv = {};
  const keys = [
    "PAPERCLIP_RUN_ID",
    "PAPERCLIP_AGENT_ID",
    "PAPERCLIP_COMPANY_ID",
    "PAPERCLIP_API_URL",
    "PAPERCLIP_API_KEY",
    "PAPERCLIP_TASK_ID",
    "PAPERCLIP_WAKE_REASON",
  ] as const;

  const extractLineValue = (key: string): string | undefined => {
    const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = message.match(
      new RegExp(`(?:^|\\n)${escapedKey}=([^\\n\\r]+)`, "m"),
    );
    return match?.[1]?.trim();
  };

  for (const key of keys) {
    const value = extractLineValue(key);
    if (value) {
      (env as Record<string, string>)[key] = value;
    }
  }

  // Paperclip's wake text also includes lowercase hints; use them as fallbacks.
  const lowerTaskId = extractLineValue("task_id");
  const lowerIssueId = extractLineValue("issue_id");
  const linkedIssueIds = extractLineValue("linked_issue_ids");

  if (!env.PAPERCLIP_TASK_ID) {
    env.PAPERCLIP_TASK_ID =
      lowerTaskId ||
      lowerIssueId ||
      linkedIssueIds?.split(",").map((v) => v.trim()).find(Boolean);
  }

  if (!env.PAPERCLIP_WAKE_REASON) {
    env.PAPERCLIP_WAKE_REASON = extractLineValue("wake_reason");
  }

  // Must have at least run ID and task ID to be a valid Paperclip wake
  if (!env.PAPERCLIP_RUN_ID) return null;
  return env;
}

function isPaperclipWake(message: string): boolean {
  return (
    message.includes("Paperclip wake event") ||
    message.includes("PAPERCLIP_RUN_ID=")
  );
}

function coerceText(value: unknown): string {
  if (typeof value === "string") return value;
  if (value == null) return "";
  if (Array.isArray(value)) {
    return value.map((item) => coerceText(item)).filter(Boolean).join("\n");
  }
  if (typeof value === "object") {
    const record = value as Record<string, unknown>;
    const preferred = [
      record.text,
      record.content,
      record.output_text,
      record.result,
      record.message,
    ];
    for (const candidate of preferred) {
      const text = coerceText(candidate);
      if (text) return text;
    }
    try {
      return JSON.stringify(value);
    } catch {
      return String(value);
    }
  }
  return String(value);
}

// ---------------------------------------------------------------------------
// Brief construction
// ---------------------------------------------------------------------------

function buildBrief(
  issue: PaperclipIssue,
  agentId: string,
  reviewPosture: "done" | "in_review",
): AssignmentBrief {
  // Combine title + description as the clean instructions
  const parts: string[] = [];
  if (issue.title) parts.push(issue.title);
  if (issue.description) parts.push(issue.description);
  const instructions = parts.join("\n\n").trim() || issue.title;

  return {
    issue_id: issue.id,
    specialist_agent_id: agentId,
    title: issue.title,
    instructions,
    review_posture: reviewPosture,
    source_summary: `Assigned from Paperclip (${issue.identifier ?? issue.id})`,
  };
}

function briefToMessage(brief: AssignmentBrief): string {
  return [
    brief.instructions,
    "",
    `[Paperclip: ${brief.source_summary}]`,
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Outcome classification
// ---------------------------------------------------------------------------

function classifyOutcome(
  brief: AssignmentBrief,
  agentResponse: string,
  exitSuccess: boolean,
): LifecycleOutcome {
  const lower = agentResponse.toLowerCase();
  const blockedSignals = [
    "blocked",
    "cannot proceed",
    "can't proceed",
    "can’t proceed",
    "failed",
    "error:",
    "can't execute",
    "can’t execute",
    "do not have campaign parameters",
    "don't have campaign parameters",
    "missing campaign parameters",
    "need campaign parameters",
  ];

  // Explicit block signals
  if (
    !exitSuccess ||
    blockedSignals.some((signal) => lower.includes(signal))
  ) {
    return {
      issue_id: brief.issue_id,
      result_state: "blocked",
      summary: agentResponse.slice(0, 500),
      duplicate_wake: false,
    };
  }

  // Use the brief's review posture as the default
  return {
    issue_id: brief.issue_id,
    result_state: brief.review_posture,
    summary: agentResponse.slice(0, 500),
    duplicate_wake: false,
  };
}

// ---------------------------------------------------------------------------
// Audit
// ---------------------------------------------------------------------------

function audit(record: AuditRecord): void {
  auditLog.push(record);
  // In production, this would write to memory/logs/paperclip-lifecycle/
  const prefix = record.success ? "OK" : "FAIL";
  console.log(
    `[paperclip-lifecycle-bridge] ${prefix}: ${record.action} issue=${record.issue_id} agent=${record.agent_id}`,
  );
}

// ---------------------------------------------------------------------------
// Plugin registration — matches OpenClaw plugin SDK pattern
// ---------------------------------------------------------------------------

interface OpenClawPluginApi {
  pluginConfig: Record<string, unknown>;
  on: (
    hookName: string,
    handler: (event: Record<string, unknown>, ctx: Record<string, unknown>) => unknown,
    opts?: { priority: number },
  ) => void;
}

function register(api: OpenClawPluginApi) {
  const raw = api.pluginConfig ?? {};
  const config: PluginConfig = {
    paperclipApiUrl: String(raw.paperclipApiUrl ?? "http://localhost:3100"),
    supportedSpecialists: Array.isArray(raw.supportedSpecialists) ? raw.supportedSpecialists as string[] : [],
    defaultReviewPosture: (raw.defaultReviewPosture === "done" ? "done" : "in_review"),
    dedupeWindowMs: Number(raw.dedupeWindowMs ?? 30_000),
  };

  console.log(
    `[paperclip-lifecycle-bridge] loaded. Supported specialists: ${config.supportedSpecialists.join(", ") || "(none — passthrough mode)"}`,
  );

  // -------------------------------------------------------------------------
  // Hook: before_prompt_build — intercept Paperclip wake before agent sees it
  // Fires after session load, before model prompt. Works for WebSocket
  // agent requests from Paperclip (message_received only fires for channels).
  // -------------------------------------------------------------------------
  api.on(
    "before_prompt_build",
    async (event, ctx) => {
      const hookAgentId = String(
        ctx?.agentId ?? event.context?.agentId ?? event.agentId ?? "",
      );
      const hookSessionKey = String(
        ctx?.sessionKey ?? ctx?.sessionId ?? "",
      );

      // Extract the latest user message from the messages array
      const messages = event.messages as Array<{ role: string; content: unknown }> | undefined;
      const lastUser = messages?.filter((m) => m.role === "user")?.pop();
      const content = coerceText(lastUser?.content ?? event.message ?? "");
      console.log(
        `[paperclip-lifecycle-bridge] before_prompt_build entry agent=${hookAgentId || "(unknown)"} chars=${content.length}`,
      );
      if (!isPaperclipWake(content)) {
        console.log(
          `[paperclip-lifecycle-bridge] before_prompt_build skip agent=${hookAgentId || "(unknown)"} reason=not_paperclip_wake`,
        );
        return; // not a Paperclip wake — passthrough
      }

      const agentId = String(
        ctx?.agentId ?? event.context?.agentId ?? event.agentId ?? "",
      );

      // Only intercept for enrolled specialists
      if (
        config.supportedSpecialists.length > 0 &&
        !config.supportedSpecialists.includes(agentId)
      ) {
        console.log(
          `[paperclip-lifecycle-bridge] before_prompt_build skip agent=${agentId || "(unknown)"} reason=unsupported_agent`,
        );
        return; // unsupported agent — let default procedure through
      }

      const env = parsePaperclipEnv(content);
      if (!env) {
        console.log(
          `[paperclip-lifecycle-bridge] before_prompt_build skip agent=${agentId || "(unknown)"} reason=env_parse_failed`,
        );
        return;
      }

      const issueId = env.PAPERCLIP_TASK_ID;
      console.log(
        `[paperclip-lifecycle-bridge] parsed_wake agent=${agentId || "(unknown)"} hasUpperTask=${content.includes("PAPERCLIP_TASK_ID=")} hasLowerTask=${content.includes("task_id=")} hasLinkedIssues=${content.includes("linked_issue_ids=")} runId=${env.PAPERCLIP_RUN_ID ? "yes" : "no"} taskId=${issueId ? "yes" : "no"}`,
      );
      if (!issueId) {
        console.log(
          `[paperclip-lifecycle-bridge] before_prompt_build skip agent=${agentId || "(unknown)"} reason=missing_issue_id`,
        );
        return;
      }

      // Dedupe check
      const lastClaim = recentClaims.get(issueId);
      if (lastClaim && Date.now() - lastClaim < config.dedupeWindowMs) {
        audit({
          run_id: env.PAPERCLIP_RUN_ID!,
          issue_id: issueId,
          agent_id: agentId,
          action: "dedupe_skip",
          success: true,
          detail: "Duplicate wake within dedup window",
        });
        return { suppress: true }; // prevent duplicate processing
      }

      // Claim the issue
      const baseUrl = env.PAPERCLIP_API_URL ?? config.paperclipApiUrl;
      const claimed = await checkoutIssue(baseUrl, issueId, env.PAPERCLIP_AGENT_ID ?? agentId, env);

      audit({
        run_id: env.PAPERCLIP_RUN_ID!,
        issue_id: issueId,
        agent_id: agentId,
        action: "claim",
        success: !!claimed,
        detail: claimed ? `status=${claimed.status}` : "checkout failed or 409",
      });

      if (!claimed) {
        // Fetch issue anyway to post a helpful comment
        await updateIssueStatus(
          baseUrl,
          issueId,
          "blocked",
          "Lifecycle bridge could not claim this issue. It may be owned by another agent.",
          env,
        );
        return { suppress: true };
      }

      // Fetch full issue context
      const issue = await fetchIssue(baseUrl, issueId, env);
      if (!issue) {
        audit({
          run_id: env.PAPERCLIP_RUN_ID!,
          issue_id: issueId,
          agent_id: agentId,
          action: "fetch_context",
          success: false,
          detail: "Could not fetch issue details",
        });
        return; // let the default wake through as fallback
      }

      audit({
        run_id: env.PAPERCLIP_RUN_ID!,
        issue_id: issueId,
        agent_id: agentId,
        action: "fetch_context",
        success: true,
      });

      // Build clean brief
      const brief = buildBrief(issue, agentId, config.defaultReviewPosture);
      const runId = env.PAPERCLIP_RUN_ID!;
      const briefKey = hookSessionKey || runId;
      activeBriefs.set(briefKey, brief);
      recentClaims.set(issueId, Date.now());

      // Store env for agent_end hook
      activeBriefs.set(`env:${briefKey}`, { ...brief, _env: env } as unknown as AssignmentBrief);

      audit({
        run_id: runId,
        issue_id: issueId,
        agent_id: agentId,
        action: "deliver_brief",
        success: true,
        detail: `title="${brief.title.slice(0, 80)}"`,
      });

      // Inject the clean brief via system context (message mutation doesn't propagate).
      // The system context override tells the agent to ignore the raw Paperclip procedure
      // in the user message and work from the brief instead.
      const briefText = briefToMessage(brief);
      return {
        prependSystemContext: [
          `<PAPERCLIP_LIFECYCLE_BRIDGE>`,
          `A Paperclip task was assigned to you. The lifecycle bridge has already claimed this task and will update Paperclip when you finish.`,
          ``,
          `IGNORE the Paperclip HTTP procedure in the user message below. Do NOT run curl commands, fetch calls, or any HTTP API procedure. The bridge handles all Paperclip API interactions.`,
          ``,
          `YOUR TASK (execute this using your normal tools):`,
          briefText,
          `</PAPERCLIP_LIFECYCLE_BRIDGE>`,
        ].join("\n"),
      };
    },
    { priority: 5 }, // run early, before other plugins
  );

  // -------------------------------------------------------------------------
  // Hook: agent_end — update Paperclip issue status from agent outcome
  // -------------------------------------------------------------------------
  api.on(
    "agent_end",
    async (event, ctx) => {
      // Find the active brief for this run
      const briefKey = String(
        ctx?.sessionKey ?? ctx?.sessionId ?? event.metadata?.runId ?? event.runId ?? "",
      );
      const brief = activeBriefs.get(briefKey);
      console.log(
        `[paperclip-lifecycle-bridge] agent_end entry run=${briefKey || "(unknown)"} bridged=${brief ? "yes" : "no"}`,
      );
      if (!brief) return; // not a Paperclip-bridged run

      const envHolder = activeBriefs.get(`env:${briefKey}`) as unknown as
        | (AssignmentBrief & { _env: PaperclipEnv })
        | undefined;
      const env = envHolder?._env ?? {};

      // Extract agent response
      const messages = event.messages as Array<{ role: string; content: unknown }> | undefined;
      const lastAssistant = messages
        ?.filter((m) => m.role === "assistant")
        ?.pop();
      const agentResponse = coerceText(
        lastAssistant?.content ??
          event.result ??
          (event as Record<string, unknown>).payloads ??
          (event as Record<string, unknown>).response,
      );
      const exitSuccess = event.metadata?.exitCode === 0 || event.metadata?.status === "ok" || !event.metadata?.error;

      // Classify outcome
      const outcome = classifyOutcome(brief, agentResponse, Boolean(exitSuccess));

      // Update Paperclip
      const baseUrl = (env as PaperclipEnv).PAPERCLIP_API_URL ?? config.paperclipApiUrl;
      const updated = await updateIssueStatus(
        baseUrl,
        outcome.issue_id,
        outcome.result_state === "no_action" ? "in_progress" : outcome.result_state,
        outcome.summary,
        env as PaperclipEnv,
      );

      audit({
        run_id: String((env as PaperclipEnv).PAPERCLIP_RUN_ID ?? briefKey),
        issue_id: outcome.issue_id,
        agent_id: brief.specialist_agent_id,
        action: "update_status",
        success: updated,
        detail: `state=${outcome.result_state}`,
      });

      // Cleanup
      activeBriefs.delete(briefKey);
      activeBriefs.delete(`env:${briefKey}`);

      // Evict old dedup entries
      const now = Date.now();
      for (const [key, ts] of recentClaims) {
        if (now - ts > config.dedupeWindowMs * 3) {
          recentClaims.delete(key);
        }
      }
    },
    { priority: 90 }, // run late, after agent has fully completed
  );
}

const plugin = {
  id: "paperclip-lifecycle-bridge",
  name: "Paperclip Lifecycle Bridge",
  description: "Translates Paperclip task assignments into clean specialist briefs for restricted agents",
  configSchema: {
    type: "object" as const,
    properties: {
      paperclipApiUrl: { type: "string" as const },
      supportedSpecialists: { type: "array" as const, items: { type: "string" as const } },
      defaultReviewPosture: { type: "string" as const, enum: ["done", "in_review"] },
      dedupeWindowMs: { type: "integer" as const },
    },
    additionalProperties: false,
  },
  register,
};

export default plugin;
