#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("summarizer-ai-mcp")
@mcp.tool(name="summarize_text")
async def summarize_text(text: str, sentences: int = 2, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    sents = [s.strip() for s in text.split('.') if s.strip()]
    return {"summary": '. '.join(sents[:sentences]) + '.', "original_length": len(text)}
@mcp.tool(name="bullet_points")
async def bullet_points(text: str, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    lines = [l.strip() for l in text.split('.') if l.strip()]
    return {"bullets": [f"• {l}" for l in lines[:5]]}
if __name__ == "__main__":
    mcp.run()
