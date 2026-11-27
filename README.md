# Unsolved Problems Mega-Atlas (`v2.11.0`)

[![CI](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/ci.yml)
[![Daily Registry Sync](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/daily-registry-sync.yml/badge.svg)](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/daily-registry-sync.yml)
[![Pages](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/pages.yml/badge.svg)](https://0thernes.github.io/unsolved-problems-mega-atlas/)
[![Lean 4.35.0](https://img.shields.io/badge/Lean-4.35.0%20%7C%20103%20audited%20model%20theorems-2ea44f)](lean/README.md)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-blue)](LICENSE)
[![Code License: Apache-2.0](https://img.shields.io/badge/Code-Apache--2.0-blue)](LICENSE-CODE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--8168--9648-A6CE39)](https://orcid.org/0009-0006-8168-9648)

![Unsolved Problems Mega-Atlas Social Preview](docs/media/social-preview.png)

> **Status:** `active` · **Version:** `2.11.0` (November 27, 2026) · **Master Archive Entry:** `0TH-BUILD-007`
> **Author / Curator:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))
> **Dual License:** Dataset, Charts, White Paper & Prose [`CC-BY-4.0`](LICENSE) · Code, Lean 4.35.0 Proofs, Tests & Tools [`Apache-2.0`](LICENSE-CODE)
> **Supported locales:** English (`en-US`, UTF-8)

An open dataset and software suite that catalogues **`2,000` deduplicated unsolved, open and hard problems** across **8 Macro-Pillars × 28 Superdomains × 8 Physical/Formal Substrates × 7 Abstraction Layers (`L0–L6`) × 1,851 subdomains** — including `100` strictly non-duplicate open conjectures verified verbatim across the **`25` baseline fronts of [Left to Solve](https://lefttosolve.com/programs)** (backed by a daily-synced `26`-front / `62,790`-target local mirror and `291` crosswalk matches; `2,549` Lean-4 formalized open as of Nov 27, 2026) — linked in a **`6,108`-edge knowledge graph** that the Python audit (NetworkX) finds biconnected (`0` articulation points, `0` bridges, `0` dangling links, `36.3%` cross-superdomain, `18.9%` cross-pillar). It comes with:

- **103 audited Lean 4.35.0 theorems without Mathlib** (of `117` declarations in `lean/`; `14` tracked `.lean` files / `1,711` lines across `lean/` + `palomar/`) about the atlas *software model*: `72` in the core modules, `12` NonVacuity witnesses, `10` `AdversarialTests` refutations of weakened variants and `9` Palomar contract theorems (`5` private helper lemmas in `GraphInvariants` and `9` intermediate `Solution` wrappers are not in `#print axioms`). All declarations are kernel-checked by Lean (`lake build`, `leanchecker --fresh`, `leanchecker-paranoid`); the `9` comparator targets in `lean/comparator.json` pass six kernel checks across five distinct implementations in Ubuntu CI (`lean` and `leanchecker-paranoid`, `lean4lean`, `nanoda`, `con-leche`, `con-ron`), alongside a live negative rejection test confirming Lean rejects a deliberately false theorem. Each audited theorem depends on at most `propext` and `Quot.sound` (`#print axioms`); whole-environment `lake check --paranoid` output also lists `Classical.choice` from Lean core. Several counted theorems are literal arithmetic identities or hypothesis restatements.
- **11-page AMS-LaTeX white paper** ([`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`](dist/Donahue_2026_unsolved_problems_mega_atlas.pdf); `0` overfull hboxes/vboxes; `scripts/check_citations.py` reports `15/15` citations reachable with Crossref/Zenodo title-token parity and `0` retractions), a deterministic clean-room source tarball [`dist/arxiv_submission.tar.gz`](dist/arxiv_submission.tar.gz) (log-audited with `0` warnings), and structurally verified timestamps of `CHECKSUMS.sha256` from DigiCert RFC 3161 ([`CHECKSUMS.sha256.tsr`](CHECKSUMS.sha256.tsr), ASN.1 verified) and Bitcoin OpenTimestamps v1 ([`CHECKSUMS.sha256.ots`](CHECKSUMS.sha256.ots), full binary tree parsed across 3 calendars).
- **Automated Daily Sync of All 16 Open-Problem Lists & Live Left to Solve Fronts:** [`.github/workflows/daily-registry-sync.yml`](.github/workflows/daily-registry-sync.yml) polls `lefttosolve.com/api/stats`, `lefttosolve.com/programs` (all `26` live fronts / `62,790` targets), `google-deepmind/formal-conjectures`, `teorth/erdosproblems`, Clay CMI, `erdosproblems.com`, `proofatlas.ai`, Open Problem Garden, Wikipedia (math/physics/CS), `bbchallenge.org`, Kourovka (`arXiv:1401.0300`), IQOQI Open Quantum Problems, Lean FRO RH statement, and `0thernes-research-archive` **daily at `06:00 UTC`**, verifying the full `pytest tests/` suite before updating [`docs/DAILY_REGISTRY_TRACKER.md`](docs/DAILY_REGISTRY_TRACKER.md), [`docs/lefttosolve-programs.md`](docs/lefttosolve-programs.md), [`results/daily_registries.json`](results/daily_registries.json), [`results/lefttosolve_programs.json`](results/lefttosolve_programs.json), and [`results/daily_registry_history.jsonl`](results/daily_registry_history.jsonl) (advisory telemetry only — zero automatic problem retirement; isolated outside frozen `CHECKSUMS.sha256` timestamps; live-hydrated onto GitHub Pages daily at `06:15 UTC`).
- **Live Interactive Web Atlas, Left to Solve 62k Mirror & Lean Proof Blueprint:** [https://0thernes.github.io/unsolved-problems-mega-atlas/](https://0thernes.github.io/unsolved-problems-mega-atlas/), [Left to Solve 26-Front Mirror (62,790 targets / 291 crosswalk matches)](https://0thernes.github.io/unsolved-problems-mega-atlas/external/lefttosolve/), and [Lean 4.35.0 Proof Blueprint DAG](https://0thernes.github.io/unsolved-problems-mega-atlas/blueprint/) (strict CSP, WCAG 2.2 AA accessible, `< 4 MB`, auto-hydrates daily registry JSON).
- **Offline SQLite FTS5 hybrid search** (`100.0%` MRR@5, `25/25` top-1 on the benchmark queries, enforcing filters on exact-ID queries with atomic DB rebuilds) and a **13-tool MCP server** with no external SDK (`mcp_server/server.py`, `1 MiB` frame cap + `-32602` `params`/object validation on both NDJSON and `Content-Length:`, including `simulate_rubric_override`, `get_live_registry_tracker`, and `query_lefttosolve_programs`), an offline read-only sovereign `formal-conjectures` target radar (`scripts/mine_sovereign_targets.py`), a fixed AutoResearch evaluation harness modelled on Karpathy's `autoresearch` (`AQS = 98.35`), and **3 finite Track B probes** (`LOG-002` Antihydra, `NT-005` Collatz, `COMB-002` Ramsey witnesses) whose parent problems stay open.
- **Python verification ladder:** `115`-test `pytest` suite, 50-digit `Decimal`/`Fraction` reference oracle (`reference/scoring_oracle.py`), 1,000-example Hypothesis property suite, 2,000-case differential tests, metamorphic and golden snapshots, strict `mypy --check-untyped-defs` (`0` errors across `42` files), `100%` non-exempt SPDX coverage, and a semantic mutation audit that kills all `14/14` planted mutants.

---

## Honest Verification Boundary (Read First)

1. **Zero (`0 / 2,000`) Mega-Atlas open problems are solved or retired by this work.** The 103 audited Lean 4.35.0 theorems concern the atlas *software model* only: bounds of the CSS, Titan, leverage and AQS formulas for in-range inputs, monotonicity of CSS, Titan and leverage, quadrant and era maps, sizes of the taxonomy lists, a generic handshaking lemma for list multigraphs, a dedup bound, the AutoResearch keep/discard rule, gradient and margin bounds, non-vacuity witnesses and refutations of weakened variants. No Lean statement refers to the 2,000-row data, its 6,108-edge graph or biconnectivity; those properties, and Lean-to-Python formula agreement, are checked by Python tests.
2. **Author's companion archive entries (`0thernes-research-archive`):** The authoritative list of the author's results is the Cycle-3 archive ledger [`RESULTS.md`](https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md) (`94` audited results across `28` entries: Section A open questions from the literature answered `= 3`, B new theorems `= 11`, C bounded/partial cases `= 11`, D refutations `= 0`, E known results formalized `= 55`, F engineering invariant suites `= 14`, with `R85` being this repository `0TH-BUILD-007`). Section A holds R1 (Banić–Elezović Conjecture 7.7, `0TH-2026-006`) and R44, R45 (questions of Muller–Saniga and Jonah, `0TH-2026-009`). All `27` other audited entries are cross-mapped into `20` companion rows in `src/v2_loader.py`, `paper/main.tex` Table 4, `RANKING.md`, and MCP tool `list_author_frontier_contributions` (`0TH-BUILD-006` is excluded as zero-Lean at pin). All entries are self-published, unreviewed preprints/builds, and every Mega-Atlas parent problem stays **OPEN**.
3. **Fall/November 2026 AI proof claims:** All `12` targets (`NT-001` Riemann Hypothesis, `NT-002` GRH, `ANL-001` 3D Navier–Stokes, etc.) stay flagged `ai-claim-under-audit-nov2026` and officially unretired pending human-readable exposition and Clay CMI / mathematical community consensus (checked with `just sync-registries`; see [`docs/registry-delta-2026-11-26.md`](docs/registry-delta-2026-11-26.md)). Primary sources for the November 20–21, 2026 Alpöge/Claude Lean RH/GRH archive (`175,187` files, `~17M` lines, followed by a Nov 22 working draft and Nov 25 `lsernau/grh-lean` compact rewrite): the [Lean FRO & Mathlib Initiative joint statement (Nov 21, 2026)](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) and [M. Rubinstein's independent verification page](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/). None of those claims is the author's own work.
4. **Editorial Rubric Disclosure & Sensitivity Simulator:** Quantitative ratings (`difficulty_score`, `tractability_2050`, `civilizational_impact`, `interdisciplinarity_index`) are disclosed AI-assisted editorial estimates — not peer-reviewed consensus measurements. Custom weights or per-problem overrides can be tested with `just rubric-diff` (`scripts/rubric_override_diff.py`) or MCP tool `simulate_rubric_override`.

---

## Reproducing the Lean 4.35.0 Audit

Reproduce the axiom audit of the 103 theorems locally:

```bash
cd lean
lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
```

Verbatim Palomar headline theorem audit from [`results/lean_axioms.txt`](results/lean_axioms.txt) (drift-checked in CI via `scripts/check_readme_axioms.py`):

<!-- LEAN_AXIOMS_START -->
```text
'MegaAtlasProofs.Palomar.m1_scoring_invariants' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m2_quadrant_and_era_invariants' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m3_taxonomy_invariants' depends on axioms: [propext]
'MegaAtlasProofs.Palomar.m4_graph_and_dedup_invariants' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m5_autoresearch_ratchet_invariants' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m6_layer_gradient_margin_invariants' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m7_nonvacuity_certificate' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.m8_adversarial_refutations' depends on axioms: [propext, Quot.sound]
'MegaAtlasProofs.Palomar.prove_all_mega_atlas_invariants' depends on axioms: [propext, Quot.sound]
```
<!-- LEAN_AXIOMS_END -->

On Linux with `bubblewrap`, run the kernel checks used in CI (6 checks across 5 distinct implementations: Lean default and paranoid modes, `lean4lean`, `nanoda`, `con-leche`, `con-ron`) with the same script CI uses. `nanoda`, `con-leche` and `con-ron` check an export of three headline theorems and their dependency closure; the Palomar comparator checks the 9 targets in `lean/comparator.json`:

```bash
bash scripts/verify_lean_six_kernels.sh   # or: just lean-kernels
```

---

## Usage

### 1. Quickstart Setup & Demo (Zero API Keys, 100% Offline)

```bash
git clone https://github.com/0thernes/unsolved-problems-mega-atlas.git
cd unsolved-problems-mega-atlas
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
python examples/quickstart_demo.py
```

### 2. Offline Hybrid RAG Search & Side-by-Side Comparison

The SQLite FTS5 index auto-builds deterministically in `< 1 s` on first run on a clean clone:

```bash
python rag/query.py "turbulence climate sensitivity" --top 8 --hops 1
python rag/query.py --problem NT-001 --hops 1
python rag/query.py --compare NT-001 CS-001
python rag/query.py --flag ai-claim-under-audit-nov2026 --top 15
```

### 3. Model Context Protocol (MCP) 13-Tool Stdio Server

Connect Claude Code, Antigravity, Cursor, or Gemini CLI directly (zero external MCP SDK required):

```json
{
  "mcpServers": {
    "unsolved-problems-mega-atlas": {
      "command": "python",
      "args": ["mcp_server/server.py"]
    }
  }
}
```

### 4. Full Deterministic Rebuild & Verification (`justfile`)

```bash
just reproduce       # Rebuild exports + pytest + 103-theorem Lean axiom audit + AMS-LaTeX paper + SHA-256
just lean-kernels    # 6 kernel checks (5 implementations) under bubblewrap on Linux + live negative rejection
just mutate          # 14-mutant semantic mutation testing (requires 14/14 kill rate)
just bench           # 10-iteration warmed benchmark harness -> docs/benchmarks.md
just audit           # Python biconnectivity audit, Zenodo dry-run & AutoResearch gates
just sync-registries # Live advisory delta check across all 16 trackers & 26 Left to Solve fronts
just rubric-diff     # Sensitivity diff (Spearman rho, Kendall tau, Top-25 Jaccard & rank movers)
```

---

## Key Artifacts & Exports

| Artifact | Location | Size | Notes |
|---|---|---|---|
| **11-Page AMS-LaTeX White Paper PDF** | [`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`](dist/Donahue_2026_unsolved_problems_mega_atlas.pdf) | `< 1 MB` | Tectonic `amsart`, `0` overfull hboxes, `15/15` title-verified citations (`0` retractions) |
| **Clean-Room arXiv Source Tarball** | [`dist/arxiv_submission.tar.gz`](dist/arxiv_submission.tar.gz) | `< 1 MB` | Deterministic (`mtime=0`), verified clean-room compile |
| **Interactive Web Atlas (WCAG 2.2 AA)** | [`outputs/MegaAtlas_Interactive_Dashboard_V2.html`](outputs/MegaAtlas_Interactive_Dashboard_V2.html) | `~3.1 MB` (`< 4 MB`) | Live at [GitHub Pages](https://0thernes.github.io/unsolved-problems-mega-atlas/) with daily JSON hydration |
| **Interactive Lean 4.35.0 Blueprint** | [`blueprint/index.html`](blueprint/index.html) | `15 KB` | SVG DAG linking all 103 audited software-model theorems |
| **Daily Open-Problem Registry Tracker** | [`docs/DAILY_REGISTRY_TRACKER.md`](docs/DAILY_REGISTRY_TRACKER.md), [`results/daily_registries.json`](results/daily_registries.json), [`results/lefttosolve_programs.json`](results/lefttosolve_programs.json) | Tracked | Auto-synced daily (`06:00 UTC`) across 16 global registries & all 26 Left to Solve fronts |
| **Tabular & Compressed JSON Exports** | `outputs/*.csv`, `*.tsv`, `*.json.gz`, `*.jsonl.gz`, `*.xlsx` (16 sheets) | `< 5 MB` each | 100% JSON Schema Draft 2020-12 valid; full uncompressed `.sqlite`/`.json`/`build/*_Legacy.xls`/170+p PDF on [GitHub Releases](https://github.com/0thernes/unsolved-problems-mega-atlas/releases) |
| **15 Analytical Figures (PNG + SVG)** | `outputs/charts/01..15.{png,svg}` + `paper/figures/*.pdf` | `35` vector/raster files | Colorblind-safe 8-pillar palette |
| **FAIR Metadata, Checksums & Dual Timestamps** | `croissant.json`, `ro-crate-metadata.json`, `.zenodo.json`, `CHECKSUMS.sha256`, `CHECKSUMS.sha256.tsr`, `CHECKSUMS.sha256.ots`, `data/MANIFEST.sha256` | Tracked | `78`-file root SHA-256 manifest + structurally verified DigiCert RFC 3161 `.tsr` & Bitcoin OTS v1 `.ots` |
| **Falsifiable Claims & Hardening Logs** | [`CLAIMS.md`](CLAIMS.md), [`VERIFICATION.md`](VERIFICATION.md), [`docs/statement-fidelity.md`](docs/statement-fidelity.md), [`docs/literature-search-log.md`](docs/literature-search-log.md), [`HARDENING_LOG.md`](HARDENING_LOG.md), [`ERRATA.md`](ERRATA.md) | Tracked | Internal adversarial audit logs (not external peer review); Round 8 `v2.11.0` hardened daily 26-front sync (`62,790` targets, `291` crosswalk matches), MCP `-32602` & atomic SQLite, strict `mypy`, 100% non-exempt SPDX, `14/14` mutants & `115` pytest checks |

---

## Limitations

See [`LIMITATIONS.md`](LIMITATIONS.md) for the complete analysis and Literal-vs-Metaphor table. Key boundaries:
- Quantitative rubric inputs (`difficulty`, `tractability_2050`, `impact`, `interdisciplinarity`) are solo AI-assisted editorial estimates, not peer-reviewed measurements.
- Pure Mathematics has denser historical registries than applied engineering/humanities (`942` of `2,000` records are flagged `ai-assisted-editorial-synthesis`).
- Lean 4.35.0 checks integer and list invariants of the scoring software model over bounded inputs, not the atlas data; IEEE-754 `log1p` terms are checked differentially against the 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`).
- Neither this dataset nor the companion white paper has undergone external journal peer review.

---

## Citation & Preservation

See [`CITATION.cff`](CITATION.cff) and [`CITATION.bib`](CITATION.bib):

```bibtex
@misc{donahue2026megaatlas,
  author  = {Donahue, Alexander Stephen},
  title   = {Unsolved Problems Mega-Atlas (V2.11.0): A Multi-Layer Taxonomy, Biconnected Knowledge Graph, Lean 4.35.0 Software-Model Invariant Suite, and Daily-Synced Research Infrastructure Across 2,000 Open Problems},
  year    = {2026},
  month   = nov,
  version = {2.11.0},
  url     = {https://github.com/0thernes/unsolved-problems-mega-atlas},
  note    = {ORCID: 0009-0006-8168-9648. Master Archive ID: 0TH-BUILD-007.}
}
```
