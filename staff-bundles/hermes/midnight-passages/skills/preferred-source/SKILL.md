---
name: preferred-source
description: Google Preferred Sources — eligibility, JS popup embed, placement, and a do-not-force fit verdict per domain
when_to_use: Use when adding Google Preferred Sources to a site, checking if a domain is eligible, generating the publisher.js snippet, or deciding whether a property should get the button at all. Also when the user asks about preferred sources, the Google source badge, AI Overviews labels, or "the Edward Sturm button".
argument-hint: "<domain>"
---

# Preferred Source

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice defined there to all output.

**Also read:** `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference.

This is an opt-in ranking *frequency and badge* signal. It does not override relevance. It is not a blog program, not a Map Pack substitute, and not a CTA to wallpaper onto every property in a portfolio.

Docs: https://developers.google.com/search/docs/appearance/preferred-sources

## Do not force it

Issue a **fit verdict** before any snippet.

| Verdict | Site type | Action |
|---|---|---|
| **SHIP** | Newsroom, magazine, research/explainers, company writing on the **root host** | JS popup on the pages people actually finish |
| **MAYBE** | Local-service site on the root domain; SaaS/product with real articles on the same host | One button on the 2–3 highest-intent public pages. Not the main lever versus Map Pack or BOFU pages |
| **SKIP** | Game, dashboard, calculator-as-app, login-walled tool, `example.com/blog` subdirectory | Print why, stop. Do not invent a blog so you have somewhere to paste the div |

Eligibility is the **host**, not a folder. `example.com` and `shop.example.com` can be preferred sources. `example.com/blog` cannot — that path is not a source. Subdomains are separate sources from the root.

Do **not** recommend starting informational blogs. Core.md still holds: purchase-intent pages, short, above-the-fold CTA. If the domain already publishes crawlable pages Google can treat as a source, the button goes on those pages. If it doesn't, skip.

## Step 1: Parse Domain

Extract the domain. Strip protocol, www, trailing slash, lowercase. Resolve against MCP Routing Map.

Flag:
- subdirectory in the input → **SKIP** (ineligible)
- localhost / IP → **SKIP**
- subdomain → eligible as its own source; note the root is separate

## Step 2: Pull Live Data

**GSC (PRIMARY for placement):**
1. Call `mcp__gscServer__get_search_analytics` — top 10 pages by clicks, last 28 days. These are the pages that earned the right to ask.

**GA4 (ENRICHMENT):**
2. Call `mcp__google-analytics__run_report` — top landing pages by sessions, last 28 days. Cross-check against GSC.

**CamoFox (ENRICHMENT, optional):**
3. If available, snapshot the homepage + the #1 GSC page. Check whether `news.google.com/swg/js/v1/publisher.js` or `google-add-preferred-source-btn` is already present. If the stealth browser is down: `[SEO] CamoFox unavailable — live-embed check skipped.`

If GSC is unavailable, warn and place on homepage + the two most obvious public article/service URLs from portfolio context. Do not guess a /blog.

## Step 3: Fit Verdict

**Section 1 — Verdict (SHIP / MAYBE / SKIP)**
One paragraph. Name the site type. If SKIP, stop after this section — no snippet, no fake calendar.

Local-service honesty: Map Pack and purchase-intent pages remain the 80/20. Preferred Sources is a secondary ask for people who already trust you (list, repeat visitors). A plumber does not need a newsroom strategy.

**Section 2 — Eligibility**
Host, subdomain vs root, subdirectory trap, public vs login-walled.

**Section 3 — Embed (only if SHIP or MAYBE)**
Recommend the **JavaScript popup**, not the old deeplink. The popup returns the reader to the article. The deeplink dumps them on Google.

Standard widget (default):

```html
<script async src="https://news.google.com/swg/js/v1/publisher.js"></script>
<div
  google-add-preferred-source-btn
  data-theme="light"
  data-lang="en"
></div>
```

Custom trigger (when the page already has a visual language — do not paste Google's badge onto a designed BOFU page):

```html
<script async preferred-sources-control="manual" src="https://news.google.com/swg/js/v1/publisher.js"></script>
<button type="button" id="preferred-source-btn">Add as a preferred source</button>
<script>
  (self.PREFERRED_SOURCE = self.PREFERRED_SOURCE || []).push(function (preferredSource) {
    preferredSource.init({ theme: "light", lang: "en" });
    var btn = document.querySelector("#preferred-source-btn");
    if (btn) btn.addEventListener("click", function () { preferredSource.addPreferredSource(); });
  });
</script>
```

Theme: `light` or `dark` to match the page. Lang: default `en` unless the site is not English.

**Section 4 — Placement (only if SHIP or MAYBE)**
Map the GSC top pages to slots. Do not recommend the footer.

1. After the first paragraph (highest intent)
2. End of the piece, before related posts
3. Share cluster (Google's own guidance: sit it next to other social CTAs)
4. Author bio, if the page has one

For MAYBE local-service: **one** slot on the top 2–3 converting pages. Not a sticky bar on the whole site.

**Section 5 — Copy and the list**
Give 2–3 lines the operator can paste. One of them must be for the **existing email list** — those readers already preferred you.

Example lines (rewrite to the vertical, keep them short):
- Lede: "If this is useful, add us as a preferred source on Google — it tells Search to show you more of this work."
- End: "Finished? One tap adds us as a preferred source. You'll see us more in Top Stories and AI Overviews."
- Email: "You already chose this list. One more tap so the same work shows up in Search."

**Section 6 — What this will not do**
- Will not buy position one
- Will not fix thin or off-intent pages
- Will not replace GBP / Map Pack for local
- Will not make a tool-only app into a publisher

## Step 4: Output

Follow the Output Protocol from core.md:
1. Print the full playbook to terminal
2. Extract structured summary
3. Save to Graphiti with name `Preferred Source — [domain]`

In Recommended Actions, the first item is the fit verdict. If SKIP, the only action is "do not ship."
