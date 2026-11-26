# AGENTS.md — Canonical Agent Instructions (`unsolved-problems-mega-atlas`)

> **Build Standard:** `v1.2.0` (`docs/build-standard.md`) · **Atlas Version:** `v2.6.0`
> **Author / Maintainer:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`, `0_0@0thernes.art`)
> **Dual License:** Data/Figures/White Paper `CC-BY-4.0` (`LICENSE`) · Code/Lean/Tests `Apache-2.0` (`LICENSE-CODE`)

## 1. Repository Map

- `src/v2_schema.py`, `src/v2_data/m01..m11.py` — 1,912 raw authored records deduplicated into `1,900` unique open problems across 8 Macro-Pillars × 28 Superdomains × 8 Substrates × 7 Abstraction Layers.
- `src/v2_loader.py` — Deterministic loader, alias redirection, NetworkX biconnectivity/PageRank/betweenness (`seed=42`, `REFERENCE_YEAR=2026`), and scoring (`CSS`, `Titan`, `Leverage`, `Gradients`, `Margins`).
- `src/v2_charts.py`, `src/v2_export_all.py` — Generates 15 PNG/SVG charts, 5 vector PDF paper figures, 1280×640 social preview, `<4 MB` WCAG 2.2 AA Interactive HTML, CSV/TSV/XLSX/XLS/MD/TXT, deterministic `.json.gz`/`.jsonl.gz`, `RANKING.md`, and gitignored `.sqlite`/`.json`/`.jsonl`/`build/` directory PDF.
- `rag/query.py`, `mcp_server/server.py` — Offline Porter-stemmed SQLite FTS5 Hybrid RAG (`100.0% MRR@5`, auto-builds DB on fresh clones) and zero-dependency dual-framed 10-tool stdio MCP server.
- `lean/`, `palomar/PalomarChallenge.lean` — Zero-Mathlib Pure Lean 4.35.0 formal invariant suite (**103 audited theorems** across 6 independent kernels + live negative kernel rejection via `scripts/verify_lean_six_kernels.sh`, `0` `sorry` in `lean/`, constructive axioms `⊆ [propext, Quot.sound]`).
- `paper/main.tex`, `paper/refs.bib`, `scripts/build_paper.py` — 10-page Tectonic AMS-LaTeX white paper (`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`) + deterministic clean-room `dist/arxiv_submission.tar.gz`.
- `reference/scoring_oracle.py`, `tests/`, `scripts/run_mutation_audit.py`, `scripts/benchmark_atlas.py` — 50-digit Decimal/Fraction oracle, Hypothesis property suite, differential/metamorphic/golden/negative tests, mutation testing (`6/6`), and 10-iteration warmed benchmarks.
- `autoresearch/evaluate.py` — **STRICTLY IMMUTABLE** Karpathy-style evaluation oracle (`AQS = 97.99`). **NEVER MODIFY THIS FILE.**

## 2. Canonical Commands (`justfile`)

```bash
just setup       # Create .venv and install editable + dev deps
just build       # Regenerate charts, exports, FAIR JSONs, llms-full.txt & checksums
just test        # Run full pytest suite (functional, Hypothesis, differential, MCP, FAIR)
just lint        # Run ruff check
just typecheck   # Run mypy
just mutate      # Run 6-mutant semantic mutation audit (requires 100% kill rate)
just bench       # Run 10-iteration warmed benchmarks -> docs/benchmarks.md
just lean        # Build Lean 4.35.0 suite, audit all 103 axioms & verify README parity
just paper       # Compile AMS-LaTeX PDF (0 overfull), clean-room arXiv tarball & verify 12 citations
just audit       # Run audit_atlas.py, forensic_audit.py, publish_zenodo.py --dry-run & evaluate.py
just reproduce   # End-to-end build + test + lean + paper + checksum verification
```

## 3. Non-Negotiable Hard Rules (Build Standard v1.2.0 R1–R8)

- **R1 (No friction):** Zero branch protection, zero required status checks, zero git hooks, zero commit/tag signing. CI is purely informational.
- **R2 (Trunk workflow):** Commit and push straight to `main`. No PRs, no feature branches. Use GitHub Issues for discussion and review.
- **R3 (No auto-merge/bot PRs):** No Dependabot, Renovate, or bot PR files.
- **R4 (No PR templates):** `.github/PULL_REQUEST_TEMPLATE.md` is banned. Keep only issue templates in `.github/ISSUE_TEMPLATE/`.
- **R5 (Lean & Hygiene):** Keep all git-tracked files strictly `< 5 MB` (`A24`). Keep `lean/**/*.lean` 100% free of `sorry`, `admit`, `native_decide`, and custom `axiom` (`palomar/PalomarChallenge.lean` holds the `sorry`-only Palomar contract outside `lean/`).
- **R6 (Immutability):** Never modify `autoresearch/evaluate.py` during research or hardening loops.
- **R7 (No fabricated claims):** Never fabricate DOIs, peer-review status, benchmark timings, or legal entities (author affiliation is strictly `Independent Researcher, Spokane, WA, USA` — never assert an unformed LLC).
- **R8 (Exact 10 Finding Classes):** Every audit, review, erratum, and issue classifies findings strictly into:
  `bug`, `error`, `issue`, `problem`, `concern`, `dilemma`, `conflict`, `gap`, `hole`, `blindspot`.

## 4. Honest Epistemic Boundaries

1. Lean 4.35.0 verifies internal scoring, quadrant/era, taxonomy, graph handshaking, deduplication, AutoResearch ratchet, gradient/margin, NonVacuity, and AdversarialTests invariants ONLY — **0 / 1,900 overarching open problems are solved or retired**.
2. Quantitative difficulty/tractability/impact/interdisciplinarity scores are disclosed AI-assisted editorial estimates, not peer-reviewed measurements.
3. All 12 Fall/Nov 2026 AI proof claims remain officially unretired pending human-readable proofs and community consensus.
