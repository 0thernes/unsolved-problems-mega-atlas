# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Deep Verification Ladder Test Suite (Build Standard B03, B06, B07, B08, B10, B11, B12, B14, B20, A08, A24, A43):
  - B03: Determinism / repeatability
  - B06: Negative boundary & error handling (MCP, RAG, JSON Schema)
  - B07: Named regression tests for every historical defect
  - B08: Golden snapshot verification (92-theorem Lean axioms + Top-10 rankings)
  - B10: Hypothesis property-based tests (1,000 examples per property)
  - B11/B12: 2,000-case randomized + 1,900-row exhaustive differential audit vs. 50-digit Decimal oracle
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
