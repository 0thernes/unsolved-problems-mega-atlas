# ADR 0002: Dual Licensing and Committed Offline Output Artifacts (A24 Trade-Off)

- **Status:** Accepted
- **Date:** 2026-11-25

## Context
Build Standard v1.2.0 item `A24` flags tracked files larger than 5 MB. However, `unsolved-problems-mega-atlas` serves a standalone 1,900-problem interactive HTML dashboard on GitHub Pages, an offline SQLite+FTS5 database powering `rag/query.py` and `mcp_server/server.py`, and a publication vector PDF monograph—six files in `outputs/` range from 5.6 MB to 21.6 MB.

## Decision
1. Retain the committed `outputs/` snapshot so GitHub Pages, offline RAG, the 9-tool MCP server, and `pytest` operate from a clean clone without Git LFS or external cloud hosting, while keeping **zero secrets, zero `.env` files, and zero build/Python caches** tracked.
2. Document this deliberate `dilemma` honestly in `LIMITATIONS.md` and `repo.yaml` (`A24: partial`) rather than gaming `Audit-Repo.ps1`.
3. Maintain dual licensing: `CC-BY-4.0` (`LICENSE`) for dataset/charts/monograph/docs and `MIT` (`LICENSE-CODE`) for code/schemas/Lean/RAG/MCP.

## Consequences
- Every downstream user and CI runner can verify 54+ SHA-256 checksums and launch the offline RAG/MCP server immediately upon `git clone`.
- `Audit-Repo.ps1` transparently flags the intentional >5 MB dataset files in `outputs/` as the sole documented exception.
