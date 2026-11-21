"""Comprehensive 21-test pytest verification suite for the Unsolved Problems Mega-Atlas (V2.2.0, 0thernes LLC)."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import jsonschema
import networkx as nx
import openpyxl
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "autoresearch"))

from v2_loader import compute_css_score, load_v2_master  # noqa: E402
from v2_schema import CANONICAL_HUBS, MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR  # noqa: E402
from query import compare_two_problems, search_atlas  # noqa: E402
from evaluate import evaluate_all  # noqa: E402

EXPECTED_ORCID = "0009-0006-8168-9648"


@pytest.fixture(scope="module")
def master_data():
    return load_v2_master()


# ==================== 1. SCHEMA & TAXONOMY INTEGRITY ====================


def test_problem_count_and_uniqueness(master_data):
    df = master_data["df"]
    assert len(df) == 1855
    assert df["id"].is_unique
    assert master_data["summary_stats"]["raw_authored_before_dedup"] >= len(df)


def test_all_pillars_superdomains_and_hubs_present(master_data):
    df = master_data["df"]
    assert set(df["macro_pillar"].unique()) == set(MACRO_PILLARS)
    assert set(df["superdomain"].unique()) == set(SUPERDOMAIN_TO_PILLAR.keys())
    id_set = set(df["id"])
    for hub_key, hub_id in CANONICAL_HUBS.items():
        assert hub_id in id_set, f"Missing canonical hub {hub_key} -> {hub_id}"


def test_json_schema_validation_all_records(master_data):
    schema = json.loads((ROOT / "schema" / "problem.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for rec in master_data["df"].to_dict(orient="records"):
        errors = list(validator.iter_errors(rec))
        assert not errors, f"Schema error on {rec['id']}: {errors[0].message}"


# ==================== 2. SCORING & LEAN-CORRESPONDING INVARIANTS ====================


def test_css_and_titan_exact_bounds(master_data):
    df = master_data["df"]
    assert (df["css_score"] >= 0.0).all() and (df["css_score"] <= 100.0).all()
    assert (df["titan_index"] >= 0.90).all() and (df["titan_index"] <= 10.00).all()
    assert (df["near_term_leverage_score"] >= 0.1).all() and (df["near_term_leverage_score"] <= 10.0).all()
    # Antiquity 300-year saturation check
    assert compute_css_score(10, 10, 10, 300, 1) == compute_css_score(10, 10, 10, 2500, 1)
    assert compute_css_score(9, 8, 10, 100, 5) > compute_css_score(8, 8, 10, 100, 5)
    assert compute_css_score(8, 8, 10, 100, 3) > compute_css_score(8, 8, 10, 100, 7)


def test_quadrant_leverage_lower_bound(master_data):
    df = master_data["df"]
    q1 = df[df["strategic_quadrant"].str.startswith("Q1:")]
    assert len(q1) > 0
    # Matches Lean theorem MegaAtlasProofs.Quadrants.Q1_leverage_ge_56
    assert (q1["near_term_leverage_score"] >= 5.6).all()


def test_pairwise_comparator_antisymmetry():
    # Matches Lean theorems MegaAtlasProofs.AutoResearchInvariants.metricDelta_self & metricDelta_antisymm
    c_ab = compare_two_problems("NT-001", "CS-001")
    c_ba = compare_two_problems("CS-001", "NT-001")
    c_aa = compare_two_problems("NT-001", "NT-001")
    for k, v in c_ab["deltas_a_minus_b"].items():
        assert round(v + c_ba["deltas_a_minus_b"][k], 6) == 0.0, f"Antisymmetry failed for {k}"
        assert c_aa["deltas_a_minus_b"][k] == 0
    assert c_ab["graph_relation"]["shared_neighbor_ids"] == c_ba["graph_relation"]["shared_neighbor_ids"]


# ==================== 3. KNOWLEDGE-GRAPH INVARIANTS ====================


def test_graph_connectivity_and_handshaking(master_data):
    df = master_data["df"]
    G = master_data["G"]
    s = master_data["summary_stats"]
    assert nx.number_connected_components(G) == 1
    assert s["largest_component_size"] == len(df)
    assert int(df["graph_degree"].sum()) == 2 * G.number_of_edges()
    assert s["cross_pillar_edges"] <= s["cross_superdomain_edges"] <= s["total_graph_edges"]
    assert abs(df["pagerank"].sum() - 1.0) < 1e-3


# ==================== 4. EPISTEMIC INTEGRITY & NOV 2026 AI AUDIT ====================


def test_nov2026_ai_claims_explicitly_flagged(master_data):
    df = master_data["df"]
    ai_claims = df[df["status_2026"] == "AI Proof Claim (Fall/Nov 2026) — Under Verification"]
    assert len(ai_claims) == 12
    assert (ai_claims["verification_flag"] == "ai-claim-under-audit-nov2026").all()
    for must_flag in ("NT-001", "NT-002", "ANL-001"):
        row = df[df["id"] == must_flag].iloc[0]
        assert row["verification_flag"] == "ai-claim-under-audit-nov2026"


def test_every_record_has_valid_verification_flag(master_data):
    df = master_data["df"]
    valid = {
        "ai-claim-under-audit-nov2026",
        "disputed-human-claim",
        "primary-registry-indexed",
        "ai-assisted-editorial-synthesis",
    }
    assert set(df["verification_flag"].unique()).issubset(valid)


# ==================== 5. CROSS-FORMAT, RAG & LIVE MCP SERVER ====================


def test_exported_files_parity(master_data):
    n = len(master_data["df"])
    csv_df = pd.read_csv(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.csv")
    tsv_df = pd.read_csv(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.tsv", sep="\t")
    payload = json.loads((ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.json").read_text(encoding="utf-8"))
    jsonl_lines = (ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.jsonl").read_text(encoding="utf-8").splitlines()

    assert len(csv_df) == n
    assert len(tsv_df) == n
    assert len(payload["problems"]) == n
    assert len(jsonl_lines) == n
    assert payload["metadata"]["orcid"] == EXPECTED_ORCID

    wb = openpyxl.load_workbook(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.xlsx", read_only=True)
    assert len(wb.sheetnames) == 13
    wb.close()

    conn = sqlite3.connect(str(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.sqlite"))
    try:
        assert conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0] == n
        assert conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0] == master_data["G"].number_of_edges()
    finally:
        conn.close()


def test_offline_rag_hybrid_bm25_and_graph_hops():
    res = search_atlas(query="Riemann Hypothesis zeta zeros", top=5, hops=1)
    assert res["count"] >= 1
    assert res["results"][0]["id"] == "NT-001"
    assert len(res["results"][0]["graph_neighbors"]) >= 1

    exact = search_atlas(problem_id="CS-001", hops=1)
    assert exact["count"] == 1
    assert exact["results"][0]["id"] == "CS-001"
    assert len(exact["results"][0]["graph_neighbors"]) >= 1


def test_mcp_stdio_server_end_to_end():
    """Spawn mcp_server/server.py over real stdio JSON-RPC 2.0 and test initialize, tools/list & 4 tools."""
    reqs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_problem", "arguments": {"problem_id": "NT-001", "hops": 1}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "compare_problems", "arguments": {"id_a": "NT-001", "id_b": "CS-001"}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "list_nov2026_ai_claims", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "get_atlas_provenance", "arguments": {}}},
    ]
    stdin_payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=stdin_payload,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    resps = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    assert len(resps) == len(reqs)
    assert resps[0]["result"]["serverInfo"]["name"] == "unsolved-problems-mega-atlas"
    tools = {t["name"] for t in resps[1]["result"]["tools"]}
    assert tools == {
        "search_problems", "get_problem", "compare_problems", "list_nov2026_ai_claims",
        "get_top_ranked", "get_pillar_summary", "get_atlas_provenance",
    }
    p_nt001 = json.loads(resps[2]["result"]["content"][0]["text"])
    assert p_nt001["id"] == "NT-001"
    comp = json.loads(resps[3]["result"]["content"][0]["text"])
    assert "deltas_a_minus_b" in comp
    claims = json.loads(resps[4]["result"]["content"][0]["text"])
    assert claims["flagged_problems_count"] == 12
    prov = json.loads(resps[5]["result"]["content"][0]["text"])
    assert prov["orcid"] == EXPECTED_ORCID
    assert prov["lean_verification"]["audited_theorems"] == 58


# ==================== 6. KARPATHY AUTORESEARCH HARNESS ====================


def test_autoresearch_evaluator_and_results_ledger():
    m = evaluate_all()
    assert m["hard_gates"] is True
    assert m["schema_health"] == 100.0
    assert m["rag_mrr5"] >= 95.0
    assert m["lean_theorems"] == 58
    assert m["aqs_score"] >= 90.0

    tsv_lines = (ROOT / "autoresearch" / "results.tsv").read_text(encoding="utf-8").splitlines()
    assert len(tsv_lines) >= 3
    headers = tsv_lines[0].split("\t")
    assert "aqs_score" in headers and "status" in headers and "hard_gates" in headers


# ==================== 7. FAIR METADATA (ZENODO, CROISSANT, RO-CRATE) ====================


def test_zenodo_json_metadata():
    z = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert z["creators"][0]["orcid"] == EXPECTED_ORCID
    assert z["license"] == "cc-by-4.0"
    assert z["version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def test_croissant_json_ld_and_sha256_parity():
    cr = json.loads((ROOT / "croissant.json").read_text(encoding="utf-8"))
    assert cr["@type"] == "sc:Dataset"
    assert cr["conformsTo"] == "http://mlcommons.org/croissant/1.0"
    assert EXPECTED_ORCID in cr["creator"]["identifier"]
    assert len(cr["recordSet"][0]["field"]) == 40
    for dist in cr["distribution"]:
        fname = dist["name"]
        actual = hashlib.sha256((ROOT / "outputs" / fname).read_bytes()).hexdigest()
        assert dist["sha256"] == actual, f"Croissant SHA-256 drift on {fname}"


def test_ro_crate_metadata():
    rc = json.loads((ROOT / "ro-crate-metadata.json").read_text(encoding="utf-8"))
    assert rc["@context"] == "https://w3id.org/ro/crate/1.1/context"
    ids = {node["@id"] for node in rc["@graph"]}
    assert f"https://orcid.org/{EXPECTED_ORCID}" in ids
    assert "lean/MegaAtlasProofs.lean" in ids
    assert "mcp_server/server.py" in ids
    assert "autoresearch/program.md" in ids


# ==================== 8. INSTITUTIONAL GOVERNANCE, LEAN & CHECKSUMS ====================


def test_institutional_orcid_and_governance_files():
    for rel in [
        "VERSION",
        "CITATION.cff",
        "CITATION.bib",
        ".zenodo.json",
        "croissant.json",
        "ro-crate-metadata.json",
        "AGENTS.md",
        "CLAUDE.md",
        "llms.txt",
        "SECURITY.md",
        "LICENSE",
        "LICENSE-CODE",
        "NOTICE",
        "AUTHORS.md",
        "PHILOSOPHY.md",
        "ARCHITECTURE.md",
        "VERIFICATION.md",
        "EVIDENCE.md",
        "RANKING.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "docs/METHODOLOGY.md",
        "docs/AI_DISCLOSURE.md",
        "docs/ACADEMIC_REVIEW.md",
        "docs/WHITE_PAPER.md",
        "docs/DATASHEET.md",
        "autoresearch/program.md",
        "autoresearch/evaluate.py",
        "autoresearch/results.tsv",
        "autoresearch/whiteboard.md",
        "autoresearch/OSS_STACK.md",
        "mcp_server/server.py",
        "mcp_server/README.md",
    ]:
        assert (ROOT / rel).exists(), f"Missing institutional artifact: {rel}"

    for rel in [
        "CITATION.cff", "CITATION.bib", ".zenodo.json", "croissant.json", "ro-crate-metadata.json",
        "README.md", "AUTHORS.md", "AGENTS.md", "llms.txt", "VERIFICATION.md", "EVIDENCE.md",
        "RANKING.md", "docs/WHITE_PAPER.md", "docs/DATASHEET.md",
    ]:
        assert EXPECTED_ORCID in (ROOT / rel).read_text(encoding="utf-8"), f"Missing ORCID in {rel}"


def test_lean_sources_zero_sorry_and_58_audited_theorems():
    lean_files = [p for p in (ROOT / "lean").rglob("*.lean") if ".lake" not in p.parts]
    assert len(lean_files) == 7
    for lf in lean_files:
        raw = lf.read_text(encoding="utf-8")
        no_blocks = re.sub(r"/-.*?-/", "", raw, flags=re.S)
        code = "\n".join(line.split("--", 1)[0] for line in no_blocks.splitlines())
        for tok in ("sorry", "admit", "native_decide"):
            assert not re.search(rf"\b{tok}\b", code), f"Forbidden '{tok}' in {lf}"
        for line in code.splitlines():
            assert not line.strip().startswith("axiom "), f"Custom axiom in {lf}: {line}"
    aud = (ROOT / "lean" / "MegaAtlasProofs" / "VerifyAxioms.lean").read_text(encoding="utf-8")
    assert sum(1 for l in aud.splitlines() if l.strip().startswith("#print axioms ")) == 58


def test_sha256_checksums_manifest_exact():
    chk = ROOT / "CHECKSUMS.sha256"
    assert chk.exists()
    lines = [l.strip() for l in chk.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) >= 44
    for line in lines:
        expected, rel = line.split(None, 1)
        target = ROOT / rel
        assert target.exists(), f"Missing hashed file: {rel}"
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        assert actual == expected, f"SHA-256 mismatch for {rel}"
