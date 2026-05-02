# Phase 1: token-cost redesign — 77% reduction without functionality change

> **Status:** DRAFT — saved here, not yet posted to GitHub. User reviews + decides whether to open the PR against `akseolabs-seo/AK-Threads-booster:main`. See bottom for opening checklist.

## Why

Each invocation of `/analyze`, `/predict`, `/draft`, `/review`, or `/topics` currently auto-loads the full knowledge library (`psychology.md` + `algorithm.md` + `ai-detection.md` ≈ 100KB) and the user's full `threads_daily_tracker.json` (≈168KB on a real account, growing). That's ~95–110K tokens of context burned **before** the model sees the user's post — and 99% of it is reference material that won't actually be consulted on this turn.

This PR pushes that knowledge **out of the auto-loaded context and into queryable tools** that skills call only when needed.

## What changes

### Three new helper scripts (`scripts/`)

- **`tracker_query.py`** — narrow-slice CLI for `threads_daily_tracker.json`. 7 subcommands (`recent`, `top`, `comparable`, `hook-stats`, `ai-tone-stats`, `post`, `meta`), each returns 1–10KB of focused JSON. Skills now run these instead of `Read`-ing the full tracker.

- **`tracker_archive.py`** — bounds tracker size by moving posts older than `--keep-days` (default 60) into `archive/<YYYY>-<MM>.json`. Idempotent: no-op when there's nothing to archive. Maintains `top_performers_alltime[]` in the main tracker so summary skills always have historical anchors. Backs up before mutation, rotates to keep last 5 `.bak-*` files.

- **`build_tracker_summary.py`** — pre-computes `tracker_summary.md`, a ~5KB markdown digest covering top 10 alltime + last-30d, hook distribution, topic clusters, AI-tone signal frequencies, posting cadence, word-count quartiles, recent topic freshness. Skills `Read` this instead of the full tracker.

All three are pure stdlib (`json` + `argparse`), zero new deps. UTF-8 stdout reconfig handles Chinese content cleanly on Windows cp950.

### `/refresh` runs the new scripts post-merge

`skills/refresh/SKILL.md` Step 7.5: after the merged tracker is written, `/refresh` calls `tracker_archive.py` then `build_tracker_summary.py`. Both are non-fatal — same convention as the existing companion-regen step.

### Sub-skill SKILL.md edits (5 files)

`skills/analyze`, `predict`, `draft`, `review`, `topics`:

- **Knowledge files become reference material, not auto-load.** Skills use `Glob + Read --offset --limit` to pull *specific sections* when a particular signal needs evaluation. The "Required knowledge files" section is replaced with on-demand access guidance.
- **Path A (preferred)** reads `tracker_summary.md` (5KB) + companion files (`style_guide.md` / `concept_library.md` / `brand_voice.md`).
- **Comparable-set lookup** routes to `tracker_query.py comparable / top / recent`.
- **Path A-legacy preserved** for installs without `tracker_summary.md`. Skill prints "Reading full tracker — run `/refresh` to enable summary mode" and continues with old behavior.

The `brand_voice.md` observation-only rule, the discussion-mode hook, and every other piece of skill behavior are preserved verbatim. **No removed functionality.**

### A/B harness (`scripts/tests/ab_compare.py`)

Measures the deterministic *context-loading* cost of each skill before vs. after. Output equivalence on the analytical layer (classification quality, recommendations) requires real LLM calls and is left to manual validation; this harness covers the part that's mechanical and reproducible.

## Numbers

Real measurement against `@choeng_919`'s working dir on plugin v1.1.0 (see `ab_report.md`):

| Skill | Before bytes | After bytes | Tokens before | Tokens after | Reduction |
|-------|-------------:|------------:|--------------:|-------------:|----------:|
| `/analyze` | 353,557 | 76,299 | ~118K | ~25K | **78.4%** |
| `/predict` | 345,713 | 68,455 | ~115K | ~23K | **80.2%** |
| `/draft` | 353,490 | 72,136 | ~118K | ~24K | **79.6%** |
| `/review` | 253,201 | 69,702 | ~84K | ~23K | **72.5%** |
| `/topics` | 243,602 | 67,145 | ~81K | ~22K | **72.4%** |
| **5 skills** | **1,549,563** | **353,737** | **~516K** | **~118K** | **77.2%** |

The biggest single saving is replacing the 168KB tracker full-Read with the 5.5KB summary + on-demand 4KB queries.

## Tests

50 unittest cases, all green:

| Suite | Count |
|-------|------:|
| `test_tracker_query.py` | 22 |
| `test_tracker_archive.py` | 13 |
| `test_build_tracker_summary.py` | 7 |
| `test_ab_compare.py` | 8 |
| **Total** | **50** |

Coverage includes idempotency (re-running archive is a no-op), backup rotation (max 5 .bak files), dry-run isolation, comparable-set dedupe, archive-aware top-performer ranking, recent-window exclusion of archived posts, AI-tone signal counting, empty-tracker fallback, and CLI smoke.

```bash
cd <plugin-root> && python -m unittest discover -s scripts/tests
# Ran 50 tests in 0.139s
# OK
```

Smoke-tested against a real tracker (32 posts, 26-day window) — `tracker_query meta` and `build_tracker_summary` both work without errors. `tracker_summary.md` came out at 5,928 bytes, which hits the design target.

## Backwards compatibility

Every change keeps the old behavior reachable:

- Skills without `tracker_summary.md` fall through to `Path A-legacy` (full tracker Read) and print one line: "Reading full tracker (no `tracker_summary.md` found) — run `/refresh` to enable summary mode for faster invocations."
- `tracker_archive.py` is idempotent — first run on a long-history tracker creates an `archive/` dir, but on a tracker that has nothing past `--keep-days`, it's a no-op.
- `/refresh` post-merge calls are non-fatal — if archive or summary build fails, the next refresh retries; lean-path skills fall back to legacy.
- No schema change to `threads_daily_tracker.json`. `top_performers_alltime[]`, `last_archive_run`, and `archived_count` are additive fields added on first archiver run.
- No removed knowledge files, no removed sub-skills, no renamed paths.

## What's intentionally NOT in this PR

This is **Phase 1**. Two follow-ups are scoped in `PLAN-token-redesign-phase2-3.md` (also added in this branch) but **not** implemented here:

- **Phase 2:** TL;DR + appendix refactor of `psychology.md` / `algorithm.md` / `ai-detection.md`, plus a `kb_query.py` CLI for section-level lookup. Targets the remaining ~10–15% reduction.
- **Phase 3:** Sub-skill SKILL.md tightening (procedural-step compression) + subagent isolation for heavy analysis steps. Targets the remaining ~5%.

Phase 2/3 are diminishing returns and should land separately so this PR stays reviewable.

## Validation plan for reviewers

1. Pull the branch and run `python -m unittest discover -s scripts/tests` — should see 50 OK in <0.2s.
2. Pick a real tracker (your own, or any in your test setup) and run `python scripts/build_tracker_summary.py` — confirm `tracker_summary.md` is created at ~5KB and renders all 9 sections.
3. Run `python scripts/tests/ab_compare.py --working-dir <your-working-dir>` — confirm the per-skill reduction is meaningful (≥70% on the big skills).
4. Manually invoke `/analyze` on a recent post — confirm output quality matches your prior expectation. The lean path doesn't change *what* the skill produces, just *how cheaply* it gets there.

## Open questions for upstream maintainers

1. **Is the lean-by-default + legacy-fallback shape the right call**, or would you prefer a config flag (`token_redesign_mode: lean | legacy`) to gate behavior?
2. **`top_performers_alltime[]` schema** — added as a top-level array of slimmed post objects. Open to renaming or restructuring before merge.
3. **Phase 2/3** — happy to follow up with separate PRs; or close them out as out-of-scope if you'd rather call this redesign Done at Phase 1.

---

## Pre-flight checklist (when you decide to open the PR)

The branch is already pushed to `kennethlaw325/AK-Threads-booster:feat/token-redesign`. To open:

```bash
gh pr create \
  --repo akseolabs-seo/AK-Threads-booster \
  --base main \
  --head kennethlaw325:feat/token-redesign \
  --draft \
  --title "Phase 1: token-cost redesign — 77% reduction without functionality change" \
  --body-file PR-DESCRIPTION-DRAFT.md
```

Or open via the web link Git already gave you:
https://github.com/kennethlaw325/AK-Threads-booster/pull/new/feat/token-redesign

**Things to double-check before clicking go:**

- [ ] You're OK with the PR title — change to taste.
- [ ] You want this as a **draft** initially (recommended — gives upstream maintainers a beat to read before it's marked ready).
- [ ] You've manually `/analyze`'d a real post on the new branch and the output quality looks right (the harness can't measure this).
- [ ] You're fine with attribution — every commit message includes `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`.

---

*Drafted overnight 2026-05-02 — not yet posted to upstream. Reviewer-action token: see PR-DESCRIPTION-DRAFT in fork.*
