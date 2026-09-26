#!/usr/bin/env node
/**
 * Poll Stripe Checkout Sessions (READ-ONLY) and email GEO Pro Pack delivery.
 *
 *   node scripts/poll-payments.mjs            # dry-run (default)
 *   node scripts/poll-payments.mjs --dry-run  # same
 *   node scripts/poll-payments.mjs --send     # Resend + append ledger + commit/push
 *   node scripts/poll-payments.mjs --selftest # license format/determinism only
 *
 * Stripe: `stripe checkout sessions list --live` when the CLI is logged in;
 * falls back to GET /v1/checkout/sessions with STRIPE_SECRET_KEY. Never writes
 * to Stripe.
 *
 * Resend From: support@readablebyai.com (readablebyai.com is the verified
 * Resend domain). midnightdev.dev is NOT verified in Resend — do not send
 * From support@midnightdev.dev until it is. Reply-To is support@midnightdev.dev.
 *
 * Env: STRIPE_SECRET_KEY (fallback), RESEND_API_KEY, LICENSE_SECRET (32+ chars).
 * Optional: RESEND_FROM, THANKS_BASE_URL.
 */
import { createHmac } from "node:crypto";
import { execFileSync } from "node:child_process";
import {
  appendFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const LEDGER = join(ROOT, "data", "fulfillment-ledger.jsonl");
const THANKS_BASE =
  process.env.THANKS_BASE_URL ?? "https://midnightdev.dev/geo-pack/thanks";
const FROM =
  process.env.RESEND_FROM ??
  "Midnight GEO Pro Pack <support@readablebyai.com>";
const REPLY_TO = "support@midnightdev.dev";
const PACK_AMOUNT = 9900;
const SKU = "midnight-geo-pro-v1";
const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
const LICENSE_RE =
  /^MDGP-[A-Z2-7]{4}-[A-Z2-7]{4}-[A-Z2-7]{4}-[A-Z2-7]{4}$/;

const argv = new Set(process.argv.slice(2));
const DRY_RUN = !argv.has("--send");
const SELFTEST = argv.has("--selftest");

function base32Encode(bytes) {
  let bits = 0;
  let value = 0;
  let output = "";
  for (const byte of bytes) {
    value = (value << 8) | byte;
    bits += 8;
    while (bits >= 5) {
      output += ALPHABET[(value >>> (bits - 5)) & 31];
      bits -= 5;
    }
  }
  if (bits > 0) {
    output += ALPHABET[(value << (5 - bits)) & 31];
  }
  return output;
}

/** Keep in sync with midnightdev src/lib/geo-pack/license.ts */
export function deriveLicenseKey(sessionId, secret) {
  const mac = createHmac("sha256", secret).update(sessionId, "utf8").digest();
  const raw = base32Encode(mac).slice(0, 16);
  const grouped = raw.match(/.{1,4}/g)?.join("-") ?? raw;
  return `MDGP-${grouped}`;
}

function selftest() {
  const secret = "test-license-secret-do-not-use-in-prod!!";
  const session = "cs_test_session_123";
  const a = deriveLicenseKey(session, secret);
  const b = deriveLicenseKey(session, secret);
  const c = deriveLicenseKey(session + "x", secret);
  if (a !== b) throw new Error("license not deterministic");
  if (a === c) throw new Error("license not session-bound");
  if (!LICENSE_RE.test(a)) throw new Error(`bad format: ${a}`);
  console.log("selftest ok", a);
}

function loadLedgerIds() {
  if (!existsSync(LEDGER)) return new Set();
  const ids = new Set();
  for (const line of readFileSync(LEDGER, "utf8").split("\n")) {
    if (!line.trim()) continue;
    try {
      const row = JSON.parse(line);
      if (row.session_id) ids.add(row.session_id);
    } catch {
      // skip malformed
    }
  }
  return ids;
}

function isGeoPackSession(s) {
  if (s?.payment_status !== "paid") return false;
  if (s?.metadata?.sku === SKU) return true;
  return s?.amount_total === PACK_AMOUNT && (s?.currency ?? "usd") === "usd";
}

function sessionEmail(s) {
  return s?.customer_details?.email || s?.customer_email || null;
}

function listSessionsViaCli() {
  const raw = execFileSync(
    "stripe",
    ["checkout", "sessions", "list", "--live", "--limit", "100"],
    { encoding: "utf8", timeout: 60_000 },
  );
  const start = raw.indexOf("{");
  if (start < 0) throw new Error("stripe CLI returned no JSON");
  const parsed = JSON.parse(raw.slice(start));
  return parsed.data ?? parsed;
}

async function listSessionsViaRest() {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    throw new Error(
      "No stripe CLI list and STRIPE_SECRET_KEY is unset (read-only retrieve/list only)",
    );
  }
  const res = await fetch(
    "https://api.stripe.com/v1/checkout/sessions?limit=100",
    { headers: { Authorization: `Bearer ${key}` } },
  );
  const body = await res.json();
  if (!res.ok) {
    throw new Error("Stripe list failed");
  }
  return body.data ?? [];
}

async function listPaidSessions() {
  try {
    return listSessionsViaCli();
  } catch {
    return listSessionsViaRest();
  }
}

function emailText({ email, license, thanksUrl }) {
  return `You're licensed for Midnight GEO Pro Pack (one seat).

Download + license page (bookmark this; it always serves the latest zip for 12 months from purchase):
${thanksUrl}

License key: ${license}

Install:
1. Unzip the pack.
2. cp -R skills/* ~/.claude/skills/  (or ~/.hermes/skills/)
3. Probe your domain — in Claude Code, /geo yourdomain.com — then fix and re-probe.

Support: ${REPLY_TO} — one clarification round after you've actually run a skill.
Do not reply to this From address if it is not ${REPLY_TO}; use Reply-To / ${REPLY_TO}.

— Alex / MidnightDev
`;
}

async function sendResend({ to, license, thanksUrl }) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) throw new Error("RESEND_API_KEY missing");
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM,
      to: [to],
      reply_to: REPLY_TO,
      subject: "Your Midnight GEO Pro Pack — download and license",
      text: emailText({ email: to, license, thanksUrl }),
    }),
  });
  const body = await res.json();
  if (!res.ok) {
    throw new Error("Resend send failed");
  }
  return body.id ?? null;
}

function appendLedger(row) {
  mkdirSync(dirname(LEDGER), { recursive: true });
  appendFileSync(LEDGER, `${JSON.stringify(row)}\n`, "utf8");
}

function commitAndPushLedger(sessionId) {
  try {
    execFileSync("git", ["add", "data/fulfillment-ledger.jsonl"], {
      cwd: ROOT,
    });
    execFileSync(
      "git",
      [
        "commit",
        "-m",
        `fulfillment: geo-pack delivery ${sessionId}`,
      ],
      { cwd: ROOT },
    );
    execFileSync("git", ["push"], { cwd: ROOT });
  } catch (err) {
    console.error("ledger git commit/push skipped or failed (non-fatal)");
    if (process.env.DEBUG_POLLER) {
      console.error(err);
    }
  }
}

async function main() {
  if (SELFTEST) {
    selftest();
    return;
  }

  const secret = process.env.LICENSE_SECRET ?? "";
  if (!DRY_RUN && secret.length < 32) {
    throw new Error("LICENSE_SECRET must be 32+ chars to send");
  }

  const seen = loadLedgerIds();
  const sessions = await listPaidSessions();
  const fresh = (Array.isArray(sessions) ? sessions : []).filter(
    (s) => isGeoPackSession(s) && s.id && !seen.has(s.id),
  );

  console.log(
    DRY_RUN ? "dry-run" : "send",
    "candidates",
    fresh.length,
    "ledger",
    seen.size,
  );

  for (const s of fresh) {
    const email = sessionEmail(s);
    const license =
      secret.length >= 32
        ? deriveLicenseKey(s.id, secret)
        : "(set LICENSE_SECRET to derive)";
    const thanksUrl = `${THANKS_BASE}?session_id=${encodeURIComponent(s.id)}`;
    const preview = {
      session_id: s.id,
      email,
      amount: s.amount_total,
      license,
      thanksUrl,
      from: FROM,
      reply_to: REPLY_TO,
    };
    if (DRY_RUN) {
      console.log("WOULD send", JSON.stringify(preview));
      continue;
    }
    if (!email) {
      console.error("skip — no email", s.id);
      continue;
    }
    const resendId = await sendResend({
      to: email,
      license,
      thanksUrl,
    });
    const row = {
      session_id: s.id,
      email,
      amount: s.amount_total,
      currency: s.currency ?? "usd",
      license,
      sent_at: new Date().toISOString(),
      resend_id: resendId,
    };
    appendLedger(row);
    commitAndPushLedger(s.id);
    console.log("sent", s.id);
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : "poller failed");
  process.exit(1);
});
