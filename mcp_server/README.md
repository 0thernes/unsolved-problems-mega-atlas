# Model Context Protocol (MCP) Server (`mcp_server/`)

Zero-dependency pure-Python **MCP stdio JSON-RPC 2.0 server** exposing all **1,855 unsolved problems**, **5,597 knowledge-graph edges**, the **November 20, 2026 AI proof-claim audit**, and **0thernes LLC provenance** directly to AI coding/research agents (**Claude Code**, **Antigravity**, **Cursor**, **Gemini CLI**, **Codex**).

## Exposed MCP Tools (7)

1. `search_problems` — Hybrid BM25 + unique-token coverage + log-degree knowledge-graph authority search (`96.0% MRR@5`) + 1-hop graph neighbors.
2. `get_problem` — Complete problem record, formal expression, Nov 2026 audit status, and 1-hop neighbors.
3. `compare_problems` — Side-by-side metric comparison with Lean-verified antisymmetric deltas & shared neighbors.
4. `list_nov2026_ai_claims` — All 12 unretired AI-claim targets + 6-item Nov 2026 verification audit ledger.
5. `get_top_ranked` — Top problems sorted by `css_score`, `titan_index`, `pagerank`, or `near_term_leverage_score`.
6. `get_pillar_summary` — 8-Macro-Pillar comparative quantitative scorecard.
7. `get_atlas_provenance` — ORCID (`0009-0006-8168-9648`), 58 Pure Lean 4.35.0 formal invariants, epistemic boundaries & dual licensing.

## Client Configuration Example (`mcp_config.json`)

```json
{
  "mcpServers": {
    "unsolved-problems-mega-atlas": {
      "command": "python",
      "args": ["Z:/unsolved-problems-mega-atlas/mcp_server/server.py"]
    }
  }
}
```
