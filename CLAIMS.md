# Claims Ledger (`CLAIMS.md`)

Every structural, formal, algorithmic, and epistemic claim made by **Unsolved Problems Mega-Atlas** is numbered, paired with verifiable evidence, and paired with an explicit falsification criterion (**what would prove us wrong**).

| ID | Claim | Verification Tier | Evidence | What Would Prove Us Wrong |
|---|---|---|---|---|
| **C1** | The dataset contains exactly `1,900` unique, strictly deduplicated problems across `8` Macro-Pillars, `28` Superdomains, `8` Substrates, and `7` Abstraction Layers (`48` typed fields), with `0` JSON Schema Draft 2020-12 errors and `0` unresolved `raw_links`. | **Automated schema & exact audit** | `tests/test_mega_atlas.py`, `scripts/audit_atlas.py`, `scripts/forensic_audit.py` | Any duplicate `id`, missing column, JSON Schema violation, or dangling `raw_links` reference. |
| **C2** | The `5,808`-edge undirected connectome has `1` connected component, `0` articulation points, and `0` bridge edges (true 2-vertex-connected biconnected graph), satisfying the Handshaking Lemma $\sum \deg = 2|E|$. | **Exact NetworkX audit + Lean 4 theorem** | `test_graph_biconnectivity_and_handshaking`, `MegaAtlasProofs.GraphInvariants` | Any disconnected vertex, articulation point, bridge edge, or degree-sum discrepancy. |
| **C3** | All `72` formal invariant theorems in `lean/MegaAtlasProofs/` compile in Pure Lean 4.35.0 (zero Mathlib, zero `sorry`, zero `admit`, zero `native_decide`, zero `Classical.choice`, axioms strictly within `[propext, Quot.sound]` or empty). | **Kernel-checked Lean 4.35.0** | `lean/MegaAtlasProofs/VerifyAxioms.lean`, `.github/workflows/ci.yml` | Any forbidden Lean token, missing theorem, or axiom outside `[propext, Quot.sound]`. |
| **C4** | The offline Hybrid BM25 + Title-Bigram + PageRank RAG engine achieves `100.0% MRR@5` (`25/25` top-1) on the immutable 25-query cross-pillar benchmark (`autoresearch/evaluate.py`, `AQS = 97.99`), and the dual-framed 9-tool MCP stdio server passes both NDJSON and `Content-Length` JSON-RPC 2.0 tests. | **Automated deterministic pytest + AutoResearch oracle** | `autoresearch/evaluate.py --verify-gates`, `test_mcp_stdio_server_*` | Any query dropping below top-1, `AQS < 97.0`, or JSON-RPC framing failure. |
| **C5** | Zero of the `1,900` open problems are claimed solved or retired by this repository (including all `12` Fall/Nov 2026 AI proof claims under `verification_flag = "ai-claim-under-audit-nov2026"` and the 2026-11-25 audit of `0thernes-research-archive`). | **Explicit epistemic audit** | `test_nov2026_ai_claims_explicitly_flagged`, `docs/0THERNES_SOLVED_AUDIT_2026-11-25.md` | Any record falsely claiming retirement of an unverified AI claim or unreviewed preprint. |
| **C6** | All frozen artifacts across CSV, TSV, JSON, JSONL, SQLite+FTS5, 14-sheet XLSX, 8-sheet XLS, 30 charts, FAIR metadata (`croissant.json`, `ro-crate-metadata.json`, `.zenodo.json`), and monographs match byte-exact SHA-256 checksums (`CHECKSUMS.sha256` and `data/MANIFEST.sha256`). | **Cryptographic SHA-256 check** | `scripts/audit_atlas.py`, `test_sha256_checksums_manifest_exact`, `test_croissant_json_ld_and_sha256_parity` | Any SHA-256 mismatch or cross-format row/column drift. |

## Explicit Falsification Protocol (What Would Prove Us Wrong)

Any of the following refutes a claim above and will be logged in `CHANGELOG.md` and corrected immediately:
1. A failing record against `schema/problem.schema.json` or an unresolved graph edge in `src/v2_loader.py`.
2. A Lean 4 kernel rejection, forbidden token, or disallowed axiom in `lean/MegaAtlasProofs/`.
3. A SHA-256 mismatch in `CHECKSUMS.sha256`, `data/MANIFEST.sha256`, or `croissant.json`.
4. A demonstrated factual error in a problem's historical status, domain taxonomy, or 2026 AI-claim verification flag (report via `.github/ISSUE_TEMPLATE/status-update-or-falsification.yml`).
