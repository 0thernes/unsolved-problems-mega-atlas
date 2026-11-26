# ADR 0001: Zero-Mathlib Pure Lean 4.35.0 for Formal Invariants

- **Date:** 2026-11-20 (updated 2026-11-25 for Lean 4.35.0 6-kernel Palomar verification)
- **Status:** Accepted

## Context
We needed machine-checked guarantees for scoring bounds, weight sums, quadrant/era classifiers, 8×28 taxonomy partitions, finite graph handshaking, deduplication bounds, AutoResearch anti-gaming ratchets, and gradient/margin geometry — without multi-gigabyte Mathlib cache downloads or slow CI builds.

## Decision
Implement all formal invariants in pure zero-Mathlib **Lean 4.35.0** (`lean/MegaAtlasProofs/*.lean`), using constructive axioms strictly within `[propext, Quot.sound]` (zero `Classical.choice`, zero `sorry` in `lean/`, zero `native_decide`).

## Consequences
- **Positive:** Clean cold build takes `< 10 s` on CPU; all 1,769 exported declarations replay cleanly across all 6 independent Lean 4.35.0 proof kernels (`lean`, `leanchecker --fresh` / `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`, `con-ron`) via `scripts/verify_lean_six_kernels.sh`.
- **Trade-off:** Transcendental `ln(1 + degree)` terms in CSS/Titan are abstracted as bounded inputs in Lean and differentially verified against our 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`), documented explicitly in `docs/statement-fidelity.md`.
