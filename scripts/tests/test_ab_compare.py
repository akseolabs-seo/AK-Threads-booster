"""Tests for ab_compare.py.

The harness measures context-load cost deterministically; tests verify
that profiles include the right files and the math is right.
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS_TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_TESTS_DIR))

import ab_compare  # noqa: E402


def make_fake_plugin(root: Path) -> None:
    (root / "skills" / "analyze").mkdir(parents=True)
    (root / "skills" / "predict").mkdir(parents=True)
    (root / "skills" / "draft").mkdir(parents=True)
    (root / "skills" / "review").mkdir(parents=True)
    (root / "skills" / "topics").mkdir(parents=True)
    (root / "skills" / "refresh").mkdir(parents=True)
    (root / "knowledge" / "_shared").mkdir(parents=True)

    # Make file sizes distinct + non-trivial so totals are meaningful
    (root / "SKILL.md").write_text("X" * 500, encoding="utf-8")
    (root / "skills" / "analyze" / "SKILL.md").write_text("X" * 5000, encoding="utf-8")
    (root / "skills" / "predict" / "SKILL.md").write_text("X" * 2500, encoding="utf-8")
    (root / "skills" / "draft" / "SKILL.md").write_text("X" * 4500, encoding="utf-8")
    (root / "skills" / "review" / "SKILL.md").write_text("X" * 3000, encoding="utf-8")
    (root / "skills" / "topics" / "SKILL.md").write_text("X" * 2000, encoding="utf-8")
    (root / "knowledge" / "psychology.md").write_text("P" * 40000, encoding="utf-8")
    (root / "knowledge" / "algorithm.md").write_text("A" * 28000, encoding="utf-8")
    (root / "knowledge" / "ai-detection.md").write_text("D" * 28000, encoding="utf-8")
    (root / "knowledge" / "data-confidence.md").write_text("C" * 3000, encoding="utf-8")
    (root / "knowledge" / "_shared" / "principles.md").write_text("p" * 1500, encoding="utf-8")
    (root / "knowledge" / "_shared" / "discovery.md").write_text("d" * 1500, encoding="utf-8")
    (root / "knowledge" / "_shared" / "config.md").write_text("c" * 2000, encoding="utf-8")


def make_fake_working_dir(wd: Path) -> None:
    wd.mkdir(parents=True, exist_ok=True)
    (wd / "threads_daily_tracker.json").write_text("T" * 168000, encoding="utf-8")
    (wd / "tracker_summary.md").write_text("S" * 5500, encoding="utf-8")
    (wd / "style_guide.md").write_text("g" * 24000, encoding="utf-8")
    (wd / "concept_library.md").write_text("c" * 13000, encoding="utf-8")
    (wd / "brand_voice.md").write_text("v" * 15000, encoding="utf-8")


class FakeFS:
    def __enter__(self) -> "FakeFS":
        self.tmp = Path(tempfile.mkdtemp(prefix="ab_test_"))
        self.plugin = self.tmp / "plugin"
        self.wd = self.tmp / "wd"
        make_fake_plugin(self.plugin)
        make_fake_working_dir(self.wd)
        return self

    def __exit__(self, *exc) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestProfiles(unittest.TestCase):
    def test_before_includes_heavy_knowledge(self) -> None:
        with FakeFS() as fs:
            prof = ab_compare.before_profile("analyze", fs.plugin, fs.wd)
            labels = [f.label for f in prof.files]
            self.assertIn("psychology_kb", labels)
            self.assertIn("algorithm_kb", labels)
            self.assertIn("ai_detection_kb", labels)
            self.assertIn("tracker_full", labels)

    def test_after_omits_heavy_knowledge(self) -> None:
        with FakeFS() as fs:
            prof = ab_compare.after_profile("analyze", fs.plugin, fs.wd)
            labels = [f.label for f in prof.files]
            self.assertNotIn("psychology_kb", labels)
            self.assertNotIn("algorithm_kb", labels)
            self.assertNotIn("ai_detection_kb", labels)
            self.assertNotIn("tracker_full", labels)
            self.assertIn("tracker_summary", labels)
            self.assertIn("tracker_query_comparable", labels)


class TestComparison(unittest.TestCase):
    def test_grand_total_reduction_above_threshold(self) -> None:
        with FakeFS() as fs:
            report = ab_compare.compare(fs.plugin, fs.wd)
            grand = report["grand_total"]
            # With heavy knowledge stripped, expect at least 60% reduction
            self.assertGreater(grand["reduction_pct"], 60.0)

    def test_per_skill_reductions_present(self) -> None:
        with FakeFS() as fs:
            report = ab_compare.compare(fs.plugin, fs.wd)
        skill_names = [r["skill"] for r in report["skills"]]
        for s in ["analyze", "predict", "draft", "review", "topics"]:
            self.assertIn(s, skill_names)

    def test_only_skill_filter(self) -> None:
        with FakeFS() as fs:
            report = ab_compare.compare(fs.plugin, fs.wd, only_skill="analyze")
        self.assertEqual(len(report["skills"]), 1)
        self.assertEqual(report["skills"][0]["skill"], "analyze")

    def test_optional_missing_files_dont_crash(self) -> None:
        with FakeFS() as fs:
            (fs.wd / "brand_voice.md").unlink()  # remove optional
            (fs.wd / "tracker_summary.md").unlink()  # the after baseline
            report = ab_compare.compare(fs.plugin, fs.wd, only_skill="analyze")
        # Should still complete, just with missing files counted as 0 bytes
        self.assertIn("after", report["skills"][0])


class TestRender(unittest.TestCase):
    def test_markdown_renders_grand_total(self) -> None:
        with FakeFS() as fs:
            report = ab_compare.compare(fs.plugin, fs.wd)
            md = ab_compare.render_markdown(report)
        self.assertIn("# A/B Token-Cost Comparison Report", md)
        self.assertIn("## Grand total", md)
        self.assertIn("Reduction:", md)
        self.assertIn("analyze", md)

    def test_json_output(self) -> None:
        with FakeFS() as fs:
            buf = io.StringIO()
            with redirect_stdout(buf):
                ab_compare.main([
                    "--plugin-root", str(fs.plugin),
                    "--working-dir", str(fs.wd),
                    "--json",
                ])
            data = json.loads(buf.getvalue())
            self.assertIn("grand_total", data)
            self.assertIn("skills", data)


if __name__ == "__main__":
    unittest.main()
