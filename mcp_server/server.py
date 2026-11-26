#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Model Context Protocol (MCP) Stdio JSON-RPC 2.0 Server for the
Unsolved Problems Mega-Atlas (V2.7.0, Alexander Stephen Donahue).

Zero external MCP SDK dependency — supports BOTH newline-delimited JSON-RPC stdio
and `Content-Length:` framed LSP/MCP stdio over `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite`
(auto-built deterministically on first run or version upgrade).

Exposes 10 grounded scientific research tools to Claude Code, Antigravity,
Cursor, Gemini CLI, and autonomous research agents:
  1. search_problems                  — Hybrid BM25 + bigram + PageRank RAG + 1-hop neighbors
  2. get_problem                      — Full problem dossier by exact Problem ID
  3. compare_problems                 — Side-by-side comparison, antisymmetric deltas & shared neighbors
  4. list_nov2026_ai_claims           — All 12 unretired Fall/Nov 2026 AI proof claims + 6-item audit ledger
  5. get_top_ranked                   — Top problems by css_score, titan_index, pagerank, or leverage
  6. get_pillar_summary               — 8-Macro-Pillar quantitative comparison scorecard
  7. get_substrate_layer_summary      — 8-Substrate × 7-Abstraction-Layer (`L0..L6`) comparative matrix
  8. get_margin_and_gradient_extremes — Extremes of Hardness-Tractability gradient, CSS-Titan margin & trans-pillar bridges
  9. list_author_frontier_contributions — 16 companion archive entries (0thernes-research-archive; explicitly separate from still-OPEN parent problems)
 10. get_atlas_provenance             — ORCID, 6-kernel Pure Lean 4.35.0 audit status, epistemic boundaries & Apache-2.0/CC-BY-4.0 license
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "rag"))

from query import DEFAULT_DB, compare_two_problems, ensure_sqlite_db, search_atlas  # noqa: E402

ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.7.0"
MAX_FRAME_BYTES = 1_048_576  # 1 MiB ceiling on Content-Length JSON-RPC frames
MAX_QUERY_CHARS = 4096


def _parse_clamped_int(val: Any, default: int, lo: int, hi: int, name: str) -> int:
    if val is None:
        return default
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError(f"Argument '{name}' must be an integer (not bool/str)")
    return max(lo, min(hi, val))
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
        "description": "Search all 1,900 unsolved, open, and hard problems using Hybrid BM25 + Title-Bigram + Knowledge-Graph PageRank Authority ranking, with optional pillar/superdomain/verification_flag filters and 1-hop graph expansion.",
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
        "description": "List the 16 author-curated Lean-verified companion archive entries (0thernes-research-archive, 76 public repos audited) mapped to parent Mega-Atlas IDs, with explicit conflict-of-interest, non-peer-reviewed status, and parent-still-OPEN flags (0/1,900 overarching parents retired).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_atlas_provenance",
        "description": "Return canonical author/ORCID identity, independent researcher affiliation, 6-kernel Pure Lean 4.35.0 Palomar formal audit status, dual-license terms (CC-BY-4.0 / Apache-2.0), and dataset summary stats.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


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
            pillar=args.get("pillar"),
            superdomain=args.get("superdomain"),
            flag=args.get("flag"),
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
        if args.get("pillar"):
            where.append("macro_pillar = ?")
            params.append(args["pillar"])
        if args.get("substrate"):
            where.append("substrate_class = ?")
            params.append(args["substrate"])
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
                "framework": "Pure Lean 4.35.0 (zero Mathlib, zero sorry in lean/, zero native_decide, 6 independent proof kernels via scripts/verify_lean_six_kernels.sh)",
                "audited_theorems": lean_thms,
                "kernels": ["lean", "leanchecker-paranoid", "lean4lean", "nanoda_bin", "con-leche", "con-ron"],
                "axiom_allowlist": ["propext", "Quot.sound"],
                "boundary": "Certifies exact scoring, quadrant, era, taxonomy, finite graph handshaking, AutoResearch keep/discard ratchet, substrate/layer/gradient/margin invariants, concrete NonVacuity witnesses, and constructive AdversarialTests refutations ONLY; does NOT prove any of the 1,900 open problems.",
            },
            "ai_disclosure": "Curated by independent researcher Alexander Stephen Donahue with disclosed AI assistance; quantitative rubric scores are falsifiable editorial estimates, not peer-reviewed measurements.",
            "summary_stats": meta,
        }
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
        line = buf.readline()
        if not line:
            break
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
                h = buf.readline()
                if not h or h in (b"\r\n", b"\n"):
                    break
            if length <= 0 or length > MAX_FRAME_BYTES:
                _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Content-Length out of bounds (1..{MAX_FRAME_BYTES}): {length}"}}, framed)
                continue
            raw_body = buf.read(length)
        else:
            raw_body = stripped
        try:
            req = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            _emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}}, framed)
            continue
        resp = handle_request(req)
        if resp is not None:
            _emit(resp, framed)


if __name__ == "__main__":
    serve_stdio()
