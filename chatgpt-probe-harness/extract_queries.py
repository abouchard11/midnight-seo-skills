#!/usr/bin/env python3
"""extract_queries.py -- pull web.run search queries + result ranks out of
ChatGPT conversation JSON (as returned by
GET https://chatgpt.com/backend-api/conversation/<conversation-id>).

stdlib only. No network calls, no third-party dependencies.

Usage:
    python3 extract_queries.py conv1.json conv2.json ... >> probes.jsonl
    cat conv.json | python3 extract_queries.py >> probes.jsonl
    python3 extract_queries.py --date 2026-08-07 conv.json >> probes.jsonl

Output: one JSON line per conversation processed (JSONL), shaped as:
    {
      "date": "<YYYY-MM-DD run date>",
      "conversation_id": "...",
      "title": "...",
      "queries": [{"q": "...", "source": "search_queries"|"system1"|"fast_dsl"|"code_dsl",
                    "freshness_days": <int|null>}, ...],
      "results": [{"url": "...", "title": "...", "rank": <int>,
                    "domain": "..." (if present), "type": "..." (if present)}, ...]
    }

Extraction walks the ACTIVE conversation path only: `current_node` back to
the root via `parent` pointers, then reversed to chronological order.
Abandoned/regenerated branches recorded in `mapping` but not on that path
are skipped, not harvested.

See README.md for the full methodology and capture procedure.
"""

import argparse
import datetime as dt
import json
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

# Fast-route DSL commands. Spec: field0 in {fast, search, find, open},
# field1 = query string, field2 (optional) = freshness window in days.
FAST_DSL_COMMANDS = {"fast", "search", "find", "open"}


# ---------------------------------------------------------------------------
# DSL / JSON payload parsing helpers
# ---------------------------------------------------------------------------

def _try_json(text: str) -> Optional[Any]:
    """Best-effort JSON parse. Never raises."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def _is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False


def parse_fast_dsl_lines(text: str) -> List[Tuple[str, str, Optional[int]]]:
    """Parse pipe-delimited fast-route DSL lines out of a content part.

    One command per line: field0 in {fast, search, find, open},
    field1 = query string, field2 (optional) = freshness window in days.
    Example: fast|"Yapword" founder daily AI word game|30

    The query field may legitimately contain a literal "|" itself (e.g. a
    quoted title with " | " in it). To avoid silently truncating that,
    only the LAST "|"-delimited segment after the command is treated as
    the optional freshness field, and only when it looks like one (blank,
    or an integer) -- otherwise the whole remainder is kept as the query,
    embedded pipes and all.

    Lines that don't match the shape (no pipe, unknown field0, empty
    query) are silently skipped -- this text may just be ordinary
    assistant prose that happens to contain a line break.
    """
    if not isinstance(text, str):
        return []
    out: List[Tuple[str, str, Optional[int]]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or "|" not in line:
            continue
        cmd_part, _sep, rest = line.partition("|")
        cmd = cmd_part.strip().lower()
        if cmd not in FAST_DSL_COMMANDS:
            continue
        if not rest:
            continue

        q = rest
        freshness_days: Optional[int] = None
        if "|" in rest:
            maybe_q, _sep2, maybe_fresh = rest.rpartition("|")
            maybe_fresh_stripped = maybe_fresh.strip()
            if maybe_fresh_stripped == "" or _is_int(maybe_fresh_stripped):
                q = maybe_q
                if maybe_fresh_stripped:
                    freshness_days = int(maybe_fresh_stripped)
            # else: the trailing segment doesn't look like a freshness
            # value (e.g. it's more query text after an embedded pipe),
            # so leave q = rest untouched -- keep the pipe.

        q = q.strip()
        if not q:
            continue
        out.append((cmd, q, freshness_days))
    return out


# ---------------------------------------------------------------------------
# Per-message extraction
# ---------------------------------------------------------------------------

def extract_queries_from_message(message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract queries from a single web.run-directed message.

    Covers all three known formats:
      (a) THINKING ROUTE: metadata.search_queries = [{"type":"search","q":...}]
          and/or a content part that is a JSON blob shaped like
          {"system1_search_query": [{"q": ...}]}.
      (b) FAST ROUTE: content_type "text" -- content.parts holding
          pipe-delimited DSL lines.
      (c) CODE ROUTE: content_type "code" -- content.text (NOT parts)
          holding pipe-delimited DSL lines. This is the shape a real
          assistant-to-web.run tool-call payload uses on a live capture:
          content keys are content_type/language/response_format_name/text,
          no "parts" array. Other content_types (e.g. "thoughts",
          "reasoning_recap") carry neither "parts" nor a matching "text"
          shape and are harmlessly skipped.
    """
    found: List[Dict[str, Any]] = []

    metadata = message.get("metadata")
    if isinstance(metadata, dict):
        search_queries = metadata.get("search_queries")
        if isinstance(search_queries, list):
            for item in search_queries:
                if isinstance(item, dict):
                    q = item.get("q")
                    if isinstance(q, str) and q:
                        found.append({"q": q, "source": "search_queries", "freshness_days": None})

    content = message.get("content")
    if isinstance(content, dict):
        if content.get("content_type") == "code":
            text = content.get("text")
            if isinstance(text, str):
                for _cmd, q, freshness_days in parse_fast_dsl_lines(text):
                    found.append({"q": q, "source": "code_dsl", "freshness_days": freshness_days})

        parts = content.get("parts")
        if isinstance(parts, list):
            for part in parts:
                if not isinstance(part, str):
                    continue

                parsed = _try_json(part)
                handled_as_json = False
                if isinstance(parsed, dict):
                    system1 = parsed.get("system1_search_query")
                    if isinstance(system1, list):
                        handled_as_json = True
                        for item in system1:
                            if isinstance(item, dict):
                                q = item.get("q")
                                if isinstance(q, str) and q:
                                    found.append({"q": q, "source": "system1", "freshness_days": None})
                if handled_as_json:
                    continue

                for _cmd, q, freshness_days in parse_fast_dsl_lines(part):
                    found.append({"q": q, "source": "fast_dsl", "freshness_days": freshness_days})

    return found


def extract_results_from_message(
    message: Dict[str, Any], rank_counter: int, seen_urls: set
) -> Tuple[List[Dict[str, Any]], int]:
    """Extract search result entries from a tool-response message carrying
    metadata.search_result_groups, continuing the running rank counter.

    `seen_urls` is a set of URLs already emitted earlier in this
    conversation (mutated in place). A URL already seen is dropped and
    does NOT consume a rank slot -- this guards against a result group
    echoed on more than one message double-counting and inflating every
    later rank.
    """
    results: List[Dict[str, Any]] = []

    metadata = message.get("metadata")
    if not isinstance(metadata, dict):
        return results, rank_counter

    groups = metadata.get("search_result_groups")
    if not isinstance(groups, list):
        return results, rank_counter

    for group in groups:
        if not isinstance(group, dict):
            continue
        entries = group.get("entries")
        if not isinstance(entries, list):
            continue
        domain = group.get("domain")
        gtype = group.get("type")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            url = entry.get("url")
            if not isinstance(url, str) or not url:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            rank_counter += 1
            title = entry.get("title")
            result: Dict[str, Any] = {
                "url": url,
                "title": title if isinstance(title, str) else None,
                "rank": rank_counter,
            }
            if isinstance(domain, str) and domain:
                result["domain"] = domain
            if isinstance(gtype, str) and gtype:
                result["type"] = gtype
            results.append(result)

    return results, rank_counter


# ---------------------------------------------------------------------------
# Whole-conversation extraction
# ---------------------------------------------------------------------------

def dedupe_queries(queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Dedupe on (query text, source, freshness_days), preserving
    first-seen order.

    Keying on query text alone would collapse two genuinely different
    probes of the same text -- e.g. the same query re-issued with a
    different freshness window, or reached via two different extraction
    routes -- discarding the second record's freshness_days/source
    silently. Widening the key avoids that while still collapsing true
    duplicates (identical text, source, and freshness).
    """
    seen = set()
    out: List[Dict[str, Any]] = []
    for item in queries:
        key = (item.get("q"), item.get("source"), item.get("freshness_days"))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _active_path_nodes(
    mapping: Dict[str, Any], current_node_id: Any
) -> Optional[List[Dict[str, Any]]]:
    """Return the node dicts on the ACTIVE conversation path -- walking
    from `current_node_id` back to the root via `parent` pointers, then
    reversed to chronological (oldest-first) order.

    Nodes recorded in `mapping` but not reachable on this path are
    abandoned/regenerated branches (e.g. a regenerated answer, an edited
    turn) and must be excluded from extraction.

    Returns None (rather than []) when the walk can't be performed at all
    -- `current_node_id` missing/not a string, or not present in
    `mapping` -- so the caller can fall back instead of silently treating
    that as "conversation has no nodes".
    """
    if not isinstance(current_node_id, str) or current_node_id not in mapping:
        return None

    path: List[Dict[str, Any]] = []
    visited = set()
    node_id: Optional[str] = current_node_id
    while isinstance(node_id, str) and node_id in mapping and node_id not in visited:
        visited.add(node_id)
        node = mapping[node_id]
        if not isinstance(node, dict):
            break
        path.append(node)
        node_id = node.get("parent")

    path.reverse()
    return path


def extract_from_conversation(convo: Dict[str, Any]) -> Dict[str, Any]:
    """Walk the active conversation path and pull queries + ranked results.

    Real ChatGPT conversation JSON is a tree: `mapping` holds every node
    ever created, including abandoned/regenerated branches that are no
    longer part of the shown conversation. Only the path from
    `current_node` back to the root -- reversed to chronological order --
    is the "live" transcript; nodes off that path are skipped, not
    harvested, so their queries and results never leak into the output.

    If `current_node` is missing or doesn't resolve (e.g. an older or
    hand-built capture without it), this falls back to walking every node
    in the mapping's insertion order rather than silently emitting
    nothing for a conversation that otherwise has content.
    """
    queries: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []
    rank_counter = 0
    seen_urls: set = set()

    mapping = convo.get("mapping")
    nodes: List[Dict[str, Any]] = []
    if isinstance(mapping, dict):
        active_path = _active_path_nodes(mapping, convo.get("current_node"))
        if active_path is not None:
            nodes = active_path
        else:
            nodes = [node for node in mapping.values() if isinstance(node, dict)]

    for node in nodes:
        message = node.get("message")
        if not isinstance(message, dict):
            continue

        if message.get("recipient") == "web.run":
            queries.extend(extract_queries_from_message(message))

        new_results, rank_counter = extract_results_from_message(message, rank_counter, seen_urls)
        results.extend(new_results)

    queries = dedupe_queries(queries)

    conversation_id = convo.get("conversation_id")
    if not isinstance(conversation_id, str):
        conversation_id = convo.get("id")

    title = convo.get("title")

    return {
        "conversation_id": conversation_id,
        "title": title,
        "queries": queries,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Input loading (argv paths or stdin; single conversation or a JSON array)
# ---------------------------------------------------------------------------

def _iter_conversations(data: Any, label: str) -> Iterable[Tuple[str, Dict[str, Any]]]:
    if isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                yield f"{label}[{i}]", item
            else:
                print(f"Warning: skipping non-object entry at {label}[{i}]", file=sys.stderr)
    elif isinstance(data, dict):
        yield label, data
    else:
        print(f"Warning: skipping {label}: not a JSON object or array", file=sys.stderr)


def load_conversation_sources(paths: List[str]) -> Iterable[Tuple[str, Dict[str, Any]]]:
    """Yield (label, conversation_dict) pairs from argv paths or stdin.
    Malformed/unreadable input is warned about on stderr and skipped --
    never raises."""
    if paths:
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                print(f"Warning: skipping {path}: {exc}", file=sys.stderr)
                continue
            yield from _iter_conversations(data, path)
    else:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"Warning: skipping stdin: {exc}", file=sys.stderr)
            return
        yield from _iter_conversations(data, "<stdin>")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract ChatGPT web.run search queries and ranked results from conversation JSON."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Conversation JSON file paths (as saved from GET /backend-api/conversation/<id>). "
        "If omitted, reads a single JSON document from stdin.",
    )
    parser.add_argument(
        "--date",
        help="Override the run date recorded on each output line (YYYY-MM-DD). Defaults to today.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run_date = args.date or dt.date.today().isoformat()

    for label, convo in load_conversation_sources(args.paths):
        try:
            record = extract_from_conversation(convo)
        except Exception as exc:  # noqa: BLE001 - extraction must never crash the run
            print(f"Warning: failed to extract from {label}: {exc}", file=sys.stderr)
            continue

        output = {
            "date": run_date,
            "conversation_id": record["conversation_id"],
            "title": record["title"],
            "queries": record["queries"],
            "results": record["results"],
        }
        try:
            print(json.dumps(output, ensure_ascii=False))
        except UnicodeEncodeError as exc:
            # Don't let one bad record (e.g. a lone UTF-16 surrogate that
            # slipped through the JSON body) abort a multi-file batch after
            # earlier lines have already been appended to probes.jsonl.
            print(f"Warning: failed to write output for {label}: {exc}", file=sys.stderr)
            continue

    return 0


if __name__ == "__main__":
    sys.exit(main())
