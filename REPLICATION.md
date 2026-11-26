# Independent Clean-Clone Replication Protocol & Log (`v2.8.0`)

Per **Build Standard for LLMs v1.2.0 (B43, B44)**, this document provides step-by-step instructions to independently replicate every quantitative result, formal proof, chart, white paper PDF, and benchmark from a fresh git clone — plus the recorded verification log of an actual clean-directory replication run.

## 1. Prerequisites

- Python `3.10+` (`3.12` tested)
- `git`
- Lean 4 via `elan` (`lean/lean-toolchain` pins `leanprover/lean4:v4.35.0` automatically)
- Tectonic (`>= 0.15`) for AMS-LaTeX PDF & clean-room arXiv tarball compilation
- Optional: `just` command runner (every command also runs directly with `python` / `lake`)

## 2. Exact Clean-Clone Replication Steps

```bash
# 1. Clone cleanly into an isolated directory
git clone https://github.com/0thernes/unsolved-problems-mega-atlas.git mega-atlas-repl
cd mega-atlas-repl

# 2. Verify tracked cryptographic manifests and dual timestamps before executing any build script
python -c "import hashlib, pathlib; lines=[l.strip().split(None,1) for l in pathlib.Path('CHECKSUMS.sha256').read_text().splitlines() if l.strip()]; assert all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h for h,p in lines); print(f'OK: {len(lines)} checksums')"
python scripts/stamp_timestamps.py --verify

# 3. Install dependencies in a fresh virtual environment
python -m venv .venv
# Windows: .\.venv\Scripts\python.exe  |  Linux/macOS: .venv/bin/python
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"

# 4. Run full verification suite (auto-builds SQLite FTS5 DB on demand!)
.venv/bin/python -m pytest tests/ -v
.venv/bin/python examples/quickstart_demo.py
.venv/bin/python scripts/audit_atlas.py --check-lean
.venv/bin/python scripts/forensic_audit.py
.venv/bin/python scripts/run_mutation_audit.py
.venv/bin/python scripts/check_readme_axioms.py
.venv/bin/python autoresearch/evaluate.py --verify-gates

# 5. Independently verify Lean 4.35.0 formal proofs (103 theorems)
cd lean && lake clean && lake build && lake env lean MegaAtlasProofs/VerifyAxioms.lean
# Compare verbatim against ../results/lean_axioms.txt (zero diff)
cd ..
# On Linux with bubblewrap (single-source 6-kernel replay + Palomar comparator):
bash scripts/verify_lean_six_kernels.sh

# 6. Independently compile AMS-LaTeX white paper & clean-room arXiv tarball
.venv/bin/python scripts/build_paper.py
.venv/bin/python scripts/check_citations.py
```

## 3. Expected Exact Tolerances

- **Dataset cardinality & topology:** Exact (`1,900` problems, `48` columns, `5,808` edges, `0` articulation points, `0` bridges, `0` dangling links).
- **Lean 4.35.0 axioms:** Byte-exact match against `results/lean_axioms.txt` (`103` lines, axioms `⊆ [propext, Quot.sound]`, zero `Classical.choice`).
- **Differential scoring oracle:** `<= 0.01` rounding tolerance across all `1,900` atlas records + `2,000` randomized inputs.
- **RAG & AutoResearch:** Exact `100.00% MRR@5` (`25/25` top-1), `AQS = 97.99`, `hard_gates = PASS`.
- **Mutation kill rate:** Exact `100.0%` (`6/6` mutants killed).
- **AMS-LaTeX PDF:** `0` overfull hboxes, `0` undefined references/citations, `12/12` live citations (`0` Crossref retractions).

## 4. Recorded Independent Replication Runs (B44)

| Date (UTC) | Environment / OS | Source Tested | Result & Exact Observed Metrics |
|---|---|---|---|
| 2026-11-25 | Windows 11 `x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15 | Fresh git clone of `v2.4.0` from portable `git bundle --all` into `<isolated-temp-dir>` (reusing read-only `.venv` packages) | **PASS** — `CHECKSUMS.sha256` 100% match before build; SQLite FTS5 auto-built cleanly; full `pytest`, `audit_atlas.py --check-lean` (`92` thms), `forensic_audit.py`, `run_mutation_audit.py` (`6/6`), `evaluate.py` (`AQS=97.99`, `100% MRR@5`), `build_paper.py` (`0` overfull), and `check_citations.py` (`12/12`) ALL PASSED with zero errors. |
| 2026-11-26 | Windows 11 `x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15 | Fresh git clone of `v2.5.0` (`7097e55`) from portable `git bundle --all` into `<isolated-temp-dir>` (reusing read-only `.venv` packages) | **PASS** — Pre-build `CHECKSUMS.sha256` `59/59` byte-exact; `pytest` `53/53` PASS; `quickstart_demo.py` PASS; `v2_export_all.py --skip-pdf` deterministic rebuild PASS; fresh Lean 4.35.0 build + `audit_atlas.py --check-lean` (`103` thms) PASS; `forensic_audit.py` (`0` dangling/APs/bridges/misses) PASS; `run_mutation_audit.py` (`6/6` = `100%`) PASS; `check_readme_axioms.py` PASS; `evaluate.py` (`AQS=97.99`, `100% MRR@5`) PASS; `build_paper.py` (`11` pages, `0` overfull, clean-room arXiv tarball) PASS; `ruff`, `mypy`, and `Audit-Repo.ps1` (`100.0%` / `73/73` / `30/30` Core) ALL PASSED. |
| 2026-11-26 | Windows 11 `x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15 | Fresh git clone of `v2.6.0` (`f786115`) from portable `git bundle --all` into `<isolated-temp-dir>` (reusing read-only `.venv` packages) | **PASS** — Pre-build `CHECKSUMS.sha256` `59/59` & `data/MANIFEST.sha256` `11/11` byte-exact + DigiCert RFC 3161 `.tsr` (`Nov 26 03:13:05 2026 GMT`) verified; `pytest` `63/63` PASS (auto-built SQLite FTS5 + live negative Lean 4.35.0 kernel rejection); `quickstart_demo.py` PASS; `v2_export_all.py --skip-pdf` deterministic rebuild PASS (`3.80 MB` HTML); fresh Lean 4.35.0 `17/17` jobs + `audit_atlas.py --check-lean` (`103` thms) PASS; `forensic_audit.py` (`0` dangling/APs/bridges/misses) PASS; `run_mutation_audit.py` (`6/6` = `100%`) PASS; `check_readme_axioms.py` PASS; `evaluate.py` (`AQS=97.99`, `100% MRR@5`) PASS; `build_paper.py` (`10` pages, `0.681 MB`, `0` overfull, clean-room arXiv tarball) PASS; `ruff` (`0`), `mypy` (`0` across 31 files), and `Audit-Repo.ps1` (`100.0%` / `73/73` / `30/30` Core) ALL PASSED. |
| 2026-11-26 | Windows 11 `x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15 | Fresh git clone of `v2.7.0` (`e910e96`) from portable `git bundle --all` into `<isolated-temp-dir>` (reusing read-only `.venv` packages) | **PASS** — Pre-build `CHECKSUMS.sha256` `59/59` & `data/MANIFEST.sha256` `11/11` byte-exact + dual cryptographic timestamps (`CHECKSUMS.sha256.tsr` DigiCert RFC 3161 `Nov 26 10:40:02 2026 GMT` + `CHECKSUMS.sha256.ots` 3-calendar Bitcoin OpenTimestamps) verified; `pytest` `69/69` PASS (auto-built SQLite FTS5 + live negative Lean 4.35.0 kernel rejection + MCP DoS/RAG auto-rebuild/CSP/LF/link regressions); `quickstart_demo.py` PASS; `v2_export_all.py --skip-pdf` deterministic rebuild PASS (`3.80 MB` HTML); fresh Lean 4.35.0 `17/17` jobs + `audit_atlas.py --check-lean` (`103` thms) PASS; `forensic_audit.py` (`0` dangling/APs/bridges/misses) PASS; `run_mutation_audit.py` (`6/6` = `100%`) PASS; `check_readme_axioms.py` PASS; `evaluate.py` (`AQS=97.99`, `100% MRR@5`) PASS; `build_paper.py` (`10` pages, `0.683 MB`, `0` overfull, clean-room `0.500 MB` arXiv tarball) PASS; `ruff` (`0`) and `mypy` (`0`) ALL PASSED. |
| 2026-11-26 | Windows 11 `x86_64`, Python 3.12.10, Lean 4.35.0, Tectonic 0.15 | Fresh git clone of `v2.8.0` (`42461d4`) from portable `git bundle --all` into `<isolated-temp-dir>` (reusing read-only `.venv` packages) | **PASS** — Pre-build `CHECKSUMS.sha256` `59/59` byte-exact + dual cryptographic timestamps (`CHECKSUMS.sha256.tsr` DigiCert RFC 3161 `Nov 26 13:42:45 2026 GMT` + `CHECKSUMS.sha256.ots` 3-calendar Bitcoin OpenTimestamps) verified; `pytest` `75/75` PASS (incl. 3 Track B probes, external registry delta sync, rubric sensitivity diff, 11-tool MCP & live negative Lean kernel rejection); `quickstart_demo.py`, `sync_external_registries.py --offline`, `rubric_override_diff.py` (`rho=0.8886`), `audit_atlas.py --check-lean` (`103` thms), `forensic_audit.py` (`0` dangling/APs/bridges/misses), `check_readme_axioms.py`, `evaluate.py` (`AQS=97.99`, `100% MRR@5`), `build_paper.py` (`10` pages, `0.684 MB`, `0` overfull, clean-room `0.501 MB` arXiv tarball), and `Audit-Repo.ps1` (`100.0%` / `73/73` / `30/30` Core) ALL PASSED. |
