# System Architecture — Unsolved Problems Mega-Atlas (`v2.6.0`)

## High-Level Data & Verification Pipeline

```text
  src/v2_data/m01..m11.py (1,912 raw authored problem entries across 11 domain modules)
         │
         ▼
  src/v2_loader.py  ──► Deduplication + 12 Alias Merges (1,900 unique, 0 dangling links)
         │          ──► NetworkX Graph (5,808 edges, 1 biconnected component, 0 APs, 0 bridges)
         │          ──► Scoring (CSS, Titan, Leverage, Gradients, Margins, Substrates, Layers)
         ├─────────────────────────┬──────────────────────────┬────────────────────────┐
         ▼                         ▼                          ▼                        ▼
  src/v2_charts.py          src/v2_export_all.py      reference/scoring_oracle.py   lean/ (Pure Lean 4.35.0)
  - 15 PNG+SVG charts       - CSV/TSV/JSON.gz/JSONL.gz - 50-digit Decimal/Fraction   - 8 core modules + AdversarialTests
  - 5 Vector PDF figs       - 15-sheet XLSX, 8-sh XLS  - 2,000+ differential tests   - Challenge/Solution/Palomar
  - 1280x640 social card    - MD, TXT, RANKING.md      - Hypothesis (1,000 ex.)      - 103 theorems, 6/6 kernels
         │                  - <4 MB WCAG 2.2 AA HTML   - 6/6 mutation audit          - results/lean_axioms.txt
         ▼                  - SQLite+FTS5 (auto-built)        │                        │
  paper/main.tex (Tectonic)        │                          ▼                        ▼
  - 10-page AMS-LaTeX PDF          ├─► rag/query.py (100% MRR@5)            blueprint/index.html
  - dist/arxiv_submission.tar.gz   ├─► mcp_server/server.py (11 tools)      (Interactive SVG DAG)
                                   └─► autoresearch/evaluate.py (IMMUTABLE, AQS=97.99)
```

## Module Responsibilities & Boundaries

| Layer | Directory / File | Responsibility | Strict Invariant |
|---|---|---|---|
| **Source Corpus** | `src/v2_schema.py`, `src/v2_data/m01..m11.py` | Authored open-problem definitions, canonical 88 hubs, 8×28 taxonomy | Every record matches JSON Schema Draft 2020-12 (`schema/problem.schema.json`) |
| **Analytics Loader** | `src/v2_loader.py` | Deduplication, alias redirection, NetworkX biconnectivity/PageRank, CSS/Titan/Gradient/Margin computation | Deterministic (`seed=42`, `REFERENCE_YEAR=2026`), `0` dangling links, `0` APs |
| **Visuals & Paper** | `src/v2_charts.py`, `paper/main.tex`, `scripts/build_paper.py` | 15 PNG/SVG charts, 5 vector PDF figures, social preview, 10-page AMS-LaTeX PDF + clean-room arXiv tarball | `0` overfull hboxes, `0` undefined refs, `12/12` live HTTP/DOI citations |
| **Exporters & Web UI** | `src/v2_export_all.py`, `blueprint/index.html` | Multi-format exports, `<4 MB` WCAG 2.2 AA dashboard, `RANKING.md` | All git-tracked files `< 5.0 MB` (A24); heavy derived files in `build/` + GitHub Releases |
| **RAG & Agent API** | `rag/query.py`, `mcp_server/server.py` | Offline SQLite FTS5 Hybrid BM25+PageRank retrieval + 11-tool dual-framed stdio MCP server | Auto-builds SQLite on clean clones; zero runtime network calls; parameterized SQL only |
| **Formal Verification** | `lean/`, `palomar/PalomarChallenge.lean` | 103 Pure Lean 4.35.0 theorems + NonVacuity + AdversarialTests + 6-kernel Palomar | `0` `sorry` in `lean/`, `0` `native_decide`, axioms strictly `⊆ [propext, Quot.sound]` |
| **Verification Ladder** | `reference/`, `tests/`, `scripts/`, `autoresearch/` | 50-digit oracle, Hypothesis property suite, mutation testing, benchmarks, immutable AutoResearch oracle | `autoresearch/evaluate.py` is strictly read-only/immutable; `100%` mutation kill rate |

See [`docs/adr/README.md`](adr/README.md) for Architecture Decision Records documenting every major design trade-off.
