---
name: parasite
description: Use when the domain can't outrank high-DA platforms for target keywords — generates platform-specific content for Reddit, Medium, Quora, YouTube, LinkedIn that captures SERP positions and funnels traffic back to the domain
argument-hint: "<domain>"
---

# Parasite — Platform Hijack Protocol

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice guidance to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Concept

Your domain is new. Authority score is low. You can't outrank Reddit, Amazon, YouTube, or Medium head-to-head. So you don't fight them — you publish ON them. Every parasite page is a funnel: platform traffic → your domain.

This is white-hat when done right: real accounts, valuable content, natural attribution. The platform gets good content. You get the SERP position. The searcher gets a better answer than whatever press release or marketplace listing currently ranks.

## Step 1: Parse Domain

Extract the domain from the user's argument. Resolve it against the MCP Routing Map in core.md:
- Strip protocol, www, trailing slashes, lowercase
- Look up group_id, GSC property, GA4 property, Semrush domain
- If domain not in map, warn and ask if user wants to proceed with Semrush only

## Step 2: Pull Live Data

**Semrush (PRIMARY):**
1. Call `mcp__semrush__execute_report` — Domain Organic Search Keywords, database=us, display_limit=30. Identify the domain's target keywords.
2. For the top 5 purchase-intent keywords by (volume × CPC), call `mcp__semrush__execute_report` — Organic Results (phrase_organic), display_limit=10 each. This reveals WHICH PLATFORMS currently rank for each keyword.

**GSC (ENRICHMENT):**
3. Call `mcp__gscServer__get_search_analytics` — last 28 days, dimensions=[query], rowLimit=50. Filter for keywords where the domain ranks position 11-100 (page 2+). These are parasite candidates — the domain can't rank on its own, so publish on platforms that can.

**CamoFox (ENRICHMENT):**
4. For the top 2 parasite opportunity keywords, use CamoFox to navigate to the highest-ranking Reddit/Medium/Quora page and snapshot it. Parse the snapshot for:
   - Content format (post length, structure, tone)
   - Engagement signals (upvotes, comments visible in accessibility tree)
   - Whether outbound links are present (can you link back naturally?)
   - Subreddit rules / platform norms visible on the page

If any source fails, print the appropriate `[SEO]` warning from core.md and continue.

## Step 3: Platform Analysis

From the SERP data, build a **Platform Ranking Matrix**:

For each target keyword, note which platforms appear in the top 10:
- Reddit (r/Biohackers, r/Nootropics, r/Supplements, etc.)
- YouTube (video results)
- Medium / Substack
- Quora
- LinkedIn
- Amazon (marketplace — can't parasite, but note as competitor)
- Wikipedia (can't parasite, but note)

Score each platform by: (frequency in SERPs × content controllability × link-back friendliness)

**Platform priority order (default):**
1. **Reddit** — Highest SERP frequency for purchase-intent queries. Google trusts Reddit. Posts can include links in context. Long shelf life. Target specific subreddits.
2. **YouTube** — Video results appear in blended SERPs. Descriptions allow links. Shorts for quick wins, long-form for authority.
3. **Medium** — High DA, dofollow links from publications. Articles index fast. Best for long-form comparison/review content.
4. **Quora** — Appears in "People Also Ask" and direct SERPs. Answers can include links. Best for question-format keywords.
5. **LinkedIn** — Articles index well for B2B/professional queries. Less useful for consumer products unless the vertical is professional.

## Step 4: Generate Parasite Content Specs

For each of the top 5 parasite opportunity keywords, generate a content spec:

**Per keyword, specify:**
- Target platform (from priority matrix)
- Target keyword + search volume + CPC
- Content format (Reddit post, Medium article, YouTube script, Quora answer)
- Title/headline (keyword-optimized for the platform)
- Content outline (3-5 sections, platform-native tone)
- Word count (match platform norms — Reddit: 200-500w, Medium: 800-1200w, Quora: 150-400w, YouTube: 60-180s script)
- Link-back strategy (how to naturally reference the domain without spam flags)
- CTA (what action the reader should take — visit domain, join waitlist, use tool)
- Publishing account requirements (age, karma, history — platform-specific)
- Estimated time to rank (Reddit: 1-7 days, Medium: 7-14 days, YouTube: 14-30 days)

**Link-back rules (non-negotiable):**
- Never post a bare URL as the entire content — that's spam
- Link must add value in context ("I found this comparison helpful: [link]")
- One link per post maximum — more triggers spam filters
- For Reddit: link in the body text, never in the title
- For Medium: link in a "Resources" or "Further Reading" section
- For YouTube: link in description + pinned comment
- For Quora: link as a supporting source mid-answer

**Anti-patterns:**
- Do NOT create fake accounts or personas
- Do NOT mass-post across multiple subreddits simultaneously
- Do NOT copy content from the domain to the platform — write platform-native content
- Do NOT use the same content template across platforms — each platform has its own voice
- Limit to 2 parasite posts per platform per week per domain (looks organic)

## Step 5: Monitoring Protocol

Generate a monitoring checklist:
- Track parasite page rankings for target keywords (weekly GSC check)
- Monitor referral traffic from platforms in GA4 (source/medium dimension)
- Check for content removal (platforms moderate — have backup plan)
- Refresh parasite content monthly (update dates, add new data, respond to comments)

## Step 6: Output

Follow the Output Protocol from core.md:
1. Print the full parasite playbook to terminal (platform matrix, content specs, link-back strategy, monitoring protocol)
2. Extract structured summary
3. Save to Graphiti with name `Parasite — [domain]`

Close with the one parasite post to publish THIS WEEK that will have the highest traffic impact. Specify the exact platform, subreddit/publication, keyword, and content angle. Post it, link back, and track the ranking.
