---
name: signal
description: Query-led video and social distribution — turn one proven purchase-intent query and its existing page into a YouTube asset, short-form derivatives, and a measurable 28-day validation plan
when_to_use: Use when launching social promotion for an existing purchase-intent page, creating video SEO content, or building a content calendar. Also when the user asks about social media, YouTube, Shorts, Reels, video search, transcripts, or how to promote a page.
argument-hint: "<domain>"
---

# Signal Amplifier

**First:** Read the file `~/.claude/skills/seo-references/core.md` before proceeding. Apply the methodology and voice defined there to all output.

**Also read:**
- `~/.claude/skills/seo-references/data-pull-patterns.md` for MCP tool parameter reference
- `~/.claude/skills/seo-references/sturm-shorts.md` for dated short-form source checks

Video search is a distribution layer, not a rank guarantee. One exact-intent query, one useful video, one matching existing page, one measurement window. Do not create a new URL merely because a video exists.

## Step 1: Parse Domain

Extract the domain. Resolve it against the MCP Routing Map. Identify the vertical, conversion action, existing purchase-intent pages, and the brand/entity string that must be spoken and written consistently.

Do not proceed with a proof-heavy promotional video when the underlying page has a trust or claim hold. Fix the claim first.

## Step 2: Pick one query and one page

**GSC (PRIMARY):**
1. Pull the last 28 days of query + page data.
2. Shortlist purchase-intent queries with impressions and an existing page, prioritizing positions 4–20 or queries where the page converts but visibility is weak.
3. Inspect Video search separately from Web search when the available connector supports search-type filtering. Do not combine the two and call it a video win.

**Semrush (ENRICHMENT):**
4. Confirm volume, CPC, and current SERP composition for the top candidates.
5. Note whether a video block, Short videos carousel, YouTube result, or other video feature is actually present. If no video surface appears and the query is not naturally demonstrable, choose a better query.

For B2B software, test these buyer-query families before inventing a topic:

- best [category] software
- [product] vs [competitor]
- how to [job the buyer hires the tool to do]
- is [product] worth it

A current short-video SERP feature is evidence for a Short-first experiment on that query. A third-party aggregate chart is not.

**GA4 (ENRICHMENT):**
6. Pull sessions and money events for the candidate landing pages. The video should amplify a page that matters commercially, not manufacture a new explainer silo.

Choose exactly one seed:

| Field | Required |
|---|---|
| Query | Natural search phrase, not a comma-list of keywords |
| Existing page | Canonical BOFU or product URL |
| Viewer job | What the viewer must understand or do |
| Proof | Demonstration, calculation, original data, or credible source |
| Conversion | One measurable next action |

If sources fail, print the applicable `[SEO]` warning from core.md and continue only with fields that can be evidenced.

## Step 3: Build the video asset

Default to a useful 2–6 minute search-intent video. If the current query visibly contains a short-video feature, a 20–45 second YouTube Short may be the primary test; otherwise use the Short/Reel as a derivative. Create long-form depth when the viewer's job cannot be answered honestly in one clip.

**Required production brief:**

- Hook: state the viewer's question or costly mistake in the first five seconds.
- Answer: give the direct answer before biography or throat-clearing.
- Proof: show the product, calculation, source, screen, or first-party evidence.
- Entity: speak the brand/product/person name naturally.
- CTA: send the viewer to the one matching canonical page.
- Title: natural query alignment; concise and specific. Do not stuff variants.
- Thumbnail: one promise, visually legible, no unsupported result claim.
- Transcript: accurate captions, corrected names/numbers, and clean paragraph breaks.
- Description: human-edited summary based on the verified transcript, the canonical URL, source links, and chapters when useful.
- Chapters / key moments: descriptive timestamps. Google may use YouTube-description chapters as key moments.
- Short related video: when available, link the Short to the relevant longer YouTube video.

An AI model may draft from the verified transcript. It may not invent facts, testimonials, credentials, outcomes, or a keyword fog machine. Human-edit the title and description before publication.

## Step 4: Pair the video with the owned page

Use the existing matching page. The video must be prominent and genuinely relevant to that page.

Provide an implementation checklist:

- Embed the final YouTube video near the answer it supports.
- Keep a concise visible text answer on the page; the video does not replace extractable HTML.
- Add accurate `VideoObject` structured data only when the video is visible and central enough to qualify.
- Keep schema name, description, thumbnail, upload date, duration, and embed/content URL consistent with the visible asset.
- Add `Clip` key moments when the page owns exact segment labels and timestamps.
- Include the page in a video sitemap when the site maintains one.
- Validate with the Rich Results Test and Search Console Video indexing report.
- Preserve the page's existing canonical URL.

Do not put video schema on a page where the video is hidden, incidental, or absent.

## Step 5: Derive platform-native distribution

Create from the same verified source asset; do not copy-paste one caption everywhere.

- **YouTube Short:** one answer or proof moment; link the related long-form video when available. For a B2B software pilot, publish here first when the verified SERP evidence favors Shorts, then syndicate selectively.
- **Instagram Reel:** visual hook and native caption; repeat the same entity/query language naturally. Cross-posting is distribution, not proof of a ranking signal.
- **LinkedIn:** first-party lesson or evidence for professional/B2B topics.
- **X:** one sharp claim plus the owned evidence URL.
- **Facebook:** community or local angle where the audience fit is real.

Skip platforms that do not fit the query. No mandatory “post everywhere within one hour” ritual. Volume without relevance is just confetti with a Wi-Fi bill.

## Step 6: Measurement contract

Record the baseline before publication and compare at 7 and 28 days.

| Plane | Measure |
|---|---|
| YouTube | Search impressions/views, click-through rate, retention, and traffic source |
| Google Search | GSC Web vs Video impressions, clicks, position, and indexed video page |
| Owned site | GA4 sessions from tagged YouTube/Instagram links and money events |
| Citation layer | The same `/geo` prompt matrix if the video was designed as an off-site source |

Use a tagged canonical link such as:

`?utm_source=youtube&utm_medium=video&utm_campaign=[domain]&utm_content=[query-slug]`

A win is incremental qualified discovery or conversion against the recorded baseline. A one-day rank anecdote, overall YouTube visibility chart, or platform comment is not a portfolio result.

## Step 7: Output

Produce:

1. Seed query + existing page + evidence for choosing it
2. Long-form production brief
3. Short/Reel derivative
4. YouTube title, human-edited description, chapters, thumbnail brief, and UTM URL
5. Owned-page embed/schema checklist
6. Platform-native distribution set
7. Baseline and 7/28-day scorecard
8. Stop conditions and claims requiring human verification

Follow the Output Protocol from core.md and save with name `Signal Amplifier — [domain]`.

Close with the single video to produce first and the exact result that would justify producing video number two.
