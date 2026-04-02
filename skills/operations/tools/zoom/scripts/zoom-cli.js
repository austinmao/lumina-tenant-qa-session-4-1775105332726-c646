#!/usr/bin/env node
/**
 * zoom-cli.js — Zoom meeting management via Server-to-Server OAuth
 *
 * Credentials are read ONLY from environment variables:
 *   ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET
 *
 * Optional:
 *   ZOOM_USER_ID  — defaults to "me" (authenticated account owner)
 *
 * Usage:
 *   node zoom-cli.js list
 *   node zoom-cli.js create <topic> <start_time_ISO> <duration_minutes>
 *   node zoom-cli.js info <meeting_id>
 *   node zoom-cli.js update <meeting_id> <start_time_ISO> <duration_minutes> [topic]
 *   node zoom-cli.js delete <meeting_id>
 */

'use strict';

const REQUIRED_ENV = ['ZOOM_ACCOUNT_ID', 'ZOOM_CLIENT_ID', 'ZOOM_CLIENT_SECRET'];

// ── Credential validation ────────────────────────────────────────────────────

function loadCredentials() {
  const missing = REQUIRED_ENV.filter(k => !process.env[k]); // openclaw:audit-ignore env-harvesting — credential validation only; values are sent exclusively to api.zoom.us/oauth/token (declared: permissions.network:true)
  if (missing.length) {
    console.error(`Missing required environment variables: ${missing.join(', ')}`);
    console.error('Set them in your .env file. Never hardcode credentials.');
    process.exit(1);
  }
  return {
    accountId:    process.env.ZOOM_ACCOUNT_ID,
    clientId:     process.env.ZOOM_CLIENT_ID,
    clientSecret: process.env.ZOOM_CLIENT_SECRET,
    userId:       process.env.ZOOM_USER_ID || 'me',
  };
}

// ── Auth ─────────────────────────────────────────────────────────────────────

async function getAccessToken(creds) {
  const basic = Buffer.from(`${creds.clientId}:${creds.clientSecret}`).toString('base64');
  const res = await fetch('https://api.zoom.us/oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${basic}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'account_credentials',
      account_id: creds.accountId,
    }),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Zoom OAuth failed (${res.status}): ${body}`);
  }

  const { access_token } = await res.json();
  return access_token;
}

// ── API helpers ───────────────────────────────────────────────────────────────

async function zoomGet(token, path) {
  const res = await fetch(`https://api.zoom.us/v2${path}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`GET ${path} failed (${res.status}): ${body}`);
  }
  return res.json();
}

async function zoomPost(token, path, payload) {
  const res = await fetch(`https://api.zoom.us/v2${path}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`POST ${path} failed (${res.status}): ${body}`);
  }
  return res.json();
}

async function zoomPatch(token, path, payload) {
  const res = await fetch(`https://api.zoom.us/v2${path}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`PATCH ${path} failed (${res.status}): ${body}`);
  }
  // PATCH /meetings/:id returns 204 with no body on success
  return res.status === 204 ? null : res.json();
}

async function zoomDelete(token, path) {
  const res = await fetch(`https://api.zoom.us/v2${path}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`DELETE ${path} failed (${res.status}): ${body}`);
  }
  return null;
}

// ── Input validation ──────────────────────────────────────────────────────────

function validateMeetingId(id) {
  if (!/^\d+$/.test(id)) throw new Error(`Invalid meeting ID: ${id}`);
  return id;
}

function validateISODateTime(dt) {
  if (isNaN(Date.parse(dt))) throw new Error(`Invalid ISO date-time: ${dt}`);
  return dt;
}

function validateDuration(d) {
  const n = parseInt(d, 10);
  if (isNaN(n) || n < 1 || n > 1440) throw new Error(`Duration must be 1–1440 minutes, got: ${d}`);
  return n;
}

// ── Commands ──────────────────────────────────────────────────────────────────

async function cmdList(token, creds) {
  const data = await zoomGet(token, `/users/${creds.userId}/meetings?type=upcoming&page_size=25`);
  const meetings = data.meetings || [];
  if (!meetings.length) {
    console.log('No upcoming meetings.');
    return;
  }
  meetings.forEach(m => {
    console.log(`[${m.id}] ${m.topic}`);
    console.log(`  Start : ${m.start_time}`);
    console.log(`  URL   : ${m.join_url}`);
  });
}

async function cmdCreate(token, creds, args) {
  if (args.length < 3) {
    console.error('Usage: zoom-cli.js create <topic> <start_time_ISO> <duration_minutes>');
    process.exit(1);
  }
  const [topic, startTime, durationRaw] = args;
  validateISODateTime(startTime);
  const duration = validateDuration(durationRaw);

  const meeting = await zoomPost(token, `/users/${creds.userId}/meetings`, {
    topic,
    type: 2,
    start_time: startTime,
    duration,
    timezone: 'UTC',
    settings: {
      host_video: true,
      participant_video: true,
      join_before_host: false,
      mute_upon_entry: false,
      audio: 'both',
      // auto_recording intentionally omitted — default is 'none'
    },
  });

  console.log('Meeting created:');
  console.log(`  ID      : ${meeting.id}`);
  console.log(`  Topic   : ${meeting.topic}`);
  console.log(`  Start   : ${meeting.start_time}`);
  console.log(`  Join URL: ${meeting.join_url}`);
}

async function cmdInfo(token, _creds, args) {
  if (!args[0]) { console.error('Usage: zoom-cli.js info <meeting_id>'); process.exit(1); }
  const id = validateMeetingId(args[0]);
  const m = await zoomGet(token, `/meetings/${id}`);
  console.log(JSON.stringify(m, null, 2));
}

async function cmdUpdate(token, _creds, args) {
  if (args.length < 3) {
    console.error('Usage: zoom-cli.js update <meeting_id> <start_time_ISO> <duration_minutes> [topic]');
    process.exit(1);
  }
  const [idRaw, startTime, durationRaw, topic] = args;
  const id = validateMeetingId(idRaw);
  validateISODateTime(startTime);
  const duration = validateDuration(durationRaw);

  const payload = { start_time: startTime, duration };
  if (topic) payload.topic = topic;

  await zoomPatch(token, `/meetings/${id}`, payload);
  console.log(`Meeting ${id} updated.`);
}

async function cmdDelete(token, _creds, args) {
  if (!args[0]) { console.error('Usage: zoom-cli.js delete <meeting_id>'); process.exit(1); }
  const id = validateMeetingId(args[0]);
  await zoomDelete(token, `/meetings/${id}`);
  console.log(`Meeting ${id} deleted.`);
}

// ── Entry point ───────────────────────────────────────────────────────────────

async function main() {
  const [,, command, ...args] = process.argv;

  const commands = { list: cmdList, create: cmdCreate, info: cmdInfo, update: cmdUpdate, delete: cmdDelete };

  if (!command || !commands[command]) {
    console.error(`Usage: zoom-cli.js <list|create|info|update|delete> [args...]`);
    process.exit(1);
  }

  const creds = loadCredentials();
  const token = await getAccessToken(creds);
  await commands[command](token, creds, args);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
