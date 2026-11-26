# Upgrading Guide

This document describes breaking and non-breaking changes when upgrading between major and minor releases of the **Unsolved Problems Mega-Atlas**.

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
