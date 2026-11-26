# Contributing to the Unsolved Problems Mega-Atlas

Thank you for helping critique, audit, falsify, and improve the **Unsolved Problems Mega-Atlas**!

## Workflow & Hard Rules (Build Standard v1.2.0)

- **Maintainer trunk workflow (R1–R4):** Maintainers commit and push straight to `main` (no branch protection, no git hooks, no commit signing, no PR templates). External reviewers and contributors are invited to open **GitHub Issues** for discussion, bug reports, academic critiques, status updates, and new problem proposals.
- **10 Standard Finding Classes:** Please classify every report strictly into one of the 10 standard classes:
  `bug`, `error`, `issue`, `problem`, `concern`, `dilemma`, `conflict`, `gap`, `hole`, `blindspot`.
- **Immutable Evaluation Oracle:** Never modify `autoresearch/evaluate.py` when evaluating RAG, taxonomy, or dataset changes.
- **No Unverified Claims:** Never mark an open problem solved without primary peer-reviewed or official registry confirmation (DOI / arXiv / Clay CMI / Erdős DB / ProofAtlas link).

## How to Submit Improvements or Challenges

1. **Challenge a quantitative score or status:** Open a [Status Update or Falsification](https://github.com/0thernes/unsolved-problems-mega-atlas/issues/new?template=status-update-or-falsification.yml) or [Academic Review](https://github.com/0thernes/unsolved-problems-mega-atlas/issues/new?template=academic-review.yml) issue with primary citations.
2. **Propose a new open problem:** Use the [Propose Open Problem](https://github.com/0thernes/unsolved-problems-mega-atlas/issues/new?template=propose-problem.yml) template, including at least two valid cross-references into existing Atlas IDs to preserve biconnectivity.
3. **Verify locally before committing changes:**
   ```bash
   just reproduce
   just lint
   just typecheck
   just mutate
   ```
   Ensure `0` tracked files exceed `5 MB` (`A24`), `0` `sorry`/`native_decide`/custom `axiom` appear in `lean/`, and `scripts/check_readme_axioms.py` passes.

## Code of Conduct & Licensing

All contributors agree to abide by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and license code/Lean contributions under **Apache-2.0** (`LICENSE-CODE`) and data/prose contributions under **CC-BY-4.0** (`LICENSE`).
