# Upgrading Guide

This document describes breaking and non-breaking changes when upgrading between major and minor releases of the **Unsolved Problems Mega-Atlas**.

## Upgrading from `v2.7.0` to `v2.8.0`

### 1. Live 43-Entry Companion Archive Sync (`16` → `17` Rows; `0 / 1,900` Parents Retired)
- Expanded `OTHERNES_VERIFIED_FRONTIER_CONTRIBUTIONS` in `src/v2_loader.py` from `16` to **`17` companion rows** reflecting all `43` public entries in `0thernes-research-archive` (`93b306b`), adding `0TH-BUILD-013` (`alife-singularity-omega-package v3.4.0`) & `0TH-BUILD-015` (`glitchling-jam v2.3.0`) and updating `cellulogonic-mecha v1.6.0`, `cellular-engine-omega v5.3.0`, `xiaomi-17t-pro-lab v3.1.0`, `autophage v1.4.0`, `noetic-organism-omega v2.1.0`, and `asmodensius-native v1.1.0`. Cached SQLite databases automatically rebuild cleanly on upgrade.

### 2. Automated External Registry Delta Auditor & Two New Track B Probes
- Added `scripts/sync_external_registries.py` (`just sync-registries`) for advisory live/offline diffing against `claymath.org`, `erdosproblems.com`, and `proofatlas.ai`.
- Added two exact finite Track B computational probes (`research/runs/NT-005_collatz_parity_pilot/` and `research/runs/COMB-001_ramsey_witness_pilot/`) wired into `just build`.

### 3. Community Rubric Sensitivity Diff Engine & 11th MCP Tool (`simulate_rubric_override`)
- Added `scripts/rubric_override_diff.py` (`just rubric-diff`, sample in `examples/rubric_override_sample.json`) and exposed `simulate_rubric_override` as the 11th tool in `mcp_server/server.py`. All existing 10 MCP tool signatures remain 100% backwards-compatible.

## Upgrading from `v2.6.0` to `v2.7.0`

### 1. Live 76-Repo Companion Archive Expansion (`12` → `16` Verified Entries; `0 / 1,900` Parents Retired)
- Expanded `OTHERNES_VERIFIED_FRONTIER_CONTRIBUTIONS` in `src/v2_loader.py` (propagated across JSON, SQLite, 15-sheet XLSX, HTML Tab 2, `RANKING.md`, `paper/main.tex` Table 4, and MCP tool `list_author_frontier_contributions`) from `12` to **`16` live-verified companion entries** (`11` Tier-I + `5` Tier-II across `76` public `0thernes` repos) — adding `0TH-2026-014` (`monodromia v1.0.0`), `0TH-2026-015` (`promislow-fracton-amoeba v1.0.0`), `0TH-2026-016` (`zero-error-torus-frontier v1.0.0`), and `0TH-BUILD-012` (`xiaomi-17t-pro-lab v3.0.0`), and upgrading 8 existing entries. Every overarching Mega-Atlas parent problem remains **OPEN** (`0 / 1,900` retired).

### 2. Dual Cryptographic Timestamping (RFC 3161 `.tsr` + Bitcoin OpenTimestamps `.ots`) & Acyclic RO-Crate
- Added [`scripts/stamp_timestamps.py`](scripts/stamp_timestamps.py) (`just stamp`) minting and verifying BOTH `CHECKSUMS.sha256.tsr` (DigiCert RFC 3161) and `CHECKSUMS.sha256.ots` (3-calendar Bitcoin OpenTimestamps) — verified inside `scripts/audit_atlas.py`, CI, and `pytest`, and attested via SLSA.
- Fixed `scripts/generate_fair_metadata.py` to exclude `.tsr`/`.ots` from self-referential hashing inside `ro-crate-metadata.json`.

### 3. Runtime Security, Freshness & Strict CSP Hardening
- Fixed `rag/query.py` (`search_atlas` / `compare_two_problems`) to always check `_db_is_fresh()` on `DEFAULT_DB` (backed by an `O(1)` stat cache) so cached `.sqlite` databases auto-rebuild transparently on version upgrades.
- Hardened `mcp_server/server.py` with a `1 MiB` `Content-Length` frame ceiling, `4,096`-char query cap, and strict integer parsing rejecting JSON booleans.
- Added strict zero-CDN `Content-Security-Policy` + `Referrer-Policy` headers on both `outputs/MegaAtlas_Interactive_Dashboard_V2.html` and `blueprint/index.html` (plus WCAG 2.2 AA skip-link & `<main>` landmark on `blueprint/index.html`).

## Upgrading from `v2.5.0` to `v2.6.0`

### 1. Live Companion Archive Expansion (`10` → `12` Verified Entries; `0 / 1,900` Parents Retired)
- Expanded `OTHERNES_VERIFIED_FRONTIER_CONTRIBUTIONS` in `src/v2_loader.py` (propagated across JSON, SQLite, 15-sheet XLSX, HTML Tab 2, `RANKING.md`, `paper/main.tex` Table 3, and MCP tool `list_author_frontier_contributions`) from `10` to **`12` live-verified companion entries** — updating `0TH-2026-012` (`v3.0.0`, 23 thms), `0TH-2026-011` (`v2.4.0`), `0TH-2026-006` (`v2.1.0`), `0TH-2026-004` (`v1.9.0`), `0TH-BUILD-003` (`v1.4.1`), and adding `0TH-2026-013` (`p-vs-np-frontier-lab v1.1.0`) and `0TH-BUILD-004` (`unsolved-mathematics v0.5.0`). Every overarching Mega-Atlas parent problem remains **OPEN** (`0 / 1,900` retired).

### 2. SQLite Auto-Rebuild on Upgrade & Hardened MCP Input Clamping
- `rag/query.py` (`ensure_sqlite_db`) now checks the cached database's `metadata.atlas_version` and `author_frontier_contributions` row count against the active codebase and automatically rebuilds `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` on version upgrades — preventing stale local caches.
- `mcp_server/server.py` now strictly clamps `top ∈ [1, 50]` and `hops ∈ [0, 1]` and validates required arguments (`problem_id`, `id_a`, `id_b`) with structured `isError: true` responses instead of raw `KeyError`.

### 3. Live Negative Lean Kernel Rejection & DigiCert RFC 3161 Timestamp
- `scripts/verify_lean_six_kernels.sh` now invokes `lake env leanchecker --fresh` and runs a live negative Lean 4.35.0 kernel rejection test asserting that a deliberately false theorem (`1 = 2`) is rejected by the kernel with non-zero exit code (Playbook v1.3 Item 12).
- Added a real DigiCert RFC 3161 Trusted Timestamp token (`CHECKSUMS.sha256.tsr`) cryptographically binding the SHA-256 imprint of `CHECKSUMS.sha256` to a verifiable third-party clock (Playbook v1.3 Item 26).

## Upgrading from `v2.4.0` to `v2.5.0`
- Expanded Pure Lean 4.35.0 formal invariants from `92` to **`103` audited theorems** by adding `lean/MegaAtlasProofs/AdversarialTests.lean` (`10` constructive `¬P` refutations bundled into `M8_AdversarialRefutations`, `9` Palomar targets) verified via single-source `scripts/verify_lean_six_kernels.sh`.
- Added live Crossref retraction checking in `scripts/check_citations.py`, 100% REUSE/SPDX headers across code/Lean/shell files, 1-to-1 `C1`–`C10` parity between `CLAIMS.md` and `paper/main.tex`, and SLSA attestation of `results/lean_axioms.txt`.

## Upgrading from `v2.3.0` to `v2.4.0`

### 1. Code License Alignment (`MIT` → `Apache-2.0`)
- All source code, Lean 4.35.0 proof modules, tests, and scripts are now dual-licensed under **Apache-2.0** (`LICENSE-CODE`), aligning with Lean 4 / Mathlib and all companion `0thernes` repositories.
- Dataset, figures, prose, and the AMS-LaTeX white paper remain **CC-BY-4.0** (`LICENSE`).

### 2. Git-Tracked Artifact Hygiene (`< 5 MB` Rule — Build Standard A24)
- Heavy derived artifacts (`outputs/MegaAtlas_Unsolved_Problems_V2.sqlite`, `.json`, `.jsonl`, and the 168-page Chrome-printed Directory PDF) are no longer committed directly to git history.
- **Tracked in git:** `.csv`, `.tsv`, deterministic `.json.gz` & `.jsonl.gz`, 15-sheet `.xlsx`, 8-sheet `.xls`, `.md`, `.txt`, `< 4 MB` Interactive HTML dashboard, 30 PNG/SVG charts, and the Tectonic AMS-LaTeX white paper PDF (`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`) + `dist/arxiv_submission.tar.gz`.
- **Automatic regeneration:** Running `python rag/query.py ...` or `python mcp_server/server.py` on a fresh clone automatically builds `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` in `< 1 s`. Running `python src/v2_export_all.py` regenerates every uncompressed file locally; all full release bundles are also attached to **GitHub Release `v2.4.0`**.

### 3. Lean 4.35.0 Module System & Palomar Verification
- All Lean files now use Lean 4.35.0's `module` system (`public import`, `@[expose] public section`) and expand from `72` to **`92` audited theorems** (adding `NonVacuity.lean`, `Challenge.lean`, `Solution.lean`, `PalomarSolution.lean`, and `palomar/PalomarChallenge.lean`).
- Run `cd lean && lake clean && lake build` after pulling `v2.4.0` to rebuild `.lake` artifacts cleanly.

### 4. MCP Server Tooling (`9` → `10` Tools)
- Added 10th tool `list_author_frontier_contributions` exposing the 7 companion author preprints with explicit COI and parent-still-OPEN flags. All existing 9 tool signatures remain 100% backwards-compatible.

### 5. Author Affiliation Correction
- Replaced legacy placeholder `"0thernes LLC"` with the accurate legal status `"Independent Researcher, Spokane, WA, USA"` matching ORCID `0009-0006-8168-9648`.

## Upgrading from `v2.2.0` to `v2.3.0`
- Dataset grew from `1,855` to `1,900` records and from `40` to `48` columns (adding `substrate_class`, `abstraction_layer`, `epistemic_spectrum_score`, `hardness_tractability_gradient`, `css_titan_margin`, `bridge_margin_ratio`, `adjacent_pillars_count`, and `margin_role`). Re-validate any downstream consumers against `schema/problem.schema.json`.
