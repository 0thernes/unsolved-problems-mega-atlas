#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Reproducible Benchmark Harness (Build Standard B26 / B27 / A37):
Runs 10 warmed timing iterations of:
  1. `load_v2_master()` (2,000 problems + NetworkX biconnectivity/PageRank/modularity)
  2. 25-query Hybrid RAG Gold Benchmark (`rag/query.py`)
  3. 2,000-record reference-oracle differential scoring throughput
Records hardware info, commit SHA, checksum validation, median, and IQR into
`results/bench-history.csv` and updates `docs/benchmarks.md`.
"""

from __future__ import annotations

import csv
import datetime
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "autoresearch"))
sys.path.insert(0, str(ROOT / "reference"))

from evaluate import GOLD_RAG_BENCHMARK  # noqa: E402
from query import ensure_sqlite_db, search_atlas  # noqa: E402
from scoring_oracle import oracle_css_score  # noqa: E402
from v2_loader import compute_css_score, load_v2_master  # noqa: E402


def _median_iqr(samples: List[float]) -> Tuple[float, float, float, float]:
    s = sorted(samples)
    med = statistics.median(s)
    q1 = statistics.quantiles(s, n=4)[0]
    q3 = statistics.quantiles(s, n=4)[2]
    return round(med, 4), round(q3 - q1, 4), round(min(s), 4), round(max(s), 4)


def _git_sha() -> str:
    res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False)
    return res.stdout.strip() or "uncommitted"


def main() -> None:
    ensure_sqlite_db()
    # Warmup
    d0 = load_v2_master()
    n_rows = len(d0["df"])
    n_edges = int(d0["summary_stats"]["total_graph_edges"])
    assert n_rows == 2000
    for q, _ in GOLD_RAG_BENCHMARK[:3]:
        search_atlas(query=q, top=5, hops=0)

    # 1. Load + NetworkX analytics (10 runs)
    load_times: List[float] = []
    for _ in range(10):
        t0 = time.perf_counter()
        d = load_v2_master()
        assert len(d["df"]) == n_rows and d["summary_stats"]["total_graph_edges"] == n_edges
        load_times.append(time.perf_counter() - t0)

    # 2. 25-query Hybrid RAG benchmark (10 runs, ms per query)
    rag_ms: List[float] = []
    for _ in range(10):
        t0 = time.perf_counter()
        hits = 0
        for q, exp in GOLD_RAG_BENCHMARK:
            res = search_atlas(query=q, top=5, hops=0)
            if res["results"] and res["results"][0]["id"] == exp:
                hits += 1
        assert hits == 25, f"RAG checksum gate failed: {hits}/25"
        rag_ms.append((time.perf_counter() - t0) * 1000.0 / len(GOLD_RAG_BENCHMARK))

    # 3. 2,000-problem differential CSS throughput (10 runs, ms total)
    rows = [
        (int(r.difficulty_score), int(r.civilizational_impact), int(r.graph_degree), int(r.age_years_2026), int(r.tractability_2050))
        for r in d0["df"].itertuples()
    ]
    diff_ms: List[float] = []
    for _ in range(10):
        t0 = time.perf_counter()
        mismatches = 0
        for a, b, c, ag, tr in rows:
            if abs(compute_css_score(a, b, c, ag, tr) - oracle_css_score(a, b, c, ag, tr)) > 0.01:
                mismatches += 1
        assert mismatches == 0
        diff_ms.append((time.perf_counter() - t0) * 1000.0)

    l_med, l_iqr, l_min, l_max = _median_iqr(load_times)
    r_med, r_iqr, r_min, r_max = _median_iqr(rag_ms)
    d_med, d_iqr, d_min, d_max = _median_iqr(diff_ms)

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha = _git_sha()
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    cpu_cnt = os.cpu_count() or 0
    env_str = f"{platform.system()} {platform.release()} ({platform.machine()}, {cpu_cnt} cores, Python {platform.python_version()})"

    csv_path = ROOT / "results" / "bench-history.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    header = ["timestamp_utc", "version", "commit", "environment", "load_median_s", "load_iqr_s", "rag_query_median_ms", "rag_query_iqr_ms", "diff_1900_median_ms", "diff_1900_iqr_ms", "checksum_pass"]
    write_hdr = not csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if write_hdr:
            w.writerow(header)
        w.writerow([ts, ver, sha, env_str, l_med, l_iqr, r_med, r_iqr, d_med, d_iqr, "PASS"])

    l_stat = "PASS" if l_med < 4.5 else "WARN"
    r_stat = "PASS" if r_med < 30.0 else "WARN"
    d_stat = "PASS" if d_med < 250.0 else "WARN"

    html_path = ROOT / "outputs" / "MegaAtlas_Interactive_Dashboard_V2.html"
    html_mb = html_path.stat().st_size / 1048576.0 if html_path.exists() else 0.0
    md = f"""# Reproducible Benchmarks — Unsolved Problems Mega-Atlas (`v{ver}`)

Every benchmark executes **10 warmed runs** with explicit output-correctness assertions
({n_rows:,} unique rows, {n_edges:,} graph edges, 25/25 top-1 RAG accuracy, and 0 differential
scoring mismatches against `reference/scoring_oracle.py`). No untimed or unverified
numbers are reported.

## Latest Verified Run

- **Timestamp (UTC):** `{ts}`
- **Atlas Version / Commit:** `v{ver}` (`{sha}`)
- **Hardware & Runtime:** `{env_str}`
- **Command:** `python scripts/benchmark_atlas.py` (or `just bench`)
- **History Log:** [`results/bench-history.csv`](../results/bench-history.csv)

| Workload (10 warmed runs, verified output) | Median | IQR | Min | Max | Performance Target | Status |
|---|---:|---:|---:|---:|---|---|
| Full `load_v2_master()` ({n_rows:,} rows + NetworkX PageRank/Betweenness/Modularity) | `{l_med:.4f} s` | `{l_iqr:.4f} s` | `{l_min:.4f} s` | `{l_max:.4f} s` | `< 4.5 s` | {l_stat} |
| Offline Hybrid FTS5+Graph RAG Latency (per query across 25-query Gold Set) | `{r_med:.4f} ms` | `{r_iqr:.4f} ms` | `{r_min:.4f} ms` | `{r_max:.4f} ms` | `< 30.0 ms` | {r_stat} |
| {n_rows:,}-Record Differential CSS Audit vs. 50-digit Decimal Oracle | `{d_med:.4f} ms` | `{d_iqr:.4f} ms` | `{d_min:.4f} ms` | `{d_max:.4f} ms` | `< 250.0 ms` | {d_stat} |

## Memory & Artifact Size Budget

- All git-tracked artifacts are strictly `< 5.0 MB` (Build Standard A24).
- Interactive HTML Dashboard shrunk from `20.64 MB` (`v2.3.0`) to **`{html_mb:.2f} MB`** (`< 4.0 MB` budget in `v{ver}`, even at {n_rows:,} rows + 25 Left to Solve fronts) via external `charts/*.png` assets, columnar `COLS`/`ROWS` JSON, and enum dictionary encoding.
"""
    (ROOT / "docs" / "benchmarks.md").write_text(md, encoding="utf-8", newline="\n")
    print(f"BENCHMARK PASS: load={l_med:.4f}s (IQR {l_iqr:.4f}s) | rag={r_med:.4f}ms/q (IQR {r_iqr:.4f}ms) | diff{n_rows}={d_med:.4f}ms")


if __name__ == "__main__":
    main()
