"""Comprehensive pytest verification suite for the Unsolved Problems Mega-Atlas (V2.1.0, 0thernes LLC)."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
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

from v2_loader import compute_css_score, load_v2_master  # noqa: E402
from v2_schema import CANONICAL_HUBS, MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR  # noqa: E402
from query import search_atlas  # noqa: E402

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
    records = master_data["df"].to_dict(orient="records")
    for rec in records:
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
    # Monotonicity spot-check
    assert compute_css_score(9, 8, 10, 100, 5) > compute_css_score(8, 8, 10, 100, 5)
    assert compute_css_score(8, 8, 10, 100, 3) > compute_css_score(8, 8, 10, 100, 7)


def test_quadrant_leverage_lower_bound(master_data):
    df = master_data["df"]
    q1 = df[df["strategic_quadrant"].str.startswith("Q1:")]
    assert len(q1) > 0
    # Matches Lean theorem MegaAtlasProofs.Quadrants.Q1_leverage_ge_56
    assert (q1["near_term_leverage_score"] >= 5.6).all()


# ==================== 3. KNOWLEDGE-GRAPH INVARIANTS ====================


def test_graph_connectivity_and_handshaking(master_data):
    df = master_data["df"]
    G = master_data["G"]
    s = master_data["summary_stats"]
    assert nx.number_connected_components(G) == 1
    assert s["largest_component_size"] == len(df)
    # Matches Lean theorem MegaAtlasProofs.GraphInvariants.handshaking_lemma
    assert int(df["graph_degree"].sum()) == 2 * G.number_of_edges()
    # Matches Lean theorem MegaAtlasProofs.GraphInvariants.edge_hierarchy
    assert s["cross_pillar_edges"] <= s["cross_superdomain_edges"] <= s["total_graph_edges"]
    # PageRank probability mass conservation
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


# ==================== 5. CROSS-FORMAT & RAG ENGINE PARITY ====================


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


def test_offline_rag_bm25_and_graph_hops():
    res = search_atlas(query="Riemann Hypothesis prime zeros", top=5, hops=1)
    assert res["count"] >= 1
    ids = [r["id"] for r in res["results"]]
    assert "NT-001" in ids
    rh = next(r for r in res["results"] if r["id"] == "NT-001")
    assert len(rh["graph_neighbors"]) >= 1

    exact = search_atlas(problem_id="CS-001", hops=1)
    assert exact["count"] == 1
    assert exact["results"][0]["id"] == "CS-001"
    assert len(exact["results"][0]["graph_neighbors"]) >= 1


# ==================== 6. INSTITUTIONAL IDENTITY & CHECKSUMS ====================


def test_institutional_orcid_and_governance_files():
    for rel in [
        "VERSION",
        "CITATION.cff",
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
    ]:
        assert (ROOT / rel).exists(), f"Missing institutional artifact: {rel}"

    for rel in ["CITATION.cff", "README.md", "AUTHORS.md", "VERIFICATION.md", "EVIDENCE.md", "RANKING.md", "docs/WHITE_PAPER.md"]:
        assert EXPECTED_ORCID in (ROOT / rel).read_text(encoding="utf-8"), f"Missing ORCID in {rel}"


def test_lean_sources_zero_sorry_and_zero_custom_axioms():
    lean_files = [p for p in (ROOT / "lean").rglob("*.lean") if ".lake" not in p.parts]
    assert len(lean_files) == 6
    for lf in lean_files:
        raw = lf.read_text(encoding="utf-8")
        no_blocks = re.sub(r"/-.*?-/", "", raw, flags=re.S)
        code = "\n".join(line.split("--", 1)[0] for line in no_blocks.splitlines())
        for tok in ("sorry", "admit", "native_decide"):
            assert not re.search(rf"\b{tok}\b", code), f"Forbidden '{tok}' in {lf}"
        for line in code.splitlines():
            assert not line.strip().startswith("axiom "), f"Custom axiom in {lf}: {line}"


def test_sha256_checksums_manifest_exact():
    chk = ROOT / "CHECKSUMS.sha256"
    assert chk.exists()
    lines = [l.strip() for l in chk.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) >= 35
    for line in lines:
        expected, rel = line.split(None, 1)
        target = ROOT / rel
        assert target.exists(), f"Missing hashed file: {rel}"
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        assert actual == expected, f"SHA-256 mismatch for {rel}"
