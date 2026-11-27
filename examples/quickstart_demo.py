#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Quickstart Demo (Build Standard A43):
Demonstrates loading the 2,000-problem Mega-Atlas, running offline Hybrid RAG search,
comparing two flagship open problems side-by-side, and verifying differential parity
against the 50-digit Decimal reference oracle — zero API keys, zero network calls.
"""

from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "reference"))

from query import compare_two_problems, search_atlas  # noqa: E402
from scoring_oracle import oracle_css_score  # noqa: E402
from v2_loader import compute_css_score, load_v2_master  # noqa: E402


def main() -> None:
    data = load_v2_master()
    s = data["summary_stats"]
    print(f"Loaded Unsolved Problems Mega-Atlas v{s['atlas_version']}:")
    print(f"  Problems: {s['total_problems']:,} | Edges: {s['total_graph_edges']:,} | Biconnected APs: {s['articulation_points']}")
    print(f"  Mean 0thernes CSS: {s['mean_css_score']} | Mean Titan: {s['mean_titan_index']} | Nov 2026 AI Claims: {s['ai_claims_nov2026_count']}")

    # 1. Offline Hybrid RAG search with 1-hop graph neighbors
    hit = search_atlas(query="riemann hypothesis zeta zeros", top=3, hops=1)
    top = hit["results"][0]
    print(f"\nTop RAG hit for 'riemann hypothesis zeta zeros': [{top['id']}] {top['name']}")
    print(f"  Status: {top['status_2026']} | Flag: {top['verification_flag']} | CSS: {top['css_score']}")

    # 2. Pairwise side-by-side comparison (Lean-verified antisymmetric deltas)
    cmp = compare_two_problems("NT-001", "CS-001")
    d = cmp["deltas_a_minus_b"]
    print(f"\nCompare NT-001 vs CS-001: dCSS={d['css_score']:+.2f}, dTitan={d['titan_index']:+.2f}, shared_neighbors={cmp['graph_relation']['shared_neighbors_count']}")

    # 3. Reference-oracle differential parity check on NT-001
    py_css = compute_css_score(top["difficulty_score"], top["civilizational_impact"], top["graph_degree"], top["age_years_2026"], top["tractability_2050"])
    ref_css = oracle_css_score(top["difficulty_score"], top["civilizational_impact"], top["graph_degree"], top["age_years_2026"], top["tractability_2050"])
    assert abs(py_css - ref_css) <= 0.01, f"Oracle drift: {py_css} vs {ref_css}"
    print(f"\nReference Oracle parity check on NT-001: Python={py_css:.2f} == 50-digit Decimal={ref_css:.2f} (PASS)")


if __name__ == "__main__":
    main()
