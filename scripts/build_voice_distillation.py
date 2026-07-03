#!/usr/bin/env python3
"""
AK-Threads-Booster: Build deterministic voice fingerprint files from a tracker.

Usage:
    python scripts/build_voice_distillation.py --tracker threads_daily_tracker.json
    python scripts/build_voice_distillation.py --tracker threads_daily_tracker.json --output-dir compiled

Outputs:
    compiled/voice_fingerprint.json
    compiled/voice_fingerprint.md

The tracker remains the source of truth. These files are derived runtime caches
for `/voice` and `/draft`; they provide statistics and source anchors, not final
brand-voice interpretation.
"""

import argparse
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


WORD_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0e00-\u0e7f]+")
SENTENCE_RE = re.compile(r"[^。！？!?.\n]+[。！？!?.]?")
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
    "]+",
    flags=re.UNICODE,
)

TEXT_FIELDS = ("text", "caption", "content", "body", "desc", "message")

JUDGMENT_MARKERS = [
    "我覺得",
    "我觉得",
    "我認為",
    "我认为",
    "我相信",
    "說白了",
    "说白了",
    "老實說",
    "老实说",
    "坦白說",
    "坦白说",
    "其實",
    "其实",
    "本質",
    "本质",
    "真正",
    "不是",
    "而是",
    "不只是",
    "不要",
    "不能",
    "應該",
    "应该",
    "必須",
    "必须",
    "最好",
    "honestly",
    "to be honest",
    "i think",
    "i believe",
    "the point is",
    "the key is",
]

AI_TEMPLATE_PATTERNS = [
    "總結來說",
    "总结来说",
    "綜上所述",
    "综上所述",
    "在這個快速變化的時代",
    "在这个快速变化的时代",
    "不僅如此",
    "不仅如此",
    "更重要的是",
    "moreover",
    "furthermore",
    "in today's world",
    "ultimately",
]

TRANSITION_CANDIDATES = [
    "但",
    "但是",
    "可是",
    "所以",
    "因為",
    "因为",
    "然後",
    "然后",
    "其實",
    "其实",
    "說真的",
    "说真的",
    "老實說",
    "老实说",
    "換句話說",
    "换句话说",
    "反過來說",
    "反过来说",
    "問題是",
    "问题是",
    "重點是",
    "重点是",
    "anyway",
    "honestly",
    "but",
    "so",
    "because",
]


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
    return parse_iso(str(post.get("created_at") or "")) or datetime.min.replace(tzinfo=timezone.utc)


def tracker_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def summarize_text(text: str, limit: int = 140) -> str:
    compact = compact_space(text)
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "..."


def post_text(post: Dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = post.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def metric(post: Dict[str, Any], name: str) -> int:
    metrics = post.get("metrics") if isinstance(post.get("metrics"), dict) else {}
    candidates = [
        metrics.get(name),
        post.get(name),
        post.get(f"{name}_count"),
    ]
    if name == "replies":
        candidates.extend([metrics.get("comments"), post.get("comments_count"), post.get("comment_count")])
    if name == "shares":
        candidates.extend([metrics.get("reposts"), post.get("reposts"), post.get("repost_count")])
    for value in candidates:
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return 0


def engagement_score(post: Dict[str, Any]) -> int:
    return (
        metric(post, "views")
        + metric(post, "likes") * 5
        + metric(post, "replies") * 30
        + metric(post, "shares") * 50
    )


def word_tokens(text: str) -> List[str]:
    return [token.lower() for token in WORD_RE.findall(text) if token.strip()]


def word_count(text: str) -> int:
    return len(word_tokens(text))


def split_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text.strip()) if p.strip()]


def split_sentences(text: str) -> List[str]:
    sentences = [m.group(0).strip() for m in SENTENCE_RE.finditer(text) if m.group(0).strip()]
    return sentences or ([text.strip()] if text.strip() else [])


def percentile(values: List[int], pct: float) -> Optional[float]:
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return float(values[0])
    position = (len(values) - 1) * pct
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return float(values[low])
    return values[low] + (values[high] - values[low]) * (position - low)


def stable_mean(values: Iterable[int]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return round(float(statistics.mean(clean)), 2)


def phase_name(index: int) -> str:
    return ("early", "middle", "recent")[index]


def top_engagement_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not posts:
        return []
    limit = max(3, math.ceil(len(posts) * 0.2))
    limit = min(limit, 25)
    return sorted(posts, key=engagement_score, reverse=True)[:limit]


def phase_posts(posts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    ordered = sorted(posts, key=sort_key)
    if not ordered:
        return {"early": [], "middle": [], "recent": []}
    phases = {"early": [], "middle": [], "recent": []}
    for idx, post in enumerate(ordered):
        bucket = min(2, int(idx * 3 / len(ordered)))
        phases[phase_name(bucket)].append(post)
    return phases


def classify_opening(text: str) -> str:
    first = split_sentences(text)[0] if text.strip() else ""
    lowered = first.lower()
    if "?" in first or "？" in first:
        return "question_opening"
    if re.search(r"\b\d+|\d+\b|[一二三四五六七八九十]+個|[一二三四五六七八九十]+个", first):
        return "number_or_result_opening"
    if any(marker in lowered for marker in ("我", "最近", "昨天", "today", "i ")):
        return "personal_experience_opening"
    if any(marker in first for marker in ("不是", "不只是", "其實", "其实", "說白了", "说白了")):
        return "judgment_or_contrast_opening"
    if any(marker in lowered for marker in ("how to", "怎麼", "怎么", "如何")):
        return "how_to_opening"
    return "direct_statement_opening"


def classify_ending(text: str) -> str:
    last = split_sentences(text)[-1] if text.strip() else ""
    lowered = last.lower()
    if "?" in last or "？" in last:
        return "question_ending"
    if any(marker in last for marker in ("留言", "告訴我", "告诉我", "分享", "你覺得", "你觉得")):
        return "explicit_cta_ending"
    if any(marker in last for marker in ("不要", "別", "别", "記得", "记得", "可以先", "試試", "试试")):
        return "action_advice_ending"
    if any(marker in last for marker in ("。", ".", "！", "!")) and len(last) <= 28:
        return "clean_cut_ending"
    if any(marker in lowered for marker in ("honestly", "anyway", "that's it")):
        return "personal_aside_ending"
    return "soft_landing_ending"


def pattern_inventory(posts: List[Dict[str, Any]], classifier, label: str) -> List[Dict[str, Any]]:
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    high_ids = {p.get("id") for p in top_engagement_posts(posts)}
    for post in posts:
        text = post_text(post)
        if not text:
            continue
        buckets[classifier(text)].append(post)
    inventory = []
    for pattern, bucket in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])):
        best = sorted(bucket, key=engagement_score, reverse=True)[:3]
        inventory.append({
            "pattern": pattern,
            "count": len(bucket),
            "high_engagement_count": sum(1 for post in bucket if post.get("id") in high_ids),
            "examples": [
                {
                    "id": post.get("id"),
                    "score": engagement_score(post),
                    "excerpt": summarize_text(post_text(post), 120),
                }
                for post in best
            ],
            "label": label,
        })
    return inventory


def top_counter(counter: Counter, limit: int = 20) -> List[Dict[str, Any]]:
    return [{"value": key, "count": value} for key, value in counter.most_common(limit)]


def phrase_inventory(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    openers = Counter()
    closers = Counter()
    transitions = Counter()
    tokens = Counter()
    emoji = Counter()
    punctuation = Counter()
    code_switch_posts = 0
    posts_with_emoji = 0
    for post in posts:
        text = post_text(post)
        if not text:
            continue
        compact = compact_space(text)
        openers[compact[:18]] += 1
        closers[compact[-18:]] += 1
        for candidate in TRANSITION_CANDIDATES:
            count = text.lower().count(candidate.lower())
            if count:
                transitions[candidate] += count
        for token in word_tokens(text):
            if len(token) >= 2:
                tokens[token] += 1
        emojis = EMOJI_RE.findall(text)
        if emojis:
            posts_with_emoji += 1
        for chunk in emojis:
            for char in chunk:
                emoji[char] += 1
        if re.search(r"[A-Za-z]{3,}", text) and re.search(r"[\u4e00-\u9fff]", text):
            code_switch_posts += 1
        for mark in ("?", "？", "!", "！", "...", "…", "(", ")", "（", "）", ":", "："):
            punctuation[mark] += text.count(mark)
    return {
        "openers": top_counter(openers, 15),
        "closers": top_counter(closers, 15),
        "transition_words": top_counter(transitions, 20),
        "content_words": top_counter(tokens, 30),
        "emoji_usage": {
            "posts_with_emoji": posts_with_emoji,
            "usage_pct": round(posts_with_emoji / max(len(posts), 1) * 100, 1),
            "top_emoji": top_counter(emoji, 15),
        },
        "punctuation": top_counter(punctuation, 20),
        "code_switching": {
            "posts_with_mixed_latin_cjk": code_switch_posts,
            "usage_pct": round(code_switch_posts / max(len(posts), 1) * 100, 1),
        },
    }


def rhythm_stats(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    word_counts = []
    paragraph_counts = []
    sentence_counts = []
    first_sentence_lengths = []
    single_line_paragraphs = 0
    total_paragraphs = 0
    for post in posts:
        text = post_text(post)
        if not text:
            continue
        paragraphs = split_paragraphs(text)
        sentences = split_sentences(text)
        word_counts.append(word_count(text))
        paragraph_counts.append(len(paragraphs))
        sentence_counts.append(len(sentences))
        if sentences:
            first_sentence_lengths.append(word_count(sentences[0]))
        for paragraph in paragraphs:
            total_paragraphs += 1
            if "\n" not in paragraph and len(paragraph) <= 70:
                single_line_paragraphs += 1
    return {
        "word_count": {
            "avg": stable_mean(word_counts),
            "p25": percentile(word_counts, 0.25),
            "p50": percentile(word_counts, 0.5),
            "p75": percentile(word_counts, 0.75),
        },
        "paragraph_count_avg": stable_mean(paragraph_counts),
        "sentence_count_avg": stable_mean(sentence_counts),
        "first_sentence_word_count_avg": stable_mean(first_sentence_lengths),
        "single_line_paragraph_ratio": round(single_line_paragraphs / max(total_paragraphs, 1), 3),
    }


def extract_user_replies(post: Dict[str, Any]) -> List[str]:
    replies = []
    raw_comments = []
    for field in ("comments", "comment_list", "replies", "comment_replies"):
        value = post.get(field)
        if isinstance(value, list):
            raw_comments.extend(value)
    for comment in raw_comments:
        if isinstance(comment, str):
            replies.append(comment.strip())
            continue
        if not isinstance(comment, dict):
            continue
        is_author = any(
            bool(comment.get(flag))
            for flag in ("is_author", "is_user", "author_reply", "from_owner", "from_self")
        )
        text = ""
        for field in TEXT_FIELDS:
            value = comment.get(field)
            if isinstance(value, str) and value.strip():
                text = value.strip()
                break
        if is_author and text:
            replies.append(text)
    return replies


def comment_reply_stats(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    replies = []
    for post in posts:
        replies.extend(extract_user_replies(post))
    return {
        "reply_count": len(replies),
        "avg_reply_word_count": stable_mean(word_count(reply) for reply in replies),
        "sample_replies": [summarize_text(reply, 120) for reply in replies[:10]],
    }


def belief_candidates(posts: List[Dict[str, Any]], limit: int = 80) -> List[Dict[str, Any]]:
    candidates = []
    for post in posts:
        text = post_text(post)
        if not text:
            continue
        for sentence in split_sentences(text):
            lowered = sentence.lower()
            markers = [marker for marker in JUDGMENT_MARKERS if marker.lower() in lowered]
            if not markers:
                continue
            if len(sentence) < 8:
                continue
            candidates.append({
                "id": post.get("id"),
                "created_at": post.get("created_at"),
                "score": engagement_score(post),
                "markers": markers[:5],
                "sentence": sentence[:240],
                "post_excerpt": summarize_text(text, 120),
            })
    return sorted(candidates, key=lambda row: row["score"], reverse=True)[:limit]


def anti_voice_candidates(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    text = "\n".join(post_text(post) for post in posts)
    total = len(posts)
    rows = []
    for pattern in AI_TEMPLATE_PATTERNS:
        count = text.lower().count(pattern.lower())
        if count <= max(1, math.floor(total * 0.02)):
            rows.append({
                "pattern": pattern,
                "observed_count": count,
                "candidate_rule": "Treat as possible not-me phrasing; verify in Manual Refinements before making it a hard rule.",
            })
    return rows


def temporal_shift(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    phases = phase_posts(posts)
    result = {}
    for name, bucket in phases.items():
        openings = pattern_inventory(bucket, classify_opening, "opening")
        endings = pattern_inventory(bucket, classify_ending, "ending")
        result[name] = {
            "post_count": len(bucket),
            "top_opening": openings[0]["pattern"] if openings else None,
            "top_ending": endings[0]["pattern"] if endings else None,
            "rhythm": rhythm_stats(bucket),
            "engagement_median": percentile([engagement_score(post) for post in bucket], 0.5),
        }
    stable = []
    for key in ("top_opening", "top_ending"):
        values = [result[name].get(key) for name in ("early", "middle", "recent") if result[name].get(key)]
        if values and len(set(values)) == 1:
            stable.append({"feature": key, "value": values[0]})
    return {"phases": result, "stable_signals": stable}


def calibration_pairs(posts: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    pairs = []
    for post in top_engagement_posts(posts)[:limit]:
        text = post_text(post)
        if not text:
            continue
        pairs.append({
            "id": post.get("id"),
            "score": engagement_score(post),
            "good_version_anchor": summarize_text(text, 280),
            "bad_version_prompt": (
                "Generate a deliberately generic AI-ish version of this same idea, then explain why the original "
                "sounds closer to the user. Do not use the bad version for drafting."
            ),
        })
    return pairs


def load_posts(tracker_path: Path) -> List[Dict[str, Any]]:
    tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
    if isinstance(tracker, list):
        posts = tracker
    else:
        posts = tracker.get("posts") or tracker.get("items") or []
    return [post for post in posts if isinstance(post, dict)]


def shared_meta(tracker_path: Path, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    text_count = sum(1 for post in posts if post_text(post))
    metric_count = sum(1 for post in posts if engagement_score(post) > 0)
    return {
        "schema_version": "2.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_tracker": tracker_path.name,
        "source_tracker_hash": tracker_hash(tracker_path),
        "posts_count": len(posts),
        "posts_with_text": text_count,
        "posts_with_engagement": metric_count,
        "coverage_notes": "Derived voice fingerprint. Tracker remains source of truth; `/voice` must verify important claims against original posts.",
    }


def build_voice_fingerprint(tracker_path: Path) -> Dict[str, Any]:
    posts = load_posts(tracker_path)
    high_posts = top_engagement_posts(posts)
    high_ids = {post.get("id") for post in high_posts}
    return {
        "_meta": shared_meta(tracker_path, posts),
        "reason_strip_when": {
            "reason": "Moves deterministic voice-pattern extraction out of `/voice` so the model spends judgment on interpretation, not counting.",
            "strip_when": "Tracker storage supports cheap, reliable queries for engagement-weighted style features with source provenance.",
        },
        "engagement_model": {
            "formula": "views + likes*5 + replies*30 + shares/reposts*50",
            "top_corpus_rule": "top 20 percent by score, min 3 and max 25 posts",
            "top_post_ids": [post.get("id") for post in high_posts if post.get("id")],
        },
        "voice_fingerprint": {
            "all_posts": {
                "rhythm": rhythm_stats(posts),
                "opening_inventory": pattern_inventory(posts, classify_opening, "opening"),
                "ending_inventory": pattern_inventory(posts, classify_ending, "ending"),
                "phrases": phrase_inventory(posts),
                "comment_replies": comment_reply_stats(posts),
            },
            "high_engagement_posts": {
                "rhythm": rhythm_stats(high_posts),
                "opening_inventory": pattern_inventory(high_posts, classify_opening, "opening"),
                "ending_inventory": pattern_inventory(high_posts, classify_ending, "ending"),
                "phrases": phrase_inventory(high_posts),
            },
        },
        "temporal_shift": temporal_shift(posts),
        "cognitive_layer_seed": {
            "belief_candidate_sentences": belief_candidates(posts),
            "high_engagement_belief_candidate_sentences": belief_candidates(high_posts, limit=40),
            "instruction": "Use these as candidates only. `/voice` must group them into core beliefs, tensions, and judgment frames with original evidence.",
        },
        "anti_voice_seed": {
            "candidate_not_me_phrases": anti_voice_candidates(posts),
            "instruction": "These are absence or low-frequency signals, not hard taboos until the user confirms or evidence is strong.",
        },
        "draft_quick_reference_seed": {
            "top_opening_formulas": pattern_inventory(high_posts, classify_opening, "opening")[:5],
            "top_ending_formulas": pattern_inventory(high_posts, classify_ending, "ending")[:5],
            "calibration_pairs": calibration_pairs(posts),
            "high_engagement_anchor_ids": [post.get("id") for post in high_posts if post.get("id")],
        },
        "source_excerpt_index": [
            {
                "id": post.get("id"),
                "created_at": post.get("created_at"),
                "score": engagement_score(post),
                "is_high_engagement": post.get("id") in high_ids,
                "excerpt": summarize_text(post_text(post), 220),
            }
            for post in sorted(posts, key=engagement_score, reverse=True)[:50]
            if post_text(post)
        ],
    }


def fmt_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def render_inventory_table(items: List[Dict[str, Any]]) -> List[str]:
    lines = ["| Pattern | Count | High-engagement count | Top evidence |", "|---|---:|---:|---|"]
    for item in items[:8]:
        example = item.get("examples", [{}])[0] if item.get("examples") else {}
        lines.append(
            f"| `{item['pattern']}` | {item['count']} | {item['high_engagement_count']} | "
            f"`{example.get('id', 'unknown')}`: {example.get('excerpt', '')} |"
        )
    return lines


def render_markdown(data: Dict[str, Any]) -> str:
    meta = data["_meta"]
    all_voice = data["voice_fingerprint"]["all_posts"]
    high_voice = data["voice_fingerprint"]["high_engagement_posts"]
    rhythm = all_voice["rhythm"]
    high_rhythm = high_voice["rhythm"]
    lines = [
        "# Voice Fingerprint",
        "",
        "> Deterministic runtime cache for `/voice` and `/draft`. Tracker remains the source of truth.",
        "",
        "```yaml",
        f"generated_at: {meta['generated_at']}",
        f"source_tracker_hash: {meta['source_tracker_hash']}",
        f"posts_count: {meta['posts_count']}",
        f"posts_with_text: {meta['posts_with_text']}",
        f"posts_with_engagement: {meta['posts_with_engagement']}",
        "```",
        "",
        "## Engagement-Weighted Corpus",
        f"- Formula: `{data['engagement_model']['formula']}`",
        f"- Top corpus rule: {data['engagement_model']['top_corpus_rule']}",
        f"- Top post IDs: {', '.join(f'`{pid}`' for pid in data['engagement_model']['top_post_ids']) or 'none'}",
        "",
        "## Rhythm Baseline",
        "| Scope | Avg words | P50 words | Avg paragraphs | Avg first sentence words | Single-line paragraph ratio |",
        "|---|---:|---:|---:|---:|---:|",
        (
            f"| All posts | {fmt_value(rhythm['word_count']['avg'])} | {fmt_value(rhythm['word_count']['p50'])} | "
            f"{fmt_value(rhythm['paragraph_count_avg'])} | {fmt_value(rhythm['first_sentence_word_count_avg'])} | "
            f"{fmt_value(rhythm['single_line_paragraph_ratio'])} |"
        ),
        (
            f"| High-engagement | {fmt_value(high_rhythm['word_count']['avg'])} | {fmt_value(high_rhythm['word_count']['p50'])} | "
            f"{fmt_value(high_rhythm['paragraph_count_avg'])} | {fmt_value(high_rhythm['first_sentence_word_count_avg'])} | "
            f"{fmt_value(high_rhythm['single_line_paragraph_ratio'])} |"
        ),
        "",
        "## Opening Inventory",
    ]
    lines.extend(render_inventory_table(all_voice["opening_inventory"]))
    lines.extend(["", "## Ending Inventory"])
    lines.extend(render_inventory_table(all_voice["ending_inventory"]))
    lines.extend(["", "## High-Engagement Opening Inventory"])
    lines.extend(render_inventory_table(high_voice["opening_inventory"]))
    lines.extend(["", "## Cognitive Layer Seed"])
    candidates = data["cognitive_layer_seed"]["high_engagement_belief_candidate_sentences"][:20]
    if candidates:
        lines.extend(["| Post | Score | Markers | Candidate sentence |", "|---|---:|---|---|"])
        for candidate in candidates:
            markers = ", ".join(candidate["markers"])
            lines.append(f"| `{candidate['id']}` | {candidate['score']} | {markers} | {candidate['sentence']} |")
    else:
        lines.append("- No belief candidates found by marker scan. `/voice` should extract manually from high-engagement source posts.")
    lines.extend(["", "## Temporal Shift"])
    phases = data["temporal_shift"]["phases"]
    lines.extend(["| Phase | Posts | Top opening | Top ending | Median score |", "|---|---:|---|---|---:|"])
    for name in ("early", "middle", "recent"):
        phase = phases[name]
        lines.append(
            f"| {name} | {phase['post_count']} | {phase.get('top_opening') or 'unknown'} | "
            f"{phase.get('top_ending') or 'unknown'} | {fmt_value(phase.get('engagement_median'))} |"
        )
    stable = data["temporal_shift"]["stable_signals"]
    if stable:
        lines.extend(["", "Stable signals:"])
        lines.extend(f"- `{item['feature']}` stayed `{item['value']}` across phases." for item in stable)
    lines.extend(["", "## Anti-Voice Seed"])
    for row in data["anti_voice_seed"]["candidate_not_me_phrases"][:12]:
        lines.append(f"- `{row['pattern']}` observed {row['observed_count']} times. {row['candidate_rule']}")
    lines.extend(["", "## /draft Quick-Reference Seed"])
    for pair in data["draft_quick_reference_seed"]["calibration_pairs"]:
        lines.extend([
            f"### Calibration Anchor `{pair['id']}`",
            f"- score: {pair['score']}",
            f"- good-version anchor: {pair['good_version_anchor']}",
            f"- bad-version task: {pair['bad_version_prompt']}",
            "",
        ])
    lines.extend([
        "## Runtime Notes",
        "- `/voice` should use this file as the first pass, then verify important claims against `threads_daily_tracker.json`.",
        "- High-engagement patterns are evidence anchors, not rules. If recent posts contradict them, mark the conflict.",
        "- Manual Refinements in `brand_voice.md` outrank every generated or compiled signal.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(tracker_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    data = build_voice_fingerprint(tracker_path)
    (output_dir / "voice_fingerprint.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "voice_fingerprint.md").write_text(
        render_markdown(data),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic voice fingerprint from a Threads tracker.")
    parser.add_argument("--tracker", required=True, help="Path to threads_daily_tracker.json")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to ./compiled beside tracker.")
    args = parser.parse_args()

    tracker_path = Path(args.tracker).resolve()
    if not tracker_path.exists():
        raise SystemExit(f"Tracker not found: {tracker_path}")
    output_dir = Path(args.output_dir).resolve() if args.output_dir else tracker_path.parent / "compiled"
    write_outputs(tracker_path, output_dir)
    print(f"Voice fingerprint written to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
