# Threat Model (`docs/threat-model.md`)

| Threat ID | Threat | Impact | Mitigations |
|---|---|---|---|
| **T1** | **Epistemic inflation / false retirement** (marking an unverified AI claim or preprint as "solved") | Misleading scientific registry | All 12 Nov 2026 AI claims locked under `verification_flag = "ai-claim-under-audit-nov2026"` (`test_nov2026_ai_claims_explicitly_flagged`); explicit `0/1,900` solved audit in `docs/0THERNES_SOLVED_AUDIT_2026-11-25.md`. |
| **T2** | **AutoResearch reward hacking** (agent alters evaluator or tests to inflate `AQS`) | Invalid benchmark score | `AGENTS.md` locks `autoresearch/evaluate.py`, `schema/*.json`, and `tests/test_mega_atlas.py`; SHA-256 of `autoresearch/evaluate.py` pinned in `CHECKSUMS.sha256`; anti-gaming gate formally proved in `MegaAtlasProofs.AutoResearchInvariants.failed_gates_always_discard`. |
| **T3** | **Graph / schema corruption** (dangling `raw_links`, articulation points, duplicate IDs) | Broken RAG hops and connectome metrics | Enforced on every push by `src/v2_loader.py`, `scripts/forensic_audit.py`, `schema/problem.schema.json`, and 25+ pytest assertions. |
| **T4** | **Lean 4 invariant bypass** (`sorry`, `admit`, `native_decide`, custom axioms) | Broken formal proofs | Comment-stripped forbidden-token scan + exact 72-theorem axiom allowlist (`[propext, Quot.sound]`) in `scripts/audit_atlas.py` and `.github/workflows/ci.yml`. |
| **T5** | **SQL injection / malformed JSON-RPC in offline RAG or MCP server** | Local crash or bad query execution | Parameterized SQLite queries in `rag/query.py`; strict JSON-RPC 2.0 input validation & dual NDJSON/`Content-Length` stdio tests in `tests/test_mega_atlas.py`; zero network sockets exposed. |
| **T6** | **Secret leakage or tampered releases** | Supply-chain compromise | `gitleaks` report-only scan in CI; `SHA256SUMS` + Sigstore SLSA attestations in `.github/workflows/release.yml`. |
