# Token Redesign — Phase 2 & Phase 3 Spec

**Branch:** `feat/token-redesign` (same branch as Phase 1; Phase 2/3 land in follow-up PRs once Phase 1 is reviewed)
**Author:** Kenneth (with Claude Code)
**Date drafted:** 2026-05-02 overnight session
**Status:** Spec — implementation deferred until Phase 1 PR is merged or feedback received
**Goal:** Capture the remaining ~15-20% of per-invocation token cost (P1 already shaved 77%)

---

## Why a separate doc

Phase 1 captured the bulk of the gain (1.55 MB → 0.35 MB across 5 skills, 77.2% reduction). Phase 2 + 3 push toward an asymptote — ~85-90% reduction at full implementation, but with diminishing returns and increased architectural complexity. They're worth doing only if Phase 1 is approved upstream and the user wants to keep iterating.

Splitting the spec keeps the PR-1 review surface bounded and gives reviewers a clear answer to "is there more?" without dragging the discussion into hypotheticals.

---

## Phase 2 — Knowledge file TL;DR refactor + `kb_query.py`

**Estimated effort:** 1 day
**Estimated additional reduction:** ~10-15% on top of Phase 1
**Status:** Specced, not implemented

### Problem (after Phase 1)

Phase 1's `analyze/SKILL.md` says "read targeted sections via Glob + Read --offset --limit only when a signal triggers a lookup". That works, but it leaves the heavy lifting to the LLM at runtime — every time it wants to consult `psychology.md` for, say, hook-types, it has to:

1. Glob to find the file
2. Guess the right line range, or read 50 lines and re-read if it landed in the wrong section
3. Repeat for the next signal

This costs tokens (the ~50-100 lines per consult) and turns each consult into a small reasoning operation. A query CLI is cheaper.

### Design

**Refactor each big knowledge file** into a directory with TL;DR + appendix structure:

```
knowledge/psychology/
  TLDR.md            (~50 lines — rubric + signal category list, auto-loadable)
  signals.json       (~200 entries: structured signal -> category mapping, queryable)
  examples/
    hook-types.md
    emotional-arcs.md
    sharing-motivation.md
    cognitive-biases.md
    ...
```

The legacy flat `psychology.md` becomes a thin pointer file that re-exports the parts (concatenated at build time so external consumers still see one file).

**Add `scripts/kb_query.py`** with subcommands:

```bash
python kb_query.py --doc psychology --topic hook-types
python kb_query.py --doc ai-detection --signal structural-perfection
python kb_query.py --doc algorithm --section suppression-risks
python kb_query.py --doc psychology --list-topics    # discoverability
python kb_query.py --doc psychology --search "share motive"
```

Each query returns 50-200 lines of focused content as plain text or markdown.

### Skill changes (Phase 2)

Update `skills/analyze`, `predict`, `draft`, `review`, `topics` — replace each "read targeted sections via Glob + Read --offset --limit" line with:

```markdown
For psychology signals → run `python scripts/kb_query.py --doc psychology --topic <category>` when evaluating that signal. The query returns 50-200 lines focused on that one category, far cheaper than guessing line ranges.
```

### Backwards compat

Existing flat `knowledge/psychology.md` etc. stay in place (concatenated build artifact + read by legacy installs that don't have `kb_query.py`). New structured `knowledge/psychology/` dir is additive.

### Migration risk

Highest in this phase. Splitting a knowledge file means defining the section taxonomy correctly the first time — wrong granularity hurts. Mitigate by:

- One knowledge file at a time (start with `psychology.md`, validate, then move to `algorithm.md`, then `ai-detection.md`)
- Keep the flat file generated from the parts at build time (or ship both flat + structured versions during transition)
- A/B harness in Phase 1 already includes `kb_query.py` cost as a 4KB synthetic; tune that estimate when real usage data exists

### Acceptance criteria

- [ ] `kb_query.py` covers every signal category referenced in any sub-skill SKILL.md
- [ ] A/B harness measures additional reduction ≥10% over Phase 1 baseline
- [ ] Output equivalence on a 5-post fixture vs Phase 1 baseline (no quality regression)
- [ ] Legacy installs still work (flat `psychology.md` etc. resolvable)
- [ ] Tests for `kb_query.py` cover all subcommands + missing topic + ambiguous topic + JSON output

---

## Phase 3 — Sub-skill tightening + subagent isolation

**Estimated effort:** 0.5-1 day
**Estimated additional reduction:** ~5% on top of Phase 2
**Status:** Specced, not implemented

### Problem

`skills/analyze/SKILL.md` is currently 416 lines. Roughly:

- ~100 lines: numbered procedural steps (necessary)
- ~150 lines: narrative + edge-case prose ("if X, then Y; here's why; here's an example")
- ~100 lines: output format specs (necessary)
- ~60 lines: front matter + headers + boundary reminders

The narrative is correct and helpful but it's loaded every invocation regardless of whether any edge case actually fires.

### Design (Phase 3.1 — tightening)

For each sub-skill (5 files), produce a leaner SKILL.md:

- Numbered procedural steps stay (1-2 lines each, ~80 lines total)
- Output format spec stays (it's actually consulted)
- Edge case + example prose moves to `<skill>/playbook.md` (loaded only when the LLM hits an edge case it can't resolve from the lean spec)
- Boundary reminders trimmed to 5 lines max — the rest goes into playbook

Estimated per-skill SKILL.md size: 416 lines → ~150 lines. Cumulative across 5 skills: -1300 lines auto-loaded per invocation (lol it's the same skill that loads though, so really -260 lines per typical call). At ~0.3 tokens/byte and ~30 chars/line, that's ~2-3K tokens saved per call.

### Design (Phase 3.2 — subagent isolation)

`/analyze` Step 5 (Algorithm Alignment) and Step 6 (AI-Tone Detection) are independent enough to run in isolated subagents:

- **AI-tone subagent** — gets only `ai-detection/TLDR.md` + the post text; returns a structured verdict.
- **Suppression-risk subagent** — gets only `algorithm/TLDR.md` + the post text + comparable set; returns a risk list.
- **Hook-classification subagent** — gets only `psychology/hook-types/` + the post text; returns hook type + alignment notes.

Main `/analyze` agent collects subagent verdicts and composes the final report. Each subagent's context is discarded after returning — the main context never stacks all three knowledge sets simultaneously.

**Tradeoff:** subagent invocation has overhead (start-up cost + serialization). Worth it only when knowledge load is heavy; skip for trivial steps. Phase 3.2 includes a benchmark step before/after to confirm net positive.

### Phase 3 SKILL.md changes

For each of the 5 sub-skills:

```markdown
## Edge cases / examples
For unusual cases (post in mixed languages, post with embedded image references,
fragment-style posts, ...), see `analyze/playbook.md`.

## Heavy step subagents (analyze only)
Steps 5 (Suppression Risk Scan) and 6 (AI-Tone Detection) may dispatch
isolated subagents for independent evaluation. See `analyze/subagent-protocol.md`.
```

### Acceptance criteria

- [ ] A/B harness measures additional ≥5% reduction over Phase 2 baseline
- [ ] Subagent invocation cost is documented (typical token overhead per dispatch)
- [ ] Output quality on the same 5-post fixture matches Phase 2 baseline
- [ ] Playbook files are clearly cross-referenced from the slim SKILL.md
- [ ] Subagent protocol covers the 3 named heavy steps end-to-end with examples

---

## Cumulative target (P1 + P2 + P3)

| Phase | Cumulative reduction | Per-call tokens (analyze) |
|------:|----------------------|--------------------------:|
| Baseline (v1.1.0) | 0% | ~118K |
| **P1 (this PR)** | **~77%** | **~25K** |
| P2 | ~87% | ~15K |
| P3 | ~92% | ~10K |

Numbers compound roughly multiplicatively because each phase trims a different layer (P1: data, P2: knowledge, P3: prose + isolation).

---

## Decision points

When (and if) Phase 1 is merged upstream, three things determine whether to proceed:

1. **Real usage measurement.** Does Phase 1 alone solve the user's pain? If `/analyze` now runs in 25K tokens and that's "fine", Phase 2's 10K extra savings may not justify the migration risk of splitting knowledge files.
2. **Upstream appetite.** If `akseolabs-seo` accepted Phase 1 cleanly, Phase 2/3 are straightforward extensions. If Phase 1 had pushback on the lean/legacy duality, doubling down on more layered structure is a worse fit.
3. **Phase 2 migration scope.** Splitting `psychology.md` (43KB) into a structured directory is non-trivial. If the user has accumulated meaningful manual edits to that file (or any other plugin user has), the migration cost can outweigh the token gain.

Recommended posture: **ship Phase 1 first, measure for 1-2 weeks, then decide on Phase 2.** Phase 3 only after Phase 2 lands.

---

## Open questions

- **Where does `kb_query.py` live?** `scripts/` alongside `tracker_query.py`? Or `knowledge/_query/`? Phase 2 spec assumes `scripts/`; revisit if upstream prefers separation.
- **Should the structured knowledge dirs ship inside the plugin, or as a separate package?** Tying them to the plugin keeps installs simple; separating allows independent versioning. Probably keep bundled for now.
- **Subagent dispatch tooling.** Phase 3.2 assumes Claude Code's `Agent` tool is the dispatch mechanism. Codex CLI integration with subagents needs verification before Phase 3 commits to a specific protocol.
