# Lean 4.35.0 Statement-Fidelity Audit Matrix (`v2.7.0`)

Per the **Defensible Independent AI Research Playbook v1.3 (Pass 4 — Statement-Fidelity Audit)**,
this document audits every single theorem group in `lean/` against the paper (`paper/main.tex`)
and Python runtime (`src/v2_loader.py`, `src/v2_schema.py`, `autoresearch/evaluate.py`, `rag/query.py`),
stating exact fidelity status and any intentional modeling abstraction.

## 1. Module-to-Runtime Correspondence Table

| # | Lean Module & Theorem(s) | Paper / Python Definition | Fidelity Status | Exact Scope Boundary / Divergence |
|---|---|---|---|---|
| 1 | `Scoring.ageScoreCentis_*` (4 thms) | `min(100.0, max(0.0, age_years / 3.0))` (`src/v2_loader.py::compute_css_score`) | Exact integer centis | Integer floor `(age * 100) / 3` vs IEEE-754 float; differs by `< 0.01` point (`0` diffs > `0.01` across 2,000 oracle checks). |
| 2 | `Scoring.css_weights_sum`, `cssBps_*` (9 thms) | `0.40*diff + 0.30*cent + 0.20*age + 0.10*(100-tract)` (`src/v2_loader.py::compute_css_score`) | Exact linear bps; `ln` abstracted | Transcendental `min(100, 25*ln(1+deg))` abstracted as bounded `cent100 <= 100`; verified differentially against 50-digit `Decimal` oracle (`reference/scoring_oracle.py`). |
| 3 | `Scoring.titan_weights_sum`, `titanCentis_*` (6 thms) | `0.35*d + 0.35*i + 0.20*r + 0.10*min(10, 2.5*ln(1+deg))` (`src/v2_loader.py::load_v2_master`) | Exact linear centis; `ln` abstracted | Same `ln(1+deg)` boundary checked via `reference/scoring_oracle.py`. |
| 4 | `Scoring.leverageTenths_*` (3 thms) | `(impact * tractability_2050) / 10.0` (`src/v2_loader.py::load_v2_master`) | Exact 1-to-1 isomorphism | Zero divergence (`impact * tract` in tenths). |
| 5 | `Quadrants.classify_eq_Q{1..4}_iff`, `classify_exhaustive`, `highImpact_preserved`, `highTract_preserved`, `Q1_leverage_ge_56` (8 thms) | `classify_quadrant(impact, tract)` (`src/v2_loader.py::classify_quadrant`) | Exact 1-to-1 isomorphism | Zero divergence; thresholds `impact >= 8` and `tract >= 7` match verbatim. |
| 6 | `Quadrants.computeEra_*` (3 thms) | `compute_era(year)` (`src/v2_schema.py::compute_era`) | Exact 1-to-1 isomorphism | Zero divergence across all 6 cutoffs (`500, 1800, 1900, 1970, 2000`). |
| 7 | `Taxonomy.pillar_count_eq_8`, `superdomain_count_eq_28`, `pillar_partition_*`, `all*_complete`, `pillarOf_surjective`, `cross_pillar_implies_cross_superdomain` (8 thms) | `MACRO_PILLARS` (8), `SUPERDOMAIN_TO_PILLAR` (28) (`src/v2_schema.py::SUPERDOMAIN_TO_PILLAR`) | Exact 1-to-1 isomorphism | Exact `[5, 3, 3, 3, 3, 4, 4, 3]` partition verified identically. |
| 8 | `GraphInvariants.handshaking_lemma` | `sum(deg(v)) == 2 * |E|` on `nx.Graph()` (`src/v2_loader.py::load_v2_master`) | Exact finite-graph theorem | Holds universally for all finite nodup vertex lists & closed edge lists; biconnectivity (`0` APs, `0` bridges) checked programmatically by NetworkX. |
| 9 | `GraphInvariants.cross_pillar_le_cross_superdomain`, `cross_superdomain_le_total`, `edge_hierarchy` | `cross_pillar_edges <= cross_superdomain_edges <= total_graph_edges` (`src/v2_loader.py::load_v2_master`) | Exact 1-to-1 isomorphism | Zero divergence (`1,084 <= 2,076 <= 5,808`). |
| 10 | `GraphInvariants.dedupBy_length_le` | First-occurrence deduplication (`src/v2_loader.py::load_v2_master`) | Exact cardinality bound | Proves `|dedup| <= |raw|` (`1,900 <= 1,912`). |
| 11 | `AutoResearchInvariants.aqs_*` (6 thms) | `aqs_score` in immutable `autoresearch/evaluate.py::evaluate_all` | Exact integer bps | Weights `25+25+20+15+15=100`, bounds `[0, 10000]`, strict monotonicity. |
| 12 | `AutoResearchInvariants.failed_gates_always_discard`, `shouldKeep_iff`, `updateBest_*` (4 thms) | Karpathy keep/discard protocol (`autoresearch/program.md`) | Exact formal policy | Guarantees failed hard gates ALWAYS discard regardless of candidate score. |
| 13 | `AutoResearchInvariants.metricDelta_self`, `metricDelta_antisymm` (2 thms) | `compare_two_problems` deltas (`rag/query.py::compare_two_problems`) | Exact integer antisymmetry | Float differences verified to `1e-6` in `test_pairwise_comparator_antisymmetry`. |
| 14 | `LayerGradients.substrate_count_eq_8`, `layer_count_eq_7`, `allSubstrates_complete`, `layerIndex_le_6` (4 thms) | `SUBSTRATE_CLASSES` (8), `ABSTRACTION_LAYERS` (7) (`src/v2_loader.py::SUBSTRATE_CLASSES`) | Exact 1-to-1 isomorphism | Zero divergence. |
| 15 | `LayerGradients.hardnessTractGradient_*`, `cssTitanMarginBps_bounds` (5 thms) | `difficulty_score - tractability_2050`, `css_score - 10 * titan_index` (`src/v2_loader.py::load_v2_master`) | Exact integer / bps bounds | Exact `[-9, +9]` and `[-10000, +10000]` bounds. |
| 16 | `LayerGradients.bridgeMarginBps_*`, `adjacent_pillars_lt_8`, `marginRole_exhaustive`, `apexKeystone_requires_3_adjacent` (5 thms) | `bridge_margin_ratio`, `adjacent_pillars_count`, `classify_margin_role` (`src/v2_loader.py::classify_margin_role`) | Exact bps correspondence | `3000 bps` matches `bridge_ratio >= 0.30`. |
| 17 | `NonVacuity.*` (12 thms) | Concrete inhabitants + exact `autoresearch/results.tsv` trace (`8026→8193→9559→9799`) + sharp negative boundaries | Non-vacuity proof | Proves zero hypothesis bundles across M1–M6 are unsatisfiable. |
| 18 | `AdversarialTests.*` (10 thms) | Constructive kernel-checked refutations (`¬P`) of deliberately false / off-by-one variants across M1–M6 + live negative kernel rejection | Adversarial test (Playbook Item 12) | Complements 6/6 (100%) Python semantic mutation kill rate. |
| 19 | `PalomarSolution.m1..m8`, `prove_all_mega_atlas_invariants` (9 thms) | `palomar/PalomarChallenge.lean` contract | Exact comparator identity | Verified via `scripts/verify_lean_six_kernels.sh` (`leanchecker --fresh`, `lake check --paranoid`, `lake comparator --paranoid`) across all 6 kernels. |

## 2. What Is Explicitly NOT Formalized in Lean

1. **None of the 1,900 cataloged open scientific or mathematical problems are proved in Lean.**
2. **Transcendental `ln(1 + degree)` floating-point calls** are verified differentially against 50-digit `Decimal` in `reference/scoring_oracle.py`, not inside Lean.
3. **NetworkX PageRank, betweenness, modularity, and biconnectivity** are audited programmatically via `tests/test_mega_atlas.py` and `scripts/forensic_audit.py`.
4. **SQLite FTS5 Porter-stemming BM25 ranking** is audited via the immutable 25-query Gold Benchmark (`100.0% MRR@5`) and negative/metamorphic tests.

## 3. Author Sign-Off (Playbook v1.3 Item 10)

- **Audited & Signed Off By:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`)
- **Date:** `2026-11-26` (`v2.7.0`, all 19 rows reviewed against Lean 4.35.0 source, Python runtime symbols, and `paper/main.tex` Table 3)
