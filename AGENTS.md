# AGENTS.md — AI Coding & Research Agent Onboarding Contract

> Standard repository instructions for Claude Code, Antigravity, Cursor, Codex, Gemini CLI, and autonomous research agents working inside **`0thernes/unsolved-problems-mega-atlas`**.

## 1. Canonical Identity & Attribution (MANDATORY)

- **Author / Human-in-the-Loop:** Alexander Stephen Donahue (`Alexander S. Donahue`)
- **ORCID:** `0009-0006-8168-9648` (`https://orcid.org/0009-0006-8168-9648`)
- **Affiliation:** 0thernes LLC, Spokane, WA, USA · `0_0@0thernes.art` · `https://0thernes.art`
- **Master Research Archive:** `0TH-BUILD-007` in `https://github.com/0thernes/0thernes-research-archive`
- **Dual License:** Data/Prose/Charts/PDF (`CC BY 4.0`, `LICENSE`) · Code/Schemas/RAG/MCP/Lean (`MIT`, `LICENSE-CODE`).

## 2. Non-Negotiable Epistemic & Verification Rules

1. **Zero Proof Inflation:** Never claim to prove, solve, or retire any of the 1,855 open problems. All 12 Fall/Nov 2026 AI proof-claim targets (`verification_flag = "ai-claim-under-audit-nov2026"`) MUST stay explicitly unretired pending independent formal-statement fidelity and peer consensus.
2. **Pure Lean 4.35.0 Hygiene (`lean/`):** Zero Mathlib, zero `sorry`, zero `admit`, zero `native_decide`, zero custom `axiom` declarations. Every theorem must be listed in `lean/MegaAtlasProofs/VerifyAxioms.lean` and depend strictly on `[propext, Quot.sound]` or empty.
3. **Anti-Gaming Harness Lock:** During autonomous optimization loops (`autoresearch/program.md`), **NEVER modify** `autoresearch/evaluate.py`, `schema/*.json`, `tests/test_mega_atlas.py` (never weaken assertions), or `VERIFICATION.md`.
4. **Honest AI Disclosure:** Never fabricate DOIs, peer-review endorsements, or fake external citations. Preserve negative/discarded experiment rows in `autoresearch/results.tsv`.
5. **ReFS Dev Drive & Windows PowerShell Safety:** When running on Windows in bracketed paths, always use `-LiteralPath`. Keep virtual environments inside `.venv/` (gitignored).

## 3. Built-In Agentic Tools & Fast Commands

```bash
# Offline Hybrid BM25 + Graph-Authority RAG CLI (<30 ms, zero API keys)
python rag/query.py "turbulence climate sensitivity" --top 6 --hops 1
python rag/query.py --compare NT-001 CS-001
python rag/query.py --flag ai-claim-under-audit-nov2026 --top 20

# Model Context Protocol (MCP) stdio JSON-RPC 2.0 server (7 live tools)
python mcp_server/server.py

# Immutable Karpathy-style AutoResearch Evaluator
python autoresearch/evaluate.py --verify-gates

# Full Verification Pipeline (must pass before any commit/PR)
cd lean && lake build && cd ..
python scripts/generate_fair_metadata.py
python scripts/audit_atlas.py --sync-checksums --check-lean
pytest -v
```

## 4. Autonomous Research Loop Entry Point

To run autonomous optimization or open-problem investigation cycles, read [`autoresearch/program.md`](autoresearch/program.md), inspect [`autoresearch/results.tsv`](autoresearch/results.tsv) and [`autoresearch/whiteboard.md`](autoresearch/whiteboard.md), and follow the strict keep/discard git ratchet proved in `MegaAtlasProofs.AutoResearchInvariants.shouldKeep_iff`.
