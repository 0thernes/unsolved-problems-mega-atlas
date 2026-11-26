# Architecture Decision Records (ADRs)

Key engineering and research-integrity decisions for the **Unsolved Problems Mega-Atlas** are recorded below.

| ADR | Date | Status | Decision |
|---|---|---|---|
| [0001](0001-zero-mathlib-lean-invariants.md) | 2026-11-20 | Accepted | Use zero-Mathlib Pure Lean 4.35.0 for all atlas formal invariants |
| [0002](0002-biconnected-graph-and-alias-dedup.md) | 2026-11-21 | Accepted | Enforce strict biconnectivity (0 APs, 0 bridges) and alias-preserving deduplication |
| [0003](0003-offline-fts5-hybrid-rag-and-mcp.md) | 2026-11-21 | Accepted | Build zero-dependency offline SQLite FTS5 Hybrid RAG and dual-framed stdio MCP server |
| [0004](0004-sub-5mb-tracked-hygiene-and-palomar-layout.md) | 2026-11-25 | Accepted | Keep all tracked git files `< 5 MB` and place `PalomarChallenge` in `palomar/` to preserve immutable `evaluate.py` |
