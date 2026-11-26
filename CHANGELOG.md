# Changelog

All notable changes to the **Unsolved Problems Mega-Atlas** are documented in this file following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [2.5.0] — 2026-11-25

### Added, Fixed & Hardened — Hostile-Referee 3-Cycle Audit: 103 Lean 4.35.0 Theorems (AdversarialTests), Crossref Retraction Verifier, Exact Ground-Truth Sync & 100% SPDX
- **Constructive Adversarial Definition Refutation Suite (`lean/MegaAtlasProofs/AdversarialTests.lean`, `92 → 103` Audited Theorems — Playbook v1.3 Item 12):**
  - Authored `AdversarialTests.lean` (`10` kernel-checked `¬P` refutations across all 6 core modules: CSS cap, age-299 non-saturation, Titan cap, tight Q1/Q2 leverage floors, superdomain cardinality, Handshaking factor, anti-reward-hacking failed-gate discard, and exact `apexKeystone`/`transPillarMargin` thresholds) bundled into `M8_AdversarialRefutations` (`Challenge.lean`, `Solution.lean`, `PalomarSolution.lean`, `palomar/PalomarChallenge.lean`, `comparator.json`, `formalization.yaml`, `blueprint/index.html`, `results/lean_axioms.txt`).
  - Audited all **103** theorems (`1,769` exported declarations) strictly within `[propext, Quot.sound]` across all **6 independent proof kernels** via new single-source script [`scripts/verify_lean_six_kernels.sh`](scripts/verify_lean_six_kernels.sh) (`just lean-kernels`), replacing non-working bare `lake comparator` commands across `README.md`, `lean/README.md`, `REPLICATION.md`, and `paper/main.tex`, and attesting `results/lean_axioms.txt` in SLSA build provenance (`ci.yml`, Playbook Item 28).
- **Hostile-Referee Factual & Parity Corrections (Logged in `ERRATA.md` & `HARDENING_LOG.md`):**
  - Fixed drifted AutoResearch numbers in `paper/main.tex` §5 (`82.22%`/`19/25`/`91.69`/mislabeled discarded `H-002`/`H-004`) and `NonVacuity.lean` (`9169→9649`) to match exact `autoresearch/results.tsv` ground truth (`89.33%` [`21/25`] → `100.0%` [`25/25`], `AQS` `80.26 → 97.99`, discarded `H-001`, kept `H-001b`/`H-002`/`H-003`/`H-004`).
  - Aligned `paper/main.tex` Table 1 to exact 1-to-1 `C1`–`C10` parity with `CLAIMS.md`.
  - Updated stale root `ARCHITECTURE.md` (`v2.3.0`/`72` thms/`MIT` → `v2.5.0`/`103` thms/`Apache-2.0`), fixed stale line 19 & exact 14-file `1,707`-line Lean table in `docs/WHITE_PAPER.md`, fixed inaccurate `< 3.5 MB` HTML dashboard claim in `scripts/benchmark_atlas.py` / `docs/benchmarks.md` to dynamic exact measured size (`3.80 MB`, `< 4.0 MB` budget), and fixed mislabeled `B34`/`B33`/`A28`/`A30` labels in `DEVIATIONS.md` & `repo.yaml`.
  - Upgraded `OTHERNES_VERIFIED_FRONTIER_CONTRIBUTIONS` in `src/v2_loader.py` (now reading `VERSION` dynamically along with `mcp_server/server.py`) to **10 live-verified companion entries** synced from `0thernes-research-archive` commit `5170a63` (7 Tier-I + 3 Tier-II 6-kernel/Lean builds incl. `ultrametrica v1.4.0` & `planaria v2.3.0`), explicitly confirming **`0 / 1,900` overarching Mega-Atlas parent problems retired**.
- **Playbook v1.3 Gold Standard Completions & 6 New Regression Tests:**
  - Added live **Crossref API retraction checks** in `scripts/check_citations.py` (`12/12` live, `0` retractions — Item 16), **`docs/literature-search-log.md`** (Item 15), **100% REUSE/SPDX headers** across all remaining source/data/script files (Item 24), **Export-Control Self-Screen (15 CFR 734.8)** & **Zenodo/JOSS/Mathlib venue disclosures** in `docs/AI_DISCLOSURE.md` (Items 37 & 40), **Author Sign-Off** in `docs/statement-fidelity.md` (Item 10), **Withdrawal & Correction Policy** in `ERRATA.md` (Item 39), **Aaronson's 8-Signs audit** in `docs/reviews/2026-11-25-redteam-hardening.md`, and **6 new regression tests** (`53` total `pytest` tests) preventing every caught defect from ever returning.

## [2.4.0] — 2026-11-25

### Added & Upgraded — Six-Kernel Lean 4.35.0 Palomar Verification, AMS-LaTeX White Paper, Deep Verification Ladder & 100% Build Standard v1.2.0 Compliance
- **Six-Kernel Pure Lean 4.35.0 Palomar Upgrade (`72 → 92` Audited Theorems):**
  - Migrated all Lean modules to Lean 4.35.0 `module` syntax (`public import`, `@[expose] public section`) with strict `[leanOptions]` (`autoImplicit = false`, `linter.unusedVariables = true`, `linter.deprecated = true`).
  - Added [`lean/MegaAtlasProofs/NonVacuity.lean`](lean/MegaAtlasProofs/NonVacuity.lean) (`12` concrete inhabitants & sharp negative boundary witnesses), [`lean/Challenge.lean`](lean/Challenge.lean), [`lean/Solution.lean`](lean/Solution.lean), [`lean/PalomarSolution.lean`](lean/PalomarSolution.lean), [`palomar/PalomarChallenge.lean`](palomar/PalomarChallenge.lean) (outside `lean/` preserving immutable `autoresearch/evaluate.py` — ADR 0004), [`lean/comparator.json`](lean/comparator.json), and [`lean/formalization.yaml`](lean/formalization.yaml).
  - Audited all **92** theorems (`1,753` exported declarations) strictly within constructive `[propext, Quot.sound]` across all 6 independent kernels (`lean`, `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche --verified`, `con-ron --verified`); froze [`results/lean_axioms.txt`](results/lean_axioms.txt) with automated README drift check (`scripts/check_readme_axioms.py`) and interactive SVG Proof Blueprint (`blueprint/index.html`).
- **Publication-Grade 10-Page AMS-LaTeX White Paper & Clean-Room arXiv Tarball (`paper/`, `dist/`):**
  - Authored `paper/main.tex` & `paper/refs.bib` with 5 vector PDF figures, Numbered Claims Ledger, Statement-Fidelity Audit Matrix, and companion author-preprint COI cross-map; compiled via Tectonic (`scripts/build_paper.py`) into `dist/Donahue_2026_unsolved_problems_mega_atlas.pdf` (`0.672 MB`, `0` overfull hboxes, `0` undefined refs) + deterministic `dist/arxiv_submission.tar.gz` (`0.498 MB`), with **12/12** live-verified URL/DOI citations (`scripts/check_citations.py`).
- **November 25, 2026 RH/GRH Update & Companion Author Preprints Cross-Audit:**
  - Updated `NT-001` & `NT-002` with the Nov 21, 2026 Lean FRO / Mathlib Initiative multi-kernel certification note while keeping all 12 AI proof-claim targets officially unretired.
  - Added transparent cross-map of 7 companion author preprints (`0thernes-research-archive`) across JSON, SQLite, 15-sheet XLSX, HTML Tab 2, `RANKING.md`, and 10th MCP tool `list_author_frontier_contributions` — explicitly verifying **`0 / 1,900` overarching Atlas parent problems retired**.
- **Deep Verification Ladder (`reference/`, `tests/test_properties_and_differential.py`, `scripts/`):**
  - Added independent 50-digit `Decimal`/`Fraction` reference oracle (`reference/scoring_oracle.py`), 1,000-example Hypothesis property suite, 2,000-case randomized + 1,900-row exhaustive differential tests, metamorphic & golden snapshot tests, negative boundary tests, 6-mutant semantic mutation audit (`100%` kill rate via `scripts/run_mutation_audit.py`), and 10-iteration warmed benchmark suite (`scripts/benchmark_atlas.py` → `docs/benchmarks.md` + `results/bench-history.csv`).
- **`< 5 MB` Git Hygiene (A24), WCAG 2.2 AA Web Atlas & Legal/License Alignment:**
  - Refactored `outputs/MegaAtlas_Interactive_Dashboard_V2.html` (`20.64 MB → 3.80 MB`, external `charts/*.png` + columnar JSON + WCAG 2.2 AA accessibility); tracked deterministic `.json.gz` (`1.28 MB`) & `.jsonl.gz` (`1.21 MB`); added auto-building `ensure_sqlite_db()` in `rag/query.py`; moved Chrome directory PDF to gitignored `build/` (attached to GitHub Releases).
  - Upgraded code license to **Apache-2.0** (`LICENSE-CODE`, SPDX headers, `THIRD_PARTY_NOTICES.md`) and replaced inaccurate `"0thernes LLC"` entity strings with `"Independent Researcher, Spokane, WA, USA"` matching ORCID `0009-0006-8168-9648`.
  - Achieved **100.0%** Build Standard v1.2.0 compliance (`repo.yaml`, `justfile`, `CLAIMS.md`, `LIMITATIONS.md`, `REPLICATION.md`, `HARDENING_LOG.md`, `ERRATA.md`, `DEVIATIONS.md`, `SUPPORT.md`, `ROADMAP.md`, `UPGRADING.md`, ADRs, threat model, operations runbook, 10-class issue templates, removed banned PR template, 3-OS + 6-kernel + Tectonic + SLSA CI, `release.yml`, and `1280×640` `docs/media/social-preview.png`).

## [2.3.1] — 2026-11-25

### Fixed & Hardened — Initial Build Standard v1.2.0 Pass, Windows UTF-8 CI Fix & Solved-Problem Cross-Check
- Initial Build Standard v1.2.0 baseline scaffolding, `.gitleaks.toml`, removal of banned PR template, initial `"0thernes LLC"` entity cure, Windows `PYTHONUTF8=1` + explicit UTF-8 subprocess decoding in tests, and `Audit-Repo.ps1` relative-path fix (all superseded and completed to 100.0% in `v2.4.0`).

## [2.3.0] — 2026-11-21

### Added & Fixed — Full Multi-Layer Forensic Audit, Biconnected 1,900-Node Atlas, 100% RAG, 9-Tool Dual-Framed MCP, 72 Lean Theorems & Options 1/2/3
- **Forensic Auditor & Zero-Bug Remediation (`scripts/forensic_audit.py`, `docs/FORENSIC_AUDIT_V2.3.md`):**
  - Fixed **24 dangling `raw_links`** via automatic canonical `dedup_alias_map` redirection in `src/v2_loader.py` → **`unresolved_raw_links_count = 0`**.
  - Merged **7 true cross-field near-duplicate pairs** (`GR-019→ANL-014`, `COMB-047→NT-077`, `AI-026→STAT-046`, `ANL-051→NT-085`, `GEOM-049→ALG-025`, `LOG-018→NT-061`, `STAT-033→GEOM-062`) → `12` total deduplicated overlaps.
  - Eliminated the **last graph articulation point (`GEOM-038`)** via mathematical cross-links on `GEOM-042` & `GEOM-045` → **`articulation_points = 0`**, **`graph_bridges = 0`**, true **2-vertex-connected biconnected connectome** (`5,808` edges, `14` communities).
- **11th Curated Source Module (`src/v2_data/m11_substrates_margins_adjacents.py`, `52` problems, `SUB-001`..`SUB-052`):** Closed 9 forensically detected blindspots across Basal/Plant/Swarm Cognition, Active Inference/FEP, Cryonics/Biostasis, Space Law/Orbital Debris, Mycology/Soil Networks, Photosynthesis/RuBisCO, Epistemic Security/Formalization Fidelity, Virology/Prions, and Optimal Transport/Information Geometry → **`1,900` strictly unique problems**.
- **8 Quantitative Multi-Layer Dimensions (`40 → 48` Typed Columns):** Added `substrate_class` (8 substrates), `abstraction_layer` (`L0–L6`, 7 layers), `epistemic_spectrum_score` (`0–100`), `hardness_tractability_gradient` (`D − T ∈ [-9, +9]`), `css_titan_margin` (`CSS − Titan×10 ∈ [-100, +100]`), `bridge_margin_ratio` (`[0, 1]`), `adjacent_pillars_count` (`[0, 7]`), and `margin_role` (4 structural boundary roles), surfaced across JSON Schema, 14-sheet XLSX, SQLite `substrate_summary`, Dashboard, PDF, and **3 new publication charts (`13`, `14`, `15` → 30 PNG/SVG files)**.
- **Pure Lean 4.35.0 Expansion (`58 → 72` Audited Theorems, 8 Modules, 1,008 Lines):** Added `lean/MegaAtlasProofs/LayerGradients.lean` (14 constructive theorems, zero Mathlib, zero `sorry`, zero `Classical.choice`, strictly `[propext, Quot.sound]` or empty).
- **100.00% MRR@5 Hybrid RAG (`H-003`) & AutoResearch `AQS = 97.99`:** Added contiguous title bigrams + NetworkX `pagerank` authority fusion in `rag/query.py`, reaching **`25/25` top-1 (`100.00% MRR@5`)** on the untouched immutable evaluator (`autoresearch/evaluate.py`).
- **Dual-Framed 9-Tool MCP Server (`mcp_server/server.py`):** Added `get_substrate_layer_summary` & `get_margin_and_gradient_extremes` (**7 → 9 tools**) + automatic support for BOTH NDJSON and LSP/MCP `Content-Length:` stdio framing.
- **Options 1, 2, 3 Preservation & Autonomous Exploration:** Added offline-validated Option 1 Zenodo publisher (`scripts/publish_zenodo.py --dry-run`), Option 1/2 honest archival dossier (`docs/PRESERVATION.md` respecting Software Heritage's Anubis PoW gate), and Option 3 Track B empirical pilot (`research/runs/LOG-002_antihydra_pilot/`) probing Busy Beaver `BB(6)`'s Antihydra map with explicit non-claim boundaries.
- **25-Test `pytest` & Hardened CI:** Expanded `tests/test_mega_atlas.py` from 19 to 25 tests and updated `.github/workflows/ci.yml` to enforce 72 Lean theorems, `forensic_audit.py`, `publish_zenodo.py --dry-run`, and `evaluate.py --verify-gates`.

## [2.2.0] — 2026-11-21

### Added — Karpathy-Style AutoResearch, MCP Server, FAIR Metadata Triad & 58 Pure Lean 4.35.0 Invariants
- **Karpathy-Style Autonomous Research Engine (`autoresearch/`):** Baked in [`program.md`](autoresearch/program.md), immutable [`evaluate.py`](autoresearch/evaluate.py) (5-axis Atlas Quality Score `AQS` + fixed 25-query cross-pillar `MRR@5` benchmark + hard gates), empirical [`results.tsv`](autoresearch/results.tsv) experiment ledger (including real baseline, honest discarded hypothesis `H-001`, and verified `keep` lift `H-001b`), OpenProver-inspired Planner–Worker–Verifier [`whiteboard.md`](autoresearch/whiteboard.md), and [`OSS_STACK.md`](autoresearch/OSS_STACK.md) documenting integration with `karpathy/autoresearch`, `SakanaAI/AI-Scientist`, `kripner/OpenProver`, `lean-dojo/LeanAgent`, `leanprover/skills`, independent Lean kernels (`lean4lean`/`nanoda`), and `teorth/erdosproblems`.
- **Hybrid BM25 + Knowledge-Graph Authority RAG Engine (`rag/query.py`):** Autonomous optimization (`H-001b`) upgraded pure-OR FTS5 retrieval to deduplicated unique-token title/body coverage + log-degree graph authority re-ranking, lifting 25-query cross-pillar `MRR@5` from **89.33% (`21/25` top-1)** to **96.00% (`23/25` top-1)**, plus added `--compare ID_A ID_B`.
- **Zero-Dependency Model Context Protocol (MCP) Server (`mcp_server/server.py`):** Stdio JSON-RPC 2.0 server exposing 7 grounded tools (`search_problems`, `get_problem`, `compare_problems`, `list_nov2026_ai_claims`, `get_top_ranked`, `get_pillar_summary`, `get_atlas_provenance`) for Claude Code, Antigravity, Cursor, and Gemini CLI — tested end-to-end over real stdio in `pytest`.
- **Pure Lean 4.35.0 Expansion (`46 → 58` Audited Theorems, 7 Modules, 817 Lines):** Added `MegaAtlasProofs/AutoResearchInvariants.lean` (12 new theorems, zero Mathlib, zero `sorry`, `[propext, Quot.sound]`) formally proving `AQS` bounds/monotonicity, the **Anti-Reward-Hacking Theorem** (`failed_gates_always_discard`), strict improvement biconditional (`shouldKeep_iff`), non-regression ratchet, and pairwise comparison delta antisymmetry.
- **FAIR Scholarly & Agentic Metadata Triad:** Auto-synced [`.zenodo.json`](.zenodo.json) (GitHub-to-Zenodo Auto-DOI), **MLCommons Croissant 1.0** ([`croissant.json`](croissant.json)), **W3C RO-Crate 1.1** ([`ro-crate-metadata.json`](ro-crate-metadata.json)), deterministic generator [`scripts/generate_fair_metadata.py`](scripts/generate_fair_metadata.py), **Gebru et al. Datasheet** ([`docs/DATASHEET.md`](docs/DATASHEET.md)), [`CITATION.bib`](CITATION.bib), [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), [`llms.txt`](llms.txt) (auto-deployed to GitHub Pages), and [`SECURITY.md`](SECURITY.md).
- **Expanded Verification & CI:** Grew `tests/test_mega_atlas.py` from 13 to 19 tests (adding live MCP stdio JSON-RPC, pairwise antisymmetry, AutoResearch oracle, Zenodo/Croissant/RO-Crate SHA-256 checks), updated CI (`.github/workflows/ci.yml`) to verify all 58 Lean theorems + AutoResearch gate, and updated GitHub Pages (`.github/workflows/pages.yml`) to serve `llms.txt`, `croissant.json`, `ro-crate-metadata.json`, `.zenodo.json`, `CITATION.cff`, and `CITATION.bib`.

## [2.1.0] — 2026-11-21

### Added — Institutional Research Standard Upgrade
- **Pure Lean 4.35.0 Formal Invariant Suite (`lean/MegaAtlasProofs/`):** 6 modules, 686 lines, **46 audited theorems** (zero Mathlib, zero `sorry`, zero `admit`, zero `native_decide`, all `#print axioms` strictly within `[propext, Quot.sound]` or empty) formally verifying exact bounds, monotonicity, weight normalization, and 300-year antiquity saturation of `CSS`, `Titan Index`, and `Near-Term Leverage`, exhaustiveness/monotonicity of the 4-Quadrant and 6-Era classifiers, surjectivity of the 8×28 taxonomy, the finite undirected Handshaking Lemma (`∑ deg = 2|E|`), cross-partition edge hierarchy, and deduplication cardinality bounds.
- **0thernes Composite Severity Score (`css_score`, 0–100):** Unified scoring formula matching sibling repository [`0thernes/unsolved-mathematics`](https://github.com/0thernes/unsolved-mathematics), surfaced across CSV, TSV, JSON, JSONL, SQLite, XLSX, XLS, MD, TXT, Interactive HTML, PDF, and auto-generated `RANKING.md`.
- **Per-Record Epistemic `verification_flag`:** Transparent 4-class epistemic provenance (`primary-registry-indexed`, `ai-assisted-editorial-synthesis`, `ai-claim-under-audit-nov2026`, `disputed-human-claim`) on all 1,855 records.
- **SQLite 3 + FTS5 Database & Streaming JSONL (`outputs/`):** `MegaAtlas_Unsolved_Problems_V2.sqlite` (9 normalized tables + Porter-stemmed FTS5 full-text search index) and `MegaAtlas_Unsolved_Problems_V2.jsonl`.
- **Offline Deterministic RAG CLI (`rag/query.py`):** Zero-API BM25 full-text + multi-hop knowledge-graph neighbor retrieval returning exact Problem IDs, formulas, CSS/Titan scores, and verification flags.
- **Formal JSON Schemas (`schema/problem.schema.json`, `schema/atlas.schema.json`):** Draft 2020-12 contracts validated on every record.
- **Comprehensive `pytest` Suite (`tests/test_mega_atlas.py`) & Standalone Auditor (`scripts/audit_atlas.py`):** Verifying schema, mathematical invariants, graph handshaking, format parity, RAG, ORCID presence, Lean hygiene, and byte-exact SHA-256 digests.
- **Dual-License Separation & Institutional Governance:** `LICENSE` (CC BY 4.0), `LICENSE-CODE` (MIT), `NOTICE`, `VERSION`, `AUTHORS.md`, `PHILOSOPHY.md`, `ARCHITECTURE.md`, `VERIFICATION.md`, `EVIDENCE.md`, `RANKING.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `docs/METHODOLOGY.md`, `docs/AI_DISCLOSURE.md`, `docs/ACADEMIC_REVIEW.md`, `docs/WHITE_PAPER.md`.
- **Build Ergonomics & Community Review:** `requirements.txt`, `pyproject.toml`, `Makefile`, `build.ps1`, structured GitHub Issue & PR templates (`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`).
- **Dual-Job CI & Automated GitHub Pages:** Upgraded `.github/workflows/ci.yml` (Python/pytest/audit + Lean 4.35.0 build) and added `.github/workflows/pages.yml` publishing the interactive atlas to `https://0thernes.github.io/unsolved-problems-mega-atlas/`.
- **Master Archive Registration:** Registered as `0TH-BUILD-007` in `0thernes/0thernes-research-archive`.

### Changed
- Made `src/v2_charts.py` and `src/v2_export_all.py` fully self-contained inside `Z:\unsolved-problems-mega-atlas`, outputting directly to `outputs/`.
- Updated `EXTERNAL_REGISTRIES_NOV2026` self-benchmark row to exact `1,855 rigorously deduplicated problems`.

## [2.0.0] — 2026-11-20

### Added
- Ground-up 10-module parallel rebuild expanding coverage to **1,855 unique, strictly deduplicated problems** across **8 Macro-Pillars × 28 Superdomains** wired into **1 connected 5,597-edge knowledge graph**.
- Live **November 20, 2026 AI Proof-Claim Verification Audit** tracking 12 AI-targeted problems (including Sept 8 Navier–Stokes, Oct 6 722-manuscript bulk release, and Nov 20 Alpöge/Claude Lean RH/GRH + Masullo human draft) and 13 global open-problem registries.
- Exported 12 PNG + 12 Vector SVG charts, CSV, TSV, JSON, 13-sheet live-formula XLSX, 8-sheet Legacy BIFF XLS, Markdown, Plain Text, Interactive HTML Dashboard, and 163-page Vector PDF Monograph.
- Published initial repository with SHA-256 manifest, `CITATION.cff`, and green GitHub Actions CI.

## [1.0.0] — 2026-11-20 (Internal Prototype)

### Added
- Initial 278-problem / 18-domain cross-disciplinary prototype; superseded by V2.0 Mega-Atlas after scale benchmarking against `ProofAtlas.ai` (1,100+) and `erdosproblems.com` (~1,221).
