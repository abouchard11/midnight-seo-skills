---
name: kilo
description: Use when ready to execute link building — generates link bait content specs, broken link targets, resource page submissions, HARO pitches, and outreach sequences with CamoFox-validated targets. Complements hunter's analysis with executable deliverables.
argument-hint: "<domain>"
---

# Kilo — Link Acquisition Protocol

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Concept

Hunter tells you where the links are. Kilo gets them. This skill generates executable link acquisition deliverables — not analysis, not strategy, but the actual content, pitches, and targets you need to build links THIS WEEK.

Core principle: you don't need many backlinks to show up for great purchase-intent keywords. A few topical, niche-relevant links beat hundreds of generic ones. Kilo targets 5-10 high-quality links, not 100 garbage ones.

## Step 1: Parse Domain

Extract the domain from the user's argument. Resolve it against the MCP Routing Map in core.md:
- Strip protocol, www, trailing slashes, lowercase
- Look up group_id, GSC property, GA4 property, Semrush domain
- If domain not in map, warn and ask if user wants to proceed with Semrush only

## Step 2: Pull Live Data

**Semrush (PRIMARY):**
1. Call `mcp__semrush__execute_report` — Backlinks for this domain, display_limit=20. Current inbound link profile.
2. Call `mcp__semrush__execute_report` — Referring Domains, display_limit=20. Authority distribution of linking domains.
3. Call `mcp__semrush__execute_report` — Competitors in Organic Search, display_limit=5. Identify who competes for the same keywords.
4. For the top 2 competitors, call `mcp__semrush__execute_report` — Backlinks, display_limit=20 each. This reveals the link gap — who links to competitors but not to this domain.

**GSC (ENRICHMENT):**
5. Call `mcp__gscServer__get_search_analytics` — last 28 days, dimensions=[page], rowLimit=20. Identify which pages on the domain have the most impressions but lowest CTR — these are the pages that need link juice to climb.

**CamoFox (ENRICHMENT):**
6. For the top 3 link gap targets (sites linking to competitors but not to this domain), use CamoFox to:
   - Navigate to the specific page that links to the competitor
   - Snapshot the page
   - Verify the link is still live
   - Identify the page type (resource page, blog post, directory, news article)
   - Find contact information (author name, about page link, contact form)
   - Check if the page accepts submissions or guest contributions

If any source fails, print the appropriate `[SEO]` warning from core.md and continue.

## Step 3: Link Gap Analysis

From the Semrush data, build a **Link Gap Matrix**:

| Linking Domain | Links to Competitor A | Links to Competitor B | Links to Us | Authority | Page Type | Action |
|---------------|----------------------|----------------------|-------------|-----------|-----------|--------|

Prioritize domains that link to 2+ competitors but NOT to this domain. These are the highest-probability targets — they already link to sites in this vertical.

## Step 4: Generate Link Acquisition Deliverables

Produce 5 executable link targets across these categories:

### A. Link Bait Content Specs (1-2 targets)

For the domain's vertical, design a linkable asset — something other sites would naturally reference and link to:

**Per asset, specify:**
- Asset type (calculator, comparison table, original data visualization, survey results, infographic data)
- Target keyword it supports (from the topical map if available)
- URL where it would live on the domain
- One-paragraph spec of what the asset does
- Why sites in this vertical would link to it (what question does it answer?)
- 3 specific sites that would likely link to this type of content (from the link gap analysis)

**Vertical-specific link bait ideas:**
- Legal: settlement calculator, statute lookup tool, case timeline generator
- Medical/Health: dosage calculator, ingredient comparison chart, clinical trial tracker
- Real estate: market value estimator, permit cost calculator, ROI tool
- E-commerce/Supplements: purity comparison table, ingredient sourcing map, lab result database

### B. Broken Link Building (1-2 targets)

If CamoFox identified any broken outbound links on competitor-linking pages:

**Per target, specify:**
- The page with the broken link (URL)
- The broken link's anchor text and original destination
- What content to create (or already exists) on the domain to replace it
- Outreach email template (3-4 sentences, value-first):

```
Subject: Broken link on [their page title]

Hi [name],

Quick heads-up — the link to [broken destination] on your [page title] page is returning a 404.

I have a similar resource at [your URL] that covers [topic]. Happy to share if you'd like a working replacement.

[Your name]
```

### C. Resource Page Submissions (1-2 targets)

From the CamoFox page analysis, identify resource pages, directories, or link roundups in the vertical:

**Per target, specify:**
- Resource page URL
- Page title and what it lists
- Submission method (contact form, email, comment, direct submission)
- Which page on the domain to submit
- Pitch angle (why this resource belongs on their page)

### D. HARO / Journalist Pitches (1 target)

Generate a journalist pitch template for the domain's vertical:

**Specify:**
- Target publications (3 vertical-specific outlets)
- Pitch angle (what expertise the domain offers)
- Quote template (2-3 sentences the domain owner can use when responding to journalist queries)
- HARO category to monitor

### E. Competitor Mention Interception (optional, if data supports)

If Semrush shows unlinked brand mentions or competitor comparisons:
- Identify articles that mention competitors but not this domain
- Generate a pitch to get included in the comparison
- Template: "I noticed your article compares [A] and [B]. We're [domain] — [one-sentence differentiator]. Would you consider including us?"

## Step 5: Outreach Sequence

For the top 3 link targets, generate a 3-touch outreach sequence:

**Touch 1 (Day 0):** Initial value-first email (see templates above)
**Touch 2 (Day 4):** Follow-up with additional context or a different angle
**Touch 3 (Day 10):** Final gentle follow-up, offer to help with something else

**Voice rules for outreach:**
- 3-4 sentences maximum per email
- Lead with value, not ask
- No "I hope this finds you well" or "I'm reaching out because"
- Pattern-interrupt subject lines (questions, specific data points)
- Close with a specific ask, not an open-ended "let me know"

## Step 6: Link Velocity & Anchor Text Plan

Based on the current backlink profile from Semrush:

**Link velocity recommendation:**
- Current referring domains: [from Semrush]
- Target: Add 2-4 quality referring domains per month
- Do NOT exceed 5 new referring domains per week (looks unnatural)

**Anchor text distribution plan:**
- Branded anchors (domain name, brand name): 40-50%
- Exact match keyword anchors: 10-15%
- Partial match / long-tail anchors: 20-25%
- Generic anchors (click here, this site, learn more): 15-20%
- Naked URLs: 5-10%

Map specific anchor text recommendations to the pages that need link juice most (from GSC data — high impressions, low position).

## Step 7: Output

Follow the Output Protocol from core.md:
1. Print the full link acquisition playbook (gap analysis, 5 targets with deliverables, outreach sequences, velocity plan)
2. Extract structured summary
3. Save to Graphiti with name `Kilo — [domain]`

Close with the ONE link to pursue THIS WEEK — the highest-probability target with the outreach email ready to send. Copy the email, send it, get the link.
