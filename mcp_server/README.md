# Model Context Protocol (MCP) Stdio Server (`v2.10.0`)

Zero-dependency JSON-RPC 2.0 stdio server (`mcp_server/server.py`) exposing **13 grounded scientific research tools** over the 2,000-problem Unsolved Problems Mega-Atlas and the 59,396-problem daily Left to Solve sidecar mirror. Speaks both **newline-delimited JSON-RPC (NDJSON)** and **`Content-Length:` framed** MCP/LSP stdio (enforcing a strict `1 MiB` frame cap, truncated-frame rejection, JSON-object `-32600` validation, and string-filter type checks on both framings), automatically builds/refreshes `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` on demand on fresh clones or version upgrades, clamps `top`/`hops`/`limit` bounds, and validates all required arguments.

- **Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`)
- **License:** `Apache-2.0` (`../LICENSE-CODE`)

## Exposed Tools (13)

1. `search_problems` — Hybrid BM25 + Title-Bigram + PageRank RAG search with pillar/superdomain/flag filters (enforced even on exact-ID queries) & 1-hop graph expansion.
2. `get_problem` — Complete 48-field structured dossier by exact Problem ID + 1-hop graph neighbors.
3. `compare_problems` — Side-by-side comparison with Lean-verified antisymmetric deltas & shared neighbors.
4. `list_nov2026_ai_claims` — All 12 Fall/Nov 2026 AI proof-claim targets (explicitly flagged unretired) + 6-item Nov 26, 2026 audit ledger with primary RH/GRH citations.
5. `get_top_ranked` — Top problems by `css_score`, `titan_index`, `pagerank`, `near_term_leverage_score`, `hardness_tractability_gradient`, or `bridge_margin_ratio`.
6. `get_pillar_summary` — 8-Macro-Pillar quantitative scorecard.
7. `get_substrate_layer_summary` — 8-Substrate × 7-Abstraction-Layer (`L0..L6`) comparative matrix.
8. `get_margin_and_gradient_extremes` — Steepest `D−T` chasms, highest tractability margins, CSS–Titan divergences, and Apex Multi-Pillar Keystones.
9. `list_author_frontier_contributions` — `20` companion rows covering all `27` other audited entries in `0thernes-research-archive` Cycle-3 [RESULTS.md](https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md) (`94` results across `28` entries; `R85` = this repo; only Section A records answers to open questions from the literature), with COI, non-peer-reviewed status, and `0/2,000` atlas problems solved.
10. `get_atlas_provenance` — Author/ORCID, Lean 4.35.0 software-model audit status and scope (`103` audited of `117` declarations in `lean/`; the `9` Palomar comparator targets pass `6` kernel checks across `5` distinct implementations), dual license, and summary stats.
11. `simulate_rubric_override` — Community rubric sensitivity simulator returning Spearman `rho`, Kendall `tau`, Top-25 Jaccard overlap, Quadrant migrations, and top rank movers under custom CSS weights or per-problem score overrides (canonical `(-css, -titan, -deg, id)` tie-break).
12. `get_live_registry_tracker` — Returns the daily-synced tracker (`06:00 UTC` via `.github/workflows/daily-registry-sync.yml`) covering all `16` global open-problem registries and all `25` mathematical programs on Left to Solve (`https://lefttosolve.com/programs`), with optional `program_filter` and `formalized_only` filters.
13. `query_lefttosolve_programs` — Offline explorer over the full daily-mirrored `59,396`-problem Left to Solve 25-program JSONL catalog (`data/external/lefttosolve/`): returns `solved_by_kind` summaries and daily deltas (`action="summary"`), filters mirrored metadata (`action="search"`), or inspects `290` curated & exact-normalised-title candidate matches against all `2,000` Mega-Atlas problems (`action="crosswalk"`). Strict `action` string validation and `is_relative_to` path containment enforced.

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
