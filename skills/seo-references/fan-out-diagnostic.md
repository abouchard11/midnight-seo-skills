# Fan-out diagnostic — one BOFU page

Owner desks: `/geo` (citation matrix) and `/aeo` (passage). Not a skill. Not a content calendar.

Google documents query fan-out for AI Mode / AI Overviews: one prompt is decomposed into related searches, then synthesized. Public 2026 playbooks sell "cover every subquery with a new URL." Dated counter-evidence (Kevin Indig + AirOps, Apr 2026): fan-out *coverage* was nearly irrelevant next to retrieval rank and heading-query match. This diagnostic follows the counter-evidence.

## When

- `/geo-crawl` is CLEAR or CONTINUE WITH FIXES. Never on STOP.
- You already have one converting URL and one money / category-recommend prompt from the GEO matrix.
- Skip on a local-only money site whose next hour belongs to `/map-flap`.

## Method

1. **Seed.** One prompt the buyer actually asks. Not a "what is GEO" prompt.
2. **Branches.** Infer at most six, from this closed list: compare, price-or-risk, eligibility, timeline, local qualifier, objection. Stop at six. Do not generate 12.
3. **Map.** Each branch lands on *one* of:
   - an existing H2 / FAQ on the same BOFU URL, or
   - an existing page in the 13-page silo (1 hub / 3 sub-hubs / 9 purchase-intent)
   - Label the landing `SAME_URL` or `SILO_PAGE`. Never `NEW_URL`.
4. **Observe (optional).** If AI Mode or AI Overviews is reachable this session, load the *seed* prompt once, as a person would. List cited domains. Do not hammer `/goto`. If the surface is unreachable, every branch stays `INFERRED`.
5. **Score the branch.**
   - `COVERED` — our URL already has a heading that matches the branch, or we are in the cited-domain list for the seed
   - `MISSING` — cited domains answer the branch and we do not, or the heading is absent on the mapped URL
   - `INFERRED` — no live AI Mode look this run
6. **Patch.** Ship one heading + one 134–167 word standalone passage on the existing BOFU URL for the worst `MISSING` branch. If the page is already at the core.md cap, replace a weak paragraph. Do not append. Do not open a thirteenth-plus URL.

## Refuse

- A 12-URL explainer silo justified as fan-out coverage
- "What is" / "How to" pages
- Selling a coverage percentage as citation probability
- Running this diagnostic while `/geo-crawl` is STOP

## Output table

| Branch type | Inferred subquery | Maps to | Score | Patch |
|---|---|---|---|---|
| compare | | SAME_URL / SILO_PAGE | COVERED / MISSING / INFERRED | one heading or none |

One patch row only in Recommended Actions.
