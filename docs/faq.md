# Frequently Asked Questions (FAQ)

### 1. Did you solve any of the 1,900 open problems in this atlas?
**No (`0 / 1,900` Atlas problems solved).** The `103` audited Lean 4.35.0 theorems in this repository concern the atlas *software model*: scoring bounds, taxonomy list sizes, a generic handshaking lemma, a dedup bound, the AutoResearch keep/discard rule, margin bounds, non-vacuity witnesses and refutations of weakened variants. No Lean statement refers to the 1,900-row data or its graph, and none addresses an open problem. The author's results in other repositories are listed in the archive ledger [`RESULTS.md`](https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md); its section A records three answers to open questions stated by other authors (R1, R44, R45), and every Mega-Atlas parent problem stays **OPEN**.

### 2. Why are the Fall/November 2026 AI proof claims (Riemann Hypothesis, Navier–Stokes, etc.) still marked OPEN?
Because a reported proof is not a retired problem until it is checked and accepted by the community. Some files in this repository describe a Nov 21, 2026 multi-kernel Lean certification of an RH/GRH archive attributed to named people; no primary source for that report has been found, so it is treated as unverified (see [`ERRATA.md`](../ERRATA.md)). Even a confirmed kernel check would certify a formal statement, not the human-readable exposition or the community review that retirement requires. All 12 Fall/Nov 2026 AI proof-claim targets remain explicitly flagged `ai-claim-under-audit-nov2026` until official community consensus retires them.

### 3. Are the `difficulty_score`, `tractability_2050`, and `civilizational_impact` scores peer-reviewed?
**No.** They are explicitly disclosed AI-assisted editorial estimates created by solo independent researcher Alexander Stephen Donahue. Treat them as a transparent, editable, falsifiable argument: edit any entry in `src/v2_data/`, run `just build`, and inspect the exact diff in `RANKING.md`.

### 4. Why aren't the `.sqlite`, `.json`, `.jsonl`, or 168-page Directory PDF files committed directly in git?
Build Standard v1.2.0 (**A24**) keeps every git-tracked file strictly `< 5 MB` so clones stay fast and clean. Deterministic `.json.gz` (`1.28 MB`), `.jsonl.gz` (`1.21 MB`), `.csv`, `.tsv`, 15-sheet `.xlsx`, `<4 MB` Interactive HTML, all 30 charts, and the 10-page AMS-LaTeX white paper PDF (`0.68 MB`) ARE committed directly. Running `rag/query.py` or `mcp_server/server.py` auto-builds the SQLite FTS5 index locally in `< 1 s` (and auto-rebuilds on version upgrades), and all full uncompressed release artifacts are attached to **GitHub Release `v2.8.0`**.

### 5. How can I verify the Lean 4.35.0 proofs myself in under 30 seconds?
```bash
cd lean
lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
```
Each of the 103 audited theorems reports axioms within `[propext, Quot.sound]` (no `sorryAx`, `Classical.choice` or `Lean.ofReduceBool` in the per-theorem `#print axioms` output). On Linux with `bubblewrap`, run `bash scripts/verify_lean_six_kernels.sh` (`just lean-kernels`) for `leanchecker --fresh`, the negative kernel test, and the six kernel checks (five distinct implementations) that CI applies to the 9 Palomar comparator targets.
