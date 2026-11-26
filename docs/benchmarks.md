# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v2.4.0`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
(1,900 unique rows, 5,808 graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `2026-11-25T23:47:51Z`
- **Atlas Version / Commit:** `v2.4.0` (`c735b9f`)
- **Hardware & Runtime:** `Windows 11 (AMD64, 24 cores, Python 3.12.10)`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` (1,900 rows + NetworkX PageRank/Betweenness/Modularity) | `1.8140 s` | `0.0683 s` | `1.7829 s` | `1.8680 s` | `< 3.0 s` | PASS |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `4.4980 ms` | `0.4570 ms` | `4.2672 ms` | `7.3976 ms` | `< 30.0 ms` | PASS |
| 1,900-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `55.5851 ms` | `1.7892 ms` | `54.9905 ms` | `58.6798 ms` | `< 250.0 ms` | PASS |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to `< 3.5 MB` (`v2.4.0`) via external `charts/*.png` assets and columnar `COLS`/`ROWS` JSON encoding (~6× faster first paint on GitHub Pages).
