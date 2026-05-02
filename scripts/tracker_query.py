#!/usr/bin/env python3
"""Query CLI for threads_daily_tracker.json.

Lets skills (analyze / predict / review / topics / draft) request narrow
slices of tracker data instead of reading the full 100KB+ file. Output
is JSON to stdout, ~1-10KB per query.

Subcommands:
  recent       Recent posts within N days
  top          Top posts by metric, optionally filtered by topic
  comparable   Posts matching content-type / hook-type / topic
  hook-stats   Aggregate hook type distribution + engagement
  ai-tone-stats  Frequency of AI-tone signals in user's own posts
  post         Single post lookup by id or date
  meta         Tracker metadata (post count, date range, schema version)

Examples:
  python tracker_query.py recent --days 30
  python tracker_query.py top --metric engagement --topic AI --limit 10
  python tracker_query.py comparable --content-type list --hook-type question --limit 5
  python tracker_query.py hook-stats --days 60
  python tracker_query.py post --id 17912345
  python tracker_query.py meta
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_TRACKER = Path("threads_daily_tracker.json")


def _ensure_utf8_stdout() -> None:
    """Force utf-8 stdout so Chinese content prints cleanly on Windows cp950."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


def load_tracker(path: Path) -> dict[str, Any]:
    if not path.exists():
        sys.stderr.write(f"tracker not found at {path}\n")
        sys.exit(2)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def parse_iso(value: str) -> datetime:
    """Parse ISO-8601 with or without trailing Z, return tz-aware UTC."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def post_created_at(post: dict[str, Any]) -> datetime | None:
    raw = post.get("created_at")
    if not raw:
        return None
    try:
        return parse_iso(raw)
    except Exception:
        return None


def engagement_score(post: dict[str, Any]) -> int:
    """Combined engagement metric: likes + replies*3 + reposts*2 + shares*2.

    Replies are weighted highest because they signal deepest engagement.
    Falls back to 0 for missing fields rather than raising.
    """
    metrics = post.get("metrics") or {}
    likes = int(metrics.get("likes") or 0)
    replies = int(metrics.get("replies") or 0)
    reposts = int(metrics.get("reposts") or 0)
    shares = int(metrics.get("shares") or 0)
    return likes + replies * 3 + reposts * 2 + shares * 2


def metric_value(post: dict[str, Any], metric: str) -> int:
    metrics = post.get("metrics") or {}
    if metric == "engagement":
        return engagement_score(post)
    return int(metrics.get(metric) or 0)


def filter_window(posts: list[dict[str, Any]], days: int) -> list[dict[str, Any]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    for p in posts:
        dt = post_created_at(p)
        if dt is None:
            continue
        if dt >= cutoff:
            out.append(p)
    return out


def slim_post(
    post: dict[str, Any], *, include_comments: bool = False, full_text: bool = True
) -> dict[str, Any]:
    """Return a smaller dict suitable for query output."""
    keep = {
        "id": post.get("id"),
        "created_at": post.get("created_at"),
        "permalink": post.get("permalink"),
        "content_type": post.get("content_type"),
        "topics": post.get("topics"),
        "hook_type": post.get("hook_type"),
        "ending_type": post.get("ending_type"),
        "emotional_arc": post.get("emotional_arc"),
        "word_count": post.get("word_count"),
        "paragraph_count": post.get("paragraph_count"),
        "posting_time_slot": post.get("posting_time_slot"),
        "metrics": post.get("metrics"),
        "engagement_score": engagement_score(post),
    }
    if full_text:
        keep["text"] = post.get("text")
    else:
        text = post.get("text") or ""
        keep["text_preview"] = text[:200]
    if include_comments:
        keep["comments"] = post.get("comments") or []
    return {k: v for k, v in keep.items() if v is not None}


# ---------- Subcommand handlers ---------- #


def cmd_recent(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = filter_window(tracker.get("posts", []), args.days)
    posts.sort(key=lambda p: post_created_at(p) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return {
        "window_days": args.days,
        "count": len(posts),
        "posts": [slim_post(p, include_comments=args.include_comments) for p in posts],
    }


def cmd_top(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = list(tracker.get("posts", []))
    if args.days:
        posts = filter_window(posts, args.days)
    if args.topic:
        topic = args.topic.lower()
        posts = [p for p in posts if any(topic in (t or "").lower() for t in (p.get("topics") or []))]
    posts.sort(key=lambda p: metric_value(p, args.metric), reverse=True)
    top = posts[: args.limit]
    return {
        "metric": args.metric,
        "topic_filter": args.topic,
        "window_days": args.days,
        "count": len(top),
        "posts": [slim_post(p, full_text=False) for p in top],
    }


def cmd_comparable(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = list(tracker.get("posts", []))
    if args.content_type:
        posts = [p for p in posts if (p.get("content_type") or "").lower() == args.content_type.lower()]
    if args.hook_type:
        posts = [p for p in posts if (p.get("hook_type") or "").lower() == args.hook_type.lower()]
    if args.topic:
        topic = args.topic.lower()
        posts = [p for p in posts if any(topic in (t or "").lower() for t in (p.get("topics") or []))]
    posts.sort(key=engagement_score, reverse=True)
    top = posts[: args.limit]
    return {
        "filters": {
            "content_type": args.content_type,
            "hook_type": args.hook_type,
            "topic": args.topic,
        },
        "count": len(top),
        "posts": [slim_post(p, full_text=False) for p in top],
    }


def cmd_hook_stats(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = filter_window(tracker.get("posts", []), args.days) if args.days else list(tracker.get("posts", []))
    buckets: dict[str, dict[str, Any]] = {}
    for p in posts:
        key = p.get("hook_type") or "unknown"
        b = buckets.setdefault(key, {"count": 0, "engagement_total": 0, "post_ids": []})
        b["count"] += 1
        b["engagement_total"] += engagement_score(p)
        b["post_ids"].append(p.get("id"))
    for k, v in buckets.items():
        v["engagement_avg"] = round(v["engagement_total"] / v["count"], 1) if v["count"] else 0
        # Keep post_ids for reference but cap at 5 to keep output small
        v["post_ids"] = v["post_ids"][:5]
    return {
        "window_days": args.days,
        "total_posts": len(posts),
        "hook_types": dict(sorted(buckets.items(), key=lambda kv: kv[1]["engagement_avg"], reverse=True)),
    }


def cmd_ai_tone_stats(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = filter_window(tracker.get("posts", []), args.days) if args.days else list(tracker.get("posts", []))
    signal_counts: dict[str, int] = {}
    for p in posts:
        sigs = p.get("psychology_signals") or {}
        ai_flags = sigs.get("ai_tone_flags") if isinstance(sigs, dict) else None
        if isinstance(ai_flags, list):
            for s in ai_flags:
                if isinstance(s, str):
                    signal_counts[s] = signal_counts.get(s, 0) + 1
        # also check algorithm_signals for risk flags
        algo = p.get("algorithm_signals") or {}
        if isinstance(algo, dict):
            for s in algo.get("risk_flags", []) or []:
                if isinstance(s, str):
                    signal_counts[f"risk:{s}"] = signal_counts.get(f"risk:{s}", 0) + 1
    return {
        "window_days": args.days,
        "total_posts": len(posts),
        "signal_frequencies": dict(sorted(signal_counts.items(), key=lambda kv: kv[1], reverse=True)),
    }


def cmd_post(args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = tracker.get("posts", [])
    matches: list[dict[str, Any]] = []
    if args.id:
        matches = [p for p in posts if str(p.get("id")) == str(args.id)]
    elif args.date:
        target = args.date  # match prefix yyyy-mm-dd
        matches = [p for p in posts if (p.get("created_at") or "").startswith(target)]
    return {
        "lookup": {"id": args.id, "date": args.date},
        "count": len(matches),
        "posts": [slim_post(p, include_comments=True) for p in matches],
    }


def cmd_meta(_args: argparse.Namespace, tracker: dict[str, Any]) -> dict[str, Any]:
    posts = tracker.get("posts", [])
    dates = sorted([p.get("created_at") for p in posts if p.get("created_at")])
    return {
        "account": tracker.get("account"),
        "last_updated": tracker.get("last_updated"),
        "post_count": len(posts),
        "date_range": {
            "earliest": dates[0] if dates else None,
            "latest": dates[-1] if dates else None,
        },
        "top_level_keys": list(tracker.keys()),
    }


# ---------- CLI assembly ---------- #


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tracker_query", description=__doc__)
    p.add_argument(
        "--tracker",
        type=Path,
        default=DEFAULT_TRACKER,
        help="Path to threads_daily_tracker.json (default: ./threads_daily_tracker.json)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s_recent = sub.add_parser("recent", help="Recent posts within N days")
    s_recent.add_argument("--days", type=int, default=30)
    s_recent.add_argument("--include-comments", action="store_true")
    s_recent.set_defaults(func=cmd_recent)

    s_top = sub.add_parser("top", help="Top posts by metric")
    s_top.add_argument("--metric", default="engagement",
                       help="engagement (default), likes, replies, reposts, shares")
    s_top.add_argument("--topic", default=None)
    s_top.add_argument("--days", type=int, default=None,
                       help="optional time window")
    s_top.add_argument("--limit", type=int, default=10)
    s_top.set_defaults(func=cmd_top)

    s_cmp = sub.add_parser("comparable", help="Posts matching content-type / hook-type / topic")
    s_cmp.add_argument("--content-type", default=None)
    s_cmp.add_argument("--hook-type", default=None)
    s_cmp.add_argument("--topic", default=None)
    s_cmp.add_argument("--limit", type=int, default=10)
    s_cmp.set_defaults(func=cmd_comparable)

    s_hook = sub.add_parser("hook-stats", help="Hook type distribution + engagement")
    s_hook.add_argument("--days", type=int, default=None)
    s_hook.set_defaults(func=cmd_hook_stats)

    s_ai = sub.add_parser("ai-tone-stats", help="AI-tone signal frequencies")
    s_ai.add_argument("--days", type=int, default=None)
    s_ai.set_defaults(func=cmd_ai_tone_stats)

    s_post = sub.add_parser("post", help="Single post lookup")
    s_post.add_argument("--id", default=None)
    s_post.add_argument("--date", default=None, help="match by yyyy-mm-dd prefix")
    s_post.set_defaults(func=cmd_post)

    s_meta = sub.add_parser("meta", help="Tracker metadata")
    s_meta.set_defaults(func=cmd_meta)

    return p


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    tracker = load_tracker(args.tracker)
    result = args.func(args, tracker)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
