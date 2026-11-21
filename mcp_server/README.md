# Model Context Protocol (MCP) Server (`mcp_server/`)

Zero-dependency pure-Python **MCP dual-framed stdio JSON-RPC 2.0 server** (auto-detects both line-delimited NDJSON AND LSP/MCP `Content-Length:` headers) exposing all **1,900 unsolved problems (48 fields)**, **5,808 biconnected knowledge-graph edges**, **8 Substrates × 7 Abstraction Layers**, the **November 20, 2026 AI proof-claim audit**, and **0thernes LLC provenance** directly to AI coding/research agents (**Claude Code**, **Antigravity**, **Cursor**, **Gemini CLI**, **Codex**).

## Exposed MCP Tools (9)

1. `search_problems` — Hybrid BM25 + contiguous title bigrams + unique-token coverage + NetworkX PageRank graph-authority search (**`100.0% MRR@5`**, `25/25` top-1) + 1-hop graph neighbors.
2. `get_problem` — Complete 48-field problem record (incl. substrate, layer, gradient, margin, spectrum, margin role), formal expression, Nov 2026 audit status, and 1-hop neighbors.
3. `compare_problems` — Side-by-side metric comparison with Lean-verified antisymmetric deltas & shared neighbors.
4. `list_nov2026_ai_claims` — All 12 unretired AI-claim targets + 6-item Nov 2026 verification audit ledger.
5. `get_top_ranked` — Top problems sorted by `css_score`, `titan_index`, `pagerank`, or `near_term_leverage_score`.
6. `get_pillar_summary` — 8-Macro-Pillar comparative quantitative scorecard.
7. `get_substrate_layer_summary` — Multi-layer comparative scorecard across all 8 Physical/Formal Substrates & 7 Abstraction Layers (`L0–L6`) with gradients, margins & adjacency reach.
8. `get_margin_and_gradient_extremes` — Extremes of Hardness–Tractability Gradient (`D − T`), Dual-Ranking Margin (`CSS − Titan×10`), and Apex Multi-Pillar Keystones (`3+` adjacent pillars).
9. `get_atlas_provenance` — ORCID (`0009-0006-8168-9648`), 72 Pure Lean 4.35.0 formal invariants, biconnected graph stats, epistemic boundaries & dual licensing.

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
