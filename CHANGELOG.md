# Changelog

All notable changes to the **Unsolved Problems Mega-Atlas** are documented in this file following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [2.1.0] — 2026-11-21

### Added — 0thernes LLC Institutional Research Standard Upgrade
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
