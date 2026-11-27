#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Mutation Testing Audit (Build Standard B13):
Applies 10 targeted semantic mutations across core scoring, quadrant, margin-role,
RAG comparator, rubric-override validation, and all three Track B frontier probes,
verifying that the pytest suite kills 100% (10/10) of planted mutants. Restores
every file cleanly in a `finally` block.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MUTANTS = [
    (
        "M01_css_diff_weight",
        ROOT / "src" / "v2_loader.py",
        "0.40 * diff_100 + 0.30 * cent_100 + 0.20 * age_100 + 0.10 * (100.0 - tract_100)",
        "0.35 * diff_100 + 0.30 * cent_100 + 0.20 * age_100 + 0.10 * (100.0 - tract_100)",
        "tests/test_properties_and_differential.py::test_b10_hypothesis_css_bounds_monotonicity_and_oracle",
    ),
    (
        "M02_age_saturation_cap",
        ROOT / "src" / "v2_loader.py",
        "age_100 = min(100.0, max(0.0, float(age_years) / 3.0))",
        "age_100 = min(100.0, max(0.0, float(age_years) / 4.0))",
        "tests/test_properties_and_differential.py::test_b10_hypothesis_css_bounds_monotonicity_and_oracle",
    ),
    (
        "M03_quadrant_threshold_off_by_one",
        ROOT / "src" / "v2_loader.py",
        "if impact >= 8 and tractability >= 7:",
        "if impact > 8 and tractability >= 7:",
        "tests/test_properties_and_differential.py::test_b10_hypothesis_quadrants_and_q1_leverage_floor",
    ),
    (
        "M04_margin_role_apex_threshold",
        ROOT / "src" / "v2_loader.py",
        "if adj_pillars >= 3:",
        "if adj_pillars >= 4:",
        "tests/test_properties_and_differential.py::test_b10_hypothesis_margin_role_and_spectrum",
    ),
    (
        "M05_epistemic_spectrum_clamp",
        ROOT / "src" / "v2_loader.py",
        "return round(min(100.0, max(0.0, val)), 1)",
        "return round(min(90.0, max(0.0, val)), 1)",
        "tests/test_properties_and_differential.py::test_b20_epistemic_spectrum_clamping_edges",
    ),
    (
        "M06_comparator_delta_sign_flip",
        ROOT / "rag" / "query.py",
        '"css_score": round(pa["css_score"] - pb["css_score"], 2),',
        '"css_score": round(pa["css_score"] + pb["css_score"], 2),',
        "tests/test_mega_atlas.py::test_pairwise_comparator_antisymmetry",
    ),
    (
        "M07_rubric_override_weight_sum_guard",
        ROOT / "scripts" / "rubric_override_diff.py",
        "if abs(total - 1.0) > 1e-6:",
        "if abs(total - 1.0) > 10.0:",
        "tests/test_properties_and_differential.py::test_b06_rubric_override_rejects_invalid_weights_ids_and_ratings",
    ),
    (
        "M08_antihydra_odd_transition",
        ROOT / "research" / "runs" / "LOG-002_antihydra_pilot" / "antihydra_probe.py",
        "            b -= 1",
        "            b -= 2",
        "tests/test_mega_atlas.py::test_track_b_antihydra_pilot_artifact_reproducible",
    ),
    (
        "M09_collatz_compressed_parity",
        ROOT / "research" / "runs" / "NT-005_collatz_parity_pilot" / "collatz_probe.py",
        "            cur = (3 * cur + 1) >> 1",
        "            cur = (3 * cur + 3) >> 1",
        "tests/test_properties_and_differential.py::test_b07_regression_track_b_collatz_pilot_reproducible",
    ),
    (
        "M10_ramsey_automorphism_symmetry",
        ROOT / "research" / "runs" / "COMB-002_ramsey_witness_pilot" / "ramsey_probe.py",
        "            if uv != vu:",
        "            if uv == vu:",
        "tests/test_properties_and_differential.py::test_b07_regression_track_b_ramsey_witnesses_reproducible",
    ),
]


def main() -> None:
    killed = 0
    results = []
    for mid, path, target, replacement, test_target in MUTANTS:
        original = path.read_text(encoding="utf-8")
        if target not in original:
            print(f"ERROR: mutant {mid} target snippet not found in {path}", file=sys.stderr)
            sys.exit(2)
        try:
            mutated = original.replace(target, replacement, 1)
            path.write_text(mutated, encoding="utf-8", newline="\n")
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", test_target, "-q", "-x", "--tb=no"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            is_killed = proc.returncode != 0
            if is_killed:
                killed += 1
            results.append((mid, "KILLED" if is_killed else "SURVIVED", proc.returncode))
            print(f"  [{('KILLED' if is_killed else 'SURVIVED'):<8}] {mid} (exit={proc.returncode})")
        finally:
            path.write_text(original, encoding="utf-8", newline="\n")

    score = 100.0 * killed / len(MUTANTS)
    print(f"\nMutation Audit Summary: {killed}/{len(MUTANTS)} killed ({score:.1f}% kill rate)")
    if killed != len(MUTANTS):
        sys.exit(1)


if __name__ == "__main__":
    main()
