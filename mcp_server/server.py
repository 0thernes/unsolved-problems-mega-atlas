#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Stdio JSON-RPC 2.0 Server for the
Unsolved Problems Mega-Atlas (V2.2.0, 0thernes LLC).

Zero external MCP SDK dependency — runs cleanly on Python 3.11+ stdlib over
`outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` (SQLite 3 + FTS5 + NetworkX edges).

Exposes 7 grounded scientific research tools to Claude Code, Antigravity,
Cursor, Gemini CLI, and autonomous research agents:
  1. search_problems        — Hybrid BM25 + graph-authority RAG + 1-hop neighbors
  2. get_problem            — Full problem dossier by exact Problem ID
  3. compare_problems       — Side-by-side comparison, antisymmetric deltas & shared neighbors
  4. list_nov2026_ai_claims — All 12 unretired Fall/Nov 2026 AI proof claims + 6-item audit ledger
  5. get_top_ranked         — Top problems by css_score, titan_index, pagerank, or leverage
  6. get_pillar_summary     — 8-Macro-Pillar quantitative comparison scorecard
  7. get_atlas_provenance   — ORCID, 58 Pure Lean 4.35.0 theorems, epistemic boundaries & license

Run:
    python mcp_server/server.py
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "rag"))

from query import DEFAULT_DB, compare_two_problems, search_atlas  # noqa: E402

SERVER_INFO = {
    "name": "unsolved-problems-mega-atlas",
    "version": "2.2.0",
}
PROTOCOL_VERSION = "2024-11-05"

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "search_problems",
        "description": "Search all 1,855 unsolved, open, and hard problems using Hybrid BM25 + Knowledge-Graph Authority ranking, with optional pillar/superdomain/verification_flag filters and 1-hop graph expansion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Free-text search query (e.g. 'turbulence climate sensitivity')"},
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
        "description": "Retrieve the complete structured dossier, formal expression, Nov 2026 audit notes, scores, and 1-hop coupled graph neighbors for a single Problem ID (e.g. 'NT-001', 'CS-001', 'GR-001').",
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
                "id_a": {"type": "string", "description": "First Problem ID (e.g. NT-001)"},
                "id_b": {"type": "string", "description": "Second Problem ID (e.g. CS-001)"},
            },
            "required": ["id_a", "id_b"],
        },
    },
    {
        "name": "list_nov2026_ai_claims",
        "description": "Return all 12 Fall/November 2026 AI proof-claim targets (explicitly flagged unretired) together with the 6-item November 20, 2026 AI Proof-Claim Verification Audit ledger.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_top_ranked",
        "description": "List top-ranked open problems sorted by 'css_score' (0thernes Composite Severity Score), 'titan_index', 'pagerank', or 'near_term_leverage_score', optionally filtered by Macro-Pillar.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": ["css_score", "titan_index", "pagerank", "near_term_leverage_score"],
                    "default": "css_score",
                },
                "pillar": {"type": "string", "description": "Optional exact Macro-Pillar filter"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 15},
            },
        },
    },
    {
        "name": "get_pillar_summary",
        "description": "Return the 8-Macro-Pillar comparative quantitative scorecard (problem counts, share, Mean CSS, Mean Titan, Difficulty, Tractability, Impact, AI claims).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_atlas_provenance",
        "description": "Return canonical author/ORCID identity, 0thernes LLC verification boundaries, Pure Lean 4.35.0 formal invariant audit status (58 theorems, 0 sorry), dual-license terms, and dataset summary stats.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _query_db(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(str(DEFAULT_DB))
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def dispatch_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "search_problems":
        return search_atlas(
            query=args.get("query"),
            pillar=args.get("pillar"),
            superdomain=args.get("superdomain"),
            flag=args.get("flag"),
            top=int(args.get("top", 8)),
            hops=int(args.get("hops", 1)),
        )
    if name == "get_problem":
        res = search_atlas(problem_id=str(args["problem_id"]), hops=int(args.get("hops", 1)))
        if not res["results"]:
            raise ValueError(f"Problem ID not found: {args['problem_id']}")
        return res["results"][0]
    if name == "compare_problems":
        return compare_two_problems(str(args["id_a"]), str(args["id_b"]))
    if name == "list_nov2026_ai_claims":
        claims = _query_db(
            "SELECT id, name, macro_pillar, superdomain, status_2026, verification_flag, css_score, titan_index, ai_verification_nov2026 "
            "FROM problems WHERE verification_flag = 'ai-claim-under-audit-nov2026' ORDER BY css_score DESC"
        )
        ledger = _query_db("SELECT * FROM ai_audit_nov2026")
        return {
            "policy": "All 12 Fall/Nov 2026 AI proof claims remain OFFICIALLY UNRETIRED pending independent statement-fidelity audit and peer consensus.",
            "flagged_problems_count": len(claims),
            "flagged_problems": claims,
            "audit_ledger": ledger,
        }
    if name == "get_top_ranked":
        allowed = {"css_score", "titan_index", "pagerank", "near_term_leverage_score"}
        metric = str(args.get("metric", "css_score"))
        if metric not in allowed:
            raise ValueError(f"Unsupported metric: {metric}")
        limit = max(1, min(100, int(args.get("limit", 15))))
        pillar = args.get("pillar")
        if pillar:
            rows = _query_db(
                f"SELECT id, name, macro_pillar, superdomain, year_formulated, css_score, titan_index, pagerank, near_term_leverage_score, status_2026, verification_flag "
                f"FROM problems WHERE macro_pillar = ? ORDER BY {metric} DESC, id ASC LIMIT ?",
                (pillar, limit),
            )
        else:
            rows = _query_db(
                f"SELECT id, name, macro_pillar, superdomain, year_formulated, css_score, titan_index, pagerank, near_term_leverage_score, status_2026, verification_flag "
                f"FROM problems ORDER BY {metric} DESC, id ASC LIMIT ?",
                (limit,),
            )
        return {"metric": metric, "pillar": pillar, "count": len(rows), "results": rows}
    if name == "get_pillar_summary":
        return {"pillars": _query_db("SELECT * FROM pillar_summary")}
    if name == "get_atlas_provenance":
        meta_rows = _query_db("SELECT key, value FROM metadata")
        meta = {r["key"]: r["value"] for r in meta_rows}
        return {
            "title": "Unsolved Problems Mega-Atlas (V2.2.0)",
            "author": "Alexander Stephen Donahue",
            "orcid": "0009-0006-8168-9648",
            "orcid_url": "https://orcid.org/0009-0006-8168-9648",
            "affiliation": "0thernes LLC, Spokane, WA, USA",
            "repository": "https://github.com/0thernes/unsolved-problems-mega-atlas",
            "web_atlas": "https://0thernes.github.io/unsolved-problems-mega-atlas/",
            "master_archive_id": "0TH-BUILD-007",
            "dual_license": {"data": "CC-BY-4.0", "code": "MIT"},
            "lean_verification": {
                "toolchain": "leanprover/lean4:v4.35.0",
                "framework": "Pure Lean 4.35.0 (zero Mathlib, zero sorry, zero native_decide)",
                "modules": 7,
                "lines": 817,
                "audited_theorems": 58,
                "axiom_allowlist": ["propext", "Quot.sound"],
                "boundary": "Certifies exact scoring, quadrant, era, taxonomy, finite graph handshaking, and AutoResearch keep/discard ratchet invariants ONLY; does NOT prove any of the 1,855 open problems.",
            },
            "ai_disclosure": "Curated by solo human researcher Alexander Stephen Donahue with disclosed AI assistance; quantitative rubric scores are falsifiable editorial estimates, not peer-reviewed measurements.",
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


def serve_stdio() -> None:
    """Serve newline-delimited JSON-RPC 2.0 over stdin/stdout (MCP standard stdio transport)."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()
            continue
        resp = handle_request(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    serve_stdio()
