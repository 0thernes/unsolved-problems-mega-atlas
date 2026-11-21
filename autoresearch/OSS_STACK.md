# Popular Open-Source Research Stack & Ecosystem Integration Guide

This atlas is engineered to interoperate cleanly with the leading 2025–2026 open-source GitHub repositories for **autonomous scientific research**, **Lean 4 formal verification**, **open-problem registries**, and **FAIR AI-ready datasets**.

---

## 1. Autonomous Scientific Research Loops

| OSS Repository | Pattern Adopted / Integrated | How It Connects to This Repo |
|---|---|---|
| **[`karpathy/autoresearch`](https://github.com/karpathy/autoresearch)** | Minimal `program.md` + immutable evaluation oracle + `results.tsv` keep/discard git ratchet | **Baked in natively** under [`autoresearch/program.md`](program.md), immutable [`autoresearch/evaluate.py`](evaluate.py), and empirical [`autoresearch/results.tsv`](results.tsv), with anti-gaming keep/discard invariants formally proved in [`lean/MegaAtlasProofs/AutoResearchInvariants.lean`](../lean/MegaAtlasProofs/AutoResearchInvariants.lean). |
| **[`SakanaAI/AI-Scientist`](https://github.com/SakanaAI/AI-Scientist)** | End-to-end hypothesis → experiment → automated review → structured white paper | Connects to Track B problem exploration (`research/runs/<PROBLEM_ID>/`) using our SQLite FTS5 RAG (`rag/query.py`) and MCP server (`mcp_server/server.py`) to ground literature reviews in exact Problem IDs and bottlenecks rather than hallucinations. |
| **[`AI4Scientist/awesome-autoresearch`](https://github.com/AI4Scientist/awesome-autoresearch)** | Benchmark & autonomous lab ecosystem index | Use this atlas's `MegaAtlas_Unsolved_Problems_V2.jsonl` + `croissant.json` as a cross-disciplinary problem-selection & RAG benchmark corpus. |

## 2. Lean 4 Formal Verification, Autoformalization & Independent Kernels

| OSS Repository | Pattern Adopted / Integrated | How It Connects to This Repo |
|---|---|---|
| **[`leanprover/skills`](https://github.com/leanprover/skills)** | Official Lean 4 agent authoring & debugging skills | Complements [`AGENTS.md`](../AGENTS.md) and [`lean/README.md`](../lean/README.md) for zero-`sorry`, zero-`native_decide` Lean 4.35.0 development. |
| **[`kripner/OpenProver`](https://github.com/kripner/OpenProver)** | Planner–Worker–Verifier architecture with shared Whiteboard scratchpad | **Baked in natively** via [`autoresearch/whiteboard.md`](whiteboard.md) and Track B Planner–Worker–Verifier protocol in `program.md`. |
| **[`lean-dojo/LeanAgent`](https://github.com/lean-dojo/LeanAgent)** | Lifelong premise retrieval across expanding Lean repositories | Compatible with `lean/MegaAtlasProofs/` and downstream Lean 4 problem repositories linked via `0thernes-research-archive`. |
| **[`epfl-lara/AutoformalizedProjects`](https://github.com/epfl-lara/AutoformalizedProjects)** | End-to-end zero-`sorry` LeanFlow formalization discipline | Matches our strict `#print axioms` CI gate (`.github/workflows/ci.yml`) auditing all 58 theorems on every commit. |
| **Independent Lean Kernels (`lean4lean`, `nanoda`, `con-leche`) & [`scottnarmstrong/yang-mills-informalization`](https://github.com/scottnarmstrong/yang-mills-informalization)** | Cross-kernel verification & natural-language statement-fidelity auditing | Directly informs our November 20, 2026 verification boundary: never equate single-kernel compilation of massive AI proof dumps with human statement-fidelity verification. |

## 3. Open-Problem Registries & Upstream Provenance Trackers

| Registry / Repo | Role | Sync Path |
|---|---|---|
| **[`ProofAtlas.ai`](https://proofatlas.ai/open-problems/)** | 1,100+ eligible open math problems (243 open in Top-500) | Benchmarked in `registries_nov2026` table; primary provenance tag `ProofAtlas`. |
| **[`teorth/erdosproblems`](https://github.com/teorth/erdosproblems) (`erdosproblems.com`)** | ~1,221 Erdős problems with Lean 4 formal tracking | Benchmarked in `registries_nov2026` & `AUDIT-06` (gold standard for human-auditable concise Lean closures). |
| **[`0thernes/unsolved-mathematics`](https://github.com/0thernes/unsolved-mathematics)** | Sibling deep-dive pure-math atlas with adversarial QA case studies | Shares the exact **0thernes Composite Severity Score (`CSS`)** formula and epistemic honesty ethic. |
| **[`0thernes/0thernes-research-archive`](https://github.com/0thernes/0thernes-research-archive)** | Cryptographically audited master research vault (ORCID `0009-0006-8168-9648`) | Pins this repository as Tier-II Build **`0TH-BUILD-007`** with SHA-256 frozen white paper, ranking, and verification dossier. |

## 4. FAIR Datasets, Scholarly Preservation & AI-Agent Interoperability

| Standard / Ecosystem | File in This Repository | Purpose |
|---|---|---|
| **Zenodo GitHub Auto-DOI** | [`.zenodo.json`](../.zenodo.json) | Automatically populates ORCID, creators, license, and metadata on every GitHub Release. |
| **MLCommons Croissant 1.0 (`mlcommons/croissant`)** | [`croissant.json`](../croissant.json) | Machine-readable JSON-LD dataset metadata for HuggingFace, Kaggle, Google Dataset Search & ML pipelines. |
| **W3C RO-Crate 1.1 (`ResearchObject/ro-crate`)** | [`ro-crate-metadata.json`](../ro-crate-metadata.json) | FAIR Research Object graph linking author ORCID, Lean 4 proofs, SQLite DB, PDF monograph, and SHA-256 checksums. |
| **Datasheets for Datasets (Gebru et al.)** | [`docs/DATASHEET.md`](../docs/DATASHEET.md) | Standardized transparency documentation (motivation, composition, collection, uses, maintenance). |
| **Model Context Protocol (`modelcontextprotocol`)** | [`mcp_server/server.py`](../mcp_server/server.py) | Zero-dependency stdio JSON-RPC 2.0 server exposing 7 live knowledge-graph & RAG tools to Claude Code, Antigravity, Cursor & Gemini CLI. |
| **`AGENTS.md` / `CLAUDE.md` / `llms.txt`** | [`AGENTS.md`](../AGENTS.md), [`CLAUDE.md`](../CLAUDE.md), [`llms.txt`](../llms.txt) | Instant onboarding and epistemic boundary enforcement for any AI coding or research agent. |
