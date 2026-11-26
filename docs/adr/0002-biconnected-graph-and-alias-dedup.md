# ADR 0002: Strict Biconnectivity and Alias-Preserving Deduplication

- **Date:** 2026-11-21
- **Status:** Accepted

## Context
Early forensic audits (`v2.2.0`) uncovered 24 dangling `raw_links`, 12 cross-field near-duplicate records, and a single-node articulation point (`GEOM-038`) whose removal disconnected leaf nodes from the knowledge graph.

## Decision
1. Maintain an explicit `EXPLICIT_DUPLICATE_ALIASES` map in `src/v2_loader.py` that merges duplicate records' `raw_links` and `registry_source` strings into canonical targets and redirects all incoming references via `dedup_alias_map`.
2. Enforce `unresolved_raw_links_count == 0`, `articulation_points == 0`, `graph_bridges == 0`, and `nx.is_biconnected(G) == True` as hard gates in `scripts/audit_atlas.py`, `scripts/forensic_audit.py`, and `tests/test_mega_atlas.py`.

## Consequences
- **Positive:** Zero silent link drops, zero duplicate problems (`1,900` unique), and resilient 2-vertex-connected cross-domain graph topology (`5,808` edges).
- **Trade-off:** Any newly authored record must supply at least two valid cross-references into the existing graph to preserve biconnectivity.
