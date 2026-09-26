# Midnight GEO Pro Pack v1.2.0 — named staff

Eight specialists + a chief. Not a folder of files.

Every operating skill is assigned to **exactly one** specialist. Shared methodology (`seo-references`) is copied into skill-bearing Hermes profiles so each bot can read `core.md`; it is not a 16th skill.

| Bot | Title | Lane | Exclusive skills |
|---|---|---|---|
| `midnight-chief` | Chief of GEO staff | routes | — |
| `midnight-probe` | Answer-engine probe | answer-engine probes | `geo` |
| `midnight-audit` | Bot-reach and portfolio audit | bot-reach + scoring | `geo-crawl`, `neural-audit` |
| `midnight-passages` | Extractable passages | writing / extractability | `aeo`, `preferred-source` |
| `midnight-entity` | Entity and indexer | entity / indexer | `entity`, `indexer` |
| `midnight-map` | Topical maps and local pack | topical maps | `topical-map`, `map-flap`, `whale` |
| `midnight-acquire` | Links and placements | acquisition | `hunter`, `kilo`, `parasite` |
| `midnight-report` | Evidence and measurement | evidence / reading the audit | `ga4`, `signal` |
| `midnight-support` | Support terms | SUPPORT.md terms | — |

Operating skills (15): `aeo`, `entity`, `ga4`, `geo`, `geo-crawl`, `hunter`, `indexer`, `kilo`, `map-flap`, `neural-audit`, `parasite`, `preferred-source`, `signal`, `topical-map`, `whale`.

## Hermes Bot Mode

Each `hermes/<bot>/` is a profile distribution (`distribution.yaml` at the root).

```bash
# from the unpacked zip
for d in staff-bundles/hermes/midnight-*; do
  hermes profile install "$d" --name "$(basename "$d")" --alias -y
done
```

Then `hermes -p midnight-chief setup` (and the same for each specialist you will actually run). Open the Bots tab in Hermes Desktop — each profile is a Bot.

These are static files. No cloud hosting, no usage gateway, no bulk Grok import.

## Grok Bot

Semi-manual. Create bots from `grok/bot-cards.md`, enable the lists in `grok/enable-lists.md`, follow `grok/setup-checklist.md`. No bulk import. On Grok, bots on one account share one cloud computer — names are not a security boundary.

## What this is not

Playbooks, not a ranking or citation guarantee. Email support is one clarification round at support@midnightdev.dev. See `SUPPORT.md` at the pack root.
