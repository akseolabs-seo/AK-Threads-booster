#!/usr/bin/env python3
"""
AK-Threads-Booster: Fetch historical posts via Meta Threads API.

Usage:
    python fetch_threads.py --token YOUR_ACCESS_TOKEN [--output threads_daily_tracker.json]

Prerequisites:
    1. Create a Meta Developer App at https://developers.facebook.com/
    2. Add "Threads API" product to your app
    3. Generate a User Access Token with threads_basic, threads_content_publish,
       threads_read_replies, threads_manage_insights permissions
    4. Exchange for a long-lived token (valid 60 days)

The script will:
    - Fetch all your historical Threads posts
    - Fetch metrics (views, likes, replies, reposts, quotes) for each post
    - Fetch reply threads (comments) for each post
    - Output a tracker JSON file in AK-Threads-Booster standard format
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' package is required.")
    print("Install it with: pip install requests")
    sys.exit(1)

API_BASE = "https://graph.threads.net/v1.0"

# Threads API rate limits: 250 calls per user per hour
RATE_LIMIT_DELAY = 0.5  # seconds between API calls


def get_user_profile(token: str) -> dict:
    """Get the authenticated user's Threads profile."""
    resp = requests.get(
        f"{API_BASE}/me",
        params={"fields": "id,username", "access_token": token},
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "id": data["id"],
        "username": data.get("username", ""),
    }


def fetch_all_threads(user_id: str, token: str) -> list:
    """Fetch all threads (posts) for the user, handling pagination."""
    all_threads = []
    url = f"{API_BASE}/{user_id}/threads"
    params = {
        "fields": "id,text,timestamp,media_type,shortcode,permalink,is_reply",
        "limit": 50,
        "access_token": token,
    }

    page = 1
    while url:
        print(f"  Fetching posts page {page}...")
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        posts = data.get("data", [])
        # Filter out replies — only keep original posts
        original_posts = [p for p in posts if not p.get("is_reply", False)]
        all_threads.extend(original_posts)

        # Handle pagination
        paging = data.get("paging", {})
        url = paging.get("next")
        params = {}  # next URL already contains params
        page += 1
        time.sleep(RATE_LIMIT_DELAY)

    return all_threads


def fetch_thread_insights(thread_id: str, token: str) -> dict:
    """Fetch metrics for a single thread."""
    metrics = {
        "views": 0,
        "likes": 0,
        "replies": 0,
        "reposts": 0,
        "quotes": 0,
    }

    try:
        resp = requests.get(
            f"{API_BASE}/{thread_id}/insights",
            params={
                "metric": "views,likes,replies,reposts,quotes",
                "access_token": token,
            },
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

        for item in data:
            name = item.get("name", "")
            if name in metrics:
                # Insights API returns values in different formats
                values = item.get("values", [{}])
                if values:
                    metrics[name] = values[0].get("value", 0)

    except requests.exceptions.HTTPError as e:
        # Some posts may not have insights available (too old, etc.)
        print(f"    Warning: Could not fetch insights for {thread_id}: {e}")

    return metrics


def fetch_thread_replies(thread_id: str, token: str) -> list:
    """Fetch replies (comments) for a single thread."""
    replies = []
    url = f"{API_BASE}/{thread_id}/replies"
    params = {
        "fields": "id,text,timestamp,username",
        "limit": 50,
        "access_token": token,
    }

    while url:
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            for reply in data.get("data", []):
                replies.append({
                    "user": reply.get("username", ""),
                    "text": reply.get("text", ""),
                    "created_at": reply.get("timestamp", ""),
                    "likes": 0,  # Reply likes not available via basic API
                })

            paging = data.get("paging", {})
            url = paging.get("next")
            params = {}
        except requests.exceptions.HTTPError:
            break
        time.sleep(RATE_LIMIT_DELAY)

    return replies


def classify_content_type(text: str) -> str:
    """Basic content type classification based on text patterns."""
    if not text:
        return "other"

    # Simple heuristic classification
    if "?" in text or "？" in text:
        if text.strip().endswith("?") or text.strip().endswith("？"):
            return "question"
    if any(marker in text for marker in ["1.", "2.", "3.", "一、", "二、", "第一", "步驟"]):
        return "tutorial"
    if any(marker in text for marker in ["數據", "data", "%", "成長", "增長"]):
        return "data-insight"
    if any(marker in text for marker in ["我的經驗", "我之前", "那時候", "故事"]):
        return "story"

    return "opinion"


def count_words(text: str) -> int:
    """Estimate word count from whitespace-separated tokens."""
    return len(text.split()) if text else 0


def count_paragraphs(text: str) -> int:
    """Count non-empty paragraphs."""
    if not text:
        return 0
    return len([chunk for chunk in text.splitlines() if chunk.strip()])


def build_posting_time_slot(timestamp: str) -> Optional[str]:
    """Convert an ISO timestamp into a coarse posting-time bucket."""
    if not timestamp:
        return None

    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None

    hour = dt.hour
    if hour < 6:
        window = "00:00-05:59"
    elif hour < 12:
        window = "06:00-11:59"
    elif hour < 18:
        window = "12:00-17:59"
    else:
        window = "18:00-23:59"

    return f"{dt.strftime('%a')} {window}"


def parse_iso_datetime(timestamp: str) -> Optional[datetime]:
    """Parse an ISO timestamp into a datetime."""
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def build_metric_snapshot(metrics: dict, created_at: str, captured_at: Optional[str] = None) -> dict:
    """Create a metrics snapshot entry for the tracker."""
    captured = captured_at or datetime.now(timezone.utc).isoformat()
    created_dt = parse_iso_datetime(created_at)
    captured_dt = parse_iso_datetime(captured)
    hours_since_publish = None

    if created_dt and captured_dt:
        delta = captured_dt - created_dt
        hours_since_publish = round(delta.total_seconds() / 3600, 2)

    return {
        "captured_at": captured,
        "hours_since_publish": hours_since_publish,
        "views": metrics.get("views", 0),
        "likes": metrics.get("likes", 0),
        "replies": metrics.get("replies", 0),
        "reposts": metrics.get("reposts", 0),
        "quotes": metrics.get("quotes", 0),
        "shares": metrics.get("shares", 0),
    }


def build_algorithm_signals() -> dict:
    """Create an empty algorithm-signals scaffold for a post."""
    return {
        "discovery_surface": {
            "threads": None,
            "instagram": None,
            "facebook": None,
            "profile": None,
            "topic_feed": None,
            "other": None,
        },
        "topic_graph": {
            "topic_tag_used": None,
            "topic_tag_count": None,
            "topic_match_clarity": None,
            "single_topic_clarity": None,
            "bio_topic_match": None,
        },
        "topic_freshness": {
            "semantic_cluster": None,
            "similar_recent_posts": None,
            "recent_cluster_frequency": None,
            "days_since_last_similar_post": None,
            "freshness_score": None,
            "fatigue_risk": None,
        },
        "originality_risk": {
            "caption_content_mismatch": None,
            "hashtag_stuffing_risk": None,
            "duplicate_cluster_risk": None,
            "minor_edit_repost_risk": None,
            "low_value_reaction_risk": None,
            "fake_engagement_pattern_risk": None,
        },
    }


def build_psychology_signals() -> dict:
    """Create an empty psychology-signals scaffold for a post."""
    return {
        "hook_payoff": {
            "hook_strength": None,
            "payoff_strength": None,
            "hook_payoff_gap": None,
        },
        "share_motive_split": {
            "dm_forwardability": None,
            "public_repostability": None,
            "identity_signal_strength": None,
            "utility_share_strength": None,
        },
        "retellability": None,
    }


def build_review_state() -> dict:
    """Create an empty review-state scaffold for a post."""
    return {
        "last_reviewed_at": None,
        "actual_checkpoint_hours": None,
        "deviation_summary": None,
        "calibration_notes": [],
        "validated_signals": {
            "discovery_surface_notes": None,
            "topic_graph_notes": None,
            "topic_freshness_notes": None,
            "originality_risk_notes": None,
            "hook_payoff_gap_notes": None,
            "share_motive_split_notes": None,
            "retellability_notes": None,
        },
    }


def build_tracker(threads: list, token: str, account_handle: str = "") -> dict:
    """Build the tracker JSON from fetched threads."""
    posts = []
    total = len(threads)

    for i, thread in enumerate(threads, 1):
        thread_id = thread["id"]
        text = thread.get("text", "")

        print(f"  Processing post {i}/{total}: {text[:40]}...")

        # Fetch metrics
        time.sleep(RATE_LIMIT_DELAY)
        metrics = fetch_thread_insights(thread_id, token)

        # Fetch replies
        time.sleep(RATE_LIMIT_DELAY)
        replies = fetch_thread_replies(thread_id, token)

        post = {
            "id": thread_id,
            "text": text,
            "created_at": thread.get("timestamp", ""),
            "permalink": thread.get("permalink", ""),
            "media_type": thread.get("media_type", "TEXT"),
            "is_reply_post": False,
            "content_type": classify_content_type(text),
            "topics": [],  # Will be populated during style guide generation
            "hook_type": None,
            "ending_type": None,
            "emotional_arc": None,
            "word_count": count_words(text),
            "paragraph_count": count_paragraphs(text),
            "posting_time_slot": build_posting_time_slot(thread.get("timestamp", "")),
            "algorithm_signals": build_algorithm_signals(),
            "psychology_signals": build_psychology_signals(),
            "metrics": {
                "views": metrics.get("views", 0),
                "likes": metrics.get("likes", 0),
                "replies": metrics.get("replies", 0),
                "reposts": metrics.get("reposts", 0),
                "quotes": metrics.get("quotes", 0),
                "shares": 0,  # Not available via API
            },
            "performance_windows": {
                "24h": None,
                "72h": None,
                "7d": None,
            },
            "snapshots": [
                build_metric_snapshot(
                    {
                        "views": metrics.get("views", 0),
                        "likes": metrics.get("likes", 0),
                        "replies": metrics.get("replies", 0),
                        "reposts": metrics.get("reposts", 0),
                        "quotes": metrics.get("quotes", 0),
                        "shares": 0,
                    },
                    thread.get("timestamp", ""),
                )
            ],
            "prediction_snapshot": None,
            "review_state": build_review_state(),
            "comments": replies,
            "source": {
                "import_path": "api",
                "data_completeness": "full",
            },
        }
        posts.append(post)

    # Sort by date, newest first
    posts.sort(key=lambda p: p.get("created_at", ""), reverse=True)

    return {
        "account": {
            "handle": account_handle,
            "source": "api",
            "timezone": "UTC",
        },
        "posts": posts,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


def exchange_long_lived_token(short_token: str, app_secret: str) -> str:
    """Exchange a short-lived token for a long-lived token (60 days)."""
    resp = requests.get(
        f"{API_BASE}/access_token",
        params={
            "grant_type": "th_exchange_token",
            "client_secret": app_secret,
            "access_token": short_token,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    print(f"  Long-lived token obtained. Expires in {data.get('expires_in', 'unknown')} seconds.")
    return data["access_token"]


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Threads historical posts via Meta Threads API"
    )
    parser.add_argument(
        "--token", required=True, help="Threads API access token"
    )
    parser.add_argument(
        "--app-secret",
        help="App secret for long-lived token exchange (optional)",
    )
    parser.add_argument(
        "--output",
        default="threads_daily_tracker.json",
        help="Output file path (default: threads_daily_tracker.json)",
    )
    args = parser.parse_args()

    token = args.token

    # Exchange for long-lived token if app secret provided
    if args.app_secret:
        print("[1/4] Exchanging for long-lived token...")
        token = exchange_long_lived_token(token, args.app_secret)
    else:
        print("[1/4] Using provided token (skip long-lived exchange)")

    # Get user profile
    print("[2/4] Fetching user profile...")
    profile = get_user_profile(token)
    user_id = profile["id"]
    print(f"  User ID: {user_id}")
    if profile["username"]:
        print(f"  Username: @{profile['username']}")

    # Fetch all threads
    print("[3/4] Fetching all historical posts...")
    threads = fetch_all_threads(user_id, token)
    print(f"  Found {len(threads)} original posts")

    if not threads:
        print("No posts found. Check your token permissions.")
        sys.exit(1)

    # Build tracker with metrics and replies
    print("[4/4] Fetching metrics and replies for each post...")
    handle = f"@{profile['username']}" if profile["username"] else ""
    tracker = build_tracker(threads, token, account_handle=handle)

    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Saved {len(tracker['posts'])} posts to {args.output}")
    print(f"Next step: Run /setup in Claude Code to generate your style guide and concept library.")


if __name__ == "__main__":
    main()
