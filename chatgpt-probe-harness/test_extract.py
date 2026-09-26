#!/usr/bin/env python3
"""test_extract.py -- test suite for extract_queries.py.

check() raises a real AssertionError on failure (rather than recording
into a global list main() alone inspects), so this file works correctly
BOTH as a standalone script:

    python3 test_extract.py

AND under pytest, which collects every test_* function and fails on any
raised AssertionError:

    python3 -m pytest test_extract.py -q

Mixes CLI-level (subprocess) tests against the fixtures with direct unit
tests against the extractor's functions.

Exits 0 on success, nonzero (with a printed failure summary) otherwise
when run as a script.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT_SCRIPT = HERE / "extract_queries.py"
FIXTURES = HERE / "fixtures"

sys.path.insert(0, str(HERE))
import extract_queries  # noqa: E402


def check(condition: bool, message: str) -> None:
    """Raise AssertionError if `condition` is false.

    A real raise -- not an append to a list only main() looks at -- is
    what makes a broken extractor fail under both `python3 test_extract.py`
    and `python3 -m pytest test_extract.py`.
    """
    if not condition:
        raise AssertionError(message)


def run_extractor(*args, input_text=None):
    """Run extract_queries.py with the given argv, return (stdout, stderr, returncode)."""
    cmd = [sys.executable, str(EXTRACT_SCRIPT), *args]
    proc = subprocess.run(
        cmd,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.stdout, proc.stderr, proc.returncode


def parse_jsonl(text: str):
    lines = [line for line in text.splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


# ---------------------------------------------------------------------------
# Test: thinking_route.json (CLI level)
# ---------------------------------------------------------------------------

def test_thinking_route():
    stdout, stderr, code = run_extractor("--date", "2026-08-07", str(FIXTURES / "thinking_route.json"))
    check(code == 0, f"thinking_route: expected exit 0, got {code} (stderr={stderr!r})")

    records = parse_jsonl(stdout)
    check(len(records) == 1, f"thinking_route: expected 1 output line, got {len(records)}")
    record = records[0]

    check(record.get("date") == "2026-08-07", f"thinking_route: date mismatch: {record.get('date')!r}")
    check(
        record.get("conversation_id") == "c1111111-aaaa-4bbb-8ccc-111122223333",
        f"thinking_route: conversation_id mismatch: {record.get('conversation_id')!r}",
    )
    check(
        record.get("title") == "Researching Yapword founder background",
        f"thinking_route: title mismatch: {record.get('title')!r}",
    )

    expected_queries = [
        {"q": "Yapword founder", "source": "system1", "freshness_days": None},
        {"q": "Yapword founder daily AI word game", "source": "search_queries", "freshness_days": None},
    ]
    check(
        record.get("queries") == expected_queries,
        f"thinking_route: queries mismatch.\n  expected={expected_queries}\n  actual  ={record.get('queries')}",
    )

    expected_results = [
        {
            "url": "https://yapword.com/about",
            "title": "About Yapword",
            "rank": 1,
            "domain": "google.com",
            "type": "search_result_group",
        },
        {
            "url": "https://example.com/press/yapword-launch",
            "title": "Yapword launches daily word game",
            "rank": 2,
            "domain": "google.com",
            "type": "search_result_group",
        },
        {
            "url": "https://news.example.com/yapword-founder-profile",
            "title": "Yapword Founder Profile",
            "rank": 3,
            "domain": "bing.com",
            "type": "search_result_group",
        },
        {
            "url": "https://blog.example.com/ai-word-games",
            "title": "Best AI Word Games 2026",
            "rank": 4,
            "type": "search_result_group",
        },
    ]
    check(
        record.get("results") == expected_results,
        f"thinking_route: results mismatch.\n  expected={expected_results}\n  actual  ={record.get('results')}",
    )

    # node-1b is a decoy: it's a sibling of node-2 (parent "node-1", not on
    # the current_node="node-5" -> root path), so the tree walk excludes it
    # outright. It ALSO has recipient "all" (not "web.run") and carries a
    # search_queries entry AND a fast-DSL content line, both q="DECOY
    # should never appear" -- so even a mutation that weakens the
    # recipient gate (e.g. `if True:`) would still need to also break the
    # tree walk to leak it in. Assert it never surfaces anywhere.
    check(
        "DECOY" not in stdout,
        f"thinking_route: DECOY leaked into extractor output (recipient gate / tree walk not enforced): {stdout!r}",
    )
    check(
        all("DECOY" not in item.get("q", "") for item in record.get("queries", [])),
        f"thinking_route: DECOY query leaked past the web.run recipient gate / tree walk: {record.get('queries')}",
    )


# ---------------------------------------------------------------------------
# Test: fast_route.json (CLI level)
# ---------------------------------------------------------------------------

def test_fast_route():
    stdout, stderr, code = run_extractor("--date", "2026-08-07", str(FIXTURES / "fast_route.json"))
    check(code == 0, f"fast_route: expected exit 0, got {code} (stderr={stderr!r})")

    records = parse_jsonl(stdout)
    check(len(records) == 1, f"fast_route: expected 1 output line, got {len(records)}")
    record = records[0]

    check(record.get("date") == "2026-08-07", f"fast_route: date mismatch: {record.get('date')!r}")
    check(
        record.get("conversation_id") == "f2222222-bbbb-4ccc-8ddd-222233334444",
        f"fast_route: conversation_id mismatch: {record.get('conversation_id')!r}",
    )
    check(
        record.get("title") == "Quick lookup: Yapword launch signals",
        f"fast_route: title mismatch: {record.get('title')!r}",
    )

    expected_queries = [
        {"q": '"Yapword" founder daily AI word game', "source": "fast_dsl", "freshness_days": 30},
        {"q": "Yapword press coverage", "source": "fast_dsl", "freshness_days": None},
        {"q": "site:yapword.com press", "source": "fast_dsl", "freshness_days": 14},
        {"q": "https://yapword.com/press", "source": "fast_dsl", "freshness_days": None},
    ]
    check(
        record.get("queries") == expected_queries,
        f"fast_route: queries mismatch.\n  expected={expected_queries}\n  actual  ={record.get('queries')}",
    )
    # Duplicate "fast|...|30" line and the two skipped lines (unknown field0,
    # no pipe) must not appear anywhere in the output.
    all_q = [item["q"] for item in record.get("queries", [])]
    check(len(all_q) == len(set(all_q)), f"fast_route: dedupe failed, duplicate q present: {all_q}")
    check(
        "should be ignored" not in all_q,
        "fast_route: unknown-command DSL line ('notacommand|...') leaked into queries",
    )

    expected_results = [
        {
            "url": "https://example.com/yapword-founder-profile",
            "title": "Yapword Founder Profile",
            "rank": 1,
            "domain": "duckduckgo.com",
            "type": "search_result_group",
        },
        {
            "url": "https://yapword.com/press",
            "title": "Yapword Press Kit",
            "rank": 2,
            "domain": "duckduckgo.com",
            "type": "search_result_group",
        },
    ]
    check(
        record.get("results") == expected_results,
        f"fast_route: results mismatch.\n  expected={expected_results}\n  actual  ={record.get('results')}",
    )


# ---------------------------------------------------------------------------
# Test: code_route.json (CLI level) -- content_type "code" / content["text"]
# ---------------------------------------------------------------------------

def test_code_route():
    stdout, stderr, code = run_extractor("--date", "2026-08-07", str(FIXTURES / "code_route.json"))
    check(code == 0, f"code_route: expected exit 0, got {code} (stderr={stderr!r})")

    records = parse_jsonl(stdout)
    check(len(records) == 1, f"code_route: expected 1 output line, got {len(records)}")
    record = records[0]

    check(record.get("date") == "2026-08-07", f"code_route: date mismatch: {record.get('date')!r}")
    check(
        record.get("conversation_id") == "d3333333-cccc-4ddd-8eee-333344445555",
        f"code_route: conversation_id mismatch: {record.get('conversation_id')!r}",
    )

    expected_queries = [
        {"q": "Yapword competitor daily word games", "source": "code_dsl", "freshness_days": 30},
        {"q": "https://example.com/yapword-review", "source": "code_dsl", "freshness_days": None},
    ]
    check(
        record.get("queries") == expected_queries,
        f"code_route: queries mismatch.\n  expected={expected_queries}\n  actual  ={record.get('queries')}",
    )

    # node-1x is an abandoned branch: a sibling of node-2, off the
    # current_node ("node-4") -> root path. Its queries (both the fast-DSL
    # content line AND the metadata.search_queries entry) must never
    # surface, even though it passes the recipient=="web.run" gate.
    check(
        "ABANDONED" not in stdout,
        f"code_route: abandoned-branch query leaked into extractor output: {stdout!r}",
    )

    expected_results = [
        {
            "url": "https://example.com/yapword-review",
            "title": "Yapword Review vs Competitors",
            "rank": 1,
            "domain": "example.com",
            "type": "search_result_group",
        },
        {
            "url": "https://competitor.example.com/word-game",
            "title": "Competitor Word Game",
            "rank": 2,
            "domain": "example.com",
            "type": "search_result_group",
        },
    ]
    check(
        record.get("results") == expected_results,
        f"code_route: results mismatch.\n  expected={expected_results}\n  actual  ={record.get('results')}",
    )


def test_code_route_fixture_yields_nonzero_queries():
    """Pytest-level guard against the 'silent empty output' failure mode:
    a code-route capture (content_type "code" / content["text"]) must
    yield at least one query end to end through the CLI, not exit 0 with
    an empty queries[] that looks superficially valid."""
    stdout, stderr, code = run_extractor("--date", "2026-08-07", str(FIXTURES / "code_route.json"))
    check(code == 0, f"code_route silent-empty guard: expected exit 0, got {code} (stderr={stderr!r})")

    records = parse_jsonl(stdout)
    check(len(records) == 1, f"code_route silent-empty guard: expected 1 output line, got {len(records)}")
    queries = records[0].get("queries", [])
    check(
        len(queries) > 0,
        f"code_route silent-empty guard: extractor returned 0 queries for a code-route capture "
        f"(this is the failure mode where content['text'] is never read): {records[0]}",
    )


# ---------------------------------------------------------------------------
# Test: malformed JSON must never crash the extractor (CLI level)
# ---------------------------------------------------------------------------

def test_malformed_json_does_not_crash():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        malformed_path = tmp_path / "malformed.json"
        malformed_path.write_text('{"title": "broken", "mapping": { totally not valid json !!!', encoding="utf-8")

        good_path = tmp_path / "good.json"
        good_path.write_text((FIXTURES / "thinking_route.json").read_text(encoding="utf-8"), encoding="utf-8")

        # Malformed file alone: must exit 0, emit nothing on stdout, warn on stderr.
        stdout, stderr, code = run_extractor("--date", "2026-08-07", str(malformed_path))
        check(code == 0, f"malformed-only: expected exit 0 (never crash), got {code}")
        check(stdout.strip() == "", f"malformed-only: expected no stdout output, got {stdout!r}")
        check(stderr.strip() != "", "malformed-only: expected a warning on stderr")

        # Malformed file mixed with a good one: good one must still be processed.
        stdout, stderr, code = run_extractor(
            "--date", "2026-08-07", str(malformed_path), str(good_path)
        )
        check(code == 0, f"malformed+good: expected exit 0, got {code}")
        records = parse_jsonl(stdout)
        check(
            len(records) == 1,
            f"malformed+good: expected 1 output line for the good file, got {len(records)}",
        )
        check(
            records[0].get("conversation_id") == "c1111111-aaaa-4bbb-8ccc-111122223333",
            "malformed+good: good file's conversation_id missing/wrong after malformed sibling",
        )

        # Malformed conversation structure that IS valid JSON but has the
        # wrong shapes throughout (mapping not a dict, node not a dict,
        # message missing fields, non-string queries/urls, no
        # current_node, etc.) must also be handled gracefully rather than
        # raising.
        weird_path = tmp_path / "weird_shapes.json"
        weird_path.write_text(
            json.dumps(
                {
                    "title": 12345,  # wrong type, should just pass through
                    "conversation_id": None,
                    "mapping": {
                        "node-a": "not-a-dict",
                        "node-b": {"message": "not-a-dict-either"},
                        "node-c": {
                            "message": {
                                "recipient": "web.run",
                                "metadata": {"search_queries": "not-a-list"},
                                "content": {"parts": [123, None, {"nested": "dict-not-string"}]},
                            }
                        },
                        "node-d": {
                            "message": {
                                "recipient": "assistant",
                                "metadata": {
                                    "search_result_groups": [
                                        {"entries": [{"url": 42, "title": "bad url type"}]},
                                        {"entries": "not-a-list"},
                                        "not-a-dict-group",
                                    ]
                                },
                            }
                        },
                    },
                }
            ),
            encoding="utf-8",
        )
        stdout, stderr, code = run_extractor("--date", "2026-08-07", str(weird_path))
        check(code == 0, f"weird-shapes: expected exit 0 (never crash), got {code} (stderr={stderr!r})")
        records = parse_jsonl(stdout)
        check(len(records) == 1, f"weird-shapes: expected 1 output line, got {len(records)}")
        check(records[0].get("queries") == [], f"weird-shapes: expected no queries, got {records[0].get('queries')}")
        check(records[0].get("results") == [], f"weird-shapes: expected no results, got {records[0].get('results')}")


# ---------------------------------------------------------------------------
# Test: stdin input path works too (CLI level)
# ---------------------------------------------------------------------------

def test_stdin_input():
    conv_text = (FIXTURES / "fast_route.json").read_text(encoding="utf-8")
    stdout, stderr, code = run_extractor("--date", "2026-08-07", input_text=conv_text)
    check(code == 0, f"stdin: expected exit 0, got {code} (stderr={stderr!r})")
    records = parse_jsonl(stdout)
    check(len(records) == 1, f"stdin: expected 1 output line, got {len(records)}")
    check(
        records[0].get("conversation_id") == "f2222222-bbbb-4ccc-8ddd-222233334444",
        "stdin: conversation_id mismatch when reading from stdin",
    )


# ---------------------------------------------------------------------------
# Unit test: tree walk follows current_node -> parent chain, not dict order
# ---------------------------------------------------------------------------

def test_tree_walk_orders_by_active_path_not_dict_order():
    # Mapping keys are deliberately inserted in REVERSE chronological
    # order. If extraction still followed dict-insertion order (the old,
    # broken behaviour) this would flip the query order; the tree walk
    # must produce chronological order regardless of key order.
    mapping = {
        "node-2": {
            "id": "node-2",
            "message": {
                "recipient": "web.run",
                "content": {"content_type": "text", "parts": ["fast|second query|"]},
                "metadata": {},
            },
            "parent": "node-1",
            "children": [],
        },
        "node-1": {
            "id": "node-1",
            "message": {
                "recipient": "web.run",
                "content": {"content_type": "text", "parts": ["fast|first query|"]},
                "metadata": {},
            },
            "parent": "node-0",
            "children": ["node-2"],
        },
        "node-0": {"id": "node-0", "message": None, "parent": None, "children": ["node-1"]},
    }
    convo = {
        "conversation_id": "unit-test-tree-order",
        "title": "unit test",
        "current_node": "node-2",
        "mapping": mapping,
    }
    record = extract_queries.extract_from_conversation(convo)
    expected = [
        {"q": "first query", "source": "fast_dsl", "freshness_days": None},
        {"q": "second query", "source": "fast_dsl", "freshness_days": None},
    ]
    check(
        record["queries"] == expected,
        f"tree-walk unit test: expected chronological order {expected}, got {record['queries']}",
    )


# ---------------------------------------------------------------------------
# Unit test: abandoned branches are excluded from both queries and results
# ---------------------------------------------------------------------------

def test_active_path_excludes_abandoned_branches():
    mapping = {
        "root": {"id": "root", "message": None, "parent": None, "children": ["a"]},
        "a": {
            "id": "a",
            "message": {
                "recipient": "web.run",
                "content": {"content_type": "text", "parts": ["fast|LIVE query|30"]},
                "metadata": {},
            },
            "parent": "root",
            "children": ["b", "b-abandoned"],
        },
        "b": {
            "id": "b",
            "message": {
                "recipient": "assistant",
                "content": {"content_type": "text", "parts": ["results"]},
                "metadata": {
                    "search_result_groups": [
                        {"entries": [{"url": "https://example.com/live", "title": "Live"}]}
                    ]
                },
            },
            "parent": "a",
            "children": ["c"],
        },
        # b-abandoned is a SIBLING of b (both children of "a"), but only
        # "b" is on the current_node="c" -> root path. It has the exact
        # same recipient=="web.run" gate as the live node "a", so only the
        # tree walk (not the recipient gate) can exclude it.
        "b-abandoned": {
            "id": "b-abandoned",
            "message": {
                "recipient": "web.run",
                "content": {"content_type": "text", "parts": ["fast|ABANDONED query should not appear|30"]},
                "metadata": {},
            },
            "parent": "a",
            "children": [],
        },
        "c": {"id": "c", "message": None, "parent": "b", "children": []},
    }
    convo = {
        "conversation_id": "unit-test-abandoned",
        "title": "unit test",
        "current_node": "c",
        "mapping": mapping,
    }
    record = extract_queries.extract_from_conversation(convo)
    check(
        record["queries"] == [{"q": "LIVE query", "source": "fast_dsl", "freshness_days": 30}],
        f"abandoned-branch unit test: unexpected queries {record['queries']}",
    )
    check(
        all("ABANDONED" not in q["q"] for q in record["queries"]),
        f"abandoned-branch unit test: abandoned query leaked: {record['queries']}",
    )
    check(
        record["results"] == [{"url": "https://example.com/live", "title": "Live", "rank": 1}],
        f"abandoned-branch unit test: unexpected results {record['results']}",
    )


# ---------------------------------------------------------------------------
# Unit test: missing current_node falls back rather than going silently empty
# ---------------------------------------------------------------------------

def test_active_path_falls_back_when_current_node_missing():
    mapping = {
        "only-node": {
            "id": "only-node",
            "message": {
                "recipient": "web.run",
                "content": {"content_type": "text", "parts": ["fast|fallback query|"]},
                "metadata": {},
            },
            "parent": None,
            "children": [],
        }
    }
    # No "current_node" key at all -- an older/hand-built capture.
    convo = {"conversation_id": "unit-test-fallback", "title": "unit test", "mapping": mapping}
    record = extract_queries.extract_from_conversation(convo)
    check(
        record["queries"] == [{"q": "fallback query", "source": "fast_dsl", "freshness_days": None}],
        f"fallback unit test: expected the lone node's query, got {record['queries']}",
    )


# ---------------------------------------------------------------------------
# Unit test: code-route extraction (content_type "code" / content["text"])
# ---------------------------------------------------------------------------

def test_code_route_extraction_unit():
    message = {
        "recipient": "web.run",
        "author": {"role": "assistant", "name": None, "metadata": {}},
        "content": {
            "content_type": "code",
            "language": "unknown",
            "response_format_name": None,
            "text": "search|Yapword founder|30\nopen|https://yapword.com|",
        },
        "metadata": {},
    }
    found = extract_queries.extract_queries_from_message(message)
    expected = [
        {"q": "Yapword founder", "source": "code_dsl", "freshness_days": 30},
        {"q": "https://yapword.com", "source": "code_dsl", "freshness_days": None},
    ]
    check(found == expected, f"code-route unit test: expected {expected}, got {found}")


def test_unknown_content_types_do_not_crash():
    for content_type in ("thoughts", "reasoning_recap"):
        message = {
            "recipient": "web.run",
            "content": {"content_type": content_type, "thoughts": [{"summary": "thinking..."}]},
            "metadata": {},
        }
        found = extract_queries.extract_queries_from_message(message)
        check(found == [], f"unknown content_type {content_type!r} unit test: expected [], got {found}")


# ---------------------------------------------------------------------------
# Unit test: fast-DSL parsing preserves an embedded pipe in the query field
# ---------------------------------------------------------------------------

def test_parse_fast_dsl_lines_preserves_embedded_pipe():
    result = extract_queries.parse_fast_dsl_lines('search|"Yapword | Daily Word Game"|30')
    expected = [("search", '"Yapword | Daily Word Game"', 30)]
    check(result == expected, f"embedded-pipe unit test: expected {expected}, got {result}")

    # No trailing freshness field at all -- the lone "|" is part of the
    # query text, not a field separator, and must be kept in full.
    result2 = extract_queries.parse_fast_dsl_lines('search|"Yapword | Daily Word Game"')
    expected2 = [("search", '"Yapword | Daily Word Game"', None)]
    check(result2 == expected2, f"embedded-pipe (no freshness) unit test: expected {expected2}, got {result2}")


# ---------------------------------------------------------------------------
# Unit test: dedupe_queries keys on (q, source, freshness_days)
# ---------------------------------------------------------------------------

def test_dedupe_queries_keeps_differing_freshness_and_source():
    queries = [
        {"q": "x", "source": "fast_dsl", "freshness_days": 7},
        {"q": "x", "source": "fast_dsl", "freshness_days": 30},
        {"q": "x", "source": "system1", "freshness_days": None},
        {"q": "x", "source": "fast_dsl", "freshness_days": 7},  # exact duplicate, must collapse
    ]
    result = extract_queries.dedupe_queries(queries)
    expected = [
        {"q": "x", "source": "fast_dsl", "freshness_days": 7},
        {"q": "x", "source": "fast_dsl", "freshness_days": 30},
        {"q": "x", "source": "system1", "freshness_days": None},
    ]
    check(result == expected, f"dedupe widened-key unit test: expected {expected}, got {result}")


# ---------------------------------------------------------------------------
# Unit test: result harvesting dedupes a URL echoed on more than one message
# ---------------------------------------------------------------------------

def test_extract_results_from_message_dedupes_repeated_url():
    message = {
        "metadata": {
            "search_result_groups": [
                {"entries": [{"url": "https://a.example.com/x", "title": "A"}]},
            ]
        }
    }
    seen_urls: set = set()
    results1, rank1 = extract_queries.extract_results_from_message(message, 0, seen_urls)
    check(
        results1 == [{"url": "https://a.example.com/x", "title": "A", "rank": 1}],
        f"result-dedupe unit test: first pass unexpected {results1}",
    )
    # Simulate the identical group echoed on a second message in the same
    # conversation -- must be dropped, and must not consume a rank slot.
    results2, rank2 = extract_queries.extract_results_from_message(message, rank1, seen_urls)
    check(results2 == [], f"result-dedupe unit test: expected duplicate URL dropped, got {results2}")
    check(rank2 == rank1, "result-dedupe unit test: rank_counter must not advance for a deduped duplicate")


# ---------------------------------------------------------------------------

TESTS = [
    test_thinking_route,
    test_fast_route,
    test_code_route,
    test_code_route_fixture_yields_nonzero_queries,
    test_malformed_json_does_not_crash,
    test_stdin_input,
    test_tree_walk_orders_by_active_path_not_dict_order,
    test_active_path_excludes_abandoned_branches,
    test_active_path_falls_back_when_current_node_missing,
    test_code_route_extraction_unit,
    test_unknown_content_types_do_not_crash,
    test_parse_fast_dsl_lines_preserves_embedded_pipe,
    test_dedupe_queries_keeps_differing_freshness_and_source,
    test_extract_results_from_message_dedupes_repeated_url,
]


def main() -> int:
    failures = []
    for test_func in TESTS:
        try:
            test_func()
        except AssertionError as exc:
            failures.append(f"{test_func.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001 - report unexpected errors too, don't hide them
            failures.append(f"{test_func.__name__}: unexpected {type(exc).__name__}: {exc}")

    if failures:
        print(f"FAILED: {len(failures)} test(s) failed\n", file=sys.stderr)
        for msg in failures:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    print(f"OK: all checks passed ({len(TESTS)} tests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
