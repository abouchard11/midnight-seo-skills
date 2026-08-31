---
name: ga4
description: Wire high-ticket conversion tracking and the AI Assistant channel — audit events, generate missing event architecture, and separate money conversions from AI-referral sessions
when_to_use: Use when setting up conversion tracking, auditing GA4 events, or addressing conversion gaps. Also when the user asks about analytics setup, tracking, conversions, AI Assistant channel, ChatGPT referral traffic, or what events to track.
argument-hint: "<domain>"
---

# GA4 Telemetry

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice defined there to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference. Dated GEO measurement note: `seo-references/gap-2026-08-31.md`.

## Step 1: Parse Domain

Extract the domain from the user's argument. Resolve it against the MCP Routing Map in core.md. The GA4 property ID is required for this skill — if the domain has no GA4 property, warn and stop.

Also identify the vertical type from the portfolio roster (legal, medical, home service, real estate, e-commerce, etc.) — this determines which conversion events to recommend.

## Step 2: Pull Live Data

**GA4 (PRIMARY for this skill):**
1. Call `mcp__google-analytics__run_report` with the resolved propertyId, dimensions=[eventName], metrics=[eventCount], dateRanges=[{startDate: "28daysAgo", endDate: "today"}]. This reveals which events are currently firing.
2. Call `mcp__google-analytics__get_property_details` with the propertyId. This shows property configuration.
3. If the property has the default AI Assistant channel, pull sessions for the last 28 days. If not, say so and add enablement to Recommended Actions.

**Cross-reference:** Check the user's CLAUDE.md for the "GA4 CONVERSION GAPS" table. This table tracks which domains have conversion events wired vs. not. Note the current status for this domain.

## Step 3: Generate Conversion Architecture

**Section 1 — Current State Assessment:**
List all events currently firing with their counts. Highlight:
- Which events are just default GA4 (page_view, scroll, click) — these are vanity
- Which events are custom/conversion events — these are money events
- What's MISSING based on the vertical

**Section 2 — Custom Event Architecture:**
Based on the vertical, recommend these high-value events:

For **legal** domains:
- `generate_lead` — contact form submission (primary conversion)
- `click_to_call` — phone number click
- `consultation_request` — case evaluation form
- `form_start` — user began filling out form (micro-conversion)

For **medical** domains:
- `generate_lead` — appointment booking or contact form (primary)
- `click_to_call` — phone number click
- `insurance_check` — insurance verification form
- `appointment_booking` — online scheduling

For **home service** domains:
- `generate_lead` — quote request (primary)
- `click_to_call` — phone number click
- `schedule_service` — online booking
- `quote_request` — estimate form submission

For **real estate** domains:
- `generate_lead` — property inquiry (primary)
- `seller_form_submit` — seller lead form
- `click_to_call` — phone number click
- `property_view` — individual listing viewed (micro-conversion)

For **e-commerce** domains:
- `purchase` — completed purchase (primary)
- `add_to_cart` — cart addition
- `begin_checkout` — checkout started
- `generate_lead` — waitlist/signup (if pre-launch)

**Section 3 — Implementation Code:**
For each recommended event, provide a ready-to-paste gtag snippet:
```javascript
// [Event Name] — [trigger description]
gtag('event', 'generate_lead', {
  event_category: '[vertical]',
  event_label: '[specific trigger]',
  source: '[page or form identifier]'
});
```

Note: These are advisory code snippets. The user applies them manually to their codebase. This skill does not modify project files.

**Section 4 — Conversion Goals:**
- Primary conversion event (mark as Key Event in GA4 Admin)
- Secondary conversion events
- Micro-conversions worth tracking

**Section 5 — UTM Parameter Template:**
Template for tracking which SEO landing pages drive conversions:
`?utm_source=organic&utm_medium=seo&utm_campaign=[domain]&utm_content=[page-slug]`

Core principle: track money events, not vanity metrics.

**Section 6 — AI Assistant channel (GEO measurement)**

Shipped as a GA4 default channel around May–June 2026. Enable it. Pull it. Do not confuse it with `/geo` citation scores.

What it usually catches: ChatGPT, Gemini, Copilot, Claude, Grok, DeepSeek referrals that arrive with an identifiable source.

What it usually misses or misfiles:
- Perplexity often stays under Referral
- Google AI Overviews / AI Mode sit inside Organic Search
- Referrer-less answers (user copied a URL, typed it, or the client stripped the referrer)

Add a complementary source/medium regex view so Perplexity and odd hosts are not invisible. Example pattern families (edit to what this property actually receives; do not paste untested):

- chatgpt.com, chat.openai.com
- perplexity.ai
- claude.ai
- gemini.google.com
- copilot.microsoft.com
- grok.com, x.ai
- deepseek.com

Report three numbers, last 28 days, side by side:
1. AI Assistant channel sessions
2. Regex referral sessions not in that channel
3. Money events on those landing pages

A session is not a citation. `/geo` still owns the prompt matrix. This section only answers "did anyone click through."

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full GA4 playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `GA4 Telemetry — [domain]`
