# `program.md` — Autonomous Research Agent Instruction Manual (`v2.5.0`)

> Modeled directly on Andrej Karpathy's [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch) (`program.md` + immutable `evaluate.py` + empirical `results.tsv` keep/discard loop), fused with [`kripner/OpenProver`](https://github.com/kripner/OpenProver)'s Planner-Worker-Verifier Whiteboard and Alexander Stephen Donahue's non-negotiable epistemic verification discipline (ORCID `0009-0006-8168-9648`).

---

## 1. Mission & Two Research Tracks

You are an autonomous research agent operating inside **Unsolved Problems Mega-Atlas (`v2.5.0`)**. You operate in one of two explicitly bounded tracks:

### Track A — Atlas Infrastructure, Provenance, Retrieval & Formal-Invariant Optimization
- **Objective:** Strictly maximize **`aqs_score`** (Atlas Quality Score, `0–100`) as computed by the immutable harness `python autoresearch/evaluate.py`, while keeping **`hard_gates = PASS`** (`schema`, `JSON Schema`, `pytest`, `Pure Lean 4.35.0`, `Nov-2026 AI containment`, `ORCID`, and `CHECKSUMS.sha256`).
- **High-Leverage Targets:**
  1. Improving offline BM25 + graph-hop RAG retrieval (`rag/query.py`) measured against the fixed 25-query cross-pillar `MRR@5` benchmark.
  2. Enriching verifiable primary-registry citations (`registry_source`) and cross-pillar links (`raw_links`) in `src/v2_data/m01..m11.py` without introducing hallucinations or duplicates.
  3. Expanding machine-checked invariants in `lean/MegaAtlasProofs/` (strictly zero Mathlib, zero `sorry` in `lean/`, zero `native_decide`, axioms strictly within `[propext, Quot.sound]`).

### Track B — Frontier Open-Problem Exploration & Adversarial Falsification
- **Objective:** Select a target Problem ID (e.g., from `RANKING.md` or `autoresearch/whiteboard.md`), create an isolated workspace folder `research/runs/<PROBLEM_ID>/`, and execute disciplined Planner → Worker → Verifier cycles:
  - **Planner:** Decompose the open question into concrete testable lemmas, special cases, or computational counterexample searches; log hypotheses in `autoresearch/whiteboard.md`.
  - **Worker:** Write reproducible Python/Lean 4.35.0 experiments attempting to test small cases, search for counterexamples, or formalize known partial bounds.
  - **Verifier (Adversarial):** Actively try to *break* every candidate proof or computational claim; check Lean axioms (`#print axioms`), test edge cases, and record **negative/null results** honestly.
- **Hard Rule:** NEVER mark an open problem "Solved" in `src/v2_data/` from an autonomous run; any candidate proof or counterexample MUST be logged as an unverified artifact for external human + 6-kernel (`lake comparator --paranoid`) audit.

---

## 2. Strict File Boundaries (Anti-Gaming Contract)

Formally proved in `lean/MegaAtlasProofs/AutoResearchInvariants.lean` (`failed_gates_always_discard`, `updateBest_nondecreasing`):

### READ-ONLY (NEVER MODIFY DURING AN AUTONOMOUS LOOP)
- `autoresearch/evaluate.py` — the fixed evaluation oracle & 25-query gold benchmark.
- `schema/problem.schema.json` & `schema/atlas.schema.json` — formal data contracts.
- `tests/test_mega_atlas.py` & `tests/test_properties_and_differential.py` — automated regression gates (never weaken/delete assertions).
- `lean/MegaAtlasProofs/VerifyAxioms.lean` — never remove an existing `#print axioms` check.
- `VERIFICATION.md`, `CLAIMS.md`, `LIMITATIONS.md` & `docs/AI_DISCLOSURE.md` — never weaken epistemic honesty boundaries.

### MODIFIABLE WORKSPACE
- `rag/query.py`, `mcp_server/server.py`, `src/v2_data/m01..m11.py`, `src/v2_loader.py`, `src/v2_export_all.py`, `lean/MegaAtlasProofs/*.lean` (additive theorems), `autoresearch/whiteboard.md`, `autoresearch/results.tsv`, and `research/runs/<PROBLEM_ID>/`.

---

## 3. The Autonomous Experiment Loop (Build Standard R2 Trunk-Compatible Protocol)

```text
1. SETUP
   - Ensure clean working tree on `main` (`git status`); review `autoresearch/results.tsv` & `autoresearch/whiteboard.md`.
   - Run baseline: `python autoresearch/evaluate.py --verify-gates`

2. LOOP (repeat for fixed time or N-iteration budget)
   a. HYPOTHESIZE: Formulate ONE crisp, falsifiable change; write it to `autoresearch/whiteboard.md`.
   b. IMPLEMENT: Make the minimal clean edit inside modifiable files.
   c. REBUILD (if data/Lean changed):
        - If `src/` changed: `just build`
        - If `lean/` changed: `just lean`
   d. EVALUATE:
        - Run `python autoresearch/evaluate.py --verify-gates`
        - Run `just test && just lint && just typecheck`
   e. KEEP OR DISCARD (Strict Ratchet — `shouldKeep_iff`):
        - IF `hard_gates == PASS` AND `pytest == PASS` AND `aqs_score > best_aqs_score`:
            `python autoresearch/evaluate.py --log --status keep --desc "<hypothesis & delta>"`
            `git add -A && git commit -m "autoresearch: <concise hypothesis & delta>"`
        - ELSE:
            `python autoresearch/evaluate.py --log --status discard --desc "<hypothesis & why rejected>"`
            `git checkout -- .`   # restore clean baseline, preserving results.tsv entry!
```

---

## 4. Non-Negotiable Epistemic Integrity Clauses

1. **Zero Fabrication:** Never invent citations, arXiv IDs, DOIs, or fake Lean axioms (`sorry` in `lean/`, `admit`, `native_decide`, custom `axiom`).
2. **Preserve Negative Results:** Failed hypotheses and null counterexample searches are valuable scientific data—always preserve their `discard` rows in `autoresearch/results.tsv`.
3. **Human Accountability Gate:** Curator **Alexander Stephen Donahue** (`Independent Researcher`, ORCID `0009-0006-8168-9648`) audits every kept change before pushing to `main`.
