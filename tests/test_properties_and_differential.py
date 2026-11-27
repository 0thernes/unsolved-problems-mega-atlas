# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Deep Verification Ladder Test Suite (Build Standard B03, B06, B07, B08, B10, B11, B12, B14, B20, A08, A24, A43):
  - B03: Determinism / repeatability
  - B06: Negative boundary & error handling (MCP, RAG, JSON Schema)
  - B07: Named regression tests for every historical defect
  - B08: Golden snapshot verification (103-theorem Lean axioms + Top-10 rankings)
  - B10: Hypothesis property-based tests (1,000 examples per property)
  - B11/B12: 2,000-case randomized + 2,000-row exhaustive differential audit vs. 50-digit Decimal oracle
  - B14: Metamorphic tests (shuffling invariance, filter subsetting, age saturation plateau)
  - B20: Floating-point precision & rounding edge checks
  - A08: Single-source version consistency across all manifests
  - A24: Zero git-tracked files >= 5 MB
  - A43: Runnable example smoke test
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

import jsonschema
import networkx as nx
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))
sys.path.insert(0, str(ROOT / "reference"))

from query import compare_two_problems, search_atlas  # noqa: E402
from scoring_oracle import (  # noqa: E402
    oracle_css_score,
    oracle_era,
    oracle_leverage,
    oracle_margin_role,
    oracle_quadrant,
    oracle_titan_index,
)
from v2_loader import (  # noqa: E402
    ATLAS_VERSION,
    EXPLICIT_DUPLICATE_ALIASES,
    classify_margin_role,
    classify_quadrant,
    compute_css_score,
    compute_epistemic_spectrum,
    load_v2_master,
)
from v2_schema import compute_era  # noqa: E402


@pytest.fixture(scope="module")
def master_data():
    return load_v2_master()


# ==================== B03: DETERMINISM & REPEATABILITY ====================


def test_b03_loader_deterministic_repeatability(master_data):
    d2 = load_v2_master()
    assert master_data["df"].equals(d2["df"]), "load_v2_master() DataFrame is non-deterministic!"
    assert sorted(master_data["G"].edges()) == sorted(d2["G"].edges())
    assert master_data["summary_stats"] == d2["summary_stats"]


# ==================== B06: NEGATIVE & BOUNDARY TESTS ====================


def test_b06_mcp_malformed_json_unknown_tool_and_missing_id():
    payload = "\n".join([
        "{this is not valid json",
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "nonexistent/method", "params": {}}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "no_such_tool", "arguments": {}}}),
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_problem", "arguments": {"problem_id": "FAKE-9999"}}}),
        json.dumps({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_top_ranked", "arguments": {"metric": "DROP TABLE problems"}}}),
    ]) + "\n"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(ln) for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(resps) == 5
    assert resps[0]["error"]["code"] == -32700
    assert resps[1]["error"]["code"] == -32601
    assert resps[2]["result"]["isError"] is True
    assert resps[3]["result"]["isError"] is True
    assert resps[4]["result"]["isError"] is True


def test_b06_schema_rejects_corrupted_records(master_data):
    schema = json.loads((ROOT / "schema" / "problem.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    valid_rec = dict(master_data["df"].iloc[0].to_dict())

    bad_diff = dict(valid_rec, difficulty_score=11)
    assert list(validator.iter_errors(bad_diff)), "Schema failed to reject difficulty_score=11"

    bad_flag = dict(valid_rec, verification_flag="invented-flag")
    assert list(validator.iter_errors(bad_flag)), "Schema failed to reject unknown verification_flag"

    extra_field = dict(valid_rec, unexpected_extra_key="should-fail")
    assert list(validator.iter_errors(extra_field)), "Schema failed to reject additionalProperties"


def test_b06_compare_unknown_problem_raises():
    with pytest.raises(ValueError, match="Unknown problem ID"):
        compare_two_problems("NT-001", "DOES-NOT-EXIST-999")


# ==================== B07: NAMED REGRESSION TESTS ====================


def test_b07_regression_dangling_links_zero(master_data):
    """Regression guard for v2.2.0 defect: 10 dangling raw_links across m01..m10."""
    assert master_data["summary_stats"]["unresolved_raw_links_count"] == 0


def test_b07_regression_articulation_point_geom038(master_data):
    """Regression guard for v2.2.0 defect: GEOM-038 articulation point disconnecting leaf nodes."""
    G = master_data["G"]
    assert "GEOM-038" in G
    assert list(nx.articulation_points(G)) == []
    assert list(nx.bridges(G)) == []
    assert nx.is_biconnected(G)


def test_b07_regression_cross_field_duplicates_merged(master_data):
    """Regression guard for v2.2.0 defect: 12 cross-field near-duplicates must redirect cleanly."""
    ids = set(master_data["df"]["id"])
    for sec, canon in EXPLICIT_DUPLICATE_ALIASES.items():
        assert sec not in ids and canon in ids


def test_b07_regression_rag_cm001_and_log001():
    """Regression guard for v2.2.0 RAG misses on CM-001 and LOG-001."""
    r_cm = search_atlas(query="high temperature superconductivity room temperature", top=5, hops=0)
    r_log = search_atlas(query="continuum hypothesis zfc cardinal", top=5, hops=0)
    assert r_cm["results"][0]["id"] == "CM-001"
    assert r_log["results"][0]["id"] == "LOG-001"


# ==================== B08: GOLDEN SNAPSHOT TESTS ====================


def test_b08_golden_lean_axioms_103_theorems():
    ax_path = ROOT / "results" / "lean_axioms.txt"
    assert ax_path.exists()
    txt = ax_path.read_text(encoding="utf-8")
    lines = [ln for ln in txt.splitlines() if ln.strip()]
    assert len(lines) == 103
    for forbidden in ("sorryAx", "Classical.choice", "Lean.ofReduceBool", "Lean.trustCompiler"):
        assert forbidden not in txt


def test_b08_golden_top10_css_snapshot(master_data):
    df = master_data["df"].sort_values(["css_score", "titan_index", "graph_degree", "id"], ascending=[False, False, False, True])
    actual_top10 = [
        {"id": r.id, "css_score": float(r.css_score), "titan_index": float(r.titan_index)}
        for r in df.head(10).itertuples()
    ]
    golden_path = ROOT / "tests" / "golden" / "top10_css_titan.json"
    if not golden_path.exists():
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(json.dumps(actual_top10, indent=2) + "\n", encoding="utf-8", newline="\n")
    expected_top10 = json.loads(golden_path.read_text(encoding="utf-8"))
    assert actual_top10 == expected_top10


# ==================== B10: HYPOTHESIS PROPERTY TESTS (1,000 EXAMPLES) ====================


@settings(max_examples=1000, deadline=None)
@given(
    diff=st.integers(min_value=1, max_value=10),
    impact=st.integers(min_value=1, max_value=10),
    degree=st.integers(min_value=0, max_value=500),
    age=st.integers(min_value=0, max_value=3000),
    tract=st.integers(min_value=1, max_value=10),
)
def test_b10_hypothesis_css_bounds_monotonicity_and_oracle(diff, impact, degree, age, tract):
    score = compute_css_score(diff, impact, degree, age, tract)
    assert 0.0 <= score <= 100.0
    assert abs(score - oracle_css_score(diff, impact, degree, age, tract)) <= 0.01
    if diff < 10:
        assert compute_css_score(diff + 1, impact, degree, age, tract) > score
    if tract < 10:
        assert compute_css_score(diff, impact, degree, age, tract + 1) < score
    if age >= 300:
        assert compute_css_score(diff, impact, degree, age, tract) == compute_css_score(diff, impact, degree, 300, tract)


@settings(max_examples=1000, deadline=None)
@given(
    impact=st.integers(min_value=1, max_value=10),
    tract=st.integers(min_value=1, max_value=10),
)
def test_b10_hypothesis_quadrants_and_q1_leverage_floor(impact, tract):
    q = classify_quadrant(impact, tract)
    assert q == oracle_quadrant(impact, tract)
    lev = oracle_leverage(impact, tract)
    assert 0.1 <= lev <= 10.0
    if q.startswith("Q1:"):
        assert lev >= 5.6


@settings(max_examples=1000, deadline=None)
@given(
    adj=st.integers(min_value=0, max_value=7),
    cross_sd=st.integers(min_value=0, max_value=50),
    ratio=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
)
def test_b10_hypothesis_margin_role_and_spectrum(adj, cross_sd, ratio):
    role = classify_margin_role(adj, cross_sd, ratio)
    assert role == oracle_margin_role(adj, cross_sd, ratio)
    assert (role == "Apex Multi-Pillar Keystone (3+ Adjacent Pillars)") == (adj >= 3)


@settings(max_examples=1000, deadline=None)
@given(y1=st.integers(min_value=-3000, max_value=2026), y2=st.integers(min_value=-3000, max_value=2026))
def test_b10_hypothesis_era_monotonicity(y1, y2):
    order = [
        "Antiquity (<500 CE)",
        "Early Modern (500-1799)",
        "19th Century (1800-1899)",
        "Early-Mid 20th C. (1900-1969)",
        "Late 20th C. (1970-1999)",
        "21st Century (2000-2026)",
    ]
    e1, e2 = compute_era(y1), compute_era(y2)
    assert e1 == oracle_era(y1) and e2 == oracle_era(y2)
    if y1 <= y2:
        assert order.index(e1) <= order.index(e2)


# ==================== B11 / B12 / B20: DIFFERENTIAL & NUMERIC EDGE TESTS ====================


def test_b11_b12_differential_2000_randomized_and_all_1900_rows(master_data):
    rng = random.Random(20261125)
    for _ in range(2000):
        d = rng.randint(1, 10)
        imp = rng.randint(1, 10)
        inter = rng.randint(1, 10)
        deg = rng.randint(0, 250)
        age = rng.randint(0, 2600)
        tr = rng.randint(1, 10)
        assert abs(compute_css_score(d, imp, deg, age, tr) - oracle_css_score(d, imp, deg, age, tr)) <= 0.01
        assert abs(oracle_titan_index(d, imp, inter, deg) - round(
            0.35 * d + 0.35 * imp + 0.20 * inter + 0.10 * min(10.0, float(__import__("math").log1p(deg) * 2.5)), 2
        )) <= 0.01

    for r in master_data["df"].itertuples():
        ref_css = oracle_css_score(r.difficulty_score, r.civilizational_impact, r.graph_degree, r.age_years_2026, r.tractability_2050)
        ref_tit = oracle_titan_index(r.difficulty_score, r.civilizational_impact, r.interdisciplinarity_index, r.graph_degree)
        ref_lev = oracle_leverage(r.civilizational_impact, r.tractability_2050)
        assert abs(r.css_score - ref_css) <= 0.01, f"CSS oracle drift on {r.id}"
        assert abs(r.titan_index - ref_tit) <= 0.01, f"Titan oracle drift on {r.id}"
        assert abs(r.near_term_leverage_score - ref_lev) <= 1e-9, f"Leverage drift on {r.id}"
        assert r.strategic_quadrant == oracle_quadrant(r.civilizational_impact, r.tractability_2050)
        assert r.era == oracle_era(r.year_formulated)
        assert r.margin_role == oracle_margin_role(r.adjacent_pillars_count, r.cross_superdomain_links, r.bridge_margin_ratio)


def test_b20_epistemic_spectrum_clamping_edges():
    assert compute_epistemic_spectrum("Formal-Deductive", "Formal Mathematical Proof") == 4.0
    assert compute_epistemic_spectrum("Normative-Philosophical", "Philosophical / Reflective Consensus") == 100.0
    assert 0.0 <= compute_epistemic_spectrum("Unknown", "Unknown") <= 100.0


# ==================== B14: METAMORPHIC INVARIANCE TESTS ====================


def test_b14_metamorphic_rag_pillar_filter_subsetting():
    unfiltered = search_atlas(query="quantum gravity", top=20, hops=0)
    filtered = search_atlas(query="quantum gravity", pillar="Fundamental Physics & Cosmos", top=20, hops=0)
    assert filtered["count"] >= 1
    assert all(r["macro_pillar"] == "Fundamental Physics & Cosmos" for r in filtered["results"])
    assert filtered["count"] <= unfiltered["count"] + 5


def test_b14_metamorphic_dataframe_shuffle_preserves_aggregates(master_data):
    df = master_data["df"]
    shuf = df.sample(frac=1.0, random_state=99)
    assert round(float(df["css_score"].mean()), 6) == round(float(shuf["css_score"].mean()), 6)
    assert round(float(df["titan_index"].mean()), 6) == round(float(shuf["titan_index"].mean()), 6)
    assert int(df["graph_degree"].sum()) == int(shuf["graph_degree"].sum())


# ==================== A08 / A24 / A43: GOVERNANCE, HYGIENE & EXAMPLES ====================


def test_a08_version_consistency_across_all_manifests():
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert ATLAS_VERSION == ver
    assert f'version = "{ver}"' in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version: "{ver}"' in (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))["version"] == ver
    assert f'version = "{ver}"' in (ROOT / "lean" / "lakefile.toml").read_text(encoding="utf-8")
    assert f'version: "{ver}"' in (ROOT / "repo.yaml").read_text(encoding="utf-8")
    assert f"## [{ver}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_a24_all_git_tracked_files_under_5mb():
    proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    oversized = []
    for rel in proc.stdout.splitlines():
        p = ROOT / rel
        if p.exists() and p.stat().st_size >= 5 * 1024 * 1024:
            oversized.append((rel, round(p.stat().st_size / 1048576, 2)))
    assert not oversized, f"Tracked files >= 5 MB violate Build Standard A24: {oversized}"


def test_a43_runnable_quickstart_example_smoke():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "examples" / "quickstart_demo.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    assert "Reference Oracle parity check on NT-001" in proc.stdout
    assert "(PASS)" in proc.stdout


def test_legal_identity_cure_no_fake_llc_in_code_or_metadata():
    checked_roots = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "LICENSE",
        ROOT / "LICENSE-CODE",
        ROOT / "NOTICE",
        ROOT / "CITATION.cff",
        ROOT / "CITATION.bib",
        ROOT / ".zenodo.json",
        ROOT / "croissant.json",
        ROOT / "ro-crate-metadata.json",
        ROOT / "repo.yaml",
        ROOT / "paper" / "main.tex",
        ROOT / "src" / "v2_loader.py",
        ROOT / "src" / "v2_export_all.py",
        ROOT / "mcp_server" / "server.py",
    ]
    hits = [str(p.relative_to(ROOT)) for p in checked_roots if p.exists() and re.search(r"0thernes\s+LLC", p.read_text(encoding="utf-8"), re.I)]
    assert not hits, f"Legacy '0thernes LLC' still present in: {hits}"


# ==================== 8. HOSTILE-REFEREE REGRESSION GUARDS (V2.5.0) ====================


def test_b07_regression_claims_md_and_paper_tex_id_parity():
    """Ensure CLAIMS.md and paper/main.tex Table 1 declare the exact same C1..C10 claim IDs."""
    claims_txt = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
    tex_txt = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
    md_ids = re.findall(r"^\|\s*\*\*(C\d+)\*\*\s*\|", claims_txt, flags=re.M)
    tex_ids = re.findall(r"^(C\d+)\s*&\s*\\tag", tex_txt, flags=re.M)
    assert md_ids == [f"C{i}" for i in range(1, 11)]
    assert tex_ids == md_ids, f"Claim ID drift: CLAIMS.md={md_ids} vs paper/main.tex={tex_ids}"


def test_b07_regression_paper_autoresearch_matches_results_tsv():
    """Ensure paper/main.tex cites exact autoresearch/results.tsv baseline/discarded/kept figures."""
    tsv = (ROOT / "autoresearch" / "results.tsv").read_text(encoding="utf-8")
    tex = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
    assert "80.26\t89.33\t21/25" in tsv
    assert "H-001:" in tsv and "\tdiscard\t" in tsv
    assert "89.33\\%" in tex and "80.26" in tex and "97.99" in tex
    assert "82.22" not in tex and "91.69" not in tex


def test_b07_regression_no_stale_v23_or_72_in_active_docs():
    """Ensure top-level active docs do not regress to stale v2.3.0 / 72-theorem / 9-tool / MIT claims."""
    active_docs = [
        "README.md",
        "ARCHITECTURE.md",
        "CLAIMS.md",
        "VERIFICATION.md",
        "docs/WHITE_PAPER.md",
        "docs/architecture.md",
        "lean/README.md",
        "mcp_server/README.md",
    ]
    stale = [
        re.compile(r"\b72\s+(?:Pure\s+)?Lean|\b72\s+audited|\b72\s+theorems", re.I),
        re.compile(r"\b9-tool\b", re.I),
        re.compile(r"\b14-sheet\b", re.I),
        re.compile(r"V2\.3\.0|v2\.3\.0"),
    ]
    hits = []
    for rel in active_docs:
        txt = (ROOT / rel).read_text(encoding="utf-8")
        for rx in stale:
            if rx.search(txt):
                hits.append((rel, rx.pattern))
    assert not hits, f"Stale metrics found in active docs: {hits}"


def test_b07_regression_all_code_lean_sh_have_spdx_headers():
    """Verify 100% REUSE/SPDX header coverage across all tracked .py, .lean, and .sh files (except immutable evaluate.py)."""
    proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    missing = []
    for rel in proc.stdout.splitlines():
        if rel == "autoresearch/evaluate.py":
            continue
        p = ROOT / rel
        if p.suffix in {".py", ".lean", ".sh"} and p.exists():
            head = "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[:5])
            if "SPDX-License-Identifier" not in head:
                missing.append(rel)
    assert not missing, f"Files missing SPDX-License-Identifier header: {missing}"


def test_b07_regression_benchmark_doc_matches_actual_html_size():
    """Verify docs/benchmarks.md reports an honest size ceiling >= actual HTML dashboard size."""
    html_mb = (ROOT / "outputs" / "MegaAtlas_Interactive_Dashboard_V2.html").stat().st_size / 1048576.0
    bench_md = (ROOT / "docs" / "benchmarks.md").read_text(encoding="utf-8")
    assert html_mb < 4.0, f"Dashboard exceeded 4.0 MB budget: {html_mb:.2f} MB"
    assert "< 3.5 MB" not in bench_md, "Stale inaccurate '< 3.5 MB' claim in docs/benchmarks.md"


def test_b07_regression_lean_adversarial_refutations_and_103_axioms():
    """Verify AdversarialTests.lean (Playbook Item 12) and exact 103-line constructive results/lean_axioms.txt."""
    adv = ROOT / "lean" / "MegaAtlasProofs" / "AdversarialTests.lean"
    assert adv.exists()
    axioms = (ROOT / "results" / "lean_axioms.txt").read_text(encoding="utf-8").splitlines()
    non_empty = [ln for ln in axioms if ln.strip()]
    assert len(non_empty) == 103
    assert any("MegaAtlasProofs.Palomar.m8_adversarial_refutations" in ln for ln in non_empty)
    for bad in ("sorryAx", "Classical.choice", "Lean.ofReduceBool", "_native"):
        assert all(bad not in ln for ln in non_empty), f"Forbidden axiom {bad} in results/lean_axioms.txt"


# ==================== 9. ROUND 3 HOSTILE-REFEREE REGRESSION GUARDS (V2.6.0) ====================


def test_b06_mcp_clamps_top_hops_and_validates_missing_args():
    """Verify MCP server clamps top/hops within schema bounds and rejects missing required args cleanly."""
    payload = "\n".join([
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "Riemann", "top": 9999, "hops": 99}}}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "Riemann", "top": -5, "hops": -2}}}),
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_problem", "arguments": {}}}),
        json.dumps({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "compare_problems", "arguments": {"id_a": "NT-001"}}}),
    ]) + "\n"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(ln) for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(resps) == 4
    r1 = json.loads(resps[0]["result"]["content"][0]["text"])
    assert resps[0]["result"]["isError"] is False
    assert 1 <= r1["count"] <= 50
    r2 = json.loads(resps[1]["result"]["content"][0]["text"])
    assert resps[1]["result"]["isError"] is False
    assert r2["count"] == 1
    assert resps[2]["result"]["isError"] is True
    assert "problem_id" in resps[2]["result"]["content"][0]["text"]
    assert resps[3]["result"]["isError"] is True
    assert "id_a" in resps[3]["result"]["content"][0]["text"]


def test_b07_regression_rag_auto_rebuilds_stale_sqlite_version(tmp_path):
    """Verify ensure_sqlite_db() detects a stale cached SQLite version and rebuilds automatically."""
    import sqlite3
    from query import ensure_sqlite_db

    stale_db = tmp_path / "stale_atlas.sqlite"
    conn = sqlite3.connect(str(stale_db))
    conn.execute("CREATE TABLE metadata (key TEXT, value TEXT)")
    conn.execute("INSERT INTO metadata VALUES ('atlas_version', '0.0.1-stale')")
    conn.commit()
    conn.close()

    ensure_sqlite_db(stale_db)
    conn2 = sqlite3.connect(str(stale_db))
    try:
        ver = conn2.execute("SELECT value FROM metadata WHERE key = 'atlas_version'").fetchone()[0]
        cnt = conn2.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        auth = conn2.execute("SELECT COUNT(*) FROM author_frontier_contributions").fetchone()[0]
        assert ver == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        assert cnt == 2000
        assert auth == 20
    finally:
        conn2.close()


def test_b07_regression_security_md_self_consistent():
    """Ensure SECURITY.md supported minor branch matches active VERSION without contradicting itself."""
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    major_minor = ".".join(ver.split(".")[:2])
    sec = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert f"`{major_minor}.x`" in sec and f"`< {ver}`" in sec
    assert "`2.4.x`" not in sec


def test_b07_regression_formalization_yaml_matches_lean_axioms():
    """Verify every Palomar theorem axiom list in lean/formalization.yaml matches results/lean_axioms.txt verbatim."""
    ax_map: dict[str, list[str]] = {}
    for ln in (ROOT / "results" / "lean_axioms.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", ln.strip())
        if m:
            ax_map[m.group(1)] = [tok.strip() for tok in m.group(2).split(",") if tok.strip()]
    fy = (ROOT / "lean" / "formalization.yaml").read_text(encoding="utf-8")
    blocks = re.findall(r'declaration:\s*"([^"]+)".*?axioms:\s*\[([^\]]*)\]', fy, flags=re.S)
    assert len(blocks) == 9
    for decl, raw_ax in blocks:
        declared = [tok.strip().strip('"').strip("'") for tok in raw_ax.split(",") if tok.strip()]
        assert decl in ax_map, f"Missing declaration {decl} in results/lean_axioms.txt"
        assert declared == ax_map[decl], f"formalization.yaml drift on {decl}: {declared} != {ax_map[decl]}"


def test_b07_regression_no_private_local_paths_in_tracked_files():
    """Ensure zero tracked documentation or code files leak private local drive/user paths."""
    proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    rx = re.compile(r"[A-Z]:\\(?:Users\\Alexa|unsolved-problems|temp_mega_atlas|\[Vibe Coded)", re.I)
    hits = []
    for rel in proc.stdout.splitlines():
        if rel.startswith("outputs/") or rel.startswith("dist/") or rel.endswith((".png", ".svg", ".pdf", ".gz", ".xlsx", ".xls", ".tsr")):
            continue
        if rel == "tests/test_properties_and_differential.py":
            continue
        p = ROOT / rel
        if p.exists() and rx.search(p.read_text(encoding="utf-8", errors="ignore")):
            hits.append(rel)
    assert not hits, f"Private workstation paths leaked in tracked files: {hits}"


def test_b07_regression_no_stale_counts_or_bare_comparator_in_active_docs():
    """Prevent regressions to stale 92-theorem, 7-preprint, 18-row, or bare lake-comparator instructions."""
    active = [
        "README.md", "AGENTS.md", "CLAIMS.md", "VERIFICATION.md", "EVIDENCE.md",
        "LIMITATIONS.md", "PHILOSOPHY.md", "ARCHITECTURE.md", "llms.txt",
        "docs/WHITE_PAPER.md", "docs/METHODOLOGY.md", "docs/faq.md", "docs/glossary.md",
        "docs/threat-model.md", "docs/operations.md", "lean/README.md", "mcp_server/README.md",
        "mcp_server/server.py", "lean/formalization.yaml",
    ]
    stale = [
        re.compile(r"\b92\s+(?:Pure\s+)?(?:Lean|audited|theorems|axioms)|lean_theorems=92", re.I),
        re.compile(r"\b(?:7|seven)\s+(?:companion|author-curated|scoped)", re.I),
        re.compile(r"\b18-row\b", re.I),
        re.compile(r"lake comparator --config comparator\.json --paranoid"),
    ]
    hits = []
    for rel in active:
        txt = (ROOT / rel).read_text(encoding="utf-8")
        for rx in stale:
            if rx.search(txt):
                hits.append((rel, rx.pattern))
    assert not hits, f"Stale metrics/commands in active files: {hits}"


def test_b07_regression_statement_fidelity_19_rows_and_symbols_valid():
    """Ensure docs/statement-fidelity.md has 19 rows and every file::symbol anchor resolves in source."""
    txt = (ROOT / "docs" / "statement-fidelity.md").read_text(encoding="utf-8")
    rows = [ln for ln in txt.splitlines() if ln.startswith("| ") and ln.split("|")[1].strip().isdigit()]
    assert len(rows) == 19
    for rel, sym in re.findall(r"`([a-zA-Z0-9_./-]+\.py)::([a-zA-Z0-9_]+)`", txt):
        src_p = ROOT / rel
        assert src_p.exists(), f"Missing file cited in statement-fidelity.md: {rel}"
        src_txt = src_p.read_text(encoding="utf-8")
        assert re.search(rf"\b(?:def\s+)?{re.escape(sym)}\b", src_txt), f"Missing symbol {sym} in {rel}"


def test_b07_regression_live_negative_lean_kernel_rejection(tmp_path):
    """Playbook Item 12: when Lean is installed, prove the active kernel rejects a deliberately false theorem."""
    import shutil

    lake_exe = Path.home() / ".elan" / "bin" / ("lake.exe" if sys.platform == "win32" else "lake")
    lake_bin = str(lake_exe) if lake_exe.exists() else shutil.which("lake")
    if not lake_bin:
        pytest.skip("Lean 4 / lake not installed on this runner")
    try:
        probe = subprocess.run([lake_bin, "--version"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        pytest.skip("Lean 4 / lake not installed on this runner")
    if probe.returncode != 0:
        pytest.skip("Lean 4 / lake not installed on this runner")
    neg = tmp_path / "NegativeKernelTest.lean"
    neg.write_text(
        "import MegaAtlasProofs.Scoring\n"
        "theorem deliberately_false_css : MegaAtlasProofs.Scoring.cssBps 100 100 100 0 = 9999 := by\n"
        "  rfl\n",
        encoding="utf-8",
        newline="\n",
    )
    res = subprocess.run([lake_bin, "env", "lean", str(neg)], cwd=ROOT / "lean", capture_output=True, text=True, check=False)
    assert res.returncode != 0, "CRITICAL: Lean 4 kernel accepted a deliberately false theorem!"


def test_b07_regression_digicert_rfc3161_tsr_present_and_binds_checksums():
    """Playbook Item 26: verify CHECKSUMS.sha256.tsr exists and cryptographically embeds SHA256(CHECKSUMS.sha256)."""
    import hashlib

    tsr_path = ROOT / "CHECKSUMS.sha256.tsr"
    chk_path = ROOT / "CHECKSUMS.sha256"
    assert tsr_path.exists() and tsr_path.stat().st_size > 200, "Missing or empty CHECKSUMS.sha256.tsr"
    tsr_bytes = tsr_path.read_bytes()
    assert tsr_bytes[0] == 0x30, "CHECKSUMS.sha256.tsr is not a valid DER ASN.1 SEQUENCE"
    expected_digest = hashlib.sha256(chk_path.read_bytes()).digest()
    assert expected_digest in tsr_bytes, "CHECKSUMS.sha256.tsr messageImprint does not match current CHECKSUMS.sha256!"


def test_b07_regression_wcag_all_6_tabpanels_and_dialogs():
    """Verify WCAG 2.2 AA ARIA roles on all 6 tabpanels and both modal dialogs in Interactive HTML."""
    html_txt = (ROOT / "outputs" / "MegaAtlas_Interactive_Dashboard_V2.html").read_text(encoding="utf-8")
    assert html_txt.count('role="tabpanel"') == 6
    assert html_txt.count('role="dialog" aria-modal="true"') == 2


def test_b06_mcp_rejects_negative_oversized_content_length_and_bool_args():
    """Verify MCP server blocks negative/oversized Content-Length DoS frames and rejects bool integers."""
    framed = (
        b"Content-Length: -1\r\n\r\n"
        b"Content-Length: 99999999\r\n\r\n"
    )
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=framed,
        capture_output=True,
        timeout=30,
        check=True,
    )
    assert proc.stdout.count(b'"code": -32700') == 2

    reqs = [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "Riemann", "top": True}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "x" * 5000}}},
    ]
    proc2 = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input="\n".join(json.dumps(r) for r in reqs) + "\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(line) for line in proc2.stdout.splitlines() if line.strip()]
    assert len(resps) == 2
    assert resps[0]["result"]["isError"] is True and "integer" in resps[0]["result"]["content"][0]["text"]
    assert resps[1]["result"]["isError"] is True and "4096" in resps[1]["result"]["content"][0]["text"]


def test_b07_regression_search_and_compare_auto_rebuild_stale_default_db(tmp_path, monkeypatch):
    """Verify search_atlas() and compare_two_problems() catch a stale existing DEFAULT_DB and auto-rebuild."""
    import sqlite3
    import query as qmod

    stale_db = tmp_path / "default_stale.sqlite"
    conn = sqlite3.connect(str(stale_db))
    conn.execute("CREATE TABLE metadata (key TEXT, value TEXT)")
    conn.execute("INSERT INTO metadata VALUES ('atlas_version', '0.0.1-stale')")
    conn.commit()
    conn.close()

    monkeypatch.setattr(qmod, "DEFAULT_DB", stale_db)
    res = qmod.search_atlas(problem_id="NT-001", hops=0, db_path=stale_db)
    assert res["count"] == 1 and res["results"][0]["id"] == "NT-001"
    comp = qmod.compare_two_problems("NT-001", "CS-001", db_path=stale_db)
    assert comp["problem_a"]["id"] == "NT-001" and comp["problem_b"]["id"] == "CS-001"


def test_b07_regression_opentimestamps_ots_present_and_binds_checksums():
    """Playbook Item 26: verify CHECKSUMS.sha256.ots exists and binds SHA256(CHECKSUMS.sha256) with OTS calendars."""
    import hashlib

    ots_path = ROOT / "CHECKSUMS.sha256.ots"
    chk_path = ROOT / "CHECKSUMS.sha256"
    assert ots_path.exists() and ots_path.stat().st_size > 100, "Missing or truncated CHECKSUMS.sha256.ots"
    ots_bytes = ots_path.read_bytes()
    magic = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94\x01\x08"
    expected_digest = hashlib.sha256(chk_path.read_bytes()).digest()
    assert ots_bytes.startswith(magic + expected_digest), "CHECKSUMS.sha256.ots does not bind current CHECKSUMS.sha256!"
    assert b"https://" in ots_bytes, "CHECKSUMS.sha256.ots missing OpenTimestamps calendar URIs"


def test_b07_regression_strict_csp_on_dashboard_and_blueprint_html():
    """Verify both GitHub Pages HTML apps enforce strict zero-CDN Content-Security-Policy & Referrer-Policy."""
    for rel in ("outputs/MegaAtlas_Interactive_Dashboard_V2.html", "blueprint/index.html"):
        txt = (ROOT / rel).read_text(encoding="utf-8")
        assert 'http-equiv="Content-Security-Policy"' in txt, f"Missing CSP header in {rel}"
        assert "default-src 'none'" in txt, f"Weak CSP in {rel}"
        assert 'name="referrer" content="no-referrer"' in txt, f"Missing Referrer-Policy in {rel}"
    bp = (ROOT / "blueprint" / "index.html").read_text(encoding="utf-8")
    assert 'class="skip-link"' in bp and '<main id="main">' in bp


def test_b07_regression_zero_crlf_and_zero_bom_in_tracked_text_files():
    """Enforce .gitattributes LF-only & zero-BOM hygiene across all tracked non-output text files."""
    proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    text_exts = {".py", ".lean", ".md", ".tex", ".bib", ".yml", ".yaml", ".json", ".toml", ".sh", ".ps1", ".html", ".txt", ".tsv", ".csv", ".cff"}
    bad_crlf, bad_bom = [], []
    for rel in proc.stdout.splitlines():
        if rel.startswith("outputs/"):
            continue
        p = ROOT / rel
        if not p.exists() or p.suffix.lower() not in text_exts:
            continue
        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            bad_bom.append(rel)
        if b"\r\n" in raw:
            bad_crlf.append(rel)
    assert not bad_bom, f"UTF-8 BOM detected in tracked text files: {bad_bom}"
    assert not bad_crlf, f"CRLF line endings detected in tracked text files: {bad_crlf}"


def test_b07_regression_zero_broken_relative_markdown_links():
    """Ensure every relative Markdown link across all tracked non-output .md files resolves on disk."""
    proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    broken = []
    for rel in proc.stdout.splitlines():
        if not rel.endswith(".md") or rel.startswith("outputs/"):
            continue
        p = ROOT / rel
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        txt = re.sub(r"```.*?```", "", txt, flags=re.S)
        txt = re.sub(r"`[^`\n]+`", "", txt)
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", txt):
            target = m.group(1).strip().split()[0]
            if target.startswith(("http://", "https://", "mailto:", "#", "file://")):
                continue
            rel_path = target.split("#")[0]
            if rel_path and not (p.parent / rel_path).exists():
                broken.append((rel, target))
    assert not broken, f"Broken relative markdown links detected: {broken}"


def test_b07_regression_external_registry_delta_offline_and_gate_parser():
    """Verify external registry delta sync works offline across all 16 trackers + 25 Left to Solve fronts and detects gates honestly."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import sync_external_registries as ser

    rep = ser.build_delta_report(live=False)
    assert rep["mode"] == "offline"
    assert rep["committed_registries_indexed"] == 16
    assert len(rep["registries"]) == 16
    assert len(rep["lefttosolve_programs"]) == 25

    t_by_key = {t["key"]: t for t in ser.TARGETS}
    gated = ser.parse_registry_html(t_by_key["clay_millennium"], "<html><title>Just a moment...</title><body>Verify you are human</body></html>", 403)
    assert gated["fetch_status"] == "js_rendered_or_gated"
    clean = ser.parse_registry_html(t_by_key["erdos_problems"], "<html><title>Erdos Problems</title><body>" + ("x " * 100) + "1221 problems tracked.</body></html>", 200)
    assert clean["fetch_status"] == "live_checked"
    assert any("1221 problems" in s for s in clean["extracted_signals"])

    sample_lts_html = (
        '<a href="/programs/Open%20Quantum%20Problems"><span>2 live</span> Open Quantum Problems 32 targets · 32 open · 0 solved here</a>'
        '<a href="/programs/Green&#x27;s%20100%20Open%20Problems">Green&#x27;s 100 Open Problems 285 targets · 128 open · 112 solved here</a>'
    )
    parsed_progs = ser.parse_lefttosolve_programs_html(sample_lts_html)
    assert len(parsed_progs) == 2
    by_name = {p["program"]: p for p in parsed_progs}
    assert by_name["Open Quantum Problems"]["targets"] == 32 and by_name["Open Quantum Problems"]["live_agents"] == 2
    assert by_name["Green's 100 Open Problems"]["url"] == "https://lefttosolve.com/programs/Green%27s%20100%20Open%20Problems"
    assert "&#x27;" not in by_name["Green's 100 Open Problems"]["url"]

    assert (ROOT / "docs" / "registry-delta-2026-11-26.md").exists()
    assert (ROOT / "results" / "registry_delta.json").exists()
    assert (ROOT / "results" / "daily_registries.json").exists()
    assert (ROOT / "results" / "lefttosolve_programs.json").exists()
    assert (ROOT / "docs" / "DAILY_REGISTRY_TRACKER.md").exists()


def test_b07_regression_track_b_collatz_pilot_reproducible():
    """Verify Track B NT-005 Collatz parity probe RESULTS.json and live Terras bijection."""
    res_path = ROOT / "research" / "runs" / "NT-005_collatz_parity_pilot" / "RESULTS.json"
    assert res_path.exists()
    data = json.loads(res_path.read_text(encoding="utf-8"))
    assert data["problem_id"] == "NT-005"
    assert "OPEN" in data["epistemic_status"]
    assert data["sweep_range"]["max_n"] == 100_000
    assert data["sweep_range"]["all_converged_to_1"] is True
    assert data["sweep_records"]["longest_stopping_time"]["n"] == 77031
    assert data["sweep_records"]["longest_stopping_time"]["steps"] == 350
    assert data["sweep_records"]["highest_peak_value"]["n"] == 77671
    assert data["sweep_records"]["highest_peak_value"]["peak"] == 1570824736
    assert len(data["terras_parity_bijection_k1_to_k12"]) == 12
    assert all(row["is_bijection"] for row in data["terras_parity_bijection_k1_to_k12"])

    sys.path.insert(0, str(ROOT / "research" / "runs" / "NT-005_collatz_parity_pilot"))
    import collatz_probe as cp

    assert cp.collatz_stats(27)["steps"] == 111
    assert cp.compressed_parity_vector(27, 8) == 0b11111011
    assert all(row["is_bijection"] for row in cp.verify_terras_bijection(6))


def test_b07_regression_track_b_ramsey_witnesses_reproducible():
    """Verify Track B COMB-002 Ramsey constructive witness RESULTS.json & live re-check of P_17 and C_24."""
    res_path = ROOT / "research" / "runs" / "COMB-002_ramsey_witness_pilot" / "RESULTS.json"
    assert res_path.exists()
    data = json.loads(res_path.read_text(encoding="utf-8"))
    assert data["problem_id"] == "COMB-002"
    assert "OPEN" in data["epistemic_status"]
    assert data["witnesses_certified_count"] == 7
    bounds = {w["lower_bound_proved"] for w in data["witnesses"]}
    assert {"R(3,3) > 5", "R(4,4) > 17", "R(4,5) > 24", "R(5,5) > 37", "R(6,6) > 101"}.issubset(bounds)
    assert all(w["certified"] and w["cyclic_automorphism_verified"] for w in data["witnesses"])

    sys.path.insert(0, str(ROOT / "research" / "runs" / "COMB-002_ramsey_witness_pilot"))
    import ramsey_probe as rp

    c24 = rp.circulant_adj(24, (1, 2, 4, 8, 9))
    assert rp.verify_cyclic_automorphism_and_symmetry(c24)
    assert not rp.has_clique_full(c24, 4)
    assert not rp.has_clique_full(rp.complement_adj(c24), 5)


def test_b07_regression_rubric_override_identity_and_sensitivity_diff():
    """Verify rubric_override_diff.py gives exact rho=1.0 on default weights and measurable sensitivity on sample override."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import rubric_override_diff as rod

    ident = rod.evaluate_rubric_override(css_weights=(0.40, 0.30, 0.20, 0.10), problem_overrides={})
    assert ident["rank_correlation"]["spearman_rho"] == 1.0
    assert ident["rank_correlation"]["kendall_tau"] == 1.0
    assert ident["rank_correlation"]["top25_jaccard_overlap"] == 1.0
    assert ident["rank_correlation"]["max_abs_rank_shift"] == 0

    sample = json.loads((ROOT / "examples" / "rubric_override_sample.json").read_text(encoding="utf-8"))
    raw_w = sample["css_weights"]
    diff = rod.evaluate_rubric_override(
        css_weights=(float(raw_w[0]), float(raw_w[1]), float(raw_w[2]), float(raw_w[3])),
        problem_overrides=sample["problem_overrides"],
        label=sample["label"],
    )
    assert diff["problems_evaluated"] == 2000
    assert diff["problem_overrides_applied"] == 3
    assert 0.5 < diff["rank_correlation"]["spearman_rho"] < 1.0
    assert diff["rank_correlation"]["max_abs_rank_shift"] > 100


def test_b06_rubric_override_rejects_invalid_weights_ids_and_ratings():
    """Negative boundary tests for rubric_override_diff.py validation."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import rubric_override_diff as rod

    with pytest.raises(ValueError, match="sum to 1.0"):
        rod.evaluate_rubric_override(css_weights=(0.5, 0.5, 0.5, 0.0))
    with pytest.raises(ValueError, match="Unknown Problem ID"):
        rod.evaluate_rubric_override(problem_overrides={"FAKE-999": {"difficulty_score": 5}})
    with pytest.raises(ValueError, match="integer in 1..10"):
        rod.evaluate_rubric_override(problem_overrides={"NT-001": {"difficulty_score": 11}})


def test_b07_regression_roadmap_no_duplicate_current_and_planned_version():
    """Ensure ROADMAP.md never lists the current shipped version again under Planned Next Releases."""
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    rm = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    assert f"**Current Release:** `v{ver}`" in rm
    planned = rm.split("## Planned Next Releases", 1)[1]
    assert f"`v{ver}`" not in planned, f"Current release v{ver} still listed under Planned Next Releases!"


# ==================== 10. V2.9.0 / V2.10.0 HOSTILE-REFEREE REGRESSION GUARDS ====================


def test_b07_regression_track_b_probe_ids_match_dataset_names(master_data):
    """Guard H-802: every Track B probe problem_id must match the actual dataset record name (no COMB-001 Ramsey mis-ID)."""
    assert not (ROOT / "research" / "runs" / "COMB-001_ramsey_witness_pilot").exists()
    name_by_id = dict(zip(master_data["df"]["id"], master_data["df"]["name"]))
    expected_keywords = {
        "LOG-002": "Busy Beaver",
        "NT-005": "Collatz",
        "COMB-002": "Ramsey",
    }
    found_ids: set[str] = set()
    for res_file in sorted((ROOT / "research" / "runs").glob("*/RESULTS.json")):
        payload = json.loads(res_file.read_text(encoding="utf-8"))
        pid = payload["problem_id"]
        found_ids.add(pid)
        assert pid in name_by_id, f"Track B probe {res_file} references nonexistent problem_id {pid}"
        assert pid in expected_keywords, f"Unexpected Track B probe ID {pid}"
        assert expected_keywords[pid].lower() in name_by_id[pid].lower(), (
            f"Track B probe {res_file} claims {pid} but dataset maps {pid} -> {name_by_id[pid]!r}"
        )
    assert found_ids == set(expected_keywords.keys())


def test_b07_regression_rag_exact_id_respects_filters():
    """Guard H-811: exact problem-ID queries must still enforce pillar, superdomain, and verification_flag filters."""
    wrong_pillar = search_atlas(query="NT-001", pillar="Life, Mind & Medicine", top=5, hops=0)
    assert wrong_pillar["count"] == 0
    right_pillar = search_atlas(query="NT-001", pillar="Pure Mathematics", top=5, hops=0)
    assert right_pillar["count"] == 1 and right_pillar["results"][0]["id"] == "NT-001"
    wrong_flag = search_atlas(query="NT-001", flag="disputed-human-claim", top=5, hops=0)
    assert wrong_flag["count"] == 0


def test_b06_mcp_rejects_non_object_json_bad_filter_and_oversized_ndjson():
    """Guard H-812: MCP stdio server rejects non-object JSON (-32600), non-string filter args, and >1 MiB NDJSON lines."""
    oversized = '{"jsonrpc":"2.0","id":9,"method":"ping","pad":"' + ("a" * (1_048_576 + 128)) + '"}'
    payload = "\n".join([
        "[1, 2, 3]",
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search_problems", "arguments": {"query": "Riemann", "pillar": 123}}}),
        oversized,
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "ping", "params": {}}),
    ]) + "\n"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(ln) for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(resps) == 4
    assert resps[0]["error"]["code"] == -32600
    assert resps[1]["result"]["isError"] is True and "string" in resps[1]["result"]["content"][0]["text"]
    assert resps[2]["error"]["code"] == -32700
    assert resps[3]["id"] == 3 and resps[3]["result"] == {}


def test_b07_regression_rubric_override_tiebreak_matches_golden_top10():
    """Guard H-810: rubric_override_diff.py baseline tie-break must match tests/golden/top10_css_titan.json verbatim."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import rubric_override_diff as rod

    golden_ids = [r["id"] for r in json.loads((ROOT / "tests" / "golden" / "top10_css_titan.json").read_text(encoding="utf-8"))]
    ident = rod.evaluate_rubric_override(css_weights=(0.40, 0.30, 0.20, 0.10), problem_overrides={})
    actual_ids = [r["id"] for r in ident["top_alt_ranked_10"]]
    assert actual_ids == golden_ids
    with pytest.raises(ValueError, match="top_movers"):
        rod.evaluate_rubric_override(top_movers=0)
    with pytest.raises(ValueError, match="top_movers"):
        rod.evaluate_rubric_override(top_movers=True)  # type: ignore[arg-type]


def test_b07_regression_no_withdrawn_rh_claim_or_false_14files_in_active_docs():
    """Guard H-801/H-805: active docs must cite primary RH/GRH verification sources (175,187 files) and never repeat the withdrawn claim."""
    checked = ["README.md", "docs/faq.md", "docs/literature-search-log.md", "paper/main.tex", "src/v2_loader.py"]
    for rel in checked:
        txt = (ROOT / rel).read_text(encoding="utf-8")
        assert "no primary source found" not in txt.lower(), f"Withdrawn RH erratum text leaked in {rel}"
        assert "(14 files)" not in txt, f"False '(14 files)' RH archive size still in {rel}"
    bib = (ROOT / "paper" / "refs.bib").read_text(encoding="utf-8")
    assert "leanprover-community.github.io/blog/posts/riemann-hypothesis/" in bib
    assert "math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/" in bib


def test_b07_regression_no_overstated_lean_kernel_or_comb001_ramsey_in_active_docs():
    """Guard H-802/H-803/H-809/H-903/H-904: active docs and paper must not overstate kernel independence, COMB-001 Ramsey, or stale MCP/test/schedule counts."""
    active = [
        "README.md", "CLAIMS.md", "VERIFICATION.md", "EVIDENCE.md", "LIMITATIONS.md",
        "ARCHITECTURE.md", "AGENTS.md", "llms.txt", "paper/main.tex", "blueprint/index.html",
        "docs/WHITE_PAPER.md", "docs/architecture.md", "docs/faq.md", "lean/README.md", "mcp_server/README.md",
    ]
    forbidden = [
        re.compile(r"six independent proof kernels|6 independent proof kernels", re.I),
        re.compile(r"COMB-001_ramsey|COMB-001.*Ramsey", re.I),
        re.compile(r"\b10-tool\s+MCP|\b12-tool\s+MCP", re.I),
        re.compile(r"\b83\s+pytest\b|\b83`?\s+automated\s+`?pytest", re.I),
        re.compile(r"07:23\s+UTC", re.I),
    ]
    hits = []
    for rel in active:
        txt = (ROOT / rel).read_text(encoding="utf-8")
        for rx in forbidden:
            if rx.search(txt):
                hits.append((rel, rx.pattern))
    assert not hits, f"Overstated or stale text found in active docs: {hits}"


def test_b07_regression_daily_sync_workflow_and_checksum_isolation():
    """Verify daily 16-registry & 25-front Left to Solve sync workflow exists and daily telemetry stays outside frozen CHECKSUMS.sha256."""
    wf = (ROOT / ".github" / "workflows" / "daily-registry-sync.yml").read_text(encoding="utf-8")
    assert 'cron: "0 6 * * *"' in wf and "--live --write-daily" in wf
    pages_wf = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert 'cron: "15 6 * * *"' in pages_wf and "daily_registries.json" in pages_wf
    chk = (ROOT / "CHECKSUMS.sha256").read_text(encoding="utf-8")
    for volatile_rel in (
        "results/daily_registries.json",
        "results/lefttosolve_programs.json",
        "results/daily_registry_history.jsonl",
        "results/lefttosolve_delta.json",
        "docs/DAILY_REGISTRY_TRACKER.md",
        "docs/lefttosolve-programs.md",
        "docs/registry-delta-latest.md",
        "data/external/lefttosolve/snapshot.json",
    ):
        assert volatile_rel not in chk, f"Volatile daily file {volatile_rel} must NOT be in release-frozen CHECKSUMS.sha256!"


def test_b07_regression_lefttosolve_100_problems_and_25_programs(master_data):
    """Verify all 100 Left to Solve problems (LTS-001..LTS-100) and all 25 program fronts are indexed cleanly."""
    df = master_data["df"]
    lts_df = df[df["id"].str.startswith("LTS-")]
    assert len(lts_df) == 100
    assert (lts_df["verification_flag"] == "primary-registry-indexed").all()
    assert len(master_data["df_lefttosolve_programs"]) == 25


def test_b07_regression_all_100_lts_ids_exist_verbatim_in_lefttosolve_mirror(master_data):
    """Guard H-901/H-902: every LTS-001..LTS-100 maps verbatim to a unique open/unformalized (solved=False) Left to Solve mirror ID and >= 280 crosswalk matches."""
    mirror_dir = ROOT / "data" / "external" / "lefttosolve" / "programs"
    mirror_by_id: dict[str, dict] = {}
    for jl in sorted(mirror_dir.glob("*.jsonl")):
        for ln in jl.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                rec = json.loads(ln)
                mirror_by_id[rec["id"]] = rec
    assert len(mirror_by_id) >= 59_000

    overrides = json.loads(
        (ROOT / "data" / "external" / "lefttosolve" / "crosswalk_overrides.json").read_text(encoding="utf-8")
    )["include"]
    cw = json.loads(
        (ROOT / "data" / "external" / "lefttosolve" / "atlas_crosswalk.json").read_text(encoding="utf-8")
    )
    assert cw["matched_atlas_problems"] >= 280

    lts_df = master_data["df"][master_data["df"]["id"].str.startswith("LTS-")]
    assert len(lts_df) == 100
    seen_primary: set[str] = set()
    for r in lts_df.itertuples():
        assert r.id in overrides, f"{r.id} missing from crosswalk_overrides.json"
        primaries = [e["id"] for e in overrides[r.id] if e.get("relation") == "primary"]
        assert primaries, f"{r.id} has no primary override entry"
        pid = primaries[0]
        assert pid not in seen_primary, f"Duplicate primary Left to Solve ID {pid} on {r.id}"
        seen_primary.add(pid)
        assert pid in mirror_by_id, f"{r.id} primary ID {pid!r} missing from Left to Solve mirror"
        mrec = mirror_by_id[pid]
        assert mrec["kind"] in {"open", "unformalized"}, f"{r.id} ({pid}) has non-open kind={mrec['kind']}"
        assert mrec["solved"] is False, f"{r.id} ({pid}) is already marked solved=True in mirror"
        assert pid in r.registry_source, f"{r.id} registry_source does not contain verbatim ID {pid!r}"


def test_b06_mcp_query_lefttosolve_rejects_non_string_action_and_bad_args():
    """Guard H-909: MCP query_lefttosolve_programs cleanly rejects non-string action, bad action, bool limit, and bad query."""
    reqs = [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "query_lefttosolve_programs", "arguments": {"action": 123}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "query_lefttosolve_programs", "arguments": {"action": ["summary"]}}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "query_lefttosolve_programs", "arguments": {"action": "drop_table"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "query_lefttosolve_programs", "arguments": {"action": "search", "limit": True}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "query_lefttosolve_programs", "arguments": {"action": "search", "query": 999}}},
    ]
    proc = subprocess.run(
        [sys.executable, str(ROOT / "mcp_server" / "server.py")],
        input="\n".join(json.dumps(r) for r in reqs) + "\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=True,
    )
    resps = [json.loads(ln) for ln in proc.stdout.splitlines() if ln.strip()]
    assert len(resps) == 5
    for resp in resps:
        assert resp["result"]["isError"] is True


def test_b07_regression_dashboard_links_to_lefttosolve_mirror_and_0600_utc():
    """Guard H-903/H-906: Interactive Dashboard links directly to external/lefttosolve/index.html (13-Tool MCP), and mirror reports 06:00 UTC."""
    dash = (ROOT / "outputs" / "MegaAtlas_Interactive_Dashboard_V2.html").read_text(encoding="utf-8")
    assert "external/lefttosolve/index.html" in dash
    assert "13-Tool MCP Server" in dash
    lts_html = (ROOT / "data" / "external" / "lefttosolve" / "index.html").read_text(encoding="utf-8")
    lts_md = (ROOT / "docs" / "lefttosolve-programs.md").read_text(encoding="utf-8")
    assert "06:00 UTC" in lts_html and "07:23 UTC" not in lts_html
    assert "07:23 UTC" not in lts_md and "290 Mega-Atlas problems" in lts_md
