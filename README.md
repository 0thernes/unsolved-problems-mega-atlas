# Unsolved Problems Mega-Atlas (`v2.7.0`)

[![CI](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/ci.yml)
[![Pages](https://github.com/0thernes/unsolved-problems-mega-atlas/actions/workflows/pages.yml/badge.svg)](https://0thernes.github.io/unsolved-problems-mega-atlas/)
[![Lean 4.35.0](https://img.shields.io/badge/Lean-4.35.0%20%7C%20103%20Thms%20%7C%206%20Kernels-2ea44f)](lean/README.md)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-blue)](LICENSE)
[![Code License: Apache-2.0](https://img.shields.io/badge/Code-Apache--2.0-blue)](LICENSE-CODE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--8168--9648-A6CE39)](https://orcid.org/0009-0006-8168-9648)

![Unsolved Problems Mega-Atlas Social Preview](docs/media/social-preview.png)

> **Status:** `active` · **Version:** `2.7.0` (November 26, 2026) · **Master Archive Entry:** `0TH-BUILD-007`
> **Author / Curator:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))
> **Dual License:** Dataset, Charts, White Paper & Prose [`CC-BY-4.0`](LICENSE) · Code, Lean 4.35.0 Proofs, Tests & Tools [`Apache-2.0`](LICENSE-CODE)
> **Supported locales:** English (`en-US`, UTF-8)

An open-source, cryptographically audited, multi-format cross-disciplinary research infrastructure cataloging **`1,900` strictly deduplicated unsolved, open, and hard problems** spanning **8 Macro-Pillars × 28 Superdomains × 8 Physical/Formal Substrates × 7 Abstraction Layers (`L0–L6`) × 1,752 subdomains**, wired into **1 biconnected `5,808`-edge knowledge graph** (`0` articulation points, `0` bridges, `0` dangling links, `35.7%` cross-superdomain, `18.7%` cross-pillar), paired with:

- **103 Zero-Mathlib Pure Lean 4.35.0 Formal Invariant & Adversarial-Refutation Theorems** (`72` core module invariants + `12` concrete NonVacuity & boundary witnesses + `10` constructive `AdversarialTests` false-variant refutations + `9` Palomar contract specifications) verified across **6 independent proof kernels** (`lean`, `leanchecker --fresh` / `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`, `con-ron`) plus live negative kernel rejection, with constructive axioms strictly within `[propext, Quot.sound]`.
- **10-Page Publication-Grade AMS-LaTeX White Paper** ([`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`](dist/Donahue_2026_unsolved_problems_mega_atlas.pdf), `0` overfull hboxes, `12/12` live-verified citations with `0` Crossref retractions) + deterministic clean-room [`dist/arxiv_submission.tar.gz`](dist/arxiv_submission.tar.gz) + **Dual Cryptographic Timestamping**: DigiCert RFC 3161 ([`CHECKSUMS.sha256.tsr`](CHECKSUMS.sha256.tsr)) + 3-Calendar Bitcoin OpenTimestamps ([`CHECKSUMS.sha256.ots`](CHECKSUMS.sha256.ots)).
- **Live Interactive Web Atlas & Lean Proof Blueprint:** [https://0thernes.github.io/unsolved-problems-mega-atlas/](https://0thernes.github.io/unsolved-problems-mega-atlas/) and [Lean 4.35.0 Proof Blueprint DAG](https://0thernes.github.io/unsolved-problems-mega-atlas/blueprint/) (strict CSP, WCAG 2.2 AA accessible, `< 4 MB`).
- **Offline SQLite FTS5 Hybrid RAG (`100.0% MRR@5`, `25/25` top-1)** + **Zero-Dependency Dual-Framed 10-Tool MCP Server** (`mcp_server/server.py`, `1 MiB` frame cap) + **Immutable Karpathy-Style AutoResearch Harness** (`AQS = 97.99`) + **Track B Antihydra (`LOG-002`) Finite Bigint Pilot**.
- **Deep Verification Ladder:** 50-digit `Decimal`/`Fraction` reference oracle (`reference/scoring_oracle.py`), 1,000-example Hypothesis property suite, 2,000-case differential tests, metamorphic & golden snapshots, and **100% (`6/6`) mutation-kill coverage**.

---

## Honest Verification Boundary (Read First)

1. **Zero (`0 / 1,900`) overarching Mega-Atlas open problems are claimed solved or retired.** Our 103 Lean 4.35.0 theorems verify the atlas's *internal* scoring, quadrant/era, taxonomy, finite graph handshaking, deduplication, AutoResearch ratchet, gradient/margin invariants, non-vacuity, and false-variant refutations **only**.
2. **Author-Curated Companion Archive Entries (`0thernes-research-archive`):** Sixteen independent companion preprints and formal builds (`11` Tier-I + `5` Tier-II across `76` audited public `0thernes` repositories) resolve narrowly scoped published sub-conjectures, formalize complexity barriers, or certify discrete model invariants (cataloged transparently in `paper/main.tex` Section 6, `RANKING.md`, and MCP tool `list_author_frontier_contributions`); all are self-published (not externally peer-reviewed) and explicitly keep every overarching Mega-Atlas parent problem **OPEN**.
3. **November 25, 2026 AI Proof Claims:** All `12` Fall/Nov 2026 AI proof-claim targets (`NT-001` Riemann Hypothesis, `NT-002` GRH, `ANL-001` 3D Navier–Stokes, etc.) remain explicitly flagged `ai-claim-under-audit-nov2026` and **officially unretired** pending human-readable exposition and Clay/community consensus.
4. **Editorial Rubric Disclosure:** Quantitative ratings (`difficulty_score`, `tractability_2050`, `civilizational_impact`, `interdisciplinarity_index`) are disclosed AI-assisted editorial estimates — not peer-reviewed consensus measurements. Edit `src/v2_data/`, run `just build`, and argue from the diff!

---

## 5-Second Lean 4.35.0 Formal Verification

Reproduce the full 103-theorem constructive axiom audit locally in under 10 seconds:

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

On Linux with `bubblewrap`, replay all **6 independent proof kernels** (`lean`, `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`, `con-ron`) using the exact single-source CI verification script:

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

### 3. Model Context Protocol (MCP) 10-Tool Stdio Server

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
just reproduce     # Rebuild exports + pytest + 103-thm Lean audit + AMS-LaTeX paper + SHA-256
just lean-kernels  # Full 6-kernel bubblewrap replay on Linux (lean, leanchecker-paranoid, lean4lean, nanoda, con-leche, con-ron)
just mutate        # 6-mutant semantic mutation testing (100% kill rate)
just bench         # 10-iteration warmed benchmark harness -> docs/benchmarks.md
just audit         # Forensic biconnectivity, Zenodo dry-run & immutable AutoResearch gates
```

---

## Key Artifacts & Exports

| Artifact | Location | Size | Notes |
|---|---|---|---|
| **10-Page AMS-LaTeX White Paper PDF** | [`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`](dist/Donahue_2026_unsolved_problems_mega_atlas.pdf) | `0.68 MB` | Tectonic `amsart`, `0` overfull hboxes, `12/12` live citations (`0` retractions) |
| **Clean-Room arXiv Source Tarball** | [`dist/arxiv_submission.tar.gz`](dist/arxiv_submission.tar.gz) | `0.50 MB` | Deterministic (`mtime=0`), verified clean-room compile |
| **Interactive Web Atlas (WCAG 2.2 AA)** | [`outputs/MegaAtlas_Interactive_Dashboard_V2.html`](outputs/MegaAtlas_Interactive_Dashboard_V2.html) | `3.80 MB` | Live at [GitHub Pages](https://0thernes.github.io/unsolved-problems-mega-atlas/) |
| **Interactive Lean 4.35.0 Blueprint** | [`blueprint/index.html`](blueprint/index.html) | `14 KB` | SVG DAG linking all 103 audited theorems |
| **Tabular & Compressed JSON Exports** | `outputs/*.csv`, `*.tsv`, `*.json.gz`, `*.jsonl.gz`, `*.xlsx` (15 sheets), `*.xls` | `< 5 MB` each | 100% JSON Schema Draft 2020-12 valid; full uncompressed `.sqlite`/`.json`/168p PDF on [GitHub Releases](https://github.com/0thernes/unsolved-problems-mega-atlas/releases) |
| **15 Analytical Figures (PNG + SVG)** | `outputs/charts/01..15.{png,svg}` + `paper/figures/*.pdf` | `35` vector/raster files | Colorblind-safe 8-pillar palette |
| **FAIR Metadata, Checksums & RFC 3161 TSA** | `croissant.json`, `ro-crate-metadata.json`, `.zenodo.json`, `CHECKSUMS.sha256`, `CHECKSUMS.sha256.tsr`, `data/MANIFEST.sha256` | Tracked | Cryptographically synced + DigiCert RFC 3161 timestamped |
| **Falsifiable Claims & Hardening Logs** | [`CLAIMS.md`](CLAIMS.md), [`VERIFICATION.md`](VERIFICATION.md), [`docs/statement-fidelity.md`](docs/statement-fidelity.md), [`docs/literature-search-log.md`](docs/literature-search-log.md), [`HARDENING_LOG.md`](HARDENING_LOG.md) | Tracked | Full multi-cycle, 10-pass red-team audit |

---

## Limitations

See [`LIMITATIONS.md`](LIMITATIONS.md) for the complete analysis and Literal-vs-Metaphor table. Key boundaries:
- Quantitative rubric inputs (`difficulty`, `tractability_2050`, `impact`, `interdisciplinarity`) are solo AI-assisted editorial estimates, not peer-reviewed measurements.
- Pure Mathematics has denser historical registries than applied engineering/humanities (`952` of `1,900` records are flagged `ai-assisted-editorial-synthesis`).
- Lean 4.35.0 certifies discrete structural invariants over bounded inputs; IEEE-754 `log1p` terms are verified differentially against the 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`).
- Neither this dataset nor the companion white paper has undergone external journal peer review.

---

## Citation & Preservation

See [`CITATION.cff`](CITATION.cff) and [`CITATION.bib`](CITATION.bib):

```bibtex
@misc{donahue2026megaatlas,
  author  = {Donahue, Alexander Stephen},
  title   = {Unsolved Problems Mega-Atlas (V2.7.0): A Multi-Layer Taxonomy, Biconnected Knowledge Graph, Six-Kernel Lean 4.35.0 Formal Invariant Suite, and Deterministic Research Infrastructure Across 1,900 Open Problems},
  year    = {2026},
  month   = nov,
  version = {2.7.0},
  url     = {https://github.com/0thernes/unsolved-problems-mega-atlas},
  note    = {ORCID: 0009-0006-8168-9648. Master Archive ID: 0TH-BUILD-007.}
}
```
