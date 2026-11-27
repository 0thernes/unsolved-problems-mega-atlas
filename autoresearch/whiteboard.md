# AutoResearch Whiteboard — Planner · Worker · Verifier Scratchpad

> Inspired by [`kripner/OpenProver`](https://github.com/kripner/OpenProver)'s shared Whiteboard architecture and [`SakanaAI/AI-Scientist`](https://github.com/SakanaAI/AI-Scientist)'s iterative hypothesis queue.

## Active Research Queue (Track A — Atlas Infrastructure)

| ID | Hypothesis | Target File(s) | Expected Metric Lift | Status |
|---|---|---|---|---|
| **H-001** | Staged Exact-Phrase → Strict-AND → OR BM25 without graph authority. | `rag/query.py` | `rag_mrr5` ↑ | **DISCARDED** (`0.00` lift; pure BM25 still outranked hubs on niche duplicates) |
| **H-001b** | Hybrid BM25 + deduplicated unique-token title/body coverage + log-degree knowledge-graph authority re-ranking. | `rag/query.py` | `rag_mrr5` ↑, `aqs_score` ↑ | **KEPT** (`rag_mrr5`: `89.33 → 96.00`, `21/25 → 23/25` top-1; `aqs`: `80.26 → 81.93`) |
| **H-002** | Adding FAIR/ML metadata triad (`.zenodo.json`, `croissant.json`, `ro-crate-metadata.json`, `docs/DATASHEET.md`, `AGENTS.md`, `llms.txt`, `SECURITY.md`, `CITATION.bib`) + zero-dependency MCP stdio server (`mcp_server/server.py`) + 12 Lean 4.35.0 AutoResearch invariants (`46 → 58` theorems). | FAIR metadata, `mcp_server/`, `lean/` | `provenance` ↑, `formal_score` ↑, `aqs_score` ↑ | **KEPT (`v2.2.0`)** (`aqs`: `81.93 → 95.59`) |
| **H-003** | Add contiguous title bigram matching + NetworkX `pagerank` authority fusion in `rag/query.py` to close the final 2 RAG benchmark misses (`CM-001` vs. `CM-003`, `LOG-001` vs. `LOG-007`). | `rag/query.py` | `rag_mrr5 → 100%` | **KEPT (`v2.3.0`)** (`rag_mrr5`: `96.00 → 100.00`, **`25/25` top-1**) |
| **H-004** | Full forensic remediation: fix 24 dangling links via `dedup_alias_map`, merge 7 cross-field near-duplicates, eliminate the last articulation point (`GEOM-038`), close 9 blindspots (`m11`, `1,900` unique problems), add 8 multi-layer columns (`48` cols), 14 Lean theorems (`58 → 72`), dual-framed 9-tool MCP, Charts 13–15, and honest registry-token calibration (`primary-registry-indexed = 925`). | `src/`, `lean/`, `mcp_server/`, `schema/`, `scripts/` | `provenance` ↑, `aqs_score` ↑, biconnected graph | **KEPT (`v2.3.0`)** (`aqs`: `95.59 → 97.99`, `provenance`: `82.96 → 89.94`, `0` dangling links, `0` articulation points) |
| **H-005** | Integrate 100 strictly non-duplicate open conjectures spanning all 25 fronts of Left to Solve (`m12_lefttosolve_programs.py`, verified `100/100` verbatim against the daily `59,396`-target mirror in `v2.10.0`, expanding the catalog to `2,000` biconnected problems / `6,108` edges and `290` curated crosswalk matches) plus 13-tool MCP & `12/12` mutation coverage. | `src/v2_data/m12_lefttosolve_programs.py`, `data/external/lefttosolve/`, `mcp_server/server.py` | `provenance` ↑, `aqs_score` ↑ | **KEPT (`v2.9.0`–`v2.10.0`)** (`aqs`: `97.99 → 98.35`, `100.00% MRR@5`, `25/25` top-1, `0` APs/bridges/dangling links) |
| **H-006** | Multi-model adversarial scoring audit (comparing independent editorial estimates across frontier model families via `scripts/rubric_override_diff.py`) to publish inter-rater calibration distributions on `CSS` and `Titan Index`. | `scripts/rubric_override_diff.py`, `docs/ACADEMIC_REVIEW.md` | Epistemic calibration | **BACKLOG (`v3.0.0`)** |

## Active Research Queue (Track B — Open-Problem Frontier Investigations)

| ID | Problem ID | Frontier Target | Falsification / Lean Gate | Status |
|---|---|---|---|---|
| **F-001** | `NT-001` / `ANL-001` | Independent statement-fidelity checklist & secondary kernel (`lean4lean` / `nanoda`) tracking for Nov 20, 2026 RH & Sept 8 Navier–Stokes AI claims. | Never retire without external fidelity + CMI consensus | **MONITORING** |
| **F-002** | `LOG-002` | Antihydra Collatz-like trajectory probe governing Busy Beaver `BB(6)` (`research/runs/LOG-002_antihydra_pilot/`): 5,000 exact big-int steps from `a₀ = 8` (`final_b = 2,599`, `even_frac = 0.5066`, `drift = +0.5198/step`, `bitlen(a) = 2,928`) + 99-seed sweep (`66` halt, `33` survive). | Strict non-claim boundary: finite probe proves NO theorem on `BB(6)`; `LOG-002` stays OPEN | **PILOT EXECUTED (`v2.3.0`)** |

## Negative / Falsified Results Ledger (Honest Epistemic Memory)
- **H-001 (`discard`, `2026-11-21`):** Pure lexical staged Phrase→AND→OR FTS5 BM25 yielded `0.00` lift on the 25-query benchmark (`rag_mrr5 = 89.33`, `21/25` top-1) because repeated query tokens and long niche records outscored canonical high-degree hubs (`NT-001`, `ASTRO-001`, `LOG-001`, `CM-001`). Diagnosing this failure directly produced winning hypotheses **H-001b** (`96.00%`) and **H-003** (**`100.00%`, `25/25` top-1**).
