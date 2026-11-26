#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Track B Reproducible Frontier Probe #3 — COMB-001 (Ramsey Lower-Bound Witnesses).

Constructs and exhaustively certifies 7 explicit circulant & Paley graph witnesses
proving exact finite Ramsey lower bounds via deterministic bitmask clique search:
  - R(3,3) > 5    via Paley P_5                  (tight: R(3,3) = 6)
  - R(3,4) > 8    via Circulant C_8({1,4})       (tight: R(3,4) = 9)
  - R(3,5) > 13   via Circulant C_13({1,5})      (tight: R(3,5) = 14)
  - R(4,4) > 17   via Paley P_17                 (tight: R(4,4) = 18)
  - R(4,5) > 24   via Circulant C_24({1,2,4,8,9})(tight: R(4,5) = 25)
  - R(5,5) > 37   via Paley P_37                 (frontier: R(5,5) in [43, 46])
  - R(6,6) > 101  via Paley P_101                (frontier: R(6,6) in [102, 160])

Because every graph is a circulant over Z_n, rotational shift i -> (i+1) mod n
is an exact automorphism (verified explicitly on the adjacency matrix), so a
k-clique exists iff one contains vertex 0. For all n <= 37 we additionally run
full all-vertex search as a cross-check.

HONEST VERIFICATION BOUNDARY:
  Certifies finite constructive lower bounds ONLY. Explicitly makes ZERO claim
  to determine exact R(5,5), R(6,6), or asymptotic R(k,k) bounds (COMB-001
  remains OPEN).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

RUN_DIR = Path(__file__).resolve().parent
RESULTS_PATH = RUN_DIR / "RESULTS.json"


def circulant_adj(n: int, diffs: tuple[int, ...]) -> list[int]:
    adj = [0] * n
    for i in range(n):
        mask = 0
        for d in diffs:
            j1 = (i + d) % n
            j2 = (i - d) % n
            if j1 != i:
                mask |= 1 << j1
            if j2 != i:
                mask |= 1 << j2
        adj[i] = mask
    return adj


def paley_diffs(p: int) -> tuple[int, ...]:
    if p % 4 != 1:
        raise ValueError(f"Paley prime must satisfy p == 1 (mod 4), got {p}")
    qr = sorted({(x * x) % p for x in range(1, p)} & set(range(1, p // 2 + 1)))
    return tuple(qr)


def complement_adj(adj: list[int]) -> list[int]:
    n = len(adj)
    full = (1 << n) - 1
    return [full ^ adj[v] ^ (1 << v) for v in range(n)]


def verify_cyclic_automorphism_and_symmetry(adj: list[int]) -> bool:
    n = len(adj)
    for u in range(n):
        if (adj[u] >> u) & 1:
            return False
        for v in range(n):
            uv = (adj[u] >> v) & 1
            vu = (adj[v] >> u) & 1
            if uv != vu:
                return False
            u1, v1 = (u + 1) % n, (v + 1) % n
            if uv != ((adj[u1] >> v1) & 1):
                return False
    return True


def has_clique_containing_zero(adj: list[int], k: int) -> bool:
    def dfs(candidates: int, depth: int) -> bool:
        if depth == 0:
            return True
        if candidates.bit_count() < depth:
            return False
        c = candidates
        while c:
            lsb = c & -c
            v = lsb.bit_length() - 1
            c ^= lsb
            if dfs(c & adj[v], depth - 1):
                return True
        return False

    return dfs(adj[0], k - 1)


def has_clique_full(adj: list[int], k: int) -> bool:
    n = len(adj)

    def dfs(candidates: int, depth: int) -> bool:
        if depth == 0:
            return True
        if candidates.bit_count() < depth:
            return False
        c = candidates
        while c:
            lsb = c & -c
            v = lsb.bit_length() - 1
            c ^= lsb
            if dfs(c & adj[v], depth - 1):
                return True
        return False

    return dfs((1 << n) - 1, k)


WITNESS_SPECS: tuple[dict[str, Any], ...] = (
    {"label": "Paley P_5", "s": 3, "t": 3, "n": 5, "diffs": paley_diffs(5), "known_status": "Tight lower bound (R(3,3) = 6)"},
    {"label": "Circulant C_8({1,4})", "s": 3, "t": 4, "n": 8, "diffs": (1, 4), "known_status": "Tight lower bound (R(3,4) = 9)"},
    {"label": "Circulant C_13({1,5})", "s": 3, "t": 5, "n": 13, "diffs": (1, 5), "known_status": "Tight lower bound (R(3,5) = 14)"},
    {"label": "Paley P_17", "s": 4, "t": 4, "n": 17, "diffs": paley_diffs(17), "known_status": "Tight lower bound (R(4,4) = 18)"},
    {"label": "Circulant C_24({1,2,4,8,9})", "s": 4, "t": 5, "n": 24, "diffs": (1, 2, 4, 8, 9), "known_status": "Tight lower bound (R(4,5) = 25)"},
    {"label": "Paley P_37", "s": 5, "t": 5, "n": 37, "diffs": paley_diffs(37), "known_status": "Classic Paley witness (open frontier R(5,5) in [43, 46])"},
    {"label": "Paley P_101", "s": 6, "t": 6, "n": 101, "diffs": paley_diffs(101), "known_status": "Classic Paley witness (open frontier R(6,6) in [102, 160])"},
)


def run_probe() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for spec in WITNESS_SPECS:
        n: int = spec["n"]
        s: int = spec["s"]
        t: int = spec["t"]
        diffs: tuple[int, ...] = spec["diffs"]
        adj = circulant_adj(n, diffs)
        comp = complement_adj(adj)

        aut_ok = verify_cyclic_automorphism_and_symmetry(adj)
        if not aut_ok:
            raise AssertionError(f"Cyclic automorphism verification failed for {spec['label']}")

        has_ks = has_clique_containing_zero(adj, s)
        has_it = has_clique_containing_zero(comp, t)
        # Tightness: verify both an (s-1)-clique and a (t-1)-independent set DO exist!
        has_ks_minus_1 = has_clique_containing_zero(adj, s - 1)
        has_it_minus_1 = has_clique_containing_zero(comp, t - 1)

        full_crosscheck = False
        if n <= 37:
            assert has_clique_full(adj, s) == has_ks
            assert has_clique_full(comp, t) == has_it
            full_crosscheck = True

        certified = (not has_ks) and (not has_it) and has_ks_minus_1 and has_it_minus_1
        if not certified:
            raise AssertionError(f"Ramsey witness certification failed for {spec['label']}")

        records.append({
            "label": spec["label"],
            "lower_bound_proved": f"R({s},{t}) > {n}",
            "s": s,
            "t": t,
            "vertices": n,
            "regular_degree": adj[0].bit_count(),
            "difference_set": list(diffs),
            "cyclic_automorphism_verified": aut_ok,
            "all_vertex_crosscheck": full_crosscheck,
            "omega_exact": s - 1,
            "alpha_exact": t - 1,
            "has_K_s": has_ks,
            "has_I_t": has_it,
            "certified": certified,
            "known_status": spec["known_status"],
        })

    payload: dict[str, Any] = {
        "problem_id": "COMB-001",
        "problem_name": "Diagonal & Off-Diagonal Ramsey Numbers R(k,k) (incl. R(5,5) & R(6,6))",
        "track": "Track B — Reproducible Finite Constructive Witness Certification",
        "epistemic_status": "OPEN — Finite constructive lower-bound witnesses only; proves ZERO upper bound or exact value for R(5,5)/R(6,6)/COMB-001.",
        "witnesses_certified_count": len(records),
        "witnesses": records,
    }
    raw_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payload["sha256_canonical_json"] = hashlib.sha256(raw_bytes).hexdigest()
    return payload


def main() -> None:
    res = run_probe()
    RESULTS_PATH.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    bounds = ", ".join(w["lower_bound_proved"] for w in res["witnesses"])
    print(f"PASS [Track B COMB-001]: Certified {res['witnesses_certified_count']}/7 exact Ramsey witnesses ({bounds}) | COMB-001 remains OPEN.")


if __name__ == "__main__":
    main()
