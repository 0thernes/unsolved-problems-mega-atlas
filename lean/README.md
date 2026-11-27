# Lean 4.35.0 Software-Model Formal Invariant Suite (`MegaAtlasProofs`, `v2.11.0`)

- **Toolchain:** `leanprover/lean4:v4.35.0` (zero Mathlib, zero external Lake dependencies)
- **Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`)
- **License:** `Apache-2.0` (`../LICENSE-CODE`)
- **Audited Theorems:** **103** audited declarations (of `117` theorem/lemma declarations in `lean/`; `5` private `sumNat_*` helpers in `GraphInvariants` and `9` intermediate `Solution` wrappers are omitted from `#print axioms`; `0` `sorry`, `0` `native_decide`, `0` custom `axiom`, `0` `unsafe`/`implemented_by`/`@[extern`/`opaque`, per-theorem `#print axioms ⊆ [propext, Quot.sound]`)
- **Interactive Proof Blueprint:** [`../blueprint/index.html`](../blueprint/index.html)

## Module Inventory

| File | Audited Thms | Scope |
|---|---:|---|
| `MegaAtlasProofs/Scoring.lean` | 22 | CSS, Titan, Leverage weights, bounds, monotonicity & 300-year antiquity cap |
| `MegaAtlasProofs/Quadrants.lean` | 11 | Strategic 4-quadrant exact iff, Q1 leverage floor ≥ 5.6, monotone 6-era classifier |
| `MegaAtlasProofs/Taxonomy.lean` | 8 | 8 Macro-Pillars × 28 Superdomains (`[5,3,3,3,3,4,4,3]`), surjectivity & separation |
| `MegaAtlasProofs/GraphInvariants.lean` | 5 | Generic list-multigraph Handshaking Lemma (`∑ deg = 2|E|`), edge hierarchy, deduplication bound (`5` private helpers unaudited) |
| `MegaAtlasProofs/AutoResearchInvariants.lean` | 12 | `aqsBps` bounds, anti-gaming keep/discard ratchet, pairwise delta antisymmetry |
| `MegaAtlasProofs/LayerGradients.lean` | 14 | 8 Substrates × 7 Layers (`L0..L6`), `D−T` gradient `[-9,+9]`, CSS−Titan margin, 4-class MarginRole |
| `MegaAtlasProofs/NonVacuity.lean` | 12 | Concrete inhabitants, exact `results.tsv` trace (`8026→8193→9559→9799`) & negative boundaries |
| `MegaAtlasProofs/AdversarialTests.lean` | 10 | Constructive kernel-checked refutations (`¬P`) of deliberately false / off-by-one variants (Playbook Item 12) |
| `Challenge.lean` / `Solution.lean` / `PalomarSolution.lean` | 9 | Clean Palomar specification (`M1`–`M8` + `prove_all_mega_atlas_invariants`) matched against `../palomar/PalomarChallenge.lean` |
| `MegaAtlasProofs/VerifyAxioms.lean` | — | Audits `#print axioms` across all **103** declarations → frozen in `../results/lean_axioms.txt` |

## Local & Multi-Kernel Verification Commands

```bash
# Cross-platform local build & 103-theorem per-theorem axiom audit:
lake clean && lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
lake env leanchecker-paranoid PalomarSolution

# Linux with bubblewrap (6 kernel checks across 5 distinct implementations on 9 Palomar targets + live negative rejection):
bash ../scripts/verify_lean_six_kernels.sh   # or: just lean-kernels
```

> **Scope Boundary:** These proofs verify discrete properties of the atlas *software model* **ONLY** (integer formulas, taxonomy sizes, generic list-multigraph handshaking, deduplication, AutoResearch ratchet, margin invariants, non-vacuity, and false-variant refutations; several counted theorems are literal arithmetic identities or hypothesis restatements). No Lean declaration references the `2,000`-row dataset, its `6,108`-edge graph, biconnectivity, or IEEE-754 floats (checked in Python), and **0 / 2,000** cataloged open problems are solved. Whole-environment `lake check --paranoid` also lists `Classical.choice` from Lean core, though none of the 103 audited theorems depends on it. See `../docs/statement-fidelity.md` and `formalization.yaml`.
