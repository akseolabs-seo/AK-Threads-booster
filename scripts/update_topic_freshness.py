#!/usr/bin/env python3
"""
AK-Threads-Booster: Build semantic clusters and annotate topic freshness.

Usage:
    python update_topic_freshness.py --tracker threads_daily_tracker.json
    python update_topic_freshness.py --tracker threads_daily_tracker.json --recent-post-window 10 --recent-day-window 30

The script:
    - reads an existing tracker JSON file
    - builds lightweight semantic clusters from historical post text
    - assigns each post a semantic_cluster label
    - estimates topic freshness and fatigue risk from prior similar posts
    - writes results into `algorithm_signals.topic_freshness`
"""

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


WORD_RE = re.compile(r"[a-z0-9][a-z0-9_+-]{1,}")
URL_RE = re.compile(r"https?://\S+")
MENTION_RE = re.compile(r"@\w+")
HASHTAG_RE = re.compile(r"#(\w+)")
NON_WORD_RE = re.compile(r"[^\w\s\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0e00-\u0e7f]+")

EN_STOPWORDS = {
    "the", "and", "for", "that", "this", "with", "from", "your", "have", "just",
    "they", "them", "then", "than", "what", "when", "will", "into", "about", "would",
    "there", "their", "because", "while", "which", "where", "been", "were", "being",
    "also", "more", "most", "really", "very", "much", "some", "only", "like", "still",
    "dont", "does", "did", "you", "are", "was", "its", "not", "can", "all", "but",
    "why", "how", "who", "our", "out", "too", "got", "get", "had", "has", "use",
    "using", "used", "make", "made", "than", "want", "need", "post", "thread", "threads",
}


def load_tracker(tracker_path: str) -> dict:
    path = Path(tracker_path)
    if not path.exists():
        print(f"Error: tracker not found at {tracker_path}")
        sys.exit(1)

    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_tracker(tracker_path: str, tracker: dict) -> None:
    with open(tracker_path, "w", encoding="utf-8") as fh:
        json.dump(tracker, fh, ensure_ascii=False, indent=2)


def parse_iso_datetime(timestamp: str) -> Optional[datetime]:
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_text(text: str) -> str:
    text = URL_RE.sub(" ", text or "")
    text = MENTION_RE.sub(" ", text)
    text = HASHTAG_RE.sub(r" \1 ", text)
    text = text.lower()
    text = NON_WORD_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_word_tokens(text: str) -> List[str]:
    tokens = []
    for token in WORD_RE.findall(normalize_text(text)):
        if token in EN_STOPWORDS:
            continue
        if token.isdigit():
            continue
        tokens.append(token)
    return tokens


def is_non_ascii_letter(ch: str) -> bool:
    return (
        "\u4e00" <= ch <= "\u9fff"
        or "\u3040" <= ch <= "\u30ff"
        or "\uac00" <= ch <= "\ud7af"
        or "\u0e00" <= ch <= "\u0e7f"
    )


def extract_char_ngrams(text: str, min_n: int = 2, max_n: int = 3) -> List[str]:
    compact = "".join(ch for ch in normalize_text(text) if is_non_ascii_letter(ch))
    ngrams: List[str] = []
    for n in range(min_n, max_n + 1):
        if len(compact) < n:
            continue
        for idx in range(len(compact) - n + 1):
            ngrams.append(compact[idx: idx + n])
    return ngrams


def jaccard(a: Sequence[str], b: Sequence[str]) -> float:
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def build_semantic_features(post: dict) -> dict:
    text = post.get("text", "")
    topics = [str(topic).strip().lower() for topic in post.get("topics", []) if str(topic).strip()]
    return {
        "words": extract_word_tokens(text),
        "char_ngrams": extract_char_ngrams(text),
        "topics": topics,
        "content_type": str(post.get("content_type", "") or "").lower(),
    }


def semantic_similarity(left: dict, right: dict) -> float:
    word_score = jaccard(left["words"], right["words"])
    char_score = jaccard(left["char_ngrams"], right["char_ngrams"])
    topic_inputs_left = list(left["topics"])
    topic_inputs_right = list(right["topics"])
    if left["content_type"]:
        topic_inputs_left.append(f"ct:{left['content_type']}")
    if right["content_type"]:
        topic_inputs_right.append(f"ct:{right['content_type']}")
    topic_score = jaccard(topic_inputs_left, topic_inputs_right)
    return (0.5 * word_score) + (0.3 * char_score) + (0.2 * topic_score)


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: int, right: int) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            self.parent[root_left] = root_right
        elif self.rank[root_left] > self.rank[root_right]:
            self.parent[root_right] = root_left
        else:
            self.parent[root_right] = root_left
            self.rank[root_left] += 1


def build_clusters(posts: List[dict], features: List[dict], threshold: float) -> Tuple[Dict[int, List[int]], Dict[Tuple[int, int], float]]:
    uf = UnionFind(len(posts))
    pair_scores: Dict[Tuple[int, int], float] = {}

    for left_idx in range(len(posts)):
        for right_idx in range(left_idx + 1, len(posts)):
            score = semantic_similarity(features[left_idx], features[right_idx])
            pair_scores[(left_idx, right_idx)] = score
            if score >= threshold:
                uf.union(left_idx, right_idx)

    clusters: Dict[int, List[int]] = defaultdict(list)
    for idx in range(len(posts)):
        clusters[uf.find(idx)].append(idx)

    return clusters, pair_scores


def best_cluster_label(cluster_posts: List[dict], cluster_features: List[dict], cluster_id: int) -> str:
    topic_counts = Counter()
    word_counts = Counter()

    for post, features in zip(cluster_posts, cluster_features):
        for topic in post.get("topics", []):
            topic = str(topic).strip().lower()
            if topic:
                topic_counts[topic] += 3
        for token in features["words"]:
            if len(token) < 3:
                continue
            word_counts[token] += 1

    if topic_counts:
        top_topics = [token for token, _ in topic_counts.most_common(2)]
        return " / ".join(top_topics)
    if word_counts:
        top_words = [token for token, _ in word_counts.most_common(2)]
        return " / ".join(top_words)
    return f"cluster-{cluster_id:03d}"


def fatigue_risk_from_score(score: float) -> str:
    if score >= 75:
        return "low"
    if score >= 45:
        return "medium"
    return "high"


def freshness_score(similar_recent_posts: int, recent_cluster_frequency: int, days_since_last: Optional[float]) -> int:
    score = 100
    score -= min(similar_recent_posts * 18, 54)
    score -= min(recent_cluster_frequency * 8, 24)

    if days_since_last is not None:
        if days_since_last <= 3:
            score -= 25
        elif days_since_last <= 7:
            score -= 18
        elif days_since_last <= 14:
            score -= 10
        elif days_since_last <= 30:
            score -= 5

    return max(0, min(100, score))


def infer_timeline(posts: List[dict]) -> List[Tuple[int, Optional[datetime]]]:
    dated = []
    undated = []

    for idx, post in enumerate(posts):
        parsed = parse_iso_datetime(str(post.get("created_at", "")))
        if parsed is None:
            undated.append((idx, None))
        else:
            dated.append((idx, parsed))

    dated.sort(key=lambda item: item[1] or datetime.min.replace(tzinfo=timezone.utc))
    # Assume tracker default order is newest-first; append undated posts in reverse index so older posts come first.
    undated.sort(key=lambda item: item[0], reverse=True)
    return dated + undated


def annotate_topic_freshness(
    posts: List[dict],
    clusters: Dict[int, List[int]],
    cluster_labels: Dict[int, str],
    recent_post_window: int,
    recent_day_window: int,
) -> None:
    timeline = infer_timeline(posts)
    prior_by_cluster: Dict[int, List[Tuple[int, Optional[datetime]]]] = defaultdict(list)

    cluster_for_post = {}
    for cluster_id, post_indexes in clusters.items():
        for post_idx in post_indexes:
            cluster_for_post[post_idx] = cluster_id

    for order_idx, (post_idx, created_at) in enumerate(timeline):
        cluster_id = cluster_for_post[post_idx]
        cluster_posts = prior_by_cluster[cluster_id]

        recent_window_start = max(0, order_idx - recent_post_window)
        recent_post_ids = {idx for idx, _ in timeline[recent_window_start:order_idx]}
        similar_recent_posts = sum(1 for idx, _ in cluster_posts if idx in recent_post_ids)

        recent_cluster_frequency = 0
        days_since_last_similar_post = None
        if created_at is not None:
            similar_dates = [dt for _, dt in cluster_posts if dt is not None]
            if similar_dates:
                last_similar = max(similar_dates)
                days_since_last_similar_post = round((created_at - last_similar).total_seconds() / 86400, 2)
            window_seconds = recent_day_window * 86400
            for _, prior_dt in cluster_posts:
                if prior_dt is None:
                    continue
                if 0 <= (created_at - prior_dt).total_seconds() <= window_seconds:
                    recent_cluster_frequency += 1
        else:
            recent_cluster_frequency = min(len(cluster_posts), recent_post_window)

        score = freshness_score(
            similar_recent_posts=similar_recent_posts,
            recent_cluster_frequency=recent_cluster_frequency,
            days_since_last=days_since_last_similar_post,
        )

        post = posts[post_idx]
        algorithm_signals = post.setdefault("algorithm_signals", {})
        freshness = algorithm_signals.setdefault("topic_freshness", {})
        freshness["semantic_cluster"] = cluster_labels[cluster_id]
        freshness["similar_recent_posts"] = similar_recent_posts
        freshness["recent_cluster_frequency"] = recent_cluster_frequency
        freshness["days_since_last_similar_post"] = days_since_last_similar_post
        freshness["freshness_score"] = score
        freshness["fatigue_risk"] = fatigue_risk_from_score(score)

        prior_by_cluster[cluster_id].append((post_idx, created_at))


def summarize_clusters(clusters: Dict[int, List[int]], cluster_labels: Dict[int, str]) -> List[str]:
    rows = []
    for cluster_id, members in sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True):
        rows.append(f"{cluster_labels[cluster_id]} ({len(members)} posts)")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build semantic clusters and annotate topic freshness in the tracker"
    )
    parser.add_argument(
        "--tracker",
        default="threads_daily_tracker.json",
        help="Path to the tracker JSON file",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.24,
        help="Similarity threshold for semantic clustering (default: 0.24)",
    )
    parser.add_argument(
        "--recent-post-window",
        type=int,
        default=10,
        help="How many recent posts count toward freshness decay (default: 10)",
    )
    parser.add_argument(
        "--recent-day-window",
        type=int,
        default=30,
        help="How many trailing days count toward cluster frequency (default: 30)",
    )
    args = parser.parse_args()

    tracker = load_tracker(args.tracker)
    posts = tracker.get("posts", [])
    if not isinstance(posts, list) or not posts:
        print("Error: tracker contains no posts to cluster")
        sys.exit(1)

    features = [build_semantic_features(post) for post in posts]
    clusters, _ = build_clusters(posts, features, args.similarity_threshold)

    cluster_labels = {}
    for cluster_id, member_indexes in clusters.items():
        cluster_posts = [posts[idx] for idx in member_indexes]
        cluster_features = [features[idx] for idx in member_indexes]
        cluster_labels[cluster_id] = best_cluster_label(cluster_posts, cluster_features, cluster_id)

    annotate_topic_freshness(
        posts=posts,
        clusters=clusters,
        cluster_labels=cluster_labels,
        recent_post_window=args.recent_post_window,
        recent_day_window=args.recent_day_window,
    )

    tracker["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_tracker(args.tracker, tracker)

    print(f"Done. Updated topic freshness for {len(posts)} posts in {args.tracker}")
    print("Largest semantic clusters:")
    for row in summarize_clusters(clusters, cluster_labels)[:10]:
        print(f"  - {row}")


if __name__ == "__main__":
    main()
