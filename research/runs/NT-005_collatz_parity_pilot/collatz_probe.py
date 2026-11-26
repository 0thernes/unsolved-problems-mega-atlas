#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Track B Reproducible Frontier Probe #2 — NT-005 (Collatz 3n+1 Parity Margins).

Executes exact arbitrary-precision integer arithmetic (zero floats in core
recurrences) across:
  1. Exhaustive total stopping-time & peak-excursion sweep over n in [1, 100_000].
  2. Exact trajectory fingerprints for canonical high-excursion benchmarks
     (27, 703, 9663, 77031, 837799).
  3. Exhaustive finite verification of the Terras (1976) compressed Collatz
     parity-vector bijection on Z / 2^k Z for k = 1..12 (2^12 = 4,096 classes).

HONEST VERIFICATION BOUNDARY:
  Certifies finite exact computational statistics and known finite modular
  bijections ONLY. Explicitly makes ZERO claim to prove or retire NT-005
  (the Collatz Conjecture remains OPEN).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

RUN_DIR = Path(__file__).resolve().parent
RESULTS_PATH = RUN_DIR / "RESULTS.json"


def collatz_stats(n: int) -> dict[str, int]:
    """Compute exact standard Collatz (n/2, 3n+1) steps, odd steps, and peak value."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    cur = n
    steps = 0
    odd_steps = 0
    peak = n
    while cur != 1:
        if cur & 1:
            cur = 3 * cur + 1
            odd_steps += 1
            if cur > peak:
                peak = cur
        else:
            cur >>= 1
        steps += 1
    return {"n": n, "steps": steps, "odd_steps": odd_steps, "even_steps": steps - odd_steps, "peak": peak}


def compressed_parity_vector(n: int, k: int) -> int:
    """Return the k-bit compressed Collatz parity vector T(x) = x/2 or (3x+1)/2."""
    bits = 0
    cur = n
    for bit_idx in range(k):
        if cur & 1:
            bits |= 1 << bit_idx
            cur = (3 * cur + 1) >> 1
        else:
            cur >>= 1
    return bits


def verify_terras_bijection(max_k: int = 12) -> list[dict[str, Any]]:
    """Exhaustively check that n mod 2^k -> k-bit parity vector is a bijection for k=1..max_k."""
    out: list[dict[str, Any]] = []
    for k in range(1, max_k + 1):
        mod = 1 << k
        seen = {compressed_parity_vector(r, k) for r in range(mod)}
        is_bij = len(seen) == mod
        if not is_bij:
            raise AssertionError(f"Terras parity bijection failed at k={k}")
        out.append({"k": k, "modulus": mod, "unique_parity_vectors": len(seen), "is_bijection": is_bij})
    return out


def run_probe(sweep_limit: int = 100_000) -> dict[str, Any]:
    # Memoized exact stopping time & peak across [1, sweep_limit]
    steps_cache: dict[int, int] = {1: 0}
    odd_cache: dict[int, int] = {1: 0}
    peak_cache: dict[int, int] = {1: 1}

    max_steps_n, max_steps_val = 1, 0
    max_peak_n, max_peak_val = 1, 1
    max_ratio_n, max_ratio_num, max_ratio_den = 1, 1, 1
    max_odd_density_n, max_odd_num, max_odd_den = 1, 0, 1

    for start in range(2, sweep_limit + 1):
        path: list[int] = []
        cur = start
        while cur not in steps_cache:
            path.append(cur)
            cur = (3 * cur + 1) if (cur & 1) else (cur >> 1)
        st = steps_cache[cur]
        od = odd_cache[cur]
        pk = peak_cache[cur]
        for node in reversed(path):
            st += 1
            if node & 1:
                od += 1
            if node > pk:
                pk = node
            steps_cache[node] = st
            odd_cache[node] = od
            peak_cache[node] = pk

        if st > max_steps_val:
            max_steps_val, max_steps_n = st, start
        if pk > max_peak_val:
            max_peak_val, max_peak_n = pk, start
        # Exact rational comparison pk/start > max_ratio_num/max_ratio_den
        if pk * max_ratio_den > max_ratio_num * start:
            max_ratio_n, max_ratio_num, max_ratio_den = start, pk, start
        # Exact odd density comparison od/st for trajectories with st >= 50
        if st >= 50 and od * max_odd_den > max_odd_num * st:
            max_odd_density_n, max_odd_num, max_odd_den = start, od, st

    benchmarks = [collatz_stats(seed) for seed in (27, 703, 9663, 77031, 837799)]
    terras = verify_terras_bijection(12)

    payload: dict[str, Any] = {
        "problem_id": "NT-005",
        "problem_name": "Collatz Conjecture (3n + 1 Problem)",
        "track": "Track B — Reproducible Finite Computational Exploration",
        "epistemic_status": "OPEN — Finite exact verification only; proves ZERO part of NT-005.",
        "sweep_range": {"min_n": 1, "max_n": sweep_limit, "all_converged_to_1": True},
        "sweep_records": {
            "longest_stopping_time": {"n": max_steps_n, "steps": max_steps_val, "odd_steps": odd_cache[max_steps_n]},
            "highest_peak_value": {"n": max_peak_n, "peak": max_peak_val},
            "highest_excursion_ratio": {
                "n": max_ratio_n,
                "peak": max_ratio_num,
                "ratio_rounded": round(max_ratio_num / max_ratio_den, 4),
            },
            "highest_odd_density_steps_ge_50": {
                "n": max_odd_density_n,
                "odd_steps": max_odd_num,
                "total_steps": max_odd_den,
                "density_rounded": round(max_odd_num / max_odd_den, 6),
                "heuristic_critical_log2_div_log3": 0.630930,
            },
        },
        "canonical_benchmarks": benchmarks,
        "terras_parity_bijection_k1_to_k12": terras,
    }
    raw_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payload["sha256_canonical_json"] = hashlib.sha256(raw_bytes).hexdigest()
    return payload


def main() -> None:
    res = run_probe(100_000)
    RESULTS_PATH.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    rec = res["sweep_records"]
    print(
        f"PASS [Track B NT-005]: Verified 1..100,000 exact Collatz convergence | "
        f"max_steps n={rec['longest_stopping_time']['n']} ({rec['longest_stopping_time']['steps']} steps) | "
        f"max_peak n={rec['highest_peak_value']['n']} ({rec['highest_peak_value']['peak']:,}) | "
        f"Terras parity bijection verified k=1..12 | NT-005 remains OPEN."
    )


if __name__ == "__main__":
    main()
