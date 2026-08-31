---
name: geo-crawl
description: Thin pointer to the ReadableByAI GEO crawl probe — whether AI crawlers can reach, fetch, and read a site before any citation work. Does not reimplement the probe.
when_to_use: Use when the user asks if ChatGPT, Claude, or Perplexity can see a site, whether a WAF is blocking AI bots, about 499s, robots.txt for GPTBot or OAI-SearchBot, CSR shells, or wants a GEO technical gate. Also the required preflight before /geo.
argument-hint: "<domain>"
---

# GEO Crawl — input gate

This skill does **not** own the probe. The engine, bot registry, log parser, and flag playbook live in [geo-crawl-audit](https://github.com/abouchard11/geo-crawl-audit) (ReadableByAI, [readablebyai.com](https://readablebyai.com)).

Do not copy `geo_probe.py`, `drain_parser.py`, or `bots.json` into this repo. Do not invent a second robots.txt checklist. Run that skill, then translate the flags into a STOP / CONTINUE verdict for the rest of this suite.

**First:** Read `~/.claude/skills/seo-references/core.md`.

**Canonical skill:** if `geo-crawl-audit/skill/SKILL.md` is on disk (sibling clone or `~/.claude/skills/geo-crawl-audit`), follow that file for Mode A / Mode B. This file is only the mount point and the suite handshake. Prefer the **public** `geo-crawl-audit` skill over any private clone. Private clones can lag on honesty-clause wording.

Public scan if the operator does not have the repo: https://readablebyai.com — treat it as Mode A lite. Logs still require Mode B on owned infrastructure.

## Planes (do not collapse)

| Plane | Repo | What this skill may do |
|---|---|---|
| Engine | public `geo-crawl-audit` | Run `geo_probe.py` + `drain_parser.py`. Cite flag codes from `references/interpreting.md`. |
| Drain receiver | private `geo-bot-drain` | Point at setup + containment. Never copy the receiver, secrets, or `ALLOWED_DOMAINS` list into this public suite. |
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

If the domain is not on the routing map, Mode A may still run. Mode B may run only on logs the operator owns or is authorized to retain. Do not ingest third-party contributor drains.

## Step 2: Run the probe (Mode A)

Locate `scripts/geo_probe.py` from a local `geo-crawl-audit` checkout. Prefer, in order:

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

`OAI-AdsBot` (OpenAI docs, `OAI-AdsBot/1.0`) is advertising verification for pages submitted as ChatGPT ads. Class: advertising. It is not retrieval and not user_fetch. Blocking it does not STOP `/geo`. Probe it only after the engine registry lists it with `probe: false`. Registry UA refresh stays in `geo-crawl-audit` `bots.json`, not here.

## Step 3: Confirm in logs when required (Mode B)

Required when Mode A raises `BOT_DIFFERENTIAL`, `SLOW_TTFB`, or `TTFB_VARIANCE` on retrieval or user_fetch bots. Do not skip because a public scan looked clean.

Use the **public** parser. The private `geo-crawl-audit-internal` copy of `drain_parser.py` is the same engine SHA as of 2026-08-31 — do not fork a third copy into this suite.

```bash
python3 scripts/drain_parser.py logs/*.ndjson --out ./audit-results --verify
```

Setup: `geo-crawl-audit/references/log-pipeline.md`. Vercel runtime logs alone miss edge/static bot hits. Do not treat `vercel___get_runtime_logs` as Mode B.

### Owned-log rule

Mode B input is owned infrastructure only:

1. Operator-exported drain files (Vercel NDJSON / combined access logs) for domains on the routing map or otherwise authorized.
2. Minimized events from the private drain receiver after they have already dropped raw IP, path, UA, and visitor id.
3. Never raw rows from `readablebyai-evidence` (those are Index / outreach evidence, not a live drain).
4. Never a drain configured as **Projects: All**. The receiver must exclude itself. If the receiver would log its own project, treat that as a containment fault and stop the parse.

No drain: print the finding as **UNCONFIRMED** and still STOP `/geo` citation work if the flag is CRITICAL on a retrieval bot. Do not invent log rows. Do not backfill from public Index reports.

## Step 4: Suite handshake

Issue one verdict. Use flag codes from `geo-crawl-audit/references/interpreting.md` — do not redefine them.

| Verdict | When | What the rest of the suite may do |
|---|---|---|
| **STOP** | `CSR_SHELL`; `BOT_DIFFERENTIAL` on retrieval or user_fetch (even UNCONFIRMED); `ROBOTS_BLOCKS` on retrieval or user_fetch; baseline not a normal 200 (inconclusive) | No prompt matrix. No passage rewrite sold as GEO. Fix the gate. Re-probe. |
| **CONTINUE WITH FIXES** | `SLOW_TTFB` / `TTFB_VARIANCE`; `THIN_HTML`; `NO_SITEMAP` / `NO_ROBOTS`; training-only `ROBOTS_BLOCKS` | `/geo` and `/aeo` may run. First Recommended Action is the probe fix, not a new blog. |
| **CLEAR** | Score 85–100, no CRITICAL retrieval flags | `/geo` proceeds normally. |

Training-bot blocks (`GPTBot`, `ClaudeBot`, `Google-Extended`, …) are a rights choice. They do not by themselves STOP citation work. Say so.
Advertising-class tokens (`OAI-AdsBot`) do not STOP citation work.

`NO_LLMS_TXT` is a footnote. Never lead with it.

## Step 5: Output

Follow the Output Protocol from core.md:
1. Print the scorecard worst-first, then the STOP / CONTINUE / CLEAR verdict
2. Extract structured summary (include flag codes, whether Mode B ran, and whether logs were owned vs missing)
3. Draft Graphiti save with name `GEO Crawl — [domain]`, `group_id` from the MCP Routing Map. Suite methodology facts use `group_id=midnight-seo-skills`. Live `add_memory` is human/policy-closed.

Do not paste a prompt-probe matrix here. That is `/geo` after CLEAR or CONTINUE WITH FIXES.
Do not paste Index probe bodies, notice lists, or drain secrets into the summary.
