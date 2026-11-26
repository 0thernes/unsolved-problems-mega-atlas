# ADR 0003: Zero-Dependency Offline SQLite FTS5 Hybrid RAG & Dual-Framed MCP Server

- **Date:** 2026-11-21 (updated 2026-11-25 for auto-build & 10th tool)
- **Status:** Accepted

## Context
Embedding-based vector databases require external model downloads, API keys, or GPU weights, breaking offline determinism and clean-clone reproducibility. Similarly, fast-moving MCP SDKs frequently introduce breaking dependency churn.

## Decision
1. Use Python's built-in `sqlite3` with Porter-stemmed `FTS5` + staged precision-first retrieval (exact ID → phrase → strict AND → relaxed OR backfill) + deterministic hybrid re-ranking (BM25 + title/bigram coverage + NetworkX degree/PageRank authority).
2. Auto-build `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` on demand (`ensure_sqlite_db()`) on clean git clones.
3. Implement `mcp_server/server.py` directly over stdlib `json`/`sys.stdin.buffer`, supporting both NDJSON and `Content-Length:` framed JSON-RPC 2.0 across 10 read-only tools.

## Consequences
- **Positive:** Sub-10 ms latency, `100.0% MRR@5` (`25/25` top-1) on the immutable 25-query Gold Benchmark, zero external API keys, zero MCP SDK dependency drift.
- **Trade-off:** Purely lexical+graph retrieval (no dense neural semantic embeddings), explicitly noted in `LIMITATIONS.md`.
