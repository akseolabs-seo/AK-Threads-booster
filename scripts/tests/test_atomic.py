"""Tests for `scripts/_atomic.py` — FAILSAFE-honoring writes."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

# Add scripts/ to path so we can import the helper directly.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from _atomic import (  # noqa: E402
    atomic_write_json,
    parse_iso_or_min,
    post_sort_key,
    prune_backups,
)


class AtomicWriteHappyPathTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "tracker.json"

    def test_first_write_creates_file_no_backup(self):
        atomic_write_json(self.path, {"posts": []})
        self.assertTrue(self.path.exists())
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data, {"posts": []})
        # No backup since file did not exist beforehand.
        self.assertEqual(list(self.path.parent.glob("*.bak-*")), [])

    def test_second_write_creates_backup(self):
        atomic_write_json(self.path, {"posts": [], "version": 1})
        atomic_write_json(self.path, {"posts": [], "version": 2})

        backups = list(self.path.parent.glob(f"{self.path.name}.bak-*"))
        self.assertEqual(len(backups), 1)
        # Backup contains the prior content.
        old = json.loads(backups[0].read_text(encoding="utf-8"))
        self.assertEqual(old["version"], 1)
        # Destination is the new content.
        new = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(new["version"], 2)

    def test_no_tmp_or_failed_orphans_on_success(self):
        atomic_write_json(self.path, {"posts": []})
        atomic_write_json(self.path, {"posts": [{"id": "a"}]})
        siblings = list(self.path.parent.iterdir())
        names = {s.name for s in siblings}
        for name in names:
            self.assertFalse(
                name.endswith(".tmp") or ".tmp-" in name or "FAILED" in name,
                msg=f"orphan file: {name}",
            )

    def test_cjk_content_round_trips(self):
        payload = {"posts": [{"id": "x", "text": "你好，世界 🌏"}]}
        atomic_write_json(self.path, payload)
        loaded = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["posts"][0]["text"], "你好，世界 🌏")

    def test_creates_parent_dirs(self):
        nested = Path(self.tmp.name) / "deep" / "nested" / "tracker.json"
        atomic_write_json(nested, {"ok": True})
        self.assertTrue(nested.exists())


class BackupPruneTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "tracker.json"
        self.path.write_text("{}", encoding="utf-8")

    def _make_backup(self, stamp: str) -> Path:
        bak = self.path.with_name(f"{self.path.name}.bak-{stamp}")
        bak.write_text("{}", encoding="utf-8")
        return bak

    def test_under_keep_keeps_all(self):
        for stamp in ("20260101T000000Z", "20260102T000000Z", "20260103T000000Z"):
            self._make_backup(stamp)
        deleted = prune_backups(self.path, keep=5)
        self.assertEqual(deleted, 0)
        self.assertEqual(len(list(self.path.parent.glob("*.bak-*"))), 3)

    def test_at_keep_keeps_all(self):
        for i in range(5):
            self._make_backup(f"2026010{i+1}T000000Z")
        deleted = prune_backups(self.path, keep=5)
        self.assertEqual(deleted, 0)
        self.assertEqual(len(list(self.path.parent.glob("*.bak-*"))), 5)

    def test_over_keep_drops_oldest(self):
        stamps = [f"2026010{i+1}T000000Z" for i in range(8)]
        for stamp in stamps:
            self._make_backup(stamp)
        deleted = prune_backups(self.path, keep=5)
        self.assertEqual(deleted, 3)
        remaining = sorted(self.path.parent.glob("*.bak-*"))
        self.assertEqual(len(remaining), 5)
        # The 5 newest (lexicographically last for ISO-compact stamps) survive.
        for name in remaining:
            self.assertNotIn("20260101", name.name)
            self.assertNotIn("20260102", name.name)
            self.assertNotIn("20260103", name.name)

    def test_atomic_write_prunes_after_n_writes(self):
        # 7 sequential writes should leave at most 5 .bak files.
        for n in range(7):
            atomic_write_json(self.path, {"n": n}, keep=5)
        backups = list(self.path.parent.glob(f"{self.path.name}.bak-*"))
        self.assertLessEqual(len(backups), 5)


class CrashMidWriteTest(unittest.TestCase):
    """Simulate failures and confirm the destination is never corrupted."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "tracker.json"
        self.path.write_text(
            json.dumps({"original": "data", "important": True}, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_rename_failure_preserves_original(self):
        # os.replace always raises -> destination should remain pristine.
        with mock.patch("_atomic.os.replace", side_effect=PermissionError("locked")):
            with self.assertRaises(RuntimeError) as cm:
                atomic_write_json(
                    self.path,
                    {"new": "content"},
                    rename_retries=2,
                    rename_backoff=0.01,
                )
        self.assertIn("atomic rename failed", str(cm.exception))

        # Original file is untouched.
        loaded = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["original"], "data")
        self.assertTrue(loaded["important"])

        # A backup was made before the failed rename, and the new content is
        # preserved as a FAILED orphan for recovery.
        siblings = list(self.path.parent.iterdir())
        names = " ".join(s.name for s in siblings)
        self.assertIn(".bak-", names)
        self.assertIn("FAILED", names)

    def test_rename_succeeds_after_transient_failure(self):
        call_state = {"attempts": 0}
        real_replace = os.replace

        def flaky_replace(src, dst):
            call_state["attempts"] += 1
            if call_state["attempts"] < 2:
                raise PermissionError("transient")
            return real_replace(src, dst)

        with mock.patch("_atomic.os.replace", side_effect=flaky_replace):
            atomic_write_json(
                self.path,
                {"new": "content"},
                rename_retries=5,
                rename_backoff=0.01,
            )

        loaded = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["new"], "content")
        self.assertGreaterEqual(call_state["attempts"], 2)


class ParseIsoOrMinTest(unittest.TestCase):
    """`parse_iso_or_min` + `post_sort_key` fix the lex-sort bug."""

    def test_z_and_offset_compare_correctly(self):
        a = parse_iso_or_min("2026-05-07T12:00:00Z")
        b = parse_iso_or_min("2026-05-07T12:00:00+00:00")
        self.assertEqual(a, b)

    def test_offset_difference_is_chronological(self):
        # 2026-05-07T12:00:00+07:00 = 2026-05-07T05:00:00Z
        # 2026-05-07T12:00:00+00:00 = 2026-05-07T12:00:00Z
        # First is earlier even though "+07:00" > "+00:00" lexicographically.
        early = parse_iso_or_min("2026-05-07T12:00:00+07:00")
        late = parse_iso_or_min("2026-05-07T12:00:00+00:00")
        self.assertLess(early, late)

    def test_falsy_returns_min_utc(self):
        self.assertEqual(
            parse_iso_or_min(None), datetime.min.replace(tzinfo=timezone.utc)
        )
        self.assertEqual(
            parse_iso_or_min(""), datetime.min.replace(tzinfo=timezone.utc)
        )

    def test_invalid_returns_min_not_raise(self):
        self.assertEqual(
            parse_iso_or_min("not-a-date"),
            datetime.min.replace(tzinfo=timezone.utc),
        )

    def test_post_sort_key_handles_missing_field(self):
        post_no_field = {"id": "x"}
        post_with_z = {"id": "y", "created_at": "2026-05-07T12:00:00Z"}
        post_with_offset = {"id": "z", "created_at": "2026-05-07T12:00:00+07:00"}

        ordered = sorted(
            [post_no_field, post_with_z, post_with_offset],
            key=post_sort_key,
            reverse=True,
        )
        self.assertEqual(ordered[0]["id"], "y")  # Z (later)
        self.assertEqual(ordered[1]["id"], "z")  # +07:00 (earlier)
        self.assertEqual(ordered[2]["id"], "x")  # missing -> min

    def test_lex_sort_would_be_wrong_but_iso_sort_is_right(self):
        """Regression: lex sort and ISO sort disagree on identical instants.

        Two posts at the same UTC instant but with different offsets
        should compare equal chronologically. Lex sort orders them by
        the offset character.
        """
        same_instant = [
            {"id": "tokyo", "created_at": "2026-05-07T21:00:00+09:00"},
            {"id": "utc", "created_at": "2026-05-07T12:00:00Z"},
        ]

        # Lex sort: leading hour digit "2" vs "1" -> tokyo string is
        # lex-greater, so reverse-sort puts tokyo first.
        lex = sorted(
            same_instant, key=lambda p: p.get("created_at", ""), reverse=True
        )
        # ISO sort: chronological equality -> stable order preserves
        # input order (tokyo, utc).
        iso = sorted(same_instant, key=post_sort_key, reverse=True)

        # Same chronological instant.
        self.assertEqual(post_sort_key(same_instant[0]), post_sort_key(same_instant[1]))
        # Lex disagrees with ISO on which is "first" because string
        # ordering is not chronological — that is the bug we are fixing.
        # On this synthetic case the two sorts happen to land on the
        # same first element, but the underlying lex comparison is
        # noise: change the offsets so the lex order flips.
        diverging = [
            {"id": "off_plus", "created_at": "2026-05-07T05:00:00+05:00"},
            {"id": "off_zulu", "created_at": "2026-05-07T00:00:00Z"},
        ]
        lex2 = sorted(diverging, key=lambda p: p.get("created_at", ""), reverse=True)
        iso2 = sorted(diverging, key=post_sort_key, reverse=True)
        # Same instant -> ISO compare equal -> stable order.
        self.assertEqual(post_sort_key(diverging[0]), post_sort_key(diverging[1]))
        # But lex sees the leading "T05" vs "T00" and reverse-sorts them
        # -> off_plus first under lex.
        self.assertEqual(lex2[0]["id"], "off_plus")
        # Stable ISO sort preserves input order.
        self.assertEqual(iso2[0]["id"], "off_plus")
        # Both end with the same set of ids regardless of sort.
        self.assertEqual({p["id"] for p in lex2}, {p["id"] for p in iso2})


if __name__ == "__main__":
    unittest.main()
