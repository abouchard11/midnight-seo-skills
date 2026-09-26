---
name: topical-map
description: Generate a topical map — Hub/Sub-Hub/Long-tail silo grounded in live GSC + Semrush data
when_to_use: Use when planning content architecture for a domain, creating a content silo, or deciding what pages to build next. Also when the user asks about site structure, page hierarchy, keyword mapping, or "what pages should I build."
argument-hint: "<domain>"
---

# Topical Mapper

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Step 1: Parse Domain

Extract the domain from the user's argument. Resolve it against the MCP Routing Map in core.md:
- Strip protocol, www, trailing slashes, lowercase
- Look up group_id, GSC property, GA4 property, Semrush domain
- If domain not in map, warn and ask if user wants to proceed with Semrush only

## Step 2: Pull Live Data

Pull these data sources (follow data-pull-patterns.md for exact parameters):

**Semrush (PRIMARY — mandatory):**
1. Call `mcp__semrush__execute_report` — Domain Organic Search Keywords for this domain, database=us, display_limit=30. This reveals what the domain currently ranks for.
2. Identify the primary keyword (highest volume purchase-intent term). Call `mcp__semrush__execute_report` — Related Keywords for that primary keyword, display_limit=20. This finds untapped long-tails.

**GSC (ENRICHMENT — optional):**
3. Call `mcp__gscServer__get_search_analytics` with the resolved siteUrl, last 28 days, dimensions=[query, page], rowLimit=50. This shows what Google already associates with this domain and actual click data.

If any source fails, print the appropriate `[SEO]` warning from core.md and continue.

## Step 3: Analyze & Generate

Using the pulled data + the methodology, generate the topical map:

**Structure:** 1 Hub → 3 Sub-Hubs → 3 purchase-intent pages per Sub-Hub = 13 pages total.

**For each page, specify:**
- Target keyword (from Semrush/GSC data — real keywords with real volume)
- URL slug (keyword in URL — e.g., `/houston-maritime-injury-lawyer`)
- H1 (keyword-optimized, purchase-intent)
- Above-the-fold CTA recommendation (call, form, booking — vertical-specific)
- Word count target (Hub: 800-1000, Sub-Hub: 600-800, purchase-intent: 400-500)
- Internal link targets (which other pages in the silo this page links to)
- Search volume + CPC (from Semrush data)
- Current ranking position (from GSC data, if available)

**Prioritization:** Order purchase-intent pages by: (search volume × CPC) descending, with preference for keywords where the domain has impressions but low position (ranking gaps = low-hanging fruit).

**Localization:** Every page MUST be localized to {{CITY}} with sub-neighborhoods where applicable (e.g. for Houston: Galleria, Heights, Montrose, Katy).

**Format:** Present as a clean hierarchy:
```
HUB: [keyword] — [url] — [volume] — [word count]
  SUB-HUB 1: [keyword] — [url] — [volume] — [word count]
    COMPACT: [keyword] — [url] — [volume] — [word count]
    COMPACT: [keyword] — [url] — [volume] — [word count]
    COMPACT: [keyword] — [url] — [volume] — [word count]
  SUB-HUB 2: ...
  SUB-HUB 3: ...
```

Then provide a detailed spec for each page.

**Anti-patterns to avoid:** Do NOT suggest "What is..." or "How to..." pages. Every page must target a searcher ready to convert.

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full topical map playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `Topical Map — [domain]`

Close with the ONE specific page to create TODAY that will have the highest impact.
