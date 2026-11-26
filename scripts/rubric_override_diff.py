#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Community Rubric Override & Sensitivity Diff Engine (Roadmap v2.8.0 / Claim C9).

Makes Claim C9 (editorial subjectivity of 1-10 rubric inputs and CSS weights)
quantitatively falsifiable in one command: accepts custom CSS weight vectors
and/or structured per-problem rating overrides, recomputes all 1,900 ranks
deterministically, and reports Spearman rho, Kendall tau, Top-25 Jaccard
overlap, Quadrant migration counts, and Top-10 rank risers & fallers.

Usage:
  python scripts/rubric_override_diff.py --override examples/rubric_override_sample.json
  python scripts/rubric_override_diff.py --weights 0.30,0.40,0.10,0.20 --json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from scipy.stats import kendalltau, spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from v2_loader import (  # noqa: E402
    ATLAS_VERSION,
    classify_quadrant,
    load_v2_master,
)

DEFAULT_CSS_WEIGHTS = (0.40, 0.30, 0.20, 0.10)  # (difficulty, centrality, antiquity, intractability)


def compute_titan_index(difficulty: int, impact: int, interdisciplinarity: int, degree: int) -> float:
    return round(
        0.35 * float(difficulty)
        + 0.35 * float(impact)
        + 0.20 * float(interdisciplinarity)
        + 0.10 * min(10.0, 2.5 * math.log1p(max(0, degree))),
        2,
    )


def compute_weighted_css(
    difficulty: int,
    impact: int,
    degree: int,
    age_years: int,
    tractability: int,
    weights: tuple[float, float, float, float],
) -> float:
    w_d, w_c, w_a, w_t = weights
    diff_100 = float(difficulty) * 10.0
    deg_norm = min(100.0, 25.0 * math.log1p(max(0, degree)))
    cent_100 = 0.50 * (float(impact) * 10.0) + 0.50 * deg_norm
    age_100 = min(100.0, max(0.0, float(age_years) / 3.0))
    tract_100 = float(tractability) * 10.0
    return round(w_d * diff_100 + w_c * cent_100 + w_a * age_100 + w_t * (100.0 - tract_100), 2)


def validate_weights(weights: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    if len(weights) != 4:
        raise ValueError("css_weights must contain exactly 4 numbers [w_diff, w_cent, w_age, w_tract]")
    if any(w < 0.0 or w > 1.0 or not math.isfinite(w) for w in weights):
        raise ValueError("Each CSS weight must be finite and in [0.0, 1.0]")
    total = sum(weights)
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"CSS weights must sum to 1.0 (got {total:.6f})")
    return weights


def evaluate_rubric_override(
    css_weights: tuple[float, float, float, float] = DEFAULT_CSS_WEIGHTS,
    problem_overrides: dict[str, dict[str, int]] | None = None,
    label: str = "custom-override",
    top_movers: int = 10,
) -> dict[str, Any]:
    """Apply alternative CSS weights and/or per-problem (d,t,i,r) overrides and diff all 1,900 ranks."""
    weights = validate_weights(css_weights)
    overrides = problem_overrides or {}
    master = load_v2_master()
    df = master["df"]
    valid_ids = set(df["id"].tolist())

    unknown_ids = sorted(set(overrides.keys()) - valid_ids)
    if unknown_ids:
        raise ValueError(f"Unknown Problem ID(s) in overrides: {unknown_ids[:5]}")

    allowed_fields = {"difficulty_score", "tractability_2050", "civilizational_impact", "interdisciplinarity_index"}
    for pid, patch in overrides.items():
        if not isinstance(patch, dict):
            raise ValueError(f"Override for {pid} must be a JSON object")
        bad_keys = set(patch.keys()) - allowed_fields
        if bad_keys:
            raise ValueError(f"Unsupported override field(s) for {pid}: {sorted(bad_keys)}")
        for k, v in patch.items():
            if isinstance(v, bool) or not isinstance(v, int) or not (1 <= v <= 10):
                raise ValueError(f"Override {pid}.{k} must be an integer in 1..10 (got {v!r})")

    base_rows: list[dict[str, Any]] = []
    alt_rows: list[dict[str, Any]] = []
    quad_migrations: dict[str, int] = {}

    for rec in df.to_dict(orient="records"):
        pid = str(rec["id"])
        patch = overrides.get(pid, {})
        d = int(patch.get("difficulty_score", rec["difficulty_score"]))
        t = int(patch.get("tractability_2050", rec["tractability_2050"]))
        imp = int(patch.get("civilizational_impact", rec["civilizational_impact"]))
        inter = int(patch.get("interdisciplinarity_index", rec["interdisciplinarity_index"]))
        deg = int(rec["graph_degree"])
        age = int(rec["age_years_2026"])

        base_css = float(rec["css_score"])
        alt_css = compute_weighted_css(d, imp, deg, age, t, weights)
        alt_titan = compute_titan_index(d, imp, inter, deg)
        base_q = str(rec["strategic_quadrant"]).split(":", 1)[0]
        alt_q = classify_quadrant(imp, t).split(":", 1)[0]
        if base_q != alt_q:
            key = f"{base_q}->{alt_q}"
            quad_migrations[key] = quad_migrations.get(key, 0) + 1

        base_rows.append({"id": pid, "name": rec["name"], "css": base_css})
        alt_rows.append({"id": pid, "name": rec["name"], "css": alt_css, "titan": alt_titan})

    base_sorted = sorted(base_rows, key=lambda r: (-r["css"], r["id"]))
    alt_sorted = sorted(alt_rows, key=lambda r: (-r["css"], r["id"]))
    base_rank = {r["id"]: idx + 1 for idx, r in enumerate(base_sorted)}
    alt_rank = {r["id"]: idx + 1 for idx, r in enumerate(alt_sorted)}

    ordered_ids = [r["id"] for r in base_rows]
    b_scores = [r["css"] for r in base_rows]
    a_scores = [r["css"] for r in alt_rows]

    rho_res = spearmanr(b_scores, a_scores)
    tau_res = kendalltau(b_scores, a_scores)
    spearman_rho = round(float(rho_res.statistic), 6)
    kendall_tau = round(float(tau_res.statistic), 6)

    top25_base = {r["id"] for r in base_sorted[:25]}
    top25_alt = {r["id"] for r in alt_sorted[:25]}
    top25_jaccard = round(len(top25_base & top25_alt) / len(top25_base | top25_alt), 4)

    movers = []
    abs_shifts = []
    name_map = {r["id"]: r["name"] for r in base_rows}
    b_map = {r["id"]: r["css"] for r in base_rows}
    a_map = {r["id"]: r["css"] for r in alt_rows}
    for pid in ordered_ids:
        shift = base_rank[pid] - alt_rank[pid]  # positive => rose in rank (smaller rank index)
        abs_shifts.append(abs(shift))
        movers.append({
            "id": pid,
            "name": name_map[pid],
            "base_rank": base_rank[pid],
            "alt_rank": alt_rank[pid],
            "rank_delta": shift,
            "base_css": b_map[pid],
            "alt_css": a_map[pid],
        })

    risers = sorted(movers, key=lambda m: (-m["rank_delta"], m["alt_rank"]))[:top_movers]
    fallers = sorted(movers, key=lambda m: (m["rank_delta"], m["alt_rank"]))[:top_movers]

    return {
        "atlas_version": ATLAS_VERSION,
        "scenario_label": label,
        "problems_evaluated": len(ordered_ids),
        "baseline_css_weights": list(DEFAULT_CSS_WEIGHTS),
        "override_css_weights": list(weights),
        "problem_overrides_applied": len(overrides),
        "rank_correlation": {
            "spearman_rho": spearman_rho,
            "kendall_tau": kendall_tau,
            "top25_jaccard_overlap": top25_jaccard,
            "top25_shared_count": len(top25_base & top25_alt),
            "mean_abs_rank_shift": round(sum(abs_shifts) / len(abs_shifts), 2),
            "max_abs_rank_shift": max(abs_shifts),
        },
        "quadrant_migrations": quad_migrations,
        "top_alt_ranked_10": [
            {"rank": i + 1, "id": r["id"], "name": r["name"], "alt_css": r["css"], "base_rank": base_rank[r["id"]]}
            for i, r in enumerate(alt_sorted[:10])
        ],
        "biggest_risers": risers,
        "biggest_fallers": fallers,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate community rubric overrides & sensitivity diffs on all 1,900 Mega-Atlas problems.")
    parser.add_argument("--override", type=Path, help="Path to JSON override specification file")
    parser.add_argument("--weights", type=str, help="Comma-separated CSS weights w_diff,w_cent,w_age,w_tract (sum=1.0)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    weights = DEFAULT_CSS_WEIGHTS
    overrides: dict[str, dict[str, int]] = {}
    label = "cli-sensitivity"

    if args.override:
        spec = json.loads(args.override.read_text(encoding="utf-8"))
        label = str(spec.get("label", args.override.stem))
        if "css_weights" in spec:
            raw_w = spec["css_weights"]
            weights = (float(raw_w[0]), float(raw_w[1]), float(raw_w[2]), float(raw_w[3]))
        overrides = spec.get("problem_overrides", {})

    if args.weights:
        parts = [float(x.strip()) for x in args.weights.split(",")]
        if len(parts) != 4:
            raise SystemExit("ERROR: --weights requires 4 comma-separated floats summing to 1.0")
        weights = (parts[0], parts[1], parts[2], parts[3])

    res = evaluate_rubric_override(css_weights=weights, problem_overrides=overrides, label=label)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        rc = res["rank_correlation"]
        print(
            f"Rubric Override Sensitivity Diff [{res['scenario_label']}] (N={res['problems_evaluated']}):\n"
            f"  Weights: {res['baseline_css_weights']} -> {res['override_css_weights']} | Per-problem overrides: {res['problem_overrides_applied']}\n"
            f"  Spearman rho = {rc['spearman_rho']:.4f} | Kendall tau = {rc['kendall_tau']:.4f} | "
            f"Top-25 Jaccard = {rc['top25_jaccard_overlap']:.4f} ({rc['top25_shared_count']}/25 shared)\n"
            f"  Mean |dRank| = {rc['mean_abs_rank_shift']:.2f} | Max |dRank| = {rc['max_abs_rank_shift']} | Quadrant migrations = {res['quadrant_migrations']}"
        )


if __name__ == "__main__":
    main()
