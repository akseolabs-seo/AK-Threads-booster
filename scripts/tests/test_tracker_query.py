"""Tests for scripts/tracker_query.py.

Run from repo root:
    python -m unittest scripts.tests.test_tracker_query

The fixture lives at scripts/tests/fixtures/sample_tracker.json and contains
4 representative posts spanning content_type, hook_type, age, and metrics
extremes so each subcommand can be exercised meaningfully.
"""
from __future__ import annotations

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow importing the script as a module
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import tracker_query  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "sample_tracker.json"


def run(argv: list[str]) -> dict:
    """Run the CLI with the test fixture and capture parsed JSON output."""
    full = ["--tracker", str(FIXTURE)] + argv
    buf = io.StringIO()
    with redirect_stdout(buf):
        tracker_query.main(full)
    return json.loads(buf.getvalue())


class FreezeTime:
    """Freeze datetime.now to a fixed value during a block."""

    def __init__(self, frozen: datetime) -> None:
        self.frozen = frozen
        self._orig = None

    def __enter__(self) -> "FreezeTime":
        frozen = self.frozen

        class _FrozenDT(datetime):
            @classmethod
            def now(cls, tz=None):  # type: ignore[override]
                if tz is None:
                    return frozen.replace(tzinfo=None)
                return frozen.astimezone(tz)

        self._orig = tracker_query.datetime  # type: ignore[attr-defined]
        tracker_query.datetime = _FrozenDT  # type: ignore[attr-defined]
        return self

    def __exit__(self, *exc) -> None:
        tracker_query.datetime = self._orig  # type: ignore[attr-defined]


# Use a fixed "today" so windowing is deterministic against the fixture
FROZEN_NOW = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)


class TestRecent(unittest.TestCase):
    def test_recent_30d_returns_posts_within_window(self) -> None:
        with FreezeTime(FROZEN_NOW):
            out = run(["recent", "--days", "30"])
        ids = [p["id"] for p in out["posts"]]
        # p001 (2026-05-01), p003 (2026-04-20), p004 (2026-04-29) are within 30d of 2026-05-02
        self.assertIn("p001", ids)
        self.assertIn("p003", ids)
        self.assertIn("p004", ids)
        self.assertNotIn("p002", ids)  # 2026-03-15 is >30d old
        self.assertEqual(out["window_days"], 30)
        self.assertEqual(out["count"], 3)

    def test_recent_sorted_newest_first(self) -> None:
        with FreezeTime(FROZEN_NOW):
            out = run(["recent", "--days", "60"])
        ids = [p["id"] for p in out["posts"]]
        # 60d from 2026-05-02 includes all 4 fixture posts; check ordering
        self.assertEqual(ids, ["p001", "p004", "p003", "p002"])

    def test_include_comments_flag(self) -> None:
        with FreezeTime(FROZEN_NOW):
            out_with = run(["recent", "--days", "30", "--include-comments"])
            out_without = run(["recent", "--days", "30"])
        # p001 has 1 comment in fixture
        post_with = next(p for p in out_with["posts"] if p["id"] == "p001")
        post_without = next(p for p in out_without["posts"] if p["id"] == "p001")
        self.assertIn("comments", post_with)
        self.assertNotIn("comments", post_without)


class TestTop(unittest.TestCase):
    def test_top_by_engagement_default(self) -> None:
        out = run(["top", "--limit", "4"])
        ids = [p["id"] for p in out["posts"]]
        # p002 has highest combined engagement (300 + 50*3 + 20*2 + 10*2 = 510)
        self.assertEqual(ids[0], "p002")
        self.assertEqual(out["metric"], "engagement")

    def test_top_with_topic_filter(self) -> None:
        out = run(["top", "--topic", "AI", "--limit", "5"])
        ids = [p["id"] for p in out["posts"]]
        # Only p001, p003, p004 have "AI" topic
        self.assertEqual(set(ids), {"p001", "p003", "p004"})

    def test_top_by_likes_metric(self) -> None:
        out = run(["top", "--metric", "likes", "--limit", "2"])
        ids = [p["id"] for p in out["posts"]]
        self.assertEqual(ids, ["p002", "p001"])  # 300, 100

    def test_top_limit_respected(self) -> None:
        out = run(["top", "--limit", "2"])
        self.assertEqual(len(out["posts"]), 2)


class TestComparable(unittest.TestCase):
    def test_filter_by_content_type(self) -> None:
        out = run(["comparable", "--content-type", "list"])
        ids = {p["id"] for p in out["posts"]}
        self.assertEqual(ids, {"p001", "p002"})

    def test_filter_by_hook_type(self) -> None:
        out = run(["comparable", "--hook-type", "question"])
        ids = {p["id"] for p in out["posts"]}
        self.assertEqual(ids, {"p001", "p002", "p004"})

    def test_combined_filters(self) -> None:
        out = run(["comparable", "--content-type", "list", "--hook-type", "question", "--topic", "AI"])
        ids = [p["id"] for p in out["posts"]]
        self.assertEqual(ids, ["p001"])

    def test_sorted_by_engagement(self) -> None:
        out = run(["comparable", "--hook-type", "question", "--limit", "10"])
        ids = [p["id"] for p in out["posts"]]
        # p002 highest, then p001, then p004
        self.assertEqual(ids[0], "p002")


class TestHookStats(unittest.TestCase):
    def test_aggregates_by_hook_type(self) -> None:
        out = run(["hook-stats"])
        hooks = out["hook_types"]
        self.assertIn("question", hooks)
        self.assertIn("shock", hooks)
        self.assertEqual(hooks["question"]["count"], 3)
        self.assertEqual(hooks["shock"]["count"], 1)
        self.assertEqual(out["total_posts"], 4)

    def test_engagement_avg_computed(self) -> None:
        out = run(["hook-stats"])
        question = out["hook_types"]["question"]
        # p001 (109+15+10+6=149... actually) p001=100+60+10+6=176, p002=300+150+40+20=510, p004=75+36+6+4=121
        # avg = (176 + 510 + 121) / 3 = 269.0
        self.assertAlmostEqual(question["engagement_avg"], 269.0, places=1)


class TestAiToneStats(unittest.TestCase):
    def test_counts_signals_across_posts(self) -> None:
        out = run(["ai-tone-stats"])
        sigs = out["signal_frequencies"]
        # p001 has structural-perfection, p003 has structural-perfection + emoji-overuse
        self.assertEqual(sigs.get("structural-perfection"), 2)
        self.assertEqual(sigs.get("emoji-overuse"), 1)
        # risk_flags also captured with risk: prefix
        self.assertEqual(sigs.get("risk:over-promotional"), 1)
        self.assertEqual(sigs.get("risk:over-tagging"), 1)


class TestPostLookup(unittest.TestCase):
    def test_lookup_by_id(self) -> None:
        out = run(["post", "--id", "p001"])
        self.assertEqual(out["count"], 1)
        self.assertEqual(out["posts"][0]["id"], "p001")
        # comments included by default for single-post lookup
        self.assertIn("comments", out["posts"][0])

    def test_lookup_by_date_prefix(self) -> None:
        out = run(["post", "--date", "2026-04-20"])
        self.assertEqual(out["count"], 1)
        self.assertEqual(out["posts"][0]["id"], "p003")

    def test_lookup_no_match(self) -> None:
        out = run(["post", "--id", "nonexistent"])
        self.assertEqual(out["count"], 0)
        self.assertEqual(out["posts"], [])


class TestMeta(unittest.TestCase):
    def test_meta_reports_post_count_and_dates(self) -> None:
        out = run(["meta"])
        self.assertEqual(out["post_count"], 4)
        self.assertEqual(out["date_range"]["earliest"], "2026-03-15T09:00:00Z")
        self.assertEqual(out["date_range"]["latest"], "2026-05-01T12:00:00Z")
        self.assertEqual(out["account"]["handle"], "@testuser")
        self.assertIn("posts", out["top_level_keys"])


class TestEngagementScore(unittest.TestCase):
    def test_weighting(self) -> None:
        post = {"metrics": {"likes": 10, "replies": 2, "reposts": 1, "shares": 1}}
        self.assertEqual(tracker_query.engagement_score(post), 10 + 6 + 2 + 2)

    def test_handles_missing_metrics(self) -> None:
        self.assertEqual(tracker_query.engagement_score({}), 0)
        self.assertEqual(tracker_query.engagement_score({"metrics": {}}), 0)


class TestParseIso(unittest.TestCase):
    def test_with_z(self) -> None:
        dt = tracker_query.parse_iso("2026-05-01T12:00:00Z")
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_with_offset(self) -> None:
        dt = tracker_query.parse_iso("2026-05-01T20:00:00+08:00")
        self.assertEqual(dt.year, 2026)


if __name__ == "__main__":
    unittest.main()
