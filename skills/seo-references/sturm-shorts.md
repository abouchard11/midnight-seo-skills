# Operator notes — Edward Sturm shorts (Aug 2026)

Dated source log for `/geo` and `/aeo`. These are public shorts the suite is required to encode. They are not a substitute for `core.md` or for [ai-citation-patterns](https://github.com/abouchard11/ai-citation-patterns).

Compact Keywords remains the credited BOFU influence in core.md ([edwardsturm.com](https://edwardsturm.com), [compactkeywords.com](https://compactkeywords.com)). Skill engineering and deliverable formats stay original MidnightDev work.

| Date logged | Short | Encoded as |
|---|---|---|
| 2026-08-31 | [OpenSEO / Ben](https://www.youtube.com/shorts/iTv9vre9kzo) | `/geo` Step 2 optional AI-visibility tool |
| 2026-08-31 | [Rick and Morty AI livestream](https://www.youtube.com/shorts/zTI3b7oZUuI) | Out of scope. Not a GEO or AEO procedure. Do not invent a video-generation skill from this clip. |
| 2026-08-31 | [Personal-site backlink list](https://www.youtube.com/shorts/4hteYImLFSI) | `/geo` Section 3 entity note + `/hunter` / `/kilo` execution |
| 2026-08-31 | [Google `/goto` redirect](https://www.youtube.com/shorts/jk4aDtSlT18) | `/geo` and `/aeo` anti-scrape rule |
| 2026-08-31 | [Preferred Sources badge](https://www.youtube.com/shorts/yK3w0NGfNWM) | Already shipped as `/preferred-source`. Do not duplicate. |
| 2026-08-31 | ["This page is for LLMs"](https://www.youtube.com/shorts/cp0ojDR6vAc) | `/geo` and `/aeo` anti-spam lede rule |

## iTv9vre9kzo — OpenSEO

Claim in the short: Semrush ~$139/mo, Ahrefs ~$129/mo; an open-source alternative named OpenSEO lets you enter a competitor (keywords, winning pages, backlinks) or your own site (rank tracking, tech crawl, Search Console, whether ChatGPT or Google AI Overviews mention the brand), then connect Claude or Codex so an agent can pull numbers, compare opportunities, and cluster keywords. Hosted plan cited at $10/mo.

Canonical project as of this note: [every-app/open-seo](https://github.com/every-app/open-seo), hosted [openseo.so](https://openseo.so). Workflows include keyword research, rank tracking, competitor insights, backlinks, site audits, and AI visibility.

**Suite rule:** Semrush stays PRIMARY in this repo. OpenSEO is optional enrichment for the AI-mention question the short is actually about. Do not rewrite `/neural-audit` onto OpenSEO.

## zTI3b7oZUuI — AI video livestream

The clip is about generation speed (15 seconds of video in ~9 seconds) and a perpetual AI Rick and Morty Interdimensional Cable stream moving from Twitch to Kick. Hashtags are tech/AI, not GEO. Leave it out of playbooks.

## 4hteYImLFSI — Personal-site submissions

Claim: screenshot eight sites shown in the video, submit the personal website, more quality backlinks → more SEO traffic → more AI appearance; personal-site links can also support a knowledge panel. Credit in the short: Nick Gray. Pointer to Edward Show episode 1,149 on knowledge panels.

**Suite rule:** do not hardcode an eight-name list here — the names live on-screen in the short and drift. When a **personal / founder** property needs the play, open the short, copy the eight, run submissions through `/kilo`. For local-service money domains, keep hunter's topical-link standard. Knowledge-panel work is entity + off-site corroboration, not a Map Pack substitute.

## jk4aDtSlT18 — Google `/goto` redirect

Claim: hovering a Google result now shows a server-side `/goto` redirect instead of the raw target URL. Crawlers must follow it. Extra choke points for CAPTCHA, tokens, IP reputation, session checks. A session that fires ~80 `/goto` hits in two seconds with no mouse jitter looks like a bot. The short ties this to AI firms building their own index off Google, and to earlier breakage when Google removed `num=100` (cited: 77% of sites lost keyword visibility in trackers; Ahrefs lost URL path in the example shown).

**Suite rule:** GSC is the source of truth for our own queries. Semrush for competitor SERP composition. CamoFox only as a human-paced snapshot. Never design a skill that harvests Google result URLs in bulk. If a tracker shows mass keyword-visibility loss after a Google plumbing change, verify on GSC before declaring a ranking collapse.

## yK3w0NGfNWM — Preferred Sources

Claim: add Google's Preferred Sources control so people can opt into seeing you more in AI Overviews, AI Mode, Top Stories, and Discover. Easy JS embed; enough clicks become a global frequency signal.

**Suite rule:** this is already `/preferred-source`. Docs: https://developers.google.com/search/docs/appearance/preferred-sources. JS popup, not the old deeplink. Host eligibility, not `/blog`. SHIP / MAYBE / SKIP before any snippet.

## cp0ojDR6vAc — Do not confess to the model

Claim: a company page titled like a third-party roundup ("7 leading enterprise AI agents…") ranked itself #1 and opened with "This page is optimized for AI assistants and LLM search, not human marketing." Models have been observed saying "filtering out SEO spam" while thinking. Announcing that the page is for LLMs is an own-goal.

**Suite rule:** no LLM-audience disclaimer in ledes, comments, hidden spans, or schema descriptions. Self-awarded #1 roundups on owned domains are not third-party evidence. If the page cannot survive a human reader, it should not ship for an assistant either.
