# Operator evidence — worked audit on a real 18-domain portfolio

This chapter is a real run, not a demo fixture. MidnightDev probed its own
portfolio on **2026-08-25** (GEO crawl) and pulled **28-day GSC**
(2026-07-10 → 2026-08-07). Domain names, scores, and bot-block evidence
are left in on purpose — that is the selling point.

Contact PII was stripped. Internal operator map notes in the GSC dump
are marked raw, not rewritten.

Use this next to `/geo-crawl`, `/geo`, and `/neural-audit`. It is a
worked example of how those skills read in production, not a substitute
for running them on your properties.

## What you are looking at

18 live properties. Crawl scores are 0–100 from a multi-UA probe
(browser baseline + training bots + retrieval bots). GSC is Search
Console performance, not the crawl score.

### Crawl scorecard (2026-08-25)

| Domain | Score | What the probe actually saw |
|---|---:|---|
| jonesactcalculator.com | 100 | SSR_FULL, retrieval bots 200 |
| htxdentalimplants.com | 100 | SSR_FULL |
| htximmigrationlaw.com | 100 | SSR_FULL |
| abogadosinmigracionhtx.com | 100 | SSR_FULL |
| htxworkinjury.com | 100 | SSR_FULL |
| htxfoundationfix.com | 100 | SSR_FULL |
| methyleneblueultra.com | 100 | SSR_FULL |
| midnightdev.dev | 100 | SSR_FULL |
| buylandfl.com | 100 | SSR_FULL |
| wordgameai.com | 100 | SSR_FULL |
| houstonlawyerlist.com | 95 | SSR_FULL; one probe artifact, not a regression |
| htxmaritimelaw.com | 88 | SSR_THIN (311 words) |
| yapword.com | 83 | deliberate training-bot robots blocks |
| thatsmybest.com | 83 | same deliberate training-bot blocks |
| htxpermitfix.com | 80 | **bot-block evidence — see below** |
| htxplasticsurgeon.com | 75 | CSR_SHELL, 100 words |
| htxaccidentattorney.com | 70 | CSR_SHELL placeholder |
| htxcommercialroofers.com | 70 | CSR_SHELL placeholder |

12 of 18 scored a clean 100. Median bot TTFB 0.191s–0.361s (threshold
1.2s). Zero 402s. Zero true crawl regressions vs the 2026-08-07 baseline.

### The bot-block that stayed (htxpermitfix.com)

robots.txt is clean (`Allow: /`). The WAF is not.

| Bot | Category | Status |
|---|---|---|
| Browser baseline | — | 200 |
| OAI-SearchBot | retrieval | 200 |
| Claude-SearchBot / ClaudeBot | retrieval | 200 |
| PerplexityBot | retrieval | 200 |
| GPTBot | training | **429** (deterministic) |
| meta-externalagent | training | **429** (deterministic) |
| Amazonbot | training/other | 403 → 200 (flaps) |

Live-citation bots get through. Training crawlers do not. That is a
long-term model-memory leak, not an outage — and it is exactly the
`BOT_DIFFERENTIAL` `/geo-crawl` is built to surface. Confirm with origin
logs; a UA-spoof probe is not identity.

### GSC 28-day snapshot (2026-08-07 pull)

Portfolio: **258 clicks / 31,137 impressions / 0.83% CTR** across 15
properties with impressions.

| # | Site | Clicks | Impr. | CTR | Avg pos |
|---:|---|---:|---:|---:|---:|
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

Read: impressions are not the constraint — position is. buylandfl has
the most impressions and converts 0.48%. houstonlawyerlist is indexed
and served for commercial-intent terms at ~position 85 with zero clicks.
htxpermitfix `/restaurants` converts 28.57% CTR at position 5.4 — small
volume, the pattern that works.

## Files in this folder

| File | What it is |
|---|---|
| `geo-crawl-audit-portfolio-2026-08-25.md` | Full probe dump (per-domain UA tables). **[raw evidence — unpolished]** |
| `gsc-export-2026-08-07/portfolio-summary.csv` | One row per GSC property |
| `gsc-export-2026-08-07/top-pages.csv` | Page-level clicks/impr/CTR/position |
| `gsc-export-2026-08-07/top-queries.csv` | Converting queries + zero-click samples |
| `gsc-export-2026-08-07/README.md` | Pull notes + caveats. **[raw evidence — unpolished]** |

## Caveats (do not skip)

1. Zero-click query rows in the CSV are an alphabetical GSC slice after
   clicks hit zero, **not** a true top-by-impressions ranking. Clicked
   queries and page-level rows are ranked correctly.
2. Probe UAs are spoofed from one IP. A WAF that checks published bot
   ranges may disagree with the probe in either direction.
3. Three GSC properties returned 403 (no permission) and are blank, not
   zero: htxaccidentattorney, stackdworkforce, abogadosinmigracionhtx.
4. Placeholders (htxaccidentattorney, htxcommercialroofers) scoring 70
   is expected CSR_SHELL, not a surprise outage.

This is a chapter, not a 30-hour sanitized case study. The numbers are
real; the prose is the operator’s working notes.
