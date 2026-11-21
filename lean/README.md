# Pure Lean 4.35.0 Formal Invariant Suite (`lean/`)

**Author:** Alexander Stephen Donahue (`0thernes LLC`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))  
**Toolchain:** `leanprover/lean4:v4.35.0` · **External Dependencies:** None (zero Mathlib)

## Scope & Honest Boundary

This proof library formally certifies **72 exact discrete mathematical invariants** (8 files, 1,008 lines) of the Unsolved Problems Mega-Atlas's scoring formulas (`CSS`, antiquity 300-year saturation, `Titan Index`, `Near-Term Leverage`), 4-Quadrant and 6-Era classifiers, 8×28 hierarchical taxonomy surjection, finite undirected graph Handshaking Lemma (`∑ deg = 2|E|`), cross-partition edge hierarchy (`cross_pillar ≤ cross_superdomain ≤ |E|`), deduplication cardinality bound, **Karpathy-style AutoResearch AQS bounds & anti-gaming keep/discard ratchet**, pairwise comparison delta antisymmetry, and **V2.3.0 multi-layer Substrate/Layer/Gradient/Margin/Bridge/Apex-Keystone invariants** (`LayerGradients.lean`).

> **Honest Boundary:** These theorems verify mathematical properties of the *atlas's quantitative and verification framework* only. They do **not** claim to prove any of the 1,900 open problems cataloged in the dataset.

## Build & Axiom Audit

```bash
cd lean
lake build
```

All 72 theorems compile (`10 jobs`) with **zero warnings**, **zero `sorry`**, **zero `admit`**, **zero `native_decide`**, **zero `Classical.choice`**, and **`#print axioms` strictly within `[propext, Quot.sound]` or empty** (audited in `MegaAtlasProofs/VerifyAxioms.lean`).
