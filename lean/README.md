# Pure Lean 4.35.0 Formal Invariant Suite (`MegaAtlasProofs`, `v2.7.0`)

- **Toolchain:** `leanprover/lean4:v4.35.0` (zero Mathlib, zero external Lake dependencies)
- **Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`)
- **License:** `Apache-2.0` (`../LICENSE-CODE`)
- **Audited Theorems:** **103** (`0` `sorry` in `lean/`, `0` `native_decide`, `0` custom `axiom`, axioms strictly `⊆ [propext, Quot.sound]`, `14` files, `1,707` lines)
- **Interactive Proof Blueprint:** [`../blueprint/index.html`](../blueprint/index.html)

## Module Inventory

| File | Theorems | Scope |
|---|---:|---|
| `MegaAtlasProofs/Scoring.lean` | 22 | CSS, Titan, Leverage weights, bounds, monotonicity & 300-year antiquity cap |
| `MegaAtlasProofs/Quadrants.lean` | 11 | Strategic 4-quadrant exact iff, Q1 leverage floor ≥ 5.6, monotone 6-era classifier |
| `MegaAtlasProofs/Taxonomy.lean` | 8 | 8 Macro-Pillars × 28 Superdomains (`[5,3,3,3,3,4,4,3]`), surjectivity & separation |
| `MegaAtlasProofs/GraphInvariants.lean` | 5 | Finite undirected Handshaking Lemma (`∑ deg = 2|E|`), edge hierarchy, deduplication bound |
| `MegaAtlasProofs/AutoResearchInvariants.lean` | 12 | `aqsBps` bounds, anti-gaming keep/discard ratchet, pairwise delta antisymmetry |
| `MegaAtlasProofs/LayerGradients.lean` | 14 | 8 Substrates × 7 Layers (`L0..L6`), `D−T` gradient `[-9,+9]`, CSS−Titan margin, 4-class MarginRole |
| `MegaAtlasProofs/NonVacuity.lean` | 12 | Concrete inhabitants, exact `results.tsv` trace (`8026→8193→9559→9799`) & negative boundaries |
| `MegaAtlasProofs/AdversarialTests.lean` | 10 | Constructive kernel-checked refutations (`¬P`) of deliberately false / off-by-one variants (Playbook Item 12) |
| `Challenge.lean` / `Solution.lean` / `PalomarSolution.lean` | 9 | Clean Palomar specification (`M1`–`M8` + `prove_all_mega_atlas_invariants`) matched against `../palomar/PalomarChallenge.lean` |
| `MegaAtlasProofs/VerifyAxioms.lean` | — | Audits `#print axioms` across all **103** theorems → frozen in `../results/lean_axioms.txt` |

## Local & 6-Kernel Verification Commands

```bash
# Cross-platform local build & 103-theorem axiom audit:
lake clean && lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean
lake env leanchecker-paranoid PalomarSolution

# Linux with bubblewrap (single-source 6-kernel replay matching CI verbatim):
bash ../scripts/verify_lean_six_kernels.sh   # or: just lean-kernels
```

> **Scope Boundary:** These proofs verify internal atlas formulas, taxonomy, finite graph handshaking, deduplication, AutoResearch ratchet, margin invariants, non-vacuity, and false-variant refutations **ONLY**. They prove **0 / 1,900** of the cataloged open problems. See `../docs/statement-fidelity.md` and `formalization.yaml`.
