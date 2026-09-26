# Measurement and tool capability note — 2026-09-02

Dated evidence note for `/ga4` and `/geo`. This is not a new skill or audit engine.

## Sources reviewed

- [Google Analytics Is Hiding Your AI Traffic (And Google Can Detect Your AI Content)](https://www.youtube.com/watch?v=NGHIvY_VKwc) and [Google's Goto Redirect Broke Rank Tracking. Moz Explains What Happens Now.](https://www.youtube.com/watch?v=arXkcZI6Eew). YouTube exposed no transcript in the review session, so the episode descriptions were treated only as topic pointers.
- [Known bot-traffic exclusion in Google Analytics](https://support.google.com/analytics/answer/9888366?hl=en), [default channel definitions](https://support.google.com/analytics/answer/9756891?hl=en), and [Google Analytics release notes](https://support.google.com/analytics/answer/9164320?hl=en).
- [SynthID](https://deepmind.google/models/synthid/) for participating-generation provenance and watermarking.
- [OpenSEO](https://github.com/every-app/open-seo) source at commit `ac9ee482d2b4cd8f472065d6f9b57db35cec560e` (package version `0.1.7`).

## 1. Keep GA4 and crawler telemetry separate

Google Analytics automatically excludes known bots and spiders. The exclusion cannot be disabled, and Analytics does not expose the removed volume. Therefore:

- GA4 measures tagged human sessions, including identifiable AI-referral click-through.
- Origin logs and verified ReadableByAI `rba_*` events measure crawler / retrieval reach.
- `/geo` repeated prompt probes measure citation, mention, and recommendation presence.
- Direct traffic is not a defensible proxy for "dark AI."
- A missing GA4 session is not evidence that a crawler did not fetch the site.
- A referral session is not evidence that the answer cited the site.

Keep AI Assistant, complementary referral regex, Organic Search landings, and money events together in the human-session report. Keep verified retrieval and user-fetch hits in a separate evidence table.

## 2. OpenSEO is enrichment, not the canonical plane

The current product is broad and useful: classic rank, keyword, backlink, local, site-audit, GSC, and GA4 workflows plus an AI-visibility UI. The source review found an important boundary:

- Brand Lookup, Prompt Explorer, cited sources, and Share of Voice exist in the application UI.
- The current MCP server registers standard SEO / analytics tools, not those AI-visibility functions.
- Hosted AI visibility is plan-gated.
- Self-hosting still requires paid DataForSEO usage; the documentation describes a small signup credit and a minimum top-up.

Decision: do not fork OpenSEO, copy its stack, or promise AI-visibility MCP calls that are not registered. Use it as optional cross-site enrichment. Preserve the canonical planes already in the suite:

| Question | Canonical plane |
|---|---|
| Can retrieval fetch and read the host? | `geo-crawl-audit` through `/geo-crawl` |
| Did a verified crawler reach origin? | Origin logs or ReadableByAI `rba_*` events |
| Did a human click through? | `/ga4` |
| What is the standard SEO baseline? | Semrush + GSC; OpenSEO may enrich |
| Is the brand actually cited? | `/geo` repeated prompt matrix |

## 3. The `/goto` change does not justify a scraper

The longer Moz discussion adds context, but it does not change this suite's architecture. GSC remains the first-party Google truth, paid providers remain the competitor layer, and browser checks stay human-paced validation. Do not build a replacement `/goto` scraper. Before reporting a rank collapse, verify whether the measurement path changed.

## 4. SynthID is provenance, not a universal SEO detector

SynthID can add or detect provenance signals for supported participating generation pipelines. That does not establish a universal detector for all AI-authored text, and it does not establish an SEO ranking penalty.

Retain human review, factual sourcing, bylines, original evidence, and brand voice. Do not add an "AI detector score" to the audit. Absence of a watermark is not proof that content was written by a human.

## Rejected additions

- A second analytics platform
- A fork of OpenSEO
- Crawler-demand inference from GA4
- Relabeling Direct as AI traffic
- Universal AI-detection or ranking-penalty claims
- A homegrown `/goto` rank scraper
