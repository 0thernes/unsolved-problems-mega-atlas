#!/usr/bin/env python3
"""
Offline Deterministic RAG & Knowledge-Graph Query Engine for the
Unsolved Problems Mega-Atlas (V2.1.0, 0thernes LLC).

Powered by SQLite FTS5 BM25 full-text ranking + multi-hop knowledge-graph
expansion over `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` — zero API keys,
zero network calls, sub-30 ms deterministic retrieval with exact provenance IDs.

Examples:
    python rag/query.py "turbulence climate sensitivity" --top 8 --hops 1
    python rag/query.py "Riemann Hypothesis" --top 5 --hops 1 --json
    python rag/query.py --problem NT-001 --hops 1
    python rag/query.py --pillar "Pure Mathematics" --flag ai-claim-under-audit-nov2026
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.sqlite"


def sanitize_fts_query(raw: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_]+", raw)
    if not tokens:
        return ""
    return " OR ".join(f'"{t}"' for t in tokens)


def get_neighbors(conn: sqlite3.Connection, seed_ids: List[str], hops: int = 1) -> Dict[str, List[Dict[str, Any]]]:
    if hops <= 0 or not seed_ids:
        return {}
    cur = conn.cursor()
    frontier = set(seed_ids)
    visited = set(seed_ids)
    neighbor_map: Dict[str, List[str]] = {sid: [] for sid in seed_ids}

    for hop in range(hops):
        next_frontier = set()
        for nid in list(frontier):
            rows = cur.execute(
                "SELECT target FROM edges WHERE source = ? UNION SELECT source FROM edges WHERE target = ?",
                (nid, nid),
            ).fetchall()
            for (nb,) in rows:
                if hop == 0 and nid in neighbor_map:
                    neighbor_map[nid].append(nb)
                if nb not in visited:
                    visited.add(nb)
                    next_frontier.add(nb)
        frontier = next_frontier

    all_nb_ids = sorted({nb for lst in neighbor_map.values() for nb in lst})
    if not all_nb_ids:
        return {sid: [] for sid in seed_ids}

    placeholders = ",".join("?" for _ in all_nb_ids)
    meta_rows = cur.execute(
        f"SELECT id, name, macro_pillar, superdomain, css_score, titan_index, verification_flag "
        f"FROM problems WHERE id IN ({placeholders})",
        all_nb_ids,
    ).fetchall()
    meta_by_id = {
        r[0]: {
            "id": r[0],
            "name": r[1],
            "macro_pillar": r[2],
            "superdomain": r[3],
            "css_score": r[4],
            "titan_index": r[5],
            "verification_flag": r[6],
        }
        for r in meta_rows
    }
    return {
        sid: sorted(
            [meta_by_id[nb] for nb in nbs if nb in meta_by_id],
            key=lambda x: (-x["css_score"], x["id"]),
        )
        for sid, nbs in neighbor_map.items()
    }


def search_atlas(
    query: Optional[str] = None,
    problem_id: Optional[str] = None,
    pillar: Optional[str] = None,
    superdomain: Optional[str] = None,
    flag: Optional[str] = None,
    top: int = 10,
    hops: int = 0,
    db_path: Path = DEFAULT_DB,
) -> Dict[str, Any]:
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite FTS5 database not found at {db_path}. Run `python src/v2_export_all.py`.")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        rows: List[sqlite3.Row] = []

        if problem_id:
            rows = cur.execute("SELECT *, 0.0 AS bm25_score FROM problems WHERE id = ?", (problem_id.upper(),)).fetchall()
        elif query:
            fts_q = sanitize_fts_query(query)
            if not fts_q:
                return {"query": query, "count": 0, "results": []}
            sql = """
                SELECT p.*, bm25(problems_fts, 0.0, 6.0, 2.0, 2.5, 2.5, 1.5, 3.0, 2.0, 1.5, 2.0, 1.5, 2.0, 1.5, 2.0, 1.5) AS bm25_score
                FROM problems_fts
                JOIN problems p ON p.id = problems_fts.id
                WHERE problems_fts MATCH ?
            """
            params: List[Any] = [fts_q]
            if pillar:
                sql += " AND p.macro_pillar = ?"
                params.append(pillar)
            if superdomain:
                sql += " AND p.superdomain = ?"
                params.append(superdomain)
            if flag:
                sql += " AND p.verification_flag = ?"
                params.append(flag)
            sql += " ORDER BY bm25_score ASC, p.css_score DESC LIMIT ?"
            params.append(top)
            rows = cur.execute(sql, params).fetchall()
        else:
            sql = "SELECT *, 0.0 AS bm25_score FROM problems WHERE 1=1"
            params = []
            if pillar:
                sql += " AND macro_pillar = ?"
                params.append(pillar)
            if superdomain:
                sql += " AND superdomain = ?"
                params.append(superdomain)
            if flag:
                sql += " AND verification_flag = ?"
                params.append(flag)
            sql += " ORDER BY css_score DESC, titan_index DESC LIMIT ?"
            params.append(top)
            rows = cur.execute(sql, params).fetchall()

        results = [dict(r) for r in rows]
        if hops > 0 and results:
            nbs = get_neighbors(conn, [r["id"] for r in results], hops=hops)
            for r in results:
                r["graph_neighbors"] = nbs.get(r["id"], [])[:8]

        return {
            "query": query or problem_id or f"filter(pillar={pillar}, superdomain={superdomain}, flag={flag})",
            "count": len(results),
            "results": results,
        }
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline BM25 + Knowledge-Graph RAG Query CLI (0thernes Mega-Atlas V2.1.0)")
    parser.add_argument("query", nargs="?", default=None, help="Free-text search query (FTS5 BM25)")
    parser.add_argument("--problem", dest="problem_id", default=None, help="Exact Problem ID (e.g., NT-001, CS-001, GR-001)")
    parser.add_argument("--pillar", default=None, help="Filter by exact Macro-Pillar name")
    parser.add_argument("--superdomain", default=None, help="Filter by exact Superdomain name")
    parser.add_argument("--flag", default=None, help="Filter by verification_flag")
    parser.add_argument("--top", type=int, default=8, help="Maximum hits to return (default: 8)")
    parser.add_argument("--hops", type=int, default=0, help="Knowledge-graph neighbor hops to expand (0 or 1)")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    out = search_atlas(
        query=args.query,
        problem_id=args.problem_id,
        pillar=args.pillar,
        superdomain=args.superdomain,
        flag=args.flag,
        top=args.top,
        hops=args.hops,
    )

    if args.as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"=== 0thernes Mega-Atlas Offline RAG | Query: {out['query']} | Hits: {out['count']} ===\n")
    for idx, r in enumerate(out["results"], 1):
        yr = f"{abs(r['year_formulated'])} BCE" if r["year_formulated"] < 0 else str(r["year_formulated"])
        print(f"{idx:>2}. [{r['id']}] {r['name']} ({yr})")
        print(f"    Pillar: {r['macro_pillar']} > {r['superdomain']} | CSS: {r['css_score']:.2f} | Titan: {r['titan_index']:.2f} | Deg: {r['graph_degree']}")
        print(f"    Status: {r['status_2026']} | Flag: {r['verification_flag']}")
        print(f"    Question: {r['core_question']}")
        print(f"    Formula : {r['formal_expression']}")
        if "graph_neighbors" in r and r["graph_neighbors"]:
            nb_str = ", ".join(f"{n['id']} ({n['name'][:32]})" for n in r["graph_neighbors"][:5])
            print(f"    1-Hop Neighbors: {nb_str}")
        print()


if __name__ == "__main__":
    main()
