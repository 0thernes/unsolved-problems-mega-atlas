# AutoResearch Track B Pilot — `LOG-002` (Busy Beaver `BB(6)` / Antihydra Margin Probe)

**Author / Curator:** Alexander Stephen Donahue (`0thernes LLC`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))  
**Target Problem:** `LOG-002` — *Busy Beaver `BB(6)` & Small-Machine Cryptids* (Logic, Statistics & Computing)  
**Mode:** `autoresearch/program.md` Track B (Planner → Worker → Verifier)

> **HONEST VERIFICATION BOUNDARY:** This pilot is a **finite exact arbitrary-precision computational probe** of the Antihydra Collatz-like map `H(a, b)` governing `BB(6)`. It proves **zero** asymptotic halting or non-halting results. `LOG-002` remains **COMPLETELY OPEN**.

## 1. Planner Hypothesis
- **Recurrence:** Starting at `(a_0, b_0) = (8, 0)`, iterate `a` even → `(3a/2, b + 2)`; `a` odd → `((3a − 1)/2, b − 1)`; halt iff `b = −1`.
- **Falsifiable Check:** Under a uniform parity heuristic, `E[Δb] = +0.5/step` and `E[Δ log₂ a] = log₂(3/2) ≈ 0.584963/step`. Does the canonical `a_0 = 8` orbit ever dip close to the `b = -1` halting boundary in the first 5,000 exact steps, and what fraction of perturbed starting seeds `a_0 ∈ [2, 100]` halt vs. escape?

## 2. Worker Execution & Reproduction
```bash
python research/runs/LOG-002_antihydra_pilot/antihydra_probe.py
```
Exact machine-readable outputs are persisted in [`RESULTS.json`](RESULTS.json).

## 3. Verifier Critique (Adversarial Check)
- Finite 5,000-step drift agreement with `+0.5/step` is purely **heuristic empirical evidence**, NOT a proof: Collatz-like maps can harbor arbitrarily late deterministic parity conspiracies (the core barrier tying `BB(6)` to `NT-005`).
- Therefore, **status of `LOG-002` is NOT changed**, and this pilot serves strictly as a reproducible Track B template demonstrating honest negative/finite-boundary discipline.
