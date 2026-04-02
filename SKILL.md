---
name: ak-threads-booster
description: "Unified Threads operating system for setup, voice analysis, drafting, prediction, review, topic mining, and decision-first post analysis based on historical data."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# AK Threads Booster

Use this as the single entry point for the AK Threads workflow.

## Intent Routing

Classify the user's request first, then open and follow one primary module below unless the task clearly needs a short sequence.

- Setup / import / initialize / backfill history -> `${CLAUDE_SKILL_DIR}/skills/setup/SKILL.md`
- Analyze a finished post / inspect / AK-review a draft -> `${CLAUDE_SKILL_DIR}/skills/analyze/SKILL.md`
- Draft / write / 起草 / 幫我寫 -> `${CLAUDE_SKILL_DIR}/skills/draft/SKILL.md`
- Predict likely 24-hour performance / expectation check -> `${CLAUDE_SKILL_DIR}/skills/predict/SKILL.md`
- Review actual post performance / compare against prediction -> `${CLAUDE_SKILL_DIR}/skills/review/SKILL.md`
- Mine next topics / topic suggestions -> `${CLAUDE_SKILL_DIR}/skills/topics/SKILL.md`
- Build brand voice / voice analysis -> `${CLAUDE_SKILL_DIR}/skills/voice/SKILL.md`

## Routing Rules

1. Do not answer from this file alone when a module exists for the request.
2. Open the matched module and follow its workflow.
3. If the user asks for a combined task, use the smallest valid sequence:
   - first-use account workflow -> setup, then voice if needed
   - write from historical data -> setup or voice first if data is missing, then draft
   - post decision flow -> analyze, then predict if the user asks for a range
   - post-publication learning flow -> review
4. Keep outputs grounded in the user's own tracker whenever available.
5. If `threads_daily_tracker.json` is missing, do not pretend the work is data-backed. Ask for fallback history or use the setup path.

## Working Data

Look in the working directory for:

- `threads_daily_tracker.json`
- `style_guide.md`
- `concept_library.md`
- `brand_voice.md`

If only the tracker exists, continue in tracker-only fallback mode when the chosen module allows it.
