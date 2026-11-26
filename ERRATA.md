# Errata & Corrections Log

All post-publication factual, typographic, schema, legal-metadata, or proof corrections are logged here chronologically and never silently overwritten.

| Date | Version | Severity | Finding Class | Location | Correction & Resolution |
|---|---|---|---|---|---|
| 2026-11-25 | `v2.4.0` | High | `problem` | 58 files + GitHub About | Replaced inaccurate legal entity string `"0thernes LLC"` with `"Independent Researcher, Spokane, WA, USA"` matching ORCID `0009-0006-8168-9648` (no LLC entity exists). |
| 2026-11-25 | `v2.4.0` | Medium | `issue` | `src/v2_data/m01_math_nt_alg.py`, `src/v2_loader.py` | Updated `NT-001` (RH) and `NT-002` (GRH) audit notes to reflect the Nov 21, 2026 Lean FRO / Mathlib Initiative multi-kernel certification of the ~17M-line Alpöge/Claude archive (while keeping both officially unretired pending a complete human-readable paper and CMI review). |
| 2026-11-25 | `v2.4.0` | Medium | `error` | `LICENSE`, `AUTHORS.md`, `SECURITY.md`, `docs/METHODOLOGY.md`, `scripts/generate_fair_metadata.py` | Fixed stale `v2.1.0`/`v2.2.0`, `1,855`, `5,597`, `58 theorems`, and `7 tools` counts that had drifted behind `v2.3.0`. |
| 2026-11-25 | `v2.4.0` | Medium | `problem` | `outputs/` | Eliminated 6 committed artifacts exceeding the 5 MB repository hygiene cap by removing base64 PNG bloat from the interactive HTML dashboard (`20.64 MB -> 3.80 MB`), tracking deterministic `.json.gz`/`.jsonl.gz`, and moving heavy derived files to gitignored `build/` + GitHub Releases. |
| 2026-11-21 | `v2.3.0` | High | `bug` | `src/v2_data/m01..m10` | Resolved 10 dangling `raw_links`, eliminated the `GEOM-038` articulation point (making the graph strictly biconnected), merged 12 cross-field near-duplicates via `EXPLICIT_DUPLICATE_ALIASES`, and fixed `CM-001` & `LOG-001` RAG misses (`94.93% -> 100.0% MRR@5`). |
