# Configuration Reference

The **Unsolved Problems Mega-Atlas (`v2.11.0`)** is designed to run **100% offline with zero configuration** for all core workflows (data loading, exporting, RAG search, 13-tool MCP stdio server, Lean 4.35.0 verification, pytest, mutation testing, rubric sensitivity diffs, and benchmarking).

## Environment Variables (All Optional)

See [`.env.example`](../.env.example). Never commit `.env` or real tokens to git.

| Variable | Required? | Default | Purpose |
|---|---|---|---|
| `ZENODO_TOKEN` | No | *(unset)* | Only required if you explicitly run `python scripts/publish_zenodo.py --publish` to create a draft Zenodo deposit via REST API. |
| `ZENODO_SANDBOX_TOKEN` | No | *(unset)* | Only required if you run `python scripts/publish_zenodo.py --sandbox`. |
| `TECTONIC_BIN` | No | `tectonic` on `PATH` or `~/.local/bin/tectonic` | Optional explicit path override for `scripts/build_paper.py`. |

## CLI Flags

- `python src/v2_export_all.py [--skip-pdf]` — Exports CSV, TSV, JSON, `.json.gz`, JSONL, `.jsonl.gz`, SQLite+FTS5 (incl. `lefttosolve_programs`), 16-sheet XLSX, 9-sheet Legacy BIFF8 XLS (into `build/`), MD, TXT, `RANKING.md`, `<4 MB` Interactive HTML (enum-dictionary compressed with live `./daily_registries.json` hydration), and (unless `--skip-pdf`) the optional Chrome-headless directory PDF into `build/`.
- `python rag/query.py [query] [--problem ID] [--compare ID_A ID_B] [--pillar P] [--superdomain S] [--flag F] [--top N] [--hops 0|1] [--json]` — Offline Hybrid RAG CLI (auto-builds SQLite FTS5 DB if missing or stale).
- `python scripts/sync_external_registries.py [--live|--offline] [--write-daily] [--write-report]` — Polls all 16 live external open-problem trackers + all 26 live Left to Solve fronts (`lefttosolve.com/programs`) in parallel (respecting anti-bot gates with zero silent retirement).
- `python scripts/rubric_override_diff.py [--override FILE]` — Re-scores all 2,000 problems under researcher-supplied CSS weights / score overrides and reports Spearman `rho`, Kendall `tau`, Top-25 Jaccard, and quadrant migrations.
- `python scripts/stamp_timestamps.py [--mint|--verify]` — Mints and structurally verifies dual DigiCert RFC 3161 (`.tsr`) and 3-calendar Bitcoin OpenTimestamps (`.ots`) proofs binding `CHECKSUMS.sha256`.
- `python scripts/audit_atlas.py [--sync-checksums] [--check-lean]` — Structural, JSON Schema, cross-format, ORCID, SHA-256, dual-timestamp, and optional Lean 4.35.0 audit.
- `python scripts/check_citations.py [--offline]` — Verifies all 15 BibTeX URLs & DOIs live via HTTP / DOI Handle API + Crossref/Zenodo title-token parity & retraction checks (`--offline` checks syntax only).
- `python autoresearch/evaluate.py [--verify-gates] [--json] [--log --status S --desc D]` — Immutable Karpathy-style AutoResearch evaluation harness.

## Supported Locale & Encoding

- **Supported locales:** English (`en-US`, UTF-8, LF line endings).
- **Frozen Reference Year:** `REFERENCE_YEAR = 2026` in `src/v2_loader.py` guarantees deterministic problem-age and CSS scores across calendar years.
