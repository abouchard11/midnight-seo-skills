---
name: indexer
description: Rapid indexing protocol — robots.txt, XML sitemap, GSC URL inspection, and IndexNow/Bing submit so new BOFU pages enter both Google and the Bing-shaped indexes ChatGPT and Copilot read
when_to_use: Use after publishing new pages, auditing indexing status, or setting up technical SEO infrastructure. Also when the user asks about indexing, sitemaps, robots.txt, IndexNow, Bing Webmaster, or why a page is missing from ChatGPT.
argument-hint: "<domain>"
---

# GSC Rapid Indexer

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology in that file to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference. Dated GEO context: `seo-references/gap-2026-08-31.md`.

Core principle: connect Google Search Console, submit sitemaps, and submit URLs whenever pages are added or edited — that covers Google. ChatGPT Search and Copilot do not read GSC. For those surfaces, IndexNow + Bing Webmaster Tools is the index path.

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
- Retrieval-bot allow/deny is owned by `/geo-crawl`. Do not invent a second crawler table here.
- Note: Print to terminal for user to apply. This skill does not write to project files.

**Section 3 — XML Sitemap Structure:**
Based on the topical map structure (13 pages per silo):
- Hub pages: priority 1.0, changefreq weekly
- Sub-Hub pages: priority 0.8, changefreq weekly
- Purchase-intent pages: priority 0.6, changefreq monthly
- Format: show the sitemap XML structure as advisory output

**Section 4 — Two-index protocol**

Google and Bing are different doors.

1. **Google — URL Inspection + sitemap.** The Indexing API is officially for JobPosting and BroadcastEvent. For BOFU pages, use URL Inspection. The legacy sitemap ping endpoint was retired in 2023; do not use it. Resubmit the sitemap in GSC after structural changes.
2. **Bing — IndexNow.** Participating engines include Bing and Yandex. Google is not a participant. After every BOFU publish or material edit:
   - Confirm an IndexNow key file is publicly reachable (`https://[host]/[key].txt`, file body = key).
   - POST the URL list to `https://api.indexnow.org/indexnow` with `host`, `key`, `keyLocation`, `urlList`.
   - Confirm the host in Bing Webmaster Tools. If the property has an AI Performance / Copilot citation report, screenshot the last 28 days into the playbook.
3. **Manual URL Inspection** remains the Google fallback when the API does not apply.

Do not tell the operator that IndexNow "indexes ChatGPT." It notifies Bing-shaped indexes that ChatGPT Search and Copilot have historically read. Retrieval can still miss the page.

**Section 5 — Post-Publish Checklist (for every new purchase-intent page):**
```
[] Submit URL in GSC via URL Inspection
[] POST the same URL to IndexNow (Bing path)
[] Confirm Bing Webmaster Tools has the host verified
[] Share on 2 social platforms (signal amplification — see /signal)
[] If this host is a SHIP/MAYBE source, confirm the Preferred Sources popup is on the page (see /preferred-source). Skip for tools and /blog paths.
[] Add internal link from hub page to the new page
[] Verify rendering in Mobile-Friendly Test
[] Check GSC indexing status after 48 hours
[] Optional: ChatGPT Search prompt for the page's money query after Bing has had a day
```

**Section 6 — GSC generative-AI toggle**
Settings → Search generative AI (documented mid-2026) includes or excludes the *property* from AI Overviews, AI Mode, and generative Discover. Default is include. Record the current state. Do not flip it as an "optimization."

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full indexing protocol to terminal
2. Extract structured summary
3. Save to Graphiti with name `Indexer — [domain]`
