#!/usr/bin/env python3
"""
AK-Threads-Booster: Build low-token compiled memory from threads_daily_tracker.json.

Usage:
    python scripts/build_compiled_memory.py --tracker threads_daily_tracker.json
    python scripts/build_compiled_memory.py --tracker threads_daily_tracker.json --output-dir compiled

Outputs:
    compiled/account_wiki.md
    compiled/account_state.md
    compiled/personal_signal_memory.md
    compiled/next_move_queue.md
    compiled/post_feature_index.jsonl
    compiled/cluster_wiki.json
    compiled/exemplar_bank.md
    compiled/recent_window.md
    compiled/voice_fingerprint.json
    compiled/voice_fingerprint.md

The tracker remains the source of truth. These files are derived runtime caches.
"""

import argparse
import hashlib
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# Make sibling scripts importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _atomic import configure_utf8_stdout  # noqa: E402

try:
    from build_voice_distillation import write_outputs as write_voice_outputs
except ModuleNotFoundError:
    from scripts.build_voice_distillation import write_outputs as write_voice_outputs


WORD_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0e00-\u0e7f]+")


def parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None


def sort_key(post: Dict[str, Any]) -> datetime:
    return parse_iso(post.get("created_at")) or datetime.min.replace(tzinfo=timezone.utc)


def post_text(post: Dict[str, Any]) -> str:
    return str(post.get("text") or "").strip()


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def paragraph_count(text: str) -> int:
    return len([p for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text.strip()) if p.strip()]) if text.strip() else 0


def summarize_text(text: str, limit: int = 110) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "..."


def metric(post: Dict[str, Any], name: str) -> Optional[int]:
    value = (post.get("metrics") or {}).get(name)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "yes", "high", "medium", "risk", "risky", "1"}


def views(post: Dict[str, Any]) -> int:
    return metric(post, "views") or 0


def replies(post: Dict[str, Any]) -> int:
    return metric(post, "replies") or 0


def shares(post: Dict[str, Any]) -> int:
    return (metric(post, "shares") or 0) + (metric(post, "reposts") or 0)


def rate(numerator: int, denominator: int) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def median_nonzero(values: Iterable[int]) -> Optional[float]:
    clean = [v for v in values if v is not None and v > 0]
    if not clean:
        return None
    return float(statistics.median(clean))


def compare_ratio(recent_value: Optional[float], baseline_value: Optional[float]) -> Optional[float]:
    if recent_value is None or baseline_value is None or baseline_value <= 0:
        return None
    return recent_value / baseline_value


def semantic_cluster(post: Dict[str, Any]) -> Optional[str]:
    signals = post.get("algorithm_signals") or {}
    freshness = signals.get("topic_freshness") or {}
    cluster = freshness.get("semantic_cluster")
    if cluster:
        return str(cluster)
    topics = post.get("topics") or []
    if topics:
        return " / ".join(str(t).strip().lower() for t in topics[:2] if str(t).strip())
    content_type = post.get("content_type")
    return str(content_type) if content_type else None


def freshness_value(post: Dict[str, Any], field: str) -> Any:
    signals = post.get("algorithm_signals") or {}
    freshness = signals.get("topic_freshness") or {}
    return freshness.get(field)


def nested_value(post: Dict[str, Any], path: Tuple[str, ...]) -> Any:
    current: Any = post
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def originality_risk_count(posts: List[Dict[str, Any]]) -> int:
    paths = [
        ("algorithm_signals", "originality_risk", "caption_content_mismatch"),
        ("algorithm_signals", "originality_risk", "hashtag_stuffing_risk"),
        ("algorithm_signals", "originality_risk", "duplicate_cluster_risk"),
        ("algorithm_signals", "originality_risk", "minor_edit_repost_risk"),
        ("algorithm_signals", "originality_risk", "low_value_reaction_risk"),
        ("algorithm_signals", "originality_risk", "fake_engagement_pattern_risk"),
    ]
    return sum(1 for post in posts for path in paths if truthy(nested_value(post, path)))


AI_TONE_PATTERNS = [
    "not just",
    "in today's world",
    "the key is",
    "ultimately",
    "furthermore",
    "moreover",
    "不只是",
    "關鍵是",
    "最重要的是",
    "總結來說",
    "換句話說",
]


def ai_tone_hits(text: str) -> int:
    lowered = text.lower()
    hits = sum(1 for pattern in AI_TONE_PATTERNS if pattern.lower() in lowered)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text.strip()) if p.strip()]
    if len(paragraphs) >= 4:
        lengths = [len(p) for p in paragraphs]
        if max(lengths) - min(lengths) < 35:
            hits += 1
    if len(re.findall(r"^\s*[-*]\s+", text, flags=re.MULTILINE)) >= 5:
        hits += 1
    return hits


def post_score(post: Dict[str, Any]) -> int:
    return views(post) + replies(post) * 30 + shares(post) * 50


def top_by_score(posts: List[Dict[str, Any]], limit: int = 8) -> List[Dict[str, Any]]:
    return sorted(posts, key=post_score, reverse=True)[:limit]


def recent_posts(posts: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    return sorted(posts, key=sort_key, reverse=True)[:limit]


def confidence_level(posts: List[Dict[str, Any]]) -> Tuple[str, str]:
    count = len(posts)
    with_text = sum(1 for p in posts if post_text(p))
    with_views = sum(1 for p in posts if metric(p, "views") is not None)
    if count >= 100 and with_text / max(count, 1) >= 0.9 and with_views / max(count, 1) >= 0.8:
        return "Deep", "Large tracker with strong text and metrics coverage."
    if count >= 50 and with_text / max(count, 1) >= 0.8:
        return "Strong", "Enough history for stable pattern references."
    if count >= 20 and with_text / max(count, 1) >= 0.7:
        return "Usable", "Enough posts for directional comparisons, with some gaps."
    if count >= 10:
        return "Weak", "Limited history; use comparisons cautiously."
    return "Directional", "Very small history; treat patterns as temporary."


def tracker_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shared_meta(tracker_path: Path, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    level, notes = confidence_level(posts)
    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_tracker": tracker_path.name,
        "source_tracker_hash": tracker_hash(tracker_path),
        "posts_count": len(posts),
        "confidence_level": level,
        "coverage_notes": notes,
    }


def post_feature_row(post: Dict[str, Any]) -> Dict[str, Any]:
    text = post_text(post)
    cluster = semantic_cluster(post)
    return {
        "id": post.get("id"),
        "created_at": post.get("created_at"),
        "summary": summarize_text(text),
        "text_excerpt": summarize_text(text, 180),
        "content_type": post.get("content_type"),
        "hook_type": post.get("hook_type"),
        "ending_type": post.get("ending_type"),
        "emotional_arc": post.get("emotional_arc"),
        "word_count": post.get("word_count") or word_count(text),
        "paragraph_count": post.get("paragraph_count") or paragraph_count(text),
        "topics": post.get("topics") or [],
        "semantic_cluster": cluster,
        "freshness_score": freshness_value(post, "freshness_score"),
        "fatigue_risk": freshness_value(post, "fatigue_risk"),
        "metrics": {
            "views": metric(post, "views"),
            "likes": metric(post, "likes"),
            "replies": metric(post, "replies"),
            "reposts": metric(post, "reposts"),
            "shares": metric(post, "shares"),
        },
        "source_post_id": post.get("id"),
    }


def top_posts(posts: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    return sorted(posts, key=views, reverse=True)[:limit]


def median(values: Iterable[int]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return float(statistics.median(clean))


def build_cluster_wiki(meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for post in posts:
        buckets[semantic_cluster(post) or "uncategorized"].append(post)

    clusters = []
    now_sorted = sorted(posts, key=sort_key, reverse=True)
    recent_ids = {p.get("id") for p in now_sorted[:10]}

    for cluster, bucket in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])):
        bucket_sorted = sorted(bucket, key=sort_key, reverse=True)
        top_bucket = top_posts(bucket, 3)
        fatigue_counts = Counter(str(freshness_value(p, "fatigue_risk") or "unknown") for p in bucket)
        common_topics = Counter()
        for post in bucket:
            for topic in post.get("topics") or []:
                if str(topic).strip():
                    common_topics[str(topic).strip().lower()] += 1
        clusters.append({
            "cluster": cluster,
            "post_count": len(bucket),
            "last_post_at": bucket_sorted[0].get("created_at") if bucket_sorted else None,
            "recent_count": sum(1 for p in bucket if p.get("id") in recent_ids),
            "median_views": median(views(p) for p in bucket),
            "top_post_ids": [p.get("id") for p in top_bucket if p.get("id")],
            "representative_post_ids": [p.get("id") for p in bucket_sorted[:3] if p.get("id")],
            "common_topics": [topic for topic, _ in common_topics.most_common(5)],
            "fatigue_risk": fatigue_counts.most_common(1)[0][0] if fatigue_counts else "unknown",
            "notes": "Derived from tracker features. Verify against source posts before making strong claims.",
        })
    return {"_meta": meta, "clusters": clusters}


def markdown_meta(meta: Dict[str, Any]) -> str:
    return (
        f"generated_at: {meta['generated_at']}\n"
        f"source_tracker_hash: {meta['source_tracker_hash']}\n"
        f"posts_count: {meta['posts_count']}\n"
        f"confidence_level: {meta['confidence_level']}\n"
        f"coverage_notes: {meta['coverage_notes']}\n"
    )


def render_account_wiki(meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> str:
    recent = sorted(posts, key=sort_key, reverse=True)[:10]
    best = top_posts(posts, 10)
    content_types = Counter(str(p.get("content_type") or "unknown") for p in posts)
    topics = Counter()
    clusters = Counter()
    for post in posts:
        clusters[semantic_cluster(post) or "uncategorized"] += 1
        for topic in post.get("topics") or []:
            if str(topic).strip():
                topics[str(topic).strip().lower()] += 1

    lines = [
        "# Account Wiki",
        "",
        "> Compiled memory for low-token runtime. Tracker remains the source of truth.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
        "## Account Baseline",
        f"- Historical posts indexed: {len(posts)}",
        f"- Confidence: {meta['confidence_level']} - {meta['coverage_notes']}",
        f"- Common content types: {', '.join(f'{k} ({v})' for k, v in content_types.most_common(5)) or 'unknown'}",
        f"- Common topics: {', '.join(f'{k} ({v})' for k, v in topics.most_common(8)) or 'unknown'}",
        f"- Common clusters: {', '.join(f'{k} ({v})' for k, v in clusters.most_common(8)) or 'unknown'}",
        "",
        "## Highest-Performing Reference Posts",
    ]
    for post in best[:8]:
        lines.append(f"- `{post.get('id')}` views={views(post)} cluster={semantic_cluster(post) or 'unknown'} :: {summarize_text(post_text(post), 130)}")
    lines.extend(["", "## Recent Window"])
    for post in recent:
        lines.append(f"- `{post.get('id')}` {post.get('created_at') or 'unknown'} cluster={semantic_cluster(post) or 'unknown'} :: {summarize_text(post_text(post), 110)}")
    lines.extend([
        "",
        "## Runtime Notes",
        "- Use post IDs above as provenance anchors.",
        "- If a claim matters, verify against `threads_daily_tracker.json` before treating it as strong.",
        "- Rebuild this file after `/setup`, `/refresh`, or `/review` changes the tracker.",
    ])
    return "\n".join(lines) + "\n"


def render_exemplar_bank(meta: Dict[str, Any], posts: List[Dict[str, Any]], limit: int = 20) -> str:
    selected = []
    seen = set()
    for post in top_posts(posts, limit=limit):
        pid = post.get("id")
        if pid not in seen:
            selected.append(post)
            seen.add(pid)
    for post in sorted(posts, key=sort_key, reverse=True)[:10]:
        if len(selected) >= limit:
            break
        pid = post.get("id")
        if pid not in seen:
            selected.append(post)
            seen.add(pid)

    lines = [
        "# Exemplar Bank",
        "",
        "> Capped representative posts for style and performance reference.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
    ]
    for idx, post in enumerate(selected, start=1):
        lines.extend([
            f"## {idx}. `{post.get('id')}`",
            f"- created_at: {post.get('created_at') or 'unknown'}",
            f"- views: {views(post)}",
            f"- cluster: {semantic_cluster(post) or 'unknown'}",
            f"- topics: {', '.join(str(t) for t in (post.get('topics') or [])) or 'unknown'}",
            "",
            post_text(post),
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def render_recent_window(meta: Dict[str, Any], posts: List[Dict[str, Any]], limit: int = 10) -> str:
    recent = sorted(posts, key=sort_key, reverse=True)[:limit]
    cluster_counts = Counter(semantic_cluster(p) or "uncategorized" for p in recent)
    lines = [
        "# Recent Window",
        "",
        "> Last posts for repetition and topic freshness checks.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
        "## Recent Cluster Distribution",
    ]
    for cluster, count in cluster_counts.most_common():
        lines.append(f"- {cluster}: {count}")
    lines.extend(["", "## Recent Posts"])
    for post in recent:
        lines.append(f"- `{post.get('id')}` {post.get('created_at') or 'unknown'} views={views(post)} cluster={semantic_cluster(post) or 'unknown'} fatigue={freshness_value(post, 'fatigue_risk') or 'unknown'} :: {summarize_text(post_text(post), 130)}")
    return "\n".join(lines) + "\n"


def account_state_summary(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    recent = recent_posts(posts, 10)
    historical_view_median = median_nonzero(views(p) for p in posts)
    recent_view_median = median_nonzero(views(p) for p in recent)
    historical_reply_rate = median_nonzero(int(rate(replies(p), max(views(p), 1)) * 10000) for p in posts if views(p))
    recent_reply_rate = median_nonzero(int(rate(replies(p), max(views(p), 1)) * 10000) for p in recent if views(p))
    historical_share_rate = median_nonzero(int(rate(shares(p), max(views(p), 1)) * 10000) for p in posts if views(p))
    recent_share_rate = median_nonzero(int(rate(shares(p), max(views(p), 1)) * 10000) for p in recent if views(p))
    cluster_counts = Counter(semantic_cluster(p) or "uncategorized" for p in recent)
    fatigue_count = sum(1 for p in recent if str(freshness_value(p, "fatigue_risk") or "").lower() in {"medium", "high"})
    ai_hits = sum(ai_tone_hits(post_text(p)) for p in recent)
    total_words = sum(max(word_count(post_text(p)), 1) for p in recent)

    view_ratio = compare_ratio(recent_view_median, historical_view_median)
    reply_ratio = compare_ratio(recent_reply_rate, historical_reply_rate)
    share_ratio = compare_ratio(recent_share_rate, historical_share_rate)

    priorities = []
    risks = []
    if view_ratio is not None and view_ratio < 0.8:
        priorities.append(("陌生人推薦性", "S9", "recent reach is below the account baseline"))
    if share_ratio is not None and share_ratio < 0.8:
        priorities.append(("私下分享潛力", "S1", "recent share/repost rate is below the account baseline"))
    if reply_ratio is not None and reply_ratio < 0.8:
        priorities.append(("深留言觸發", "S2", "recent reply rate is below the account baseline"))
    if fatigue_count >= 3 or (cluster_counts and cluster_counts.most_common(1)[0][1] >= 3):
        priorities.append(("題材新鮮度", "S14", "recent posts cluster too tightly"))
        risks.append(("R5", "連續同題材", "recent semantic clusters repeat enough to watch for fatigue"))
    if originality_risk_count(recent) > 0:
        risks.append(("R4", "低原創性風險", "recent tracker signals include originality-risk flags"))
    if ai_hits / max(total_words, 1) > 0.01 or ai_hits >= 3:
        priorities.append(("人的判斷痕跡", "Anti-AI", "recent text has possible AI-tone patterns"))
        risks.append(("R10", "AI 內容標示與人格感", "verify whether generated material is being presented as personal judgment"))

    if not priorities:
        priorities.append(("信任圖譜", "S8", "no obvious weak signal; keep reinforcing account consistency"))

    return {
        "recent_count": len(recent),
        "historical_view_median": historical_view_median,
        "recent_view_median": recent_view_median,
        "view_ratio": view_ratio,
        "historical_reply_rate": historical_reply_rate,
        "recent_reply_rate": recent_reply_rate,
        "reply_ratio": reply_ratio,
        "historical_share_rate": historical_share_rate,
        "recent_share_rate": recent_share_rate,
        "share_ratio": share_ratio,
        "cluster_counts": cluster_counts,
        "fatigue_count": fatigue_count,
        "ai_hits": ai_hits,
        "priorities": priorities,
        "risks": risks,
    }


def format_ratio(value: Optional[float]) -> str:
    if value is None:
        return "unknown"
    return f"{value:.2f}x baseline"


def render_account_state(meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> str:
    state = account_state_summary(posts)
    top_clusters = ", ".join(f"{k} ({v})" for k, v in state["cluster_counts"].most_common(5)) or "unknown"
    lines = [
        "# Account State",
        "",
        "> Three-axis diagnosis for low-token runs. Algorithm red lines and positive signals remain the source of truth.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
        "## Output Language",
        "- Mirror the user's language in the current run.",
        "- If the user writes in Chinese, avoid unnecessary English jargon and explain internal IDs in Chinese the first time.",
        "- If the user writes in English, normal English professional terms are fine; still explain AK-specific IDs the first time.",
        "",
        "## Axis 1: Algorithm State",
        f"- Recent posts checked: {state['recent_count']}",
        f"- Recent reach vs baseline: {format_ratio(state['view_ratio'])}",
        f"- Recent reply-rate vs baseline: {format_ratio(state['reply_ratio'])}",
        f"- Recent share-rate vs baseline: {format_ratio(state['share_ratio'])}",
        f"- Recent semantic clusters: {top_clusters}",
        f"- Freshness pressure count: {state['fatigue_count']}",
        "",
        "## Axis 2: Audience Psychology State",
        "- Read this axis through the quick psychology card: hook payoff, concrete experience, useful tension, and retellability.",
        "- Current priority should follow the S-targets below, not a generic content formula.",
        "",
        "## Axis 3: Anti-AI State",
        f"- Possible AI-tone pattern hits in recent window: {state['ai_hits']}",
        "- Treat this as a warning light, not a verdict. Verify against the actual post before making a strong claim.",
        "",
        "## Current Priority Signals",
    ]
    for label, signal_id, reason in state["priorities"][:5]:
        lines.append(f"- {signal_id}: {label} - {reason}")
    lines.append("")
    lines.append("## Current Risk Watch")
    if state["risks"]:
        for risk_id, label, reason in state["risks"][:5]:
            lines.append(f"- {risk_id}: {label} - {reason}")
    else:
        lines.append("- No obvious compiled red-line pressure. Still scan the actual draft before publishing.")
    lines.extend([
        "",
        "## Runtime Notes",
        "- This file guides `/topics`, `/draft`, `/analyze`, and `/review`; it does not override `knowledge/_shared/red-lines.md`.",
        "- Use tracker evidence before making a strong account-level claim.",
    ])
    return "\n".join(lines) + "\n"


def signal_memory_lines(posts: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    if len(posts) < 10:
        return {
            "algorithm": ["Data is not mature enough for stable algorithm signal memory."],
            "psychology": ["Data is not mature enough for stable psychology signal memory."],
            "anti_ai": ["Data is not mature enough for stable anti-AI signal memory."],
        }

    best = top_by_score(posts, 8)
    recent = recent_posts(posts, 10)
    best_clusters = Counter(semantic_cluster(p) or "uncategorized" for p in best)
    best_types = Counter(str(p.get("content_type") or "unknown") for p in best)
    high_reply_posts = sorted(posts, key=lambda p: replies(p), reverse=True)[:5]
    high_share_posts = sorted(posts, key=lambda p: shares(p), reverse=True)[:5]
    ai_light_posts = [p for p in best if ai_tone_hits(post_text(p)) == 0]
    ai_heavy_recent = [p for p in recent if ai_tone_hits(post_text(p)) >= 2]

    algorithm = []
    psychology = []
    anti_ai = []

    if best_clusters:
        cluster, count = best_clusters.most_common(1)[0]
        algorithm.append(f"Best weighted posts often come from `{cluster}` ({count}/8 top scored posts). Use S7 semantic consistency, but check S14 freshness before repeating it.")
    if high_share_posts and shares(high_share_posts[0]) > 0:
        ids = ", ".join(f"`{p.get('id')}`" for p in high_share_posts if shares(p) > 0) or "none"
        algorithm.append(f"Posts with share/repost evidence should anchor S1 DM-sharing checks: {ids}.")
    if originality_risk_count(recent):
        algorithm.append("Recent tracker originality-risk flags exist. Run R4 checks before using any similar angle.")

    if best_types:
        content_type, count = best_types.most_common(1)[0]
        psychology.append(f"`{content_type}` appears often among top scored posts ({count}/8). Treat it as a likely audience-fit signal, not a template.")
    if high_reply_posts and replies(high_reply_posts[0]) > 0:
        ids = ", ".join(f"`{p.get('id')}`" for p in high_reply_posts if replies(p) > 0) or "none"
        psychology.append(f"Deep-comment references should start from posts with real replies: {ids}. Look for concrete examples or useful disagreement before copying surface wording.")

    if ai_light_posts:
        ids = ", ".join(f"`{p.get('id')}`" for p in ai_light_posts[:5])
        anti_ai.append(f"Top posts with low compiled AI-tone hits: {ids}. Use them as voice texture anchors only after checking exact wording.")
    if ai_heavy_recent:
        ids = ", ".join(f"`{p.get('id')}`" for p in ai_heavy_recent[:5])
        anti_ai.append(f"Recent posts with higher possible AI-tone hits: {ids}. Verify before claiming AI tone, then reduce symmetry, generic phrasing, or over-complete explanation.")
    if not anti_ai:
        anti_ai.append("No strong compiled AI-tone pattern. Still run the AI-tone card on each actual draft.")

    return {"algorithm": algorithm, "psychology": psychology, "anti_ai": anti_ai}


def render_personal_signal_memory(meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> str:
    memory = signal_memory_lines(posts)
    lines = [
        "# Personal Signal Memory",
        "",
        "> Personal account signals only. This is not a case-study library and not a formula bank.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
        "## Algorithm Signals",
    ]
    lines.extend(f"- {line}" for line in memory["algorithm"])
    lines.append("")
    lines.append("## Audience Psychology Signals")
    lines.extend(f"- {line}" for line in memory["psychology"])
    lines.append("")
    lines.append("## Anti-AI Signals")
    lines.extend(f"- {line}" for line in memory["anti_ai"])
    lines.extend([
        "",
        "## Runtime Notes",
        "- These are compact signals, not universal advice.",
        "- If a signal lacks enough post IDs, downgrade confidence in the user-facing output.",
    ])
    return "\n".join(lines) + "\n"


MOVE_LIBRARY = [
    {
        "name": "補人格判斷",
        "primary_when": {"Anti-AI", "S8", "S2"},
        "algorithm_targets": ["S2 深留言觸發", "S3 停留時間", "S8 信任圖譜"],
        "avoid": ["R4 低原創性", "R10 未標示 AI 內容", "R12 軟風險疊加"],
        "use_when": "資訊量足夠，但人的判斷、限制、現場感偏少。",
        "good_for": "信任、自然留言、品牌記憶。",
        "texture": "用具體經驗、取捨、限制感來寫；不要寫成完整教學文。",
    },
    {
        "name": "澄清分歧",
        "primary_when": {"S2", "S7", "S9"},
        "algorithm_targets": ["S2 深留言觸發", "S7 語意鄰近一致", "S9 陌生人推薦性"],
        "avoid": ["R1 互動誘導", "R2 標題黨", "R7 敏感議題聳動化", "R8 負面回饋觸發", "R12 軟風險疊加"],
        "use_when": "需要提高討論密度，但不能靠吵架或釣留言。",
        "good_for": "高品質留言、觀點辨識度、可轉述的差異。",
        "texture": "提出真實區分，給理由與限制；不要煽動站隊。",
    },
    {
        "name": "擴散型實用觀點",
        "primary_when": {"S1", "S3", "S9", "S14"},
        "algorithm_targets": ["S1 私下分享潛力", "S3 停留時間", "S9 陌生人推薦性", "S14 題材新鮮度"],
        "avoid": ["R3 開頭與內文不一致", "R4 低原創性", "R5 連續同題材", "R6 低品質外部連結", "R9 主題混雜"],
        "use_when": "需要讓非粉也能一眼理解價值，且題材還有新鮮度。",
        "good_for": "收藏、分享、非粉觸及。",
        "texture": "讓陌生人能轉述一句重點；避免 AI checklist 或工具清單感。",
    },
]


def render_next_move_queue(meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> str:
    state = account_state_summary(posts)
    priority_ids = {signal_id for _, signal_id, _ in state["priorities"]}
    ordered = sorted(
        MOVE_LIBRARY,
        key=lambda move: 0 if move["primary_when"] & priority_ids else 1,
    )
    lines = [
        "# Next Move Queue",
        "",
        "> Generated from the account state. A move is allowed only when it names S-targets and R-risks.",
        "",
        "```yaml",
        markdown_meta(meta).rstrip(),
        "```",
        "",
        "## Required Gate",
        "- First scan hard red lines from `knowledge/_shared/red-lines.md`.",
        "- Then choose the S signal this post should strengthen.",
        "- Finally adjust psychology and anti-AI texture.",
        "- Mirror the user's language. Explain AK-specific IDs the first time, such as `S2` meaning deep-comment trigger.",
        "",
    ]
    for index, move in enumerate(ordered[:3], start=1):
        lines.extend([
            f"## Move {index}: {move['name']}",
            f"- Algorithm Target: {', '.join(move['algorithm_targets'])}",
            f"- Must Avoid: {', '.join(move['avoid'])}",
            f"- Use When: {move['use_when']}",
            f"- Good For: {move['good_for']}",
            f"- Human Texture: {move['texture']}",
            "",
        ])
    lines.extend([
        "## Runtime Notes",
        "- Do not call these formulas.",
        "- Do not promise virality.",
        "- If the user asks why, cite the R/S rule and the account-state evidence.",
    ])
    return "\n".join(lines) + "\n"


def write_jsonl(path: Path, meta: Dict[str, Any], posts: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"_meta": meta}, ensure_ascii=False) + "\n")
        for post in sorted(posts, key=sort_key, reverse=True):
            fh.write(json.dumps(post_feature_row(post), ensure_ascii=False) + "\n")


def write_outputs(tracker_path: Path, output_dir: Path) -> None:
    tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
    posts = tracker.get("posts") or []
    output_dir.mkdir(parents=True, exist_ok=True)
    meta = shared_meta(tracker_path, posts)

    (output_dir / "account_wiki.md").write_text(render_account_wiki(meta, posts), encoding="utf-8", newline="\n")
    (output_dir / "account_state.md").write_text(render_account_state(meta, posts), encoding="utf-8", newline="\n")
    (output_dir / "personal_signal_memory.md").write_text(render_personal_signal_memory(meta, posts), encoding="utf-8", newline="\n")
    (output_dir / "next_move_queue.md").write_text(render_next_move_queue(meta, posts), encoding="utf-8", newline="\n")
    write_jsonl(output_dir / "post_feature_index.jsonl", meta, posts)
    (output_dir / "cluster_wiki.json").write_text(
        json.dumps(build_cluster_wiki(meta, posts), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "exemplar_bank.md").write_text(render_exemplar_bank(meta, posts), encoding="utf-8", newline="\n")
    (output_dir / "recent_window.md").write_text(render_recent_window(meta, posts), encoding="utf-8", newline="\n")
    write_voice_outputs(tracker_path, output_dir)


def main() -> int:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(description="Build low-token compiled memory from a Threads tracker.")
    parser.add_argument("--tracker", required=True, help="Path to threads_daily_tracker.json")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to ./compiled beside tracker.")
    args = parser.parse_args()

    tracker_path = Path(args.tracker).resolve()
    if not tracker_path.exists():
        raise SystemExit(f"Tracker not found: {tracker_path}")
    output_dir = Path(args.output_dir).resolve() if args.output_dir else tracker_path.parent / "compiled"
    write_outputs(tracker_path, output_dir)
    print(f"Compiled memory written to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
