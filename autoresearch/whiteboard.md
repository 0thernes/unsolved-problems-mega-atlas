# AutoResearch Whiteboard — Planner · Worker · Verifier Scratchpad

> Inspired by [`kripner/OpenProver`](https://github.com/kripner/OpenProver)'s shared Whiteboard architecture and [`SakanaAI/AI-Scientist`](https://github.com/SakanaAI/AI-Scientist)'s iterative hypothesis queue.

## Active Research Queue (Track A — Atlas Infrastructure)

| ID | Hypothesis | Target File(s) | Expected Metric Lift | Status |
|---|---|---|---|---|
| **H-001** | Staged Exact-Phrase → Strict-AND → OR BM25 without graph authority. | `rag/query.py` | `rag_mrr5` ↑ | **DISCARDED** (`0.00` lift; pure BM25 still outranked hubs on niche duplicates) |
| **H-001b** | Hybrid BM25 + deduplicated unique-token title/body coverage + log-degree knowledge-graph authority re-ranking. | `rag/query.py` | `rag_mrr5` ↑, `aqs_score` ↑ | **KEPT** (`rag_mrr5`: `89.33 → 96.00`, `21/25 → 23/25` top-1; `aqs`: `80.26 → 81.93`) |
| **H-002** | Adding FAIR/ML metadata triad (`.zenodo.json`, `croissant.json`, `ro-crate-metadata.json`, `docs/DATASHEET.md`, `AGENTS.md`, `llms.txt`, `SECURITY.md`, `CITATION.bib`) + zero-dependency MCP stdio server (`mcp_server/server.py`) + 12 Lean 4.35.0 AutoResearch invariants (`46 → 58` theorems). | FAIR metadata, `mcp_server/`, `lean/` | `provenance` ↑, `formal_score` ↑, `aqs_score` ↑ | **KEPT (`v2.2.0`)** |
| **H-003** | Syncing verified external registry identifiers from `teorth/erdosproblems` and `ProofAtlas.ai` for currently `ai-assisted-editorial-synthesis` pure-math entries to lift `primary-registry-indexed` provenance above 50%. | `src/v2_data/m01..m02, m10` | `provenance` ↑ | **BACKLOG (`v2.3.0`)** |
| **H-004** | Multi-model adversarial scoring audit (comparing independent editorial estimates across frontier model families per `0thernes/unsolved-mathematics`) to compute inter-rater variance on `CSS` and `Titan Index`. | `docs/ACADEMIC_REVIEW.md`, `src/v2_loader.py` | Epistemic calibration | **BACKLOG (`v2.3.0`)** |

## Active Research Queue (Track B — Open-Problem Frontier Investigations)

| ID | Problem ID | Frontier Target | Falsification / Lean Gate | Status |
|---|---|---|---|---|
| **F-001** | `NT-001` / `ANL-001` | Independent statement-fidelity checklist & secondary kernel (`lean4lean` / `nanoda`) tracking for Nov 20, 2026 RH & Sept 8 Navier–Stokes AI claims. | Never retire without external fidelity + CMI consensus | **MONITORING** |
| **F-002** | `LOG-002` | Finite small-machine Busy Beaver `BB(6)` Antihydra / Collatz-like decider verification stubs in Pure Lean 4.35.0. | Finite decider proof compiles with 0 `sorry` | **PROPOSED** |

## Negative / Falsified Results Ledger (Honest Epistemic Memory)
- **H-001 (`discard`, `2026-11-21`):** Pure lexical staged Phrase→AND→OR FTS5 BM25 yielded `0.00` lift on the 25-query benchmark (`rag_mrr5 = 89.33`, `21/25` top-1) because repeated query tokens and long niche records outscored canonical high-degree hubs (`NT-001`, `ASTRO-001`, `LOG-001`, `CM-001`). Diagnosing this failure directly produced winning hypothesis **H-001b** (`rag_mrr5 = 96.00`, `23/25` top-1).
