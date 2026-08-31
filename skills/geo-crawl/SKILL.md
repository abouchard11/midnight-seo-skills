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

**Canonical skill:** if `geo-crawl-audit/skill/SKILL.md` is on disk (sibling clone or `~/.claude/skills/geo-crawl-audit`), follow that file for Mode A / Mode B. This file is only the mount point and the suite handshake.

Public scan if the operator does not have the repo: https://readablebyai.com — treat it as Mode A lite. Logs still require Mode B on owned infrastructure.

## Route, do not duplicate

- Citation / mention matrix → `/geo` (only after this gate)
- Passages / snippets → `/aeo`
- Preferred Sources badge → `/preferred-source`
- GSC indexing → `/indexer`

## Step 1: Parse Domain

Extract the domain. Strip protocol, www, trailing slash, lowercase. Resolve against the MCP Routing Map. Portfolio runs iterate the roster.

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

## Step 3: Confirm in logs when required (Mode B)

Required when Mode A raises `BOT_DIFFERENTIAL`, `SLOW_TTFB`, or `TTFB_VARIANCE` on retrieval or user_fetch bots.

```bash
python3 scripts/drain_parser.py logs/*.ndjson --out ./audit-results --verify
```

Setup: `geo-crawl-audit/references/log-pipeline.md`. Vercel runtime logs alone miss edge/static bot hits.

No drain: print the finding as **UNCONFIRMED** and still STOP `/geo` citation work if the flag is CRITICAL on a retrieval bot. Do not invent log rows.

## Step 4: Suite handshake

Issue one verdict. Use flag codes from `geo-crawl-audit/references/interpreting.md` — do not redefine them.

| Verdict | When | What the rest of the suite may do |
|---|---|---|
| **STOP** | `CSR_SHELL`; `BOT_DIFFERENTIAL` on retrieval or user_fetch (even UNCONFIRMED); `ROBOTS_BLOCKS` on retrieval or user_fetch; baseline not a normal 200 (inconclusive) | No prompt matrix. No passage rewrite sold as GEO. Fix the gate. Re-probe. |
| **CONTINUE WITH FIXES** | `SLOW_TTFB` / `TTFB_VARIANCE`; `THIN_HTML`; `NO_SITEMAP` / `NO_ROBOTS`; training-only `ROBOTS_BLOCKS` | `/geo` and `/aeo` may run. First Recommended Action is the probe fix, not a new blog. |
| **CLEAR** | Score 85–100, no CRITICAL retrieval flags | `/geo` proceeds normally. |

Training-bot blocks (`GPTBot`, `ClaudeBot`, `Google-Extended`, …) are a rights choice. They do not by themselves STOP citation work. Say so.

`NO_LLMS_TXT` is a footnote. Never lead with it.

## Step 5: Output

Follow the Output Protocol from core.md:
1. Print the scorecard worst-first, then the STOP / CONTINUE / CLEAR verdict
2. Extract structured summary (include flag codes and whether Mode B ran)
3. Save to Graphiti with name `GEO Crawl — [domain]`

Do not paste a prompt-probe matrix here. That is `/geo` after CLEAR or CONTINUE WITH FIXES.
