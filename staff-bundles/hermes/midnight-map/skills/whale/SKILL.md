---
name: whale
description: Hunt new high-ticket exact-match local-service domains — validated with Semrush volume and CPC data
when_to_use: Use when exploring portfolio expansion, researching new verticals, or evaluating domain acquisitions. Also when the user asks about new domains, new verticals, or "what should I acquire next".
argument-hint: "(no argument — portfolio expansion mode)"
---

# Whale Hunter Engine

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the core methodology and voice defined there to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

## Step 1: Identify Current Portfolio Coverage

Read the Full 13-Domain Roster from core.md. Map verticals already covered:
- PI law ({{YOUR_DOMAIN}})
- Immigration law ({{YOUR_DOMAIN}})
- Maritime/admiralty law ({{YOUR_DOMAIN}} + syndicate)
- Work accidents ({{YOUR_DOMAIN}})
- Dental implants ({{YOUR_DOMAIN}})
- Plastic surgery ({{YOUR_DOMAIN}})
- Pool building ({{YOUR_DOMAIN}})
- AC repair ({{YOUR_DOMAIN}})
- Gold buying ({{YOUR_DOMAIN}})
- Commercial roofing ({{YOUR_DOMAIN}})
- Permit expediting ({{YOUR_DOMAIN}})
- Florida land ({{YOUR_DOMAIN}})
- Legal directory ({{YOUR_DOMAIN}})

New suggestions MUST target NET NEW verticals — no overlap with the above.

## Step 2: Pull Validation Data

For each candidate vertical (generate 7 candidates based on high-ticket {{CITY}} services):

**Semrush (PRIMARY):**
1. Call `mcp__semrush__execute_report` — Keyword Overview for "{{CITY}} [service]" to validate search volume + CPC. Only proceed with candidates that have meaningful volume (>500/mo) and CPC (>$20).
2. For the top candidates (CPC x volume highest), call `mcp__semrush__execute_report` — Organic Results for "{{CITY}} [service]" to assess who's ranking and how beatable they are.

## Step 3: Generate Whale Targets

**Candidate Verticals to Research** (starting points — validate all with Semrush data):
- Foundation repair ({{CANDIDATE_DOMAIN}})
- Water damage restoration ({{CANDIDATE_DOMAIN}})
- Medical malpractice ({{CANDIDATE_DOMAIN}})
- Commercial HVAC ({{CANDIDATE_DOMAIN}})
- Bail bonds ({{CANDIDATE_DOMAIN}})
- Crane rental ({{CANDIDATE_DOMAIN}})
- Industrial cleaning ({{CANDIDATE_DOMAIN}})
- Elder care / nursing home ({{CANDIDATE_DOMAIN}})
- DWI defense ({{CANDIDATE_DOMAIN}})
- Truck accident ({{CANDIDATE_DOMAIN}})

**For each of the top 7 validated domains, provide:**

1. **Domain name:** `{{CITY_ABBREV}}______.com` format (e.g. `htx______.com` for Houston)
2. **Vertical / service type**
3. **Validated CPC:** from Semrush Keyword Overview (not estimated — real data)
4. **Validated monthly volume:** from Semrush (real data)
5. **Why it's a "Whale":** profit margin analysis for this vertical in {{CITY}}
6. **Purchase-intent keyword examples:** 3 bottom-of-funnel keywords this domain would target
7. **Competition assessment:** from Semrush Organic Results — who ranks #1-3, their domain authority, how beatable
8. **Domain availability note:** Suggest checking availability via registrar. This skill does not verify domain registration status.

**Ranking formula:** Sort by (CPC x volume x beatable-competition-score) descending. Beatable = low DA competitors in top positions, missing on-page SEO signals, thin content.

Close with: "Never stop acquiring. The portfolio is the moat."

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full Whale Hunter report to terminal
2. Extract structured summary
3. Save to Graphiti with name `Whale Hunter — Portfolio` and group_id `{{GRAPHITI_GROUP_ID}}`
