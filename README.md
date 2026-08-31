# midnight-seo-skills

Claude Code skill suite for running SEO operations across a portfolio of local-service and niche sites: auditing, topical mapping, link acquisition, local pack strategy, analytics wiring, rapid indexing, and AI-search citation/answer work (GEO + AEO).

Built and maintained by [Alex Bouchard](https://github.com/abouchard11) ([MidnightDev](https://midnightdev.dev)). Extracted from the skill set I run daily against my own portfolio; the working examples use Houston as the metro because that is where I operate. Swap in your own market via the configuration described below.

## Skills

| Skill | What it does |
|---|---|
| `neural-audit` | Portfolio-wide SEO audit: authority, traffic, keyword coverage, and deployment status per domain (Semrush + GSC + GA4) |
| `topical-map` | Generates the 13-page architecture per domain: 1 hub, 3 sub-hubs, 9 purchase-intent pages, prioritized by volume x CPC |
| `indexer` | GSC rapid-indexing protocol: sitemap hygiene, URL inspection workflow, post-publish checklist |
| `signal` | Social distribution plan for new pages: platform-specific posts, scheduling, tracking |
| `preferred-source` | Google Preferred Sources: eligibility, JS popup embed, placement. Issues a SHIP / MAYBE / SKIP verdict so the button is not wallpapered onto tools, games, or `/blog` paths |
| `geo-crawl` | Thin mount of [geo-crawl-audit](https://github.com/abouchard11/geo-crawl-audit): can retrieval bots reach, fetch, and read the host. Hard preflight before `/geo`. Does not fork the probe |
| `geo` | Generative Engine Optimization: prompt-probe matrix across ChatGPT, Perplexity, Gemini, Claude, and AI Mode; citation vs mention vs absent; on-page citability on BOFU pages |
| `aeo` | Answer Engine Optimization: extractable passages for featured snippets, People Also Ask, voice, and the short AI Overview block — still on purchase-intent pages |
| `hunter` | Backlink gap analysis: referring-domain audit, link targets, linkable-asset specs |
| `kilo` | Executable link acquisition: outreach sequences, broken-link targets, resource-page submissions, journalist pitches |
| `parasite` | Parasite SEO: publish on high-authority platforms to capture SERPs a new domain cannot win head-to-head |
| `whale` | New-domain discovery: exact-match local-service domains validated with real volume and CPC data |
| `map-flap` | Google Map Pack strategy for local sub-markets: GBP optimization plus a geo-grid attack plan |
| `ga4` | GA4 telemetry wiring: track money events, not vanity metrics; UTM discipline and conversion gap checks |
| `seo-references` | Shared methodology core, MCP data-pull patterns, and dated Sturm-short operator notes used by all skills |

## Install

Copy each directory under `skills/` into `~/.claude/skills/`:

```bash
cp -R skills/* ~/.claude/skills/
```

Then invoke any skill from Claude Code, e.g. `/neural-audit yourdomain.com`.

`/geo-crawl` expects a local checkout of [geo-crawl-audit](https://github.com/abouchard11/geo-crawl-audit) so it can run `scripts/geo_probe.py`. It will not copy that engine into this repo. Public single-domain scan: [readablebyai.com](https://readablebyai.com).

## Configure

The skills read shared context from `~/.claude/skills/seo-references/core.md`:

1. Fill in the Portfolio Configuration table (your domains, analytics properties, and market focus).
2. Replace `{{CITY}}` / `{{CITY_ABBREV}}` placeholders with your metro where a skill uses them.

## Requirements

Designed around MCP servers for Semrush, Google Search Console, and GA4; several skills also use a stealth browser ([Camoufox](https://github.com/daijro/camoufox)) for SERP validation. Every skill degrades gracefully when a data source is unavailable; the failure-handling order lives in `seo-references/core.md`.

## Related

- [geo-crawl-audit](https://github.com/abouchard11/geo-crawl-audit) — ReadableByAI probe. Input side of GEO (reach, TTFB, raw HTML, robots, logs). `/geo-crawl` is the mount; `/geo` will not write citation copy on a STOP verdict.
- [ai-citation-patterns](https://github.com/abouchard11/ai-citation-patterns) — dated, sourced research on how AI answer engines select and cite content. `/geo` and `/aeo` are the execution paths.
- [claude-desktop-skills](https://github.com/abouchard11/claude-desktop-skills) — sibling skill suite for knowledge-work prompts; different layer than this SEO ops pack.

## Credits

Parts of the bottom-of-funnel approach were informed by Edward Sturm's publicly taught Compact Keywords framework ([edwardsturm.com](https://edwardsturm.com)). Dated operator notes from specific Aug 2026 shorts live in `skills/seo-references/sturm-shorts.md` and are executed by `/geo`, `/aeo`, and `/preferred-source`. The skill engineering, tool orchestration, and deliverable formats are original work.

## Rights

**Proprietary — all rights reserved. No license is granted.** See [LICENSE](LICENSE).
