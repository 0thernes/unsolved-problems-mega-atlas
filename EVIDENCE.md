# Cryptographic & Formal Evidence Dossier (`v2.10.0`)

**Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))
**Date:** November 25–26, 2026 · **Archive ID:** `0TH-BUILD-007`

## 1. Lean 4.35.0 Software-Model Formal Evidence

- **Toolchain:** `leanprover/lean4:v4.35.0` (zero Mathlib, strict compiler options `autoImplicit = false`, `linter.unusedVariables = true`, `linter.deprecated = true`)
- **Audited Theorems:** **103** audited declarations (of `117` theorem/lemma declarations in `lean/`: `72` core module invariants + `12` concrete NonVacuity & boundary witnesses + `10` constructive AdversarialTests refutations + `9` Palomar contract targets; `5` private helper lemmas in `GraphInvariants` and `9` intermediate `Solution` wrappers are omitted from `#print axioms`)
- **Axiom Allowlist (Per-Theorem):** Strictly constructive **`[propext, Quot.sound]`** on all 103 `#print axioms` lines (zero `Classical.choice`, zero `sorryAx`, zero `Lean.ofReduceBool`, zero custom axioms; hardened H46 scanner also forbids `unsafe`, `implemented_by`, `@[extern`, and `opaque`). Note: whole-environment `lake check --paranoid` also lists `Classical.choice` from Lean's imported `Init` core.
- **Frozen Axiom Transcript:** [`results/lean_axioms.txt`](results/lean_axioms.txt) (`103` lines; exact line-by-line parity checked by `scripts/audit_atlas.py --check-lean` and README parity checked by `scripts/check_readme_axioms.py`)
- **Multi-Kernel Replay (`scripts/verify_lean_six_kernels.sh` — 6 kernel checks across 5 distinct implementations):**
  1. `lean` (default C++ kernel — `lake build` 17/17 jobs, 0 warnings + live negative kernel rejection test)
  2. `leanchecker --fresh` & `leanchecker-paranoid` (shares Lean's C++ kernel — `Solution`, `PalomarSolution` PASS)
  3. `lean4lean` (Lean implementation — verified inside Linux `bwrap` `lake check --paranoid` & `lake comparator --challenge-from-export=... --paranoid` CI on the `9` Palomar targets)
  4. `nanoda_bin` (Rust — `permitted_axioms: ["propext", "Quot.sound"]`, `nat_extension: true`, `string_extension: true` on `1,769` exported decls — PASS)
  5. `con-leche --verified` (OCaml — `1,769` exported declarations accepted — PASS)
  6. `con-ron --verified` (Rust — `1,769` exported declarations accepted — PASS)

## 2. Automated Verification Ladder Evidence

| Check | Script / Suite | Observed Evidence (2026-11-26) |
|---|---|---|
| Structural, JSON Schema, Parity & Checksums | `python scripts/audit_atlas.py --check-lean` | `2,000` unique rows, `48` cols, `6,108` edges, `0` APs, `0` bridges, `0` dangling links, 100% SHA-256 parity across `78` root files & `13` data manifest files |
| Forensic Biconnectivity & RAG Audit | `python scripts/forensic_audit.py` | `nx.is_biconnected(G) == True`, `0` dangling links, `0/25` RAG top-1 misses |
| Functional, Hypothesis (1,000 ex.), Differential (2,000+ cases), Metamorphic, Golden, Negative & Regression Tests | `pytest tests/ -v` | 100% PASS across all **109** tests (incl. 100/100 verbatim Left to Solve mirror parity, 25-front 59,396-target mirror & 290 crosswalk matches, sovereign target radar, daily sync workflow & checksum isolation, 3 Track B probes with dataset ID parity, filter-enforced exact-ID RAG, 13-tool MCP dual-framing DoS/type/path/length guards, rubric tie-break parity, external registry delta sync, live negative Lean kernel rejection, dual `.tsr`+`.ots` binding, strict CSP, zero-CRLF/BOM & zero broken links) |
| Semantic Mutation Audit (B13) | `python scripts/run_mutation_audit.py` | **`12/12` mutants killed (`100.0%` kill rate)** across scoring, RAG, rubric diff, MCP frame cap, Left to Solve manifest integrity, and all 3 Track B probes |
| Static Lint & Typecheck | `ruff check` + `mypy` (incl. `research/`) | `0` lint errors, `0` type errors |
| Immutable AutoResearch Evaluator | `python autoresearch/evaluate.py --verify-gates` | `aqs_score=98.35`, `rag_mrr5=100.00` (`25/25` top-1), `lean_theorems=103`, `hard_gates=PASS` |
| AMS-LaTeX White Paper & arXiv Tarball | `python scripts/build_paper.py && python scripts/check_citations.py` | 11-page PDF (`0` overfull hboxes, `0` warnings), clean-room `arxiv_submission.tar.gz`, **`15/15` live HTTP/DOI 200 with Crossref/Zenodo title-token parity (`0` retractions)** |
| Daily Open-Problem Registry Sync | `python scripts/sync_external_registries.py --live --write-daily` | `16/16` live HTTP 200 across global trackers + all `25` Left to Solve fronts (`06:00 UTC` daily via `.github/workflows/daily-registry-sync.yml`, isolated from frozen checksums) |
| Reproducible 10-Run Benchmarks | `python scripts/benchmark_atlas.py` | Recorded in [`docs/benchmarks.md`](docs/benchmarks.md) & [`results/bench-history.csv`](results/bench-history.csv) |
| Build Standard v1.2.0 Audit | `pwsh scripts/Audit-Repo.ps1` | **98.6%** (`72/73`, `29/30` Core) — sole FAIL is `A23` flagging 2 immutable historical `github-actions[bot]` daily-sync commits (`4688cf8`, `af0a850`); workflow cured for all future commits and exception declared transparently in [`DEVIATIONS.md`](DEVIATIONS.md) (`H-913`) |

## 3. Cryptographic Integrity Manifests, Structurally Verified Dual Timestamping & Provenance

- Root manifest: [`CHECKSUMS.sha256`](CHECKSUMS.sha256) (`78` tracked core source, Lean, paper, Track B, FAIR, chart & export files; daily telemetry files intentionally excluded so daily auto-sync never breaks frozen release seals)
- **DigiCert RFC 3161 Trusted Timestamp (Playbook v1.3 Item 26):** [`CHECKSUMS.sha256.tsr`](CHECKSUMS.sha256.tsr) — structurally verified via `openssl ts -reply -text` (`Status: Granted.` + exact `Message data:` hex digest match) in `python scripts/stamp_timestamps.py --verify`
- **Bitcoin OpenTimestamps Multi-Calendar Proof (Playbook v1.3 Item 26):** [`CHECKSUMS.sha256.ots`](CHECKSUMS.sha256.ots) — full OpenTimestamps v1 binary Merkle/fork tree parsed with zero trailing bytes across 3 independent HTTPS calendars in `python scripts/stamp_timestamps.py --verify`
- Data & paper manifest: [`data/MANIFEST.sha256`](data/MANIFEST.sha256) (`13` files incl. all 3 Track B `RESULTS.json` & `results/registry_delta.json`)
- FAIR descriptors: [`croissant.json`](croissant.json), [`ro-crate-metadata.json`](ro-crate-metadata.json), [`.zenodo.json`](.zenodo.json)
- Build provenance: GitHub `actions/attest-build-provenance@v2` SLSA attestations on `main` pushes and `v*` releases (attesting PDF, arXiv tarball, `results/lean_axioms.txt`, `CHECKSUMS.sha256`, `CHECKSUMS.sha256.tsr`, and `CHECKSUMS.sha256.ots`).
