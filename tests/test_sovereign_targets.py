# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Offline unit & negative tests for the sovereign target radar and bridge scaffolder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import mine_sovereign_targets as mst  # noqa: E402


def test_mine_open_targets_returns_deterministic_ranked_list():
    r1 = mst.mine_targets(kind="open", limit=20)
    r2 = mst.mine_targets(kind="open", limit=20)
    assert r1["total_lean_stated_in_mirror"] >= 3900
    assert r1["total_matching"] >= 1900
    assert len(r1["targets"]) == 20
    assert [t["id"] for t in r1["targets"]] == [t["id"] for t in r2["targets"]]
    assert all(t["kind"] == "open" for t in r1["targets"])
    scores = [t["score"] for t in r1["targets"]]
    assert scores == sorted(scores, reverse=True)


def test_mine_domain_filter_quantum_returns_quantum_entries():
    rep = mst.mine_targets(kind="open", domains_filter=["quantum"], limit=50)
    assert rep["total_matching"] >= 20
    assert all("quantum" in t["domains"] for t in rep["targets"])
    ids = {t["id"] for t in rep["targets"]}
    assert any(i.startswith("OpenQuantumProblem") for i in ids)


def test_mine_known_targets_excludes_solved_by_default():
    rep = mst.mine_targets(kind="known", limit=30)
    assert rep["total_matching"] >= 900
    assert all(t["kind"] == "known" for t in rep["targets"])


def test_markdown_render_contains_pinned_commit_and_orcid():
    rep = mst.mine_targets(kind="open", domains_filter=["combinatorics"], limit=10)
    md = mst.render_markdown(rep)
    assert mst.AUTHOR_ORCID in md
    assert "9097e2f90e66" in md
    assert "0thernes LLC" not in md
    assert "| Rank | Score |" in md


def test_scaffold_sovereign_bridge_creates_palomar_and_bridge_files(tmp_path: Path):
    dest = tmp_path / "barker-demo"
    res = mst.scaffold_sovereign_bridge("Arxiv.2104.00502.barker_conjecture", dest)
    assert res["target_id"] == "Arxiv.2104.00502.barker_conjecture"
    assert res["kind"] == "open"
    assert (dest / "lean" / "Challenge.lean").is_file()
    assert (dest / "lean" / "FormalConjecturesBridge.lean").is_file()
    assert (dest / "lean" / "Reduction.lean").is_file()
    assert (dest / "lean" / "comparator.json").is_file()
    assert (dest / "formalization.yaml").is_file()
    assert (dest / "THIRD_PARTY_NOTICES.md").is_file()

    comp = json.loads((dest / "lean" / "comparator.json").read_text(encoding="utf-8"))
    assert comp["permitted_axioms"] == ["propext", "Quot.sound", "Classical.choice"]

    fyaml = (dest / "formalization.yaml").read_text(encoding="utf-8")
    assert mst.AUTHOR_ORCID in fyaml
    assert "Independent Researcher" in fyaml
    assert "0thernes LLC" not in fyaml


def test_scaffold_rejects_unknown_target_id(tmp_path: Path):
    with pytest.raises(ValueError, match="not found"):
        mst.scaffold_sovereign_bridge("Nonexistent.fake_theorem_99999", tmp_path / "bad")


def test_get_upstream_commit_refuses_to_fabricate_when_missing():
    with pytest.raises(ValueError, match="missing upstream.commit"):
        mst.get_upstream_commit({"retrieved_utc": "2026-11-27T00:00:00Z"})


def test_difficulty_zero_sorts_before_positive_difficulty(tmp_path: Path):
    """Regression test: difficulty=0 must not be coerced to 999 via `or 999`."""
    mirror = tmp_path / "mirror"
    (mirror / "programs").mkdir(parents=True)
    snap = {
        "retrieved_utc": "2026-11-27T00:00:00Z",
        "upstream": {"commit": "deadbeef" * 5},
        "programs": [{"program": "Demo", "files": ["programs/demo.jsonl"]}],
    }
    (mirror / "snapshot.json").write_text(json.dumps(snap), encoding="utf-8")
    rows = [
        {"id": "A.diff_pos", "title": "Alpha", "kind": "open", "difficulty": 10, "fields": [], "solved": False, "prize": None, "url": "https://lefttosolve.com/p/A.diff_pos"},
        {"id": "B.diff_zero", "title": "Beta", "kind": "open", "difficulty": 0, "fields": [], "solved": False, "prize": None, "url": "https://lefttosolve.com/p/B.diff_zero"},
        {"id": "C.diff_none", "title": "Gamma", "kind": "open", "difficulty": None, "fields": [], "solved": False, "prize": None, "url": "https://lefttosolve.com/p/C.diff_none"},
    ]
    (mirror / "programs" / "demo.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    # Force equal score to test the difficulty tie-breaker directly
    rep = mst.mine_targets(mirror, kind="open", limit=10)
    ids = [t["id"] for t in rep["targets"]]
    assert ids.index("B.diff_zero") < ids.index("A.diff_pos") < ids.index("C.diff_none")


def test_scaffold_escapes_quotes_and_sanitizes_project_name(tmp_path: Path):
    """Regression test: titles with double quotes produce valid quoted YAML and public Lean module decls."""
    mirror = tmp_path / "mirror"
    (mirror / "programs").mkdir(parents=True)
    snap = {
        "retrieved_utc": "2026-11-27T00:00:00Z",
        "upstream": {"commit": "abcdef12" * 5},
        "programs": [{"program": "Demo", "files": ["programs/demo.jsonl"]}],
    }
    (mirror / "snapshot.json").write_text(json.dumps(snap), encoding="utf-8")
    row = {
        "id": "Demo.quoted_problem",
        "title": 'The "Quoted" \\ Conjecture',
        "kind": "open",
        "difficulty": 50,
        "fields": [],
        "solved": False,
        "prize": None,
        "url": "https://lefttosolve.com/p/Demo.quoted_problem",
    }
    (mirror / "programs" / "demo.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    dest = tmp_path / "out"
    res = mst.scaffold_sovereign_bridge("Demo.quoted_problem", dest, mirror_dir=mirror, project_name="99-bad name!")
    assert res["project_name"] == "T_99_bad_name_"
    fyaml = (dest / "formalization.yaml").read_text(encoding="utf-8")
    assert r'title: "The \"Quoted\" \\ Conjecture — Sovereign Formalization"' in fyaml
    ch = (dest / "lean" / "Challenge.lean").read_text(encoding="utf-8")
    assert "public def TargetStatement" in ch and "public theorem target_main" in ch


def test_mine_targets_rejects_negative_limit_and_invalid_filters(tmp_path: Path):
    with pytest.raises(ValueError, match="limit must be non-negative"):
        mst.mine_targets(limit=-1)
    with pytest.raises(ValueError, match="Unsupported kind"):
        mst.mine_targets(kind="bogus")
    with pytest.raises(ValueError, match="Unknown domain filter"):
        mst.mine_targets(domains_filter=["quantum", "nonexistent_domain"])
    rep_zero = mst.mine_targets(kind="open", limit=0)
    assert rep_zero["targets"] == [] and rep_zero["total_matching"] >= 1900


def test_load_lean_stated_targets_reports_malformed_jsonl_with_location(tmp_path: Path):
    mirror = tmp_path / "mirror"
    (mirror / "programs").mkdir(parents=True)
    snap = {
        "retrieved_utc": "2026-11-27T00:00:00Z",
        "upstream": {"commit": "abcdef12" * 5},
        "programs": [{"program": "Demo", "files": ["programs/bad.jsonl"]}],
    }
    (mirror / "snapshot.json").write_text(json.dumps(snap), encoding="utf-8")
    (mirror / "programs" / "bad.jsonl").write_text('{"id": "ok", "kind": "open"}\n{not valid json\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"Malformed JSON in bad\.jsonl:2"):
        mst.load_lean_stated_targets(mirror)

