#!/usr/bin/env python3
"""A/B token-cost comparison harness for the redesign.

Measures the deterministic *context-loading* cost of each skill before
and after the redesign. Output equivalence on the analytical layer
(classification, recommendations) requires real LLM calls and is
covered by manual validation; this harness covers the part that is
mechanical and reproducible.

Per-skill profiles describe which files would be Read at the start of
an invocation. The harness:
  1. Resolves each profile entry to a real file
  2. Sums byte counts
  3. Estimates token count (1 tok ≈ 4 chars English, ≈ 2 chars CJK;
     we use a 3.0 chars/token blended estimate for mixed content)
  4. Reports before/after delta per skill + grand total

The "after" profile assumes:
  - tracker_summary.md exists in the working dir
  - tracker_query.py exists and is invoked for narrow slices (cost
    counted as the typical query output size, not the script size)
  - knowledge files referenced on-demand only when a signal triggers
    (counted as 0 baseline; future Phase 2 will refine this)

Examples:
  python ab_compare.py --plugin-root /path/to/plugin --working-dir .
  python ab_compare.py --json
  python ab_compare.py --skill analyze
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Heuristic: blended ratio for mixed Chinese + English content.
# Anthropic tokenizer averages ~3.0 chars/token for the user's posts.
CHARS_PER_TOKEN = 3.0


@dataclass
class FileSpec:
    """One file pulled into context for a skill invocation."""
    path: Path
    label: str
    optional: bool = False
    typical_bytes_override: int | None = None  # for synthetic queries


@dataclass
class SkillProfile:
    skill: str
    files: list[FileSpec] = field(default_factory=list)


def measure(spec: FileSpec) -> dict[str, Any]:
    if spec.typical_bytes_override is not None:
        bytes_ = spec.typical_bytes_override
        return {
            "label": spec.label,
            "path": str(spec.path),
            "bytes": bytes_,
            "tokens_est": int(bytes_ / CHARS_PER_TOKEN),
            "exists": True,
            "synthetic": True,
        }
    if not spec.path.exists():
        return {
            "label": spec.label,
            "path": str(spec.path),
            "bytes": 0,
            "tokens_est": 0,
            "exists": False,
            "missing_optional": spec.optional,
        }
    bytes_ = spec.path.stat().st_size
    return {
        "label": spec.label,
        "path": str(spec.path),
        "bytes": bytes_,
        "tokens_est": int(bytes_ / CHARS_PER_TOKEN),
        "exists": True,
    }


def aggregate(profile: SkillProfile) -> dict[str, Any]:
    measurements = [measure(s) for s in profile.files]
    total_bytes = sum(m["bytes"] for m in measurements)
    total_tokens = sum(m["tokens_est"] for m in measurements)
    return {
        "skill": profile.skill,
        "files": measurements,
        "total_bytes": total_bytes,
        "total_tokens_est": total_tokens,
    }


# ---------- Profile builders ---------- #


def before_profile(skill: str, plugin_root: Path, working_dir: Path) -> SkillProfile:
    """Profile that reflects the v1.1.0 behavior — heavy auto-load."""
    sub = plugin_root / "skills" / skill
    knowledge = plugin_root / "knowledge"
    files = [
        FileSpec(plugin_root / "SKILL.md", "main_skill"),
        FileSpec(sub / "SKILL.md", f"{skill}_skill"),
        FileSpec(knowledge / "_shared" / "principles.md", "shared_principles"),
        FileSpec(knowledge / "_shared" / "discovery.md", "shared_discovery"),
        FileSpec(knowledge / "_shared" / "config.md", "shared_config", optional=True),
        FileSpec(knowledge / "data-confidence.md", "data_confidence"),
    ]
    if skill in {"analyze", "predict", "draft"}:
        files += [
            FileSpec(knowledge / "psychology.md", "psychology_kb"),
            FileSpec(knowledge / "algorithm.md", "algorithm_kb"),
            FileSpec(knowledge / "ai-detection.md", "ai_detection_kb"),
        ]
    if skill in {"refresh", "review"}:
        files += [FileSpec(knowledge / "chrome-selectors.md", "chrome_selectors", optional=True)]
    # User-data files — read in full under v1.1.0
    files += [
        FileSpec(working_dir / "threads_daily_tracker.json", "tracker_full"),
        FileSpec(working_dir / "style_guide.md", "style_guide", optional=True),
        FileSpec(working_dir / "concept_library.md", "concept_library", optional=True),
        FileSpec(working_dir / "brand_voice.md", "brand_voice", optional=True),
    ]
    return SkillProfile(skill=skill, files=files)


def after_profile(skill: str, plugin_root: Path, working_dir: Path) -> SkillProfile:
    """Profile after Phase 1 redesign — lean baseline + on-demand queries."""
    sub = plugin_root / "skills" / skill
    files = [
        FileSpec(plugin_root / "SKILL.md", "main_skill"),
        FileSpec(sub / "SKILL.md", f"{skill}_skill"),
    ]
    # No bulk knowledge auto-load. Phase 2 will add kb_query.py per-section
    # reads; Phase 1 leaves them as on-demand-only with zero baseline.
    files += [
        FileSpec(working_dir / "tracker_summary.md", "tracker_summary"),
        FileSpec(working_dir / "style_guide.md", "style_guide", optional=True),
        FileSpec(working_dir / "concept_library.md", "concept_library", optional=True),
        FileSpec(working_dir / "brand_voice.md", "brand_voice", optional=True),
    ]
    # Typical narrow query output size from tracker_query.py for skills
    # that need comparable-set lookup (~3-5 KB).
    if skill in {"analyze", "predict", "topics"}:
        files.append(FileSpec(
            path=working_dir / "(tracker_query comparable)",
            label="tracker_query_comparable",
            typical_bytes_override=4096,
        ))
    return SkillProfile(skill=skill, files=files)


SKILLS_TO_COMPARE = ["analyze", "predict", "draft", "review", "topics"]


def compare(
    plugin_root: Path,
    working_dir: Path,
    only_skill: str | None = None,
) -> dict[str, Any]:
    skills = [only_skill] if only_skill else SKILLS_TO_COMPARE
    rows = []
    for s in skills:
        before = aggregate(before_profile(s, plugin_root, working_dir))
        after = aggregate(after_profile(s, plugin_root, working_dir))
        delta_bytes = before["total_bytes"] - after["total_bytes"]
        delta_pct = (delta_bytes / before["total_bytes"] * 100) if before["total_bytes"] else 0
        rows.append({
            "skill": s,
            "before": before,
            "after": after,
            "delta_bytes": delta_bytes,
            "delta_tokens_est": before["total_tokens_est"] - after["total_tokens_est"],
            "reduction_pct": round(delta_pct, 1),
        })
    grand_before_bytes = sum(r["before"]["total_bytes"] for r in rows)
    grand_after_bytes = sum(r["after"]["total_bytes"] for r in rows)
    grand_before_tok = sum(r["before"]["total_tokens_est"] for r in rows)
    grand_after_tok = sum(r["after"]["total_tokens_est"] for r in rows)
    return {
        "plugin_root": str(plugin_root),
        "working_dir": str(working_dir),
        "skills": rows,
        "grand_total": {
            "before_bytes": grand_before_bytes,
            "after_bytes": grand_after_bytes,
            "delta_bytes": grand_before_bytes - grand_after_bytes,
            "before_tokens_est": grand_before_tok,
            "after_tokens_est": grand_after_tok,
            "delta_tokens_est": grand_before_tok - grand_after_tok,
            "reduction_pct": round(
                (grand_before_bytes - grand_after_bytes) / grand_before_bytes * 100, 1
            ) if grand_before_bytes else 0,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# A/B Token-Cost Comparison Report")
    lines.append("")
    lines.append(f"- Plugin root: `{report['plugin_root']}`")
    lines.append(f"- Working dir: `{report['working_dir']}`")
    lines.append(f"- Token estimate: {CHARS_PER_TOKEN} chars/token (blended CJK+English)")
    lines.append("")
    lines.append("## Per-skill comparison")
    lines.append("")
    lines.append("| Skill | Before bytes | After bytes | Δ bytes | Δ tokens est | Reduction |")
    lines.append("|-------|------|-------|---------|---------|-----------|")
    for r in report["skills"]:
        lines.append(
            f"| {r['skill']} | {r['before']['total_bytes']:,} | {r['after']['total_bytes']:,} | "
            f"{r['delta_bytes']:,} | {r['delta_tokens_est']:,} | {r['reduction_pct']}% |"
        )
    lines.append("")
    g = report["grand_total"]
    lines.append("## Grand total")
    lines.append(f"- Before: **{g['before_bytes']:,} bytes** (~{g['before_tokens_est']:,} tokens)")
    lines.append(f"- After:  **{g['after_bytes']:,} bytes** (~{g['after_tokens_est']:,} tokens)")
    lines.append(f"- Reduction: **{g['reduction_pct']}%** ({g['delta_bytes']:,} bytes, ~{g['delta_tokens_est']:,} tokens)")
    lines.append("")
    lines.append("## Per-file breakdown (analyze, before)")
    a_before = next(r["before"] for r in report["skills"] if r["skill"] == "analyze") \
        if any(r["skill"] == "analyze" for r in report["skills"]) else None
    if a_before:
        lines.append("")
        lines.append("| File | Bytes | Tokens est |")
        lines.append("|------|-------|------------|")
        for f in a_before["files"]:
            mark = " (missing)" if not f.get("exists") else ""
            lines.append(f"| {f['label']}{mark} | {f['bytes']:,} | {f['tokens_est']:,} |")
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ab_compare", description=__doc__)
    p.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent,
        help="Path to plugin root (default: this repo)",
    )
    p.add_argument(
        "--working-dir",
        type=Path,
        default=Path("C:/Users/Kenneth/Claude/threads-personal"),
        help="User working dir containing tracker + companion files",
    )
    p.add_argument("--skill", default=None, help="Only compare this skill")
    p.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    p.add_argument("--output", type=Path, default=None, help="Write report to file")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    args = build_parser().parse_args(argv)
    report = compare(args.plugin_root, args.working_dir, args.skill)
    out = json.dumps(report, indent=2) if args.json else render_markdown(report)
    if args.output:
        args.output.write_text(out, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
