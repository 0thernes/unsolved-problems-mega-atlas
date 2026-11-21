# AI-Assistance Transparency & Epistemic Containment Policy

**Curator & Responsible Human-in-the-Loop:** Alexander Stephen Donahue (`0thernes LLC`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))

## 1. Transparent Disclosure of Solo Human + AI-Assisted Authorship

This project is built by an **independent solo researcher working with frontier AI assistants**. Rather than obscuring AI involvement—or inflating AI outputs into pretended institutional peer review—0thernes LLC adheres to full disclosure:

- **Human Role (Alexander Stephen Donahue):** Conceived the project and its V2.0/V2.1 cross-disciplinary scope, enforced benchmarking against primary registries (`ProofAtlas.ai`, `erdosproblems.com`, Clay CMI, Kourovka, Kirby), established the November 2026 AI proof-claim containment policy, mandated dual-licensing (`CC BY 4.0` / `MIT`), defined the 0thernes `CSS` unification and Pure Lean 4.35.0 formal invariant verification standard, reviewed visual outputs and audit results, and assumes sole editorial accountability.
- **AI Role (Disclosed Assistance):** Parallel drafting and structuring of the 10 domain modules (`m01`–`m10`), initial editorial rubric scoring, Python pipeline engineering (`v2_loader.py`, `v2_charts.py`, `v2_export_all.py`, `rag/query.py`, `tests/`, `scripts/audit_atlas.py`), and scaffolding of the Pure Lean 4.35.0 formal invariant suite (`lean/MegaAtlasProofs/`).

## 2. Mandatory Anti-Hallucination & Integrity Guardrails

Because AI-assisted large-scale synthesis carries known risks (citation drift, duplicate entries, overconfident status claims, silent schema corruption), this repository enforces **six hard engineering guardrails**:

1. **Strict Machine-Checked Schema (`schema/problem.schema.json`):** Every single one of the 1,855 records must pass JSON Schema Draft 2020-12 validation in CI.
2. **Formal Lean 4.35.0 Formula Verification (`lean/`):** Scoring, quadrant, era, taxonomy, and finite graph invariants are kernel-checked in Pure Lean 4.35.0 (`0 sorry`, `0 admit`, `0 native_decide`, strictly `[propext, Quot.sound]`).
3. **Per-Record Verification Flags (`verification_flag`):** Every record explicitly states whether it is `primary-registry-indexed`, `ai-assisted-editorial-synthesis`, `disputed-human-claim`, or `ai-claim-under-audit-nov2026`.
4. **Conservative November 2026 Proof-Claim Containment:** Zero problems targeted by Fall–November 2026 AI proof announcements (Navier–Stokes, Oct 6 722-manuscript dump, Nov 20 Alpöge/Claude Lean RH/GRH) are marked solved. Machine kernel compilation of massive un-audited Lean artifacts is explicitly distinguished from human formalization-fidelity review and community consensus.
5. **Cryptographic Immutability (`CHECKSUMS.sha256`):** Every generated dataset, chart, database, schema, ranking table, and monograph is SHA-256 hashed and audited on every push in GitHub Actions.
6. **Zero Fabricated Credentials:** No fake DOIs, no fabricated peer review, no fake institutional affiliations, and no programmatic bypassing of external anti-bot/PoW gates (e.g., Software Heritage Anubis).

## 3. Multi-Model & External Human Review Roadmap

Consistent with [`0thernes/unsolved-mathematics`](https://github.com/0thernes/unsolved-mathematics), future revisions (`v2.2+`) aim to run structured adversarial cross-model audits (comparing independent critiques across frontier model families) AND welcome human domain-expert audits via [`docs/ACADEMIC_REVIEW.md`](ACADEMIC_REVIEW.md), upgrading individual records to `human-expert-verified` only when an identified specialist with verifiable credentials signs off in a tracked PR.
