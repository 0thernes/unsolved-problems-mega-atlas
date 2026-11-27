# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v2.11.0`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
(2,000 unique rows, 6,108 graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `2026-11-27T19:08:03Z`
- **Atlas Version / Commit:** `v2.11.0` (`9c543fc`)
- **Hardware & Runtime:** `Windows 11 (AMD64, 24 cores, Python 3.12.10)`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` (2,000 rows + NetworkX PageRank/Betweenness/Modularity) | `4.1517 s` | `1.7194 s` | `2.6559 s` | `7.9517 s` | `< 4.5 s` | PASS |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `25.2189 ms` | `88.0253 ms` | `19.4128 ms` | `185.5026 ms` | `< 30.0 ms` | PASS |
| 2,000-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `109.8077 ms` | `16.4325 ms` | `89.5949 ms` | `135.2307 ms` | `< 250.0 ms` | PASS |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to **`3.11 MB`** (`< 4.0 MB` budget in `v2.11.0`, even at 2,000 rows + live Left to Solve fronts) via external `charts/*.png` assets, columnar `COLS`/`ROWS` JSON, and enum dictionary encoding.
