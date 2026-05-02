"""Tests for scripts/tracker_archive.py.

Covers:
- Splits posts by keep_days cutoff
- Groups archived posts by year-month
- Idempotent: second run on already-archived data is a no-op
- Backups created before mutation, max 5 retained
- Dry-run path makes no file changes
- Top performers recomputed across recent + archives
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import tracker_archive  # noqa: E402
import tracker_query  # noqa: E402


def fixture_tracker_with_old_and_recent() -> dict:
    """Build a tracker where some posts are >60d old (frozen now=2026-05-02)."""
    return {
        "account": {"handle": "@test", "source": "fixture", "timezone": "UTC"},
        "last_updated": "2026-05-02T10:00:00Z",
        "posts": [
            # Recent (within 60d)
            {"id": "recent1", "text": "recent 1", "created_at": "2026-04-15T00:00:00Z",
             "metrics": {"likes": 50, "replies": 5, "reposts": 1, "shares": 1}},
            {"id": "recent2", "text": "recent 2", "created_at": "2026-05-01T00:00:00Z",
             "metrics": {"likes": 100, "replies": 10, "reposts": 5, "shares": 3}},
            # Old (>60d)
            {"id": "old1", "text": "old jan", "created_at": "2026-01-15T00:00:00Z",
             "metrics": {"likes": 200, "replies": 30, "reposts": 10, "shares": 5}},
            {"id": "old2", "text": "old feb", "created_at": "2026-02-10T00:00:00Z",
             "metrics": {"likes": 80, "replies": 8, "reposts": 2, "shares": 1}},
            {"id": "old3", "text": "old jan 2", "created_at": "2026-01-25T00:00:00Z",
             "metrics": {"likes": 60, "replies": 4, "reposts": 1, "shares": 0}},
        ],
    }


class FreezeTime:
    def __init__(self, frozen: datetime) -> None:
        self.frozen = frozen

    def __enter__(self) -> "FreezeTime":
        frozen = self.frozen

        class _FrozenDT(datetime):
            @classmethod
            def now(cls, tz=None):  # type: ignore[override]
                if tz is None:
                    return frozen.replace(tzinfo=None)
                return frozen.astimezone(tz)

        self._orig_q = tracker_query.datetime  # type: ignore[attr-defined]
        self._orig_a = tracker_archive.datetime  # type: ignore[attr-defined]
        tracker_query.datetime = _FrozenDT  # type: ignore[attr-defined]
        tracker_archive.datetime = _FrozenDT  # type: ignore[attr-defined]
        return self

    def __exit__(self, *exc) -> None:
        tracker_query.datetime = self._orig_q  # type: ignore[attr-defined]
        tracker_archive.datetime = self._orig_a  # type: ignore[attr-defined]


FROZEN_NOW = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)


class TempEnv:
    """Context that creates a temp dir, writes a tracker fixture, returns paths."""

    def __init__(self, tracker_data: dict | None = None) -> None:
        self.tracker_data = tracker_data or fixture_tracker_with_old_and_recent()

    def __enter__(self) -> "TempEnv":
        self.tmp = Path(tempfile.mkdtemp(prefix="trackerarchtest_"))
        self.tracker_path = self.tmp / "threads_daily_tracker.json"
        self.archive_dir = self.tmp / "archive"
        self.tracker_path.write_text(json.dumps(self.tracker_data, ensure_ascii=False), encoding="utf-8")
        return self

    def __exit__(self, *exc) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


def run_archive(env: TempEnv, *, dry_run: bool = False, keep_days: int = 60, top_n: int = 50) -> dict:
    return tracker_archive.archive(
        env.tracker_path, env.archive_dir, keep_days, top_n, dry_run
    )


class TestSplit(unittest.TestCase):
    def test_split_recent_old_uses_keep_days(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            result = run_archive(env, dry_run=True, keep_days=60)
        self.assertEqual(result["split"]["recent_keep"], 2)  # recent1, recent2
        self.assertEqual(result["split"]["old_to_archive"], 3)  # old1, old2, old3

    def test_keep_days_120_keeps_more(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            result = run_archive(env, dry_run=True, keep_days=120)
        # 120d from 2026-05-02 cutoff is ~2026-01-02, all posts within window
        self.assertEqual(result["split"]["old_to_archive"], 0)


class TestArchiveWrite(unittest.TestCase):
    def test_writes_per_month_archive_files(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            result = run_archive(env, dry_run=False)
            jan = env.archive_dir / "2026-01.json"
            feb = env.archive_dir / "2026-02.json"
            self.assertTrue(jan.exists(), "jan archive missing")
            self.assertTrue(feb.exists(), "feb archive missing")
            jan_data = json.loads(jan.read_text(encoding="utf-8"))
            feb_data = json.loads(feb.read_text(encoding="utf-8"))
            jan_ids = {p["id"] for p in jan_data["posts"]}
            feb_ids = {p["id"] for p in feb_data["posts"]}
            self.assertEqual(jan_ids, {"old1", "old3"})
            self.assertEqual(feb_ids, {"old2"})
            self.assertEqual(result["action"], "wrote")
            self.assertEqual(result["archive_added_total"], 3)

    def test_main_tracker_keeps_recent_only(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            run_archive(env, dry_run=False)
            new_tracker = json.loads(env.tracker_path.read_text(encoding="utf-8"))
            ids = {p["id"] for p in new_tracker["posts"]}
            self.assertEqual(ids, {"recent1", "recent2"})
            self.assertIn("top_performers_alltime", new_tracker)
            self.assertEqual(new_tracker["archived_count"], 3)
            self.assertIn("last_archive_run", new_tracker)

    def test_top_performers_includes_archived_posts(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            run_archive(env, dry_run=False, top_n=10)
            new_tracker = json.loads(env.tracker_path.read_text(encoding="utf-8"))
            top_ids = [t["id"] for t in new_tracker["top_performers_alltime"]]
            # old1 has highest engagement (200 + 90 + 20 + 10 = 320)
            self.assertEqual(top_ids[0], "old1")
            # All 5 posts should appear in top-10 (top_n=10 > total)
            self.assertEqual(set(top_ids), {"recent1", "recent2", "old1", "old2", "old3"})


class TestBackup(unittest.TestCase):
    def test_backup_created_before_mutation(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            run_archive(env, dry_run=False)
            baks = list(env.tmp.glob("threads_daily_tracker.json.bak-*"))
            self.assertEqual(len(baks), 1)

    def test_max_5_backups_retained(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            # Pre-seed 7 fake backups
            for i in range(7):
                fake = env.tmp / f"threads_daily_tracker.json.bak-2026010{i}T120000Z"
                fake.write_text("{}", encoding="utf-8")
            run_archive(env, dry_run=False)
            baks = list(env.tmp.glob("threads_daily_tracker.json.bak-*"))
            # Pre-seeded 7 + 1 new = 8 → rotate keeps 5
            self.assertEqual(len(baks), 5, f"expected 5 baks, got {[b.name for b in baks]}")

    def test_dry_run_creates_no_backup(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            run_archive(env, dry_run=True)
            baks = list(env.tmp.glob("threads_daily_tracker.json.bak-*"))
            self.assertEqual(len(baks), 0)


class TestIdempotency(unittest.TestCase):
    def test_second_run_is_no_op(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            run_archive(env, dry_run=False)
            first_tracker = env.tracker_path.read_text(encoding="utf-8")
            first_baks = sorted(env.tmp.glob("threads_daily_tracker.json.bak-*"))

            second = run_archive(env, dry_run=False)
            second_tracker = env.tracker_path.read_text(encoding="utf-8")
            second_baks = sorted(env.tmp.glob("threads_daily_tracker.json.bak-*"))

            self.assertEqual(second["action"], "no-op")
            self.assertEqual(first_tracker, second_tracker)
            # No new backup added on no-op
            self.assertEqual(len(first_baks), len(second_baks))

    def test_re_archiving_existing_keys_dedupes(self) -> None:
        # Simulate: existing archive already has old1; run archive against tracker
        # that still contains old1 (e.g., post resurrected after a refresh bug).
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            env.archive_dir.mkdir(exist_ok=True)
            preseed = {
                "month": "2026-01",
                "posts": [
                    {"id": "old1", "text": "old jan (preseeded)", "created_at": "2026-01-15T00:00:00Z",
                     "metrics": {"likes": 200, "replies": 30, "reposts": 10, "shares": 5}}
                ],
            }
            (env.archive_dir / "2026-01.json").write_text(
                json.dumps(preseed, ensure_ascii=False), encoding="utf-8"
            )
            run_archive(env, dry_run=False)
            jan = json.loads((env.archive_dir / "2026-01.json").read_text(encoding="utf-8"))
            ids = [p["id"] for p in jan["posts"]]
            # old1 should appear exactly once (preseeded) + old3 added
            self.assertEqual(sorted(ids), ["old1", "old3"])


class TestDryRun(unittest.TestCase):
    def test_dry_run_writes_nothing(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            original = env.tracker_path.read_text(encoding="utf-8")
            result = run_archive(env, dry_run=True)
            after = env.tracker_path.read_text(encoding="utf-8")
            self.assertEqual(original, after)
            self.assertFalse(env.archive_dir.exists())
            self.assertEqual(result["action"], "dry-run")

    def test_dry_run_still_reports_plan(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            result = run_archive(env, dry_run=True)
            self.assertEqual(result["split"]["old_to_archive"], 3)
            self.assertEqual(len(result["archive_actions"]), 2)  # jan + feb groups


class TestCLIIntegration(unittest.TestCase):
    def test_cli_returns_json_summary(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            buf = io.StringIO()
            with redirect_stdout(buf):
                tracker_archive.main([
                    "--tracker", str(env.tracker_path),
                    "--archive-dir", str(env.archive_dir),
                    "--dry-run",
                ])
            data = json.loads(buf.getvalue())
            self.assertEqual(data["dry_run"], True)
            self.assertIn("split", data)


if __name__ == "__main__":
    unittest.main()
