# ADR 0001: Biconnected 1,900-Node Connectome and Pure Lean 4 Invariant Verification

- **Status:** Accepted
- **Date:** 2026-11-21 (documented in ADR format 2026-11-25)

## Context
Open-problem taxonomies frequently suffer from isolated domain silos, broken cross-references, and unverified scoring formulas. Meanwhile, importing Mathlib just to prove arithmetic bounds on scoring functions introduces multi-gigabyte CI overhead.

## Decision
1. Enforce a strict **2-vertex-connected (biconnected)** undirected dependency graph across all 1,900 deduplicated problems (`0` dangling links, `0` articulation points, `0` bridge edges) verified in `scripts/forensic_audit.py` and `tests/test_mega_atlas.py`.
2. Verify all 72 scoring, quadrant, era, taxonomy, graph-handshaking, and AutoResearch anti-gaming invariants in **Pure Lean 4.35.0** with zero Mathlib dependencies (`[propext, Quot.sound]` or empty).

## Consequences
- Clean clones verify all 72 formal theorems in ~15 seconds without external caches.
- Offline 1-hop RAG expansion (`rag/query.py`) and MCP graph queries can never hit disconnected islands or dangling IDs.
