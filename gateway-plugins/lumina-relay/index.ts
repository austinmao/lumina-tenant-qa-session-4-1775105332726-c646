// @ts-nocheck

const RELAY_FORWARD_TIMEOUT_MS = 5_000;
const MAX_RETRY_ATTEMPTS = 3;
const RELAY_AGENT_ID = "agents-platform-relay";
const CHANNEL_ALIASES = {
  imessage: "imessage",
  whatsapp: "whatsapp",
  telegram: "telegram",
  discord: "discord",
  slack: "slack",
};

let execFilePromise;
let timingSafeEqualPromise;

function log(api, level, event, meta = {}) {
  const prefix = `[lumina-relay] ${level} ${event}`;
  if (level === "error") console.error(prefix, meta);
  else if (level === "warn") console.warn(prefix, meta);
  else console.log(prefix, meta);
  api?.logger?.[level]?.(`${event} ${JSON.stringify(meta)}`);
}

async function getExecFileAsync() {
  if (!execFilePromise) {
    execFilePromise = (async () => {
      const { execFile } = await import("node:child_process");
      const { promisify } = await import("node:util");
      return promisify(execFile);
    })();
  }
  return execFilePromise;
}

function normalizeText(value) {
  if (typeof value !== "string") return "";
  return value.trim();
}

async function getTimingSafeEqual() {
  if (!timingSafeEqualPromise) {
    timingSafeEqualPromise = import("node:crypto").then(({ timingSafeEqual }) => timingSafeEqual);
  }
  return timingSafeEqualPromise;
}

async function timingSafeBearerMatch(authHeader, expectedToken) {
  if (!expectedToken || typeof authHeader !== "string" || !authHeader.startsWith("Bearer ")) {
    return false;
  }

  const presented = authHeader.slice(7);
  const presentedBuf = Buffer.from(presented);
  const expectedBuf = Buffer.from(expectedToken);
  if (presentedBuf.length !== expectedBuf.length) return false;

  const timingSafeEqual = await getTimingSafeEqual();
  return timingSafeEqual(presentedBuf, expectedBuf);
}

function buildRelayMessageId(event, senderPhone) {
  const metadataId = normalizeText(event?.metadata?.messageId);
  if (metadataId) return metadataId;

  const stamp = typeof event?.timestamp === "number" ? event.timestamp : Date.now();
  return `relay-${senderPhone.replace(/[^\d+]/g, "")}-${stamp}`;
}

function resolveSenderPhone(event) {
  const candidates = [
    event?.metadata?.senderE164,
    event?.metadata?.senderId,
    event?.from,
  ];

  for (const candidate of candidates) {
    const text = normalizeText(candidate);
    if (text.startsWith("+")) return text;
  }

  return null;
}

function resolveChannelOrigin(event, ctx) {
  const candidates = [
    ctx?.channelId,
    event?.metadata?.originatingChannel,
    event?.metadata?.provider,
  ];

  for (const candidate of candidates) {
    const normalized = normalizeText(candidate).toLowerCase();
    if (CHANNEL_ALIASES[normalized]) return CHANNEL_ALIASES[normalized];
  }

  return "imessage";
}

async function lookupByPhone(phone) {
  const { sql } = await import("@vercel/postgres");
  const { rows } = await sql`
    SELECT phone_number, tenant_id, relay_endpoint, relay_status, redirect_hint
    FROM hub_relay_routing
    WHERE phone_number = ${phone}
    LIMIT 1
  `;
  return rows.length > 0 ? rows[0] : null;
}

async function recordRelayedMessage(messageId, tenantId, senderPhone, channelOrigin) {
  const { sql } = await import("@vercel/postgres");
  await sql`
    INSERT INTO hub_relay_messages (message_id, tenant_id, sender_phone, channel_origin)
    VALUES (${messageId}, ${tenantId}, ${senderPhone}, ${channelOrigin})
    ON CONFLICT (message_id) DO NOTHING
  `;
}

async function lookupRelayedMessage(messageId) {
  const { sql } = await import("@vercel/postgres");
  const { rows } = await sql`
    SELECT message_id, tenant_id, sender_phone, channel_origin, callback_count
    FROM hub_relay_messages
    WHERE message_id = ${messageId}
    LIMIT 1
  `;
  return rows.length > 0 ? rows[0] : null;
}

async function incrementCallbackCount(messageId) {
  const { sql } = await import("@vercel/postgres");
  await sql`
    UPDATE hub_relay_messages
    SET callback_count = callback_count + 1
    WHERE message_id = ${messageId}
  `;
}

async function forwardToTenant(endpoint, payload, tenantId) {
  const inboundSecret = process.env.LUMINA_RELAY_INBOUND_SECRET;
  if (!inboundSecret) {
    return { success: false, detail: "LUMINA_RELAY_INBOUND_SECRET not configured" };
  }

  for (let attempt = 1; attempt <= MAX_RETRY_ATTEMPTS; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), RELAY_FORWARD_TIMEOUT_MS);
      const res = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${inboundSecret}`,
          "X-Lumina-Tenant-ID": tenantId,
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      clearTimeout(timeout);

      if (res.ok) {
        return { success: true, detail: `Forwarded to ${tenantId} (status ${res.status})` };
      }

      if (attempt === MAX_RETRY_ATTEMPTS) {
        const body = await res.text().catch(() => "");
        return {
          success: false,
          detail: `Tenant returned HTTP ${res.status}${body ? `: ${body}` : ""}`,
        };
      }
    } catch (err) {
      if (attempt === MAX_RETRY_ATTEMPTS) {
        return {
          success: false,
          detail: `Failed after ${MAX_RETRY_ATTEMPTS} attempts: ${err?.message || String(err)}`,
        };
      }
    }
  }

  return { success: false, detail: `Failed after ${MAX_RETRY_ATTEMPTS} attempts` };
}

async function sendTextViaChannel(channelOrigin, target, text) {
  const execFileAsync = await getExecFileAsync();
  const args = [
    "message",
    "send",
    "--channel",
    channelOrigin,
    "--target",
    target,
    "--message",
    text,
    "--json",
  ];

  return execFileAsync("openclaw", args, {
    env: process.env,
    timeout: 20_000,
    maxBuffer: 1024 * 1024,
  });
}

function parseOutboundPayload(body) {
  let payload = body;
  if (typeof payload === "string") {
    try {
      payload = JSON.parse(payload);
    } catch {
      return null;
    }
  } else if (Buffer.isBuffer(payload)) {
    try {
      payload = JSON.parse(payload.toString("utf8"));
    } catch {
      return null;
    }
  }

  if (!payload || typeof payload !== "object") return null;
  if (
    typeof payload.tenant_id !== "string" ||
    typeof payload.message_id !== "string" ||
    typeof payload.recipient_phone !== "string" ||
    typeof payload.reply !== "string"
  ) {
    return null;
  }

  return {
    tenant_id: payload.tenant_id,
    message_id: payload.message_id,
    recipient_phone: payload.recipient_phone,
    reply: payload.reply,
    sequence: typeof payload.sequence === "number" ? payload.sequence : 1,
  };
}

async function readJsonBody(req, maxBytes = 64 * 1024) {
  if (req?.body !== undefined) return req.body;

  const chunks = [];
  let totalBytes = 0;
  for await (const chunk of req) {
    const bufferChunk = Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk));
    totalBytes += bufferChunk.length;
    if (totalBytes > maxBytes) {
      throw new Error("Request body too large");
    }
    chunks.push(bufferChunk);
  }

  if (chunks.length === 0) return null;
  const raw = Buffer.concat(chunks).toString("utf8").trim();
  if (!raw) return null;
  return JSON.parse(raw);
}

async function handleInboundRelay(event, ctx, api) {
  const senderPhone = resolveSenderPhone(event);
  if (!senderPhone) return;

  const entry = await lookupByPhone(senderPhone);
  if (!entry) return;
  if (entry.relay_status === "disabled") {
    log(api, "info", "relay.disabled", { phone: senderPhone, tenant_id: entry.tenant_id });
    return;
  }

  const channelOrigin = resolveChannelOrigin(event, ctx);

  if (entry.relay_status === "dormant") {
    const hint = normalizeText(entry.redirect_hint) || "your direct assistant channel";
    await sendTextViaChannel(
      channelOrigin,
      senderPhone,
      `You can now reach your assistant directly at ${hint}.`,
    );
    log(api, "info", "relay.dormant", { phone: senderPhone, tenant_id: entry.tenant_id, channel: channelOrigin });
    return;
  }

  const text = normalizeText(event?.content);
  if (!text) {
    await sendTextViaChannel(
      channelOrigin,
      senderPhone,
      "I can only handle text messages right now. Please send your question as text.",
    );
    log(api, "info", "relay.unsupported_message", {
      phone: senderPhone,
      tenant_id: entry.tenant_id,
      channel: channelOrigin,
    });
    return;
  }

  const messageId = buildRelayMessageId(event, senderPhone);
  const existing = await lookupRelayedMessage(messageId);
  if (existing) {
    log(api, "info", "relay.duplicate", {
      message_id: messageId,
      tenant_id: existing.tenant_id,
      phone: senderPhone,
    });
    return;
  }

  const payload = {
    message_id: messageId,
    sender_phone: senderPhone,
    text,
    channel_origin: channelOrigin,
    relayed_at: new Date().toISOString(),
  };

  const result = await forwardToTenant(entry.relay_endpoint, payload, entry.tenant_id);
  if (!result.success) {
    await sendTextViaChannel(
      channelOrigin,
      senderPhone,
      "I'm having trouble reaching your assistant right now. Please try again in a moment.",
    );
    log(api, "error", "relay.error", {
      message_id: messageId,
      tenant_id: entry.tenant_id,
      phone: senderPhone,
      detail: result.detail,
    });
    return;
  }

  await recordRelayedMessage(messageId, entry.tenant_id, senderPhone, channelOrigin);
  log(api, "info", "relay.routed", {
    message_id: messageId,
    tenant_id: entry.tenant_id,
    phone: senderPhone,
    channel: channelOrigin,
  });
}

async function handleOutboundCallback(req, res, api) {
  const outboundSecret = process.env.LUMINA_RELAY_OUTBOUND_SECRET;
  if (!outboundSecret) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "LUMINA_RELAY_OUTBOUND_SECRET not configured" }));
    return true;
  }

  const authHeader = req.headers?.authorization;
  if (!await timingSafeBearerMatch(authHeader, outboundSecret)) {
    log(api, "warn", "relay.callback_unauthorized", {});
    res.statusCode = 401;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Unauthorized" }));
    return true;
  }

  let rawBody;
  try {
    rawBody = await readJsonBody(req);
  } catch (err) {
    log(api, "warn", "relay.callback_read_failed", {
      error: err?.message || String(err),
    });
    res.statusCode = 400;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Invalid payload" }));
    return true;
  }

  const payload = parseOutboundPayload(rawBody);
  if (!payload) {
    res.statusCode = 400;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Invalid payload" }));
    return true;
  }

  const record = await lookupRelayedMessage(payload.message_id);
  if (!record) {
    res.statusCode = 404;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Message not found or expired" }));
    return true;
  }

  if (record.tenant_id !== payload.tenant_id || record.sender_phone !== payload.recipient_phone) {
    log(api, "warn", "relay.callback_forbidden", {
      message_id: payload.message_id,
      claimed_tenant: payload.tenant_id,
      claimed_phone: payload.recipient_phone,
    });
    res.statusCode = 403;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Forbidden" }));
    return true;
  }

  await sendTextViaChannel(record.channel_origin, record.sender_phone, payload.reply);
  await incrementCallbackCount(payload.message_id);

  log(api, "info", "relay.callback_received", {
    message_id: payload.message_id,
    tenant_id: payload.tenant_id,
    channel: record.channel_origin,
  });

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify({ status: "delivered" }));
  return true;
}

export function register(api) {
  log(api, "info", "relay.plugin_loaded", { mode: "hub", phase: 2 });

  api.on("message_received", async (event, ctx) => {
    try {
      await handleInboundRelay(event, ctx, api);
    } catch (err) {
      log(api, "error", "relay.message_received_failed", {
        error: err?.message || String(err),
      });
    }
  });

  api.registerHttpRoute({
    path: "/lumina-relay/outbound",
    auth: "plugin",
    match: "exact",
    handler: async (req, res) => {
      try {
        return await handleOutboundCallback(req, res, api);
      } catch (err) {
        log(api, "error", "relay.callback_failed", {
          error: err?.message || String(err),
        });
        res.statusCode = 500;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ error: "Internal server error" }));
        return true;
      }
    },
  });

  api.on("before_model_resolve", async (_event, ctx) => {
    if (ctx?.agentId !== RELAY_AGENT_ID) return;
    return {
      modelOverride: process.env.LUMINA_RELAY_SINK_MODEL || "gpt-5.3-codex",
      providerOverride: process.env.LUMINA_RELAY_SINK_PROVIDER || "openai-codex",
    };
  });
}

export function activate(api) {
  register(api);
}

export default { register, activate };
