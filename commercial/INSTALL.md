# Install the Midnight GEO Pro Pack

You need a Stripe receipt for a single-seat commercial license. Public clone
access is not a license. Terms: [LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md).

The zip layout:

```
midnight-geo-pro-v1.2.0/
  LICENSE
  LICENSE-COMMERCIAL.md
  README.md
  SUPPORT.md
  MANIFEST.md
  commercial/
  skills/
  research/ai-citation-patterns/
  operator-evidence/
  chatgpt-probe-harness/
  staff-bundles/
```

## Claude Code

```bash
cp -R skills/* ~/.claude/skills/
```

Open a Claude Code session and invoke a skill, for example `/geo yourdomain.com`.

Fill `~/.claude/skills/seo-references/core.md` (portfolio table + `{{CITY}}`).

## Hermes

Copy each skill directory into the active profile skills tree, typically:

```bash
cp -R skills/* ~/.hermes/skills/
# or, for a named profile:
cp -R skills/* ~/.hermes/profiles/<profile>/skills/
```

Then `hermes skills list` (or the profile equivalent) and confirm the GEO skills
are enabled.

## Named staff — Hermes Bot Mode and Grok Bot (v1.2)

The pack also installs as eight specialists + a chief, not only a folder of
skill files. Roster and host steps: `staff-bundles/STAFF.md`.

Hermes (each `staff-bundles/hermes/<bot>/` is a profile distribution):

```bash
for d in staff-bundles/hermes/midnight-*; do
  hermes profile install "$d" --name "$(basename "$d")" --alias -y
done
```

Then `hermes -p midnight-chief setup`. Open the Bots tab — each profile is a Bot.

Grok: semi-manual. Create bots from `staff-bundles/grok/bot-cards.md`, enable
`staff-bundles/grok/enable-lists.md`, follow
`staff-bundles/grok/setup-checklist.md`. No bulk import.

Every operating skill is assigned to exactly one specialist. This is still
playbooks, not a citation guarantee.

## Citation research

Read `research/ai-citation-patterns/README.md`. `/geo` and `/aeo` are the
execution paths; the research file is the dated source, not a skill.

## Operator evidence (v1.1)

Worked 18-domain crawl + GSC export: `operator-evidence/README.md`.

## ChatGPT probe harness (v1.1)

One-page protocol: `chatgpt-probe-harness/PROTOCOL.md`. Then:

```bash
python3 chatgpt-probe-harness/test_extract.py
```

## Support

What email support covers (and does not): [SUPPORT.md](../SUPPORT.md).

## geo-crawl probe

`/geo-crawl` still expects a local checkout of
https://github.com/abouchard11/geo-crawl-audit so it can run `scripts/geo_probe.py`.
That probe is not copied into this pack.

## Requirements

Semrush, Google Search Console, and GA4 MCP servers plus (optionally) Camoufox.
Skills degrade when a source is missing; order of failure is in
`skills/seo-references/core.md`.
