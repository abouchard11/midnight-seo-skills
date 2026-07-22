---
name: map-flap
description: Google Map Pack domination strategy for local sub-markets with geo-grid attack plan
when_to_use: "Use when optimizing for local search, Map Pack ranking, or Google Business Profile. LOCAL-ONLY skill: if the domain is not a Houston-area local service (e.g., {{DOMAIN_A}}, {{DOMAIN_B}}), warn the user that Map Pack strategy is not applicable and suggest /topical-map or /signal instead."
argument-hint: "<domain>"
---

# Map Flap — Google Map Pack Domination

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the core methodology and voice to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Step 1: Parse Domain & Validate Local Eligibility

Extract the domain from the user's argument. Resolve it against the MCP Routing Map in core.md.

**Critical check:** Verify the domain is in the Local Domains list in core.md (Section 2D). If NOT a local domain:
- Print: `[SEO] Warning: {domain} is not a local service. Map Pack strategy is not applicable.`
- Suggest: `/topical-map` for content architecture or `/signal` for social amplification.
- STOP. Do not generate a Map Pack strategy for non-local domains.

If local, extract the service type from the domain name and portfolio roster (e.g., {{DOMAIN}} → "[service type]", based on the domain's naming pattern).

## Step 2: Pull Live Data

**Semrush (PRIMARY):**
1. Call `mcp__semrush__execute_report` — Keyword Overview for "[service type] {{CITY}}" and "[service type] near me" variants. This reveals volume + CPC for local-intent keywords.

**GSC (ENRICHMENT):**
2. Call `mcp__gscServer__get_search_analytics` with the resolved siteUrl, last 28 days, dimensions=[query], rowLimit=50. Filter results for geo terms: queries containing "{{CITY}}", "{{CITY_ABBREV}}", "near me", or your metro's neighborhood names (e.g. for Houston: Galleria, Heights, Montrose, Katy, Sugar Land).

## Step 3: Generate Map Pack Strategy

**Section 1 — GBP Optimization Checklist:**
- Primary category (exact Google Business category for this vertical)
- 2 secondary categories
- Business description (750 characters max, keyword-rich, {{CITY}}-specific)
- Service area configuration: which {{CITY}} sub-markets to claim
- Photo strategy: storefront, team, work examples, before/after
- Attributes to enable (wheelchair accessible, appointment required, etc.)

**Section 2 — Geo-Grid Attack Plan:**
Identify 8-10 {{CITY}} sub-markets to target. For each sub-market:
- Sub-market name (e.g., "Galleria / Uptown")
- Target keyword page that supports it (URL slug, target keyword)
- Estimated local search volume (from Semrush data)
- Proximity manipulation tactics: service area pages, localized content, geo-specific schema markup

**Section 3 — Map Pack Ranking Factors (Pareto):**
- **Relevance:** exact-match business name + categories + localized content
- **Proximity:** service area configuration + localized pages
- **Prominence:** reviews, citations, links, brand signals
- For each factor: specific actions to take THIS WEEK

**Section 4 — Review Generation Script:**
- Post-service review request template (text message format, under 160 chars)
- Review response templates: one for positive reviews, one for negative
- Target: 5 new reviews per month minimum

Close with the #1 thing to do TODAY to start showing up in the Map Pack.

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full Map Pack playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `Map Flap — [domain]`
