# Known Limitations & Scope Boundaries

Per **Build Standard for LLMs v1.2.0 (B41)** and the **Defensible Independent AI Research Playbook v1.3**, every known limitation, platform caveat, methodological bias, and literal-vs-metaphor boundary is stated plainly below.

## 1. Epistemic & Methodological Limitations

1. **Editorial Rubric Subjectivity:** The `1–10` ratings (`difficulty_score`, `tractability_2050`, `civilizational_impact`, `interdisciplinarity_index`) are curated AI-assisted editorial estimates by a solo independent researcher, NOT multi-rater peer-reviewed consensus scores. They should be treated as explicit, editable, falsifiable hypotheses (`src/v2_data/`).
2. **Disciplinary Registry Skew:** Pure Mathematics (`514` problems, `27.1%`) has deep historical registries (`ProofAtlas`, `Erdős Problems`, `Clay Millennium`, `Kourovka`, `Kirby`), whereas emerging engineering, design, and humanities frontiers lack centralized problem registries. Accordingly, `952 / 1,900` records carry the explicit flag `ai-assisted-editorial-synthesis` rather than `primary-registry-indexed`.
3. **Volatility of Fall–November 2026 AI Proof Claims:** The `12` problems flagged `ai-claim-under-audit-nov2026` (including `NT-001` Riemann Hypothesis, `NT-002` GRH, and `ANL-001` 3D Navier–Stokes) reflect a point-in-time snapshot as of **November 25, 2026**. Even where Lean multi-kernel certification succeeded (Alpöge/Claude RH/GRH archive on Nov 21, 2026), lack of a complete human-readable paper and pending Clay CMI/community evaluation keep all 12 officially unretired.
4. **No External Peer Review:** Neither this dataset, the AMS-LaTeX white paper, nor the 12 cross-referenced companion archive entries in `0thernes-research-archive` have undergone external journal peer review.
5. **Formal Verification Scope Boundary:** Lean 4.35.0 (`103` theorems across 6 kernels) certifies ONLY discrete formula bounds, monotonicity, taxonomy partitions, finite graph handshaking, deduplication monotonicity, AutoResearch keep/discard ratchet properties, gradient/margin bounds, concrete NonVacuity witnesses, and constructive AdversarialTests refutations. It proves **ZERO** of the `1,900` open problems themselves (`0 / 1,900` retired). IEEE-754 `log1p(degree)` calculations are checked differentially against our 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`), not inside Lean.
6. **Track B Antihydra Pilot Is Finite Only:** `research/runs/LOG-002_antihydra_pilot/` evaluates `5,000` exact bigint steps (`a_0=8`) and `99` seeds (`a_0 ∈ [2, 100]` to `2,000` steps). It provides zero proof regarding asymptotic halting of Antihydra or `BB(6)`.

## 2. Platform, Runtime & Packaging Caveats

- **Tested Platforms:** Local execution verified on Windows 11 (`x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15). GitHub Actions CI executes across `ubuntu-latest`, `macos-latest`, and `windows-latest`.
- **`lake comparator` Sandbox (`bubblewrap`):** Full `bwrap`-sandboxed 6-kernel verification runs via `bash scripts/verify_lean_six_kernels.sh` on Linux (`ubuntu-latest` CI), exporting `PalomarChallenge` to `/tmp/PalomarChallenge.export` and passing `--challenge-from-export` to `lake comparator --paranoid`; Windows lacks Linux `bwrap` user namespaces, so local Windows verification replays `lean`, `leanchecker --fresh`, `leanchecker-paranoid`, `nanoda_bin`, `con-leche --verified`, `con-ron --verified`, and the live negative kernel rejection test directly while Linux CI runs the full sandboxed 6-kernel comparator including `lean4lean`.
- **Optional 168-Page Chrome Directory PDF:** `src/v2_export_all.py` builds the optional 168-page directory PDF into gitignored `build/` only when Chrome/Edge is installed (`--skip-pdf` skips it cleanly on headless CI; the canonical scholarly PDF is `dist/Donahue_2026_unsolved_problems_mega_atlas.pdf` compiled by Tectonic).
- **Locale Scope:** All text, search tokenization (`porter unicode61`), and UI copy target **English (`en-US`, UTF-8)** only.

## 3. Literal vs. Metaphor Boundary Table

| Term Used in Atlas / Paper | Literal Technical Meaning | What It Does NOT Claim |
|---|---|---|
| **Biconnected Connectome / Knowledge Graph** | An undirected NetworkX graph (`1,900` vertices, `5,808` edges) with `nx.is_biconnected(G) == True` (`0` articulation points, `0` bridges). | Does NOT claim biological neural anatomy or causal proof-reduction between every adjacent pair. |
| **Keystone Domino Hub** | A vertex with high PageRank, graph degree, and ≥ 3 adjacent foreign Macro-Pillars (`adjacent_pillars_count >= 3`). | Does NOT prove that solving the hub mathematically implies solving all neighbors. |
| **Hardness–Tractability Chasm / Gradient (`D − T`)** | Signed integer difference `difficulty_score - tractability_2050 ∈ [-9, +9]`. | Not a physical PDE gradient or thermodynamic potential. |
| **Multi-Layer Reality Stack (`8 Substrates × 7 Layers`)** | A deterministic 2D taxonomic lookup table mapping each of the 28 Superdomains to one Substrate and one Abstraction Layer (`L0..L6`). | Not a claim of ontological reductionism across physics, biology, and ethics. |
| **AutoResearch Ratchet** | Automated local evaluation against immutable `autoresearch/evaluate.py` keeping changes only when hard gates pass and `AQS` strictly increases. | Not autonomous discovery of mathematical proofs of open conjectures. |
| **Verified / Formalized** | Machine-checked in Lean 4.35.0 across 6 kernels for the 103 structural invariant & adversarial-refutation theorems in `lean/`, OR schema/parity-checked in Python for dataset properties. | NEVER means that any of the 1,900 cataloged open problems are solved or peer-reviewed. |
