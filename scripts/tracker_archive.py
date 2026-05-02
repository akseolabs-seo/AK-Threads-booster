#!/usr/bin/env python3
"""Archive old posts out of threads_daily_tracker.json into per-month files.

Bounds tracker size by moving posts older than --keep-days (default 60)
into archive/<YYYY>-<MM>.json files. Maintains a frozen
top_performers_alltime[] list in the main tracker so analysis skills
can still see historical bests without reading archives.

Idempotent: re-running with no new posts past the cutoff makes no
changes (no .bak file, no archive write). Safe to invoke from /refresh.

Backup convention: before any mutation, copies the current tracker to
tracker.json.bak-<ISO>. Keeps the 5 most recent .bak files; older are
deleted.

Examples:
  python tracker_archive.py
  python tracker_archive.py --keep-days 90 --top-n 30
  python tracker_archive.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Reuse helpers from tracker_query
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from tracker_query import (  # noqa: E402
    engagement_score,
    parse_iso,
    post_created_at,
    _ensure_utf8_stdout,
)


DEFAULT_TRACKER = Path("threads_daily_tracker.json")
DEFAULT_ARCHIVE_DIR = Path("archive")
MAX_BACKUPS = 5


def iso_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def archive_key(post: dict[str, Any]) -> str:
    """Return YYYY-MM from a post's created_at, or 'undated' if missing."""
    dt = post_created_at(post)
    if dt is None:
        return "undated"
    return dt.strftime("%Y-%m")


def split_recent_old(
    posts: list[dict[str, Any]], keep_days: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    recent: list[dict[str, Any]] = []
    old: list[dict[str, Any]] = []
    for p in posts:
        dt = post_created_at(p)
        if dt is None or dt >= cutoff:
            recent.append(p)
        else:
            old.append(p)
    return recent, old


def merge_into_archive_file(
    archive_dir: Path, key: str, new_posts: list[dict[str, Any]], dry_run: bool
) -> tuple[int, int]:
    """Merge new posts into archive/<key>.json. Dedupe by id.

    Returns (added, total_after).
    """
    target = archive_dir / f"{key}.json"
    existing: list[dict[str, Any]] = []
    if target.exists():
        try:
            with target.open(encoding="utf-8") as f:
                existing = json.load(f).get("posts", [])
        except Exception as e:
            sys.stderr.write(f"warning: failed to read {target}: {e}\n")
            existing = []
    existing_ids = {str(p.get("id")) for p in existing if p.get("id") is not None}
    added = 0
    for p in new_posts:
        pid = str(p.get("id"))
        if pid not in existing_ids:
            existing.append(p)
            existing_ids.add(pid)
            added += 1
    if dry_run:
        return added, len(existing)
    if added > 0:
        archive_dir.mkdir(parents=True, exist_ok=True)
        # sort by created_at desc within archive
        existing.sort(key=lambda p: post_created_at(p) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        target.write_text(
            json.dumps({"month": key, "posts": existing}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return added, len(existing)


def collect_all_posts_for_top(
    tracker_posts: list[dict[str, Any]], archive_dir: Path
) -> list[dict[str, Any]]:
    """Combine recent (in-tracker) posts with archived posts to compute top_performers."""
    pool = list(tracker_posts)
    seen_ids = {str(p.get("id")) for p in pool if p.get("id") is not None}
    if archive_dir.exists():
        for archive_file in sorted(archive_dir.glob("*.json")):
            try:
                with archive_file.open(encoding="utf-8") as f:
                    arch_posts = json.load(f).get("posts", [])
                for p in arch_posts:
                    pid = str(p.get("id"))
                    if pid not in seen_ids:
                        pool.append(p)
                        seen_ids.add(pid)
            except Exception as e:
                sys.stderr.write(f"warning: skipping {archive_file}: {e}\n")
    return pool


def compute_top_performers(
    posts: list[dict[str, Any]], top_n: int
) -> list[dict[str, Any]]:
    """Return slimmed top-N posts by engagement_score across the pool."""
    ranked = sorted(posts, key=engagement_score, reverse=True)[:top_n]
    out = []
    for p in ranked:
        out.append({
            "id": p.get("id"),
            "created_at": p.get("created_at"),
            "permalink": p.get("permalink"),
            "content_type": p.get("content_type"),
            "topics": p.get("topics"),
            "hook_type": p.get("hook_type"),
            "engagement_score": engagement_score(p),
            "metrics": p.get("metrics"),
            "text_preview": (p.get("text") or "")[:200],
        })
    return out


def rotate_backups(tracker_path: Path) -> None:
    pattern = f"{tracker_path.name}.bak-*"
    backups = sorted(tracker_path.parent.glob(pattern), reverse=True)
    for old in backups[MAX_BACKUPS:]:
        try:
            old.unlink()
        except Exception as e:
            sys.stderr.write(f"warning: failed to delete old backup {old}: {e}\n")


def make_backup(tracker_path: Path) -> Path:
    bak = tracker_path.with_name(f"{tracker_path.name}.bak-{iso_compact()}")
    shutil.copy2(tracker_path, bak)
    rotate_backups(tracker_path)
    return bak


def archive(
    tracker_path: Path,
    archive_dir: Path,
    keep_days: int,
    top_n: int,
    dry_run: bool,
) -> dict[str, Any]:
    if not tracker_path.exists():
        sys.stderr.write(f"tracker not found at {tracker_path}\n")
        sys.exit(2)
    with tracker_path.open(encoding="utf-8") as f:
        tracker = json.load(f)

    posts = tracker.get("posts", [])
    recent, old = split_recent_old(posts, keep_days)

    # Group old by archive key (year-month)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for p in old:
        grouped.setdefault(archive_key(p), []).append(p)

    archive_actions: list[dict[str, Any]] = []
    total_added = 0
    for key, plist in sorted(grouped.items()):
        added, total_after = merge_into_archive_file(archive_dir, key, plist, dry_run)
        archive_actions.append(
            {"key": key, "added": added, "total_after": total_after, "incoming": len(plist)}
        )
        total_added += added

    # Compute new top performers from recent + archives
    pool = collect_all_posts_for_top(recent, archive_dir if not dry_run or archive_dir.exists() else Path("/nonexistent"))
    new_top = compute_top_performers(pool, top_n)

    old_top = tracker.get("top_performers_alltime") or []
    top_changed = [{"id": t.get("id"), "engagement_score": t.get("engagement_score")} for t in new_top] != \
                  [{"id": t.get("id"), "engagement_score": t.get("engagement_score")} for t in old_top]

    needs_tracker_write = (len(old) > 0) or top_changed or "top_performers_alltime" not in tracker

    summary = {
        "dry_run": dry_run,
        "tracker_path": str(tracker_path),
        "archive_dir": str(archive_dir),
        "keep_days": keep_days,
        "top_n": top_n,
        "before": {
            "post_count": len(posts),
            "had_top_performers": "top_performers_alltime" in tracker,
        },
        "split": {
            "recent_keep": len(recent),
            "old_to_archive": len(old),
        },
        "archive_actions": archive_actions,
        "archive_added_total": total_added,
        "top_performers_changed": top_changed,
        "needs_tracker_write": needs_tracker_write,
    }

    if dry_run or not needs_tracker_write:
        summary["action"] = "dry-run" if dry_run else "no-op"
        return summary

    backup = make_backup(tracker_path)
    new_tracker = dict(tracker)
    new_tracker["posts"] = recent
    new_tracker["top_performers_alltime"] = new_top
    new_tracker["last_archive_run"] = datetime.now(timezone.utc).isoformat()
    new_tracker.setdefault("archived_count", 0)
    new_tracker["archived_count"] = int(new_tracker.get("archived_count") or 0) + total_added

    tracker_path.write_text(
        json.dumps(new_tracker, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    summary["action"] = "wrote"
    summary["backup"] = str(backup)
    summary["after"] = {
        "post_count": len(recent),
        "top_performers_count": len(new_top),
    }
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tracker_archive", description=__doc__)
    p.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    p.add_argument("--archive-dir", type=Path, default=DEFAULT_ARCHIVE_DIR)
    p.add_argument("--keep-days", type=int, default=60)
    p.add_argument("--top-n", type=int, default=50)
    p.add_argument("--dry-run", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)
    summary = archive(
        args.tracker,
        args.archive_dir,
        args.keep_days,
        args.top_n,
        args.dry_run,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
