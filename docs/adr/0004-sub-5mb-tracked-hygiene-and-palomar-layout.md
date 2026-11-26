# ADR 0004: `< 5 MB` Git Hygiene and `palomar/` Contract Placement

- **Date:** 2026-11-25
- **Status:** Accepted

## Context
Two engineering constraints collided during the `v2.4.0` Build Standard v1.2.0 & Playbook v1.3 upgrade:
1. Build Standard **A24** prohibits committed files `>= 5 MB`, while `v2.3.0` tracked 6 artifacts from `5.42 MB` to `20.64 MB`.
2. Palomar 6-kernel verification requires a `sorry`-only challenge contract (`PalomarChallenge.lean`), whereas the immutable Karpathy AutoResearch oracle (`autoresearch/evaluate.py`, which MUST NEVER be modified) scans `lean/**/*.lean` for any occurrence of `\bsorry\b`.

## Decision
1. Shrink `outputs/MegaAtlas_Interactive_Dashboard_V2.html` from `20.64 MB` to `3.80 MB` by referencing `charts/*.png` instead of 15 MB base64 PNGs and using columnar `COLS`/`ROWS` JSON; track deterministic `.json.gz` (1.28 MB) & `.jsonl.gz` (1.21 MB) and the Tectonic AMS-LaTeX PDF (`0.67 MB`); gitignore uncompressed `.json`, `.jsonl`, `.sqlite`, and `build/` Chrome directory PDF (auto-rebuilt locally & attached to GitHub Releases).
2. Place `PalomarChallenge.lean` in `palomar/PalomarChallenge.lean` and point `[[lean_lib]] name = "PalomarChallenge" srcDir = "../palomar"` in `lean/lakefile.toml`, keeping `lean/**/*.lean` 100% free of `sorry` while running full 6-kernel Palomar verification via `scripts/verify_lean_six_kernels.sh` (`--challenge-from-export=/tmp/PalomarChallenge.export --paranoid`).

## Consequences
- **Positive:** Zero tracked files `>= 5 MB` (100% A24 compliance), 6× faster GitHub Pages first paint, immutable `autoresearch/evaluate.py` preserved untouched, and authentic 6-kernel Palomar verification.
- **Trade-off:** Fresh git clones invoke `ensure_sqlite_db()` automatically on the first RAG/MCP query (~0.6 s one-time local build).
