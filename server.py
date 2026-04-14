#!/usr/bin/env python3
"""Summarize long texts into key points. — MEOK AI Labs."""
import json, os, re, hashlib, uuid as _uuid, random
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit/day"})
    _usage[c].append(now); return None

mcp = FastMCP("summarizer", instructions="MEOK AI Labs — Summarize long texts into key points.")


@mcp.tool()
def summarize(text: str, max_sentences: int = 3) -> str:
    """Summarize text by extracting key sentences."""
    if err := _rl(): return err
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 10]
    scored = []
    words = text.lower().split()
    freq = defaultdict(int)
    for w in words: freq[w] += 1
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in s.split()) / max(len(s.split()), 1)
        scored.append((score, s))
    scored.sort(reverse=True)
    summary = ". ".join(s for _, s in scored[:max_sentences]) + "."
    return json.dumps({"summary": summary, "original_sentences": len(sentences), "summary_sentences": min(max_sentences, len(sentences))}, indent=2)

if __name__ == "__main__":
    mcp.run()
