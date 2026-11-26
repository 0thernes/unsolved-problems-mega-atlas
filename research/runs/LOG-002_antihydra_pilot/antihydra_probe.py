#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
AutoResearch Track B Pilot — LOG-002 (Busy Beaver BB(6) / Antihydra Recurrence Probe)
Author: Alexander Stephen Donahue (Independent Researcher, ORCID 0009-0006-8168-9648)

EPISTEMIC BOUNDARY (READ FIRST):
  This script performs EXACT arbitrary-precision finite computational exploration
  of the Antihydra Collatz-like threshold map H(a, b) associated with the 6-state
  Busy Beaver holdout (mxdys / bbchallenge 2024). It proves NO asymptotic halting or
  non-halting theorem for Antihydra or BB(6) (status remains OPEN).

Exact Antihydra Recurrence (starting from a_0 = 8, b_0 = 0):
  - If a is even: (a, b) -> (3*a // 2, b + 2)
  - If a is odd : (a, b) -> ((3*a - 1) // 2, b - 1)
  - Halts iff b == -1.

We probe:
  1. Exact canonical Antihydra trajectory for N = 5,000 macro-steps (exact Python bigints),
     recording parity balance, minimum b margin, growth rate log2(a_n), and empirical drift.
  2. Perturbation margin sweep across nearby initial seeds a_0 in [2, 100] (b_0 = 0) up to
     2,000 macro-steps each, mapping the exact halting vs. escaping boundary!
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Any

OUT_JSON = Path(__file__).resolve().parent / "RESULTS.json"


def run_antihydra(a0: int, b0: int = 0, max_steps: int = 5000) -> Dict[str, Any]:
    a, b = a0, b0
    evens = 0
    odds = 0
    min_b = b
    max_b = b
    halted_at = None

    for step in range(1, max_steps + 1):
        if a % 2 == 0:
            a = (3 * a) // 2
            b += 2
            evens += 1
        else:
            a = (3 * a - 1) // 2
            b -= 1
            odds += 1
        if b < min_b:
            min_b = b
        if b > max_b:
            max_b = b
        if b == -1:
            halted_at = step
            break

    steps_done = halted_at if halted_at is not None else max_steps
    even_frac = round(evens / max(1, steps_done), 6)
    drift_per_step = round((b - b0) / max(1, steps_done), 6)
    return {
        "a0": a0,
        "b0": b0,
        "steps_executed": steps_done,
        "halted": halted_at is not None,
        "halted_at_step": halted_at,
        "final_b": b,
        "min_b_margin": min_b,
        "max_b": max_b,
        "even_steps": evens,
        "odd_steps": odds,
        "even_fraction": even_frac,
        "empirical_b_drift_per_step": drift_per_step,
        "final_a_bit_length": a.bit_length(),
        "log2_a_per_step": round(a.bit_length() / max(1, steps_done), 6),
    }


def main() -> None:
    canonical = run_antihydra(a0=8, b0=0, max_steps=5000)
    halted_seeds = []
    surviving_seeds = []
    min_b_near_zero = []

    for seed in range(2, 101):
        res = run_antihydra(a0=seed, b0=0, max_steps=2000)
        if res["halted"]:
            halted_seeds.append({"a0": seed, "halted_at_step": res["halted_at_step"]})
        else:
            surviving_seeds.append(seed)
            if res["min_b_margin"] <= 2:
                min_b_near_zero.append({"a0": seed, "min_b_margin": res["min_b_margin"], "final_b": res["final_b"]})

    report = {
        "problem_id": "LOG-002",
        "pilot_name": "Antihydra Collatz-Like BB(6) Finite Margin & Perturbation Probe",
        "author": "Alexander Stephen Donahue (Independent Researcher, ORCID 0009-0006-8168-9648)",
        "epistemic_boundary": (
            "Finite exact arbitrary-precision computational probe ONLY. Proves NO asymptotic halting "
            "or non-halting theorem for Antihydra or Busy Beaver BB(6); LOG-002 remains OPEN."
        ),
        "theoretical_random_walk_drift": 0.5,
        "theoretical_log2_growth_per_step": round(math.log2(1.5), 6),
        "canonical_a0_8_5000_steps": canonical,
        "seed_sweep_a0_2_to_100_max2000": {
            "total_seeds_tested": 99,
            "halted_count": len(halted_seeds),
            "surviving_count": len(surviving_seeds),
            "halted_seeds_sample": halted_seeds[:20],
            "surviving_close_calls_min_b_le_2": min_b_near_zero[:15],
        },
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Canonical Antihydra (a0=8, 5000 steps): halted={canonical['halted']} | final_b={canonical['final_b']} | "
          f"min_b={canonical['min_b_margin']} | even_frac={canonical['even_fraction']} | drift={canonical['empirical_b_drift_per_step']}/step | "
          f"bitlen(a)={canonical['final_a_bit_length']}")
    print(f"Perturbation sweep a0 in [2..100] (2000 steps): {len(halted_seeds)} halted, {len(surviving_seeds)} survived.")


if __name__ == "__main__":
    main()
