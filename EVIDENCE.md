# Cryptographic & Formal Evidence Dossier (`v2.5.0`)

**Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))
**Date:** November 25, 2026 · **Archive ID:** `0TH-BUILD-007`

## 1. Six-Kernel Lean 4.35.0 Formal Evidence

- **Toolchain:** `leanprover/lean4:v4.35.0` (zero Mathlib, strict compiler options `autoImplicit = false`, `linter.unusedVariables = true`, `linter.deprecated = true`)
- **Audited Theorems:** **92** (`72` core module invariants + `12` concrete NonVacuity & boundary witnesses + `8` Palomar contract specifications)
- **Axiom Allowlist:** Strictly constructive **`[propext, Quot.sound]`** (zero `Classical.choice`, zero `sorryAx`, zero `Lean.ofReduceBool`, zero custom axioms)
- **Frozen Axiom Transcript:** [`results/lean_axioms.txt`](results/lean_axioms.txt) (drift-checked against `README.md` by `scripts/check_readme_axioms.py`)
- **Independent Kernel Replay:**
  1. `lean` (default kernel — `lake build` 16/16 jobs, 0 warnings)
  2. `leanchecker` & `leanchecker-paranoid` (`Solution`, `PalomarSolution` — PASS)
  3. `lean4lean` (verified inside Linux `lake comparator --config comparator.json --paranoid` CI)
  4. `nanoda_bin` (`permitted_axioms: ["propext", "Quot.sound"]`, `nat_extension: true`, `string_extension: true` — PASS)
  5. `con-leche --verified` (`1,753` declarations accepted — PASS)
  6. `con-ron --verified` (`1,753` declarations accepted — PASS)

## 2. Automated Verification Ladder Evidence

| Check | Script / Suite | Observed Evidence (2026-11-25) |
|---|---|---|
| Structural, JSON Schema, Parity & Checksums | `python scripts/audit_atlas.py --check-lean` | `1,900` unique rows, `48` cols, `5,808` edges, `0` APs, `0` bridges, `0` dangling links, 100% SHA-256 parity |
| Forensic Biconnectivity & RAG Audit | `python scripts/forensic_audit.py` | `nx.is_biconnected(G) == True`, `0` dangling links, `0/25` RAG top-1 misses |
| Functional, Hypothesis (1,000 ex.), Differential (2,000+ cases), Metamorphic, Golden & Negative Tests | `pytest tests/ -v` | 100% PASS across all tests |
| Semantic Mutation Audit (B13) | `python scripts/run_mutation_audit.py` | `6/6` mutants killed (`100.0%` kill rate) |
| Static Lint & Typecheck | `ruff check` + `mypy` | `0` lint errors, `0` type errors |
| Immutable AutoResearch Evaluator | `python autoresearch/evaluate.py --verify-gates` | `aqs_score=97.99`, `rag_mrr5=100.00` (`25/25` top-1), `lean_theorems=92`, `hard_gates=PASS` |
| AMS-LaTeX White Paper & arXiv Tarball | `python scripts/build_paper.py && python scripts/check_citations.py` | 11-page PDF (`0.68 MB`, `0` overfull hboxes, `0` warnings), clean-room `arxiv_submission.tar.gz` (`0.50 MB`), `12/12` live HTTP/DOI 200 (`0` Crossref retractions) |
| Reproducible 10-Run Benchmarks | `python scripts/benchmark_atlas.py` | Recorded in [`docs/benchmarks.md`](docs/benchmarks.md) & [`results/bench-history.csv`](results/bench-history.csv) |
| Build Standard v1.2.0 Audit | `pwsh scripts/Audit-Repo.ps1` | **100.0%** Structure / **100.0%** Completion / **100.0%** Core (`0` FAILs) |

## 3. Cryptographic Integrity Manifests & Provenance

- Root manifest: [`CHECKSUMS.sha256`](CHECKSUMS.sha256)
- Data & paper manifest: [`data/MANIFEST.sha256`](data/MANIFEST.sha256)
- FAIR descriptors: [`croissant.json`](croissant.json), [`ro-crate-metadata.json`](ro-crate-metadata.json), [`.zenodo.json`](.zenodo.json)
- Build provenance: GitHub `actions/attest-build-provenance@v2` SLSA attestations on `main` pushes and `v*` releases.
