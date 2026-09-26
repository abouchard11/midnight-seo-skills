# ChatGPT search-query probe harness

Tools for capturing and extracting the web-search queries and result
rankings ChatGPT issues when it browses the web (`web.run`), so query
drift and ranking changes for our sites can be tracked over time.

Files:

- `extract_queries.py` -- stdlib-only Python 3 extractor. Reads one or
  more saved conversation JSON files (or stdin) and prints JSONL, one
  line per conversation, to stdout. Extraction walks the ACTIVE
  conversation path only (`current_node` back to the root via `parent`
  pointers, reversed to chronological order); abandoned/regenerated
  branches recorded in `mapping` are skipped, not harvested.
- `fixtures/thinking_route.json`, `fixtures/fast_route.json`,
  `fixtures/code_route.json` -- minimal synthetic conversations
  exercising every extraction path (thinking-route metadata/JSON-blob,
  fast-route `content["parts"]` DSL, and code-route `content["text"]`
  DSL), each with a `current_node` and `code_route.json` additionally
  carrying an abandoned branch that must not appear in the output.
- `test_extract.py` -- test suite covering all three fixtures, the
  tree-walk/abandoned-branch behavior, and malformed-input handling, plus
  direct unit tests against the extractor's functions. Works both as a
  plain script (`python3 test_extract.py`) and under pytest
  (`python3 -m pytest test_extract.py`).

## (a) Methodology warning: use temporary chats only

**Every ranking probe must be run in a temporary chat, logged out of any
memory-carrying context, or otherwise memory-disabled.** A logged-in
ChatGPT account with memory turned on will silently rewrite what gets
searched: it injects prior conversation history, saved memories, and
inferred user profile into the query the model actually issues to
`web.run`. Two people (or the same person on different days) asking the
"same" question will not get the same probe queries or the same result
ranking once memory is contaminating the input.

For a clean, reproducible probe:

- Start a **Temporary Chat** (ChatGPT > New temporary chat), which runs
  with memory and chat history off for that conversation.
- If you can't use Temporary Chat for some reason, at minimum turn off
  "Reference saved memories" and "Reference chat history" in Settings >
  Personalization before probing, and treat the run as lower-confidence.
- Don't reuse a probe conversation for a second, differently-phrased
  question -- start a fresh temporary chat per probe so history within
  the conversation itself doesn't bias later turns.
- Record which account/plan tier ran the probe (free/Plus/Pro can route
  to different search backends) alongside the JSONL date field.

## (b) How to capture a conversation JSON

1. Ask your probe question in a Temporary Chat and **let the answer
   finish completely** (including any citations/sources rendering).
2. **Reload the conversation** (refresh the page, or navigate away and
   back to the same conversation URL). The initial page load re-fetches
   the full conversation from the backend, which is the request we want
   to capture -- don't try to catch the incremental streaming requests
   from the first turn.
3. Open **DevTools > Network** *before* the reload finishes (open
   DevTools first, then reload) and filter by **Fetch/XHR**.
4. Find the request `GET /backend-api/conversation/<conversation-id>`.
5. Right-click the request > **Copy** > **Copy response** (not "Copy as
   cURL" -- you want the JSON body itself).
6. Paste into a file, e.g. `probes/2026-08-07-yapword-founder.json`.
7. Run the extractor and append to your running log:

   ```bash
   python3 extract_queries.py probes/2026-08-07-yapword-founder.json >> probes.jsonl
   ```

   You can pass multiple files at once (`extract_queries.py f1.json
   f2.json ...`), or pipe a single conversation JSON in via stdin:

   ```bash
   cat probes/2026-08-07-yapword-founder.json | python3 extract_queries.py >> probes.jsonl
   ```

   By default the `date` field on each output line is today's date. To
   backfill or correct it (e.g. re-processing an older capture), pass
   `--date YYYY-MM-DD`:

   ```bash
   python3 extract_queries.py --date 2026-08-01 probes/old-capture.json >> probes.jsonl
   ```

## (c) Alternative: fetch-hook to grab the response automatically

If you'd rather not hunt through the Network panel every time, paste
this into the DevTools **Console** immediately after navigating to (or
reloading) the conversation page -- it must run **before the app's own
request fires**, so paste it right after the URL bar shows the new page
loading, not after the answer has already appeared:

```js
(() => {
  if (window.__probesHooked) return;
  window.__probesHooked = true;
  window.__probes = window.__probes || [];

  const origFetch = window.fetch;
  window.fetch = async (...args) => {
    const response = await origFetch(...args);
    try {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
      if (url && /\/backend-api\/conversation\//.test(url)) {
        const clone = response.clone();
        clone.json().then((data) => {
          window.__probes.push({ url, capturedAt: new Date().toISOString(), data });
          console.log("[probe] captured", url, data);
        }).catch(() => {});
      }
    } catch (e) {
      // never let the hook break the app
    }
    return response;
  };
  console.log("[probe] fetch hook installed -- reload the conversation now");
})();
```

After reloading, `window.__probes` holds every captured response. Pull
the JSON back out with:

```js
copy(JSON.stringify(window.__probes[window.__probes.length - 1].data));
```

then paste the clipboard contents into a `.json` file and run
`extract_queries.py` on it as above.

This is a convenience, not a replacement for step (b) -- if the hook
gets installed late (after the app's own `fetch` call has already fired
and been captured by ChatGPT's own code), you'll just fall back to
reloading and using DevTools Network directly.

## (d) The websocket stream exists but is not the reliable path

ChatGPT also maintains a websocket connection at
`wss://ws.chatgpt.com/p21/ws/user/<user-id>` used for realtime delivery
(e.g. background/async responses, notifications). Frames on this socket
carry `encoded_item` payloads that are server-sent-event-style encoded
chunks of a response, not a clean conversation JSON document. It's
fragile to depend on: the encoding has changed across ChatGPT releases,
not every turn goes over it (interactive turns are usually plain HTTP
streaming), and reconstructing a full `mapping` from partial frames is
brittle.

**Reload-and-extract (option b) is the reliable path.** Treat the
websocket as a debugging curiosity, not a capture mechanism, unless a
future need specifically requires realtime capture and justifies the
extra fragility.

## (e) JSONL schema

One line per conversation processed, keyed by `date` so query drift and
rank changes are trackable over time (append new runs to the same
`probes.jsonl` file rather than overwriting):

```json
{
  "date": "2026-08-07",
  "conversation_id": "c1111111-aaaa-4bbb-8ccc-111122223333",
  "title": "Researching Yapword founder background",
  "queries": [
    {"q": "Yapword founder", "source": "system1", "freshness_days": null},
    {"q": "Yapword founder daily AI word game", "source": "search_queries", "freshness_days": null}
  ],
  "results": [
    {"url": "https://yapword.com/about", "title": "About Yapword", "rank": 1, "domain": "google.com", "type": "search_result_group"}
  ]
}
```

Field notes:

- `date` -- the run date (today's date unless overridden with
  `--date`), **not** extracted from the conversation itself. This is
  what you filter/group on to track drift across runs.
- `conversation_id` -- from the conversation JSON's top-level
  `conversation_id` (falls back to `id` if absent); `null` if neither
  is present.
- `title` -- the conversation's title as ChatGPT rendered it, verbatim.
- `queries[]` -- deduped (by exact query text + source + freshness
  window -- so two probes of the same text with a different freshness
  window or extraction route both survive), order preserved as first
  encountered while walking the ACTIVE conversation path (`current_node`
  back to the root, chronological order; abandoned/regenerated branches
  are excluded entirely):
  - `q` -- the literal query/command-argument string.
  - `source` -- which extraction path produced it:
    - `"search_queries"` -- thinking-route `metadata.search_queries`.
    - `"system1"` -- thinking-route `system1_search_query` JSON blob
      embedded in a content part.
    - `"fast_dsl"` -- fast-route pipe-delimited DSL line found in a
      `content_type: "text"` content's `parts` array
      (`fast|find|search|open`).
    - `"code_dsl"` -- the same pipe-delimited DSL, but carried in a
      `content_type: "code"` content's `text` field (no `parts`) --
      the shape a real assistant-to-`web.run` tool-call payload uses.
  - `freshness_days` -- integer freshness window in days if the
    DSL line specified one (its optional third field), otherwise `null`.
- `results[]` -- every `search_result_groups` entry found on the active
  path, deduped by `url` (a URL already emitted doesn't consume another
  rank slot -- guards against a result group echoed on more than one
  message double-counting), flattened into a single global rank order
  (rank is 1-based and continues across multiple result groups/messages,
  it is not per-group):
  - `url`, `title` -- as returned by the search tool.
  - `rank` -- 1-based position in the flattened, deduped result order.
  - `domain`, `type` -- included only when the source result group
    carried them (some groups omit `domain`).

To spot week-over-week drift, `jq` against the accumulated log works
well, e.g.:

```bash
# All queries ever issued for a given date
jq -c 'select(.date == "2026-08-07") | .queries[]' probes.jsonl

# Rank history for a specific URL across every run
jq -c '.date as $d | .results[] | select(.url == "https://yapword.com/about") | {date: $d, rank}' probes.jsonl
```
