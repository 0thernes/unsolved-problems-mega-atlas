# Quantitative Methodology, Scoring Formulas & Known Limitations

**Release:** `v2.10.0` · **Reference Year:** `2026` (frozen in `src/v2_loader.py`)  
**Formal Verification:** Exact discrete counterparts of all scoring, quadrant, era, taxonomy, generic list-multigraph, AutoResearch ratchet, gradient/margin, NonVacuity, and AdversarialTests formulas are machine-checked in zero-Mathlib Lean 4.35.0 (`lean/`, **103** audited declarations of `117` in `lean/`, 0 `sorry`, per-theorem axioms within `[propext, Quot.sound]`; kernel-checked by Lean, with the `9` Palomar comparator targets also accepted by `6` kernel checks across `5` distinct implementations via `scripts/verify_lean_six_kernels.sh`). These are invariants of the scoring software model, not of the 2,000-row data or its graph, which are checked in Python.

---

## 1. Taxonomic Architecture

Every entry is assigned to an exact multi-layer hierarchy enforced by `src/v2_schema.py` and `schema/problem.schema.json`:
- **8 Macro-Pillars** (surjective partition proven in `MegaAtlasProofs.Taxonomy.pillarOf_surjective`),
- **28 Superdomains** (`5 + 3 + 3 + 3 + 3 + 4 + 4 + 3 = 28`, proven in `pillar_partition_sum_28`),
- **8 Physical/Formal Substrates × 7 Abstraction Layers (`L0–L6`)**,
- **1,851 fine-grained Subdomains**,
- **88 Canonical Hub Anchors (`HUB:*`)** enabling deterministic cross-module linkage across `m01`–`m12`.

## 2. Deduplication & Knowledge-Graph Construction

1. **Strict Deduplication (`src/v2_loader.py`):** 2,012 raw authored entries are scanned in canonical priority order (`m01`–`m12`). Collisions by exact `id`, normalized title (`_norm_name`), or `EXPLICIT_DUPLICATE_ALIASES` preserve the primary record and redirect every incoming link via `dedup_alias_map` so zero edges are lost (`12` overlaps cleanly merged → **`2,000` unique problems**, `0` unresolved raw links). Cardinality bound `|dedup| ≤ |raw|` is proved in `MegaAtlasProofs.GraphInvariants.dedupBy_length_le`.
2. **Biconnected Undirected Knowledge Graph (`NetworkX`):** Every `HUB:*` alias and direct problem ID is resolved into undirected simple edges (no self-loops). Resulting graph: **`2,000` nodes, `6,108` edges, `1` connected component, `0` articulation points, `0` bridges (`nx.is_biconnected(G) == True`), `14` greedy modularity communities**.
3. **Centrality Metrics:** Degree `deg(v)`, PageRank (`alpha = 0.85`), approximate betweenness centrality (`k = 280`, `seed = 42` for deterministic reproducibility), cross-superdomain links (`2,215`, `36.3%`), and cross-pillar bridge links (`1,152`, `18.9%`; `cross_pillar ≤ cross_superdomain ≤ |E|` formally verified in `edge_hierarchy`).

## 3. Dual Ranking Formulas (`0thernes CSS` & `Titan Index`)

### A. 0thernes Composite Severity Score (`css_score`, 0–100)
Directly unified with sibling repository [`0thernes/unsolved-mathematics`](https://github.com/0thernes/unsolved-mathematics/blob/main/docs/methodology/RANKING.md):

```text
difficulty_100   = difficulty_score * 10                                  ∈ [10, 100]
deg_centrality   = min(100.0, 25.0 * ln(1 + graph_degree))                ∈ [0, 100]
centrality_100   = 0.50 * (civilizational_impact * 10) + 0.50 * deg_centrality
age_score_100    = min(100.0, max(0.0, (2026 - year_formulated) / 3.0))   ∈ [0, 100]
tractability_100 = tractability_2050 * 10                                 ∈ [10, 100]

CSS = 0.40 * difficulty_100
    + 0.30 * centrality_100
    + 0.20 * age_score_100
    + 0.10 * (100.0 - tractability_100)
```

- **Why the 300-Year Saturation Cap?** Problems older than 300 years (e.g., antiquity puzzles posed 300–500 BCE) saturate at `age_score = 100` (formally verified in `ageScoreCentis_saturates_at_300`), preventing antiquity from infinitely swamping difficulty and structural centrality.
- **Weight Rationale:** Intrinsic difficulty (`0.40`) + structural/civilizational centrality (`0.30`) account for 70% of the score; longevity (`0.20`) rewards centuries-long resistance; inverse tractability (`0.10`) lightly separates entrenched enigmas from imminent breakthroughs.

### B. Composite Titan Index (`titan_index`, 0.90–10.00)
Emphasizes cross-disciplinary civilizational leverage without historical age weighting:
```text
Titan = 0.35 * difficulty_score
      + 0.35 * civilizational_impact
      + 0.20 * interdisciplinarity_index
      + 0.10 * min(10.0, 2.5 * ln(1 + graph_degree))
```

### C. Near-Term Leverage & Strategic 4-Quadrants
- `near_term_leverage_score = (civilizational_impact * tractability_2050) / 10.0` (`∈ [0.1, 10.0]`).
- **Strategic Quadrants:**
  - `Q1` (`impact ≥ 8, tract ≥ 7`): Near-Term Civilizational Levers (Lean-verified: every `Q1` problem satisfies `near_term_leverage_score ≥ 5.6`).
  - `Q2` (`impact ≥ 8, tract < 7`): Grand Centuries-Scale Titans.
  - `Q3` (`impact < 8, tract ≥ 7`): Targeted Technical Frontiers.
  - `Q4` (`impact < 8, tract < 7`): Deep Foundational & Formal Enigmas.

## 4. Epistemic Verification Flags

Every record carries a deterministic `verification_flag`:
- `ai-claim-under-audit-nov2026` (`12`): Targeted by unverified Fall/Nov 2026 AI proof claims; explicitly unretired.
- `disputed-human-claim` (`11`): Contested human proof claims lacking community consensus (e.g., abc/IUT).
- `primary-registry-indexed` (`1,035`): Problem provenance explicitly anchored to a named open-problem registry or canonical institutional canon (Left to Solve / `formal-conjectures`, Clay CMI, ProofAtlas, Erdős DB, OEIS, Ben Green's 100, Open Quantum Problems, Hilbert, Smale, Landau, Kourovka, Kirby, SEP/PhilPapers, NAE, DARPA, DOE, IPCC, WHO, CERN, LIGO, IRDS, etc.).
- `ai-assisted-editorial-synthesis` (`942`): Curated frontier research problem synthesized from domain literature under human direction; awaiting external specialist audit.

## 5. Known Limitations & Biases (Disclosed Honestly)

1. **Rubric Subjectivity:** Integer 1–10 input ratings (`difficulty`, `tractability_2050`, `impact`, `interdisciplinarity`) are editorial estimates, not objective physical constants.
2. **Graph Construction Bias:** Hub density reflects curated cross-references (`HUB:*`), so well-known keystone problems (P vs. NP, Riemann Hypothesis, Turbulence, Exact Ramsey Numbers, Langlands) naturally accumulate higher PageRank/degree than niche specialist conjectures.
3. **Antiquity Effect in CSS:** Because Philosophy & Metaphysics problems frequently date to 300 BCE–1750 CE with high difficulty and low empirical tractability, they naturally rank near the top of `CSS` while modern physics/CS/math problems dominate `Titan Index` and `PageRank`. Publishing **both** `CSS` and `Titan Index` exposes this structural contrast transparently.
4. **Completeness Horizon:** No finite list captures every open question in existence—this atlas is a `2,000`-problem unified cross-disciplinary baseline designed for reproducible versioning and community extension. See [`LIMITATIONS.md`](../LIMITATIONS.md).
