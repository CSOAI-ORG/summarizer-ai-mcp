#!/usr/bin/env python3
"""Text summarization and key-point extraction — MEOK AI Labs."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
import re
import math
from datetime import datetime, timezone
from collections import defaultdict, Counter
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)


def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now)
    return None


def _split_sentences(text: str) -> list:
    """Split text into sentences using regex."""
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in parts if s.strip()]


def _word_frequencies(text: str) -> Counter:
    """Calculate word frequencies excluding stop words."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "out", "off", "over", "under", "again", "further",
        "then", "once", "and", "but", "or", "nor", "not", "so", "yet", "both",
        "either", "neither", "each", "every", "all", "any", "few", "more",
        "most", "other", "some", "such", "no", "only", "own", "same", "than",
        "too", "very", "just", "because", "if", "when", "where", "how",
        "what", "which", "who", "whom", "this", "that", "these", "those",
        "i", "me", "my", "myself", "we", "our", "ours", "you", "your",
        "he", "him", "his", "she", "her", "it", "its", "they", "them", "their",
    }
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return Counter(w for w in words if w not in stop_words and len(w) > 2)


def _score_sentences(sentences: list, freq: Counter) -> list:
    """Score sentences by sum of word frequencies."""
    scored = []
    for i, sent in enumerate(sentences):
        words = re.findall(r'\b[a-z]+\b', sent.lower())
        score = sum(freq.get(w, 0) for w in words)
        if words:
            score /= len(words)
        scored.append((score, i, sent))
    return scored


mcp = FastMCP("summarizer-ai", instructions="Text summarization and extraction by MEOK AI Labs.")


@mcp.tool()
def summarize_text(text: str, sentences: int = 3, api_key: str = "") -> dict:
    """Summarize text by extracting the most important sentences."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    all_sents = _split_sentences(text)
    if not all_sents:
        return {"error": "No sentences found in input text."}

    freq = _word_frequencies(text)
    scored = _score_sentences(all_sents, freq)
    scored.sort(key=lambda x: x[0], reverse=True)
    top_indices = sorted([s[1] for s in scored[:sentences]])
    summary_sents = [all_sents[i] for i in top_indices]

    compression = round((1 - len(" ".join(summary_sents)) / max(len(text), 1)) * 100, 1)
    return {
        "summary": " ".join(summary_sents),
        "sentence_count": len(summary_sents),
        "original_sentences": len(all_sents),
        "original_length": len(text),
        "compressed_length": len(" ".join(summary_sents)),
        "compression_percent": compression,
    }


@mcp.tool()
def extract_key_points(text: str, max_points: int = 5, api_key: str = "") -> dict:
    """Extract key points from text as bullet points."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    all_sents = _split_sentences(text)
    if not all_sents:
        return {"error": "No content to extract from."}

    freq = _word_frequencies(text)
    scored = _score_sentences(all_sents, freq)
    scored.sort(key=lambda x: x[0], reverse=True)

    key_points = []
    for score, idx, sent in scored[:max_points]:
        clean = sent.strip().rstrip(".")
        key_points.append(clean)

    top_words = freq.most_common(10)
    topics = [w for w, _ in top_words[:5]]

    return {
        "key_points": key_points,
        "count": len(key_points),
        "detected_topics": topics,
        "source_length": len(text),
    }


@mcp.tool()
def generate_abstract(text: str, max_words: int = 100, api_key: str = "") -> dict:
    """Generate a concise abstract from longer text."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    all_sents = _split_sentences(text)
    if not all_sents:
        return {"error": "No content to abstract."}

    freq = _word_frequencies(text)
    scored = _score_sentences(all_sents, freq)
    scored.sort(key=lambda x: x[0], reverse=True)

    abstract_sents = []
    word_count = 0
    for score, idx, sent in scored:
        sent_words = len(sent.split())
        if word_count + sent_words > max_words:
            break
        abstract_sents.append((idx, sent))
        word_count += sent_words

    abstract_sents.sort(key=lambda x: x[0])
    abstract = " ".join(s for _, s in abstract_sents)

    return {
        "abstract": abstract,
        "word_count": word_count,
        "max_words": max_words,
        "sentences_used": len(abstract_sents),
        "total_sentences": len(all_sents),
    }


@mcp.tool()
def compare_summaries(text_a: str, text_b: str, api_key: str = "") -> dict:
    """Compare two texts by their key terms and structural similarity."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    freq_a = _word_frequencies(text_a)
    freq_b = _word_frequencies(text_b)

    words_a = set(freq_a.keys())
    words_b = set(freq_b.keys())

    shared = words_a & words_b
    only_a = words_a - words_b
    only_b = words_b - words_a

    union = words_a | words_b
    jaccard = round(len(shared) / max(len(union), 1), 4)

    cosine_num = sum(freq_a[w] * freq_b[w] for w in shared)
    mag_a = math.sqrt(sum(v ** 2 for v in freq_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in freq_b.values()))
    cosine_sim = round(cosine_num / max(mag_a * mag_b, 1e-9), 4)

    sents_a = _split_sentences(text_a)
    sents_b = _split_sentences(text_b)

    return {
        "jaccard_similarity": jaccard,
        "cosine_similarity": cosine_sim,
        "shared_terms": sorted(list(shared))[:20],
        "unique_to_a": sorted(list(only_a))[:10],
        "unique_to_b": sorted(list(only_b))[:10],
        "text_a_stats": {"sentences": len(sents_a), "chars": len(text_a), "unique_terms": len(words_a)},
        "text_b_stats": {"sentences": len(sents_b), "chars": len(text_b), "unique_terms": len(words_b)},
    }


if __name__ == "__main__":
    mcp.run()
