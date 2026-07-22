---
name: signal
description: Social signal amplification — platform-specific posts, YouTube Shorts scripts, and 7-day content calendar
when_to_use: Use when launching social promotion for new pages, creating video SEO content, or building a content calendar. Also when the user asks about social media, YouTube, or "how do I promote this page".
argument-hint: "<domain>"
---

# Signal Amplifier

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice defined there to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

VIDEO-FIRST SEO: "YouTube Shorts rank on Google SERPs — often within hours. An 18-second video ranked #1 in 8 hours."

## Step 1: Parse Domain

Extract the domain. Resolve against MCP Routing Map. Identify the vertical type and service offering.

## Step 2: Pull Live Data

**GSC (ENRICHMENT):**
1. Call `mcp__gscServer__get_search_analytics` — top 10 pages by clicks (last 28 days). These are the highest-performing pages to amplify first.

**GA4 (ENRICHMENT):**
2. Call `mcp__google-analytics__run_report` — dimensions=[sessionDefaultChannelGroup], metrics=[sessions], last 28 days. Shows current traffic source mix (how much is organic vs. social vs. direct).

## Step 3: Generate Signal Amplification Plan

**Section 1 — Platform-Specific Posts (locally targeted, purchase-intent):**

**Twitter/X** (280 chars max):
- Post text with local hashtags ({{#CITY}} {{#CITY_ABBREV}} + vertical-specific; e.g. #Houston #HTX)
- CTA: direct link to the highest-performing purchase-intent page
- 3 tweet variations to rotate

**Facebook** (150 words max):
- Community-focused angle, link to purchase-intent page
- Include a question to drive engagement
- Suggested image: service in action, local skyline, team photo

**LinkedIn** (200 words max):
- Professional angle, thought leadership hook
- Relevant to B2B if applicable, or position as industry expertise
- Tag relevant local business groups

**Instagram** (100 words + 15 metro-local hashtags):
- Visual-first caption
- 15 hashtags: mix of city, metro-abbreviation, vertical-specific, neighborhood-specific
- Story template: before/after or quick tip format

**Section 2 — YouTube Shorts Script (15-60 seconds):**
- Hook (first 3 seconds): pattern interrupt — surprising stat or bold claim from the vertical
- Value delivery (10-30 seconds): one specific tip related to the domain's service
- CTA (5 seconds): "Call us" / "Link in bio" / domain name spoken clearly
- Title: keyword-optimized, under 70 chars
- Description: keyword-rich, geo-localized, include full URL
- Tags: 10 relevant tags mixing vertical + {{CITY}} + intent terms

**Section 3 — 7-Day Content Calendar:**
Daily posting schedule across platforms. Map each post to a purchase-intent page.
"The more you post, the more visibility and followers you get."
Day 1-7: specific content type + platform + linked page for each day.

**Section 4 — Signal Validation Protocol:**
- Share every new purchase-intent page across ALL platforms within 1 hour of publishing
- Pin the most important post on each profile
- This sends traffic signals that validate the page to Google
- Consistency is the weapon

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full Signal Amplifier playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `Signal Amplifier — [domain]`
