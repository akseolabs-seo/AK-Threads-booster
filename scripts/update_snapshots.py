#!/usr/bin/env python3
"""
AK-Threads-Booster: Refresh tracker metrics and append API-backed snapshots.

Usage:
    python update_snapshots.py --token YOUR_ACCESS_TOKEN [--tracker threads_daily_tracker.json]
    python update_snapshots.py --token YOUR_ACCESS_TOKEN --post-id 12345
    python update_snapshots.py --token YOUR_ACCESS_TOKEN --recent 5 --update-comments

The script:
    - Reads an existing tracker JSON file
    - Fetches the latest metrics for selected posts via Threads API
    - Appends a snapshot entry to each selected post
    - Updates checkpoint fields (`performance_windows`) when the snapshot is near 24h / 72h / 7d
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from fetch_threads import (
        RATE_LIMIT_DELAY,
        build_algorithm_signals,
        build_metric_snapshot,
        build_psychology_signals,
        build_review_state,
        exchange_long_lived_token,
        fetch_thread_insights,
        fetch_thread_replies,
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
    """Write tracker JSON back to disk."""
    with open(tracker_path, "w", encoding="utf-8") as fh:
        json.dump(tracker, fh, ensure_ascii=False, indent=2)


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
    parser = argparse.ArgumentParser(
        description="Refresh tracker metrics and append snapshots via Threads API"
    )
    parser.add_argument("--token", required=True, help="Threads API access token")
    parser.add_argument(
        "--app-secret",
        help="App secret for long-lived token exchange (optional)",
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
    args = parser.parse_args()

    token = args.token
    if args.app_secret:
        print("[1/4] Exchanging for long-lived token...")
        token = exchange_long_lived_token(token, args.app_secret)
    else:
        print("[1/4] Using provided token (skip long-lived exchange)")

    print("[2/4] Loading tracker...")
    tracker = load_tracker(args.tracker)
    posts = tracker.get("posts", [])
    if not isinstance(posts, list) or not posts:
        print("Error: tracker contains no posts to refresh")
        sys.exit(1)

    selected_posts = select_posts(posts, args.post_id, args.recent, args.all)
    if not selected_posts:
        print("Error: no matching posts found in the tracker")
        sys.exit(1)

    print(f"[3/4] Refreshing {len(selected_posts)} post(s)...")
    for idx, post in enumerate(selected_posts, 1):
        post_id = str(post.get("id", ""))
        summary = post.get("text", "")[:40].replace("\n", " ")
        print(f"  [{idx}/{len(selected_posts)}] {post_id}: {summary}...")
        refresh_post(post, token, update_comments=args.update_comments)
        time.sleep(RATE_LIMIT_DELAY)

    tracker["last_updated"] = datetime.now(timezone.utc).isoformat()

    print("[4/4] Writing tracker...")
    save_tracker(args.tracker, tracker)
    print(f"Done. Updated {len(selected_posts)} post(s) in {args.tracker}")


if __name__ == "__main__":
    main()
