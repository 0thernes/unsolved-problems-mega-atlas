# Pure Lean 4.35.0 Formal Invariant Suite (`lean/`)

**Author:** Alexander Stephen Donahue (`0thernes LLC`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))  
**Toolchain:** `leanprover/lean4:v4.35.0` · **External Dependencies:** None (zero Mathlib)

## Scope & Honest Boundary

This proof library formally certifies **46 exact discrete mathematical invariants** of the Unsolved Problems Mega-Atlas's scoring formulas (`CSS`, antiquity 300-year saturation, `Titan Index`, `Near-Term Leverage`), 4-Quadrant and 6-Era classifiers, 8×28 hierarchical taxonomy surjection, finite undirected graph Handshaking Lemma (`∑ deg = 2|E|`), cross-partition edge hierarchy (`cross_pillar ≤ cross_superdomain ≤ |E|`), and deduplication cardinality bound.

> **Honest Boundary:** These theorems verify mathematical properties of the *atlas's quantitative framework* only. They do **not** claim to prove any of the 1,855 open problems cataloged in the dataset.

## Build & Axiom Audit

```bash
cd lean
lake build
```

All 46 theorems compile with **zero warnings**, **zero `sorry`**, **zero `admit`**, **zero `native_decide`**, and **`#print axioms` strictly within `[propext, Quot.sound]` or empty** (audited in `MegaAtlasProofs/VerifyAxioms.lean`).
