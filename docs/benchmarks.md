# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v2.5.0`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
(1,900 unique rows, 5,808 graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `2026-11-26T02:09:48Z`
- **Atlas Version / Commit:** `v2.5.0` (`f838db1`)
- **Hardware & Runtime:** `Windows 11 (AMD64, 24 cores, Python 3.12.10)`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` (1,900 rows + NetworkX PageRank/Betweenness/Modularity) | `2.7079 s` | `0.1161 s` | `2.4029 s` | `3.4773 s` | `< 3.0 s` | PASS |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `6.7164 ms` | `0.6216 ms` | `5.7962 ms` | `8.7501 ms` | `< 30.0 ms` | PASS |
| 1,900-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `61.7447 ms` | `3.1125 ms` | `56.4336 ms` | `70.8139 ms` | `< 250.0 ms` | PASS |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to **`3.80 MB`** (`< 4.0 MB` budget in `v2.5.0`) via external `charts/*.png` assets and columnar `COLS`/`ROWS` JSON encoding (~5.4× smaller first-paint payload on GitHub Pages).
