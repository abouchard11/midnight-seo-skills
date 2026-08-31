---
name: aeo
description: Answer Engine Optimization — make a page the extractable answer for featured snippets, People Also Ask, voice, and the short block inside AI Overviews
when_to_use: Use when the user asks about AEO, answer engine optimization, featured snippets, People Also Ask, voice answers, passage extraction, FAQ schema, or how to become the sentence Google or an assistant reads aloud. Distinct from GEO (citations inside a synthesized answer).
argument-hint: "<domain>"
---

# AEO — Answer Engine Optimization

**First:** Read `~/.claude/skills/seo-references/core.md`. Apply the methodology and voice to all output. AEO lives on purchase-intent pages. It is not a program for spawning "what is" articles so a snippet has somewhere to live.

**Also read:**
- `~/.claude/skills/seo-references/data-pull-patterns.md`
- `~/.claude/skills/seo-references/sturm-shorts.md`
- Companion research: https://github.com/abouchard11/ai-citation-patterns — passage length, schema, and AIO overlap numbers. Do not dump the research file into the playbook.

Unit of success: the **extracted passage**. Featured snippet, PAA answer, voice response, or the short sentence an AI Overview lifts. GEO (`/geo`) owns brand mentions and citations inside a multi-source synthesis. If the user wants both, run AEO on the page structure and GEO on the prompt matrix.

Route, do not duplicate:
- Preferred Sources frequency badge on AIO / AI Mode / Discover / Top Stories → `/preferred-source` (SHIP / MAYBE / SKIP first)
- Citation share across ChatGPT / Perplexity / Claude → `/geo`
- Links → `/hunter` then `/kilo`
- Indexing → `/indexer`

## Do not do this

- Do not label the page "optimized for AI assistants and LLM search, not human marketing." That line is a confession. Assistants already say "filtering out SEO spam" in the thinking phase. Write the answer a buyer would trust.
- Do not recommend a new informational blog so schema has a home. Put one question + one 40–60 word answer on the money page that already ranks.
- Do not treat `llms.txt` or hidden LLM-only blocks as an AEO tactic. Google has said normal SEO works; Danny Sullivan warned against chunking pages "for LLMs."
- Do not scrape live SERP snippet HTML through Google `/goto` redirects to prove a win. Use GSC appearance data and a CamoFox snapshot of the result the operator is allowed to load like a person.

## Step 1: Parse Domain

Extract the domain. Strip protocol, www, trailing slash, lowercase. Resolve against the MCP Routing Map. Flag local-service vs national so Map Pack is not sacrificed for a snippet vanity play.

## Step 2: Pull Live Data

**GSC (PRIMARY for AEO):**
1. `mcp__gscServer__get_search_analytics` — last 28 days, dimensions=[query, page], rowLimit=50. Sort by impressions. These queries are the answer inventory.
2. Same call filtered or noted for queries that look like questions (who / what / where / when / how much / near me / vs). Those are snippet and PAA candidates.

**Semrush (ENRICHMENT):**
3. `mcp__semrush__execute_report` — Domain Organic Search Keywords, display_limit=30. Note SERP features where the tool exposes them (featured snippet, PAA, AIO).
4. For the top 3 question-shaped keywords, `mcp__semrush__execute_report` — Organic Results, display_limit=10. Who currently owns the answer box.

**GA4 (ENRICHMENT):**
5. `mcp__google-analytics__run_report` — top landing pages by sessions, last 28 days. Snippet work goes on pages that already take traffic, not on a draft URL.

**CamoFox (ENRICHMENT):**
6. Load the #1 GSC page. Snapshot H1, first 150 words, FAQ headings, table presence, schema in raw HTML (view-source if needed), CTA above the fold. Optional: load the Google result for one target query **as a person would** — do not hammer `/goto` links. If CamoFox is down: `[SEO] CamoFox unavailable — snippet-owner snapshot skipped.`

If a source fails, print the `[SEO]` warning from core.md and continue.

## Step 3: Answer inventory

Build a table of at most 10 queries:

| Query | Intent | Current URL | Impressions | Position | Snippet owner | Our passage exists? | Action |
|---|---|---|---|---|---|---|---|

Prioritize:
1. High impressions, position 4–12, question-shaped, page already converts
2. "How much" / price / timeline / city + service — these stay BOFU
3. Drop pure "what is [generic noun]" unless that noun **is the offer**

## Step 4: Generate the AEO Playbook

**Section 1 — Verdict**
Which one query should own the next engineering hour. If the domain has no question-shaped impressions on a money page, say so and stop — do not invent a blog calendar.

**Section 2 — Passage spec (one page at a time)**
For each chosen URL + query, write the exact block the operator should paste:

- **Lead answer:** 40–60 words, first two sentences of the relevant section. Direct SVO. No throat-clearing.
- **Expandable passage:** 134–167 words total for Google AIO extraction. Atomic. Stands alone if the rest of the page is dropped.
- **H2:** the query in question form only when the page is already about that job. Do not tack five unrelated FAQs onto a service page.
- **Table or numbered list:** only if the query is comparison, steps, or pricing tiers.
- **Schema:** FAQPage or Product / LocalBusiness / Service JSON-LD that mirrors visible text. Never schema-only answers.

Stay inside core.md word caps. If the page is already at 500 words, replace a weak paragraph — do not append.

**Section 3 — SERP feature honesty**
- Featured snippet and PAA are passage contests. Winning them does not require more backlinks than the current owner if the passage is cleaner — but a zero-RD new domain still loses most AIO slots. Say which case this is.
- AI Overviews now show Preferred Sources labels. That is frequency for people who opted in, not a snippet override. Point to `/preferred-source` with a fit verdict, do not paste `publisher.js` here.
- Voice assistants read the same short answer. Write it so it can be spoken without the table.

**Section 4 — Anti-spam**
Reject any draft that:
- Announces machine-optimization in the lede
- Lists the operator's own product as "#1" inside a fake roundup on their own domain and expects an assistant to treat it as a third-party ranking
- Hides the answer below 800 words of preamble

**Section 5 — Measurement**
Re-check in 28 days via GSC (impressions + position for the query set) and one manual SERP look. Do not treat Ahrefs/Semrush URL-path loss after Google's `/goto` change as "we lost the snippet." Confirm on the live result.

## Step 5: Output

Follow the Output Protocol from core.md:
1. Print the full AEO playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `AEO — [domain]`

In Recommended Actions, first item is the single passage to ship, with the pasted copy included so the operator does not have to rewrite it.
