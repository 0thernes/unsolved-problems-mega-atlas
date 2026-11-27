# AGENTS.md — Canonical Agent Instructions (`unsolved-problems-mega-atlas`)

> **Build Standard:** `v1.2.0` (`docs/build-standard.md`) · **Atlas Version:** `v2.10.0`
> **Author / Maintainer:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID `0009-0006-8168-9648`, `0_0@0thernes.art`)
> **Dual License:** Data/Figures/White Paper `CC-BY-4.0` (`LICENSE`) · Code/Lean/Tests `Apache-2.0` (`LICENSE-CODE`)

## 1. Repository Map

- `src/v2_schema.py`, `src/v2_data/m01..m12.py` — 2,012 raw authored records deduplicated into `2,000` unique open problems across 8 Macro-Pillars × 28 Superdomains × 8 Substrates × 7 Abstraction Layers (including `m12_lefttosolve_programs.py` covering all 25 fronts on `lefttosolve.com/programs`).
- `src/v2_loader.py` — Deterministic loader, alias redirection, NetworkX biconnectivity/PageRank/betweenness (`seed=42`, `REFERENCE_YEAR=2026`), scoring (`CSS`, `Titan`, `Leverage`, `Gradients`, `Margins`), `16`-registry + `25`-front Left to Solve baselines, and `20`-row Cycle-3 companion archive cross-map.
- `src/v2_charts.py`, `src/v2_export_all.py` — Generates 15 PNG/SVG charts, 5 vector PDF paper figures, 1280×640 social preview, `<4 MB` WCAG 2.2 AA Interactive HTML (enum-dictionary encoded + same-origin `./daily_registries.json` live hydration), CSV/TSV/16-sheet XLSX/MD/TXT, deterministic `.json.gz`/`.jsonl.gz`, `RANKING.md`, and gitignored `.sqlite`/`.json`/`.jsonl`/`build/*_Legacy.xls`/`build/` directory PDF.
- `rag/query.py`, `mcp_server/server.py` — Offline Porter-stemmed SQLite FTS5 Hybrid RAG (`100.0% MRR@5`, filter-enforced exact-ID lookup, auto-builds DB on fresh clones) and zero-dependency dual-framed 13-tool stdio MCP server (`1 MiB` cap on both NDJSON and `Content-Length:`, incl. `simulate_rubric_override`, `get_live_registry_tracker`, & `query_lefttosolve_programs`).
- `lean/`, `palomar/PalomarChallenge.lean` — Zero-Mathlib Lean 4.35.0 software-model invariant suite (**103 audited theorems** of `117` declarations in `lean/`, `0` `sorry`, per-theorem axioms `⊆ [propext, Quot.sound]`; `9` Palomar targets checked by `6` kernel checks across `5` distinct implementations + live negative kernel rejection via `scripts/verify_lean_six_kernels.sh`).
- `paper/main.tex`, `paper/refs.bib`, `scripts/build_paper.py` — 11-page Tectonic AMS-LaTeX white paper (`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`) + deterministic clean-room `dist/arxiv_submission.tar.gz` (`15/15` title-verified citations, `0` retractions).
- `reference/scoring_oracle.py`, `tests/`, `scripts/run_mutation_audit.py`, `scripts/benchmark_atlas.py`, `.github/workflows/daily-registry-sync.yml` — 50-digit Decimal/Fraction oracle, `99`-test `pytest` suite (Hypothesis, differential, metamorphic, golden, negative, regressions, Left to Solve mirror), `12`-mutant semantic mutation audit (`12/12`), 10-iteration warmed benchmarks, and automated daily 16-registry + 25-front Left to Solve sync (`06:00 UTC`, `59,396`-target mirror, `290` curated crosswalk matches).
- `research/runs/` — Three reproducible exact finite Track B probes (`LOG-002` Antihydra, `NT-005` Collatz, `COMB-002` Ramsey witnesses; all parents remain **OPEN**).
- `autoresearch/evaluate.py` — **STRICTLY IMMUTABLE** Karpathy-style evaluation oracle (`AQS = 98.35`). **NEVER MODIFY THIS FILE.**

## 2. Canonical Commands (`justfile`)

```bash
just setup           # Create .venv and install editable + dev deps
just build           # Run Track B probes; regenerate charts, exports, FAIR JSONs, llms-full.txt & checksums
just test            # Run full 99-test pytest suite (functional, Hypothesis, differential, MCP, FAIR, LTS mirror)
just lint            # Run ruff check (incl. research/)
just typecheck       # Run mypy (incl. research/)
just mutate          # Run 12-mutant semantic mutation audit (requires 12/12 = 100% kill rate)
just bench           # Run 10-iteration warmed benchmarks -> docs/benchmarks.md
just lean            # Build Lean 4.35.0 suite, audit all 103 axioms & verify README parity
just paper           # Compile AMS-LaTeX PDF (0 overfull), clean-room arXiv tarball & verify 15 citations
just sync-registries # Live poll all 16 public trackers & 25 Left to Solve fronts -> daily telemetry
just audit           # Run audit_atlas.py, forensic_audit.py, publish_zenodo.py --dry-run & evaluate.py
just reproduce       # End-to-end build + test + lean + paper + checksum & timestamp verification
```

## 3. Non-Negotiable Hard Rules (Build Standard v1.2.0 R1–R8)

- **R1 (No friction):** Zero branch protection, zero required status checks, zero git hooks, zero commit/tag signing. CI is purely informational.
- **R2 (Trunk workflow):** Commit and push straight to `main`. No PRs, no feature branches. Use GitHub Issues for discussion and review.
- **R3 (No auto-merge/bot PRs):** No Dependabot, Renovate, or bot PR files.
- **R4 (No PR templates):** `.github/PULL_REQUEST_TEMPLATE.md` is banned. Keep only issue templates in `.github/ISSUE_TEMPLATE/`.
- **R5 (Lean & Hygiene):** Keep all git-tracked files strictly `< 5 MB` (`A24`). Keep `lean/**/*.lean` 100% free of `sorry`, `admit`, `native_decide`, `unsafe`, `implemented_by`, `@[extern`, `opaque`, and custom `axiom` (`palomar/PalomarChallenge.lean` holds the `sorry`-only Palomar contract outside `lean/`).
- **R6 (Immutability):** Never modify `autoresearch/evaluate.py` during research or hardening loops.
- **R7 (No fabricated claims):** Never fabricate DOIs, peer-review status, benchmark timings, or legal entities (author affiliation is strictly `Independent Researcher, Spokane, WA, USA` — never assert an unformed LLC).
- **R8 (Exact 10 Finding Classes):** Every audit, review, erratum, and issue classifies findings strictly into:
  `bug`, `error`, `issue`, `problem`, `concern`, `dilemma`, `conflict`, `gap`, `hole`, `blindspot`.

## 4. Honest Epistemic Boundaries

1. Lean 4.35.0 verifies discrete software-model invariants ONLY — no Lean theorem refers to the `2,000`-row dataset or its `6,108`-edge graph, and **0 / 2,000 overarching open problems are solved or retired**.
2. Quantitative difficulty/tractability/impact/interdisciplinarity scores are disclosed AI-assisted editorial estimates, not peer-reviewed measurements.
3. All 12 Fall/Nov 2026 AI proof claims remain officially unretired pending human-readable proofs and community consensus.
