# Threat Model & Security Analysis (Build Standard B36)

This repository is an offline-first scientific dataset, Lean 4.35.0 proof suite, static HTML/JS web dashboard, SQLite FTS5 RAG CLI, and local stdio MCP JSON-RPC 2.0 server. It runs **no public web backend, handles zero user authentication or PII, and makes zero runtime outbound network calls**.

## 1. STRIDE Analysis Across Trust Boundaries

| Surface | Threat (STRIDE) | Concrete Risk | Mitigation Implemented |
|---|---|---|---|
| **MCP Stdio Server (`mcp_server/server.py`)** | Tampering / Injection | Malformed JSON-RPC, invalid `Content-Length`, SQL injection via `query`, `pillar`, `substrate`, or `metric` arguments | Strict parameterized SQLite `?` bindings; allowlist validation on `metric` enum (`allowed = {...}`); clamped integer `limit`/`top`/`hops`; structured JSON-RPC `-32700`/`-32601` & `isError: true` error handling; negative boundary tests in `tests/test_properties_and_differential.py`. |
| **SQLite FTS5 Query (`rag/query.py`)** | DoS / FTS5 Syntax Injection | Special characters (`"`, `*`, `NEAR/`, unbalanced parens) crashing FTS5 `MATCH` | `tokenize_query()` strips non-alphanumeric chars via `re.findall(r"[A-Za-z0-9_]+", raw)` and wraps every token in safe double quotes before `MATCH ?`. |
| **Interactive Web Atlas (`outputs/MegaAtlas_Interactive_Dashboard_V2.html`)** | Cross-Site Scripting (XSS) | Malicious HTML/script payloads inside problem fields or `</script>` breakout | Every dynamic text interpolation passes through `esc()` HTML entity escaping in JS and `html.escape()` in Python; embedded JSON escapes `</` as `<\/`. Static read-only page with zero user-submitted backend persistence. |
| **Lean 4.35.0 Formal Proofs (`lean/`)** | Spoofing / Proof Forgery | Hidden `sorry`, `admit`, `native_decide`, `Lean.ofReduceBool`, custom `axiom` (including modifier-prefixed `private axiom`), or statement drift between paper and proof | Hardened H46 zero-`sorry`/`admit`/`native_decide`/`axiom` scanner in `scripts/audit_atlas.py` & `tests/test_mega_atlas.py`; verbatim `#print axioms` drift checker (`scripts/check_readme_axioms.py`); live negative kernel rejection test; 6 independent proof kernels + `leanchecker --fresh` via `scripts/verify_lean_six_kernels.sh`. |
| **Supply Chain / Release Artifacts** | Tampering / Repudiation | Corrupted PDF, arXiv tarball, or dataset files after build | `CHECKSUMS.sha256` + DigiCert RFC 3161 `.tsr` timestamp (`CHECKSUMS.sha256.tsr`) + `data/MANIFEST.sha256` verified in CI; deterministic archives (`mtime=0`); GitHub `actions/attest-build-provenance@v2` SLSA provenance attestations on `main` pushes. |
| **Optional Zenodo Token (`scripts/publish_zenodo.py`)** | Information Disclosure | Accidental secret commit to git | `.env` gitignored; `.env.example` contains empty placeholders only; CI runs regex secret-leak scan (`ghp_`, `sk-`, `AKIA`, private key headers). |

## 2. OWASP LLM / Agentic Consumption Risks (MCP & `llms.txt`)

- **Prompt Injection via Corpus Text:** Because the corpus is authored and audited statically in `src/v2_data/`, all 1,900 records are deterministic and git-versioned. MCP tool responses return structured JSON strictly tagged with `verification_flag`, `ai_disclosure`, and `conflict_of_interest_disclosure` so consuming agents cannot conflate editorial estimates or unverified AI claims with peer-reviewed facts.
- **Reward Hacking in AutoResearch:** Immutable `autoresearch/evaluate.py` + Lean-verified `failed_gates_always_discard` theorem prevent an autonomous agent from inflating `AQS` while breaking schema, biconnectivity, or Lean zero-sorry gates.
