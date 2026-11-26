# Frequently Asked Questions (FAQ)

### 1. Did you solve any of the 1,900 open problems in this atlas?
**No (`0 / 1,900` overarching Atlas problems retired).** The Lean 4.35.0 proofs in this repository (`103` theorems across 6 kernels + live negative kernel rejection) certify the atlas's *internal* scoring, taxonomy, graph handshaking, deduplication, AutoResearch ratchet, margin invariants, non-vacuity, and adversarial refutations — NOT the 1,900 open problems themselves. Twelve companion independent preprints and formal builds in `0thernes-research-archive` resolve narrowly scoped published sub-conjectures, formalize complexity barriers, or certify discrete model invariants (documented transparently in `paper/main.tex` Section 6 and MCP tool `list_author_frontier_contributions`), and every single one explicitly keeps its overarching Mega-Atlas parent problem **OPEN**.

### 2. Why are the Fall/November 2026 AI proof claims (Riemann Hypothesis, Navier–Stokes, etc.) still marked OPEN?
Because compiling a multi-million-line Lean proof archive (such as the Nov 21, 2026 Lean FRO / Mathlib Initiative multi-kernel certification of the Alpöge/Claude RH/GRH archive) checks deductive soundness, NOT human-readable exposition or Clay Mathematics Institute community retirement. All 12 Fall/Nov 2026 AI proof-claim targets remain explicitly flagged `ai-claim-under-audit-nov2026` until official community consensus retires them.

### 3. Are the `difficulty_score`, `tractability_2050`, and `civilizational_impact` scores peer-reviewed?
**No.** They are explicitly disclosed AI-assisted editorial estimates created by solo independent researcher Alexander Stephen Donahue. Treat them as a transparent, editable, falsifiable argument: edit any entry in `src/v2_data/`, run `just build`, and inspect the exact diff in `RANKING.md`.

### 4. Why aren't the `.sqlite`, `.json`, `.jsonl`, or 168-page Directory PDF files committed directly in git?
Build Standard v1.2.0 (**A24**) keeps every git-tracked file strictly `< 5 MB` so clones stay fast and clean. Deterministic `.json.gz` (`1.28 MB`), `.jsonl.gz` (`1.21 MB`), `.csv`, `.tsv`, 15-sheet `.xlsx`, `<4 MB` Interactive HTML, all 30 charts, and the 10-page AMS-LaTeX white paper PDF (`0.68 MB`) ARE committed directly. Running `rag/query.py` or `mcp_server/server.py` auto-builds the SQLite FTS5 index locally in `< 1 s` (and auto-rebuilds on version upgrades), and all full uncompressed release artifacts are attached to **GitHub Release `v2.6.0`**.

### 5. How can I verify the Lean 4.35.0 proofs myself in under 30 seconds?
```bash
cd lean
lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
```
Every one of the 103 theorems reports axioms strictly within `[propext, Quot.sound]` (zero `sorryAx`, zero `Classical.choice`, zero `Lean.ofReduceBool`). On Linux with `bubblewrap`, run `bash scripts/verify_lean_six_kernels.sh` (`just lean-kernels`) to replay all 6 independent proof kernels plus `leanchecker --fresh` and the live negative kernel rejection test.
