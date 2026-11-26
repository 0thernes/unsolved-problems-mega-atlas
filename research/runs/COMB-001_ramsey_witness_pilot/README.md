# Track B Pilot #3 — `COMB-001`: Constructive Ramsey Lower-Bound Witness Certification

- **Atlas Problem ID:** `COMB-001` (*Diagonal & Off-Diagonal Ramsey Numbers `R(k,k)`*)
- **Epistemic Status:** **OPEN** — Certifies exact finite lower-bound graph witnesses only; makes **zero** claim on `R(5,5) ∈ [43, 46]`, `R(6,6) ∈ [102, 160]`, or general `R(k,k)`.
- **Script:** [`ramsey_probe.py`](ramsey_probe.py) · **Deterministic Artifact:** [`RESULTS.json`](RESULTS.json)

## Certified Witnesses (Zero-Dependency Exact Bitmask Clique Search)

| Witness Graph | Lower Bound Proved | Exact `ω(G)` | Exact `α(G)` | Literature Context |
|---|---|---|---|---|
| Paley `P_5` | `R(3,3) > 5` | `2` | `2` | Tight (`R(3,3) = 6`) |
| Circulant `C_8({1,4})` | `R(3,4) > 8` | `2` | `3` | Tight (`R(3,4) = 9`) |
| Circulant `C_13({1,5})` | `R(3,5) > 13` | `2` | `4` | Tight (`R(3,5) = 14`) |
| Paley `P_17` | `R(4,4) > 17` | `3` | `3` | Tight (`R(4,4) = 18`) |
| Circulant `C_24({1,2,4,8,9})` | `R(4,5) > 24` | `3` | `4` | Tight (`R(4,5) = 25`, McKay–Radziszowski 1995) |
| Paley `P_37` | `R(5,5) > 37` | `4` | `4` | Classic Paley bound (`R(5,5) ∈ [43, 46]` OPEN) |
| Paley `P_101` | `R(6,6) > 101` | `5` | `5` | Classic Paley bound (`R(6,6) ∈ [102, 160]` OPEN) |

Every graph's symmetry and cyclic automorphism `i ↦ (i + 1) mod n` are explicitly verified on the full adjacency matrix, with full all-vertex clique search cross-checked on every witness with `n ≤ 37`.

## Reproduction

```bash
python research/runs/COMB-001_ramsey_witness_pilot/ramsey_probe.py
```
