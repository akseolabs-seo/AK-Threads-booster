# AK-Threads-Booster — Token Footprint Redesign Plan

**Branch:** `feat/token-redesign`
**Author:** Kenneth (with Claude Code)
**Date:** 2026-05-02
**Status:** Draft, awaiting approval to start Phase 1
**Goal:** Reduce per-invocation token cost by 70-90% **without removing or changing any user-facing functionality**.

---

## 1. Problem Statement

Current per-`/analyze` invocation auto-loads:

| File | Size | Tokens (est.) |
|---|---|---|
| `knowledge/psychology.md` | 858 lines / 43 KB | ~12-15K |
| `knowledge/algorithm.md` | 752 lines / 29 KB | ~8-10K |
| `knowledge/ai-detection.md` | 601 lines / 28 KB | ~8-10K |
| `knowledge/_shared/*.md` + `data-confidence.md` | ~150 lines | ~2K |
| `skills/analyze/SKILL.md` | 375 lines | ~5K |
| `threads_daily_tracker.json` | 168 KB (and growing) | ~40-50K |
| `style_guide.md` | 24 KB | ~6K |
| `concept_library.md` | 13 KB | ~3K |
| `brand_voice.md` | 15 KB | ~4K |
| **TOTAL baseline** | | **~90-110K tokens** |

These tokens are paid **before any analysis of the user's actual post**. The same baseline burden exists on `/draft`, `/predict`, `/review`, and `/topics` (each auto-loads similar combinations).

**Root cause:** The skill currently treats knowledge as **inlined context** rather than **queryable data**. Every invocation re-loads the entire reference library.

---

## 2. Design Principles

1. **Push knowledge out of context, into queryable tools.** LLM should not pre-load 100KB of reference material to maybe use 5KB of it. Same pattern as `grep` / `Read --offset --limit` — query on demand.
2. **Pre-compute aggregates.** Heavy aggregation (top performers, hook stats, AI-tone signal frequencies) should run once in `/refresh`, write derived files. Other skills read summaries.
3. **TL;DR + appendix structure.** Every knowledge file gets a thin TL;DR (auto-loaded) and a sectioned appendix (loaded on demand).
4. **Bounded tracker size.** Old posts archive monthly, recent window stays small.
5. **Backwards compatible.** Legacy file shapes still work; new shape is additive. No breaking change for users with existing setups.
6. **No functionality removal.** Same outputs, same quality. Only the path to producing them changes.

---

## 3. Phased Approach

| Phase | Scope | Token Reduction | Effort |
|---|---|---|---|
| **P1** | Tracker query CLI + monthly archive + derived summary | ~70% | ~1 day |
| **P2** | Knowledge file TL;DR refactor + `kb_query.py` CLI | ~10-15% additional | ~1 day |
| **P3** | Sub-skill SKILL.md tightening + subagent isolation for heavy steps | ~5% additional | ~0.5-1 day |

**Phase 1 captures the bulk of the gain** (tracker is the single largest hog). P2 and P3 are diminishing returns — worth doing but not blocking.

---

## 4. Phase 1 Detailed Spec

### 4.1 New Script: `scripts/tracker_query.py`

Query CLI exposing structured slices of `threads_daily_tracker.json` instead of forcing skills to read the whole file.

**Command surface:**

```bash
# Recent window — replaces full tracker read for /analyze, /predict
python scripts/tracker_query.py recent --days 30 [--include-comments]

# Top performers — for comparable-set construction
python scripts/tracker_query.py top --metric engagement --topic "<tag>" --limit 10

# Comparable set — by content_type / hook_type / topic_cluster
python scripts/tracker_query.py comparable --content-type list --hook-type question --topic AI --limit 10

# Hook stats — aggregated over window
python scripts/tracker_query.py hook-stats --days 60

# AI-tone signal frequency — for /analyze drift baseline
python scripts/tracker_query.py ai-tone-stats --days 60

# Single post lookup — for /predict, /review
python scripts/tracker_query.py post --id <post_id>
python scripts/tracker_query.py post --date 2026-05-01

# Tracker meta — schema version, post count, date range
python scripts/tracker_query.py meta
```

**Output:** JSON to stdout, ~1-10 KB per query.
**Implementation:** Pure stdlib (json + argparse). No new dependencies.
**Location:** `scripts/tracker_query.py` (alongside existing `fetch_threads.py`, `update_snapshots.py`).
**Tests:** `scripts/tests/test_tracker_query.py` — fixture-driven, covers each subcommand.

### 4.2 New Script: `scripts/tracker_archive.py`

Monthly archival to bound `threads_daily_tracker.json` size.

**Behavior:**
- Posts older than 60 days move to `archive/<YYYY>-<MM>.json`
- Main tracker keeps last 60 days + a frozen `top_performers_alltime[]` list (top 50 by engagement, immutable except when archiver runs)
- Existing backup convention preserved (`tracker.json.bak-<ISO>`)
- Idempotent: re-running on already-archived data is a no-op

**Command:**
```bash
python scripts/tracker_archive.py [--keep-days 60] [--top-n 50] [--dry-run]
```

**When invoked:** Hooked into `/refresh` workflow at the end (after merge), so archival runs on every refresh. Also runnable manually.

### 4.3 New Derived File: `tracker_summary.md`

Pre-computed aggregate written by `/refresh` for skills to read instead of full tracker.

**Contents (target ~5 KB):**
- Top 10 posts (alltime + last 30d)
- Hook type distribution (with engagement averages)
- Topic cluster distribution
- AI-tone signal baseline (frequency of detected AI phrases in user's own writing)
- Posting cadence summary
- Word count distribution (median, p25, p75)
- Recent topic freshness (last 30d)
- Schema version + last-refresh timestamp

**Generator:** `scripts/build_tracker_summary.py` (callable standalone or from `/refresh`).

**Skill consumption:** `/analyze`, `/predict`, `/topics` Read this instead of full tracker. Drop to `tracker_query.py` only when comparable-set lookup needs full data.

### 4.4 Sub-skill Updates

**`skills/analyze/SKILL.md` changes:**

Current (line ~37-41):
```
## Required knowledge files
... For /analyze specifically, load:
- psychology.md · algorithm.md · ai-detection.md · data-confidence.md
```

Replace with:
```
## Required reference files
- Read tracker_summary.md (canonical baseline)
- Read style_guide.md, concept_library.md, brand_voice.md if present (observation only)

## On-demand knowledge lookup
- For psychology signals → query kb_query.py (Phase 2) OR Read knowledge/psychology.md targeted sections
- For algorithm risk → same pattern
- For AI-tone detection → same pattern

DO NOT bulk-Read knowledge/*.md files at start. Look up only signals you actually need to evaluate.
```

Current (line ~50-57):
```
### Path A: Full system data (preferred)
... threads_daily_tracker.json, style_guide.md, concept_library.md, brand_voice.md
```

Replace with:
```
### Path A: Full system data (preferred)
- tracker_summary.md (always read — small)
- style_guide.md, concept_library.md, brand_voice.md (observation only)
- For comparable-set lookup: Bash `python scripts/tracker_query.py comparable --content-type X --hook-type Y --topic Z --limit 10`
- DO NOT bulk-Read threads_daily_tracker.json
```

Same edits applied to: `skills/predict/SKILL.md`, `skills/review/SKILL.md`, `skills/topics/SKILL.md`, `skills/draft/SKILL.md`.

`skills/refresh/SKILL.md` gets one addition at end:
```
## Post-merge derived outputs
After writing the merged tracker:
1. Run `python scripts/tracker_archive.py` (auto-archive >60d old)
2. Run `python scripts/build_tracker_summary.py` (regenerate tracker_summary.md)
3. Both run via Bash; LLM does not read the outputs.
```

### 4.5 Migration / Backwards Compatibility

- Users without `tracker_summary.md` (legacy installs): skill detects absence, falls back to current full-Read behavior, prints "Run /refresh to enable summary mode for faster invocations".
- Users without archive setup: same fallback.
- Old skills calling raw tracker still work (no removal of read paths, just deprioritized).
- No schema change to `threads_daily_tracker.json`.

### 4.6 Validation / Acceptance

| Check | Target |
|---|---|
| Token cost of `/analyze` on 30-post test fixture | <35K tokens (from ~100K) |
| Token cost of `/predict` on test fixture | <25K tokens |
| Output quality vs current — same fixture, same post submitted | A/B identical or equivalent classification + recommendations |
| `tracker_query.py` covers all current tracker access patterns in skills | Grep audit shows zero `Read threads_daily_tracker.json` in skill files (except setup/refresh) |
| Archive idempotency | Running twice produces zero diff |

A/B comparison harness:
```bash
python scripts/tests/ab_compare.py --post fixtures/sample_post.txt --skill analyze
# Outputs: tokens_before, tokens_after, classification_diff, recommendation_diff
```

### 4.7 Phase 1 Deliverables Checklist

- [ ] `scripts/tracker_query.py` + tests
- [ ] `scripts/tracker_archive.py` + tests
- [ ] `scripts/build_tracker_summary.py` + tests
- [ ] `scripts/tests/ab_compare.py` (validation harness)
- [ ] Sub-skill SKILL.md edits (analyze, predict, review, topics, draft)
- [ ] `skills/refresh/SKILL.md` post-merge step added
- [ ] One round of A/B validation with token counts in PR description
- [ ] CHANGELOG.md entry under Unreleased
- [ ] PR opened against upstream `main` (or kept on fork if not contributing back yet)

---

## 5. Phase 2 Outline

### 5.1 Knowledge File TL;DR Refactor

Each of `psychology.md`, `algorithm.md`, `ai-detection.md` splits into:

```
knowledge/psychology/
  TLDR.md            (~50 lines — rubric + signal category list)
  signals.json       (~200 entries, queryable structured form)
  examples/
    hook-types.md
    emotional-arcs.md
    sharing-motivation.md
    ...
```

Existing flat `psychology.md` becomes a thin pointer + back-compat re-export (concatenates the parts at build time so external consumers still see one file).

### 5.2 New Script: `scripts/kb_query.py`

```bash
python scripts/kb_query.py --doc psychology --topic hook-types
python scripts/kb_query.py --doc ai-detection --signals structural-perfection
python scripts/kb_query.py --doc algorithm --section suppression-risks
```

Returns 50-200 lines per query. Skills call this in their analysis loop instead of pre-loading full files.

### 5.3 Skill changes

Sub-skills replace "Load knowledge/X.md" with "Bash kb_query.py --doc X --topic Y when evaluating Z signal".

---

## 6. Phase 3 Outline

### 6.1 Sub-skill SKILL.md Tightening

Current `analyze/SKILL.md` is 375 lines. ~150 lines are narrative + edge case prose. Compress to:
- Numbered procedural steps (1-2 lines each, 60-80 lines total)
- Edge-case + example content moved to `analyze/playbook.md`
- LLM Reads playbook only when stuck or hitting an edge case

Apply same compression to `draft/`, `predict/`, `review/`, `topics/`, `voice/`.

### 6.2 Subagent Isolation for Heavy Analysis Steps

`/analyze` runs ~11-step analysis in main context. Steps that are independent + knowledge-heavy spawn isolated subagents:

- AI-tone detection subagent — loads only `ai-detection/` knowledge, returns verdict
- Suppression risk subagent — loads only `algorithm/` knowledge
- Hook classification subagent — loads only `psychology/hook-types/`

Main agent collects subagent verdicts, composes final report. Each subagent's context is discarded after returning, so main context never stacks 3 sets of knowledge.

Tradeoff: subagent overhead (start-up cost + serialization). Worth it only when knowledge load is large; skip for trivial steps.

---

## 7. Open Questions / Decisions Needed

1. **Contribute back to upstream?** Once Phase 1 is validated, do we open a PR to `akseolabs-seo/AK-Threads-booster`, or keep this as a private fork? Recommend: open the PR — the gain is generic and benefits all users.
2. **Schema version bump?** `tracker_summary.md` is additive, no schema change. But if Phase 2 changes knowledge file layout, that's a breaking change for forks/customizations. Need a `SCHEMA_VERSION` in tracker meta to gate behavior.
3. **A/B validation rigor.** How many sample posts does the harness need to call "equivalent quality"? Suggest 5-10 historical posts spanning content types.
4. **Phase 2/3 priority.** After Phase 1 ships, is the remaining 15-20% gain worth the effort, or do we stop at Phase 1 and reinvest the time elsewhere?

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Output quality regression after summary-only reads | A/B harness with hard equivalence check before merge |
| `tracker_query.py` misses an access pattern → skill falls back to full read silently | Grep audit + CI rule: zero raw-tracker reads in non-setup/refresh skills |
| Archive corrupts data during concurrent refresh | File lock + dry-run mode + always-backup-before-mutate (existing convention) |
| Users on legacy setups break | Fallback path detects missing summary and uses old behavior + prints upgrade hint |
| Upstream maintainer rejects PR (style / scope) | Plan keeps changes additive + behind backwards-compat fallbacks; worst case we run on fork only |

---

## 9. Next Step

**Awaiting approval to start Phase 1 implementation.**

If approved, work order:
1. Build `tracker_query.py` + tests (~3 hr)
2. Build `tracker_archive.py` + tests (~2 hr)
3. Build `build_tracker_summary.py` + tests (~2 hr)
4. Build A/B harness (~1 hr)
5. Edit sub-skill SKILL.md files (~1 hr)
6. Run validation, iterate (~1 hr)
7. Open PR with token-cost numbers (~30 min)

**Total: ~1 working day.**
