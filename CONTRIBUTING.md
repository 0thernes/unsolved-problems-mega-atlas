# Contributing & Scientific Challenge Guide

Thank you for helping audit, sharpen, and expand the **Unsolved Problems Mega-Atlas**!  
Because this atlas is curated by an independent solo researcher with disclosed AI assistance, **critical review, score challenges, primary-source citations, and falsification reports are the highest-value contributions possible.**

## Ways to Contribute

1. **Challenge a Score or Ranking:** Disagree with a problem's `difficulty_score`, `tractability_2050`, `civilizational_impact`, `CSS`, or `Titan Index`? Open a PR editing its entry in `src/v2_data/m*.py`, justify the change with domain evidence, and regenerate outputs so reviewers can judge directly from the diff.
2. **Report a Status Change, Resolution, or Falsification:** Has a conjecture been proved, disproved, retired, or had a Fall/Nov 2026 AI proof claim verified or refuted? Use the **Status Update / Falsification** issue template (`.github/ISSUE_TEMPLATE/status-update-or-falsification.yml`) with a primary citation (arXiv, journal DOI, Clay CMI, ProofAtlas, Erdős Problems DB, or Lean archive URL).
3. **Propose a Missing Open Problem:** Use the **Propose Open Problem** issue template (`.github/ISSUE_TEMPLATE/propose-problem.yml`) specifying Macro-Pillar, Superdomain, formal expression, originator, year, and primary registry reference.
4. **Conduct an Academic Domain Audit:** Domain specialists can sign off on or critique any Superdomain using the **Academic Review** template and [`docs/ACADEMIC_REVIEW.md`](docs/ACADEMIC_REVIEW.md).
5. **Strengthen Formal Invariants or Tooling:** Add Lean 4.35.0 theorems in `lean/MegaAtlasProofs/` (strictly zero Mathlib, zero `sorry`, zero `native_decide`, axioms within `[propext, Quot.sound]`), add `pytest` cases in `tests/`, or improve `rag/query.py`.

## Pull Request Verification Checklist

Before opening a PR, run the full local verification pipeline:

```bash
# Windows PowerShell
.\build.ps1

# Unix / macOS / WSL
make all
```

Or step-by-step:
```bash
python src/v2_export_all.py
python scripts/audit_atlas.py --sync-checksums --check-lean
pytest -v
```

Every PR must pass both GitHub Actions CI jobs (`python-audit-and-tests` and `lean-formal-invariants`), maintain zero duplicate IDs/names, satisfy `schema/problem.schema.json` on all records, and keep `CHECKSUMS.sha256` byte-exact.

## Licensing of Contributions

By submitting a pull request, you agree that:
- Data, prose, and taxonomy contributions are licensed under **CC BY 4.0** (`LICENSE`).
- Code, schema, RAG, test, and Lean 4 proof contributions are licensed under **MIT** (`LICENSE-CODE`).
