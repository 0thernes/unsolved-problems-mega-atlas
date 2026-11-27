# ADR 0001: Zero-Mathlib Lean 4.35.0 for Software-Model Formal Invariants

- **Date:** 2026-11-20 (updated 2026-11-26 for Lean 4.35.0 software-model scope clarity)
- **Status:** Accepted

## Context
We needed machine-checked guarantees for the atlas *software model*—scoring bounds, weight sums, quadrant/era classifiers, 8×28 taxonomy partitions, generic list-multigraph handshaking, deduplication bounds, AutoResearch anti-gaming ratchets, and gradient/margin geometry—without multi-gigabyte Mathlib cache downloads or slow CI builds.

## Decision
Implement all discrete software-model invariants in zero-Mathlib **Lean 4.35.0** (`lean/MegaAtlasProofs/*.lean`), with per-theorem `#print axioms` strictly within `[propext, Quot.sound]` across `103` audited declarations of `117` in `lean/` (zero `sorry`, zero `native_decide`, zero custom axioms).

## Consequences
- **Positive:** Clean cold build takes `< 10 s` on CPU; the `9` exported Palomar comparator targets pass `6` kernel checks across `5` distinct checker implementations (`lean` and `leanchecker --fresh`/`leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`, `con-ron`) plus a live negative kernel rejection test via `scripts/verify_lean_six_kernels.sh`.
- **Trade-off:** Transcendental `ln(1 + degree)` terms in CSS/Titan are abstracted as bounded inputs in Lean and differentially verified against our 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`), while the `2,000`-row dataset and `6,108`-edge biconnectivity are audited in Python (NetworkX), documented explicitly in `docs/statement-fidelity.md`.
