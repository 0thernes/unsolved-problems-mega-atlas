# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v2.8.0`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
(1,900 unique rows, 5,808 graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `2026-11-26T13:37:44Z`
- **Atlas Version / Commit:** `v2.8.0` (`541f093`)
- **Hardware & Runtime:** `Windows 11 (AMD64, 24 cores, Python 3.12.10)`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` (1,900 rows + NetworkX PageRank/Betweenness/Modularity) | `3.6831 s` | `0.6044 s` | `3.2597 s` | `4.1080 s` | `< 4.5 s` | PASS |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `10.2804 ms` | `1.0523 ms` | `9.3531 ms` | `10.8753 ms` | `< 30.0 ms` | PASS |
| 1,900-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `79.9292 ms` | `8.2996 ms` | `73.8725 ms` | `86.6144 ms` | `< 250.0 ms` | PASS |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to **`3.81 MB`** (`< 4.0 MB` budget in `v2.8.0`) via external `charts/*.png` assets and columnar `COLS`/`ROWS` JSON encoding (~5.4× smaller first-paint payload on GitHub Pages).
