# Core — SEO Methodology & Portfolio Reference

## 1. Methodology

Core operating principles for all SEO skill output in this repo:

- **Bottom-of-funnel focus.** Target purchase-intent keywords only. Every page targets a searcher who KNOWS WHAT THEY WANT and is ready to hire/buy/call.
- **Short, high-intent pages.** Bottom-of-funnel pages: **400-500 words MAX**. Not 2,000-3,000 word blog posts. Hub pages (800-1000 words) and Sub-Hub pages (600-800 words) are structural — they organize the silo as navigation and internal linking anchors.
- **Above-the-fold clarity.** Every page needs a clear H1 + 3-5 sentence intro + CTA button. The CTA must be visible without scrolling.
- **Link quality over volume.** A few topical, niche-relevant backlinks beat hundreds of generic ones.
- **Blog SEO is declining.** AI Overviews reduce informational blog CTR by 34%. Purchase-intent pages are the counter-strategy.
- **GEO and AEO sit on those pages.** GEO (`/geo`) optimizes for a citation or brand mention inside a synthesized answer. AEO (`/aeo`) optimizes for the extracted passage (snippet, PAA, voice, short AIO block). Neither skill is permission to stand up a "what is" blog or to label a page "for LLMs, not humans."
- **80/20 focus.** 80% of results come from 20% of effort. The 20% that matters most: keyword in page title, meta description, URL slug, H1, and first sentence. Get these right and most technical SEO is handled.
- **Data-driven validation.** Back every recommendation with specific data pulled from connected tools. No vague claims. Do not scrape Google SERP URLs in bulk after the `/goto` redirect change — GSC is first-party truth.

**Anti-patterns (never recommend these):**
- "What is..." or "How to..." informational pages
- 2,000+ word comprehensive guides
- Generic link building campaigns
- Vanity metrics (pageviews, time on site without conversion context)
- Content calendars that prioritize volume over purchase intent
- Ledes or hidden text that admit the page exists for LLM manipulation
- Treating `llms.txt` as a ranking or citation lever

Parts of the bottom-of-funnel approach here were informed by Edward Sturm's publicly taught Compact Keywords framework (edwardsturm.com). Dated notes from specific shorts live in `sturm-shorts.md`.

## 2. Portfolio Configuration

Replace the placeholder rows below with your own portfolio properties before running these skills.

### A. Domain Roster

| ID | Name | Domain | Tier | CPC | Volume | Type | Status | Value |
|----|------|--------|------|-----|--------|------|--------|-------|
| 1 | Example Site | example.com | apex | {{CPC}} | {{VOLUME}} | Local Service | LIVE | $$$ |
| 2 | Example Site Two | example2.com | niche | {{CPC}} | {{VOLUME}} | E-commerce | LIVE | $$ |

### B. MCP Routing Map

Use this table to resolve domain input to MCP tool parameters and Graphiti group_id. Only domains listed here have live analytics properties.

| Domain | group_id | GSC Property | GA4 Property | Semrush Domain |
|--------|----------|-------------|-------------|----------------|
| example.com | example | sc-domain:example.com | properties/{{GA4_PROPERTY_ID}} | example.com |
| example2.com | example2 | sc-domain:example2.com | properties/{{GA4_PROPERTY_ID}} | example2.com |

### C. Domain Resolution

When a skill receives a domain argument:
1. Strip protocol (https://), www., trailing slashes, and lowercase
2. Look up in the MCP Routing Map above
3. If found: use the row's group_id, GSC Property, GA4 Property, and Semrush Domain
4. If NOT found: warn the user that the domain is not in the portfolio map. Ask if they want to proceed with Semrush data only (no GSC/GA4).

### D. Local vs. Non-Local Domains

Optionally track which domains in your portfolio are local service businesses (eligible for Map Pack / local SEO) versus national, e-commerce, or content-driven properties, so skills know when local SEO tactics apply.

## 3. Output Protocol

Every skill follows this exact output sequence:

### Step A: Print Playbook
Print the full generated playbook to terminal in markdown format. Use H2 headers for major sections. Include all data, recommendations, and action items.

### Step B: Extract Summary
Extract key findings into a structured summary with these exact sections:

```
## Key Findings
- [bullet list of 5-10 actionable facts discovered]

## Metrics
- [data points pulled from MCP sources with values]

## Recommended Actions
1. [numbered next steps, most impactful first]

## Data Sources Used
- Semrush: [available/unavailable — what was pulled]
- GSC: [available/unavailable — what was pulled]
- GA4: [available/unavailable — what was pulled]
```

### Step C: Save to Graphiti
Call `mcp__graphiti__add_memory` with:
- `name`: deterministic format `[Skill Name] — [domain]` (e.g., "Topical Map — example.com"). For portfolio-wide skills, use `[Skill Name] — Portfolio`.
- `group_id`: resolved from MCP Routing Map, or `global` for portfolio-wide skills
- `source`: "text"
- `source_description`: "SEO skill output — YYYY-MM-DD"
- `episode_body`: the structured summary from Step B

Before saving, search Graphiti with `mcp__graphiti__search_nodes` for the same `name` to check for prior runs. If found, note in the episode_body that this is an update to a prior analysis.

## 4. MCP Failure Handling

**Data source priority:**
- **Semrush** = PRIMARY (mandatory for quality). If Semrush fails, warn: `[SEO] Semrush unavailable — generating from methodology only. Results will be less specific.`
- **GSC** = ENRICHMENT (optional). If GSC fails, warn: `[SEO] GSC data unavailable — proceeding with Semrush data.` Exception: `/aeo` treats GSC as PRIMARY because snippet inventory is first-party query data.
- **GA4** = ENRICHMENT (optional). If GA4 fails, warn: `[SEO] GA4 data unavailable — proceeding with Semrush data.`

**Date windows:** All data pulls use "last 28 days" unless noted. GSC has ~3-day latency, GA4 ~24-48h, Semrush ~monthly refresh.

**Failure sequence:**
1. Attempt each MCP pull
2. On failure, print the appropriate warning above
3. Generate with whatever data was successfully pulled
4. In the Graphiti save (Data Sources Used section), note which sources returned data vs. were unavailable

## 5. Stealth Browser (CamoFox)

CamoFox MCP is a stealth browser available as an MCP server (`camofox` in ~/.claude.json). It provides 46 anti-detection browser tools powered by Camoufox (Firefox fork with engine-level fingerprint spoofing). It can access pages behind Cloudflare, DataDome, PerimeterX, and other anti-bot systems that block standard crawlers.

**Architecture:** Docker container `camofox-browser` on port 9377 + `camofox-mcp` MCP bridge (stdio via npx).

### When to use CamoFox in SEO skills

Use CamoFox when a skill needs to see a **competitor's actual page content** that Semrush/GSC data alone can't provide. Semrush gives you keywords and rankings. CamoFox gives you what's actually on the page.

| Skill | CamoFox use case | When to invoke |
|-------|-----------------|----------------|
| `/topical-map` | Verify competitor above-the-fold CTAs, H1s, page structure | When analyzing ranking gaps — navigate to top competitor pages to see their content strategy |
| `/hunter` | Scrape competitor pages to find their link placements, outbound links, and content that earned links | When building the competitive link gap analysis |
| `/kilo` | Validate link targets are live, find contact info, verify broken links on competitor-linking pages | When building executable link acquisition deliverables — scrape the actual pages that link to competitors to verify targets and find pitch angles |
| `/parasite` | Scrape Reddit/Medium/Quora pages currently ranking for target keywords to analyze content format, engagement, and platform norms | When identifying what parasite content format works for each platform — see what's actually ranking |
| `/whale` | Check what's currently live on candidate domain names | When validating whether a domain is parked, active, or expired |
| `/signal` | Verify social posts and profile pages are rendering correctly after posting | Optional — only if amplification verification is requested |
| `/preferred-source` | Confirm `publisher.js` / the preferred-source div is already on the live host | After a SHIP or MAYBE verdict — skip entirely on SKIP hosts |
| `/geo` | Confirm brand-in-first-sentence, SSR facts, no LLM-disclaimer lede, schema present | Homepage + #1 converting page. Do not bulk-harvest Google `/goto` URLs |
| `/aeo` | Snapshot our page passage + one human-paced SERP look at the current snippet owner | Only the target URL and one query. No `/goto` hammering |

**Skills that do NOT need CamoFox:** `neural-audit` (API data only), `ga4` (GA4 event audit), `indexer` (GSC data), `map-flap` (GBP/local strategy from API data).

### How to use CamoFox in a skill

1. **Check availability:** Look for `camofox` tools in the deferred tools list at session start. If not present, skip CamoFox steps and note in output: `[SEO] CamoFox stealth browser not available — using API data only.`
2. **Health check:** Call the CamoFox health tool to verify the browser server is running.
3. **Navigate:** Use CamoFox navigate tool to load a competitor URL.
4. **Snapshot:** Use CamoFox snapshot tool to capture the page's accessibility tree (text content, headings, links, CTAs).
5. **Extract:** Parse the snapshot for the specific data the skill needs (H1, CTA text, outbound links, page structure).

### CamoFox as ENRICHMENT, not PRIMARY

CamoFox is always **optional enrichment**, never mandatory. If the Docker container is stopped or the MCP server isn't connected, every skill must still work using Semrush/GSC/GA4 data alone. The failure handling follows the same pattern as GSC/GA4:
- If CamoFox is unavailable: `[SEO] CamoFox stealth browser unavailable — competitor page analysis skipped.`
- In the Graphiti summary, note under Data Sources Used: `CamoFox: [available/unavailable — what was scraped]`
