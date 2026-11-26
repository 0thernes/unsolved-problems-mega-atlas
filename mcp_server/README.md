# Model Context Protocol (MCP) Stdio Server (`v2.6.0`)

Zero-dependency JSON-RPC 2.0 stdio server (`mcp_server/server.py`) exposing **10 grounded scientific research tools** over the 1,900-problem Unsolved Problems Mega-Atlas. Speaks both **newline-delimited JSON-RPC (NDJSON)** and **`Content-Length:` framed** MCP/LSP stdio, automatically builds/refreshes `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` on demand on fresh clones or version upgrades, clamps `top`/`hops`/`limit` bounds, and validates all required arguments.

- **Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`)
- **License:** `Apache-2.0` (`../LICENSE-CODE`)

## Exposed Tools (10)

1. `search_problems` — Hybrid BM25 + Title-Bigram + PageRank RAG search with pillar/superdomain/flag filters & 1-hop graph expansion.
2. `get_problem` — Complete 48-field structured dossier by exact Problem ID + 1-hop graph neighbors.
3. `compare_problems` — Side-by-side comparison with Lean-verified antisymmetric deltas & shared neighbors.
4. `list_nov2026_ai_claims` — All 12 Fall/Nov 2026 AI proof-claim targets (explicitly flagged unretired) + 6-item Nov 25, 2026 audit ledger.
5. `get_top_ranked` — Top problems by `css_score`, `titan_index`, `pagerank`, `near_term_leverage_score`, `hardness_tractability_gradient`, or `bridge_margin_ratio`.
6. `get_pillar_summary` — 8-Macro-Pillar quantitative scorecard.
7. `get_substrate_layer_summary` — 8-Substrate × 7-Abstraction-Layer (`L0..L6`) comparative matrix.
8. `get_margin_and_gradient_extremes` — Steepest `D−T` chasms, highest tractability margins, CSS–Titan divergences, and Apex Multi-Pillar Keystones.
9. `list_author_frontier_contributions` — 12 companion archive entries (`0thernes-research-archive`) with explicit COI, non-peer-reviewed status, and `0/1,900` overarching Atlas parents retired.
10. `get_atlas_provenance` — Author/ORCID, 103-theorem 6-kernel Lean 4.35.0 audit status, dual license, and summary stats.

## Client Configuration (Claude Code / Antigravity / Cursor / Gemini CLI)

```json
{
  "mcpServers": {
    "unsolved-problems-mega-atlas": {
      "command": "python",
      "args": ["mcp_server/server.py"]
    }
  }
}
```
