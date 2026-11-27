# System Architecture — Unsolved Problems Mega-Atlas (`V2.9.0`)

See also [`docs/architecture.md`](docs/architecture.md) and Architecture Decision Records in [`docs/adr/`](docs/adr/README.md).

```mermaid
flowchart LR
    A["12 Modular Python Datasets\nsrc/v2_data/m01..m12\n(2,012 raw -> 2,000 unique)"] --> B["Master Loader & Graph Engine\nsrc/v2_loader.py + v2_schema.py\nStrict Enum Check · Dedup Alias Map\n0 Dangling Links · 88 HUBs · Biconnected\n8 Substrates · L0-L6 · 25 Left-to-Solve Fronts"]
    B --> C["Visual Analytics Engine\nsrc/v2_charts.py\n15 PNG+SVG · 5 PDF Figs · Social Card"]
    B --> D["Unified Deterministic Exporter\nsrc/v2_export_all.py"]
    C --> D
    D --> E1["Tabular & Compressed Exports (<5 MB)\nCSV · TSV · JSON.gz · JSONL.gz (48 cols)\n16-Sheet XLSX · build/ 9-Sheet XLS"]
    D --> E2["Offline RAG & 13-Tool MCP\nAuto-Built SQLite 3 + FTS5 Porter\nrag/query.py (100% MRR@5)\nmcp_server/server.py (NDJSON + Content-Length)"]
    D --> E3["Publications, Web Atlas & Daily Sync\n11-Page AMS-LaTeX PDF + arXiv Tarball\nRANKING.md · MD · TXT · Daily 16-Registry Sync\nWCAG 2.2 AA HTML (~3.1 MB) + Blueprint"]
    F["Zero-Mathlib Lean 4.35.0 Model Suite\nlean/ + palomar/ (14 Files · 1,707 Lines)\n103 Audited Model Thms (of 117 decls)\n6 Kernel Checks / 5 Impl. on 9 Targets\n0 sorry in lean/ · [propext, Quot.sound]"] --> G["Deep Verification & 3-OS CI\n50-Digit Oracle · Hypothesis · 10/10 Mutants\nschema/*.json · 105+ pytest · ruff · mypy\nautoresearch/evaluate.py (AQS=98.35)\nCHECKSUMS.sha256 · SLSA Provenance"]
    E1 --> G
    E2 --> G
    E3 --> G
    G --> H["Distribution & Preservation\nGitHub Release v2.9.0 · Daily GitHub Pages\nZenodo CLI/FAIR (Croissant/RO-Crate) · Dual RFC 3161 + OTS\n0thernes-research-archive (0TH-BUILD-007)"]
```

## Directory Map

| Path | Role | License |
|---|---|---|
| `src/v2_schema.py` | Strict enum definitions (`8` Macro-Pillars, `28` Superdomains, `88` `CANONICAL_HUBS`, `P(...)` constructor) | Apache-2.0 |
| `src/v2_data/m01..m12.py` | 12 domain-specialized problem modules (`2,012` raw authored entries, incl. `m11` substrates/margins blindspots & `m12_lefttosolve_programs.py` covering all 25 fronts of `lefttosolve.com/programs`) | CC-BY-4.0 |
| `src/v2_loader.py` | Strict deduplication with `dedup_alias_map` (`0` dangling links), HUB resolution, biconnected NetworkX analytics, 0thernes `CSS`, `Titan Index`, 8 Substrates, 7 Layers (`L0–L6`), Gradients, Margins, Spectrum, Margin Roles, 16-registry & 25-front Left to Solve baselines, & 20-row Cycle-3 archive cross-map | Apache-2.0 |
| `src/v2_charts.py` | Generates 15 analytical figures (PNG + vector SVG = 30 files), 5 vector PDF paper figures, and the `1280×640` social preview card | Apache-2.0 |
| `src/v2_export_all.py` | Deterministic cross-OS exporter for LF CSV/TSV, deterministic `.json.gz`/`.jsonl.gz`, auto-built SQLite+FTS5 (12 tables), deterministic 16-sheet XLSX, `build/` 9-sheet Legacy XLS, MD, TXT, `RANKING.md`, enum-dictionary WCAG 2.2 AA `~3.1 MB` HTML (live-hydrating `./daily_registries.json`), and optional `build/` Directory PDF | Apache-2.0 |
| `lean/` & `palomar/` | Zero-Mathlib Lean 4.35.0 software-model invariant suite certifying **103 audited declarations** (of `117` in `lean/`: `72` core + `12` NonVacuity + `10` AdversarialTests + `9` Palomar comparator targets) across 14 files; `9` Palomar targets pass `6` kernel checks across `5` distinct implementations | Apache-2.0 |
| `paper/` & `dist/` | 11-page Tectonic AMS-LaTeX white paper (`paper/main.tex`, `refs.bib`, 5 PDF figures) compiled to `dist/Donahue_2026_unsolved_problems_mega_atlas.pdf` + clean-room `dist/arxiv_submission.tar.gz` | CC-BY-4.0 |
| `blueprint/` | Interactive SVG Lean 4.35.0 dependency DAG deployed alongside the Web Atlas on GitHub Pages | CC-BY-4.0 |
| `reference/` | Independent 50-digit `Decimal` / `Fraction` reference oracle (`scoring_oracle.py`) with zero shared production code | Apache-2.0 |
| `schema/` | JSON Schema Draft 2020-12 formal contracts (`problem.schema.json` with 48 typed fields, `atlas.schema.json`) | Apache-2.0 |
| `rag/` | Zero-API offline Hybrid BM25 + Title-Bigram + PageRank + graph-hop retrieval CLI (`rag/query.py`, `100.0% MRR@5`, filter-enforced exact-ID lookup, auto-builds SQLite on clean clones) | Apache-2.0 |
| `mcp_server/` | Zero-dependency dual-framed (NDJSON + `Content-Length:`, `1 MiB` cap on both) stdio JSON-RPC 2.0 server exposing **13 grounded research tools** (incl. `simulate_rubric_override`, `get_live_registry_tracker`, and `query_lefttosolve_programs`) | Apache-2.0 |
| `autoresearch/` | Karpathy-style autonomous research loop (`program.md`, immutable `evaluate.py`, empirical `results.tsv`, `whiteboard.md`, `OSS_STACK.md`) | Apache-2.0 |
| `research/runs/` | Three exact finite Track B computational pilots (`LOG-002_antihydra_pilot/`, `NT-005_collatz_parity_pilot/`, `COMB-002_ramsey_witness_pilot/`) with strict non-claim bounds | Apache-2.0 / CC-BY-4.0 |
| `tests/` | Automated **105+ test `pytest` suite** (`test_mega_atlas.py`, `test_properties_and_differential.py`, `test_external_mirrors.py`, `test_sovereign_targets.py`, `golden/top10_css_titan.json`) covering schema, Hypothesis, 50-digit oracle differential, metamorphic, golden, negative, 100% RAG, 13-tool MCP, Left to Solve & daily sync isolation, sovereign target radar, 3 Track B probes, rubric sensitivity, FAIR, Lean & SHA-256 | Apache-2.0 |
| `scripts/` | `audit_atlas.py`, `forensic_audit.py`, `run_mutation_audit.py` (`10/10`), `benchmark_atlas.py`, `build_paper.py`, `check_citations.py` (Crossref + Zenodo title parity & retraction check), `check_readme_axioms.py`, `verify_lean_six_kernels.sh`, `stamp_timestamps.py` (structural ASN.1 + OTS v1 parser), `sync_external_registries.py` (16 trackers + 25 Left to Solve fronts), `sync_lefttosolve.py` (full 59,396-item JSONL mirror + 190-problem crosswalk), `mine_sovereign_targets.py` (offline target radar & Palomar bridge scaffolder), `rubric_override_diff.py`, `generate_fair_metadata.py`, `generate_llms_full.py`, `publish_zenodo.py`, `Audit-Repo.ps1` | Apache-2.0 |
| `data/external/lefttosolve/` | Daily sidecar metadata mirror of all 25 Left to Solve programs (`programs/*.jsonl` `< 4 MB`, `snapshot.json`, `atlas_crosswalk.json` covering 190 Atlas problems + `crosswalk_overrides.json`, `CHANGES.jsonl`, strict-CSP `index.html`, `MANIFEST.sha256`), published on GitHub Pages at `/external/lefttosolve/` (never mutates frozen 2,000-row dataset) | Upstream sources (carved out of CC-BY-4.0; see `THIRD_PARTY_NOTICES.md`) |
| `outputs/` | All `< 5 MB` tracked `v2.9.0` datasets, 15×2 charts, and WCAG 2.2 AA Interactive HTML (heavy `.sqlite`/`.json`/`.jsonl`/`build/*_Legacy.xls`/170+p PDF regenerated deterministically & attached to GitHub Releases) | CC-BY-4.0 |
| `docs/` | `WHITE_PAPER.md`, `DATASHEET.md`, `DAILY_REGISTRY_TRACKER.md`, `FORENSIC_AUDIT_V2.3.md`, `PRESERVATION.md`, `METHODOLOGY.md`, `AI_DISCLOSURE.md`, `ACADEMIC_REVIEW.md`, `statement-fidelity.md`, `literature-search-log.md`, `benchmarks.md`, `threat-model.md`, `operations.md`, `adr/`, `reviews/`, `media/` | CC-BY-4.0 |
| `.github/` | 3-OS + multi-kernel Lean + Tectonic + SLSA CI (`ci.yml`), automated daily 16-registry + 25-front sync (`daily-registry-sync.yml` at `06:00 UTC`), daily GitHub Pages (`pages.yml` at `06:15 UTC`), tag release bundler (`release.yml`), 10-class `labels.tsv`, and structured Issue templates (no PR template per R4) | Apache-2.0 |

## One-Command Reproduction

```bash
just setup && just reproduce && just test && just lean && just paper
# On Linux with bubblewrap (6 kernel checks across 5 implementations):
just lean-kernels
```
