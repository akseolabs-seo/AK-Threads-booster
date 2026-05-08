#!/usr/bin/env python3
"""
AK-Threads-Booster: Refresh tracker metrics and append API-backed snapshots.

Usage:
    python update_snapshots.py --token YOUR_ACCESS_TOKEN [--tracker threads_daily_tracker.json]
    python update_snapshots.py --token YOUR_ACCESS_TOKEN --post-id 12345
    python update_snapshots.py --token YOUR_ACCESS_TOKEN --recent 5 --update-comments
    python update_snapshots.py --include-new-posts --update-comments --backup  # full daily refresh (token from $THREADS_API_TOKEN)

The script:
    - Reads an existing tracker JSON file
    - Fetches the latest metrics for selected posts via Threads API
    - Appends a snapshot entry to each selected post
    - Updates checkpoint fields (`performance_windows`) when the snapshot is near 24h / 72h / 7d
    - Optionally pulls in any new posts that aren't yet tracked (--include-new-posts)
    - Optionally backs up the tracker to `.bak-<ISO>` before writing (--backup)

The token can be passed via --token or the environment variable THREADS_API_TOKEN.
Env-var fallback is preferred for scheduled daily runs so the token isn't visible
in the process listing.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Make sibling scripts importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _atomic import (  # noqa: E402  (post-sys.path)
    atomic_write_json,
    configure_utf8_stdout,
    post_sort_key,
)

try:
    from fetch_threads import (
        RATE_LIMIT_DELAY,
        build_algorithm_signals,
        build_metric_snapshot,
        build_posting_time_slot,
        build_psychology_signals,
        build_review_state,
        classify_content_type,
        count_paragraphs,
        count_words,
        exchange_long_lived_token,
        fetch_all_threads,
        fetch_thread_insights,
        fetch_thread_replies,
        get_user_profile,
    )
except ImportError as exc:
    print(f"Error: could not import helper functions from fetch_threads.py: {exc}")
    sys.exit(1)

CHECKPOINT_TARGETS = {
    "24h": 24.0,
    "72h": 72.0,
    "7d": 168.0,
}


def ensure_extended_fields(post: dict) -> None:
    """Backfill newer tracker scaffolds on existing posts."""
    post.setdefault("algorithm_signals", build_algorithm_signals())
    post.setdefault("psychology_signals", build_psychology_signals())
    post.setdefault("review_state", build_review_state())


def load_tracker(tracker_path: str) -> dict:
    """Load tracker JSON from disk."""
    path = Path(tracker_path)
    if not path.exists():
        print(f"Error: tracker not found at {tracker_path}")
        sys.exit(1)

    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_tracker(tracker_path: str, tracker: dict) -> None:
    """Write tracker JSON back to disk per templates/FAILSAFE.md.

    Backup-then-atomic-rename is unconditional: a SIGKILL or OS reboot
    mid-write must never leave the user's tracker truncated. See
    `scripts/_atomic.atomic_write_json` for the contract.
    """
    atomic_write_json(tracker_path, tracker, backup=True, keep=5)


def build_new_post_entry(thread: dict, token: str) -> dict:
    """Build a full v1 post entry for a post that isn't yet in the tracker."""
    thread_id = thread["id"]
    text = thread.get("text", "")
    created_at = thread.get("timestamp", "")

    time.sleep(RATE_LIMIT_DELAY)
    metrics = fetch_thread_insights(thread_id, token)
    time.sleep(RATE_LIMIT_DELAY)
    replies = fetch_thread_replies(thread_id, token)

    snapshot_metrics = {
        "views": metrics.get("views", 0),
        "likes": metrics.get("likes", 0),
        "replies": metrics.get("replies", 0),
        "reposts": metrics.get("reposts", 0),
        "quotes": metrics.get("quotes", 0),
        "shares": 0,
    }

    return {
        "id": thread_id,
        "text": text,
        "created_at": created_at,
        "permalink": thread.get("permalink", ""),
        "media_type": thread.get("media_type", "TEXT"),
        "is_reply_post": False,
        "content_type": classify_content_type(text),
        "topics": [],
        "hook_type": None,
        "ending_type": None,
        "emotional_arc": None,
        "word_count": count_words(text),
        "paragraph_count": count_paragraphs(text),
        "posting_time_slot": build_posting_time_slot(created_at),
        "algorithm_signals": build_algorithm_signals(),
        "psychology_signals": build_psychology_signals(),
        "metrics": snapshot_metrics,
        "performance_windows": {"24h": None, "72h": None, "7d": None},
        "snapshots": [build_metric_snapshot(snapshot_metrics, created_at)],
        "prediction_snapshot": None,
        "review_state": build_review_state(),
        "comments": replies,
        "source": {
            "import_path": "api-delta",
            "data_completeness": "full",
        },
    }


def ingest_new_posts(tracker: dict, token: str) -> int:
    """Fetch the full thread list and append any posts not yet in the tracker.

    Returns the number of newly inserted posts.
    """
    print("  Listing posts from API to find new entries...")
    user = get_user_profile(token)
    threads = fetch_all_threads(user["id"], token)
    known_ids = {str(p.get("id", "")) for p in tracker.get("posts", [])}
    new_threads = [t for t in threads if str(t["id"]) not in known_ids]

    if not new_threads:
        print("  No new posts to ingest.")
        return 0

    print(f"  Found {len(new_threads)} new post(s); fetching full data...")
    for thread in new_threads:
        entry = build_new_post_entry(thread, token)
        tracker.setdefault("posts", []).insert(0, entry)

    # Re-sort newest-first on created_at so the tracker stays ordered.
    # ISO strings with mixed offsets (`+07:00` / `Z` / `+00:00`) compare
    # wrong lexicographically — use the timezone-aware key from _atomic.
    tracker["posts"].sort(key=post_sort_key, reverse=True)
    return len(new_threads)


def select_posts(posts: list, post_ids: list[str], recent: int, update_all: bool) -> list:
    """Select which posts should be refreshed."""
    if post_ids:
        wanted = set(post_ids)
        return [post for post in posts if str(post.get("id", "")) in wanted]

    if update_all:
        return posts

    return posts[:recent]


def snapshot_distance(snapshot: dict, target_hours: float) -> float:
    """Distance from a snapshot to a checkpoint target."""
    hours = snapshot.get("hours_since_publish")
    if hours is None:
        return float("inf")
    return abs(hours - target_hours)


def update_performance_windows(post: dict, snapshot: dict) -> None:
    """Update checkpoint windows if the new snapshot is a better fit."""
    performance_windows = post.setdefault("performance_windows", {})

    for key, target_hours in CHECKPOINT_TARGETS.items():
        current = performance_windows.get(key)
        new_distance = snapshot_distance(snapshot, target_hours)
        if new_distance == float("inf"):
            continue

        # Accept snapshots within a reasonable range around the checkpoint.
        if key == "24h" and new_distance > 12:
            continue
        if key == "72h" and new_distance > 24:
            continue
        if key == "7d" and new_distance > 48:
            continue

        current_distance = snapshot_distance(current or {}, target_hours)
        if current is None or new_distance < current_distance:
            performance_windows[key] = snapshot


def append_snapshot(post: dict, snapshot: dict) -> None:
    """Append or replace the latest snapshot if the run is too close to the previous one."""
    snapshots = post.setdefault("snapshots", [])
    if snapshots:
        last = snapshots[-1]
        last_captured_at = last.get("captured_at")
        current_captured_at = snapshot.get("captured_at")
        if last_captured_at == current_captured_at:
            snapshots[-1] = snapshot
            return

    snapshots.append(snapshot)


def refresh_post(post: dict, token: str, update_comments: bool) -> None:
    """Refresh a single post from the Threads API."""
    ensure_extended_fields(post)
    post_id = str(post.get("id", ""))
    created_at = post.get("created_at", "")
    metrics = fetch_thread_insights(post_id, token)

    snapshot_metrics = {
        "views": metrics.get("views", 0),
        "likes": metrics.get("likes", 0),
        "replies": metrics.get("replies", 0),
        "reposts": metrics.get("reposts", 0),
        "quotes": metrics.get("quotes", 0),
        "shares": post.get("metrics", {}).get("shares", 0),
    }
    captured_at = datetime.now(timezone.utc).isoformat()
    snapshot = build_metric_snapshot(snapshot_metrics, created_at, captured_at=captured_at)

    post["metrics"] = snapshot_metrics
    append_snapshot(post, snapshot)
    update_performance_windows(post, snapshot)

    if update_comments:
        time.sleep(RATE_LIMIT_DELAY)
        post["comments"] = fetch_thread_replies(post_id, token)


def main() -> None:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Refresh tracker metrics and append snapshots via Threads API"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("THREADS_API_TOKEN"),
        help="Threads API access token (defaults to $THREADS_API_TOKEN)",
    )
    parser.add_argument(
        "--app-secret",
        default=os.environ.get("THREADS_APP_SECRET"),
        help="App secret for long-lived token exchange (optional; $THREADS_APP_SECRET)",
    )
    parser.add_argument(
        "--tracker",
        default="threads_daily_tracker.json",
        help="Path to the tracker JSON file",
    )
    parser.add_argument(
        "--post-id",
        action="append",
        default=[],
        help="Specific post id to refresh (can be passed multiple times)",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=10,
        help="Refresh the most recent N posts when no --post-id is given",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Refresh all posts in the tracker",
    )
    parser.add_argument(
        "--update-comments",
        action="store_true",
        help="Refresh replies/comments for selected posts as well",
    )
    parser.add_argument(
        "--include-new-posts",
        action="store_true",
        help="Also fetch and insert any new posts not yet in the tracker (daily-refresh mode)",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help=(
            "Deprecated: backup is now always on per templates/FAILSAFE.md. "
            "Flag is accepted for backward compatibility with existing cron commands."
        ),
    )
    args = parser.parse_args()

    if not args.token:
        print("Error: no API token. Pass --token or set $THREADS_API_TOKEN.")
        sys.exit(1)

    token = args.token
    if args.app_secret:
        print("[1/4] Exchanging for long-lived token...")
        token = exchange_long_lived_token(token, args.app_secret)
    else:
        print("[1/4] Using provided token (skip long-lived exchange)")

    print("[2/5] Loading tracker...")
    tracker = load_tracker(args.tracker)
    posts = tracker.get("posts", [])
    if not isinstance(posts, list):
        print("Error: tracker posts field is not an array")
        sys.exit(1)

    new_post_count = 0
    if args.include_new_posts:
        print("[3/5] Checking for new posts via API...")
        new_post_count = ingest_new_posts(tracker, token)
        posts = tracker.get("posts", [])
    else:
        print("[3/5] Skipping new-post discovery (pass --include-new-posts to enable)")

    if not posts:
        print("Error: tracker contains no posts to refresh")
        sys.exit(1)

    selected_posts = select_posts(posts, args.post_id, args.recent, args.all)
    if not selected_posts:
        print("Error: no matching posts found in the tracker")
        sys.exit(1)

    print(f"[4/5] Refreshing metrics on {len(selected_posts)} post(s)...")
    for idx, post in enumerate(selected_posts, 1):
        post_id = str(post.get("id", ""))
        summary = post.get("text", "")[:40].replace("\n", " ")
        print(f"  [{idx}/{len(selected_posts)}] {post_id}: {summary}...")
        refresh_post(post, token, update_comments=args.update_comments)
        time.sleep(RATE_LIMIT_DELAY)

    tracker["last_updated"] = datetime.now(timezone.utc).isoformat()

    print("[5/5] Writing tracker (backup + atomic rename per FAILSAFE)...")
    save_tracker(args.tracker, tracker)
    print(
        f"Done. Refreshed {len(selected_posts)} post(s)"
        f"{f', ingested {new_post_count} new' if new_post_count else ''} in {args.tracker}"
    )


if __name__ == "__main__":
    main()
