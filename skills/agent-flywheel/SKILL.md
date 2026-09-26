---
name: agent-flywheel
description: Operating method for running an agent team on GEO/SEO work — plan in cheap space, decompose into self-contained task cards, execute with a swarm, review in disciplined rounds until the work converges
when_to_use: Use when planning a multi-session GEO campaign, decomposing work into tasks for agent specialists or subagents, deciding whether to keep planning or start executing, running review passes on agent output, or when work keeps expanding instead of converging.
argument-hint: "<campaign, feature, or audit>"
---

# Agent Flywheel — running an agent team without improvising

The core economics: an error caught at planning costs 1x, at task decomposition 5x, in shipped code 25x. Most of your judgment belongs in the cheapest space. This skill is the operating discipline behind the Midnight staff — the chief routes with it, and any operator running their own agent team can apply it directly.

## The three spaces

| Space | You are deciding | Cost of a mistake |
|---|---|---|
| **Plan** | architecture, workflow, what "done" means | 1x — pure reasoning |
| **Cards** | task boundaries, order, what each agent needs to know | 5x — rework + coordination |
| **Execution** | files, code, fixes | 25x — implementation + cleanup |

**Stay-or-move rule:** if whole-workflow questions are still moving or a design debate is open, keep planning — refuse to start the swarm. Move to cards only when the remaining questions are about execution structure, ordering, and context, not about what the system is.

## Cards are executable memory

Every task card must be self-contained: the executing agent should never need to reopen the plan or the original conversation. A good card carries:

- full context (paths, constraints, prior findings),
- explicit dependencies (what must finish first),
- the verification obligation (what test or evidence proves it done),
- known failure modes to avoid.

Long, rich cards are correct. Terse bullet-titles are the failure mode: they force the agent to improvise architecture mid-execution, which is exactly where slop comes from.

## The plan-to-cards transition (where most teams fail)

Two disciplines, both mandatory:

1. **Convert explicitly.** When planning converges, decompose into cards in the same working session. A plan that is "decomposed" into nothing produces orphan work and duplicate chains. After decomposition, read the task list back and count: every plan element should appear in exactly one card, and every card should trace to a plan element.
2. **Kill duplicates immediately.** Two agents building the same thing from two interpretations of one plan is the most expensive silent failure in swarm work. The count-back is the detector.

## Review rounds that actually find things

Single review passes stop early — models (and humans) find 15-20 issues and declare satisfaction. Three techniques that break that:

- **Repeat the critique 5 times.** The same prompt, run again, finds what pass one's found-list hid. By pass three to five you are catching the subtle inconsistencies no single pass surfaces.
- **Overshoot the count.** Ask for "all 80+ problems" even when you suspect fewer — the claimed number keeps the search going past self-satisfaction.
- **Demand diffs.** "Show the exact text that changes and why" blocks vague review verdicts. A reviewer who cannot show the transformation has not done the review.
- **Fresh eyes.** When review improvements flatline, hand the work to a brand-new agent session with no accumulated assumptions. Stale reviewers re-see their own conclusions.

## Convergence — and when to stop differently

Iterations are done when three signals hold together: outputs shrinking, changes decelerating, successive rounds similar. But the red flags matter more than the count:

- **Oscillation** (alternating between two versions) → the framing is wrong; reframe, don't round again.
- **Expansion** (output growing each round) → something is adding complexity; cut scope.
- **Plateau at low quality** → kill the approach and restart fresh; more rounds will not fix a broken approach.

## Feature ideation on an existing site or campaign (Idea-Wizard)

1. Read current state + the existing task list (prevents duplicates).
2. Brainstorm 30 improvement ideas, self-select the best 5 with justification.
3. Ask for the "next best 10" → 15 total, each checked against the existing list for novelty.
4. You pick.
5. Picked ideas become cards; polish the cards 4-5 rounds before execution.

Generating 30 then winnowing beats asking for 5 directly: the winnow forces evaluation instead of listing.

## Adopting an external method (research-and-reimagine)

When a proven external system solved a problem you face: study the real thing firsthand (read the source, not memories of it) → push your first proposal past its conservative draft → **invert**: "what can we do that they cannot, because of what we already have?" → repeat critique passes after each expansion → convert every open question into a concrete decision before executing. Never port blindly; reimagine through your own capabilities.

## Escape hatch

Work too small for a card but too large to trust to memory: write a durable checklist where the next session will find it, never in conversation context. Promote to a real card the moment the work expands, depends on other work, or should survive into the project record.

## Running it with the Midnight staff

- **midnight-chief is the plan-space seat.** It routes, sequences, and owns the probe → fix → re-probe loop — which is this method's convergence loop, applied to citations.
- **Specialists are one-card executors.** Hand one self-contained card per handoff, with the verification obligation attached. Never hand a specialist a whole plan.
- **The probe → fix → re-probe loop is the flywheel:** each re-probe is a review round on the previous fix; convergence means the citation position holds without further churn.
- Keep campaign state in your notes system (per `seo-references/core.md`), so any agent — after any context reset — can reload the plan and cards without asking you what was decided.

## Honest constraints

No outcomes are guaranteed — not rankings, citations, traffic, or convergence speed. This is a working discipline, not a promise. Iteration costs tokens and time; the method spends them where they are cheapest (planning) instead of where they are dearest (rework).
