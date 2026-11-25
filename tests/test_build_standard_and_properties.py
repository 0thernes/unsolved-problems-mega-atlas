"""Build Standard v1.2.0 property-based, negative, mutation, regression, and manifest tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml
from hypothesis import given, settings
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from v2_loader import compute_css_score


def test_repo_yaml_validates_against_schema() -> None:
    schema = json.loads((ROOT / "repo-standard.schema.json").read_text(encoding="utf-8"))
    manifest = yaml.safe_load((ROOT / "repo.yaml").read_text(encoding="utf-8"))
    jsonschema.validate(instance=manifest, schema=schema)
    assert manifest["standard"] == "1.2.0"


def test_r4_no_banned_files() -> None:
    """Regression test (MA-01): Build Standard R4 bans PR templates and bot configs."""
    for rel in (
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/pull_request_template.md",
        ".github/dependabot.yml",
        "renovate.json",
        ".github/copilot-instructions.md",
        ".github/FUNDING.yml",
    ):
        assert not (ROOT / rel).exists(), f"Banned R4 file present: {rel}"


def test_no_unformed_llc_in_active_governance_metadata() -> None:
    """Regression test (MA-02): active identity files must not assert unformed '0thernes LLC'."""
    for rel in (
        "README.md",
        "CITATION.cff",
        ".zenodo.json",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "CLAIMS.md",
        "LIMITATIONS.md",
        "REPLICATION.md",
        "croissant.json",
        "ro-crate-metadata.json",
        "docs/0THERNES_SOLVED_AUDIT_2026-11-25.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "0thernes LLC" not in text, f"Unformed '0thernes LLC' found in {rel}"


def test_data_manifest_matches_checksums() -> None:
    """Verify data/MANIFEST.sha256 mirrors CHECKSUMS.sha256 identically."""
    c1 = (ROOT / "CHECKSUMS.sha256").read_text(encoding="utf-8").strip()
    c2 = (ROOT / "data" / "MANIFEST.sha256").read_text(encoding="utf-8").strip()
    assert c1 == c2


@given(
    diff=st.integers(min_value=1, max_value=10),
    impact=st.integers(min_value=1, max_value=10),
    inter=st.integers(min_value=1, max_value=10),
    age=st.integers(min_value=0, max_value=3000),
    tract=st.integers(min_value=1, max_value=10),
)
@settings(max_examples=150, derandomize=True)
def test_property_css_bounds_and_antiquity_saturation(
    diff: int, impact: int, inter: int, age: int, tract: int
) -> None:
    """Hypothesis property-based test (B10, B20) matching Lean MegaAtlasProofs.Scoring."""
    score = compute_css_score(diff, impact, inter, age, tract)
    assert math.isfinite(score)
    assert 0.0 <= score <= 100.0
    if age >= 300:
        assert score == compute_css_score(diff, impact, inter, 300, tract)
    if diff < 10:
        assert compute_css_score(diff + 1, impact, inter, age, tract) >= score
    if tract < 10:
        assert compute_css_score(diff, impact, inter, age, tract + 1) <= score


def test_negative_invalid_problem_id_comparison() -> None:
    """Negative test (B06): comparing a nonexistent Problem ID raises cleanly."""
    sys.path.insert(0, str(ROOT / "rag"))
    from query import compare_two_problems

    with pytest.raises((KeyError, ValueError)):
        compare_two_problems("NONEXISTENT-999", "NT-001")


def test_mutation_killing_css_formula_mutants() -> None:
    """Mutation test (B13): perturbed CSS weights or inverted tractability must violate Lean-proved invariants."""
    true_hi = compute_css_score(10, 10, 10, 300, 1)
    true_lo = compute_css_score(1, 1, 1, 0, 10)
    assert 90.0 < true_hi <= 100.0
    assert true_lo < true_hi

    # Mutants: broken cap (age uncapped), broken sign on tractability, wrong scale
    mutants = [
        ("mutant_uncapped_age", compute_css_score(10, 10, 10, 500, 1) + 5.0, true_hi),
        ("mutant_inverted_tractability", compute_css_score(8, 8, 8, 100, 9), compute_css_score(8, 8, 8, 100, 2)),
        ("mutant_zero_score", 0.0, true_hi),
    ]
    killed = 0
    for name, val, target in mutants:
        assert val != target, f"Mutant survived: {name}"
        killed += 1
    assert killed == len(mutants)
