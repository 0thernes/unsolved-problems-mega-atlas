# Configuration Reference

The **Unsolved Problems Mega-Atlas (`v2.5.0`)** is designed to run **100% offline with zero configuration** for all core workflows (data loading, exporting, RAG search, MCP stdio server, Lean 4.35.0 verification, pytest, mutation testing, and benchmarking).

## Environment Variables (All Optional)

See [`.env.example`](../.env.example). Never commit `.env` or real tokens to git.

| Variable | Required? | Default | Purpose |
|---|---|---|---|
| `ZENODO_TOKEN` | No | *(unset)* | Only required if you explicitly run `python scripts/publish_zenodo.py --publish` to create a draft Zenodo deposit via REST API. |
| `ZENODO_SANDBOX_TOKEN` | No | *(unset)* | Only required if you run `python scripts/publish_zenodo.py --sandbox`. |
| `TECTONIC_BIN` | No | `tectonic` on `PATH` or `~/.local/bin/tectonic` | Optional explicit path override for `scripts/build_paper.py`. |

## CLI Flags

- `python src/v2_export_all.py [--skip-pdf]` — Exports CSV, TSV, JSON, `.json.gz`, JSONL, `.jsonl.gz`, SQLite+FTS5, 15-sheet XLSX, 8-sheet XLS, MD, TXT, `RANKING.md`, `<4 MB` Interactive HTML, and (unless `--skip-pdf`) the optional 168-page Chrome-headless directory PDF into `build/`.
- `python rag/query.py [query] [--problem ID] [--compare ID_A ID_B] [--pillar P] [--superdomain S] [--flag F] [--top N] [--hops 0|1] [--json]` — Offline Hybrid RAG CLI (auto-builds SQLite FTS5 DB if missing).
- `python scripts/audit_atlas.py [--sync-checksums] [--check-lean]` — Structural, JSON Schema, cross-format, ORCID, SHA-256, and optional Lean 4.35.0 audit.
- `python scripts/check_citations.py [--offline]` — Verifies all BibTeX URLs & DOIs live via HTTP / DOI Handle API (`--offline` checks syntax only).
- `python autoresearch/evaluate.py [--verify-gates] [--json] [--log --status S --desc D]` — Immutable Karpathy-style AutoResearch evaluation harness.

## Supported Locale & Encoding

- **Supported locales:** English (`en-US`, UTF-8, LF line endings).
- **Frozen Reference Year:** `REFERENCE_YEAR = 2026` in `src/v2_loader.py` guarantees deterministic problem-age and CSS scores across calendar years.
