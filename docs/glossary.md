# Glossary of Terms & Metrics

- **0thernes CSS (Composite Severity Score):** Deterministic `0–100` ranking metric combining Difficulty (`40%`), Centrality (`30%`, split 50/50 between Impact and `min(100, 25*ln(1+degree))`), 300-year-saturated Antiquity (`20%`), and Inverse 2050 Tractability (`10%`). Exact linear bounds & monotonicity are proved in `lean/MegaAtlasProofs/Scoring.lean`.
- **Abstraction Layer (`L0`–`L6`):** Seven-level vertical hierarchy from `L0: Formal & Axiomatic` up to `L6: Normative, Economic & Semantic`.
- **Apex Multi-Pillar Keystone:** A problem directly linked in the knowledge graph to `>= 3` distinct foreign Macro-Pillars (`68` problems in `v2.4.0`).
- **AQS (Atlas Quality Score):** Immutable `0–100` objective computed by `autoresearch/evaluate.py` (`25%` schema health + `25%` 25-query Gold RAG MRR@5 + `20%` provenance/FAIR + `15%` graph coupling + `15%` Lean/agentic interop). Currently `97.99`.
- **Biconnected Graph:** An undirected graph with `1` connected component, `0` articulation points (cut vertices), and `0` bridge edges — removing any single problem never disconnects the atlas.
- **Bridge Margin Ratio:** `cross_pillar_links / max(1, graph_degree) ∈ [0, 1]`, measuring the fraction of a problem's neighbors lying in foreign Macro-Pillars.
- **Composite Titan Index:** `0.90–10.00` complementary metric emphasizing civilizational impact and cross-disciplinary leverage (`35%` Difficulty + `35%` Impact + `20%` Interdisciplinarity + `10%` log-Degree).
- **CSS–Titan Margin (`M_CT`):** `css_score - 10 * titan_index ∈ [-100, +100]`, contrasting age-weighted structural severity against impact/interdisciplinarity leverage.
- **Epistemic Spectrum (`S`):** Continuous `0–100` coordinate from Pure Formal-Deductive (`0`) to Normative-Philosophical (`100`).
- **Hardness–Tractability Gradient (`D − T`):** Signed integer `difficulty_score - tractability_2050 ∈ [-9, +9]`.
- **Macro-Pillar:** Top-level partition of all human inquiry into 8 domains (`Pure Mathematics`, `Logic, Statistics & Computing`, `Fundamental Physics & Cosmos`, `Matter, Materials & Chemistry`, `Life, Mind & Medicine`, `AI, Quantum Tech, Hardware & Systems`, `Engineering, Design, Earth & Energy`, `Philosophy, Social & Humanities`).
- **Margin Role:** Exact 4-class structural boundary classification (`Apex Multi-Pillar Keystone`, `Trans-Pillar Boundary Interface`, `Intra-Pillar Bridge`, `Core Intra-Pillar Specialist`).
- **Palomar Comparator:** Lean 4.35.0's `lake comparator --config comparator.json --paranoid` sandboxed verifier checking statement identity and proof validity across 6 independent kernels (`lean`, `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`, `con-ron`).
- **Substrate Class:** Eight-class physical/formal ontology (`Abstract / Formal-Symbolic` through `Planetary / Cosmic / Socio-Technical`).
- **Verification Flag (`verification_flag`):** Per-record provenance label (`primary-registry-indexed`, `ai-assisted-editorial-synthesis`, `ai-claim-under-audit-nov2026`, or `disputed-human-claim`).
