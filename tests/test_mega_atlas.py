"""Comprehensive 25-test pytest verification suite for the Unsolved Problems Mega-Atlas (V2.3.0, 0thernes LLC)."""

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

from v2_loader import (  # noqa: E402
    ABSTRACTION_LAYERS,
    SUBSTRATE_CLASSES,
    compute_css_score,
    load_v2_master,
)
from v2_schema import CANONICAL_HUBS, MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR  # noqa: E402
from query import compare_two_problems, search_atlas  # noqa: E402
from evaluate import evaluate_all  # noqa: E402

EXPECTED_ORCID = "0009-0006-8168-9648"


@pytest.fixture(scope="module")
def master_data():
    return load_v2_master()


# ==================== 1. SCHEMA & TAXONOMY INTEGRITY ====================


def test_problem_count_uniqueness_and_zero_dangling_links(master_data):
    df = master_data["df"]
    s = master_data["summary_stats"]
    assert len(df) == 1900
    assert df.shape[1] == 48
    assert df["id"].is_unique
    assert s["raw_authored_before_dedup"] >= len(df)
    assert s["unresolved_raw_links_count"] == 0


def test_all_pillars_superdomains_substrates_layers_and_hubs_present(master_data):
    df = master_data["df"]
    assert set(df["macro_pillar"].unique()) == set(MACRO_PILLARS)
    assert set(df["superdomain"].unique()) == set(SUPERDOMAIN_TO_PILLAR.keys())
    assert set(df["substrate_class"].unique()) == set(SUBSTRATE_CLASSES)
    assert set(df["abstraction_layer"].unique()) == set(ABSTRACTION_LAYERS)
    id_set = set(df["id"])
    for hub_key, hub_id in CANONICAL_HUBS.items():
        assert hub_id in id_set, f"Missing canonical hub {hub_key} -> {hub_id}"


def test_json_schema_validation_all_records(master_data):
    schema = json.loads((ROOT / "schema" / "problem.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for rec in master_data["df"].to_dict(orient="records"):
        errors = list(validator.iter_errors(rec))
        assert not errors, f"Schema error on {rec['id']}: {errors[0].message}"


# ==================== 2. SCORING, LAYER & LEAN-CORRESPONDING INVARIANTS ====================


def test_css_and_titan_exact_bounds(master_data):
    df = master_data["df"]
    assert (df["css_score"] >= 0.0).all() and (df["css_score"] <= 100.0).all()
    assert (df["titan_index"] >= 0.90).all() and (df["titan_index"] <= 10.00).all()
    assert (df["near_term_leverage_score"] >= 0.1).all() and (df["near_term_leverage_score"] <= 10.0).all()
    # Antiquity 300-year saturation check
    assert compute_css_score(10, 10, 10, 300, 1) == compute_css_score(10, 10, 10, 2500, 1)
    assert compute_css_score(9, 8, 10, 100, 5) > compute_css_score(8, 8, 10, 100, 5)
    assert compute_css_score(8, 8, 10, 100, 3) > compute_css_score(8, 8, 10, 100, 7)


def test_layer_gradient_margin_spectrum_bounds(master_data):
    """Verify V2.3.0 multi-layer invariants matching Lean MegaAtlasProofs.LayerGradients."""
    df = master_data["df"]
    assert ((df["hardness_tractability_gradient"] >= -9) & (df["hardness_tractability_gradient"] <= 9)).all()
    assert (df["hardness_tractability_gradient"] == df["difficulty_score"] - df["tractability_2050"]).all()
    assert ((df["css_titan_margin"] >= -100.0) & (df["css_titan_margin"] <= 100.0)).all()
    assert ((df["epistemic_spectrum_score"] >= 0.0) & (df["epistemic_spectrum_score"] <= 100.0)).all()
    assert ((df["bridge_margin_ratio"] >= 0.0) & (df["bridge_margin_ratio"] <= 1.0)).all()
    assert ((df["adjacent_pillars_count"] >= 0) & (df["adjacent_pillars_count"] <= 7)).all()
    # Apex Multi-Pillar Keystone iff adjacent_pillars_count >= 3
    apex_mask = df["margin_role"] == "Apex Multi-Pillar Keystone (3+ Adjacent Pillars)"
    assert (apex_mask == (df["adjacent_pillars_count"] >= 3)).all()


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


# ==================== 3. BICONNECTED KNOWLEDGE-GRAPH INVARIANTS ====================


def test_graph_biconnectivity_and_handshaking(master_data):
    df = master_data["df"]
    G = master_data["G"]
    s = master_data["summary_stats"]
    assert nx.number_connected_components(G) == 1
    assert s["largest_component_size"] == len(df)
    assert s["articulation_points"] == 0
    assert s["graph_bridges"] == 0
    assert nx.is_biconnected(G)
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


# ==================== 5. CROSS-FORMAT, RAG & DUAL-FRAMED 9-TOOL MCP SERVER ====================


def test_exported_files_parity(master_data):
    n = len(master_data["df"])
    csv_df = pd.read_csv(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.csv")
    tsv_df = pd.read_csv(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.tsv", sep="\t")
    payload = json.loads((ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.json").read_text(encoding="utf-8"))
    jsonl_lines = (ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.jsonl").read_text(encoding="utf-8").splitlines()

    assert len(csv_df) == n and csv_df.shape[1] == 48
    assert len(tsv_df) == n and tsv_df.shape[1] == 48
    assert len(payload["problems"]) == n
    assert len(jsonl_lines) == n
    assert payload["metadata"]["orcid"] == EXPECTED_ORCID

    wb = openpyxl.load_workbook(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.xlsx", read_only=True)
    assert len(wb.sheetnames) == 14
    wb.close()

    conn = sqlite3.connect(str(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.sqlite"))
    try:
        assert conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0] == n
        assert conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0] == master_data["G"].number_of_edges()
        assert conn.execute("SELECT COUNT(*) FROM substrate_summary").fetchone()[0] == 8
    finally:
        conn.close()


def test_offline_rag_hybrid_bm25_pagerank_and_graph_hops():
    for q, expected_id in [
        ("Riemann Hypothesis zeta zeros", "NT-001"),
        ("high temperature superconductivity cuprates pairing", "CM-001"),
        ("Continuum Hypothesis independence ZFC forcing", "LOG-001"),
    ]:
        res = search_atlas(query=q, top=5, hops=1)
        assert res["count"] >= 1
        assert res["results"][0]["id"] == expected_id
        assert len(res["results"][0]["graph_neighbors"]) >= 1

    exact = search_atlas(problem_id="CS-001", hops=1)
    assert exact["count"] == 1
    assert exact["results"][0]["id"] == "CS-001"
    assert len(exact["results"][0]["graph_neighbors"]) >= 1


def test_mcp_stdio_server_ndjson_all_9_tools():
    """Spawn mcp_server/server.py over real NDJSON stdio JSON-RPC 2.0 and test all 9 tools."""
    reqs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "Navier-Stokes", "top": 3}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_problem", "arguments": {"problem_id": "NT-001", "hops": 1}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "compare_problems", "arguments": {"id_a": "NT-001", "id_b": "CS-001"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "list_nov2026_ai_claims", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "get_top_ranked", "arguments": {"metric": "css_score", "limit": 5}}},
        {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "get_pillar_summary", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": "get_substrate_layer_summary", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "get_margin_and_gradient_extremes", "arguments": {"limit": 5}}},
        {"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": {"name": "get_atlas_provenance", "arguments": {}}},
    ]
    stdin_payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=stdin_payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    assert len(resps) == len(reqs)
    expected_ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert resps[0]["result"]["serverInfo"]["name"] == "unsolved-problems-mega-atlas"
    assert resps[0]["result"]["serverInfo"]["version"] == expected_ver
    tools = {t["name"] for t in resps[1]["result"]["tools"]}
    assert tools == {
        "search_problems", "get_problem", "compare_problems", "list_nov2026_ai_claims",
        "get_top_ranked", "get_pillar_summary", "get_substrate_layer_summary",
        "get_margin_and_gradient_extremes", "get_atlas_provenance",
    }
    p_nt001 = json.loads(resps[3]["result"]["content"][0]["text"])
    assert p_nt001["id"] == "NT-001"
    comp = json.loads(resps[4]["result"]["content"][0]["text"])
    assert "deltas_a_minus_b" in comp
    claims = json.loads(resps[5]["result"]["content"][0]["text"])
    assert claims["flagged_problems_count"] == 12
    sub_sum = json.loads(resps[8]["result"]["content"][0]["text"])
    assert len(sub_sum["substrates"]) == 8
    assert len(sub_sum["abstraction_layers"]) == 7
    margins = json.loads(resps[9]["result"]["content"][0]["text"])
    assert len(margins["steepest_hardness_tractability_chasms"]) == 5
    assert len(margins["highest_tractability_over_hardness_margins"]) == 5
    assert len(margins["largest_positive_css_over_titan_margins"]) == 5
    assert len(margins["apex_multi_pillar_keystones"]) == 5
    prov = json.loads(resps[10]["result"]["content"][0]["text"])
    assert prov["orcid"] == EXPECTED_ORCID
    assert prov["lean_verification"]["audited_theorems"] == 72


def test_mcp_stdio_server_content_length_framing():
    """Verify MCP server also speaks standard LSP/MCP Content-Length header framing."""
    req = json.dumps({"jsonrpc": "2.0", "id": 99, "method": "initialize", "params": {}}).encode("utf-8")
    framed = f"Content-Length: {len(req)}\r\n\r\n".encode("ascii") + req
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=framed,
        capture_output=True,
        timeout=30,
        check=True,
    )
    assert proc.stdout.startswith(b"Content-Length: ")
    header, body = proc.stdout.split(b"\r\n\r\n", 1)
    expected_len = int(header.decode("ascii").split(":", 1)[1].strip())
    assert len(body) == expected_len
    msg = json.loads(body.decode("utf-8"))
    assert msg["id"] == 99
    assert msg["result"]["serverInfo"]["version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()


# ==================== 6. KARPATHY AUTORESEARCH HARNESS & TRACK B PILOT ====================


def test_autoresearch_evaluator_100pct_rag_and_results_ledger():
    m = evaluate_all()
    assert m["hard_gates"] is True
    assert m["schema_health"] == 100.0
    assert m["rag_mrr5"] == 100.0
    assert m["rag_top1"] == 25
    assert m["lean_theorems"] == 72
    assert m["aqs_score"] >= 97.0

    tsv_lines = (ROOT / "autoresearch" / "results.tsv").read_text(encoding="utf-8").splitlines()
    assert len(tsv_lines) >= 6
    headers = tsv_lines[0].split("\t")
    assert "aqs_score" in headers and "status" in headers and "hard_gates" in headers


def test_track_b_antihydra_pilot_artifact_reproducible():
    res_path = ROOT / "research" / "runs" / "LOG-002_antihydra_pilot" / "RESULTS.json"
    assert res_path.exists()
    data = json.loads(res_path.read_text(encoding="utf-8"))
    assert data["problem_id"] == "LOG-002"
    assert data["canonical_a0_8_5000_steps"]["steps_executed"] == 5000
    assert data["canonical_a0_8_5000_steps"]["halted"] is False
    assert data["canonical_a0_8_5000_steps"]["final_b"] == 2599
    assert data["seed_sweep_a0_2_to_100_max2000"]["halted_count"] == 66
    assert data["seed_sweep_a0_2_to_100_max2000"]["surviving_count"] == 33


def test_alias_redirection_eliminates_all_duplicate_secondaries(master_data):
    from v2_loader import EXPLICIT_DUPLICATE_ALIASES
    id_set = set(master_data["df"]["id"])
    for secondary_id, canonical_id in EXPLICIT_DUPLICATE_ALIASES.items():
        assert secondary_id not in id_set, f"Secondary duplicate {secondary_id} still present!"
        assert canonical_id in id_set, f"Canonical merge target {canonical_id} missing!"


def test_substrate_layer_and_margin_matrices_partition_all_1900(master_data):
    assert int(master_data["df_substrates"]["Problem_Count"].sum()) == 1900
    ct_sl = master_data["ct_substrate_layer"].drop(index="Total", columns="Total", errors="ignore")
    assert int(ct_sl.values.sum()) == 1900
    ct_mp = master_data["ct_margin_pillar"].drop(index="Total", columns="Total", errors="ignore")
    assert int(ct_mp.values.sum()) == 1900


def test_all_15_charts_png_and_svg_present_and_nonempty():
    chart_dir = ROOT / "outputs" / "charts"
    pngs = sorted(chart_dir.glob("*.png"))
    svgs = sorted(chart_dir.glob("*.svg"))
    assert len(pngs) == 15
    assert len(svgs) == 15
    for p in pngs + svgs:
        assert p.stat().st_size > 5_000, f"Chart file suspiciously small: {p.name}"


# ==================== 7. FAIR METADATA & OPTION 1 ZENODO DRY-RUN ====================


def test_zenodo_json_metadata_and_publisher_dry_run():
    z = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert z["creators"][0]["orcid"] == EXPECTED_ORCID
    assert z["license"] == "cc-by-4.0"
    assert z["version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "publish_zenodo.py"), "--dry-run"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    assert "DRY-RUN PASS" in proc.stdout


def test_croissant_json_ld_and_sha256_parity():
    cr = json.loads((ROOT / "croissant.json").read_text(encoding="utf-8"))
    assert cr["@type"] == "sc:Dataset"
    assert cr["conformsTo"] == "http://mlcommons.org/croissant/1.0"
    assert EXPECTED_ORCID in cr["creator"]["identifier"]
    assert len(cr["recordSet"][0]["field"]) == 48
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
        "docs/FORENSIC_AUDIT_V2.3.md",
        "docs/PRESERVATION.md",
        "autoresearch/program.md",
        "autoresearch/evaluate.py",
        "autoresearch/results.tsv",
        "autoresearch/whiteboard.md",
        "autoresearch/OSS_STACK.md",
        "mcp_server/server.py",
        "mcp_server/README.md",
        "scripts/forensic_audit.py",
        "scripts/publish_zenodo.py",
    ]:
        assert (ROOT / rel).exists(), f"Missing institutional artifact: {rel}"

    for rel in [
        "CITATION.cff", "CITATION.bib", ".zenodo.json", "croissant.json", "ro-crate-metadata.json",
        "README.md", "AUTHORS.md", "AGENTS.md", "llms.txt", "VERIFICATION.md", "EVIDENCE.md",
        "RANKING.md", "docs/WHITE_PAPER.md", "docs/DATASHEET.md", "docs/FORENSIC_AUDIT_V2.3.md",
        "docs/PRESERVATION.md",
    ]:
        assert EXPECTED_ORCID in (ROOT / rel).read_text(encoding="utf-8"), f"Missing ORCID in {rel}"


def test_lean_sources_zero_sorry_and_72_audited_theorems():
    lean_files = [p for p in (ROOT / "lean").rglob("*.lean") if ".lake" not in p.parts]
    assert len(lean_files) == 8
    for lf in lean_files:
        raw = lf.read_text(encoding="utf-8")
        no_blocks = re.sub(r"/-.*?-/", "", raw, flags=re.S)
        code = "\n".join(line.split("--", 1)[0] for line in no_blocks.splitlines())
        for tok in ("sorry", "admit", "native_decide"):
            assert not re.search(rf"\b{tok}\b", code), f"Forbidden '{tok}' in {lf}"
        for line in code.splitlines():
            assert not line.strip().startswith("axiom "), f"Custom axiom in {lf}: {line}"
    aud = (ROOT / "lean" / "MegaAtlasProofs" / "VerifyAxioms.lean").read_text(encoding="utf-8")
    assert sum(1 for l in aud.splitlines() if l.strip().startswith("#print axioms ")) == 72


def test_sha256_checksums_manifest_exact():
    chk = ROOT / "CHECKSUMS.sha256"
    assert chk.exists()
    lines = [l.strip() for l in chk.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) >= 52
    for line in lines:
        expected, rel = line.split(None, 1)
        target = ROOT / rel
        assert target.exists(), f"Missing hashed file: {rel}"
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        assert actual == expected, f"SHA-256 mismatch for {rel}"
