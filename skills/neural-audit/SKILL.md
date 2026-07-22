---
name: neural-audit
description: Full portfolio analysis — TAM, priority matrix, attack sequencing across all live domains
when_to_use: Use for portfolio-level strategic planning, budget allocation, or weekly priority review. Also when the user asks "what should I work on", "which domain is most valuable", or "portfolio status".
argument-hint: "(no argument — runs across full portfolio)"
---

# Neural Portfolio Audit

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the core methodology and voice defined there to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Step 1: Pull Portfolio-Wide Data

This skill has NO domain argument — it runs across the entire portfolio. Iterate through the MCP Routing Map in core.md and pull data for each domain that has live properties.

**Semrush (PRIMARY — run for each domain):**
1. For each domain in the MCP Routing Map, call `mcp__semrush__execute_report` — Domain Overview (database=us). Captures: authority score, organic traffic estimate, keyword count. This is the most important data for the audit.

**GA4 (ENRICHMENT — run for each property):**
2. For each GA4 property in the MCP Routing Map, call `mcp__google-analytics__run_report` with metrics=[sessions, bounceRate], dateRanges=[{startDate: "28daysAgo", endDate: "today"}]. Captures: real traffic + engagement.

**GSC (ENRICHMENT — run for each property):**
3. For each GSC property, call `mcp__gscServer__get_search_analytics` with dimensions=[], rowLimit=1 (totals only). Captures: total clicks + impressions per property.

**Note:** This skill makes many MCP calls. If rate limits or timeouts occur, collect as much data as possible and note which domains had incomplete data.

## Step 2: Analyze with Pareto Ruthlessness

Using the pulled data + the Full 13-Domain Roster (including LOCKED domains with CPC/volume data):

**Section 1 — Total Addressable Market (TAM):**
Per domain: rough TAM = CPC × monthly volume × 12 × estimated CTR (use 3% for top-3 position, 1% for positions 4-10). Sum for total portfolio valuation.

**Section 2 — Priority Matrix:**
Rank all 13 domains by: (CPC × Volume × Conversion Probability). Factor in:
- Domain status: LIVE (can act now) > ACTIVE > ACQUIRED (needs setup) > LOCKED (blocked)
- Vertical profit margins (legal = highest, home service = moderate, retail = lowest)
- Current traffic (from GA4) vs. potential traffic (from Semrush)
Identify the top 3 domains that represent 80% of revenue potential.

**Section 3 — Attack Sequencing (THIS WEEK):**
For each of the top 3 domains, give 3 specific actions with exact deliverables:
- Domain 1: [highest priority] — specific pages to create, specific keywords to target
- Domain 2: [second priority] — specific actions
- Domain 3: [third priority] — specific actions

**Section 4 — Blind Spots & Risks:**
- Sleeping assets: LOCKED domains with high CPC × volume (what's being left on the table?)
- Wasted effort: domains with low CPC in commoditized verticals
- Portfolio concentration risk: what % of TAM is in the top 1-2 domains?

**Section 5 — Purchase-Intent Page Deployment Status:**
Per domain: how many purchase-intent pages are deployed vs. how many are needed (based on topical map estimates of 13 pages per domain)?

**Section 6 — No-BS Verdict:**
"Here's where you should put $1,000 in SEO budget this month. Here's why. Here's what you'll get."

Close with the one move that changes everything: the single highest-leverage action to take this week.

## Step 3: Output

Follow the Output Protocol from core.md:
1. Print the full audit playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `Neural Audit — Portfolio` and group_id `{{GRAPHITI_GROUP_ID}}`
