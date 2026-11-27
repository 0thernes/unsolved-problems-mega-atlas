# System Architecture — Unsolved Problems Mega-Atlas (`v2.11.0`)

## High-Level Data & Verification Pipeline

```text
  src/v2_data/m01..m12.py (2,012 raw authored problem entries across 12 domain modules, incl. Left to Solve 25 baseline fronts)
         │
         ▼
  src/v2_loader.py  ──► Deduplication + 12 Alias Merges (2,000 unique, 0 dangling links)
         │          ──► NetworkX Graph (6,108 edges, 1 biconnected component, 0 APs, 0 bridges)
         │          ──► Scoring (CSS, Titan, Leverage, Gradients, Margins, Substrates, Layers)
         ├─────────────────────────┬──────────────────────────┬────────────────────────┐
         ▼                         ▼                          ▼                        ▼
  src/v2_charts.py          src/v2_export_all.py      reference/scoring_oracle.py   lean/ (Zero-Mathlib Lean 4.35.0)
  - 15 PNG+SVG charts       - CSV/TSV/JSON.gz/JSONL.gz - 50-digit Decimal/Fraction   - Software-model invariants ONLY
  - 5 Vector PDF figs       - 16-sheet XLSX, build/XLS - 2,000+ differential tests   - 103 audited of 117 decls (1,711 lines)
  - 1280x640 social card    - MD, TXT, RANKING.md      - Hypothesis (1,000 ex.)      - 6 kernel checks / 5 impl. (9 tgts)
         │                  - ~3.1 MB WCAG 2.2 AA HTML - 14/14 mutation audit        - results/lean_axioms.txt
         ▼                  - SQLite+FTS5 (atomic)            │                        │
  paper/main.tex (Tectonic)        │                          ▼                        ▼
  - 11-page AMS-LaTeX PDF          ├─► rag/query.py (100% MRR@5)            blueprint/index.html
  - dist/arxiv_submission.tar.gz   ├─► mcp_server/server.py (13 tools)      (Interactive SVG DAG)
                                   ├─► .github/workflows/daily-registry-sync.yml (06:00 UTC daily, 16 trackers + 26 LTS fronts + 62k JSONL mirror)
                                   └─► autoresearch/evaluate.py (IMMUTABLE, AQS=98.35)
```

## Module Responsibilities & Boundaries

| Layer | Directory / File | Responsibility | Strict Invariant |
|---|---|---|---|
| **Source Corpus** | `src/v2_schema.py`, `src/v2_data/m01..m12.py` | Authored open-problem definitions, canonical 88 hubs, 8×28 taxonomy, 100 Left to Solve conjectures | Every record matches JSON Schema Draft 2020-12 (`schema/problem.schema.json`) |
| **Analytics Loader** | `src/v2_loader.py` | Deduplication, alias redirection, NetworkX biconnectivity/PageRank, CSS/Titan/Gradient/Margin computation, 16-registry & 26-front Left to Solve baselines, 20-row Cycle-3 companion ledger | Deterministic (`seed=42`, `REFERENCE_YEAR=2026`), `0` dangling links, `0` APs |
| **Visuals & Paper** | `src/v2_charts.py`, `paper/main.tex`, `scripts/build_paper.py` | 15 PNG/SVG charts, 5 vector PDF figures, social preview, 11-page AMS-LaTeX PDF + clean-room arXiv tarball | `0` overfull hboxes/vboxes, `0` undefined refs (incl. clean-room arXiv log), `15/15` live title-verified citations (`0` retractions) |
| **Exporters & Web UI** | `src/v2_export_all.py`, `blueprint/index.html` | Multi-format exports (`LeftToSolve_Programs` sheet), enum-dictionary `~3.1 MB` WCAG 2.2 AA dashboard (live-hydrating `./daily_registries.json`), `RANKING.md` | All git-tracked files `< 5.0 MB` (A24); strict CSP; heavy derived files in `build/` + GitHub Releases |
| **Daily Registry Sync** | `scripts/sync_external_registries.py`, `scripts/sync_lefttosolve.py`, `scripts/mine_sovereign_targets.py`, `.github/workflows/daily-registry-sync.yml` | Automated daily (`06:00 UTC`) polling of 16 public trackers + full 26-program Left to Solve JSONL mirror (`data/external/lefttosolve/`, `62,790` targets, `291` crosswalk) + offline sovereign target radar | Advisory only (zero auto-retirement; runs full `pytest tests/` before push); strictly excluded from release-frozen `CHECKSUMS.sha256` |
| **RAG & Agent API** | `rag/query.py`, `mcp_server/server.py` | Offline SQLite FTS5 Hybrid BM25+PageRank retrieval + 13-tool dual-framed stdio MCP server | Atomically auto-builds SQLite on clean clones; filter-enforced exact-ID queries; `1 MiB` frame cap + `-32602` `params` validation; parameterized SQL & path containment |
| **Formal Verification** | `lean/`, `palomar/PalomarChallenge.lean` | 103 audited Lean 4.35.0 software-model theorems (of `117` decls; `14` files / `1,711` lines) + NonVacuity + AdversarialTests + Palomar targets | `0` `sorry`, `0` `native_decide`, per-theorem axioms `⊆ [propext, Quot.sound]`; `6` kernel checks across `5` distinct implementations on `9` targets |
| **Verification Ladder** | `reference/`, `tests/`, `scripts/`, `research/`, `autoresearch/` | 50-digit oracle, Hypothesis property suite, `14/14` mutation testing, 3 Track B probes (`LOG-002`, `NT-005`, `COMB-002`), benchmarks, immutable AutoResearch oracle | `autoresearch/evaluate.py` is strictly read-only/immutable; `115` `pytest` checks; strict `mypy --check-untyped-defs`; `100%` mutation kill rate |

See [`docs/adr/README.md`](adr/README.md) for Architecture Decision Records documenting every major design trade-off.
