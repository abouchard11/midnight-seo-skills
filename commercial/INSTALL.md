# Install the Midnight GEO Pro Pack

You need a Stripe receipt for a single-seat commercial license. Public clone
access is not a license. Terms: [LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md).

The zip layout:

```
midnight-geo-pro-v1.0.0/
  LICENSE
  LICENSE-COMMERCIAL.md
  README.md
  commercial/
  skills/
  research/ai-citation-patterns/
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

## Citation research

Read `research/ai-citation-patterns/README.md`. `/geo` and `/aeo` are the
execution paths; the research file is the dated source, not a skill.

## geo-crawl probe

`/geo-crawl` still expects a local checkout of
https://github.com/abouchard11/geo-crawl-audit so it can run `scripts/geo_probe.py`.
That probe is not copied into this pack.

## Requirements

Semrush, Google Search Console, and GA4 MCP servers plus (optionally) Camoufox.
Skills degrade when a source is missing; order of failure is in
`skills/seo-references/core.md`.
