# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v2.9.0`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
(2,000 unique rows, 6,108 graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `2026-11-27T05:00:31Z`
- **Atlas Version / Commit:** `v2.9.0` (`ad3d5ed`)
- **Hardware & Runtime:** `Windows 11 (AMD64, 24 cores, Python 3.12.10)`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` (2,000 rows + NetworkX PageRank/Betweenness/Modularity) | `2.1249 s` | `0.1455 s` | `2.0041 s` | `2.8982 s` | `< 4.5 s` | PASS |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `5.6863 ms` | `1.6325 ms` | `4.8549 ms` | `7.3937 ms` | `< 30.0 ms` | PASS |
| 2,000-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `71.0162 ms` | `24.9382 ms` | `61.2565 ms` | `92.7761 ms` | `< 250.0 ms` | PASS |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to **`3.11 MB`** (`< 4.0 MB` budget in `v2.9.0`, even at 2,000 rows + 25 Left to Solve fronts) via external `charts/*.png` assets, columnar `COLS`/`ROWS` JSON, and enum dictionary encoding.
