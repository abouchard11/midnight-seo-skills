---
name: geo-crawl
description: Thin pointer to the ReadableByAI GEO crawl probe — whether AI crawlers can reach, fetch, and read a site before any citation work. Does not reimplement the probe.
when_to_use: Use when the user asks if ChatGPT, Claude, or Perplexity can see a site, whether a WAF is blocking AI bots, about 499s, robots.txt for GPTBot or OAI-SearchBot, CSR shells, or wants a GEO technical gate. Also the required preflight before /geo.
argument-hint: "<domain>"
---

# GEO Crawl — input gate

This skill does **not** own the probe. The engine, bot registry, log parser, and flag playbook live in [geo-crawl-audit](https://github.com/abouchard11/geo-crawl-audit) (ReadableByAI, [readablebyai.com](https://readablebyai.com)). Prefer engine SHA `de557923` or later (PR #3, 2026-08-31): RFC 9309 Allow/Disallow tie-break, failed-baseline scoring, CSR_SHELL scoped to the baseline body. `ROBOTS_BLOCKS` from before that merge is suspect.

Do not copy `geo_probe.py`, `drain_parser.py`, or `bots.json` into this repo. Do not invent a second robots.txt checklist. Run that skill, then translate the flags into a STOP / CONTINUE verdict for the rest of this suite.

**First:** Read `~/.claude/skills/seo-references/core.md`.

**Canonical skill:** if `geo-crawl-audit/skill/SKILL.md` is on disk (sibling clone or `~/.claude/skills/geo-crawl-audit`), follow that file for Mode A and for the origin-log parser. This file is only the mount point and the suite handshake. Prefer the **public** `geo-crawl-audit` skill over any private clone. Private clones can lag on honesty-clause wording.

Public scan if the operator does not have the repo: https://readablebyai.com — treat it as Mode A lite.

## Planes (do not collapse)

Two log instruments. Do not feed one into the other.

| Plane | Repo | What this skill may do |
|---|---|---|
| Engine | public `geo-crawl-audit` | Run `geo_probe.py` + `drain_parser.py`. Cite flag codes from `references/interpreting.md`. |
| Mode B parser | public `drain_parser.py` | Origin-class logs only: nginx/apache/LiteSpeed combined access logs, or a raw Vercel NDJSON export that still has `proxy.userAgent` and `proxy.clientIp`. |
| Drain product | public ReadableByAI | A **different** instrument. Hosted: [readablebyai.com/logs/hosted](https://readablebyai.com/logs/hosted) → `/api/drain/<key>`. Owner receiver: `https://drain.readablebyai.com/api/drain` (GET `ok`). Events: `rba_crawler_hit` / minimized `rba_benchmark_crawler_hit`. The receiver verifies IP in memory and **discards** UA, IP, and exact path. Never pipe those events into `drain_parser.py`. Never reconstruct a UA. Do **not** POST to `https://readablebyai.com/api/drain` (410 tombstone). Never copy drain keys or secrets. |
| Drain receiver source | private `geo-bot-drain` | Contained receiver behind `drain.readablebyai.com`. Pointer only. Never copy the receiver, secrets, or `ALLOWED_DOMAINS`. |
| Evidence store | private `readablebyai-evidence` | Pointer only. Never copy `index-1/`, outreach lists, notice archives, or raw probe JSON into this repo or into Graphiti. |
| Operator artifacts | private `hq` (`outputs/geo-*`) | May cite that a dated portfolio run exists. Do not paste the run. |
| Marketplace | private `alex-private-marketplace` | Not a GEO source. Do not install or duplicate desks from it. |

Private evidence is never public. A visibility flip on the site repo must not be able to publish Index mappings or outreach kits — that is why the evidence store is split.

## Route, do not duplicate

- Citation / mention matrix → `/geo` (only after this gate)
- Passages / snippets → `/aeo`
- Preferred Sources badge → `/preferred-source`
- GSC indexing → `/indexer`
- Entity name / sameAs → `/entity`

## Step 1: Parse Domain

Extract the domain. Strip protocol, www, trailing slash, lowercase. Resolve against the MCP Routing Map. Portfolio runs iterate the roster.

If the domain is not on the routing map, Mode A may still run. Log confirmation may run only on logs the operator owns or is authorized to retain. Do not ingest third-party contributor drains.

## Step 2: Run the probe (Mode A)

Locate `scripts/geo_probe.py` from a local `geo-crawl-audit` checkout at PR #3 or later. Prefer, in order:

1. `../geo-crawl-audit/scripts/geo_probe.py` relative to this suite
2. A path the operator already has on disk
3. Clone `https://github.com/abouchard11/geo-crawl-audit` if missing, then run

```bash
python3 scripts/geo_probe.py example.com --out ./audit-results
```

Read `geo_audit_report.md` and `geo_audit.json`. Apply the honesty clause from that repo: a simulated-UA differential means a bot-sensitive layer exists, not that the real crawler is blocked.

If the probe cannot run:
- Print `[SEO] geo-crawl-audit probe unavailable — clone https://github.com/abouchard11/geo-crawl-audit or scan https://readablebyai.com.`
- Do not fake flags.
- `/geo` may continue only if the operator explicitly accepts an unprobed run. Record that in the Graphiti summary.

`OAI-AdsBot` (OpenAI docs, `OAI-AdsBot/1.0`) is advertising verification for pages submitted as ChatGPT ads. Class: advertising. Registry: `category: advertising`, `probe: false`. It is not retrieval and not user_fetch. Blocking it does not STOP `/geo`.

Amazonbot is retrieval in the registry and publishes **no** IP range (`ip_ranges: null`). A Mode A Amazonbot differential cannot be vendor-range verified in either direction. Label identity **UNVERIFIABLE**. It is not a clean true positive.

## Step 3: Confirm when required — pick the instrument

Required when Mode A raises `BOT_DIFFERENTIAL`, `SLOW_TTFB`, or `TTFB_VARIANCE` on retrieval or user_fetch bots. Do not skip because a public scan looked clean. Name which instrument ran.

### Instrument 1 — Mode B (`drain_parser.py`)

Needs an **origin-logging** host. Combined access logs (LiteSpeed / nginx / apache) are the default class. A raw Vercel NDJSON export is origin-class only if UA and client IP are still on the row.

```bash
python3 scripts/drain_parser.py access.log --format combined --verify --out ./audit-results
python3 scripts/drain_parser.py logs/*.ndjson --out ./audit-results --verify
```

`--verify` is a no-op for bots with no published range (Amazonbot, several Anthropic tokens except the pinned ClaudeBot CIDR). Do not treat `verification=unknown` as confirmed identity.

Vercel runtime logs are not Mode B. Do not treat `vercel___get_runtime_logs` as origin logs.

LiteSpeed hosts (example: `htxpermitfix.com`) **are** the right class for this instrument. Minimized ReadableByAI drain events are the wrong class.

### Instrument 2 — ReadableByAI drain (not the parser)

Use when the host is already on the owner-portfolio drain (`drain.readablebyai.com`) or a customer-owned hosted drain. Query owned `rba_crawler_hit` or minimized `rba_benchmark_crawler_hit` events. Read `bot`, `verification`, `status_class` (and `verification_method` / `collection_basis` when present). Do not call `drain_parser.py` on those rows. Do not invent UA strings so the parser will accept them.

First owned result on this instrument (readablebyai.com, 2026-08-31, operator PostHog): CLEAR for retrieval. Verified 2xx from vendor ranges on googlebot, oai-searchbot, gptbot, chatgpt-user, bingbot, perplexitybot. Impostor populations stay in the dataset and do not flip CLEAR.

### Owned-log rule

1. Origin combined / raw NDJSON the operator exported — Instrument 1.
2. ReadableByAI drain events the operator already owns — Instrument 2.
3. Never raw rows from `readablebyai-evidence`.
4. Never a drain configured as **Projects: All**. Receiver excludes itself.
5. Never the tombstone at `readablebyai.com/api/drain` (HTTP 410).

No origin log and no owned RBA events: print **UNCONFIRMED** and still STOP `/geo` citation work if the flag is CRITICAL on a retrieval bot whose identity is vendor-verifiable. For Amazonbot / other `ip_ranges: null` tokens, keep the Mode A lead but do not sell it as a confirmed block.

## Step 4: Suite handshake

Issue one verdict. Use flag codes from `geo-crawl-audit/references/interpreting.md` — do not redefine them. Say which log instrument ran, or that neither did.

| Verdict | When | What the rest of the suite may do |
|---|---|---|
| **STOP** | `CSR_SHELL`; `BOT_DIFFERENTIAL` on retrieval or user_fetch when the bot has a published range or pinned CIDR (even UNCONFIRMED); `ROBOTS_BLOCKS` on retrieval or user_fetch from engine SHA `de557923`+; baseline not a normal 200 (inconclusive) | No prompt matrix. No passage rewrite sold as GEO. Fix the gate. Re-probe. |
| **CONTINUE WITH FIXES** | `SLOW_TTFB` / `TTFB_VARIANCE`; `THIN_HTML`; `NO_SITEMAP` / `NO_ROBOTS`; training-only `ROBOTS_BLOCKS`; Amazonbot-only differential with identity UNVERIFIABLE | `/geo` and `/aeo` may run. First Recommended Action is the probe fix or a Mode B origin-log pull, not a new blog. |
| **CLEAR** | Score 85–100, no CRITICAL retrieval flags — or Instrument 2 shows verified 2xx on retrieval tokens | `/geo` proceeds normally. |

Training-bot blocks (`GPTBot`, `ClaudeBot`, `Google-Extended`, …) are a rights choice. They do not by themselves STOP citation work. Say so.
Advertising-class tokens (`OAI-AdsBot`) do not STOP citation work.

`NO_LLMS_TXT` is a footnote. Never lead with it.

Pre-PR #3 `ROBOTS_BLOCKS` must be re-probed before it can STOP `/geo`.

## Step 5: Output

Follow the Output Protocol from core.md:
1. Print the scorecard worst-first, then the STOP / CONTINUE / CLEAR verdict
2. Extract structured summary (include flag codes, which log instrument ran, owned vs missing)
3. Draft Graphiti save with name `GEO Crawl — [domain]`, `group_id` from the MCP Routing Map. Suite methodology facts use `group_id=midnight-seo-skills`. Live `add_memory` is human/policy-closed. Episodes already in the write-ahead spool must not be re-drafted.

Do not paste a prompt-probe matrix here. That is `/geo` after CLEAR or CONTINUE WITH FIXES.
Do not paste Index probe bodies, notice lists, or drain secrets into the summary.
