# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Offline tests for the daily external-registry mirrors (Left to Solve programs & Clay/Erdős/ProofAtlas)."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_external_registries as ser  # noqa: E402
import sync_lefttosolve as lts  # noqa: E402


def test_committed_lefttosolve_mirror_verifies_offline():
    snap = lts.verify_offline()
    assert snap["schema_version"] == lts.SCHEMA_VERSION
    assert snap["fetched_total"] >= lts.MIN_COMPLETENESS * snap["reported_total"]
    assert len(snap["programs"]) >= 20
    assert sum(p["total"] for p in snap["programs"]) == snap["fetched_total"]
    assert isinstance(snap["solved_by_kind"], dict)
    assert sum(snap["solved_by_kind"].values()) == sum(p["solved"] for p in snap["programs"])
    for p in snap["programs"]:
        assert p["url"].startswith("https://lefttosolve.com/programs/")
        assert sum(p["by_kind"].values()) == p["total"]
        assert sum(p["solved_by_kind"].values()) == p["solved"]
        assert 0 <= p["solved"] <= p["total"]
        for k, v in p["solved_by_kind"].items():
            assert 0 <= v <= p["by_kind"].get(k, 0)
    millennium = next(p for p in snap["programs"] if p["program"] == "Millennium Prize")
    assert millennium["solved_by_kind"].get("open", 0) == 0


def test_mirror_stores_metadata_only():
    snap = json.loads(lts.SNAPSHOT.read_text(encoding="utf-8"))
    first = lts.OUT_DIR / snap["programs"][0]["files"][0]
    item = json.loads(first.read_text(encoding="utf-8").splitlines()[0])
    assert set(item) == set(lts.KEEP_FIELDS) | {"url"}
    assert "excerpt" not in item and "liveAgents" not in item and "claimed" not in item


def test_html_dashboard_has_strict_csp_and_disaggregated_fields():
    html_text = lts.HTML_INDEX.read_text(encoding="utf-8")
    assert "Content-Security-Policy" in html_text
    assert "default-src 'none'" in html_text
    assert '<main id="main-content">' in html_text
    assert "Skip to main content" in html_text
    assert "Solved (by kind)" in html_text
    assert "CC BY-SA 4.0" in html_text
    assert "not affiliated" in html_text.lower()


def test_crosswalk_carries_kind_solved_and_advisory_policy():
    cw = json.loads(lts.CROSSWALK.read_text(encoding="utf-8"))
    assert cw["status"] == "ok"
    assert cw["atlas_problems"] == 2000
    assert cw["matched_atlas_problems"] == len(cw["matches"])
    assert cw["matched_atlas_problems"] >= 150
    assert cw.get("curated_override_problems", 0) >= 150
    assert "Advisory only" in cw["policy"]
    assert isinstance(cw["external_solved_signals"], list)
    matched_ids = {m["atlas_id"] for m in cw["matches"]}
    assert {"CS-001", "NT-003", "NT-005", "NT-006", "ANL-001", "QC-037", "COMB-050", "XNT-027"}.issubset(matched_ids)
    # Explicit false-positive exclusions must not leak back in
    assert "GEO-039" not in matched_ids
    assert "GR-018" not in matched_ids
    for m in cw["matches"]:
        for c in m["lefttosolve"]:
            assert "kind" in c and "solved" in c and isinstance(c["solved"], bool)
            assert c.get("relation") in {"primary", "variant", "related"}
            assert c.get("via") in {"normalized-title", "curated-override"}


def test_tampered_manifest_is_rejected(tmp_path, monkeypatch):
    bad = tmp_path / "MANIFEST.sha256"
    lines = lts.MANIFEST.read_text(encoding="utf-8").splitlines()
    digest, rel = lines[0].split("  ", 1)
    lines[0] = ("0" * 64) + "  " + rel
    bad.write_text("\n".join(lines) + "\n", encoding="utf-8")
    monkeypatch.setattr(lts, "MANIFEST", bad)
    with pytest.raises(lts.SyncError):
        lts.verify_offline()


def test_unmanifested_stray_file_is_rejected(tmp_path, monkeypatch):
    mirror = tmp_path / "lefttosolve"
    shutil.copytree(lts.OUT_DIR, mirror)
    (mirror / "stray.txt").write_text("untracked\n", encoding="utf-8")
    monkeypatch.setattr(lts, "OUT_DIR", mirror)
    monkeypatch.setattr(lts, "PROGRAM_DIR", mirror / "programs")
    monkeypatch.setattr(lts, "SNAPSHOT", mirror / "snapshot.json")
    monkeypatch.setattr(lts, "CHANGES", mirror / "CHANGES.jsonl")
    monkeypatch.setattr(lts, "CROSSWALK", mirror / "atlas_crosswalk.json")
    monkeypatch.setattr(lts, "HTML_INDEX", mirror / "index.html")
    monkeypatch.setattr(lts, "MANIFEST", mirror / "MANIFEST.sha256")
    with pytest.raises(lts.SyncError, match="unmanifested"):
        lts.verify_offline()


def test_rebuild_is_deterministic_and_verifies_offline(tmp_path, monkeypatch):
    mirror = tmp_path / "lefttosolve"
    shutil.copytree(lts.OUT_DIR, mirror)
    report = tmp_path / "lefttosolve-programs.md"
    monkeypatch.setattr(lts, "OUT_DIR", mirror)
    monkeypatch.setattr(lts, "PROGRAM_DIR", mirror / "programs")
    monkeypatch.setattr(lts, "SNAPSHOT", mirror / "snapshot.json")
    monkeypatch.setattr(lts, "CHANGES", mirror / "CHANGES.jsonl")
    monkeypatch.setattr(lts, "CROSSWALK", mirror / "atlas_crosswalk.json")
    monkeypatch.setattr(lts, "HTML_INDEX", mirror / "index.html")
    monkeypatch.setattr(lts, "MANIFEST", mirror / "MANIFEST.sha256")
    monkeypatch.setattr(lts, "REPORT", report)
    lts.run_rebuild()
    first_manifest = (mirror / "MANIFEST.sha256").read_text(encoding="utf-8")
    first_html = (mirror / "index.html").read_text(encoding="utf-8")
    lts.run_rebuild()
    assert (mirror / "MANIFEST.sha256").read_text(encoding="utf-8") == first_manifest
    assert (mirror / "index.html").read_text(encoding="utf-8") == first_html
    snap = lts.verify_offline()
    assert snap["fetched_total"] == snap["reported_total"]
    assert report.exists()


def test_delta_detects_added_removed_solved_and_kind_changes():
    old = {
        "a": {"id": "a", "kind": "open", "solved": False, "program": "P"},
        "b": {"id": "b", "kind": "open", "solved": False, "program": "P"},
        "c": {"id": "c", "kind": "unformalized", "solved": False, "program": "P"},
    }
    new = {"P": [
        {"id": "a", "kind": "open", "solved": True},
        {"id": "c", "kind": "open", "solved": False},
        {"id": "d", "kind": "warmup", "solved": False},
    ]}
    d = lts.compute_delta(old, new)
    assert (d["added"], d["removed"], d["newly_solved"], d["kind_changes"]) == (1, 1, 1, 1)
    assert d["newly_solved_ids"] == ["a"] and d["added_sample"] == ["d"] and d["removed_sample"] == ["b"]


def test_slug_and_title_normalisation_are_stable():
    assert lts.slugify("Erdős Problems (not formalized)") == "erdos-problems-not-formalized"
    assert lts.slugify("Green's 100 Open Problems") == "green-s-100-open-problems"
    assert lts.norm_title("The Riemann Hypothesis") == lts.norm_title("Riemann hypothesis (RH)")
    assert lts.problem_url("ComplexityTheory.P_ne_NP") == "https://lefttosolve.com/p/ComplexityTheory.P_ne_NP"


def test_non_json_response_fails_closed(monkeypatch):
    class _Resp:
        headers = {"Content-Type": "text/html"}

        def read(self):
            return b"<html><title>Just a moment...</title></html>"

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(lts.urllib.request, "urlopen", lambda *a, **k: _Resp())
    with pytest.raises(lts.SyncError):
        lts._get_json("https://lefttosolve.com/api/problems")


def test_registry_delta_latest_exists_and_baseline_preserved():
    baseline = (ROOT / "docs" / "registry-delta-2026-11-26.md").read_text(encoding="utf-8")
    latest = (ROOT / "docs" / "registry-delta-latest.md").read_text(encoding="utf-8")
    assert "Daily External Open-Problem Registry" in baseline
    assert "Daily External Open-Problem Registry" in latest
    rep = ser.build_delta_report(live=False)
    assert rep["mode"] == "offline" and len(rep["registries"]) == len(ser.TARGETS) >= 16


def test_mcp_tool_query_lefttosolve_summary_search_and_crosswalk():
    sys.path.insert(0, str(ROOT / "mcp_server"))
    import server as mcp

    summary = mcp.dispatch_tool("query_lefttosolve_programs", {"action": "summary"})
    assert summary["program_count"] >= 20
    assert summary["fetched_total"] == summary["reported_total"]
    assert isinstance(summary["solved_by_kind"], dict)
    assert summary["crosswalk_matches"] >= 30

    search = mcp.dispatch_tool(
        "query_lefttosolve_programs",
        {"action": "search", "program": "Millennium", "query": "Riemann", "limit": 10},
    )
    assert search["programs_searched"] == 1
    assert search["total_matches"] >= 1
    assert all(r["url"].startswith("https://lefttosolve.com/p/") for r in search["results"])

    cw = mcp.dispatch_tool("query_lefttosolve_programs", {"action": "crosswalk", "atlas_id": "NT-005"})
    assert cw["total_matched"] == 1
    assert cw["matches"][0]["atlas_id"] == "NT-005"


def test_expanded_external_registry_program_parser():
    lts_target = next(t for t in ser.TARGETS if t["key"] == "lefttosolve_stats")
    assert lts_target["url"].endswith("/api/stats")
    parsed = ser.parse_lefttosolve_programs_html(
        '<a href="/programs/Millennium%20Prize">Millennium Prize 21 targets · 14 open · 7 solved here</a>'
    )
    assert len(parsed) == 1
    assert parsed[0]["program"] == "Millennium Prize"
    assert (parsed[0]["targets"], parsed[0]["open"], parsed[0]["solved_here"]) == (21, 14, 7)


def test_mcp_query_lefttosolve_rejects_oversized_filter_strings():
    sys.path.insert(0, str(ROOT / "mcp_server"))
    import server as mcp

    huge = "x" * (mcp.MAX_QUERY_CHARS + 1)
    with pytest.raises(ValueError, match="exceeds"):
        mcp.dispatch_tool("query_lefttosolve_programs", {"action": "search", "program": huge})
    with pytest.raises(ValueError, match="exceeds"):
        mcp.dispatch_tool("query_lefttosolve_programs", {"action": "search", "field": huge})
    with pytest.raises(ValueError, match="exceeds"):
        mcp.dispatch_tool("query_lefttosolve_programs", {"action": "crosswalk", "atlas_id": huge})
