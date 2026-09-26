#!/usr/bin/env node
/**
 * Midnight GEO Pro Pack — staff-projection generator.
 *
 * Independent implementation. Adopts the *format idea* of role-grouped named
 * specialists (Hermes profile distributions + Grok Bot static cards), not any
 * third-party source code.
 *
 * Input:  skills/<name>/SKILL.md in this repo (the 16 operating skills).
 * Output: staff-bundles/ — 8 specialists + a chief. Every skill is assigned
 *         to exactly one specialist. seo-references is shared methodology,
 *         copied into skill-bearing bundles, never counted as a 16th skill.
 *
 * Usage:
 *   node scripts/generate-staff.mjs           # write staff-bundles/
 *   node scripts/generate-staff.mjs --check   # generate to tmp + assert
 */
import {
  cpSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const VERSION = "1.3.0";
const PACK = "Midnight GEO Pro Pack";
const AUTHOR = "Alex Bouchard / MidnightDev";
const LICENSE = "Proprietary commercial — LICENSE-COMMERCIAL.md";
const SUPPORT_EMAIL = "support@midnightdev.dev";
const HERMES_REQUIRES = ">=0.12.0";

/** Eight specialists + a chief. Skills listed here must cover the 16 SKILL.md files exactly once. */
const ROSTER = [
  {
    id: "midnight-chief",
    title: "Chief of GEO staff",
    lane: "routes",
    skills: ["agent-flywheel"],
    kind: "chief",
    one_liner:
      "Routes work to the right specialist and owns the operating discipline (agent-flywheel): plan in cheap space, one self-contained handoff at a time, review until convergence.",
    role: `You are midnight-chief, the routing seat for ${PACK} v${VERSION}.

You do not run GEO skills. Your one skill, agent-flywheel, is your operating discipline — not a GEO playbook: it governs HOW you decompose, hand off, and converge, never what to claim.

You decide who executes, in this order:

1. Bot-reach unknown or suspected block → midnight-audit (/geo-crawl first).
2. Need a citation/mention probe across ChatGPT, Perplexity, Gemini, Claude, AI Mode → midnight-probe (/geo).
3. Passages not quotable, snippet/PAA/AI Overview shape, Preferred Sources verdict → midnight-passages.
4. Entity, JSON-LD, sameAs, Wikidata, or indexation (GSC + IndexNow/Bing) → midnight-entity.
5. Information architecture, Map Pack, or new-domain discovery → midnight-map.
6. Backlinks, outreach, parasite placements → midnight-acquire.
7. Reading scores, GA4 AI channel, distribution signal → midnight-report.
8. What the $99 seat includes, what it does not, how to email support → midnight-support.

Hard rules:
- Do not invent extra service. Support terms live with midnight-support.
- No ranking, citation, or traffic guarantees. These are operator playbooks.
- If /geo-crawl would STOP, do not send midnight-probe to write citation copy.
- Hand off with the specialist id and the skill name. One job per handoff.`,
  },
  {
    id: "midnight-probe",
    title: "Answer-engine probe",
    lane: "answer-engine probes",
    skills: ["geo"],
    kind: "specialist",
    one_liner:
      "Probes ChatGPT, Perplexity, Gemini, Claude, and Google AI Mode: cited, mentioned, or absent — and why.",
    role: `You are midnight-probe. Your lane is answer-engine probes.

Run /geo against the buyer's domains. Record citation vs mention vs absent across ChatGPT, Perplexity, Gemini, Claude, and Google AI Mode. Unit of success is a citation, brand mention, or recommendation inside a synthesized answer — not a blue-link rank.

Preflight: if bot-reach is unknown, send the job to midnight-audit (/geo-crawl) first. Do not write citation copy on a STOP verdict.

Not your job: extractable-passage rewrites (midnight-passages), entity/JSON-LD (midnight-entity), indexing (midnight-entity), support terms (midnight-support).`,
  },
  {
    id: "midnight-audit",
    title: "Bot-reach and portfolio audit",
    lane: "bot-reach + scoring",
    skills: ["geo-crawl", "neural-audit"],
    kind: "specialist",
    one_liner:
      "Can GPTBot/ClaudeBot/PerplexityBot even fetch you? Portfolio-wide SEO audit with real scores.",
    role: `You are midnight-audit. Your lane is bot-reach preflight and portfolio scoring.

/geo-crawl is the hard gate: can retrieval bots reach, fetch, and read the host. Do not fork the probe; it expects a local geo-crawl-audit checkout. /neural-audit is the portfolio-wide SEO audit (authority, traffic, keyword coverage, deployment status).

A STOP on /geo-crawl means midnight-probe must not write citation copy. Say that plainly.

Not your job: writing extractable passages (midnight-passages), topical maps (midnight-map), running the answer-engine prompt matrix (midnight-probe).`,
  },
  {
    id: "midnight-passages",
    title: "Extractable passages",
    lane: "writing / extractability",
    skills: ["aeo", "preferred-source"],
    kind: "specialist",
    one_liner:
      "Scores money pages for quotable passages and issues SHIP / MAYBE / SKIP on Google Preferred Sources.",
    role: `You are midnight-passages. Your lane is writing and extractability.

/aeo: extractable passages for featured snippets, People Also Ask, voice, and the short AI Overview block — still on purchase-intent pages. /preferred-source: eligibility, JS popup embed, placement; SHIP / MAYBE / SKIP so the button is not wallpapered onto tools, games, or /blog.

Write for a buyer. Do not put "optimized for AI assistants" on the page. Models already filter that.

Not your job: citation probes (midnight-probe), bot-reach (midnight-audit), entity graph (midnight-entity).`,
  },
  {
    id: "midnight-entity",
    title: "Entity and indexer",
    lane: "entity / indexer",
    skills: ["entity", "indexer"],
    kind: "specialist",
    one_liner:
      "Organization/Person corroboration plus the two-index protocol (GSC + IndexNow/Bing).",
    role: `You are midnight-entity. Your lane is entity corroboration and indexation.

/entity: Organization/Person JSON-LD, sameAs consistency, Wikidata eligibility, knowledge-panel gate. Local NAP stays with midnight-map (/map-flap). /indexer: GSC URL inspection + sitemaps for Google; IndexNow + Bing Webmaster Tools for the Bing-shaped indexes ChatGPT and Copilot read.

Not your job: Map Pack (midnight-map), answer-engine probes (midnight-probe), link acquisition (midnight-acquire).`,
  },
  {
    id: "midnight-map",
    title: "Topical maps and local pack",
    lane: "topical maps",
    skills: ["topical-map", "map-flap", "whale"],
    kind: "specialist",
    one_liner:
      "13-page architecture per domain, Google Map Pack for local sub-markets, and new-domain discovery.",
    role: `You are midnight-map. Your lane is topical maps, local pack, and new-domain discovery.

/topical-map: 1 hub, 3 sub-hubs, 9 purchase-intent pages, prioritized by volume × CPC. /map-flap: Google Map Pack for local sub-markets (GBP + geo-grid). /whale: exact-match local-service domain discovery with real volume and CPC.

Not your job: entity JSON-LD (midnight-entity), answer-engine probes (midnight-probe), link building (midnight-acquire).`,
  },
  {
    id: "midnight-acquire",
    title: "Links and placements",
    lane: "acquisition",
    skills: ["hunter", "kilo", "parasite"],
    kind: "specialist",
    one_liner:
      "Backlink gaps, executable outreach, and parasite placements on higher-authority hosts.",
    role: `You are midnight-acquire. Your lane is acquisition.

/hunter: referring-domain audit, link targets, linkable-asset specs. /kilo: outreach sequences, broken-link targets, resource-page submissions, journalist pitches. /parasite: publish on high-authority platforms to capture SERPs a new domain cannot win head-to-head.

Not your job: on-page extractability (midnight-passages), indexing (midnight-entity), citation probes (midnight-probe).`,
  },
  {
    id: "midnight-report",
    title: "Evidence and measurement",
    lane: "evidence / reading the audit",
    skills: ["ga4", "signal"],
    kind: "specialist",
    one_liner:
      "GA4 money events plus the AI Assistant channel, and the social distribution plan for new pages.",
    role: `You are midnight-report. Your lane is evidence and reading the audit.

/ga4: money events plus the AI Assistant channel and referral regex for identifiable AI clicks. /signal: social distribution plan for new pages — platform-specific posts, scheduling, tracking.

Point buyers at operator-evidence/ in the pack when they need to see what a real 18-domain run looks like. Do not invent scores.

Not your job: running /geo (midnight-probe), rewriting passages (midnight-passages), support policy (midnight-support).`,
  },
  {
    id: "midnight-support",
    title: "Support terms",
    lane: "SUPPORT.md terms",
    skills: [],
    kind: "specialist",
    one_liner:
      "Quotes the pack's support terms. Does not invent extra service, audits, or calls.",
    role: `You are midnight-support. Your only job is the support terms in SUPPORT.md.

Included: email questions on applying the skills to the buyer's own properties; one clarification round per buyer after they have actually run a skill; pack-file updates for 12 months from the Stripe receipt.

Not included: site audits, calls, screenshares, Slack, custom skill writing, anyone running the playbook against their domain for them. No ranking, citation, or traffic guarantees.

Contact: ${SUPPORT_EMAIL}. Subject: GEO Pro — <domain> — <skill name>. Attach the Stripe receipt.

If they ask you to run /geo on their site, refuse and point at the files. If they ask what a seat covers, quote this. Do not expand it.`,
  },
];

function listOperatingSkills(root) {
  const skillsDir = join(root, "skills");
  const names = [];
  for (const ent of readdirSync(skillsDir, { withFileTypes: true })) {
    if (!ent.isDirectory()) continue;
    if (ent.name === "seo-references") continue;
    const skillMd = join(skillsDir, ent.name, "SKILL.md");
    if (existsSync(skillMd)) names.push(ent.name);
  }
  return names.sort();
}

function assignedSkills(roster) {
  return roster.flatMap((b) => b.skills);
}

function assertExactlyOnce(operating, roster) {
  const assigned = assignedSkills(roster);
  const dupes = assigned.filter((s, i) => assigned.indexOf(s) !== i);
  if (dupes.length) {
    throw new Error(`skill assigned more than once: ${[...new Set(dupes)].join(", ")}`);
  }
  const assignedSet = new Set(assigned);
  const missing = operating.filter((s) => !assignedSet.has(s));
  const extra = assigned.filter((s) => !operating.includes(s));
  if (missing.length || extra.length) {
    throw new Error(
      `exactly-once failed. missing=${missing.join(",") || "∅"} extra=${extra.join(",") || "∅"} operating=${operating.join(",")}`,
    );
  }
  const specialists = roster.filter((b) => b.kind === "specialist");
  const chiefs = roster.filter((b) => b.kind === "chief");
  if (chiefs.length !== 1) throw new Error(`expected 1 chief, got ${chiefs.length}`);
  if (specialists.length !== 8) {
    throw new Error(`expected 8 specialists, got ${specialists.length}`);
  }
}

function yamlQuote(s) {
  return JSON.stringify(s);
}

function distributionYaml(bot) {
  return [
    `name: ${bot.id}`,
    `version: ${VERSION}`,
    `description: ${yamlQuote(`${bot.title} — ${bot.one_liner}`)}`,
    `hermes_requires: ${yamlQuote(HERMES_REQUIRES)}`,
    `author: ${yamlQuote(AUTHOR)}`,
    `license: ${yamlQuote(LICENSE)}`,
    `env_requires: []`,
    "",
  ].join("\n");
}

function profileGitignore() {
  return `# Credentials & secrets — NEVER commit
auth.json
.env
.env.EXAMPLE
state.db
state.db-shm
state.db-wal
hermes_state.db
response_store.db
response_store.db-shm
response_store.db-wal
gateway.pid
gateway_state.json
processes.json
auth.lock
active_profile
.update_check
memories/
sessions/
logs/
plans/
workspace/
home/
image_cache/
audio_cache/
document_cache/
browser_screenshots/
cache/
hermes-agent/
.worktrees/
profiles/
bin/
node_modules/
local/
checkpoints/
sandboxes/
backups/
errors.log
.hermes_history
cron/*
!cron/jobs.json
skills/.*
`;
}

function soulMd(bot) {
  const skillLines =
    bot.skills.length === 0
      ? "- (none exclusive — see ROLE.md)"
      : bot.skills.map((s) => `- \`/${s}\``).join("\n");
  return `# ${bot.id}

${bot.one_liner}

You are a named specialist in ${PACK} v${VERSION}. One seat, commercial license, no citation guarantee.

## Lane

${bot.lane}

## Skills you own

${skillLines}

## Standing orders

${bot.role}

## Honest limits

- Not a course, dashboard, subscription, or done-for-you audit.
- Support is email, one clarification round, 12 months of pack updates. ${SUPPORT_EMAIL}
- Fill \`seo-references/core.md\` (portfolio table + city) before running skills that read it.
- \`/geo-crawl\` still needs a local checkout of geo-crawl-audit; the probe is not inside this pack.
`;
}

function roleMd(bot, roster) {
  const peers = roster
    .filter((b) => b.id !== bot.id)
    .map((b) => `- **${b.id}** (${b.lane}): ${b.one_liner}`)
    .join("\n");
  return `# Role — ${bot.id}

**Title:** ${bot.title}
**Kind:** ${bot.kind}
**Lane:** ${bot.lane}
**Skills (exclusive):** ${bot.skills.length ? bot.skills.join(", ") : "(none)"}

${bot.role}

## Rest of the staff

${peers}
`;
}

function copySkill(root, destSkills, name) {
  const src = join(root, "skills", name);
  const dest = join(destSkills, name);
  cpSync(src, dest, { recursive: true });
}

function writeHermesBot(root, outRoot, bot, roster) {
  const dir = join(outRoot, "hermes", bot.id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "distribution.yaml"), distributionYaml(bot));
  writeFileSync(join(dir, "SOUL.md"), soulMd(bot));
  writeFileSync(join(dir, "ROLE.md"), roleMd(bot, roster));
  writeFileSync(join(dir, ".gitignore"), profileGitignore());
  writeFileSync(
    join(dir, "README.md"),
    `# ${bot.id}

${bot.one_liner}

Hermes Bot Mode profile distribution for ${PACK} v${VERSION}.

\`\`\`bash
hermes profile install "${relative(ROOT, dir)}" --name ${bot.id} --alias -y
hermes -p ${bot.id} setup
\`\`\`

Local directory install — the paid zip is the distribution. There is no public git URL for these profiles.

Skills this bot owns: ${bot.skills.length ? bot.skills.join(", ") : "(none exclusive)"}.
`,
  );

  const destSkills = join(dir, "skills");
  if (bot.skills.length) {
    mkdirSync(destSkills, { recursive: true });
    for (const s of bot.skills) copySkill(root, destSkills, s);
    copySkill(root, destSkills, "seo-references");
  }
  if (bot.id === "midnight-support") {
    cpSync(join(root, "SUPPORT.md"), join(dir, "SUPPORT.md"));
  }
}

function staffMd(roster, operating) {
  const rows = roster
    .map(
      (b) =>
        `| \`${b.id}\` | ${b.title} | ${b.lane} | ${b.skills.length ? b.skills.map((s) => "`" + s + "`").join(", ") : "—"} |`,
    )
    .join("\n");
  return `# ${PACK} v${VERSION} — named staff

Eight specialists + a chief. Not a folder of files.

Every operating skill is assigned to **exactly one** specialist. Shared methodology (\`seo-references\`) is copied into skill-bearing Hermes profiles so each bot can read \`core.md\`; it is not a 16th skill.

| Bot | Title | Lane | Exclusive skills |
|---|---|---|---|
${rows}

Operating skills (${operating.length}): ${operating.map((s) => "`" + s + "`").join(", ")}.

## Hermes Bot Mode

Each \`hermes/<bot>/\` is a profile distribution (\`distribution.yaml\` at the root).

\`\`\`bash
# from the unpacked zip
for d in staff-bundles/hermes/midnight-*; do
  hermes profile install "$d" --name "$(basename "$d")" --alias -y
done
\`\`\`

Then \`hermes -p midnight-chief setup\` (and the same for each specialist you will actually run). Open the Bots tab in Hermes Desktop — each profile is a Bot.

These are static files. No cloud hosting, no usage gateway, no bulk Grok import.

## Grok Bot

Semi-manual. Create bots from \`grok/bot-cards.md\`, enable the lists in \`grok/enable-lists.md\`, follow \`grok/setup-checklist.md\`. No bulk import. On Grok, bots on one account share one cloud computer — names are not a security boundary.

## What this is not

Playbooks, not a ranking or citation guarantee. Email support is one clarification round at ${SUPPORT_EMAIL}. See \`SUPPORT.md\` at the pack root.
`;
}

function grokBotCards(roster) {
  const cards = roster
    .map((b) => {
      const skills =
        b.skills.length === 0
          ? "(none exclusive — paste the SOUL and the role)"
          : b.skills.map((s) => `/${s}`).join(", ");
      return `## ${b.id}

**Title:** ${b.title}
**Lane:** ${b.lane}
**Enable skills:** ${skills}

### Description (paste)

${b.one_liner}

### Instructions (paste)

${b.role}

---
`;
    })
    .join("\n");
  return `# Grok Bot cards — ${PACK} v${VERSION}

Create one Grok Bot per heading. No bulk import. Copy the title, description, and instructions into the Grok Bot UI. Then enable the skill names in \`enable-lists.md\`.

${cards}
`;
}

function grokEnableLists(roster) {
  const blocks = roster
    .map((b) => {
      const lines =
        b.skills.length === 0
          ? ["- (no pack skills to enable)"]
          : b.skills.map((s) => `- ${s}`);
      return `## ${b.id}\n\n${lines.join("\n")}\n`;
    })
    .join("\n");
  return `# Grok enable lists — ${PACK} v${VERSION}

After creating each bot from \`bot-cards.md\`, enable only that bot's exclusive skills. Do not enable all 16 on every bot — the point of staff is a lane.

Shared methodology (\`seo-references\`) should be readable by any skill-bearing bot if your host has a shared-skill slot; it is not an exclusive assignment.

${blocks}
`;
}

function grokChecklist(roster) {
  const creates = roster.map((b, i) => `${i + 1}. Create bot **${b.id}** from the matching card in \`bot-cards.md\`.`).join("\n");
  return `# Grok Bot setup checklist — ${PACK} v${VERSION}

Grok has no bulk import. Do this once per seat.

${creates}
${roster.length + 1}. For each bot, enable only the skills in \`enable-lists.md\`.
${roster.length + 2}. Paste the Instructions block as the bot's standing prompt. Do not add ranking guarantees.
${roster.length + 3}. Point the chief at the other eight names so it can route.
${roster.length + 4}. Confirm midnight-support's prompt still matches pack-root \`SUPPORT.md\`.
${roster.length + 5}. Smoke: ask midnight-chief "who runs a ChatGPT citation probe?" — it should name midnight-probe, not offer to run /geo itself.

On Grok, every bot on an account shares one cloud computer. Names are labels, not a security boundary.
`;
}

function rosterJson(roster, operating) {
  return {
    pack: PACK,
    version: VERSION,
    generated_by: "scripts/generate-staff.mjs",
    rule: "every operating skill assigned to exactly one specialist",
    counts: {
      specialists: roster.filter((b) => b.kind === "specialist").length,
      chiefs: roster.filter((b) => b.kind === "chief").length,
      operating_skills: operating.length,
      assigned_skills: assignedSkills(roster).length,
    },
    operating_skills: operating,
    bots: roster.map((b) => ({
      id: b.id,
      title: b.title,
      lane: b.lane,
      kind: b.kind,
      skills: b.skills,
      one_liner: b.one_liner,
    })),
  };
}

function parseDistributionName(text) {
  const m = text.match(/^name:\s*([A-Za-z0-9_-]+)\s*$/m);
  if (!m) throw new Error("distribution.yaml missing name");
  return m[1];
}

function walkFiles(dir, acc = []) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, ent.name);
    if (ent.isDirectory()) walkFiles(p, acc);
    else acc.push(p);
  }
  return acc;
}

function verifyOutput(outRoot, roster, operating) {
  const parsed = JSON.parse(readFileSync(join(outRoot, "roster.json"), "utf8"));
  if (parsed.counts.assigned_skills !== operating.length) {
    throw new Error("roster.json assigned_skills != operating length");
  }
  const seen = [];
  for (const bot of roster) {
    const dist = join(outRoot, "hermes", bot.id, "distribution.yaml");
    const soul = join(outRoot, "hermes", bot.id, "SOUL.md");
    if (!existsSync(dist) || !existsSync(soul)) {
      throw new Error(`missing hermes bundle for ${bot.id}`);
    }
    const name = parseDistributionName(readFileSync(dist, "utf8"));
    if (name !== bot.id) throw new Error(`distribution name ${name} != ${bot.id}`);
    const skillRoot = join(outRoot, "hermes", bot.id, "skills");
    for (const s of bot.skills) {
      const md = join(skillRoot, s, "SKILL.md");
      if (!existsSync(md)) throw new Error(`missing ${md}`);
      seen.push(s);
    }
    if (bot.skills.length) {
      if (!existsSync(join(skillRoot, "seo-references", "core.md"))) {
        throw new Error(`${bot.id} missing shared seo-references`);
      }
    }
  }
  const dupes = seen.filter((s, i) => seen.indexOf(s) !== i);
  if (dupes.length) throw new Error(`output skills duplicated: ${dupes.join(",")}`);
  const missing = operating.filter((s) => !seen.includes(s));
  if (missing.length) throw new Error(`output missing skills: ${missing.join(",")}`);

  for (const f of ["STAFF.md", "grok/bot-cards.md", "grok/enable-lists.md", "grok/setup-checklist.md"]) {
    if (!existsSync(join(outRoot, f))) throw new Error(`missing ${f}`);
  }
  const files = walkFiles(outRoot);
  return { bots: roster.length, files: files.length, skills: seen.length };
}

function generate(root, outRoot) {
  const operating = listOperatingSkills(root);
  if (operating.length !== 16) {
    throw new Error(`expected 16 operating skills, found ${operating.length}: ${operating.join(",")}`);
  }
  assertExactlyOnce(operating, ROSTER);
  rmSync(outRoot, { recursive: true, force: true });
  mkdirSync(join(outRoot, "hermes"), { recursive: true });
  mkdirSync(join(outRoot, "grok"), { recursive: true });

  for (const bot of ROSTER) writeHermesBot(root, outRoot, bot, ROSTER);

  writeFileSync(join(outRoot, "STAFF.md"), staffMd(ROSTER, operating));
  writeFileSync(join(outRoot, "roster.json"), JSON.stringify(rosterJson(ROSTER, operating), null, 2) + "\n");
  writeFileSync(join(outRoot, "grok", "bot-cards.md"), grokBotCards(ROSTER));
  writeFileSync(join(outRoot, "grok", "enable-lists.md"), grokEnableLists(ROSTER));
  writeFileSync(join(outRoot, "grok", "setup-checklist.md"), grokChecklist(ROSTER));
  writeFileSync(
    join(outRoot, "grok", "README.md"),
    `# Grok Bot setup pack — ${PACK} v${VERSION}\n\nStatic files. Semi-manual. Start at \`setup-checklist.md\`.\n`,
  );

  return verifyOutput(outRoot, ROSTER, operating);
}

function main(argv) {
  const check = argv.includes("--check");
  const outRoot = check
    ? join(mkdtempSync(join(tmpdir(), "midnight-staff-")), "staff-bundles")
    : join(ROOT, "staff-bundles");
  try {
    const stats = generate(ROOT, outRoot);
    const line = `staff-bundles ok bots=${stats.bots} exclusive_skills=${stats.skills} files=${stats.files} dest=${outRoot}`;
    console.log(line);
    if (check) {
      // Also assert the committed generator still matches ROSTER vs repo skills when run in-place later.
      rmSync(dirname(outRoot), { recursive: true, force: true });
    }
  } catch (err) {
    console.error(err instanceof Error ? err.message : err);
    process.exit(1);
  }
}

main(process.argv.slice(2));

