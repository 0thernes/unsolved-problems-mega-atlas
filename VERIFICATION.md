# Verification & Epistemic Boundaries

**Author / Curator:** Alexander Stephen Donahue (`0thernes LLC`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))  
**Release:** `v2.2.0` (November 21, 2026)

This document defines the **exact, non-negotiable epistemic boundary** between what is **machine-proved**, what is **programmatically audited**, what is **anchored to named external registries**, and what remains **curated editorial estimation or unverified frontier claims**.

---

## Five-Tier Epistemic Verification Ladder

| Tier | Verification Level | Scope in This Repository | Mechanism | What It Does **NOT** Prove |
|---:|---|---|---|---|
| **L1** | **Kernel-Checked Formal Proof (Pure Lean 4.35.0)** | Exact discrete invariants of `CSS`, antiquity 300-year saturation, `Titan Index`, `Near-Term Leverage`, 4-Quadrant exhaustiveness/monotonicity, `Q1` leverage bound `≥ 5.6`, 6-Era monotonicity, 8×28 taxonomy surjection, Handshaking Lemma (`∑ deg = 2|E|`), cross-pillar ≤ cross-superdomain ≤ `|E|`, deduplication bound, **AutoResearch `AQS` bounds & anti-gaming keep/discard ratchet**, and pairwise delta antisymmetry. | `lean/MegaAtlasProofs/` (**7 modules, 817 lines, 58 audited theorems**, zero Mathlib, zero `sorry`, zero `admit`, zero `native_decide`, `#print axioms` strictly within `[propext, Quot.sound]` or empty). | Does **NOT** prove or resolve any of the 1,855 open mathematical or scientific problems. |
| **L2** | **Deterministic Software & Cryptographic Audit** | All 1,855 record types/enums, JSON Schema Draft 2020-12 compliance, unique IDs, all 88 canonical hubs, single connected graph component (`1,855/1,855`), empirical Handshaking parity (`11,194 = 2 × 5,597`), PageRank mass conservation (`∑ PR ≈ 1.0`), CSV/TSV/JSON/JSONL/SQLite+FTS5/XLSX/XLS parity, RAG retrieval, ORCID presence, and byte-exact SHA-256 digests. | `pytest -v` (`tests/test_mega_atlas.py`), `python scripts/audit_atlas.py --check-lean`, `CHECKSUMS.sha256`, and GitHub Actions CI (`.github/workflows/ci.yml`). | Does **NOT** validate historical attribution dates, scientific consensus, or subjective rubric scores against external primary journals. |
| **L3** | **Primary-Registry Indexed (`primary-registry-indexed`)** | **687 problems** explicitly cross-referenced to canonical external trackers (Clay CMI, ProofAtlas, Erdős Problems DB, Hilbert, Smale, Landau, Kourovka, Kirby, Brass-Moser-Pach, SEP/PhilPapers, NAE, DARPA, DOE, IPCC, WHO, CERN, LIGO, IRDS, etc.). | `registry_source` provenance metadata + `verification_flag = "primary-registry-indexed"`. | Existence and prominence are registry-anchored, while numeric rubric scores remain editorial estimates (Tier L4). |
| **L4** | **AI-Assisted Editorial Synthesis (`ai-assisted-editorial-synthesis`)** | **1,145 frontier problems** and all quantitative rubric scores (`difficulty_score`, `tractability_2050`, `civilizational_impact`, `interdisciplinarity_index`, derived `CSS` and `Titan Index`). | Directed by solo human curator Alexander S. Donahue with disclosed AI assistance; fully editable & falsifiable via PRs. | **Not human-peer-reviewed.** Must be treated as structured research infrastructure and falsifiable editorial estimates. |
| **L5** | **Unverified Frontier Proof Claims (`ai-claim-under-audit-nov2026` / `disputed-human-claim`)** | **12 Fall/Nov 2026 AI proof claims** (including Sept 8 OpenAI Navier–Stokes, Oct 6 722-manuscript bulk dump targets, and Nov 20 Alpöge/Claude Lean RH/GRH + Masullo human draft) + **11 disputed human claims** (e.g., abc/IUT). | Isolated via dedicated `status_2026`, `verification_flag`, and the 6-item `ai_verification_audit_nov2026` ledger. | **Explicitly NOT retired as solved.** Machine kernel compilation of a multi-million-line Lean archive checks logical deduction, not statement fidelity or peer consensus. |

---

## Pure Lean 4.35.0 Formal Audit Summary

- **Toolchain:** `leanprover/lean4:v4.35.0` (zero external dependencies; zero Mathlib)
- **Entry Point:** `lean/MegaAtlasProofs.lean`
- **Axiom Audit File:** `lean/MegaAtlasProofs/VerifyAxioms.lean`
- **Modules (7 files, 817 lines):**
  1. `MegaAtlasProofs/Scoring.lean` (159 lines) — 22 theorems (`CSS`, antiquity saturation, `Titan Index`, `Near-Term Leverage`)
  2. `MegaAtlasProofs/Quadrants.lean` (139 lines) — 11 theorems (4-Quadrant partition & `Q1 ≥ 5.6` leverage, 6-Era monotonicity)
  3. `MegaAtlasProofs/Taxonomy.lean` (138 lines) — 8 theorems (8×28 surjection, partition `[5,3,3,3,3,4,4,3]` summing to 28, cross-pillar separation)
  4. `MegaAtlasProofs/GraphInvariants.lean` (173 lines) — 5 theorems (finite Handshaking Lemma, cross-partition edge hierarchy, deduplication cardinality bound)
  5. `MegaAtlasProofs/AutoResearchInvariants.lean` (115 lines) — 12 theorems (`AQS` bounds & monotonicity, anti-reward-hacking `failed_gates_always_discard`, strict improvement `shouldKeep_iff`, non-regression ratchet, pairwise delta antisymmetry)
  6. `MegaAtlasProofs/VerifyAxioms.lean` (81 lines) — `#print axioms` verification for all 58 theorems
  7. `MegaAtlasProofs.lean` (12 lines) — root library export
- **Audit Result:** `Build completed successfully (9 jobs)`; **0 warnings**, **0 `sorry`**, **0 `admit`**, **0 `native_decide`**, **0 custom axioms**; all 58 audited theorems strictly within `[propext, Quot.sound]` or empty (no `Classical.choice` required).

## Independent Falsification Commands

```bash
# 1. Verify all 46 Pure Lean 4.35.0 theorems & print axioms
cd lean && lake build && cd ..

# 2. Run the full pytest verification suite (schema, math, graph, parity, RAG, checksums)
pytest -v

# 3. Run the standalone cryptographic & structural auditor (including Lean check)
python scripts/audit_atlas.py --check-lean
```
