#!/usr/bin/env python3
"""
IMMUTABLE AutoResearch Evaluation Harness (`autoresearch/evaluate.py`)
Inspired by Andrej Karpathy's `karpathy/autoresearch` read-only `prepare.py` pattern.

DO NOT MODIFY THIS FILE DURING AUTONOMOUS EXPERIMENT LOOPS.
Modifying this harness invalidates comparability across `autoresearch/results.tsv`.

Computes the deterministic Atlas Quality Score (AQS, 0–100) matching the
Pure Lean 4.35.0 formal invariant `MegaAtlasProofs.AutoResearchInvariants.aqsBps`:
    AQS = 0.25 * schema_health
        + 0.25 * rag_mrr5_pct
        + 0.20 * provenance_score
        + 0.15 * graph_coupling_score
        + 0.15 * formal_and_interop_score

Usage:
    python autoresearch/evaluate.py
    python autoresearch/evaluate.py --verify-gates
    python autoresearch/evaluate.py --log --status baseline --desc "v2.1.0 baseline (pure-OR FTS5)"
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))

from v2_loader import load_v2_master  # noqa: E402
from v2_schema import CANONICAL_HUBS, MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR  # noqa: E402
from query import search_atlas  # noqa: E402

EXPECTED_ORCID = "0009-0006-8168-9648"
RESULTS_TSV = ROOT / "autoresearch" / "results.tsv"

# Fixed 25-query cross-disciplinary Gold Benchmark across all 8 Macro-Pillars
# Format: (query_text, expected_canonical_id)
GOLD_RAG_BENCHMARK: List[Tuple[str, str]] = [
    ("riemann hypothesis zeta zeros", "NT-001"),
    ("navier stokes existence smoothness blowup", "ANL-001"),
    ("p versus np computational complexity", "CS-001"),
    ("yang mills mass gap gauge theory", "QM-002"),
    ("quantum gravity general relativity unification", "GR-001"),
    ("black hole information paradox hawking", "GR-002"),
    ("fluid turbulence intermittency closure", "FLD-001"),
    ("equilibrium climate sensitivity cloud aerosol", "GEO-002"),
    ("high temperature superconductivity room temperature", "CM-001"),
    ("protein folding dynamics conformational", "BIO-003"),
    ("hard problem of consciousness qualia", "NEURO-001"),
    ("ai alignment value loading superintelligence", "AI-001"),
    ("fault tolerant quantum computer logical qubits", "QC-001"),
    ("post moore silicon cmos atomic scaling", "HW-001"),
    ("commercial nuclear fusion plasma energy", "ENR-001"),
    ("is ought gap moral realism ethics", "PHIL-004"),
    ("free will determinism moral responsibility", "PHIL-003"),
    ("origin of human language glottogony", "HUM-001"),
    ("social choice arrow voting aggregation", "ECON-002"),
    ("dark matter wimps axions galactic", "ASTRO-001"),
    ("dark energy cosmological constant vacuum", "ASTRO-002"),
    ("abiogenesis origin of life rna", "BIO-001"),
    ("continuum hypothesis zfc cardinal", "LOG-001"),
    ("busy beaver turing machine unprovable", "LOG-002"),
    ("hodge conjecture algebraic cycles cohomology", "GEOM-001"),
]


def count_audited_lean_theorems() -> Tuple[int, bool]:
    """Count `#print axioms` entries and check zero sorry/admit/native_decide in lean/."""
    lean_dir = ROOT / "lean"
    lean_files = [p for p in lean_dir.rglob("*.lean") if ".lake" not in p.parts]
    clean = len(lean_files) >= 6
    for lf in lean_files:
        raw = lf.read_text(encoding="utf-8")
        no_blocks = re.sub(r"/-.*?-/", "", raw, flags=re.S)
        code = "\n".join(line.split("--", 1)[0] for line in no_blocks.splitlines())
        for tok in ("sorry", "admit", "native_decide"):
            if re.search(rf"\b{tok}\b", code):
                clean = False
        for line in code.splitlines():
            if line.strip().startswith("axiom "):
                clean = False
    audit_file = lean_dir / "MegaAtlasProofs" / "VerifyAxioms.lean"
    thms = 0
    if audit_file.exists():
        thms = sum(
            1 for line in audit_file.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("#print axioms ")
        )
    return thms, clean


def evaluate_rag_mrr5() -> Tuple[float, int]:
    """Compute Mean Reciprocal Rank @ 5 (0..100) and top-1 hits on the 25-query benchmark."""
    rr_sum = 0.0
    top1 = 0
    for q_text, expected_id in GOLD_RAG_BENCHMARK:
        res = search_atlas(query=q_text, top=5, hops=0)
        ids = [r["id"] for r in res["results"]]
        if expected_id in ids:
            rank = ids.index(expected_id) + 1
            rr_sum += 1.0 / rank
            if rank == 1:
                top1 += 1
    mrr5_pct = round(100.0 * rr_sum / len(GOLD_RAG_BENCHMARK), 2)
    return mrr5_pct, top1


def evaluate_all() -> dict:
    t0 = time.perf_counter()
    data = load_v2_master()
    df = data["df"]
    G = data["G"]
    s = data["summary_stats"]

    # 1. Hard integrity gates & schema health
    schema_checks = []
    schema_checks.append(len(df) >= 1850 and df["id"].is_unique)
    schema_checks.append(df["macro_pillar"].nunique() == len(MACRO_PILLARS))
    schema_checks.append(df["superdomain"].nunique() == len(SUPERDOMAIN_TO_PILLAR))
    schema_checks.append(set(CANONICAL_HUBS.values()).issubset(set(df["id"])))
    schema_checks.append(s["connected_components"] == 1)
    schema_checks.append(int(df["graph_degree"].sum()) == 2 * G.number_of_edges())
    schema_checks.append(s["cross_pillar_edges"] <= s["cross_superdomain_edges"] <= s["total_graph_edges"])

    # Nov 2026 AI proof-claim containment gate
    ai_claims = df[df["status_2026"] == "AI Proof Claim (Fall/Nov 2026) — Under Verification"]
    schema_checks.append(len(ai_claims) == 12 and (ai_claims["verification_flag"] == "ai-claim-under-audit-nov2026").all())

    # JSON Schema validation
    prob_schema = json.loads((ROOT / "schema" / "problem.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(prob_schema)
    schema_valid = all(next(validator.iter_errors(rec), None) is None for rec in df.to_dict(orient="records"))
    schema_checks.append(schema_valid)

    # SQLite parity
    db_path = ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.sqlite"
    sqlite_ok = False
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        try:
            sqlite_ok = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0] == len(df)
        finally:
            conn.close()
    schema_checks.append(sqlite_ok)

    # Lean hygiene + ORCID gate
    lean_thms, lean_clean = count_audited_lean_theorems()
    orcid_ok = EXPECTED_ORCID in (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    schema_checks.append(lean_clean and orcid_ok)

    schema_health = round(100.0 * sum(schema_checks) / len(schema_checks), 2)
    hard_gates = all(schema_checks)

    # 2. Offline RAG MRR@5 Benchmark (25 cross-pillar queries)
    rag_mrr5, rag_top1 = evaluate_rag_mrr5()

    # 3. Provenance & FAIR Scholarly Metadata Score (0..100)
    indexed_ratio = float(
        df["verification_flag"].isin(["primary-registry-indexed", "ai-claim-under-audit-nov2026", "disputed-human-claim"]).mean()
    )
    fair_files = [
        ".zenodo.json",
        "croissant.json",
        "ro-crate-metadata.json",
        "CITATION.cff",
        "CITATION.bib",
        "docs/DATASHEET.md",
        "AGENTS.md",
        "llms.txt",
        "SECURITY.md",
    ]
    fair_present = sum(1 for rel in fair_files if (ROOT / rel).exists())
    provenance_score = round(min(100.0, indexed_ratio * 60.0 + (fair_present / len(fair_files)) * 60.0), 2)

    # 4. Knowledge-Graph Coupling Score (0..100)
    graph_coupling = round(
        min(
            100.0,
            s["cross_superdomain_edge_pct"] * 1.4
            + s["cross_pillar_edge_pct"] * 1.8
            + (20.0 if s["connected_components"] == 1 else 0.0),
        ),
        2,
    )

    # 5. Formal Verification & Agentic Interop Score (0..100)
    has_mcp = (ROOT / "mcp_server" / "server.py").exists()
    has_ar = (ROOT / "autoresearch" / "program.md").exists() and (ROOT / "autoresearch" / "whiteboard.md").exists()
    formal_score = round(
        min(100.0, (min(lean_thms, 58) / 58.0) * 60.0 + (20.0 if has_mcp else 0.0) + (20.0 if has_ar else 0.0)),
        2,
    )

    # Exact AQS formula matching MegaAtlasProofs.AutoResearchInvariants.aqsBps
    aqs_score = round(
        0.25 * schema_health
        + 0.25 * rag_mrr5
        + 0.20 * provenance_score
        + 0.15 * graph_coupling
        + 0.15 * formal_score,
        2,
    )

    elapsed_s = round(time.perf_counter() - t0, 3)
    return {
        "aqs_score": aqs_score,
        "schema_health": schema_health,
        "rag_mrr5": rag_mrr5,
        "rag_top1": rag_top1,
        "rag_total_queries": len(GOLD_RAG_BENCHMARK),
        "provenance_score": provenance_score,
        "registry_indexed_pct": round(indexed_ratio * 100.0, 2),
        "fair_files_present": f"{fair_present}/{len(fair_files)}",
        "graph_coupling": graph_coupling,
        "formal_score": formal_score,
        "lean_theorems": lean_thms,
        "hard_gates": hard_gates,
        "elapsed_s": elapsed_s,
    }


def git_short_sha() -> str:
    res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False)
    return res.stdout.strip() if res.returncode == 0 else "uncommitted"


def append_results_tsv(metrics: dict, status: str, desc: str) -> None:
    header = "timestamp_utc\tcommit\taqs_score\trag_mrr5\trag_top1\tprovenance\tgraph_coupling\tformal_score\tlean_theorems\thard_gates\tstatus\tdescription\n"
    if not RESULTS_TSV.exists():
        RESULTS_TSV.write_text(header, encoding="utf-8", newline="\n")
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = (
        f"{ts}\t{git_short_sha()}\t{metrics['aqs_score']:.2f}\t{metrics['rag_mrr5']:.2f}\t"
        f"{metrics['rag_top1']}/{metrics['rag_total_queries']}\t{metrics['provenance_score']:.2f}\t"
        f"{metrics['graph_coupling']:.2f}\t{metrics['formal_score']:.2f}\t{metrics['lean_theorems']}\t"
        f"{'PASS' if metrics['hard_gates'] else 'FAIL'}\t{status}\t{desc}\n"
    )
    with RESULTS_TSV.open("a", encoding="utf-8", newline="\n") as f:
        f.write(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Immutable AutoResearch Evaluator (Karpathy-style harness).")
    parser.add_argument("--verify-gates", action="store_true", help="Exit non-zero if any hard gate fails")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON metrics")
    parser.add_argument("--log", action="store_true", help="Append run to autoresearch/results.tsv")
    parser.add_argument("--status", default="keep", choices=["baseline", "keep", "discard", "crash"], help="Status for results.tsv")
    parser.add_argument("--desc", default="", help="One-line hypothesis/change description for results.tsv")
    args = parser.parse_args()

    m = evaluate_all()

    if args.log:
        append_results_tsv(m, args.status, args.desc or "evaluation run")

    if args.as_json:
        print(json.dumps(m, indent=2))
    else:
        print(
            f"aqs_score={m['aqs_score']:.2f} | rag_mrr5={m['rag_mrr5']:.2f} ({m['rag_top1']}/{m['rag_total_queries']} top-1) | "
            f"schema={m['schema_health']:.1f} | provenance={m['provenance_score']:.2f} (FAIR {m['fair_files_present']}) | "
            f"coupling={m['graph_coupling']:.2f} | formal={m['formal_score']:.2f} ({m['lean_theorems']} Lean thms) | "
            f"hard_gates={'PASS' if m['hard_gates'] else 'FAIL'} | elapsed={m['elapsed_s']}s"
        )

    if args.verify_gates and not m["hard_gates"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
