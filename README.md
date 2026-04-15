# Summarizer Ai

> By [MEOK AI Labs](https://meok.ai) — Text summarization and extraction by MEOK AI Labs.

Text summarization and key-point extraction — MEOK AI Labs.

## Installation

```bash
pip install summarizer-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install summarizer-ai-mcp
```

## Tools

### `summarize_text`
Summarize text by extracting the most important sentences.

**Parameters:**
- `text` (str)
- `sentences` (int)

### `extract_key_points`
Extract key points from text as bullet points.

**Parameters:**
- `text` (str)
- `max_points` (int)

### `generate_abstract`
Generate a concise abstract from longer text.

**Parameters:**
- `text` (str)
- `max_words` (int)

### `compare_summaries`
Compare two texts by their key terms and structural similarity.

**Parameters:**
- `text_a` (str)
- `text_b` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/summarizer-ai-mcp](https://github.com/CSOAI-ORG/summarizer-ai-mcp)
- **PyPI**: [pypi.org/project/summarizer-ai-mcp](https://pypi.org/project/summarizer-ai-mcp/)

## License

MIT — MEOK AI Labs
