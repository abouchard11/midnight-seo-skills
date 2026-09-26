---
name: hunter
description: Targeted backlink acquisition — outreach templates, linkable assets, and competitive link gap analysis grounded in Semrush data
when_to_use: Use when building backlinks, planning outreach campaigns, or analyzing competitor link profiles. Also when the user asks about link building, outreach, or "how do I get backlinks".
argument-hint: "<domain>"
---

# Hunter Protocol — Backlink Acquisition

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

Core principle: a few topical, niche-relevant links beat hundreds of generic ones. You don't need many backlinks to show up for great purchase-intent keywords.

## Step 1: Parse Domain

Extract the domain. Resolve against MCP Routing Map. Identify the vertical type.

## Step 2: Pull Live Data

**Semrush (PRIMARY):**
1. Call `mcp__semrush__execute_report` — Backlinks for this domain, display_limit=20. Shows current inbound link profile.
2. Call `mcp__semrush__execute_report` — Referring Domains for this domain, display_limit=20. Shows authority distribution of linking domains.
3. Call `mcp__semrush__execute_report` — Competitors in Organic Search for this domain, display_limit=5. Identifies who to compare link profiles against.

## Step 3: Generate Hunter Protocol

**Section 1 — Current Link Profile:**
Summarize what the Semrush data shows: total backlinks, referring domains, authority distribution, anchor text patterns. Identify strengths and gaps.

**Section 2 — Target Personas (3 specific local link targets):**
For each target:
- Type (local news, industry blog, complementary business, professional directory)
- Specific example targets (real types of local organizations in this vertical)
- Why they'd link to us (value exchange — what do they get?)
- Estimated domain authority range
- Outreach channel (email, LinkedIn, Twitter)

**Section 3 — Cold Email Template:**
- Subject line: pattern-interrupt, not generic
- Body: 3-4 sentences maximum. Value-first. Specific about what you're offering.
- CTA: one clear ask
- Follow-up: one follow-up template, 3 days later

**Section 4 — Linkable Asset Ideas (3 for this vertical):**
Think: calculators, data visualizations, local statistics, free tools. Examples:
- Legal: "Houston Maritime Injury Settlement Calculator"
- Medical: "Houston Dental Implant Cost Estimator"
- Home service: "Houston Home Repair Cost Guide by Neighborhood"
Each asset should attract links naturally while targeting purchase-intent keyword pages.

**Section 5 — Low-Effort Link Wins:**
- Featured.com journalist pitches (~75% success rate) — 2 specific pitch angles for this vertical
- Niche directory submissions: 5 specific directories for this vertical (not generic web directories)
- Podcast guesting pitch template
- Press release strategy ($6-80 each, influences LLM citations) — 1 specific PR angle
- Product Hunt launch (if applicable for the vertical)

**Section 6 — Outbound Link Strategy:**
Core principle: pages with outbound links to authoritative sources outrank pages without them.
- Recommend 2-3 outbound links per purchase-intent keyword page to authoritative, topically relevant sources
- Specific sources for this vertical (government sites, industry associations, research institutions)

**Section 7 — Competitive Link Gap:**
Compare this domain's backlink profile to the top 2-3 competitors from Semrush data. Identify: links competitors have that this domain doesn't, sorted by authority.

Close with: "5-10 quality topical links will do more than 100 generic ones."

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full Hunter Protocol to terminal
2. Extract structured summary
3. Save to Graphiti with name `Hunter Protocol — [domain]`
