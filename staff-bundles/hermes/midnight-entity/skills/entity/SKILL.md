---
name: entity
description: Entity corroboration for GEO — make Organization and Person facts consistent across schema, sameAs profiles, Wikidata, and knowledge-panel sources so engines can name the brand when no URL is cited
when_to_use: Use when the user asks about knowledge panels, Wikidata, sameAs, entity SEO, brand knowledge graph, founder entity, or why ChatGPT or Gemini names a competitor but not this brand. Not for Map Pack or GBP edits — that is map-flap. Not for citation copy — that is geo after this desk.
argument-hint: "<domain or person>"
---

# Entity — corroboration desk

**First:** Read `~/.claude/skills/seo-references/core.md`. Purchase-intent pages stay the 80/20. This skill does not create a Wikipedia essay or a "what is" blog.

**Also read:** `seo-references/gap-2026-08-31.md` (why this desk exists) and `seo-references/sturm-shorts.md` (personal-site / knowledge-panel short).

Unit of success: engines **name the same legal/brand/person string** across surfaces, with off-site corroboration. Not a blue-link rank. Not a featured snippet (`/aeo`). Not a citation matrix (`/geo`).

Route, do not duplicate:

- GBP, NAP, reviews, geo-grid → `/map-flap`
- Citation / prompt matrix → `/geo` after `/geo-crawl`
- Referring-domain asks → `/hunter` then `/kilo`
- Preferred Sources badge → `/preferred-source`

## Do not do this

- Do not file a Wikipedia article that fails WP:N. A rejected draft is a stain, not an entity win.
- Do not invent Wikidata claims. Only write statements that already have a citable source.
- Do not wallpaper eight personal-site directories onto a local-service money domain. That list is for founder / personal properties; copy it from the Sturm short at execution time via `/kilo`.
- Do not treat a self-authored "About" page as third-party corroboration.

## Step 1: Name the entity

Extract the domain or person. Resolve against the MCP Routing Map.

Write the canonical strings the engines should learn:

| Field | Value |
|---|---|
| Brand string | |
| Legal name | |
| Product names | |
| Founder / author (only if the property is personal or expert-led) | |
| City / service area (local only) | |
| Official URL | |

If the homepage says "we" and never writes the proper noun, stop after this table and make that the first Recommended Action. GEO cannot attach a mention to a pronoun.

## Step 2: On-site identity (server-rendered)

Check homepage + About + the #1 converting page.

Required, visible in first-byte HTML:

- Organization or Person JSON-LD with stable `@id`, `name`, `url`, `logo` or `image`
- `sameAs` only for profiles that exist and match the name string (LinkedIn, YouTube, Wikidata, Wikipedia, Crunchbase, GBP). Empty or typo `sameAs` is worse than none.
- Visible byline or organization name in the first screen, not only in schema
- One sentence that states what the entity *is* in SVO form ("MidnightDev is a forward-deployed AI practice in Houston.")

CamoFox optional enrichment. If down: `[SEO] CamoFox unavailable — schema check is source-only.`

## Step 3: Off-site corroboration pool

List current third-party pages that already use the canonical string. Mark each CONFIRMED / MISSING / WRONG (wrong city, old name, dead URL).

Minimum viable set by property type:

| Type | Must-have | Nice | Never invent |
|---|---|---|---|
| Local service | GBP, 2–3 local citations with matching NAP | Review platforms already in `/map-flap` | Wikipedia |
| Product / SaaS | G2 or Capterra or equivalent, official docs, changelog | GitHub org, product Hunt-class pages if real | Fake comparison blogs |
| Founder / personal | LinkedIn, one high-quality personal-site listing | Wikidata if notable, knowledge panel if earned | Vanity wiki mirrors |

Personal-site directory submissions: open the Sturm short, copy the eight names on screen, run through `/kilo`. Do not hardcode the list here.

## Step 4: Wikidata / knowledge panel gate

Issue one verdict.

| Verdict | When | Action |
|---|---|---|
| **SKIP** | Local-service money site with no notability beyond the city | Stay on `/map-flap`. Do not open a Wikidata item. |
| **PREP** | Distinct brand + independent coverage exists or is being pitched | Align `sameAs` and legal name. Do not create the item this run. |
| **FILE** | Independent reliable sources already exist; item missing or stale | Draft the item statements + sources. Human files. Model does not click "publish." |

Knowledge panels are a side effect of corroboration + notability, not a form you submit.

## Step 5: Output

Follow the Output Protocol from core.md.

Playbook sections:

1. Entity table + proper-noun verdict
2. On-site schema / sameAs diff
3. Off-site pool (CONFIRMED / MISSING / WRONG)
4. Wikidata / panel gate (SKIP / PREP / FILE)
5. What this will not do

Graphiti name: `Entity — [domain or person]`. `group_id` from the routing map.
