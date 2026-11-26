# AI-Assistance Transparency, Export-Control & Venue Disclosure Policy (`v2.5.0`)

**Principal Author & Responsible Human-in-the-Loop:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA` · ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))

## 1. Transparent Disclosure of Independent Human + AI-Assisted Authorship

This project is built by an **independent solo researcher working with frontier AI coding and research assistants (`Gemini / Antigravity`)**. Rather than obscuring AI involvement—or inflating AI outputs into pretended institutional peer review—this repository adheres to full disclosure:

- **Human Role (Alexander Stephen Donahue — sole author):** Conceived the project and its `v2.0`–`v2.5` cross-disciplinary scope, enforced benchmarking against primary registries (`ProofAtlas.ai`, `erdosproblems.com`, Clay CMI, Kourovka, Kirby), established the November 2026 AI proof-claim containment policy, mandated dual-licensing (`CC-BY-4.0` / `Apache-2.0`), directed the 6-kernel Pure Lean 4.35.0 formal invariant & adversarial-refutation suite and multi-cycle adversarial hardening reviews, verified visual & typesetting outputs, and assumes sole scholarly accountability.
- **AI Role (Disclosed Tooling Assistance — non-author):** Parallel drafting and structuring of domain modules (`m01`–`m11`), initial editorial rubric scoring, Python pipeline/RAG/MCP/oracle/test engineering, Lean 4.35.0 tactic proof drafting & witness scaffolding (independently audited across 6 proof kernels), and AMS-LaTeX typesetting under human supervision.

## 2. Venue-Specific AI Disclosure Alignment (Playbook v1.3 Item 40)

- **Zenodo Policy Compliance:** This repository documents human-directed independent scholarly curation, deterministic software engineering, and machine-checked formal verification with disclosed AI tooling assistance—NOT autonomous AI-authored paper generation. No Zenodo deposit or DOI is claimed prior to verified external assignment.
- **JOSS / Software-Venue Disclosure:** Tools used (`Gemini / Antigravity`), exact scope (code/proof/draft assistance), and human core design/verification ownership are explicitly documented above and in `lean/formalization.yaml`.
- **Mathlib / Lean Zulip Rules:** Zero Mathlib dependency (`lean/` uses Lean 4.35.0 core only). Any future upstream Mathlib contribution derived from helper lemmas would be explicitly labeled `LLM-generated` with all editorial/reviewer correspondence written directly by the human author.

## 3. Mandatory Anti-Hallucination & Integrity Guardrails

1. **Strict Machine-Checked Schema (`schema/problem.schema.json`):** Every single one of the `1,900` records (`48` typed columns) must pass JSON Schema Draft 2020-12 validation in CI.
2. **Six-Kernel Formal Lean 4.35.0 Invariants & Adversarial Refutations (`lean/`):** All **103** theorems (`72` core + `12` NonVacuity + `10` AdversarialTests + `9` Palomar targets) compile with `0` `sorry` in `lean/`, `0` `native_decide`, axioms strictly `⊆ [propext, Quot.sound]`, across `6/6` independent kernels via `scripts/verify_lean_six_kernels.sh`.
3. **Differential Reference Oracle & 100% Mutation Testing (`reference/`, `scripts/run_mutation_audit.py`):** 50-digit `Decimal`/`Fraction` differential verification across `2,000+` cases, 1,000-example Hypothesis property checks, and `6/6` mutation-kill auditing.
4. **Per-Record Verification Flags (`verification_flag`):** Every record explicitly declares `primary-registry-indexed` (`925`), `ai-assisted-editorial-synthesis` (`952`), `ai-claim-under-audit-nov2026` (`12`), or `disputed-human-claim` (`11`).
5. **Conservative November 25, 2026 Proof-Claim Containment:** Zero (`0/1,900`) overarching problems—including all 12 Fall/Nov 2026 AI proof-claim targets and the parent IDs of all 10 companion archive entries—are marked solved or retired.
6. **Live Citation, Retraction & Cryptographic Auditing:** `scripts/check_citations.py` verifies `12/12` BibTeX URLs/DOIs live with `0` Crossref retractions; `CHECKSUMS.sha256` & `data/MANIFEST.sha256` verify byte-exact artifact integrity; GitHub `actions/attest-build-provenance@v2` issues SLSA attestations on the frozen PDF, arXiv tarball, Lean axiom report, and checksums.
7. **Zero Fabricated Credentials:** No fake DOIs, no fabricated peer review, no fake legal entities, and no programmatic bypassing of external anti-bot/PoW gates.

## 4. Export-Control Self-Screen (Playbook v1.3 Item 37)

- **Self-Screen Result (2026-11-25):** All datasets, mathematical/scientific open-problem summaries, Lean 4.35.0 arithmetic/graph invariant proofs, Python retrieval utilities, and documentation in this repository consist strictly of publicly available, open-licensed fundamental research metadata and verification software intended for unrestricted public sharing (**15 CFR 734.8** fundamental research scope). The repository contains **zero** encryption implementation source code, zero weapon/aerospace/nuclear engineering blueprints, and zero controlled technical data under EAR/ITAR.

## 5. Open External Review Invitation

External domain-expert critiques and falsification diffs are welcomed via GitHub Issues (`.github/ISSUE_TEMPLATE/academic-review.yml`) and [`docs/ACADEMIC_REVIEW.md`](ACADEMIC_REVIEW.md).
