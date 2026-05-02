---
name: refresh
description: "Refresh threads_daily_tracker.json. Prefer the Threads API when available; fall back to Chrome MCP profile scraping when API access is not available. Trigger words: 'refresh', 'update tracker', 'scrape profile', '更新貼文', '抓最新數據'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__javascript_tool, mcp__Claude_in_Chrome__tabs_create_mcp, mcp__Claude_in_Chrome__tabs_close_mcp
---

# AK-Threads-Booster Profile Refresh Module

You are the tracker-refresh worker for the AK-Threads-Booster system. Your job is to pull the user's latest posts, metrics, and comments, then merge them into `threads_daily_tracker.json` without losing existing data.

Two refresh sources are supported and must be tried in this order:

1. **Threads API** - preferred when a token is available. Faster, more reliable, and better for scheduled refresh.
2. **Chrome MCP** - fallback for users who cannot or do not want to use the API. Scrapes the user's own logged-in Threads profile.

Chrome scraping is slower and more fragile than the API. Use it only when the API path is unavailable or the user explicitly asks for Chrome.

---

## Step 0: Pick the Refresh Source

Choose the source in this order:

1. **API path** if any of these are true:
   - `$ARGUMENTS` contains `--token <value>` or `--api`
   - the environment variable `THREADS_API_TOKEN` is set
   - the tracker says `account.source = "api"` and the user confirms the token is still valid

   Run:

   ```bash
   python scripts/update_snapshots.py \
     --tracker "<user-working-dir>/threads_daily_tracker.json" \
     --include-new-posts \
     --update-comments \
     --backup
   ```

   The token should come from `THREADS_API_TOKEN` unless the user passed `--token` explicitly.

   After a successful API refresh, regenerate companion files with:

   ```bash
   python scripts/render_companions.py --tracker "<tracker-path>" --output-dir "<dir>"
   ```

   Then stop. Do not run the Chrome flow.

2. **Chrome path** only if the API path is not available. Continue with the Chrome flow below.

If the user explicitly asks for Chrome scraping, honor that even if an API token exists, but mention the override in the final summary.

---

## Execution Modes

`/refresh` runs in one of two modes.

### Interactive mode

Triggered when the user invokes `/refresh` directly in a live session. Interactive mode may:

- ask for missing handle or confirmation
- tell the user to log in and retry
- pause for user action

### Headless mode

Triggered when `/refresh` is invoked by a scheduler, another skill, or with `--headless` in `$ARGUMENTS`. Headless mode must:

- not ask questions
- not pause for user action
- read inputs from the tracker or exit fast
- fail within bounded time if login or selector health checks fail

Recognized headless arguments:

| Arg | Meaning | Default |
|-----|---------|---------|
| `--headless` | headless mode | off |
| `--handle @name` | target profile handle | tracker value |
| `--max-posts N` | stop after N posts | 200 |
| `--max-minutes N` | hard runtime limit | 5 |
| `--force` | bypass recent-refresh skip | off |
| `--log-file PATH` | log file path | `threads_refresh.log` |

### Headless log contract

When headless mode aborts, append one JSON line:

```json
{"ts":"<ISO>","ok":false,"reason":"login_wall|handle_mismatch|no_chrome_mcp|selector_health_failed|timeout|backup_failed|other","detail":"<short>"}
```

On success, append:

```json
{"ts":"<ISO>","ok":true,"posts_scraped":N,"new_posts":X,"updated_posts":Y,"replies_added":Z}
```

`/review` reads `threads_refresh.log`, so do not skip logging in headless mode.

---

## Preconditions

Before starting the Chrome path, verify all of the following:

1. **Chrome MCP exists**  
   The Chrome tools in `allowed-tools` must be callable.  
   Interactive: tell the user to install Chrome MCP.  
   Headless: log `no_chrome_mcp` and exit.

2. **Threads is logged in**  
   Navigate to `https://www.threads.com/` and confirm the page is a logged-in feed.  
   Interactive: tell the user to log in and retry.  
   Headless: log `login_wall` and exit.

3. **Logged-in account matches the target handle**  
   Read the signed-in handle from the page.  
   Interactive: ask which account to use.  
   Headless: log `handle_mismatch` and exit.

4. **The target handle is known**  
   Interactive may ask.  
   Headless requires `--handle` or `account.handle` in the tracker.

---

## Principles and Knowledge

Load `knowledge/_shared/principles.md` before scraping. Follow discovery order in `knowledge/_shared/discovery.md`. For `/refresh`, also load:

- `data-confidence.md`
- `chrome-selectors.md`

Never hard-code selectors in this skill. `chrome-selectors.md` is the source of truth.

---

## Chrome Execution Flow

### Step 1: Load or Create Tracker

1. Glob for `threads_daily_tracker.json`.
2. If found, read it and record existing post IDs plus `last_updated`.
3. If not found, create a minimal skeleton:

```json
{
  "account": { "handle": "", "source": "chrome-scrape", "timezone": "UTC" },
  "posts": [],
  "last_updated": null
}
```

Interactive mode may ask for the handle if needed.

### Step 2: Navigate to the Profile

Navigate to `https://www.threads.com/@<handle>` and confirm the header handle matches the requested handle.

### Step 2.5: Selector Health Check

Run the selector health check defined in `knowledge/chrome-selectors.md`:

1. Count elements matching the post-card selector.
2. If zero and a login-wall selector matches, abort with `login_wall`.
3. If zero and no login wall matches, abort with `selector_health_failed`.
4. If one or more cards are present, continue.

This step is mandatory. Do not continue if it fails.

### Step 3: Scroll and Collect Posts

Use `javascript_tool` to scroll until:

- no new posts load
- `--max-posts` is reached
- `--max-minutes` is reached

Use the post-card selector from `chrome-selectors.md` as the count target.

### Step 4: Extract Post Data

Extract a JSON array with:

- `id`
- `text`
- `created_at`
- `permalink`
- `media_type`
- `metrics.likes`
- `metrics.replies`
- `metrics.reposts`
- `metrics.quotes`
- `metrics.shares`
- `metrics.views` when visible

If a metric token cannot be parsed, preserve the last-known tracker value instead of writing a bad value.

### Step 5: Extract Replies

For each post that is new or whose reply count changed:

1. Open the permalink in a new tab.
2. Extract replies.
3. If a reply author matches the logged-in handle, append it to `author_replies[]` and set `my_replies = true`.
4. Close the tab.

Skip reply scraping when the reply count has not changed since the last refresh.

### Step 5.5: Sweep Expired Prediction Placeholders

Before merging, scan `posts[]` for expired `pending-` placeholders:

- move expired ones into `discarded_drafts[]`
- preserve `prediction_snapshot` and text
- add `discarded_at = now`
- remove them from `posts[]`

If a pending placeholder matches a newly scraped post, merge the prediction snapshot into the real post entry and remove the placeholder.

### Step 6: Merge Into Tracker

Merge rules:

1. Existing post, same metrics -> leave unchanged
2. Existing post, new metrics -> update metrics and append a new snapshot
3. Existing post, new replies -> append replies, do not delete old ones
4. New post -> insert with the current tracker skeleton
5. Existing `prediction_snapshot` -> keep untouched
6. If the snapshot lands near 24h / 72h / 7d, also fill `performance_windows`

Always update `last_updated` to the refresh timestamp.

### Step 7: Persist

Persistence intentionally writes more than one file. That is allowed in this skill because backup, audit, and companion files are part of the refresh contract.

Before writing:

1. Copy the current tracker to `threads_daily_tracker.json.bak-<ISO>`
2. Keep only the 5 newest backups
3. If backup fails, abort and report the error

Then:

1. Write the merged tracker back to `threads_daily_tracker.json`
2. Regenerate companion files with `scripts/render_companions.py`
3. In headless mode, write success or failure to `threads_refresh.log`

Companion regeneration failures are non-fatal. Note them in the summary, but do not roll back a successful tracker write.

### Step 7.5: Post-merge derived outputs (Phase 1 token redesign)

After the merged tracker is written, regenerate the derived files that other skills (`/analyze`, `/predict`, `/review`, `/topics`, `/draft`) read instead of the full tracker. This is what makes the lean baseline path work.

Run from the working directory:

```bash
python <plugin>/scripts/tracker_archive.py
python <plugin>/scripts/build_tracker_summary.py
```

`<plugin>` resolves via `Glob **/scripts/tracker_archive.py` (same pattern as the other scripts).

Behavior:

- `tracker_archive.py` — moves posts older than 60 days into `archive/<YYYY>-<MM>.json`. Idempotent: no-op when there are no aged-out posts. Maintains `top_performers_alltime[]` in the main tracker so summary skills always have historical anchors.
- `build_tracker_summary.py` — writes `tracker_summary.md` (~5KB markdown digest with top-10 alltime + last-30d, hook distribution, topic clusters, AI-tone signal frequencies, posting cadence, word-count quartiles, recent topic freshness).

Both scripts are non-destructive: they back up before mutating and rotate `.bak-<ISO>` files to keep 5 most recent.

These post-merge calls are **non-fatal** — like companion regeneration. If either script fails, log the error and continue. The next `/refresh` will retry. Skills with the lean Path A will fall back to Path A-legacy (full tracker Read with upgrade hint) when `tracker_summary.md` is stale or missing.

### Step 8: Report

Report in this shape:

```text
## Refresh Summary
- Handle: @<handle>
- Posts scraped: X (Y new, Z updated)
- Replies added: N (M from the account itself, available to /topics as validated demand)
- Performance windows filled: 24h=<k>, 72h=<k>, 7d=<k>
- Tracker level: <Directional / Weak / Usable / Strong / Deep>
- last_updated: <ISO>
```

If the refresh was partial, list the failed post IDs or the failed stage.

---

## Scheduling

Tell the user once, after the first successful run, that `/refresh` can be scheduled automatically:

- API users can schedule `scripts/update_snapshots.py`
- Chrome users can schedule `/refresh --headless`

Chrome must already be running and logged in when the headless job fires.

---

## Failure Modes

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `navigate` lands on a login page | Chrome session lost login | tell user to log in and retry |
| Scroll stops early | Threads soft rate-limit | save partial state and report it |
| Timestamps all look wrong | relative-time selector drift | update selector mapping |
| Numbers parse as `NaN` | metric parser missed a unit | extend parser before writing |
| Refresh ran within the last 10 minutes | redundant refresh | skip unless `--force` |

---

## Boundary Reminders

- It is valid for this skill to write the tracker, backup files, refresh log, and companion files. Those writes are part of the contract.
- Do not modify `prediction_snapshot`, `review_state`, or enriched analysis fields outside the merge rules above.
- If a post is no longer visible on profile, report it but do not delete historical data.
- Chrome MCP actions must stay inside `threads.com` during this flow.
