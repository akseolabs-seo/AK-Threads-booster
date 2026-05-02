"""Tests for scripts/build_tracker_summary.py.

Covers:
- All sections present in output
- Top tables include archive-resident posts
- AI-tone section detects flagged signals
- Empty-data fallback messages render
- Output file is written and size is reported
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

import build_tracker_summary as bts  # noqa: E402
import tracker_query  # noqa: E402


def fixture_with_archive() -> dict:
    return {
        "account": {"handle": "@summarytest", "source": "fixture", "timezone": "UTC"},
        "last_updated": "2026-05-02T10:00:00Z",
        "posts": [
            {"id": "r1", "text": "recent A", "created_at": "2026-04-25T00:00:00Z",
             "content_type": "list", "hook_type": "question",
             "topics": ["AI", "tools"], "word_count": 150, "posting_time_slot": "afternoon",
             "metrics": {"likes": 80, "replies": 8, "reposts": 2, "shares": 1},
             "psychology_signals": {"ai_tone_flags": ["structural-perfection"]}},
            {"id": "r2", "text": "recent B", "created_at": "2026-05-01T00:00:00Z",
             "content_type": "story", "hook_type": "shock",
             "topics": ["productivity"], "word_count": 220, "posting_time_slot": "evening",
             "metrics": {"likes": 50, "replies": 5, "reposts": 1, "shares": 0},
             "psychology_signals": {"ai_tone_flags": []}},
        ],
    }


def archive_data() -> dict:
    return {
        "month": "2026-01",
        "posts": [
            {"id": "a1", "text": "archived best post", "created_at": "2026-01-15T00:00:00Z",
             "content_type": "list", "hook_type": "question",
             "topics": ["AI"], "word_count": 300, "posting_time_slot": "morning",
             "metrics": {"likes": 500, "replies": 80, "reposts": 30, "shares": 20}}
        ]
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
        self._orig_b = bts.datetime  # type: ignore[attr-defined]
        tracker_query.datetime = _FrozenDT  # type: ignore[attr-defined]
        bts.datetime = _FrozenDT  # type: ignore[attr-defined]
        return self

    def __exit__(self, *exc) -> None:
        tracker_query.datetime = self._orig_q  # type: ignore[attr-defined]
        bts.datetime = self._orig_b  # type: ignore[attr-defined]


FROZEN_NOW = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)


class TempEnv:
    def __enter__(self) -> "TempEnv":
        self.tmp = Path(tempfile.mkdtemp(prefix="bts_test_"))
        self.tracker_path = self.tmp / "threads_daily_tracker.json"
        self.archive_dir = self.tmp / "archive"
        self.output_path = self.tmp / "tracker_summary.md"
        self.tracker_path.write_text(
            json.dumps(fixture_with_archive(), ensure_ascii=False), encoding="utf-8"
        )
        return self

    def __exit__(self, *exc) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestSections(unittest.TestCase):
    def test_summary_includes_all_sections(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        self.assertIn("## Meta", md)
        self.assertIn("## Top 10 — alltime", md)
        self.assertIn("## Top 10 — last 30 days", md)
        self.assertIn("## Hook Type Distribution", md)
        self.assertIn("## Topic Cluster Distribution", md)
        self.assertIn("## AI-Tone Signal Frequencies", md)
        self.assertIn("## Posting Cadence", md)
        self.assertIn("## Word Count Distribution", md)
        self.assertIn("## Recent Topic Freshness", md)

    def test_archive_posts_count_in_alltime(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            env.archive_dir.mkdir()
            (env.archive_dir / "2026-01.json").write_text(
                json.dumps(archive_data(), ensure_ascii=False), encoding="utf-8"
            )
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        # a1 is archived but should appear in alltime top
        self.assertIn("`a1`", md)
        self.assertIn("Total posts (tracker + archives): **3**", md)
        self.assertIn("Tracker post count: **2**", md)

    def test_archive_post_outranks_recent_in_alltime(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            env.archive_dir.mkdir()
            (env.archive_dir / "2026-01.json").write_text(
                json.dumps(archive_data(), ensure_ascii=False), encoding="utf-8"
            )
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        alltime_section = md.split("## Top 10 — alltime")[1].split("## Top 10 — last 30 days")[0]
        # a1 has highest engagement (500 + 240 + 60 + 40 = 840)
        a1_pos = alltime_section.find("`a1`")
        r1_pos = alltime_section.find("`r1`")
        self.assertNotEqual(a1_pos, -1)
        self.assertLess(a1_pos, r1_pos, "a1 should rank above r1 in alltime top")

    def test_recent_window_excludes_archived(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            env.archive_dir.mkdir()
            (env.archive_dir / "2026-01.json").write_text(
                json.dumps(archive_data(), ensure_ascii=False), encoding="utf-8"
            )
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        recent_section = md.split("## Top 10 — last 30 days")[1].split("##")[0]
        # a1 is from January, outside 30d from May 2 → should NOT appear in recent top
        self.assertNotIn("`a1`", recent_section)


class TestAITone(unittest.TestCase):
    def test_ai_tone_signal_counted(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        self.assertIn("structural-perfection", md)
        # 1 of 2 posts flagged → 50.0%
        self.assertIn("Posts flagged: **1** of 2", md)


class TestEmptyData(unittest.TestCase):
    def test_empty_tracker_renders_fallbacks(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            empty = {"account": {"handle": "@empty"}, "posts": []}
            env.tracker_path.write_text(json.dumps(empty), encoding="utf-8")
            md = bts.build_summary(env.tracker_path, env.archive_dir)
        self.assertIn("Total posts", md)  # meta still renders
        self.assertIn("_No posts in this window._", md)


class TestCLIOutput(unittest.TestCase):
    def test_main_writes_output_file(self) -> None:
        with FreezeTime(FROZEN_NOW), TempEnv() as env:
            buf = io.StringIO()
            with redirect_stdout(buf):
                bts.main([
                    "--tracker", str(env.tracker_path),
                    "--archive-dir", str(env.archive_dir),
                    "--output", str(env.output_path),
                ])
            self.assertTrue(env.output_path.exists())
            data = json.loads(buf.getvalue())
            self.assertEqual(data["wrote"], str(env.output_path))
            self.assertGreater(data["size_bytes"], 100)


if __name__ == "__main__":
    unittest.main()
