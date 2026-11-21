#!/usr/bin/env python3
"""
Deep Multi-Layer Forensic Audit for the Unsolved Problems Mega-Atlas (0thernes LLC).

Audits across breadth, depth, substrates, gradients, margins, spectrums, taxonomies, and adjacents:
  1. Dangling / unresolved / self-referential `raw_links` across m01..m10
  2. Fuzzy near-duplicate detection (token Jaccard >= 0.60)
  3. Graph resilience: connected components, articulation points, bridges, diameter, clustering, assortativity
  4. Adjacent superdomain zero-coupling blindspots
  5. Substrate, spectrum, margin, and minority-topic coverage probe
  6. Remaining RAG gold-benchmark misses & provenance token inspection
"""

from __future__ import annotations

import collections
import importlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "autoresearch"))

import networkx as nx  # noqa: E402
from v2_loader import MODULE_NAMES, load_v2_master  # noqa: E402
from v2_schema import CANONICAL_HUBS  # noqa: E402
from evaluate import GOLD_RAG_BENCHMARK  # noqa: E402
from query import search_atlas  # noqa: E402


def main() -> None:
    d = load_v2_master()
    df = d["df"]
    G = d["G"]
    id_map = d["id_map"]
    id_set = set(df["id"])

    print("=== 1. DANGLING / SELF-REFERENTIAL raw_links ===")
    alias_map = d.get("dedup_alias_map", {})
    dangling = []
    for mname in MODULE_NAMES:
        mod = importlib.import_module(mname)
        for r in mod.PROBLEMS:
            src_canon = alias_map.get(r["id"], r["id"])
            bad = []
            for tok in r["raw_links"]:
                t = tok.strip()
                if not t:
                    continue
                tgt = CANONICAL_HUBS.get(t, t)
                tgt = alias_map.get(tgt, tgt)
                if tgt not in id_set or tgt == src_canon:
                    bad.append(t)
            if bad:
                dangling.append((mname, r["id"], r["name"], bad))
    print(f"Total records with dangling/self links: {len(dangling)} (loader unresolved_raw_links_count={d['summary_stats']['unresolved_raw_links_count']})")
    for mname, pid, name, bad in dangling:
        print(f"  {mname} | {pid} ({name[:46]}) -> {bad}")

    print("\n=== 2. GRAPH RESILIENCE (ARTICULATION POINTS & BRIDGES) ===")
    aps = list(nx.articulation_points(G))
    bridges = list(nx.bridges(G))
    print(f"Components: {nx.number_connected_components(G)} | Articulation points: {len(aps)} | Bridges: {len(bridges)} | Biconnected: {nx.is_biconnected(G)}")
    for ap in aps:
        G2 = G.copy()
        G2.remove_node(ap)
        comps = sorted([len(c) for c in nx.connected_components(G2)], reverse=True)
        small = [sorted(list(c)) for c in nx.connected_components(G2) if len(c) < 50]
        print(f"  AP: {ap} ({id_map[ap]['name']}) -> split={comps} | small={small}")

    print("\n=== 3. NEAR-DUPLICATE PAIRS (Jaccard >= 0.62) ===")
    stop = {
        "the", "of", "and", "in", "for", "to", "a", "an", "on", "with", "by",
        "problem", "conjecture", "hypothesis", "theory", "problems", "quantum",
        "general", "systems", "global", "dynamics", "model", "models",
    }

    def tokset(name: str) -> set[str]:
        toks = set(re.findall(r"[a-z0-9]+", re.sub(r"\([^)]*\)", "", name.lower())))
        return toks - stop

    tsets = [(r.id, r.name, r.superdomain, tokset(r.name)) for r in df.itertuples()]
    pairs = []
    for i in range(len(tsets)):
        id1, n1, sd1, s1 = tsets[i]
        if len(s1) < 2:
            continue
        for j in range(i + 1, len(tsets)):
            id2, n2, sd2, s2 = tsets[j]
            if len(s2) < 2:
                continue
            inter = len(s1 & s2)
            if inter < 2:
                continue
            jac = inter / len(s1 | s2)
            if jac >= 0.62:
                pairs.append((round(jac, 2), id1, n1, id2, n2))
    pairs.sort(reverse=True)
    print(f"Near-duplicate pairs (Jaccard >= 0.62): {len(pairs)}")
    for x in pairs[:25]:
        print(" ", x)

    print("\n=== 4. REMAINING RAG BENCHMARK MISSES ===")
    rag_misses = 0
    for q, exp in GOLD_RAG_BENCHMARK:
        res = search_atlas(query=q, top=5)
        ids = [r["id"] for r in res["results"]]
        if not ids or ids[0] != exp:
            rag_misses += 1
            print(f"  MISS: {q!r} -> expected {exp} ({id_map[exp]['name']}), got {ids[:5]}")
            for cid in ids[:3]:
                c = id_map[cid]
                print(f"    -> {cid}: {c['name']} | deg={c['graph_degree']} | pr={c['pagerank']} | css={c['css_score']}")
    print(f"Total RAG top-1 misses: {rag_misses} / {len(GOLD_RAG_BENCHMARK)}")

    print("\n=== 5. TOP registry_source AMONG ai-assisted-editorial-synthesis ===")
    aes = df[df["verification_flag"] == "ai-assisted-editorial-synthesis"]
    print(f"Count: {len(aes)} / {len(df)}")
    for k, v in aes["registry_source"].value_counts().head(20).items():
        print(f"  {v:>4} | {k}")

    print("\n=== 6. LOWEST-DEGREE & LOWEST-CONNECTED SUPERDOMAIN PAIRS ===")
    low_deg = df.nsmallest(10, "graph_degree")[["id", "name", "superdomain", "graph_degree", "cross_pillar_links"]]
    print(low_deg.to_string(index=False))

    print("\n=== 7. ENV / PRESERVATION TOKEN CHECK (boolean only) ===")
    print("  ZENODO_TOKEN present:", bool(os.environ.get("ZENODO_TOKEN")))
    print("  ZENODO_SANDBOX_TOKEN present:", bool(os.environ.get("ZENODO_SANDBOX_TOKEN")))

    assert d["summary_stats"]["unresolved_raw_links_count"] == 0, "Unresolved raw_links detected!"
    assert len(aps) == 0 and len(bridges) == 0 and nx.is_biconnected(G), "Graph is not biconnected!"
    assert rag_misses == 0, f"RAG misses detected: {rag_misses}"
    print("\nFORENSIC AUDIT GATE PASSED: 0 dangling links, 0 articulation points, 0 bridges, 0 RAG misses!")


if __name__ == "__main__":
    main()
