# Data Pull Patterns — MCP Tool Reference

All tool names use the `mcp__<server>__<tool>` convention. During implementation, verify exact names against the deferred tools list at session start.

## Semrush (`mcp__semrush__`)

All Semrush calls go through the discovery → schema → execute flow:
1. Call `mcp__semrush__get_report_schema` with the report type name to get exact parameters
2. Call `mcp__semrush__execute_report` with the discovered parameters

| Report Type | Use Case | Key Parameters |
|-------------|----------|----------------|
| Domain Organic Search Keywords | Top keywords a domain ranks for | domain, database=us, display_limit=30 |
| Related Keywords | Expand from a seed keyword | phrase=[keyword], database=us, display_limit=20 |
| Keyword Overview | Volume + CPC + difficulty for a keyword | phrase=[keyword], database=us |
| Competitors in Organic Search | Who competes for the same keywords | domain, database=us, display_limit=10 |
| Organic Results | Who ranks for a specific keyword | phrase=[keyword], database=us, display_limit=10 |
| Backlinks | Inbound links to a domain | target=[domain], display_limit=20 |
| Referring Domains | Domains linking to target | target=[domain], display_limit=20 |
| Domain Overview | Authority score + traffic summary | domain, database=us |

## GSC (`mcp__gscServer__`)

| Tool | Use Case | Key Parameters |
|------|----------|----------------|
| `get_search_analytics` | Rankings, clicks, impressions | siteUrl (from MCP Routing Map), startDate (28 days ago), endDate (today), dimensions (query, page, country), rowLimit (50) |
| `list_sitemaps_enhanced` | Sitemap status + indexing counts | siteUrl |
| `inspect_url_enhanced` | Per-URL indexing status | inspectionUrl (full URL), siteUrl |
| `get_sitemaps` | List existing sitemaps | siteUrl |

**GSC siteUrl format:** Use the GSC Property value from the MCP Routing Map exactly. For sc-domain: properties, pass `sc-domain:example.com`. For URL-prefix properties, pass the full URL.

## GA4 (`mcp__google-analytics__`)

| Tool | Use Case | Key Parameters |
|------|----------|----------------|
| `run_report` | Traffic, events, sources | propertyId (from MCP Routing Map, just the number e.g. "{{GA4_PROPERTY_ID}}"), dateRanges ([{startDate: "28daysAgo", endDate: "today"}]), metrics, dimensions |
| `get_property_details` | Property config | propertyId |

**Common report configurations:**

Traffic by page:
- dimensions: [pagePath], metrics: [sessions, bounceRate]

Events audit:
- dimensions: [eventName], metrics: [eventCount]

Traffic sources:
- dimensions: [sessionDefaultChannelGroup], metrics: [sessions]

## CamoFox Stealth Browser (`mcp__camofox__`)

Anti-detection browser for scraping pages behind Cloudflare and other bot protection. Optional enrichment — see core.md Section 5 for when to use.

**Pre-flight:** Check for `camofox` tools in the deferred tools list. If absent, skip all CamoFox steps.

**Tool name discovery:** CamoFox exposes ~46 tools. The exact MCP tool names follow the `mcp__camofox__<tool>` pattern. At session start, check the deferred tools list for tools matching `camofox` to discover available tool names. Core tools to look for:

| Likely Tool Pattern | Use Case | Key Parameters |
|---------------------|----------|----------------|
| `*health*` or `*status*` | Verify browser server is running | (none) |
| `*navigate*` | Load a URL in stealth browser | url |
| `*snapshot*` | Capture page accessibility tree (headings, links, text, CTAs) | (tab identifier) |
| `*extract*` or `*content*` | Pull specific page content | (selector or extraction config) |
| `*search*` | Search within a page or across the web | query |
| `*click*` or `*interact*` | Click elements, fill forms | (element identifier) |
| `*tabs*` | Manage multiple browser tabs | (tab action) |
| `*session*` or `*profile*` | Persist cookies/sessions across runs | (session config) |

**Typical flow for competitor page analysis:**
1. Health check → verify browser server is running
2. Navigate → load competitor URL (e.g., the #1 ranking page for a target keyword)
3. Snapshot → capture the full page structure
4. Parse snapshot for: H1 text, above-the-fold CTA, outbound links, word count, schema markup presence

**Docker dependency:** CamoFox tools require the `camofox-browser` Docker container running on port 9377. If health check fails, the container may be stopped — tell the user to run `docker start camofox-browser`.

## Graphiti (`mcp__graphiti__`)

| Tool | Use Case | Parameters |
|------|----------|------------|
| `search_nodes` | Check for prior skill runs | query (skill name + domain), group_ids ([group_id]) |
| `add_memory` | Save structured summary | name, episode_body, group_id, source="text", source_description |
