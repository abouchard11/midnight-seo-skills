---
name: indexer
description: Rapid indexing protocol — robots.txt, XML sitemap, Indexing API setup, and post-publish checklist grounded in GSC data
when_to_use: Use after publishing new pages, auditing indexing status, or setting up technical SEO infrastructure. Also when the user asks about indexing, sitemaps, robots.txt, or "why isn't my page showing up".
argument-hint: "<domain>"
---

# GSC Rapid Indexer

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology in that file to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

Core principle: connect Google Search Console, submit sitemaps, and submit URLs whenever pages are added or edited — that covers the most pressing aspects of technical SEO.

## Step 1: Parse Domain

Extract the domain. Resolve against MCP Routing Map. The GSC property is required for this skill's data pulls — if unavailable, warn but still generate advisory output.

## Step 2: Pull Live Data

**GSC (PRIMARY for this skill):**
1. Call `mcp__gscServer__list_sitemaps_enhanced` — current sitemap status (submitted count, indexed count, errors). Shows health of current sitemap infrastructure.
2. Call `mcp__gscServer__get_sitemaps` — list existing sitemap URLs.
3. Call `mcp__gscServer__inspect_url_enhanced` for 3-5 key pages (homepage + top pages from portfolio context). Shows per-URL indexing status, last crawl date, and any issues.

## Step 3: Generate Indexing Protocol

**Section 1 — Current Indexing Status:**
Based on GSC data:
- How many pages are submitted vs. indexed?
- Which key pages are indexed vs. not?
- Any crawl errors or indexing issues?
- Last crawl dates — is Googlebot visiting regularly?

**Section 2 — Robots.txt (advisory output):**
Generate an optimized robots.txt. Rules:
- Allow all important content pages
- Block: /admin, /api, /_next/static (framework internals), /staging, duplicate content paths
- Include Sitemap directive pointing to XML sitemap URL
- Note: Print to terminal for user to apply. This skill does not write to project files.

**Section 3 — XML Sitemap Structure:**
Based on the topical map structure (13 pages per silo):
- Hub pages: priority 1.0, changefreq weekly
- Sub-Hub pages: priority 0.8, changefreq weekly
- Purchase-intent pages: priority 0.6, changefreq monthly
- Format: show the sitemap XML structure as advisory output

**Section 4 — Rapid Indexing Protocol:**
1. **Google Indexing API** — setup steps for the 24-hour indexing method. Note: this API is officially for JobPosting and BroadcastEvent schema types. For other content types, use the manual URL inspection approach instead.
2. **Bing IndexNow** — instant indexing via IndexNow protocol. Simpler to implement, no restrictions on content type.
3. **Manual URL Inspection** — submit each new URL via GSC URL Inspection tool.
4. **Sitemap resubmission** — resubmit the sitemap in GSC after updates (the legacy Google ping endpoint was retired in 2023; do not use it).

**Section 5 — Post-Publish Checklist (for every new purchase-intent page):**
```
[] Submit URL in GSC via URL Inspection
[] Ping sitemap URL
[] Share on 2 social platforms (signal amplification — see /signal)
[] If this host is a SHIP/MAYBE source, confirm the Preferred Sources popup is on the page (see /preferred-source). Skip for tools and /blog paths.
[] Add internal link from hub page to the new page
[] Verify rendering in Mobile-Friendly Test
[] Check indexing status after 48 hours
```

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full indexing protocol to terminal
2. Extract structured summary
3. Save to Graphiti with name `Indexer — [domain]`
