# Track B Pilot #2 — `NT-005`: Collatz (`3n+1`) Parity Margins & Terras Bijection

- **Atlas Problem ID:** `NT-005` (*Collatz Conjecture / 3n + 1 Problem*)
- **Epistemic Status:** **OPEN** — Finite exact arbitrary-precision verification only; proves **zero** part of `NT-005`.
- **Script:** [`collatz_probe.py`](collatz_probe.py) · **Deterministic Artifact:** [`RESULTS.json`](RESULTS.json)

## Scope & Reproducible Checks

1. **Exact Sweep (`n ∈ [1, 100,000]`):** Verifies convergence to `1` for all `100,000` positive integers using exact arbitrary-precision Python `int` arithmetic, recording exact longest stopping time (`n = 77,031`, `350` steps), highest excursion peak (`n = 77,671`, peak `1,570,824,736`), highest excursion ratio `peak / n`, and highest odd-step parity density (`k_odd / steps` for `steps >= 50`).
2. **Canonical Benchmarks:** Exact trajectories for `n ∈ {27, 703, 9663, 77031, 837799}`.
3. **Terras (1976) Finite Bijection Audit (`k = 1..12`):** Exhaustively confirms that the compressed Collatz parity map `T(x) = x/2` (even) or `(3x+1)/2` (odd) induces an exact bijection between `Z / 2^k Z` and `{0,1}^k` for every `k = 1..12` (`2^12 = 4,096` classes).

## Reproduction

```bash
python research/runs/NT-005_collatz_parity_pilot/collatz_probe.py
```
