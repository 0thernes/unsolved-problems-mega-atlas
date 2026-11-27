# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Offline tests for the daily external-registry mirrors (Left to Solve programs)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_lefttosolve as lts  # noqa: E402


def test_committed_lefttosolve_mirror_verifies_offline():
    snap = lts.verify_offline()
    assert snap["schema_version"] == lts.SCHEMA_VERSION
    assert snap["fetched_total"] >= lts.MIN_COMPLETENESS * snap["reported_total"]
    assert len(snap["programs"]) >= 20
    assert sum(p["total"] for p in snap["programs"]) == snap["fetched_total"]
    for p in snap["programs"]:
        assert p["url"].startswith("https://lefttosolve.com/programs/")
        assert sum(p["by_kind"].values()) == p["total"]
        assert 0 <= p["solved"] <= p["total"]


def test_mirror_stores_metadata_only():
    snap = json.loads(lts.SNAPSHOT.read_text(encoding="utf-8"))
    first = lts.OUT_DIR / snap["programs"][0]["files"][0]
    item = json.loads(first.read_text(encoding="utf-8").splitlines()[0])
    assert set(item) == set(lts.KEEP_FIELDS) | {"url"}
    assert "excerpt" not in item and "liveAgents" not in item and "claimed" not in item


def test_tampered_manifest_is_rejected(tmp_path, monkeypatch):
    bad = tmp_path / "MANIFEST.sha256"
    lines = lts.MANIFEST.read_text(encoding="utf-8").splitlines()
    digest, rel = lines[0].split("  ", 1)
    lines[0] = ("0" * 64) + "  " + rel
    bad.write_text("\n".join(lines) + "\n", encoding="utf-8")
    monkeypatch.setattr(lts, "MANIFEST", bad)
    with pytest.raises(lts.SyncError):
        lts.verify_offline()


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
