# GSC Export — All Active Sites

> **[raw evidence — unpolished]** 2026-08-07 pull notes. Buyer chapter is
> `../README.md`. Property names and metrics stay. Ignore internal map-path
> remarks; they are operator scratch, not a buyer deliverable.

# GSC Export — All Active Sites

**Pulled:** 2026-08-07
**Window:** 2026-07-10 → 2026-08-07 (28 days, GSC default lag applies to last ~2 days)
**Source:** `gscServer` MCP · `get_performance_overview` + `get_search_analytics`
**Properties queried:** all 22 in the account

## Files

| File | Contents |
| --- | --- |
| `portfolio-summary.csv` | One row per GSC property: clicks, impressions, CTR, avg position, status |
| `top-pages.csv` | Page-level performance for every site with meaningful volume |
| `top-queries.csv` | Converting queries + highest-impression zero-click queries per site |

## Portfolio totals (28d)

| Metric | Value |
| --- | ---: |
| Clicks | **258** |
| Impressions | **31,137** |
| Portfolio CTR | **0.83%** |
| Properties with impressions | 15 |
| Properties with clicks | 9 |

## Ranking

| # | Site | Clicks | Impr. | CTR | Avg pos |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | methyleneblueultra.com | 102 | 7,672 | 1.33% | 17.7 |
| 2 | buylandfl.com | 45 | 9,282 | 0.48% | 14.6 |
| 3 | jonesactcalculator.com | 32 | 3,208 | 1.00% | 23.5 |
| 4 | htxpermitfix.com | 25 | 1,225 | 2.04% | 29.4 |
| 5 | wordgameai.com | 16 | 1,333 | 1.20% | 13.9 |
| 6 | htxdentalimplants.com | 12 | 4,557 | 0.26% | 47.7 |
| 7 | yapword.com | 11 | 596 | 1.85% | 48.7 |
| 8 | midnightdev.dev | 9 | 224 | 4.02% | 6.7 |
| 9 | htxworkinjury.com | 6 | 220 | 2.73% | 30.3 |
| 10 | houstonlawyerlist.com | 0 | 2,339 | 0.00% | 85.1 |
| 11 | htxmaritimelaw.com | 0 | 421 | 0.00% | 68.1 |
| 12 | htxfoundationfix.com | 0 | 29 | 0.00% | 76.1 |
| 13 | thatsmybest.com | 0 | 12 | 0.00% | 1.8 |
| 14 | htximmigrationlaw.com | 0 | 10 | 0.00% | 26.7 |
| 15 | htxplasticsurgeon.com | 0 | 9 | 0.00% | 55.3 |

## Observations

**Impressions are not the constraint — position is.** buylandfl has the most impressions in the
portfolio (9,282) and converts 0.48% of them. `florida-land-prices-by-county` alone draws 4,456
impressions at position 9.0 for 7 clicks — a page ranking on the page-1 boundary for
high-volume informational terms it isn't winning the click on.

**houstonlawyerlist is the single largest dead weight.** 2,339 impressions, zero clicks, average
position 85.1. Two pages (`/truck-accidents` 1,188 imps @ 86.2, `/wrongful-death` 1,024 @ 87.6)
generate 95% of it, both ranking around position 86 — page 9. It is indexed and being served for
commercial-intent terms ("18 wheeler accident attorney houston", 152 imps) but nowhere near
clickable. This is an indexed-not-ranking problem, not a traffic problem.

**htxdentalimplants has the worst CTR-to-impression ratio of any site with volume** — 4,557
impressions, 12 clicks, average position 47.7. `/cost-guide` draws 1,503 impressions at position
58.5; `/dentists` draws 863 at position 78.4. Both are deep-page rankings on high-volume terms.

**Sites punching above their weight:** midnightdev.dev (4.02% CTR, avg position 6.7) and
htxpermitfix (2.04%) are the only two converting at a healthy rate. htxpermitfix's `/restaurants`
page converts 28.57% CTR at position 5.4 — small volume, but the pattern that works.

**yapword's Spanish opportunity is unworked** — "alternativas a wordle" is the site's
highest-impression query (103 imps) sitting at position 70.1, and `/wordle-alternative/` draws
466 impressions at position 60.2 with zero clicks.

**htxworkinjury's employer data pages are converting at extreme rates** on tiny volume — four
`/data/employer/*` pages produced 5 of the site's 6 clicks at 50–100% CTR and positions 1–7.
That programmatic surface works; it just has almost no impression volume yet.

## Data caveats — read before acting on `top-queries.csv`

1. **The zero-click query tail is an alphabetical slice, not a top-by-impressions ranking.** The
   GSC API sorts rows by clicks descending; once clicks hit zero the remaining rows come back in
   alphabetical order. With a 20-row limit, sites with few clicks returned an alphabetical
   fragment. Rows marked `zero-click sample` in the CSV are illustrative, **not** the true top
   queries. Clicked queries and all page-level data are correctly ranked. To get true
   top-by-impression queries, a re-pull with a much higher `row_limit` and client-side sorting is
   needed.
2. **Page lists are complete** where the site returned fewer rows than the limit
   (houstonlawyerlist, wordgameai, yapword, htxmaritimelaw, midnightdev, htxpermitfix) and
   **truncated at 15** for methyleneblueultra, htxdentalimplants, jonesactcalculator,
   htxworkinjury.
3. **thatsmybest.com and htximmigrationlaw.com returned no query-dimension rows** despite having
   12 and 10 impressions — GSC anonymizes query data below a volume threshold.
4. **The last ~2 days of the window are incomplete** — standard GSC reporting lag.

## Property-map discrepancies found (`~/.claude/references/property-maps.md` needs updating)

These surfaced while running the export and are worth acting on separately:

| Finding | Detail |
| --- | --- |
| **New unmapped property** | `sc-domain:jonesactcalculator.com` now exists and returns byte-identical data to the mapped `https://www.jonesactcalculator.com/`. The map says "do NOT flip" to domain format — still true operationally, but the duplicate should be recorded so it isn't double-counted. |
| **New unmapped property** | `sc-domain:ultramethyleneblue.com` exists in the account, zero data, no group_id, not in the map. |
| **Map is stale** | Map says htxfoundationfix is "NOT YET IN GSC — needs DNS verification". It **is** verified (`siteFullUser`) and has been collecting impressions since 2026-08-01. |
| **Access regression** | `stackdworkforce.com` is now `siteUnverifiedUser` → 403. Map records it as "verified 2026-04-30". Access was lost at some point. |
| **Access regression** | `sc-domain:htxaccidentattorney.com` is `siteUnverifiedUser` → 403. Map lists it as a normal domain property. |
| **Still unverified** | `abogadosinmigracionhtx.com` → 403, consistent with the map's "pending DNS TXT verification" note. |
| **Retired properties still present** | `sc-domain:semantix.live` and `https://semantix.live/` both return zero data. Map says "keep until retired" — they are now fully dark. |

Three properties (htxaccidentattorney, stackdworkforce, abogadosinmigracionhtx) could **not** be
exported — the service account lacks permission. Their rows in `portfolio-summary.csv` are marked
`403-no-permission` with blank metrics rather than zeros, so they aren't mistaken for dead sites.
