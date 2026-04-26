# Shared Config: `threads_booster_config.json`

This file is the **single source of truth** for all AK-Threads-Booster runtime toggles. Any skill that reads or writes these values must link here rather than duplicate the schema.

---

## File Location

Working directory root: `threads_booster_config.json`. If absent, all skills use the documented defaults.

## Full Schema

```json
{
  "draft": {
    "discussion_mode": "ask | always_on | always_off",
    "research_angle_expansion": true
  },
  "analyze": {
    "discussion_mode": "ask | always_on | always_off"
  },
  "review": {
    "discussion_mode": "ask | always_on | always_off"
  }
}
```

## Defaults

When a key is absent:

| Key | Default | Meaning |
|---|---|---|
| `*.discussion_mode` | `"ask"` | Prompt the user once per skill, persist their answer |
| `draft.research_angle_expansion` | `true` | During research, surface angles the user may not have considered |

## `discussion_mode` — canonical semantics

These rules apply identically to `/draft`, `/analyze`, `/review`:

| Value | Behavior |
|---|---|
| `"ask"` | On the **first invocation** of this skill (= `discussion_mode` key absent OR equal to `"ask"`), prompt: *"Want me to pause and discuss / ask follow-up questions? You can answer just this run, or say 'always on' / 'always off' and I'll remember."* Apply the answer for this run. If the user chose `always_on` / `always_off`, persist to the config file (see Persistence below). If they answered only for this run, leave `discussion_mode` as `"ask"` — the skill will ask again next time. |
| `"always_on"` | Run the discussion/questions block every time. No prompt. |
| `"always_off"` | Skip the discussion/questions block. Always offer a one-line opt-in at the end: *"Want me to dig deeper? Say the word."* Safety checks (personal-fact conflicts, red-line warnings) still run — those are not "discussion". |

**Skill-specific mapping** (what the "discussion/questions block" actually is in each skill):

- `/draft` → Step 3c (research discussion) and Step 6 (post-draft improvement questions). Both gated by the same toggle.
- `/analyze` → Section 11 "Questions for You" in the output.
- `/review` → "Questions for You" section in the final report.

## Persistence

Only `/draft` has `Write` in its `allowed-tools` among skills using this config. Therefore:

- **Only `/draft` writes `threads_booster_config.json`.** If a user tells `/analyze` or `/review` "always off", those skills must not write the file — instead, acknowledge the preference for the current run and tell the user: *"To make this permanent, tell `/draft` (which can write the config), or edit `threads_booster_config.json` directly."*
- When `/draft` persists a choice, it writes only the changed key, preserving all other existing keys. If the file does not exist, `/draft` creates it with just that key set.

## reason + strip_when

| Component | Reason | Strip when |
|---|---|---|
| `discussion_mode` toggle | Users differ: some want deep dialogue, some want fast output. A single default alienates one group. | Product telemetry shows >95% of users keep the same mode → remove the toggle and adopt that mode as fixed behavior. |
| `research_angle_expansion` toggle | Surfaced angles occasionally derail users who already know what they want to say. Opt-out exists for that case. | If post-publish data shows accepted angles consistently lift performance, flip default to always-on and remove the toggle. |
| `ask` mode | Reduces friction for new users who don't yet know which mode fits them. | After 2-3 skill invocations, most users have converged — if logs show `ask` mode rarely persists beyond N runs, collapse to a binary default + one setup question. |

## Conflict Resolution

If a skill's documented behavior contradicts this file, **this file wins.** Update the skill to match, not the other way around.
