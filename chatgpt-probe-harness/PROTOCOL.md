# ChatGPT `web.run` probe — one-page protocol

Goal: capture the search queries ChatGPT actually issues, and the result
ranks it saw, so you can track query drift against your domains.

stdlib Python 3 only. No network calls in the extractor.

## 1. Isolate the chat

Every probe runs in a **Temporary Chat** (memory off, history off). A
logged-in account with memory on will rewrite the query. One question
per temporary chat. Record plan tier (free / Plus / Pro) — backends
differ.

## 2. Ask, finish, reload

Ask the probe question. Let citations finish rendering. Reload the
conversation (do not scrape the streaming turn).

## 3. Save the conversation JSON

DevTools → Network → Fetch/XHR →
`GET /backend-api/conversation/<id>` → Copy response (the JSON body).
Save as `probes/YYYY-MM-DD-<slug>.json`.

Optional: paste the fetch-hook from `README.md` into the console
*before* reload so `window.__probes` catches it.

Do not use the chatgpt websocket. It is not a reliable capture path.

## 4. Extract

```bash
python3 extract_queries.py probes/YYYY-MM-DD-<slug>.json >> probes.jsonl
# backfill an older capture:
python3 extract_queries.py --date 2026-08-07 probes/old.json >> probes.jsonl
```

Walks the **active** path only (`current_node` → root). Abandoned
branches in `mapping` are skipped.

## 5. Read the JSONL

One line per conversation: `date`, `conversation_id`, `title`,
`queries[]` (`q`, `source`, `freshness_days`), `results[]` (`url`,
`title`, `rank`, …).

```bash
jq -c 'select(.date == "2026-08-07") | .queries[]' probes.jsonl
jq -c '.date as $d | .results[] | select(.url | test("yourdomain")) | {date:$d, rank, url}' probes.jsonl
```

## 6. Verify the extractor

```bash
python3 test_extract.py
```

Fixtures under `fixtures/` cover thinking / fast / code routes plus an
abandoned branch that must not appear.

Full capture notes, hook snippet, and schema: `README.md`.
