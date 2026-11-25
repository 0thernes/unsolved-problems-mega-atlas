#!/usr/bin/env python3
"""Minimal runnable example querying the offline Mega-Atlas RAG & pairwise comparator."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "rag"))

from query import compare_two_problems, search_atlas


def main() -> int:
    res = search_atlas(query="Riemann Hypothesis zeta zeros", top=3, hops=1)
    print(f"Top {res['count']} hits for 'Riemann Hypothesis zeta zeros':")
    for item in res["results"]:
        print(f"  - {item['id']}: {item['name']} (CSS={item['css_score']}, flag={item['verification_flag']})")

    cmp = compare_two_problems("NT-001", "CS-001")
    print("\nPairwise delta (NT-001 minus CS-001):", cmp["deltas_a_minus_b"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
