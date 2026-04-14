#!/usr/bin/env python3
import json
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("summarizer-ai-mcp")
@mcp.tool(name="summarize_text")
async def summarize_text(text: str, sentences: int = 2) -> str:
    sents = [s.strip() for s in text.split('.') if s.strip()]
    return json.dumps({"summary": '. '.join(sents[:sentences]) + '.', "original_length": len(text)})
@mcp.tool(name="bullet_points")
async def bullet_points(text: str) -> str:
    lines = [l.strip() for l in text.split('.') if l.strip()]
    return json.dumps({"bullets": [f"• {l}" for l in lines[:5]]})
if __name__ == "__main__":
    mcp.run()
