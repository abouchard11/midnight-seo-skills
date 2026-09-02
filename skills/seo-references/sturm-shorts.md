# Operator notes — Edward Sturm short-form sources (2026)

Dated source log for `/geo` and `/aeo`. These are public short-form posts the suite has reviewed. They are not a substitute for `core.md` or for [ai-citation-patterns](https://github.com/abouchard11/ai-citation-patterns).

Compact Keywords remains the credited BOFU influence in core.md ([edwardsturm.com](https://edwardsturm.com), [compactkeywords.com](https://compactkeywords.com)). Skill engineering and deliverable formats stay original MidnightDev work.

| Date logged | Short | Encoded as |
|---|---|---|
| 2026-08-31 | [OpenSEO / Ben](https://www.youtube.com/shorts/iTv9vre9kzo) | `/geo` Step 2 optional AI-visibility tool |
| 2026-08-31 | [Rick and Morty AI livestream](https://www.youtube.com/shorts/zTI3b7oZUuI) | Out of scope. Not a GEO or AEO procedure. Do not invent a video-generation skill from this clip. |
| 2026-08-31 | [Personal-site backlink list](https://www.youtube.com/shorts/4hteYImLFSI) | `/geo` Section 3 entity note + `/hunter` / `/kilo` execution |
| 2026-08-31 | [Google `/goto` redirect](https://www.youtube.com/shorts/jk4aDtSlT18) | `/geo` and `/aeo` anti-scrape rule |
| 2026-08-31 | [Preferred Sources badge](https://www.youtube.com/shorts/yK3w0NGfNWM) | Already shipped as `/preferred-source`. Do not duplicate. |
| 2026-08-31 | ["This page is for LLMs"](https://www.youtube.com/shorts/cp0ojDR6vAc) | `/geo` and `/aeo` anti-spam lede rule |
| 2026-09-02 | [YouTube core-update opportunity](https://www.instagram.com/edward.builds/reel/DWtiID9DFU3/) | `/signal` query-led video protocol; 2,500% headline rejected as a durable claim |
| 2026-09-02 | [Short video in B2B SaaS SERPs](https://www.instagram.com/edward.builds/reel/DcwM5W1MmVa/) | `/signal` Short-first branch for verified video-feature queries |

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


## DWtiID9DFU3 — YouTube core-update opportunity

Claim in the April 4 Instagram reel: YouTube gained 2,500% after a Google core update; creators should make videos for searches important to the brand, use the exact search term naturally in the title, and turn the transcript into an SEO description.

**Evidence check logged 2026-09-02:**

- Query-led video production is a useful tactic when the SERP actually contains a video surface and the query maps to an existing purchase-intent page.
- The 2,500% figure was not accompanied by a reproducible denominator or source in the reel. “More clicks than there are clicks in Google” is evidence that a third-party estimation model or chart is being misread, not that arithmetic resigned.
- Lily Ray's later [March 2026 analysis](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/) using SISTRIX data described YouTube as the greatest absolute visibility loser in that update. The analysis explicitly distinguishes visibility estimates from raw traffic.
- [SE Ranking's May 2026 study](https://seranking.com/blog/google-may-2026-core-update-analysis/) found YouTube's ordinary top-three share declining from 2.50% after March to 2.14% after May, while noting that video may be moving into dedicated SERP features.
- Google documents [video SEO](https://developers.google.com/search/docs/appearance/video), [VideoObject and key moments](https://developers.google.com/search/docs/appearance/structured-data/video), and [video sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps). These are eligibility and understanding mechanisms, not ranking guarantees.

**Suite rule:** `/signal` owns the workflow. Do not create a separate YouTube-SEO skill. Pick one evidenced query and one existing BOFU page, produce a useful video plus a Short/Reel derivative, use an accurate human-edited transcript/description, add page-level video markup only where the video is prominent, and compare YouTube Analytics + GSC Web/Video + GA4 conversions at 7 and 28 days. No “rank in hours,” traffic-signal, or posting-volume promises.


## DcwM5W1MmVa — Short video in B2B SaaS SERPs

Claim in the September 1 Instagram reel: YouTube Shorts, Instagram Reels, and TikTok appear prominently for “best inventory management software,” “best ERP software,” “best project management software,” and “best scheduling software.” The proposed tactic is to put the buyer query at the start of the YouTube title and platform description, then add a rich description.

The figures closely match [Foundation's July 29 short-form B2B study](https://foundationinc.co/lab/short-form-video):

- Its tracked “best + software” set showed YouTube Shorts ranking for 587 keywords, up 117% across the displayed December–June window; Instagram reached 187 (+156%) and TikTok 140 (+192%) from smaller bases.
- It reports 475 U.S. “best + software” top-ten placements for YouTube Shorts, with roughly three in four at position one and about 108,000 combined monthly searches.
- It reports the four software-query examples named in the reel.
- It also reports AI Overviews on 92% of the result pages where its tracked YouTube Shorts appeared. That is co-occurrence, not proof that the Short caused or “fed” the AI answer.
- The article does not publish the full tracked keyword list or enough raw data in the public page to reproduce every aggregate. Treat the figures as a strong opportunity signal, not a universal platform guarantee.
- A same-day Google SERP verification attempt from the audit environment was stopped by Google's unusual-traffic screen. Do not encode the claimed live positions as independently observed.

**Suite rule:** extend the existing `/signal` branch; do not create another skill. For B2B software, inspect current SERP features for “best [category] software,” “[product] vs [competitor],” “how to [buyer job],” and “is [product] worth it.” When a short-video feature is present, allow a YouTube Short to be the primary experiment instead of forcing long-form first. Publish to YouTube first when the query evidence supports it, syndicate selectively to Instagram/TikTok, and measure the exact query at 7 and 28 days. Query alignment belongs in the title/description naturally; keyword stuffing and causal AI-citation claims do not.
