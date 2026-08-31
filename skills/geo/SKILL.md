---
name: geo
description: Generative Engine Optimization — get the brand cited inside ChatGPT, Perplexity, Gemini, Claude, and Google AI Mode answers rather than just ranked on a SERP
when_to_use: Use when the user asks about GEO, generative engine optimization, AI citations, ChatGPT mentions, Perplexity citations, share of model, AI visibility, or whether an LLM recommends the brand. Also when measuring or improving citation presence across generative engines.
argument-hint: "<domain>"
---

# GEO — Generative Engine Optimization

**First:** Read `~/.claude/skills/seo-references/core.md`. Apply the methodology and voice to all output. Purchase-intent pages stay the 80/20. GEO is a citation layer on those pages, not a license to stand up a "what is" blog.

**Also read:**
- `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool names
- `~/.claude/skills/seo-references/sturm-shorts.md` for the dated operator notes this skill encodes
- Companion research: https://github.com/abouchard11/ai-citation-patterns — engine-by-engine citation behavior. Do not copy that file into the playbook. Use it as the evidence desk.

Unit of success: a **citation, brand mention, or recommendation** inside a synthesized answer. Not a blue-link rank. Not a featured snippet (that is `/aeo`).

Route, do not duplicate:
- Preferred Sources badge → `/preferred-source`
- Extractable passages / snippets / PAA → `/aeo`
- Referring-domain work → `/hunter` then `/kilo`
- Indexing → `/indexer`

## Do not do this

- Do not put "this page is optimized for AI assistants and LLM search, not human marketing" (or any cousin) at the top of a page. Models already filter "SEO spam" in the thinking trace. Admitting the page is for machines is a self-report. Write for a buyer. Let the structure do the extractability work.
- Do not ship `llms.txt` as a ranking lever. Google ignores it. Treat it as optional agent-hygiene only.
- Do not scrape Google SERPs as a primary data path. The `/goto` redirect plus the retired `num=100` parameter broke that class of tracker. Use GSC, Semrush, and first-party AI-visibility tools.
- Do not invent an eight-site directory list from memory. If the personal-site submission list from the Sturm short is needed, pull it from the video itself (see sturm-shorts.md). Then execute through `/kilo`.

## Step 1: Parse Domain

Extract the domain. Strip protocol, www, trailing slash, lowercase. Resolve against the MCP Routing Map.

Name the entity the engines should learn: brand string, legal name, product names, founder name if the property is personal. GEO fails when the page talks about "we" and never writes the proper noun.

## Step 2: Pull Live Data

**Semrush (PRIMARY):**
1. `mcp__semrush__execute_report` — Domain Overview (database=us). Authority + organic baseline.
2. `mcp__semrush__execute_report` — Referring Domains, display_limit=20. ChatGPT retrieval is gated hard by referring-domain count. Note the RD total in the verdict.
3. `mcp__semrush__execute_report` — Domain Organic Search Keywords, display_limit=30. Separate branded vs unbranded. GEO probes use both.

**GSC (ENRICHMENT):**
4. `mcp__gscServer__get_search_analytics` — last 28 days, dimensions=[query], rowLimit=50. Queries that already impress are the first prompt set.

**GA4 (ENRICHMENT):**
5. `mcp__google-analytics__run_report` — sessions by landing page, last 28 days. Pages that already convert are the pages that should become citable, not a new explainer silo.

**CamoFox (ENRICHMENT):**
6. Snapshot the homepage + the #1 converting page. Check: brand name in H1 / first sentence, server-rendered facts (price, specs, city, phone), author byline, outbound citations, FAQ block, schema present, no "for LLMs" disclosure. If CamoFox is down: `[SEO] CamoFox unavailable — on-page extractability check skipped.`

**Optional AI-visibility tool (ENRICHMENT, never PRIMARY):**
OpenSEO ([every-app/open-seo](https://github.com/every-app/open-seo), hosted [openseo.so](https://openseo.so)) tracks whether ChatGPT or Google AI Overviews mention the brand and exposes MCP/skills for agents. Use it if connected. Do not replace Semrush or GSC with it. Self-host or $10/mo hosted is an operator choice, not a recommendation to cancel the primary stack.

If a source fails, print the `[SEO]` warning from core.md and continue.

## Step 3: Prompt Probe Set

Build 8–12 prompts the engines will actually be asked. Split:

| Bucket | Count | Pattern |
|---|---|---|
| Category recommend | 3 | "best [vertical] in [city / for X]" |
| Comparison | 2 | "[brand] vs [competitor]" |
| Entity | 2 | "what is [brand]", "who makes [product]" |
| Money | 2 | price / "hire [vertical] in [city]" / availability |
| Correction | 1–3 | the wrong fact a model already says |

Run each prompt against whatever surfaces the operator can reach this session (ChatGPT Search, Perplexity, Gemini, Claude with web search, Google AI Mode / AI Overviews). Repeat ChatGPT prompts — backend switching makes a single snapshot unreliable.

Score each surface per prompt:

| Score | Meaning |
|---|---|
| **CITED** | Brand or URL named with a source link |
| **MENTIONED** | Brand named, no link |
| **ABSENT** | Competitors present, we are not |
| **WRONG** | Hallucinated fact, dead URL, or wrong city / price |
| **UNTESTED** | Surface not reachable this run |

## Step 4: Generate the GEO Playbook

**Section 1 — Verdict**
One paragraph. Are we in the answer, next to the answer, or invisible? Name the highest-leverage missing citation.

**Section 2 — Citation matrix**
Table: prompt × surface × score × who got cited instead. No theater. Empty cells stay UNTESTED.

**Section 3 — Entity and off-site pool**
Engines fan out to the sources they already trust. List the third-party pages that should mention this brand (G2/Capterra/Clutch if software, GBP + local citations if local-service, Wikipedia / Wikidata only if notable, Reddit threads that already rank, YouTube titles + transcripts). Route the actual link asks to `/hunter` and `/kilo`.

Personal-site / founder-entity properties: quality referring domains help both classic SEO and AI appearance, and they are one path toward a knowledge panel. Do not wallpaper generic directories onto a local-service money site.

**Section 4 — On-page citability (BOFU pages only)**
For the top 2–3 converting URLs, specify the smallest patch that makes a passage reusable:
- Proper noun in the first sentence
- One standalone 134–167 word passage that answers the category prompt without the rest of the page
- One dated statistic or price with an outbound source
- Comparison table only if the page already competes on "vs" queries
- FAQ answers as atomic paragraphs, not a new /blog
- Server-rendered facts — prices and specs must not live only in JS

Keep pages at core.md length caps. GEO is extractability, not word count.

**Section 5 — Crawler hygiene**
Check `robots.txt` intent for the bots the operator wants citing them: `OAI-SearchBot`, `ChatGPT-User`, `GPTBot` (training, separate), `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`, `Claude-User`, `ClaudeBot`, `Google-Extended` (training opt-out only — Googlebot is Gemini / AIO visibility). Do not block search bots while "doing GEO." Note WAF allowlists for Perplexity IPs if fetches fail.

**Section 6 — Measurement**
What to re-run in 28 days: the same prompt matrix, RD count, branded GSC queries, OpenSEO AI-visibility if connected. Do not use scraped Google rank-tracker URL paths as proof — `/goto` ate those.

**Section 7 — What this will not do**
- Will not replace Map Pack for local
- Will not buy position one
- Will not make a login-walled tool citable
- Will not reward a page that announces it is spam for machines

## Step 5: Output

Follow the Output Protocol from core.md:
1. Print the full GEO playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `GEO — [domain]`

In Recommended Actions, first item is the single prompt + surface where a one-page patch would most likely flip ABSENT → CITED this month.
