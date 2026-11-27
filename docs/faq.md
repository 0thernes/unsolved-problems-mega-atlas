# Frequently Asked Questions (FAQ)

### 1. Did you solve any of the 2,000 open problems in this atlas?
**No (`0 / 2,000` Atlas problems solved).** The `103` audited Lean 4.35.0 declarations (of `117` in `lean/`) concern the atlas *software model*: scoring bounds, taxonomy list sizes, a generic list-multigraph handshaking lemma, a dedup bound, the AutoResearch keep/discard rule, margin bounds, non-vacuity witnesses and refutations of weakened variants. No Lean statement refers to the 2,000-row data or its graph, and none addresses an open problem. The author's results in other repositories are listed in the archive Cycle-3 ledger [`RESULTS.md`](https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md) (`94` results across `28` entries); its Section A records three answers to open questions stated by other authors (`R1`, `R44`, `R45`), and every Mega-Atlas parent problem stays **OPEN**.

### 2. Why are the Fall/November 2026 AI proof claims (Riemann Hypothesis, Navier–Stokes, etc.) still marked OPEN?
Because formal kernel compilation or a preprint announcement is not the same thing as community retirement of a conjecture. For `NT-001` (RH) and `NT-002` (GRH), primary verification sources confirm the Nov 21, 2026 multi-kernel Lean certification of the `175,187`-file (`~17M`-line) Alpöge/Claude archive ([Lean FRO & Mathlib Initiative joint statement](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) and [M. Rubinstein's independent verification notes](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/), followed by a Nov 22 working draft and Nov 25 `lsernau/grh-lean` compact rewrite). However, full peer-reviewed mathematical exposition and Clay Mathematics Institute prize retirement remain pending. All 12 Fall/Nov 2026 AI proof-claim targets remain explicitly flagged `ai-claim-under-audit-nov2026` until official community consensus retires them.

### 3. Are the `difficulty_score`, `tractability_2050`, and `civilizational_impact` scores peer-reviewed?
**No.** They are explicitly disclosed AI-assisted editorial estimates created by solo independent researcher Alexander Stephen Donahue. Treat them as a transparent, editable, falsifiable argument: test custom weights or overrides in one command via `just rubric-diff` (`scripts/rubric_override_diff.py`) or MCP tool `simulate_rubric_override`, or edit any entry in `src/v2_data/`, run `just build`, and inspect the exact diff in `RANKING.md`.

### 4. Why aren't the `.sqlite`, `.json`, `.jsonl`, Legacy `.xls`, or 170+ page Directory PDF files committed directly in git?
Build Standard v1.2.0 (**A24**) keeps every git-tracked file strictly `< 5 MB` so clones stay fast and clean. Deterministic `.json.gz` (`1.33 MB`), `.jsonl.gz` (`1.25 MB`), `.csv`, `.tsv`, 16-sheet `.xlsx` (`2.00 MB`), `~3.1 MB` Interactive HTML, all 30 charts, and the 11-page AMS-LaTeX white paper PDF (`< 1 MB`) ARE committed directly. Running `rag/query.py` or `mcp_server/server.py` auto-builds the SQLite FTS5 index locally in `< 1 s` (and auto-rebuilds on version upgrades), and all full uncompressed release artifacts (including `build/MegaAtlas_Unsolved_Problems_V2_Legacy.xls`) are attached to **GitHub Release `v2.11.0`**.

### 5. How can I verify the Lean 4.35.0 proofs myself in under 30 seconds?
```bash
cd lean
lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
```
Each of the 103 audited theorems reports axioms within `[propext, Quot.sound]` (no `sorryAx`, `Classical.choice` or `Lean.ofReduceBool` in the per-theorem `#print axioms` output). On Linux with `bubblewrap`, run `bash scripts/verify_lean_six_kernels.sh` (`just lean-kernels`) for `leanchecker --fresh`, the live negative kernel rejection test, and the six kernel checks (five distinct implementations) that CI applies to the 9 Palomar comparator targets.
