#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Model Context Protocol (MCP) Stdio JSON-RPC 2.0 Server for the
Unsolved Problems Mega-Atlas (V2.10.0, Alexander Stephen Donahue).

Zero external MCP SDK dependency — supports BOTH newline-delimited JSON-RPC stdio
and `Content-Length:` framed LSP/MCP stdio over `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite`
(auto-built deterministically on first run or version upgrade).

Exposes 13 grounded scientific research tools to Claude Code, Antigravity,
Cursor, Gemini CLI, and autonomous research agents:
  1. search_problems                  — Hybrid BM25 + bigram + PageRank RAG + 1-hop neighbors
  2. get_problem                      — Full problem dossier by exact Problem ID
  3. compare_problems                 — Side-by-side comparison, antisymmetric deltas & shared neighbors
  4. list_nov2026_ai_claims           — All 12 unretired Fall/Nov 2026 AI proof claims + 6-item audit ledger
  5. get_top_ranked                   — Top problems by css_score, titan_index, pagerank, or leverage
  6. get_pillar_summary               — 8-Macro-Pillar quantitative comparison scorecard
  7. get_substrate_layer_summary      — 8-Substrate × 7-Abstraction-Layer (`L0..L6`) comparative matrix
  8. get_margin_and_gradient_extremes — Extremes of Hardness-Tractability gradient, CSS-Titan margin & trans-pillar bridges
  9. list_author_frontier_contributions — 20 companion archive rows covering all 27 other audited archive entries in RESULTS.md (parent problems remain OPEN)
 10. get_atlas_provenance             — ORCID, Lean 4.35.0 audit status and scope, epistemic boundaries & Apache-2.0/CC-BY-4.0 license
 11. simulate_rubric_override         — Community rubric sensitivity diff (Spearman rho, Kendall tau, Top-25 Jaccard, movers & Quadrant shifts)
 12. get_live_registry_tracker        — Daily-synced 16 public open-problem trackers & all 25 Left to Solve mathematical fronts (`lefttosolve.com/programs`)
 13. query_lefttosolve_programs       — Offline explorer over the full daily-mirrored 59,396-problem Left to Solve 25-program JSONL catalog (`data/external/lefttosolve/`) & candidate Atlas crosswalk
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "scripts"))

from query import DEFAULT_DB, compare_two_problems, ensure_sqlite_db, search_atlas  # noqa: E402
from rubric_override_diff import DEFAULT_CSS_WEIGHTS, evaluate_rubric_override  # noqa: E402

ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.10.0"
MAX_FRAME_BYTES = 1_048_576  # 1 MiB ceiling on both Content-Length and NDJSON frames
MAX_QUERY_CHARS = 4096


def _parse_clamped_int(val: Any, default: int, lo: int, hi: int, name: str) -> int:
    if val is None:
        return default
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError(f"Argument '{name}' must be an integer (not bool/str)")
    return max(lo, min(hi, val))


def _parse_opt_str(val: Any, name: str, max_len: int = 256) -> str | None:
    if val is None:
        return None
    if not isinstance(val, str):
        raise ValueError(f"Argument '{name}' must be a string")
    if len(val) > max_len:
        raise ValueError(f"Argument '{name}' exceeds {max_len} characters")
    return val
SERVER_INFO = {
    "name": "unsolved-problems-mega-atlas",
    "version": ATLAS_VERSION,
}
PROTOCOL_VERSION = "2024-11-05"


def _count_lean_axioms_audited() -> int:
    audit_path = ROOT / "lean" / "MegaAtlasProofs" / "VerifyAxioms.lean"
    if not audit_path.exists():
        return 0
    return sum(
        1 for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("#print axioms ")
    )


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "search_problems",
        "description": "Search all 2,000 unsolved, open, and hard problems using Hybrid BM25 + Title-Bigram + Knowledge-Graph PageRank Authority ranking, with optional pillar/superdomain/verification_flag filters and 1-hop graph expansion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Free-text search query"},
                "pillar": {"type": "string", "description": "Optional exact Macro-Pillar filter"},
                "superdomain": {"type": "string", "description": "Optional exact Superdomain filter"},
                "flag": {"type": "string", "description": "Optional verification_flag filter"},
                "top": {"type": "integer", "minimum": 1, "maximum": 50, "default": 8},
                "hops": {"type": "integer", "minimum": 0, "maximum": 1, "default": 1},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_problem",
        "description": "Retrieve the complete 48-field structured dossier (including substrate_class, abstraction_layer, gradients, margins, formal expression, Nov 25, 2026 audit notes, and 1-hop coupled graph neighbors) for a single Problem ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "problem_id": {"type": "string", "description": "Exact Problem ID (e.g. NT-001)"},
                "hops": {"type": "integer", "minimum": 0, "maximum": 1, "default": 1},
            },
            "required": ["problem_id"],
        },
    },
    {
        "name": "compare_problems",
        "description": "Compare any two cataloged problems side-by-side with Lean-verified antisymmetric metric deltas (CSS, Titan, Difficulty, Tractability, Impact, Degree, Age), direct link check, and shared knowledge-graph neighbors.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id_a": {"type": "string", "description": "First Problem ID"},
                "id_b": {"type": "string", "description": "Second Problem ID"},
            },
            "required": ["id_a", "id_b"],
        },
    },
    {
        "name": "list_nov2026_ai_claims",
        "description": "Return all 12 Fall/November 2026 AI proof-claim targets (explicitly flagged unretired) together with the 6-item November 25, 2026 AI Proof-Claim Verification Audit ledger.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_top_ranked",
        "description": "List top-ranked open problems sorted by 'css_score', 'titan_index', 'pagerank', 'near_term_leverage_score', 'hardness_tractability_gradient', or 'bridge_margin_ratio', optionally filtered by Macro-Pillar or Substrate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": [
                        "css_score", "titan_index", "pagerank", "near_term_leverage_score",
                        "hardness_tractability_gradient", "bridge_margin_ratio",
                    ],
                    "default": "css_score",
                },
                "pillar": {"type": "string", "description": "Optional exact Macro-Pillar filter"},
                "substrate": {"type": "string", "description": "Optional exact substrate_class filter"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 15},
            },
        },
    },
    {
        "name": "get_pillar_summary",
        "description": "Return the 8-Macro-Pillar comparative quantitative scorecard.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_substrate_layer_summary",
        "description": "Return the 8-Substrate comparative scorecard (Mean CSS, Titan, Difficulty, Tractability, Hardness-Tractability Gradient, CSS-Titan Margin, Epistemic Spectrum, Bridge Ratio, Adjacent Pillars) and abstraction-layer breakdown.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_margin_and_gradient_extremes",
        "description": "Inspect boundary/margin phenomena across the atlas: steepest hardness-tractability chasms (D-T), largest CSS-vs-Titan divergences, apex multi-pillar keystones (3+ adjacent pillars), and highest trans-pillar bridge ratios.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "minimum": 1, "maximum": 30, "default": 10},
            },
        },
    },
    {
        "name": "list_author_frontier_contributions",
        "description": "List 20 author-curated companion rows from 0thernes-research-archive covering all 27 other audited archive entries in RESULTS.md (R1-R94, with R85 = this repo) mapped to parent Mega-Atlas IDs. Only section A records answers to open questions from the literature; all entries carry conflict-of-interest, non-peer-reviewed status and parent-still-OPEN flags (0/2,000 atlas problems solved by this work).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_atlas_provenance",
        "description": "Return canonical author/ORCID identity, independent researcher affiliation, Lean 4.35.0 audit status and scope (103 audited theorems; 9 Palomar comparator targets also checked by six kernel checks), dual-license terms (CC-BY-4.0 / Apache-2.0), and dataset summary stats.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "simulate_rubric_override",
        "description": "Simulate alternative CSS weights [w_diff, w_cent, w_age, w_tract] (sum=1.0) and/or per-problem editorial rating overrides (1..10) across all 2,000 problems, returning Spearman rho, Kendall tau, Top-25 Jaccard overlap, Quadrant migrations, and top rank movers (makes Claim C9 quantitatively falsifiable).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "css_weights": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 4,
                    "maxItems": 4,
                    "description": "Optional 4-element weight vector [w_diff, w_cent, w_age, w_tract] summing to 1.0",
                },
                "problem_overrides": {
                    "type": "object",
                    "description": "Optional map of Problem ID -> {difficulty_score?, tractability_2050?, civilizational_impact?, interdisciplinarity_index?} in 1..10",
                },
                "label": {"type": "string", "default": "mcp-rubric-override"},
                "top_movers": {"type": "integer", "minimum": 1, "maximum": 25, "default": 5},
            },
        },
    },
    {
        "name": "get_live_registry_tracker",
        "description": "Return the daily-synced tracker covering all 16 global open-problem registries and all 25 mathematical programs on Left to Solve (https://lefttosolve.com/programs, 59,396 total targets / 1,939 Lean-4 open), with optional program substring and Lean-formalized-only filters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "program_filter": {"type": "string", "description": "Optional case-insensitive substring filter over Left to Solve program names"},
                "formalized_only": {"type": "boolean", "default": False, "description": "If true, return only Lean-4 formalized Left to Solve programs"},
            },
        },
    },
    {
        "name": "query_lefttosolve_programs",
        "description": "Query the full daily-synced offline JSONL metadata mirror of all 25 Left to Solve program lists (59,396 problems in data/external/lefttosolve/): returns program summary with solved_by_kind disaggregation + daily delta, searches mirrored problem metadata by program/query/kind/solved/field/difficulty, or inspects exact-normalised-title candidate matches against the 2,000 Mega-Atlas problems.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["summary", "search", "crosswalk"],
                    "default": "summary",
                    "description": "'summary' for all 25 programs & daily delta, 'search' to filter problems across program JSONL files, 'crosswalk' for candidate Atlas matches.",
                },
                "program": {"type": "string", "description": "Optional program name or slug substring filter (for 'search')"},
                "query": {"type": "string", "description": "Optional case-insensitive title/id substring filter (for 'search' or 'crosswalk')"},
                "kind": {
                    "type": "string",
                    "enum": ["open", "known", "warmup", "unformalized"],
                    "description": "Optional Left to Solve kind filter (for 'search')",
                },
                "solved": {"type": "boolean", "description": "Optional upstream solved flag filter (for 'search')"},
                "field": {"type": "string", "description": "Optional mathematical field substring filter (for 'search')"},
                "min_difficulty": {"type": "integer", "minimum": 0, "maximum": 100, "description": "Optional minimum difficulty score filter (for 'search')"},
                "atlas_id": {"type": "string", "description": "Optional exact Mega-Atlas Problem ID filter (for 'crosswalk', e.g. NT-005)"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
        },
    },
]


def _query_lefttosolve(args: Dict[str, Any]) -> Dict[str, Any]:
    lts_dir = ROOT / "data" / "external" / "lefttosolve"
    lts_root = lts_dir.resolve()
    snap_path = lts_dir / "snapshot.json"
    if not snap_path.exists():
        raise ValueError("Left to Solve mirror not found (run: python scripts/sync_lefttosolve.py --live)")
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    action_raw = args.get("action", "summary")
    if not isinstance(action_raw, str):
        raise ValueError("Argument 'action' must be a string")
    action = action_raw.strip().lower()
    if action not in {"summary", "search", "crosswalk"}:
        raise ValueError(f"Unsupported action '{action}'; expected 'summary', 'search', or 'crosswalk'")

    if action == "summary":
        delta_path = ROOT / "results" / "lefttosolve_delta.json"
        delta = json.loads(delta_path.read_text(encoding="utf-8")) if delta_path.exists() else None
        changes_path = lts_dir / "CHANGES.jsonl"
        recent_changes: List[Dict[str, Any]] = []
        if changes_path.exists():
            lines = [ln for ln in changes_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            recent_changes = [json.loads(ln) for ln in lines[-10:]]
        return {
            "source": snap["source"],
            "retrieved_utc": snap["retrieved_utc"],
            "reported_total": snap["reported_total"],
            "fetched_total": snap["fetched_total"],
            "program_count": len(snap["programs"]),
            "catalog": snap.get("catalog", {}),
            "solved_by_kind": snap.get("solved_by_kind", {}),
            "upstream": snap.get("upstream", {}),
            "crosswalk_matches": snap.get("crosswalk_matches", 0),
            "policy": snap.get("policy", ""),
            "note": "Sidecar daily metadata mirror only; 'solved' (disaggregated in solved_by_kind) and 'Lean-stated' flags are Left to Solve's own and are not re-verified here; never mutates the frozen 2,000-problem Mega-Atlas.",
            "latest_delta": delta,
            "recent_daily_runs": recent_changes,
            "programs": snap["programs"],
        }

    if action == "crosswalk":
        cw_path = lts_dir / "atlas_crosswalk.json"
        cw = json.loads(cw_path.read_text(encoding="utf-8")) if cw_path.exists() else {"matches": []}
        matches = list(cw.get("matches", []))
        atlas_id = args.get("atlas_id")
        if atlas_id is not None:
            if not isinstance(atlas_id, str):
                raise ValueError("Argument 'atlas_id' must be a string")
            if len(atlas_id) > MAX_QUERY_CHARS:
                raise ValueError(f"Argument 'atlas_id' exceeds {MAX_QUERY_CHARS} characters")
            aid_u = atlas_id.strip().upper()
            matches = [m for m in matches if str(m.get("atlas_id", "")).upper() == aid_u]
        q_raw = args.get("query")
        if q_raw is not None:
            if not isinstance(q_raw, str):
                raise ValueError("Argument 'query' must be a string")
            if len(q_raw) > MAX_QUERY_CHARS:
                raise ValueError(f"Argument 'query' exceeds {MAX_QUERY_CHARS} characters")
            q_low = q_raw.strip().lower()
            if q_low:
                matches = [
                    m for m in matches
                    if q_low in str(m.get("atlas_name", "")).lower()
                    or q_low in str(m.get("atlas_id", "")).lower()
                    or any(q_low in str(x.get("title", "")).lower() or q_low in str(x.get("program", "")).lower() for x in m.get("lefttosolve", []))
                ]
        limit = _parse_clamped_int(args.get("limit"), 50, 1, 100, "limit")
        return {
            "retrieved_utc": snap["retrieved_utc"],
            "method": cw.get("method", ""),
            "policy": cw.get("policy", "Advisory only; automatic exact-normalised-title candidates."),
            "external_solved_signals": cw.get("external_solved_signals", []),
            "total_matched": len(matches),
            "returned": min(len(matches), limit),
            "matches": matches[:limit],
        }

    prog_filter = args.get("program")
    if prog_filter is not None:
        if not isinstance(prog_filter, str):
            raise ValueError("Argument 'program' must be a string")
        if len(prog_filter) > MAX_QUERY_CHARS:
            raise ValueError(f"Argument 'program' exceeds {MAX_QUERY_CHARS} characters")
    q_raw = args.get("query")
    if q_raw is not None:
        if not isinstance(q_raw, str):
            raise ValueError("Argument 'query' must be a string")
        if len(q_raw) > MAX_QUERY_CHARS:
            raise ValueError(f"Argument 'query' exceeds {MAX_QUERY_CHARS} characters")
    kind_filter = args.get("kind")
    if kind_filter is not None and kind_filter not in {"open", "known", "warmup", "unformalized"}:
        raise ValueError(f"Unsupported kind '{kind_filter}'")
    solved_filter = args.get("solved")
    if solved_filter is not None and not isinstance(solved_filter, bool):
        raise ValueError("Argument 'solved' must be a boolean")
    field_filter = args.get("field")
    if field_filter is not None:
        if not isinstance(field_filter, str):
            raise ValueError("Argument 'field' must be a string")
        if len(field_filter) > MAX_QUERY_CHARS:
            raise ValueError(f"Argument 'field' exceeds {MAX_QUERY_CHARS} characters")
    min_diff = (
        _parse_clamped_int(args.get("min_difficulty"), 0, 0, 100, "min_difficulty")
        if args.get("min_difficulty") is not None
        else None
    )
    limit = _parse_clamped_int(args.get("limit"), 20, 1, 100, "limit")

    p_low = prog_filter.strip().lower() if prog_filter else ""
    q_low = q_raw.strip().lower() if q_raw else ""
    f_low = field_filter.strip().lower() if field_filter else ""

    selected_programs = [
        p for p in snap["programs"]
        if not p_low or p_low in p["program"].lower() or p_low in p["slug"].lower()
    ]
    results: List[Dict[str, Any]] = []
    total_matches = 0
    for prog in selected_programs:
        pname = prog["program"]
        for rel in prog.get("files", []):
            fpath = (lts_dir / rel).resolve()
            if not fpath.is_relative_to(lts_root) or not fpath.exists():
                continue
            with fpath.open("r", encoding="utf-8") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    if kind_filter is not None and row.get("kind") != kind_filter:
                        continue
                    if solved_filter is not None and bool(row.get("solved")) is not solved_filter:
                        continue
                    if min_diff is not None:
                        diff_val = row.get("difficulty")
                        if not isinstance(diff_val, (int, float)) or diff_val < min_diff:
                            continue
                    if f_low:
                        fields = row.get("fields") or []
                        if not any(f_low in str(fl).lower() for fl in fields):
                            continue
                    if q_low:
                        if q_low not in str(row.get("title", "")).lower() and q_low not in str(row.get("id", "")).lower():
                            continue
                    total_matches += 1
                    if len(results) < limit:
                        item = dict(row)
                        item["program"] = pname
                        results.append(item)
    return {
        "retrieved_utc": snap["retrieved_utc"],
        "programs_searched": len(selected_programs),
        "total_matches": total_matches,
        "returned": len(results),
        "results": results,
    }


def _query_db(sql: str, params: tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
    ensure_sqlite_db(DEFAULT_DB)
    conn = sqlite3.connect(str(DEFAULT_DB))
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def dispatch_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(args, dict):
        raise ValueError("Tool arguments must be a JSON object")
    if name == "search_problems":
        q_raw = args.get("query")
        if q_raw is not None:
            if not isinstance(q_raw, str):
                raise ValueError("Argument 'query' must be a string")
            if len(q_raw) > MAX_QUERY_CHARS:
                raise ValueError(f"Argument 'query' exceeds {MAX_QUERY_CHARS} characters")
        top = _parse_clamped_int(args.get("top"), 8, 1, 50, "top")
        hops = _parse_clamped_int(args.get("hops"), 1, 0, 1, "hops")
        return search_atlas(
            query=q_raw,
            pillar=_parse_opt_str(args.get("pillar"), "pillar"),
            superdomain=_parse_opt_str(args.get("superdomain"), "superdomain"),
            flag=_parse_opt_str(args.get("flag"), "flag"),
            top=top,
            hops=hops,
        )
    if name == "get_problem":
        pid = args.get("problem_id")
        if not pid or not isinstance(pid, str):
            raise ValueError("Missing required string argument: problem_id")
        hops = _parse_clamped_int(args.get("hops"), 1, 0, 1, "hops")
        res = search_atlas(problem_id=pid, hops=hops)
        if not res["results"]:
            raise ValueError(f"Problem ID not found: {pid}")
        return res["results"][0]
    if name == "compare_problems":
        id_a = args.get("id_a")
        id_b = args.get("id_b")
        if not id_a or not isinstance(id_a, str) or not id_b or not isinstance(id_b, str):
            raise ValueError("Missing required string arguments: id_a and id_b")
        return compare_two_problems(id_a, id_b)
    if name == "list_nov2026_ai_claims":
        claims = _query_db(
            "SELECT id, name, macro_pillar, superdomain, status_2026, verification_flag, css_score, titan_index, ai_verification_nov2026 "
            "FROM problems WHERE verification_flag = 'ai-claim-under-audit-nov2026' ORDER BY css_score DESC"
        )
        ledger = _query_db("SELECT * FROM ai_audit_nov2026")
        return {
            "policy": "All 12 Fall/Nov 2026 AI proof claims remain OFFICIALLY UNRETIRED pending independent human-readable proofs, statement-fidelity audit, and peer consensus.",
            "flagged_problems_count": len(claims),
            "flagged_problems": claims,
            "audit_ledger": ledger,
        }
    if name == "get_top_ranked":
        allowed = {
            "css_score", "titan_index", "pagerank", "near_term_leverage_score",
            "hardness_tractability_gradient", "bridge_margin_ratio",
        }
        metric = str(args.get("metric", "css_score"))
        if metric not in allowed:
            raise ValueError(f"Unsupported metric: {metric}")
        limit = _parse_clamped_int(args.get("limit"), 15, 1, 100, "limit")
        where = ["1=1"]
        params: List[Any] = []
        pillar_f = _parse_opt_str(args.get("pillar"), "pillar")
        substrate_f = _parse_opt_str(args.get("substrate"), "substrate")
        if pillar_f:
            where.append("macro_pillar = ?")
            params.append(pillar_f)
        if substrate_f:
            where.append("substrate_class = ?")
            params.append(substrate_f)
        params.append(limit)
        rows = _query_db(
            f"SELECT id, name, macro_pillar, superdomain, substrate_class, abstraction_layer, year_formulated, "
            f"css_score, titan_index, hardness_tractability_gradient, bridge_margin_ratio, adjacent_pillars_count, "
            f"margin_role, status_2026, verification_flag "
            f"FROM problems WHERE {' AND '.join(where)} ORDER BY {metric} DESC, id ASC LIMIT ?",
            tuple(params),
        )
        return {"metric": metric, "count": len(rows), "results": rows}
    if name == "get_pillar_summary":
        return {"pillars": _query_db("SELECT * FROM pillar_summary")}
    if name == "get_substrate_layer_summary":
        substrates = _query_db("SELECT * FROM substrate_summary")
        layers = _query_db(
            "SELECT abstraction_layer, COUNT(*) AS problem_count, "
            "ROUND(AVG(css_score), 2) AS mean_css, ROUND(AVG(titan_index), 2) AS mean_titan, "
            "ROUND(AVG(hardness_tractability_gradient), 2) AS mean_gradient_d_minus_t, "
            "ROUND(AVG(epistemic_spectrum_score), 1) AS mean_spectrum "
            "FROM problems GROUP BY abstraction_layer ORDER BY abstraction_layer ASC"
        )
        return {"substrates": substrates, "abstraction_layers": layers}
    if name == "get_margin_and_gradient_extremes":
        lim = _parse_clamped_int(args.get("limit"), 10, 1, 30, "limit")
        steepest = _query_db(
            "SELECT id, name, macro_pillar, substrate_class, difficulty_score, tractability_2050, hardness_tractability_gradient, css_score "
            "FROM problems ORDER BY hardness_tractability_gradient DESC, css_score DESC LIMIT ?", (lim,)
        )
        most_tractable_margin = _query_db(
            "SELECT id, name, macro_pillar, substrate_class, difficulty_score, tractability_2050, hardness_tractability_gradient, near_term_leverage_score "
            "FROM problems ORDER BY hardness_tractability_gradient ASC, near_term_leverage_score DESC LIMIT ?", (lim,)
        )
        css_gt_titan = _query_db(
            "SELECT id, name, macro_pillar, year_formulated, css_score, titan_index, css_titan_margin "
            "FROM problems ORDER BY css_titan_margin DESC LIMIT ?", (lim,)
        )
        apex_keystones = _query_db(
            "SELECT id, name, macro_pillar, substrate_class, graph_degree, cross_pillar_links, adjacent_pillars_count, bridge_margin_ratio, margin_role "
            "FROM problems ORDER BY adjacent_pillars_count DESC, cross_pillar_links DESC LIMIT ?", (lim,)
        )
        return {
            "steepest_hardness_tractability_chasms": steepest,
            "highest_tractability_over_hardness_margins": most_tractable_margin,
            "largest_positive_css_over_titan_margins": css_gt_titan,
            "apex_multi_pillar_keystones": apex_keystones,
        }
    if name == "list_author_frontier_contributions":
        contribs = _query_db("SELECT * FROM author_frontier_contributions")
        return {
            "conflict_of_interest_disclosure": "Self-authored independent preprints by Alexander Stephen Donahue (ORCID 0009-0006-8168-9648); none have undergone external journal peer review.",
            "results_ledger": "https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md",
            "results_ledger_note": "RESULTS.md is the authoritative list of results and their kinds. Only its section A records answers to open questions stated by other authors (R1 for 0TH-2026-006; R44 and R45 for 0TH-2026-009).",
            "overarching_atlas_problems_retired": 0,
            "scoped_preprints_count": len(contribs),
            "contributions": contribs,
        }
    if name == "get_atlas_provenance":
        meta_rows = _query_db("SELECT key, value FROM metadata")
        meta = {r["key"]: r["value"] for r in meta_rows}
        lean_thms = _count_lean_axioms_audited()
        return {
            "title": f"Unsolved Problems Mega-Atlas (V{ATLAS_VERSION})",
            "author": "Alexander Stephen Donahue",
            "orcid": "0009-0006-8168-9648",
            "orcid_url": "https://orcid.org/0009-0006-8168-9648",
            "affiliation": "Independent Researcher, Spokane, WA, USA",
            "repository": "https://github.com/0thernes/unsolved-problems-mega-atlas",
            "web_atlas": "https://0thernes.github.io/unsolved-problems-mega-atlas/",
            "master_archive_id": "0TH-BUILD-007",
            "dual_license": {"data": "CC-BY-4.0", "code": "Apache-2.0"},
            "lean_verification": {
                "toolchain": "leanprover/lean4:v4.35.0",
                "framework": "Pure Lean 4.35.0 (zero Mathlib, zero sorry in lean/, zero native_decide). Kernel-checked by Lean (lake build, leanchecker --fresh, leanchecker-paranoid); the 9 Palomar comparator targets were also accepted by six kernel checks (five distinct implementations) via scripts/verify_lean_six_kernels.sh in Ubuntu CI.",
                "audited_theorems": lean_thms,
                "kernels": ["lean", "leanchecker-paranoid", "lean4lean", "nanoda_bin", "con-leche", "con-ron"],
                "axiom_allowlist": ["propext", "Quot.sound"],
                "axiom_scope": "Each of the 103 audited theorems depends on at most propext and Quot.sound (#print axioms). The whole-environment lake check --paranoid step also reports Classical.choice, which the per-theorem audit does not cover.",
                "boundary": (
                    "Integer and list invariants of the atlas software model only: scoring bounds, monotonicity of CSS, Titan and leverage, "
                    "quadrant and era maps, taxonomy list sizes, a generic list-multigraph handshaking lemma, a dedup bound, the AutoResearch keep/discard rule, "
                    "gradient/margin bounds, NonVacuity witnesses and AdversarialTests refutations. "
                    f"No Lean statement refers to the {int(meta.get('total_problems', 2000)):,}-row data, its {int(meta.get('total_graph_edges', 6111)):,}-edge graph or biconnectivity (checked in Python). "
                    f"Several counted theorems are literal arithmetic identities or restate a hypothesis. Does NOT prove any of the {int(meta.get('total_problems', 2000)):,} open problems."
                ),
            },
            "ai_disclosure": "Curated by independent researcher Alexander Stephen Donahue with disclosed AI assistance; quantitative rubric scores are falsifiable editorial estimates, not peer-reviewed measurements.",
            "summary_stats": meta,
        }
    if name == "simulate_rubric_override":
        raw_w = args.get("css_weights")
        if raw_w is None:
            weights = DEFAULT_CSS_WEIGHTS
        else:
            if not isinstance(raw_w, list) or len(raw_w) != 4 or any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in raw_w):
                raise ValueError("Argument 'css_weights' must be a 4-element list of numbers summing to 1.0")
            weights = (float(raw_w[0]), float(raw_w[1]), float(raw_w[2]), float(raw_w[3]))
        overrides = args.get("problem_overrides")
        if overrides is not None and not isinstance(overrides, dict):
            raise ValueError("Argument 'problem_overrides' must be a JSON object")
        label = str(args.get("label", "mcp-rubric-override"))[:120]
        top_movers = _parse_clamped_int(args.get("top_movers"), 5, 1, 25, "top_movers")
        return evaluate_rubric_override(
            css_weights=weights,
            problem_overrides=overrides,
            label=label,
            top_movers=top_movers,
        )
    if name == "get_live_registry_tracker":
        prog_filter = _parse_opt_str(args.get("program_filter"), "program_filter")
        form_only = args.get("formalized_only", False)
        if not isinstance(form_only, bool):
            raise ValueError("Argument 'formalized_only' must be a boolean")
        daily_path = ROOT / "results" / "daily_registries.json"
        if daily_path.exists():
            payload = json.loads(daily_path.read_text(encoding="utf-8"))
            progs = list(payload.get("lefttosolve_programs", []))
            regs = list(payload.get("registries", []))
            checked_utc = payload.get("checked_utc")
            deltas = payload.get("daily_deltas", [])
            source_mode = payload.get("mode", "live")
        else:
            db_progs = _query_db("SELECT * FROM lefttosolve_programs")
            progs = [
                {
                    "program": r["Program"],
                    "formalized_in_lean": r["Formalized_In_Lean"] == "Yes",
                    "targets": int(r["Targets"]),
                    "open": int(r["Open"]),
                    "solved_here": int(r["Solved_Here"]),
                    "live_agents": 0,
                    "url": r["URL"],
                }
                for r in db_progs
            ]
            regs = _query_db("SELECT * FROM registries_nov2026")
            checked_utc = "baseline-snapshot"
            deltas = ["Loaded committed baseline snapshot (run scripts/sync_external_registries.py --live --write-daily for live counts)."]
            source_mode = "sqlite_baseline"
        if prog_filter:
            pf = prog_filter.lower()
            progs = [p for p in progs if pf in str(p.get("program", "")).lower()]
        if form_only:
            progs = [p for p in progs if p.get("formalized_in_lean")]
        return {
            "source_url": "https://lefttosolve.com/programs",
            "update_cadence": "Daily at 06:00 UTC via .github/workflows/daily-registry-sync.yml",
            "policy": "Advisory daily telemetry ONLY — zero automatic problem retirement.",
            "checked_utc": checked_utc,
            "mode": source_mode,
            "daily_deltas": deltas,
            "registries_polled_count": len(regs),
            "lefttosolve_programs_matched": len(progs),
            "lefttosolve_targets_sum": sum(int(p.get("targets", 0)) for p in progs),
            "lefttosolve_open_sum": sum(int(p.get("open", 0)) for p in progs),
            "lefttosolve_programs": progs,
            "registries": regs,
        }
    if name == "query_lefttosolve_programs":
        return _query_lefttosolve(args)
    raise ValueError(f"Unknown tool: {name}")


def handle_request(req: Dict[str, Any]) -> Dict[str, Any] | None:
    req_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params") or {}

    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        tname = params.get("name", "")
        targs = params.get("arguments") or {}
        try:
            payload = dispatch_tool(tname, targs)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}],
                    "isError": False,
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error calling {tname}: {exc}"}],
                    "isError": True,
                },
            }
    if req_id is None:
        return None
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def _emit(resp: Dict[str, Any], framed: bool) -> None:
    body = json.dumps(resp, ensure_ascii=False).encode("utf-8")
    if framed:
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        sys.stdout.buffer.write(header + body)
        sys.stdout.buffer.flush()
    else:
        sys.stdout.buffer.write(body + b"\n")
        sys.stdout.buffer.flush()


def serve_stdio() -> None:
    """Serve BOTH newline-delimited JSON-RPC 2.0 and `Content-Length:` framed MCP stdio."""
    buf = sys.stdin.buffer
    while True:
        line = buf.readline(MAX_FRAME_BYTES + 1)
        if not line:
            break
        if len(line) > MAX_FRAME_BYTES and not line.endswith(b"\n"):
            # Drain remainder of oversized line cleanly and emit JSON-RPC parse error
            while True:
                chunk = buf.readline(MAX_FRAME_BYTES)
                if not chunk or chunk.endswith(b"\n"):
                    break
            _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Line exceeds {MAX_FRAME_BYTES} byte cap"}}, False)
            continue
        stripped = line.strip()
        if not stripped:
            continue
        framed = False
        if stripped.lower().startswith(b"content-length:"):
            framed = True
            try:
                length = int(stripped.split(b":", 1)[1].strip())
            except ValueError as exc:
                _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Invalid Content-Length: {exc}"}}, framed)
                continue
            while True:
                h = buf.readline(MAX_FRAME_BYTES)
                if not h or h in (b"\r\n", b"\n"):
                    break
            if length <= 0 or length > MAX_FRAME_BYTES:
                _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Content-Length out of bounds (1..{MAX_FRAME_BYTES}): {length}"}}, framed)
                continue
            raw_body = buf.read(length)
            if len(raw_body) < length:
                _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Truncated Content-Length frame ({len(raw_body)}/{length} bytes)"}}, framed)
                break
        else:
            raw_body = stripped
        try:
            req = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}}, framed)
            continue
        if not isinstance(req, dict):
            _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request: JSON-RPC payload must be a JSON object"}}, framed)
            continue
        resp = handle_request(req)
        if resp is not None:
            _emit(resp, framed)


if __name__ == "__main__":
    serve_stdio()
