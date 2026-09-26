# GEO Crawl Audit — 2026-08-25 vs 2026-08-07 Baseline

> **[raw evidence — unpolished]** Operator dump from 2026-08-25. Buyer
> chapter is `README.md` in this folder. Domain names, scores, and bot-block
> rows are intentional. Contact PII stripped.

# GEO Crawl Audit — 2026-08-25 vs 2026-08-07 Baseline

## VERDICT: ALL CLEAR on regressions — 1 OPEN ISSUE still open (htxpermitfix.com, day 18)

**No 402s anywhere. Vercel spend limit is healthy — all 18 domains served 200 to the baseline probe.**

### Baseline diff (18/18 domains)

| Domain | Baseline (08-07) | Now (08-25) | Δ |
|---|---|---|---|
| htxmaritimelaw.com | 88 | 88 | — |
| jonesactcalculator.com | 100 | 100 | — |
| htxdentalimplants.com | 100 | 100 | — |
| htxplasticsurgeon.com | 75 | 75 | — |
| houstonlawyerlist.com | 100 | 95 | −5 *(probe artifact — see below)* |
| htximmigrationlaw.com | 100 | 100 | — |
| abogadosinmigracionhtx.com | 100 | 100 | — |
| htxaccidentattorney.com | 70 | 70 | — |
| htxworkinjury.com | 100 | 100 | — |
| htxfoundationfix.com | 100 | 100 | — |
| htxcommercialroofers.com | 70 | 70 | — |
| methyleneblueultra.com | 100 | 100 | — |
| yapword.com | 83 | 83 | — |
| midnightdev.dev | 100 | 100 | — |
| buylandfl.com | 100 | 100 | — |
| htxpermitfix.com | 80 | 80 | — |
| wordgameai.com | 100 | 100 | — |
| thatsmybest.com | 83 | 83 | — |

**Zero true regressions. Zero new CRITICAL flags. Zero improvements.** Portfolio is static since post-recovery baseline.

---

## OPEN ISSUE: htxpermitfix.com bot filtering — STILL PRESENT, but less severe than logged

Re-verified with 6-second spacing and cache-busted URLs to rule out probe-induced rate limiting:

| Bot | Category | Status | vs baseline |
|---|---|---|---|
| Browser baseline | — | **200** | — |
| GPTBot | training | **429** | ❌ persistent, deterministic |
| meta-externalagent | training | **429** | ❌ persistent, deterministic |
| Amazonbot | training/other | 403 → 403 → **200** | ⚠️ intermittent |
| **OAI-SearchBot** | **retrieval** | **200** | ✅ passing |
| **Claude-SearchBot / ClaudeBot** | **retrieval** | **200** | ✅ passing |
| **PerplexityBot** | **retrieval** | **200** | ✅ passing |

robots.txt is clean (`User-agent: * / Allow: /`). The 429/403 is coming from the WAF/edge layer, not robots.

**Business read:** every bot that drives *live citations* is getting through. The blocked pair are *training* crawlers. Impact is long-term model memory, not current AI-search visibility. The WAF fix is still worth landing — it's an 18-day-old known defect and 429s on a training bot compound quietly — but it does not belong on the same shelf as an outage. Priority: this week, not today.

**Fix:** allowlist `GPTBot` and `meta-externalagent` UAs (or their published IP ranges) in the WAF / bot-management rule. Amazonbot's flapping suggests a rate-limit threshold rather than a hard rule — raise or exempt it in the same pass.

---

## Verification notes — three flags in the raw report below are FALSE POSITIVES

The probe container's network egress showed intermittent TLS handshake failures (`SSL_ERROR_SYSCALL`) at roughly a 20% rate. These surfaced as bot-specific findings that do not reproduce:

- **houstonlawyerlist.com `NO_ROBOTS`** — robots.txt is present, valid, and explicitly `Allow: /` for GPTBot, ChatGPT-User, ClaudeBot, Claude-Web, PerplexityBot, Googlebot, Bingbot. Confirmed 9/12 successful fetches; the 3 failures were egress-side, and the identical failure rate reproduced against htxworkinjury.com, htxfoundationfix.com, and jonesactcalculator.com. **True score is 100 — no regression.**
- **methyleneblueultra.com `PROBE_ERROR` (Claude-User)** — 4/4 clean 200s on re-test at 0.24s TTFB. Not a block.
- **htxcommercialroofers.com `PROBE_ERROR` (Amazonbot)** — same egress artifact on an unlaunched placeholder. Ignore.

---

## Known/accepted — not re-alerting (per standing context)

- htxaccidentattorney.com, htxcommercialroofers.com — unlaunched "launching soon" placeholders (CSR_SHELL + no robots.txt expected)
- htxplasticsurgeon.com — known thin-HTML issue pending fix (CSR_SHELL, 100 words)
- yapword.com, thatsmybest.com — deliberate training-bot blocks in robots.txt
- htxmaritimelaw.com (311 words), thatsmybest.com (221 words) — known-thin homepages

## Health markers, portfolio-wide

- Median bot TTFB: **0.191s – 0.361s** across all 18 domains. Threshold is 1.2s. Nothing close to 499-abandon risk.
- Cold/warm TTFB gaps are negligible except jonesactcalculator.com (0.305s warm → 0.905s cold). Still well inside tolerance; worth a glance if it widens.
- 12 of 18 domains score a clean 100.

---
---

# GEO Crawl Audit

**Generated:** 2026-08-25 15:46 UTC  
**Method:** active multi-UA probe (see caveat at bottom)

## Portfolio scorecard

| Domain | Score | Raw HTML | Words | Warm TTFB | Cold TTFB | Bot TTFB (med) | Differentials | Sitemap |
|---|---|---|---|---|---|---|---|---|
| htxaccidentattorney.com | **70** | CSR_SHELL | 42 | 0.199s | 0.242s | 0.213s | — | ✗ |
| htxcommercialroofers.com | **70** | CSR_SHELL | 40 | 0.172s | 0.279s | 0.265s | — | ✗ |
| htxplasticsurgeon.com | **75** | CSR_SHELL | 100 | 0.229s | 0.458s | 0.214s | — | ✓ |
| htxpermitfix.com | **80** | SSR_FULL | 628 | 0.368s | 0.432s | 0.361s | 3 | ✓ |
| yapword.com | **83** | SSR_THIN | 234 | 0.199s | 0.222s | 0.212s | — | ✓ |
| thatsmybest.com | **83** | SSR_THIN | 221 | 0.268s | 0.198s | 0.221s | — | ✓ |
| htxmaritimelaw.com | **88** | SSR_THIN | 311 | 0.535s | 0.527s | 0.206s | — | ✓ |
| houstonlawyerlist.com | **95** | SSR_FULL | 3691 | 0.253s | 0.35s | 0.218s | — | ✗ |
| htxdentalimplants.com | **100** | SSR_FULL | 1344 | 0.273s | 0.0s | 0.247s | — | ✓ |
| jonesactcalculator.com | **100** | SSR_FULL | 1308 | 0.305s | 0.905s | 0.252s | — | ✓ |
| abogadosinmigracionhtx.com | **100** | SSR_FULL | 462 | 0.296s | 0.215s | 0.223s | — | ✓ |
| htxworkinjury.com | **100** | SSR_FULL | 1254 | 0.208s | 0.21s | 0.191s | — | ✓ |
| htximmigrationlaw.com | **100** | SSR_FULL | 467 | 0.423s | 0.262s | 0.231s | — | ✓ |
| htxfoundationfix.com | **100** | SSR_FULL | 891 | 0.26s | 0.269s | 0.242s | — | ✓ |
| midnightdev.dev | **100** | SSR_FULL | 1231 | 0.369s | 0.301s | 0.287s | — | ✓ |
| buylandfl.com | **100** | SSR_FULL | 2836 | 0.261s | 0.406s | 0.201s | — | ✓ |
| wordgameai.com | **100** | SSR_FULL | 2753 | 0.197s | 0.174s | 0.211s | — | ✓ |
| methyleneblueultra.com | **100** | SSR_FULL | 1230 | 0.246s | 0.264s | 0.243s | — | ✓ |

## Flags (worst first)

- **[CRITICAL] htxaccidentattorney.com** `CSR_SHELL` — only 42 visible words in raw HTML — invisible to non-JS AI crawlers
- **[CRITICAL] htxcommercialroofers.com** `CSR_SHELL` — only 40 visible words in raw HTML — invisible to non-JS AI crawlers
- **[CRITICAL] htxplasticsurgeon.com** `CSR_SHELL` — only 100 visible words in raw HTML — invisible to non-JS AI crawlers
- **[CRITICAL] htxpermitfix.com** `BOT_DIFFERENTIAL` — Amazonbot: status 403 vs baseline 200 — bot-sensitive filtering; confirm with logs
- **[HIGH] htxpermitfix.com** `BOT_DIFFERENTIAL` — GPTBot: status 429 vs baseline 200 — bot-sensitive filtering; confirm with logs
- **[HIGH] htxpermitfix.com** `BOT_DIFFERENTIAL` — meta-externalagent: status 429 vs baseline 200 — bot-sensitive filtering; confirm with logs
- **[HIGH] yapword.com** `ROBOTS_BLOCKS` — robots.txt blocks: GPTBot, ClaudeBot, Amazonbot, CCBot, Google-Extended, Applebot-Extended
- **[HIGH] thatsmybest.com** `ROBOTS_BLOCKS` — robots.txt blocks: GPTBot, ClaudeBot, Amazonbot, CCBot, Google-Extended, Applebot-Extended
- **[WARN] htxaccidentattorney.com** `NO_ROBOTS` — robots.txt missing or erroring
- **[WARN] htxcommercialroofers.com** `PROBE_ERROR` — Amazonbot: connection failed after retry (twice) — could be transient network or connection-level bot blocking; check logs, re-run to confirm
- **[WARN] htxcommercialroofers.com** `NO_ROBOTS` — robots.txt missing or erroring
- **[WARN] yapword.com** `THIN_HTML` — 234 visible words — thin for passage retrieval
- **[WARN] thatsmybest.com** `THIN_HTML` — 221 visible words — thin for passage retrieval
- **[WARN] htxmaritimelaw.com** `THIN_HTML` — 311 visible words — thin for passage retrieval
- **[WARN] houstonlawyerlist.com** `NO_ROBOTS` — robots.txt missing or erroring
- **[WARN] methyleneblueultra.com** `PROBE_ERROR` — Claude-User: connection failed after retry (twice) — could be transient network or connection-level bot blocking; check logs, re-run to confirm

## Per-domain detail

### htxaccidentattorney.com — 70/100

- Final URL: https://htxaccidentattorney.com/ · server: `Vercel` · cache: `HIT`
- Title: 'HTX Accident Attorney — Launching Soon' · H1: 'Houston personal injury representation — launching soon.' · JSON-LD blocks: 0
- llms.txt: no · sitemaps: 0

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.292s | — |
| OAI-SearchBot | retrieval | 200 | 0.306s | — |
| ChatGPT-User | user_fetch | 200 | 0.192s | — |
| ClaudeBot | training | 200 | 0.177s | — |
| Claude-SearchBot | retrieval | 200 | 0.236s | — |
| Claude-User | user_fetch | 200 | 0.23s | — |
| PerplexityBot | retrieval | 200 | 0.195s | — |
| Perplexity-User | user_fetch | 200 | 0.152s | — |
| bingbot | retrieval | 200 | 0.193s | — |
| Amazonbot | retrieval | 200 | 0.173s | — |
| CCBot | training | 200 | 0.319s | — |
| meta-externalagent | training | 200 | 0.303s | — |

### htxcommercialroofers.com — 70/100

- Final URL: https://htxcommercialroofers.com/ · server: `Vercel` · cache: `HIT`
- Title: 'HTX Commercial Roofers — Launching Soon' · H1: 'Commercial roofing for Houston — launching soon.' · JSON-LD blocks: 0
- llms.txt: no · sitemaps: 0

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.325s | — |
| OAI-SearchBot | retrieval | 200 | 0.193s | — |
| ChatGPT-User | user_fetch | 200 | 0.285s | — |
| ClaudeBot | training | 200 | 0.173s | — |
| Claude-SearchBot | retrieval | 200 | 0.173s | — |
| Claude-User | user_fetch | 200 | 0.296s | — |
| PerplexityBot | retrieval | 200 | 0.256s | — |
| Perplexity-User | user_fetch | 200 | 0.227s | — |
| bingbot | retrieval | 200 | 0.265s | — |
| Amazonbot | retrieval | 0 | 0.0s | — |
| CCBot | training | 200 | 0.543s | — |
| meta-externalagent | training | 200 | 0.27s | — |

### htxplasticsurgeon.com — 75/100

- Final URL: https://htxplasticsurgeon.com/ · server: `Vercel` · cache: `HIT`
- Title: 'HTX Plastic Surgeon | Elite Cosmetic Surgery Houston' · H1: 'Sculpt Your Ultimate Identity.' · JSON-LD blocks: 0
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.182s | — |
| OAI-SearchBot | retrieval | 200 | 0.244s | — |
| ChatGPT-User | user_fetch | 200 | 0.193s | — |
| ClaudeBot | training | 200 | 0.304s | — |
| Claude-SearchBot | retrieval | 200 | 0.221s | — |
| Claude-User | user_fetch | 200 | 0.245s | — |
| PerplexityBot | retrieval | 200 | 0.356s | — |
| Perplexity-User | user_fetch | 200 | 0.303s | — |
| bingbot | retrieval | 200 | 0.193s | — |
| Amazonbot | retrieval | 200 | 0.205s | — |
| CCBot | training | 200 | 0.207s | — |
| meta-externalagent | training | 200 | 0.152s | — |

### htxpermitfix.com — 80/100

- Final URL: https://htxpermitfix.com/ · server: `LiteSpeed` · cache: `None`
- Title: 'HTX Permit Fix | Houston Permit Problems? We Fix Them Fast.' · H1: 'Houston PermitProblems?\n                    We Fix Them.' · JSON-LD blocks: 2
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 429 | 0.368s | status 429 vs baseline 200 |
| OAI-SearchBot | retrieval | 200 | 0.388s | — |
| ChatGPT-User | user_fetch | 200 | 0.362s | — |
| ClaudeBot | training | 200 | 0.357s | — |
| Claude-SearchBot | retrieval | 200 | 0.581s | — |
| Claude-User | user_fetch | 200 | 0.346s | — |
| PerplexityBot | retrieval | 200 | 0.359s | — |
| Perplexity-User | user_fetch | 200 | 0.384s | — |
| bingbot | retrieval | 200 | 0.346s | — |
| Amazonbot | retrieval | 403 | 0.361s | status 403 vs baseline 200 |
| CCBot | training | 200 | 0.343s | — |
| meta-externalagent | training | 429 | 0.384s | status 429 vs baseline 200 |

### yapword.com — 83/100

- Final URL: https://yapword.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Yapword — Free Daily AI Word Game & Wordle Alternative' · H1: 'Yapword — the daily word game where an AI emperor roasts your guesses' · JSON-LD blocks: 2
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.249s | — |
| OAI-SearchBot | retrieval | 200 | 0.196s | — |
| ChatGPT-User | user_fetch | 200 | 0.208s | — |
| ClaudeBot | training | 200 | 0.214s | — |
| Claude-SearchBot | retrieval | 200 | 0.255s | — |
| Claude-User | user_fetch | 200 | 0.204s | — |
| PerplexityBot | retrieval | 200 | 0.211s | — |
| Perplexity-User | user_fetch | 200 | 0.221s | — |
| bingbot | retrieval | 200 | 0.248s | — |
| Amazonbot | retrieval | 200 | 0.29s | — |
| CCBot | training | 200 | 0.193s | — |
| meta-externalagent | training | 200 | 0.174s | — |

### thatsmybest.com — 83/100

- Final URL: https://thatsmybest.com/ · server: `Vercel` · cache: `HIT`
- Title: "That's My Best — do you actually know them?" · H1: 'Are you actually their best friend?' · JSON-LD blocks: 1
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.221s | — |
| OAI-SearchBot | retrieval | 200 | 0.223s | — |
| ChatGPT-User | user_fetch | 200 | 0.213s | — |
| ClaudeBot | training | 200 | 0.329s | — |
| Claude-SearchBot | retrieval | 200 | 0.269s | — |
| Claude-User | user_fetch | 200 | 0.177s | — |
| PerplexityBot | retrieval | 200 | 0.178s | — |
| Perplexity-User | user_fetch | 200 | 0.269s | — |
| bingbot | retrieval | 200 | 0.216s | — |
| Amazonbot | retrieval | 200 | 0.196s | — |
| CCBot | training | 200 | 0.254s | — |
| meta-externalagent | training | 200 | 0.221s | — |

### htxmaritimelaw.com — 88/100

- Final URL: https://htxmaritimelaw.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Houston Maritime Injury Lawyer | Jones Act Attorney 2026' · H1: 'Control Your Recovery.' · JSON-LD blocks: 1
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.194s | — |
| OAI-SearchBot | retrieval | 200 | 0.409s | — |
| ChatGPT-User | user_fetch | 200 | 0.215s | — |
| ClaudeBot | training | 200 | 0.243s | — |
| Claude-SearchBot | retrieval | 200 | 0.151s | — |
| Claude-User | user_fetch | 200 | 0.191s | — |
| PerplexityBot | retrieval | 200 | 0.235s | — |
| Perplexity-User | user_fetch | 200 | 0.178s | — |
| bingbot | retrieval | 200 | 0.148s | — |
| Amazonbot | retrieval | 200 | 0.962s | — |
| CCBot | training | 200 | 0.285s | — |
| meta-externalagent | training | 200 | 0.197s | — |

### houstonlawyerlist.com — 95/100

- Final URL: https://houstonlawyerlist.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Top 25 Houston Personal Injury Lawyers | HoustonLawyerList.com' · H1: 'Top 25 Houston Personal Injury Lawyers' · JSON-LD blocks: 0
- llms.txt: yes · sitemaps: 0

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.486s | — |
| OAI-SearchBot | retrieval | 200 | 0.209s | — |
| ChatGPT-User | user_fetch | 200 | 0.227s | — |
| ClaudeBot | training | 200 | 0.175s | — |
| Claude-SearchBot | retrieval | 200 | 0.206s | — |
| Claude-User | user_fetch | 200 | 0.339s | — |
| PerplexityBot | retrieval | 200 | 0.357s | — |
| Perplexity-User | user_fetch | 200 | 0.204s | — |
| bingbot | retrieval | 200 | 0.196s | — |
| Amazonbot | retrieval | 200 | 1.047s | — |
| CCBot | training | 200 | 0.167s | — |
| meta-externalagent | training | 200 | 0.625s | — |

### htxdentalimplants.com — 100/100

- Final URL: https://htxdentalimplants.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Dental Implants Houston TX | Find & Compare Top Specialists | HTX Dental Implants' · H1: 'Stop Hiding Your Smile. Compare Houston Implant Dentists.' · JSON-LD blocks: 2
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.266s | — |
| OAI-SearchBot | retrieval | 200 | 0.269s | — |
| ChatGPT-User | user_fetch | 200 | 0.203s | — |
| ClaudeBot | training | 200 | 0.234s | — |
| Claude-SearchBot | retrieval | 200 | 0.202s | — |
| Claude-User | user_fetch | 200 | 0.183s | — |
| PerplexityBot | retrieval | 200 | 0.249s | — |
| Perplexity-User | user_fetch | 200 | 0.268s | — |
| bingbot | retrieval | 200 | 0.246s | — |
| Amazonbot | retrieval | 200 | 0.252s | — |
| CCBot | training | 200 | 0.34s | — |
| meta-externalagent | training | 200 | 0.236s | — |

### jonesactcalculator.com — 100/100

- Final URL: https://www.jonesactcalculator.com/ · server: `Vercel` · cache: `MISS`
- Title: 'Jones Act Settlement Calculator ($250K–$6M) | Free 2026' · H1: 'Jones Act Settlement Calculator.' · JSON-LD blocks: 3
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.242s | — |
| OAI-SearchBot | retrieval | 200 | 0.274s | — |
| ChatGPT-User | user_fetch | 200 | 0.251s | — |
| ClaudeBot | training | 200 | 0.264s | — |
| Claude-SearchBot | retrieval | 200 | 0.286s | — |
| Claude-User | user_fetch | 200 | 0.232s | — |
| PerplexityBot | retrieval | 200 | 0.29s | — |
| Perplexity-User | user_fetch | 200 | 0.252s | — |
| bingbot | retrieval | 200 | 0.203s | — |
| Amazonbot | retrieval | 200 | 0.236s | — |
| CCBot | training | 200 | 0.233s | — |
| meta-externalagent | training | 200 | 0.397s | — |

### abogadosinmigracionhtx.com — 100/100

- Final URL: https://abogadosinmigracionhtx.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Abogados de Inmigración Houston TX | Defensa contra Deportación 24/7' · H1: 'Detenga la Deportación.Proteja a su Familia.' · JSON-LD blocks: 0
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.244s | — |
| OAI-SearchBot | retrieval | 200 | 0.237s | — |
| ChatGPT-User | user_fetch | 200 | 0.208s | — |
| ClaudeBot | training | 200 | 0.211s | — |
| Claude-SearchBot | retrieval | 200 | 0.252s | — |
| Claude-User | user_fetch | 200 | 0.219s | — |
| PerplexityBot | retrieval | 200 | 0.211s | — |
| Perplexity-User | user_fetch | 200 | 0.235s | — |
| bingbot | retrieval | 200 | 0.227s | — |
| Amazonbot | retrieval | 200 | 0.2s | — |
| CCBot | training | 200 | 0.218s | — |
| meta-externalagent | training | 200 | 0.32s | — |

### htxworkinjury.com — 100/100

- Final URL: https://htxworkinjury.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Work Injury Lawyer Houston | Free Claim Calculator 2026' · H1: 'Houston WorkInjury Lawyer' · JSON-LD blocks: 5
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.428s | — |
| OAI-SearchBot | retrieval | 200 | 0.161s | — |
| ChatGPT-User | user_fetch | 200 | 0.182s | — |
| ClaudeBot | training | 200 | 0.177s | — |
| Claude-SearchBot | retrieval | 200 | 0.145s | — |
| Claude-User | user_fetch | 200 | 0.201s | — |
| PerplexityBot | retrieval | 200 | 0.23s | — |
| Perplexity-User | user_fetch | 200 | 0.277s | — |
| bingbot | retrieval | 200 | 0.199s | — |
| Amazonbot | retrieval | 200 | 0.171s | — |
| CCBot | training | 200 | 0.219s | — |
| meta-externalagent | training | 200 | 0.177s | — |

### htximmigrationlaw.com — 100/100

- Final URL: https://htximmigrationlaw.com/ · server: `Vercel` · cache: `HIT`
- Title: 'HTX Immigration Law | Houston Immigration Defense Attorneys' · H1: 'Detenga la Deportación.Proteja a su Familia.' · JSON-LD blocks: 0
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.201s | — |
| OAI-SearchBot | retrieval | 200 | 0.225s | — |
| ChatGPT-User | user_fetch | 200 | 0.219s | — |
| ClaudeBot | training | 200 | 0.228s | — |
| Claude-SearchBot | retrieval | 200 | 0.321s | — |
| Claude-User | user_fetch | 200 | 0.249s | — |
| PerplexityBot | retrieval | 200 | 0.949s | — |
| Perplexity-User | user_fetch | 200 | 0.301s | — |
| bingbot | retrieval | 200 | 0.16s | — |
| Amazonbot | retrieval | 200 | 0.158s | — |
| CCBot | training | 200 | 0.234s | — |
| meta-externalagent | training | 200 | 0.239s | — |

### htxfoundationfix.com — 100/100

- Final URL: https://htxfoundationfix.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Foundation Repair Houston TX | Free Evaluation, $0 Down | HTX Foundation Fix' · H1: 'Stop the Shift.Secure Your Equity.' · JSON-LD blocks: 1
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.212s | — |
| OAI-SearchBot | retrieval | 200 | 0.254s | — |
| ChatGPT-User | user_fetch | 200 | 0.23s | — |
| ClaudeBot | training | 200 | 0.27s | — |
| Claude-SearchBot | retrieval | 200 | 0.185s | — |
| Claude-User | user_fetch | 200 | 0.283s | — |
| PerplexityBot | retrieval | 200 | 0.231s | — |
| Perplexity-User | user_fetch | 200 | 0.297s | — |
| bingbot | retrieval | 200 | 0.147s | — |
| Amazonbot | retrieval | 200 | 0.254s | — |
| CCBot | training | 200 | 0.289s | — |
| meta-externalagent | training | 200 | 0.23s | — |

### midnightdev.dev — 100/100

- Final URL: https://midnightdev.dev/ · server: `cloudflare` · cache: `HIT`
- Title: 'Alex Bouchard — Forward-Deployed AI Lead · MidnightDev | ReadableByAI, Yapword | $400M CRE' · H1: 'I build AI products—and the systems that get them discovered, measured, and used.' · JSON-LD blocks: 2
- llms.txt: no · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.304s | — |
| OAI-SearchBot | retrieval | 200 | 0.265s | — |
| ChatGPT-User | user_fetch | 200 | 0.312s | — |
| ClaudeBot | training | 200 | 0.222s | — |
| Claude-SearchBot | retrieval | 200 | 0.31s | — |
| Claude-User | user_fetch | 200 | 0.278s | — |
| PerplexityBot | retrieval | 200 | 0.23s | — |
| Perplexity-User | user_fetch | 200 | 0.247s | — |
| bingbot | retrieval | 200 | 0.296s | — |
| Amazonbot | retrieval | 200 | 0.331s | — |
| CCBot | training | 200 | 0.3s | — |
| meta-externalagent | training | 200 | 0.251s | — |

### buylandfl.com — 100/100

- Final URL: https://buylandfl.com/ · server: `None` · cache: `None`
- Title: 'Florida Land Buyers | We Buy Vacant Land for Cash — Fast Closing' · H1: 'Land Buyers in Florida\n                    We Buy Land for Cash' · JSON-LD blocks: 1
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.243s | — |
| OAI-SearchBot | retrieval | 200 | 0.172s | — |
| ChatGPT-User | user_fetch | 200 | 0.572s | — |
| ClaudeBot | training | 200 | 0.174s | — |
| Claude-SearchBot | retrieval | 200 | 0.198s | — |
| Claude-User | user_fetch | 200 | 0.201s | — |
| PerplexityBot | retrieval | 200 | 0.213s | — |
| Perplexity-User | user_fetch | 200 | 0.193s | — |
| bingbot | retrieval | 200 | 0.211s | — |
| Amazonbot | retrieval | 200 | 0.165s | — |
| CCBot | training | 200 | 0.222s | — |
| meta-externalagent | training | 200 | 0.2s | — |

### wordgameai.com — 100/100

- Final URL: https://wordgameai.com/ · server: `Vercel` · cache: `HIT`
- Title: '9 Best AI Word Games in 2026 (Free Games You Can Actually Play)' · H1: "9 Best AI Word Games in 2026 (That Aren't Just ChatGPT Prompts)" · JSON-LD blocks: 5
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.185s | — |
| OAI-SearchBot | retrieval | 200 | 0.188s | — |
| ChatGPT-User | user_fetch | 200 | 0.216s | — |
| ClaudeBot | training | 200 | 0.271s | — |
| Claude-SearchBot | retrieval | 200 | 0.224s | — |
| Claude-User | user_fetch | 200 | 0.208s | — |
| PerplexityBot | retrieval | 200 | 0.215s | — |
| Perplexity-User | user_fetch | 200 | 0.228s | — |
| bingbot | retrieval | 200 | 0.484s | — |
| Amazonbot | retrieval | 200 | 0.199s | — |
| CCBot | training | 200 | 0.198s | — |
| meta-externalagent | training | 200 | 0.199s | — |

### methyleneblueultra.com — 100/100

- Final URL: https://methyleneblueultra.com/ · server: `Vercel` · cache: `HIT`
- Title: 'Methylene Blue Ultra: USP Methylene Blue Capsules for Biomarker Tracking' · H1: 'The Methylene Blue Supplement with Proof.' · JSON-LD blocks: 4
- llms.txt: yes · sitemaps: 1

| Bot | Cat | Status | TTFB | Differential |
|---|---|---|---|---|
| GPTBot | training | 200 | 0.22s | — |
| OAI-SearchBot | retrieval | 200 | 0.26s | — |
| ChatGPT-User | user_fetch | 200 | 0.271s | — |
| ClaudeBot | training | 200 | 0.24s | — |
| Claude-SearchBot | retrieval | 200 | 0.228s | — |
| Claude-User | user_fetch | 0 | 0.0s | — |
| PerplexityBot | retrieval | 200 | 0.264s | — |
| Perplexity-User | user_fetch | 200 | 0.439s | — |
| bingbot | retrieval | 200 | 0.243s | — |
| Amazonbot | retrieval | 200 | 0.242s | — |
| CCBot | training | 200 | 0.263s | — |
| meta-externalagent | training | 200 | 0.24s | — |


---
### Method caveat
Probes are sent from this machine's IP with simulated bot user-agents. WAFs that verify bots by IP range may treat the simulation differently than the real crawler (in either direction). A differential here means *a bot-sensitive filtering layer exists* — confirm actual bot outcomes with server logs via `drain_parser.py`.