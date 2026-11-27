# AI-Assistance Transparency, Export-Control & Venue Disclosure Policy (`v2.11.0`)

**Principal Author & Responsible Human-in-the-Loop:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))

## 1. Transparent Disclosure of Independent Human + AI-Assisted Authorship

This project is built by an **independent solo researcher working with frontier AI coding and research assistants (`Gemini / Antigravity`, alongside an external `Claude` statement audit)**. Rather than obscuring AI involvement—or inflating AI outputs into pretended institutional peer review—this repository adheres to full disclosure:

- **Human Role (Alexander Stephen Donahue — sole author):** Conceived the project and its `v2.0`–`v2.11` cross-disciplinary scope, enforced benchmarking against primary registries (`Left to Solve` / `formal-conjectures`, `ProofAtlas.ai`, `erdosproblems.com`, Clay CMI, Kourovka, Kirby), established the November 2026 AI proof-claim containment policy and daily automated registry sync architecture, mandated dual-licensing (`CC-BY-4.0` / `Apache-2.0`), directed the Lean 4.35.0 software-model invariant & adversarial-refutation suite and multi-cycle adversarial hardening reviews, verified visual & typesetting outputs, and assumes sole scholarly accountability.
- **AI Role (Disclosed Tooling Assistance — non-author):** Parallel drafting and structuring of domain modules (`m01`–`m12`), initial editorial rubric scoring, Python pipeline/RAG/MCP/oracle/test/daily-sync engineering, Lean 4.35.0 tactic proof drafting & witness scaffolding, adversarial statement auditing, and AMS-LaTeX typesetting under human supervision.

## 2. Venue-Specific AI Disclosure Alignment (Playbook v1.3 Item 40)

- **Zenodo Policy Compliance:** This repository documents human-directed independent scholarly curation, deterministic software engineering, and machine-checked software-model formal verification with disclosed AI tooling assistance—NOT autonomous AI-authored paper generation. No Zenodo deposit or DOI is claimed prior to verified external assignment.
- **JOSS / Software-Venue Disclosure:** Tools used (`Gemini / Antigravity`, external `Claude` audit), exact scope (code/proof/audit/draft assistance), and human core design/verification ownership are explicitly documented above and in `lean/formalization.yaml`.
- **Mathlib / Lean Zulip Rules:** Zero Mathlib dependency (`lean/` uses Lean 4.35.0 core only). Any future upstream Mathlib contribution derived from helper lemmas would be explicitly labeled `LLM-generated` with all editorial/reviewer correspondence written directly by the human author.

## 3. Mandatory Anti-Hallucination & Integrity Guardrails

1. **Strict Machine-Checked Schema (`schema/problem.schema.json`):** Every single one of the `2,000` records (`48` typed columns) must pass JSON Schema Draft 2020-12 validation in CI.
2. **Lean 4.35.0 Software-Model Invariants & Adversarial Refutations (`lean/`):** All **103** audited declarations (of `117` in `lean/`: `72` core + `12` NonVacuity + `10` AdversarialTests + `9` Palomar targets) compile with `0` `sorry`, `0` `native_decide`, per-theorem axioms `⊆ [propext, Quot.sound]`; they are kernel-checked by Lean, and the `9` comparator targets pass `6` kernel checks across `5` distinct implementations via `scripts/verify_lean_six_kernels.sh` (+ live negative kernel rejection). They concern the scoring software model only, not the atlas data or graph.
3. **Differential Reference Oracle & 100% Mutation Testing (`reference/`, `scripts/run_mutation_audit.py`):** 50-digit `Decimal`/`Fraction` differential verification across `2,000+` cases, 1,000-example Hypothesis property checks, and `14/14` semantic mutation-kill auditing.
4. **Per-Record Verification Flags (`verification_flag`):** Every record explicitly declares `primary-registry-indexed` (`1,035`), `ai-assisted-editorial-synthesis` (`942`), `ai-claim-under-audit-nov2026` (`12`), or `disputed-human-claim` (`11`).
5. **Conservative November 27, 2026 Proof-Claim Containment:** Zero (`0/2,000`) overarching problems—including all 12 Fall/Nov 2026 AI proof-claim targets and the parent IDs of all `20` companion archive rows covering all `27` other audited entries in Cycle-3 [`RESULTS.md`](https://github.com/0thernes/0thernes-research-archive/blob/main/RESULTS.md) (`94` results across `28` entries)—are marked solved or retired.
6. **Live Title-Verified Citations, Retractions & Structural Dual Timestamps:** `scripts/check_citations.py` verifies `15/15` BibTeX URLs/DOIs live with Crossref/Zenodo title-token parity and `0` retractions; `CHECKSUMS.sha256` (`78` frozen files) & `data/MANIFEST.sha256` (`13` files) verify byte-exact artifact integrity (daily telemetry files isolated outside frozen seals); structurally verified DigiCert RFC 3161 (`CHECKSUMS.sha256.tsr`, ASN.1) + 3-calendar Bitcoin OpenTimestamps v1 (`CHECKSUMS.sha256.ots`, full binary tree) timestamp `CHECKSUMS.sha256` (verified by `scripts/stamp_timestamps.py --verify`); GitHub `actions/attest-build-provenance@v4` issues SLSA attestations on the frozen PDF, arXiv tarball, Lean axiom report, checksums, `.tsr`, and `.ots`.
7. **Zero Fabricated Credentials:** No fake DOIs, no fabricated peer review, no fake legal entities, and no programmatic bypassing of external anti-bot/PoW gates.

## 4. Export-Control Self-Screen (Playbook v1.3 Item 37)

- **Self-Screen Result (2026-11-27):** All datasets, mathematical/scientific open-problem summaries, Lean 4.35.0 arithmetic/graph invariant proofs, Python retrieval utilities, and documentation in this repository consist strictly of publicly available, open-licensed fundamental research metadata and verification software intended for unrestricted public sharing (**15 CFR 734.8** fundamental research scope). The repository contains **zero** encryption implementation source code, zero weapon/aerospace/nuclear engineering blueprints, and zero controlled technical data under EAR/ITAR.

## 5. Redacted AI Workflow & Session Provenance Log (Playbook v1.3 Item 33)

To preserve auditability without exposing secrets, API tokens, local drive paths, or third-party personal data (unredacted local conversation logs remain private off-repo), every human-directed AI-assisted release cycle is bound publicly to its immutable git commit, audit ledger, and SHA-256 manifest:

| Release | Date (UTC) | Disclosed Assistant | Redacted Scope of AI Assistance | Public Cryptographic Anchor |
|---|---|---|---|---|
| `v2.4.0` | 2026-11-25 | `Gemini / Antigravity` | Lean 4.35.0 Palomar upgrade (`92` thms), AMS-LaTeX white paper, 50-digit oracle, mutation audit, `<5 MB` HTML refactor | Commit `f838db1` · CI `#45728933812` |
| `v2.5.0` | 2026-11-26 | `Gemini / Antigravity` | Round 2 hostile-referee audit (`H-401`–`H-411`), `AdversarialTests.lean` (`103` thms), Crossref retraction checks, 100% SPDX headers | Commit `ceeee0c` · CI `#45743507132` |
| `v2.6.0` | 2026-11-26 | `Gemini / Antigravity` | Round 3 3-cycle audit (`H-501`–`H-527`), `leanchecker --fresh` + live negative Lean rejection, DigiCert RFC 3161 `.tsr`, 10-page PDF visual QA | Commit `d23b4d7` · CI `#45749252063` |
| `v2.7.0` | 2026-11-26 | `Gemini / Antigravity` | Round 4 3-cycle audit (`H-601`–`H-614`), 76-repo/16-entry archive sync, dual RFC 3161 `.tsr` + 3-calendar Bitcoin `.ots`, strict CSP, MCP/RAG hardening | Commit `541f093` · CI `#45806252859` |
| `v2.8.0` | 2026-11-26 | `Gemini / Antigravity` | 4-roadmap release: archive sync (`17` rows), `sync_external_registries.py`, Track B `NT-005`/Ramsey probes, `rubric_override_diff.py` + 11th MCP tool | Commit `9e16554` · Tag `v2.8.0` |
| `v2.9.0` | 2026-11-26 | `Claude` (statement audit `703e3db`/`ad3d5ed`) + `Gemini / Antigravity` (Round 6 cure + Left to Solve / daily sync) | Source-level cure of all statement-audit errata, Cycle-3 `20`-row `RESULTS.md` sync, primary RH/GRH sources, `COMB-001→COMB-002` fix, Left to Solve 25-front (`1,900→2,000` problems, `AQS 98.35`) & automated daily 16-registry sync, 12-tool MCP, RAG/rubric/timestamp/citation hardening, `10/10` mutants, `83` pytest checks | Commit `af0a850` · Tag `v2.9.0` · CI `#45946262545` |
| `v2.10.0` | 2026-11-27 | `Gemini / Antigravity` | Round 7 3-cycle audit (`H-901`–`H-913`): 100/100 verbatim Left to Solve mirror parity (eliminated 3 duplicates & 2 overlaps, `199→290` crosswalk matches across `59,396` targets), sovereign target radar (`d66bcb0`), 13-tool MCP validation/path containment, dashboard mirror links, Node 24 workflows, `12/12` mutants, `109` pytest checks | Commit `0436349` · Tag `v2.10.0` · CI `#46015278037` |
| `v2.11.0` | 2026-11-27 | `Gemini / Antigravity` | Round 8 3-cycle audit (`H-1001`–`H-1015`): live 26-front daily-sync resilience (`62,790` targets, `291` crosswalk matches, advisory `external_solved_signals` table w/ zero auto-retirement, full `pytest` in daily sync), MCP `-32602` non-object `params` cure, atomic SQLite FTS5 rebuild, 5 `mypy --check-untyped-defs` fixes in `v2_charts.py`, 100% non-exempt SPDX headers, paper/BibTeX/Chart 11/doc `@v4` & `1,711`-line parity, `14/14` mutants, `115` pytest checks | Tag `v2.11.0` · `CHECKSUMS.sha256` + `.tsr` + `.ots` |

## 6. Open External Review Invitation

External domain-expert critiques and falsification diffs are welcomed via GitHub Issues (`.github/ISSUE_TEMPLATE/academic-review.yml`) and [`docs/ACADEMIC_REVIEW.md`](ACADEMIC_REVIEW.md).
