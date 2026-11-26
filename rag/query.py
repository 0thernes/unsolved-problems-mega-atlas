#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Offline Deterministic RAG & Knowledge-Graph Query Engine for the
Unsolved Problems Mega-Atlas (V2.6.0, Alexander Stephen Donahue).

Powered by SQLite FTS5 staged BM25 ranking (Exact phrase + Strict-AND precision pass +
relaxed OR backfill + hybrid title/bigram/PageRank re-ranker) + multi-hop knowledge-graph
expansion + pairwise problem comparison over `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` —
zero API keys, zero network calls, sub-30 ms deterministic retrieval. Automatically
rebuilds the local SQLite FTS5 index on demand on clean git clones or version upgrades.

Examples:
    python rag/query.py "turbulence climate sensitivity" --top 8 --hops 1
    python rag/query.py "Riemann Hypothesis" --top 5 --hops 1 --json
    python rag/query.py --problem NT-001 --hops 1
    python rag/query.py --compare NT-001 CS-001
    python rag/query.py --pillar "Pure Mathematics" --flag ai-claim-under-audit-nov2026
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.sqlite"


def _db_is_fresh(db_path: Path) -> bool:
    """Return True iff `db_path` exists, is readable, and matches the active VERSION & schema."""
    if not (db_path.exists() and db_path.stat().st_size > 0):
        return False
    ver_file = ROOT / "VERSION"
    expected_ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.exists() else None
    try:
        conn = sqlite3.connect(str(db_path))
        try:
            row = conn.execute("SELECT value FROM metadata WHERE key = 'atlas_version'").fetchone()
            if expected_ver and (row is None or str(row[0]).strip() != expected_ver):
                return False
            cnt = conn.execute("SELECT COUNT(*) FROM problems").fetchone()
            auth_cnt = conn.execute("SELECT COUNT(*) FROM author_frontier_contributions").fetchone()
            if cnt is None or int(cnt[0]) != 1900 or auth_cnt is None or int(auth_cnt[0]) < 1:
                return False
            return True
        finally:
            conn.close()
    except sqlite3.Error:
        return False


def ensure_sqlite_db(db_path: Path = DEFAULT_DB) -> Path:
    """Auto-build the local SQLite FTS5 index deterministically if absent or stale after an upgrade."""
    if _db_is_fresh(db_path):
        return db_path
    if db_path.exists():
        db_path.unlink()
    src_dir = str(ROOT / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    import pandas as pd  # noqa: PLC0415
    from v2_loader import load_v2_master  # noqa: PLC0415

    db_path.parent.mkdir(parents=True, exist_ok=True)
    data = load_v2_master()
    df = data["df"]
    conn = sqlite3.connect(str(db_path))
    try:
        df.to_sql("problems", conn, index=False, if_exists="replace")
        pd.DataFrame(
            [{"source": u, "target": v} for u, v in sorted(data["G"].edges())]
        ).to_sql("edges", conn, index=False, if_exists="replace")
        data["df_ai_audit"].to_sql("ai_audit_nov2026", conn, index=False, if_exists="replace")
        data["df_registries"].to_sql("registries_nov2026", conn, index=False, if_exists="replace")
        data["df_author_contributions"].to_sql("author_frontier_contributions", conn, index=False, if_exists="replace")
        data["df_benchmarks"].to_sql("benchmarks", conn, index=False, if_exists="replace")
        data["df_contrasts"].to_sql("contrasts", conn, index=False, if_exists="replace")
        data["df_pillars"].to_sql("pillar_summary", conn, index=False, if_exists="replace")
        data["df_superdomains"].to_sql("superdomain_summary", conn, index=False, if_exists="replace")
        data["df_substrates"].to_sql("substrate_summary", conn, index=False, if_exists="replace")
        pd.DataFrame(
            [{"key": k, "value": json.dumps(v) if isinstance(v, (dict, list)) else str(v)}
             for k, v in data["summary_stats"].items()]
        ).to_sql("metadata", conn, index=False, if_exists="replace")
        cur = conn.cursor()
        cur.execute("CREATE UNIQUE INDEX idx_problems_id ON problems(id)")
        cur.execute("CREATE INDEX idx_problems_pillar ON problems(macro_pillar)")
        cur.execute("CREATE INDEX idx_problems_superdomain ON problems(superdomain)")
        cur.execute("CREATE INDEX idx_problems_status ON problems(status_2026)")
        cur.execute("CREATE INDEX idx_problems_vflag ON problems(verification_flag)")
        cur.execute("CREATE INDEX idx_problems_css ON problems(css_score DESC)")
        cur.execute("CREATE INDEX idx_edges_src ON edges(source)")
        cur.execute("CREATE INDEX idx_edges_tgt ON edges(target)")
        cur.execute("""
            CREATE VIRTUAL TABLE problems_fts USING fts5(
                id UNINDEXED, name, macro_pillar, superdomain, subdomain, originator,
                core_question, formal_expression, primary_bottleneck, competing_approaches,
                closest_progress_2026, ai_verification_nov2026, affected_industries,
                registry_source, contrast_axis, tokenize='porter unicode61'
            )
        """)
        cur.execute("""
            INSERT INTO problems_fts(
                id, name, macro_pillar, superdomain, subdomain, originator,
                core_question, formal_expression, primary_bottleneck, competing_approaches,
                closest_progress_2026, ai_verification_nov2026, affected_industries,
                registry_source, contrast_axis
            )
            SELECT
                id, name, macro_pillar, superdomain, subdomain, originator,
                core_question, formal_expression, primary_bottleneck, competing_approaches,
                closest_progress_2026, ai_verification_nov2026, affected_industries,
                registry_source, contrast_axis
            FROM problems
        """)
        conn.commit()
    finally:
        conn.close()
    return db_path

STOPWORDS = {
    "the", "of", "and", "or", "in", "on", "to", "for", "with", "by", "at",
    "from", "as", "is", "are", "be", "an", "that", "this", "it", "vs", "versus",
}

BM25_WEIGHTS = "0.0, 12.0, 2.0, 3.0, 4.0, 2.0, 3.5, 3.0, 1.5, 2.0, 1.5, 2.0, 1.5, 2.5, 1.5"


def tokenize_query(raw: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z0-9_]+", raw)
    if not tokens:
        return []
    filtered = [t.lower() for t in tokens if t.lower() not in STOPWORDS]
    dedup = list(dict.fromkeys(filtered if filtered else [t.lower() for t in tokens]))
    return dedup


def _stem_prefix(tok: str) -> str:
    return tok[:6] if len(tok) > 6 else tok


def rerank_hybrid(candidates: List[Dict[str, Any]], query_tokens: List[str]) -> List[Dict[str, Any]]:
    """Hybrid Lexical + Title-Bigram + Knowledge-Graph PageRank/Degree Authority re-ranker (H-003).
    Combines FTS5 BM25 relevance, unique query-token coverage in title & body, contiguous
    query bigram hits in the title, and NetworkX graph authority (degree + PageRank).
    """
    if not candidates or not query_tokens:
        return candidates
    q_stems = [_stem_prefix(t) for t in query_tokens]
    q_bigrams = [f"{query_tokens[i]} {query_tokens[i+1]}" for i in range(len(query_tokens) - 1)]
    raw_bm25 = [-float(c.get("bm25_score", 0.0)) for c in candidates]
    max_b = max(raw_bm25) if raw_bm25 else 1.0
    min_b = min(raw_bm25) if raw_bm25 else 0.0
    span_b = max(1e-6, max_b - min_b)

    max_pr = max((float(c.get("pagerank", 0.0)) for c in candidates), default=1e-6)
    max_pr = max(max_pr, 1e-6)

    scored = []
    for c, rb in zip(candidates, raw_bm25):
        bm25_norm = (rb - min_b) / span_b
        name_low = re.sub(r"[^a-z0-9]+", " ", c.get("name", "").lower()).strip()
        title_txt = (c.get("name", "") + " " + c.get("subdomain", "")).lower()
        body_txt = (
            title_txt + " " + c.get("core_question", "") + " "
            + c.get("formal_expression", "") + " " + c.get("competing_approaches", "")
        ).lower()
        title_hits = sum(1 for st in q_stems if st in title_txt)
        body_hits = sum(1 for st in q_stems if st in body_txt)
        title_cov = title_hits / len(q_stems)
        body_cov = body_hits / len(q_stems)
        bigram_cov = (
            sum(1 for bg in q_bigrams if bg in name_low) / len(q_bigrams)
            if q_bigrams else title_cov
        )
        deg_auth = min(1.0, math.log1p(max(0, int(c.get("graph_degree", 0)))) / math.log1p(45.0))
        pr_auth = min(1.0, float(c.get("pagerank", 0.0)) / max_pr)
        graph_auth = 0.50 * deg_auth + 0.50 * pr_auth
        css_prior = min(1.0, float(c.get("css_score", 50.0)) / 100.0)

        hybrid = (
            0.22 * bm25_norm
            + 0.24 * title_cov
            + 0.18 * bigram_cov
            + 0.10 * body_cov
            + 0.23 * graph_auth
            + 0.03 * css_prior
        )
        c["hybrid_score"] = round(hybrid, 4)
        scored.append((hybrid, c))

    scored.sort(key=lambda x: (-x[0], -float(x[1].get("css_score", 0.0)), x[1]["id"]))
    return [c for _, c in scored]


def build_fts_stages(raw: str) -> List[Tuple[str, float]]:
    """Build staged precision-first FTS5 queries:
      1. Exact phrase (when >=2 tokens) with strong tie-break bonus
      2. Strict AND across all meaningful tokens (high precision)
      3. Relaxed OR backfill across all meaningful tokens (high recall)
    """
    tokens = tokenize_query(raw)
    if not tokens:
        return []
    quoted = [f'"{t}"' for t in tokens]
    stages: List[Tuple[str, float]] = []
    if len(tokens) >= 2:
        phrase = '"' + " ".join(tokens) + '"'
        stages.append((phrase, -1000.0))
        stages.append((" AND ".join(quoted), -100.0))
    stages.append((" OR ".join(quoted), 0.0))
    return stages


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
        if db_path == DEFAULT_DB:
            ensure_sqlite_db(db_path)
        else:
            raise FileNotFoundError(f"SQLite FTS5 database not found at {db_path}. Run `python src/v2_export_all.py`.")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        results: List[Dict[str, Any]] = []

        if problem_id:
            rows = cur.execute("SELECT *, 0.0 AS bm25_score FROM problems WHERE id = ?", (problem_id.upper(),)).fetchall()
            results = [dict(r) for r in rows]
        elif query:
            # Direct Problem ID lookup shortcut if query looks like an exact ID
            q_trim = query.strip().upper()
            if re.fullmatch(r"[A-Z0-9]+-[0-9]{3,4}", q_trim):
                exact_rows = cur.execute("SELECT *, -2000.0 AS bm25_score FROM problems WHERE id = ?", (q_trim,)).fetchall()
                results.extend(dict(r) for r in exact_rows)

            seen_ids = {r["id"] for r in results}
            q_tokens = tokenize_query(query)
            stages = build_fts_stages(query)
            if not stages and not results:
                return {"query": query, "count": 0, "results": []}

            pool_limit = max(40, top * 5)
            pool: List[Dict[str, Any]] = []
            for fts_q, _stage_bonus in stages:
                if len(pool) >= pool_limit:
                    break
                sql = f"""
                    SELECT p.*, bm25(problems_fts, {BM25_WEIGHTS}) AS bm25_score
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
                params.append(pool_limit)
                for row in cur.execute(sql, params).fetchall():
                    rid = row["id"]
                    if rid not in seen_ids:
                        seen_ids.add(rid)
                        pool.append(dict(row))
                        if len(pool) >= pool_limit:
                            break

            reranked = rerank_hybrid(pool, q_tokens)
            results.extend(reranked[: max(0, top - len(results))])
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
            results = [dict(r) for r in cur.execute(sql, params).fetchall()]

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


def compare_two_problems(id_a: str, id_b: str, db_path: Path = DEFAULT_DB) -> Dict[str, Any]:
    """Compare any two problems side-by-side with antisymmetric deltas and shared neighbors."""
    if not db_path.exists() and db_path == DEFAULT_DB:
        ensure_sqlite_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        ra = cur.execute("SELECT * FROM problems WHERE id = ?", (id_a.upper(),)).fetchone()
        rb = cur.execute("SELECT * FROM problems WHERE id = ?", (id_b.upper(),)).fetchone()
        if not ra or not rb:
            missing = [x for x, r in [(id_a, ra), (id_b, rb)] if not r]
            raise ValueError(f"Unknown problem ID(s): {', '.join(missing)}")
        pa, pb = dict(ra), dict(rb)
        nbs = get_neighbors(conn, [pa["id"], pb["id"]], hops=1)
        set_a = {n["id"] for n in nbs.get(pa["id"], [])}
        set_b = {n["id"] for n in nbs.get(pb["id"], [])}
        direct_edge = pb["id"] in set_a or pa["id"] in set_b
        shared = sorted(set_a & set_b)
        return {
            "problem_a": pa,
            "problem_b": pb,
            "deltas_a_minus_b": {
                "difficulty_score": pa["difficulty_score"] - pb["difficulty_score"],
                "tractability_2050": pa["tractability_2050"] - pb["tractability_2050"],
                "civilizational_impact": pa["civilizational_impact"] - pb["civilizational_impact"],
                "interdisciplinarity_index": pa["interdisciplinarity_index"] - pb["interdisciplinarity_index"],
                "css_score": round(pa["css_score"] - pb["css_score"], 2),
                "titan_index": round(pa["titan_index"] - pb["titan_index"], 2),
                "graph_degree": pa["graph_degree"] - pb["graph_degree"],
                "age_years_2026": pa["age_years_2026"] - pb["age_years_2026"],
            },
            "graph_relation": {
                "direct_edge": direct_edge,
                "same_macro_pillar": pa["macro_pillar"] == pb["macro_pillar"],
                "same_superdomain": pa["superdomain"] == pb["superdomain"],
                "shared_neighbors_count": len(shared),
                "shared_neighbor_ids": shared,
            },
        }
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline BM25 + Knowledge-Graph RAG Query CLI (0thernes Mega-Atlas V2.5.0)")
    parser.add_argument("query", nargs="?", default=None, help="Free-text search query (staged FTS5 BM25)")
    parser.add_argument("--problem", dest="problem_id", default=None, help="Exact Problem ID (e.g., NT-001, CS-001, GR-001)")
    parser.add_argument("--compare", nargs=2, metavar=("ID_A", "ID_B"), default=None, help="Compare two Problem IDs side-by-side")
    parser.add_argument("--pillar", default=None, help="Filter by exact Macro-Pillar name")
    parser.add_argument("--superdomain", default=None, help="Filter by exact Superdomain name")
    parser.add_argument("--flag", default=None, help="Filter by verification_flag")
    parser.add_argument("--top", type=int, default=8, help="Maximum hits to return (default: 8)")
    parser.add_argument("--hops", type=int, default=0, help="Knowledge-graph neighbor hops to expand (0 or 1)")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    if args.compare:
        comp = compare_two_problems(args.compare[0], args.compare[1])
        if args.as_json:
            print(json.dumps(comp, indent=2, ensure_ascii=False))
            return
        pa, pb, d, rel = comp["problem_a"], comp["problem_b"], comp["deltas_a_minus_b"], comp["graph_relation"]
        print(f"=== Side-by-Side Comparison: [{pa['id']}] {pa['name']}  vs.  [{pb['id']}] {pb['name']} ===")
        print(f"  ΔCSS={d['css_score']:+.2f} | ΔTitan={d['titan_index']:+.2f} | ΔDiff={d['difficulty_score']:+d} | ΔTract={d['tractability_2050']:+d} | ΔImpact={d['civilizational_impact']:+d} | ΔDeg={d['graph_degree']:+d}")
        print(f"  Direct Edge: {rel['direct_edge']} | Same Pillar: {rel['same_macro_pillar']} | Shared Neighbors ({rel['shared_neighbors_count']}): {', '.join(rel['shared_neighbor_ids'][:10])}")
        return

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
