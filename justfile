# SPDX-License-Identifier: Apache-2.0
# Canonical command runner for Unsolved Problems Mega-Atlas (V2.10.0)
# Usage: `just` to list recipes, `just reproduce` to rebuild & verify everything.

set windows-shell := ["pwsh", "-NoLogo", "-Command"]

python := if os() == "windows" { ".venv/Scripts/python.exe" } else { ".venv/bin/python" }

# Show available recipes
default:
    @just --list

# Create local virtual environment and install pinned dev dependencies
setup:
    python -m venv .venv
    {{python}} -m pip install --upgrade pip
    {{python}} -m pip install -e ".[dev]"

# Regenerate all 3 Track B probes, 15 charts, 5 PDF paper figures, social card, exports, FAIR metadata & checksums
build:
    {{python}} research/runs/LOG-002_antihydra_pilot/antihydra_probe.py
    {{python}} research/runs/NT-005_collatz_parity_pilot/collatz_probe.py
    {{python}} research/runs/COMB-002_ramsey_witness_pilot/ramsey_probe.py
    {{python}} src/v2_charts.py
    {{python}} src/v2_export_all.py --skip-pdf
    {{python}} scripts/generate_fair_metadata.py
    {{python}} scripts/generate_llms_full.py
    {{python}} scripts/audit_atlas.py --sync-checksums

# Full end-to-end deterministic reproduction (data + Lean + paper + checksums + tests + audits)
reproduce: build lean paper
    {{python}} scripts/audit_atlas.py --sync-checksums --check-lean
    {{python}} -m pytest tests/ -v
    {{python}} autoresearch/evaluate.py --verify-gates

# Run full pytest suite (functional, property, differential, metamorphic, golden, MCP, FAIR)
test:
    {{python}} -m pytest tests/ -v

# Run static lint checks (ruff)
lint:
    {{python}} -m ruff check src rag mcp_server reference scripts examples tests research

# Run static type checking (mypy)
typecheck:
    {{python}} -m mypy src rag mcp_server reference scripts examples research --ignore-missing-imports

# Run mutation testing audit (assert 100% kill rate across planted mutants)
mutate:
    {{python}} scripts/run_mutation_audit.py

# Run reproducible 10-iteration warmed benchmark suite
bench:
    {{python}} scripts/benchmark_atlas.py

# Build and audit all 103 Pure Lean 4.35.0 theorems + README verbatim axiom parity
lean:
    cd lean && lake build && lake env lean MegaAtlasProofs/VerifyAxioms.lean
    {{python}} scripts/check_readme_axioms.py

# Full 6-kernel bubblewrap replay (Linux: lean, leanchecker-paranoid, lean4lean, nanoda, con-leche, con-ron)
lean-kernels:
    bash scripts/verify_lean_six_kernels.sh

# Compile AMS-LaTeX white paper, package clean-room arXiv tarball & verify citations
paper:
    {{python}} scripts/build_paper.py
    {{python}} scripts/check_citations.py

# Run Build Standard v1.2.0 repository audit and forensic/Zenodo audits
audit:
    {{python}} scripts/audit_atlas.py --check-lean
    {{python}} scripts/forensic_audit.py
    {{python}} scripts/publish_zenodo.py --dry-run
    {{python}} autoresearch/evaluate.py --verify-gates

# Verify GitHub Pages deployment readiness locally
deploy:
    {{python}} src/v2_export_all.py --skip-pdf
    @echo "Pages artifacts ready in outputs/MegaAtlas_Interactive_Dashboard_V2.html, outputs/charts/, blueprint/, llms.txt"

# Verify dual cryptographic timestamps (DigiCert RFC 3161 .tsr + Bitcoin OpenTimestamps .ots)
stamp:
    {{python}} scripts/stamp_timestamps.py --verify

# Poll all 16 public external open-problem registries & 25 Left to Solve fronts (advisory telemetry only; zero auto-retirement)
sync-registries:
    {{python}} scripts/sync_external_registries.py --live --write-daily --write-report

# Mirror every Left to Solve program list into data/external/lefttosolve/ + verify offline
sync-lefttosolve:
    {{python}} scripts/sync_lefttosolve.py --live
    {{python}} scripts/sync_lefttosolve.py --offline

# Verify the committed Left to Solve mirror offline without network access
lefttosolve-check:
    {{python}} scripts/sync_lefttosolve.py --offline

# Mine the offline Left to Solve mirror for sovereign 0thernes frontier targets
sovereign-radar:
    {{python}} scripts/mine_sovereign_targets.py rank --kind open --limit 25

# Run community rubric sensitivity diff (Spearman rho, Kendall tau, Top-25 Jaccard & rank movers)
rubric-diff:
    {{python}} scripts/rubric_override_diff.py --override examples/rubric_override_sample.json

# Print rollback instructions for static GitHub Pages / GitHub Releases
rollback:
    @echo "Rollback procedure: checkout prior release tag (e.g. git checkout v2.9.0) or revert commit on main; GitHub Pages redeploys automatically via .github/workflows/pages.yml. See docs/operations.md."

# Remove untracked build caches while preserving tracked repository files
clean:
    rm -rf build/ paper/build/ .pytest_cache/ .mypy_cache/ .ruff_cache/
