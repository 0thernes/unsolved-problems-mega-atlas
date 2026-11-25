# Frequently Asked Questions (`docs/faq.md`)

### 1. Did any of Alexander Donahue's / 0thernes's papers solve one of the 1,900 Mega-Atlas problems?
**No (`0 / 1,900` retired).** A full 1,900-problem cross-reference completed on 2026-11-25 confirmed that zero grand Mega-Atlas problems are retired, and `multinomial-tv-conjecture` (`0TH-2026-006`) is a specialized 2026 preprint conjecture not cataloged in the 61 macro `STAT-*` problems. Seven macro nodes (`QM-011`, `QC-037`, `CS-053`, `CS-026`, `QC-042`, `CS-005`, `NEURO-001`) have explicit partial/special-case methodological overlaps; see [`docs/0THERNES_SOLVED_AUDIT_2026-11-25.md`](0THERNES_SOLVED_AUDIT_2026-11-25.md).

### 2. Why are the 12 Fall/Nov 2026 AI proof claims still listed as OPEN?
Lean compilation verifies logical deduction from formalized statements, NOT whether those formalized statements match the historical open problem without subtle drift or community peer consensus. Every AI claim stays unretired under `verification_flag = "ai-claim-under-audit-nov2026"`.

### 3. Why do the 72 Lean 4 proofs not use Mathlib?
Keeping `lean/MegaAtlasProofs/` 100% Pure Lean 4.35.0 (zero Mathlib, zero `Classical.choice`, strictly `[propext, Quot.sound]` or empty) lets anyone compile and audit all 72 theorems in ~15 seconds from a clean clone without downloading multi-gigabyte caches.

### 4. Why are large files (`outputs/*.pdf`, `*.html`, `*.sqlite`) committed to Git?
So GitHub Pages, the offline RAG CLI (`rag/query.py`), the 9-tool MCP server (`mcp_server/server.py`), and `pytest` work immediately after `git clone` with zero cloud or LFS dependencies (see [ADR 0002](adr/0002-dual-license-and-committed-atlas-artifacts.md)).
