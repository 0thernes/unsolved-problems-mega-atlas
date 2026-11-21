# Academic & Domain-Specialist Review Protocol

The **Unsolved Problems Mega-Atlas** is published openly as a **living, falsifiable research instrument** (not yet externally peer-reviewed). We explicitly invite mathematicians, physicists, chemists, biologists, neuroscientists, computer scientists, engineers, economists, and philosophers to audit any superdomain or individual entry.

## How to Submit a Domain Audit

1. Open an issue using the **Academic / Specialist Review** template (`.github/ISSUE_TEMPLATE/academic-review.yml`) or open a Pull Request editing `src/v2_data/m*.py`.
2. Reference specific Problem IDs (e.g., `NT-001`, `ANL-001`, `GR-001`, `BIO-001`) and evaluate any of the following dimensions:
   - **Statement Fidelity:** Does `core_question` and `formal_expression` accurately represent the open problem without conflating distinct conjectures?
   - **Historical Provenance:** Are `year_formulated`, `originator`, and `registry_source` historically accurate?
   - **Status Accuracy (Nov 2026):** Has the problem been resolved, disproved, shown independent, or materially updated since the snapshot date?
   - **Rubric Calibration:** Are `difficulty_score`, `tractability_2050`, `civilizational_impact`, and `interdisciplinarity_index` well-calibrated relative to peer problems in the same superdomain?
   - **Coupling Accuracy:** Are `related_problem_ids` mathematically or causally justified? Are major cross-domain bridges missing?

## Verification Status Promotion Policy

- Records remain flagged `primary-registry-indexed` or `ai-assisted-editorial-synthesis` until an external reviewer provides verifiable primary citations in a merged PR.
- No Fall/Nov 2026 AI proof claim (`ai-claim-under-audit-nov2026`) will be promoted to "Resolved" without **both** independent formal-statement fidelity confirmation and recognized community/institution consensus (e.g., Clay Mathematics Institute, peer-reviewed journal publication, or authoritative registry closure on `ProofAtlas.ai` / `erdosproblems.com`).
- Reviewers who contribute audited corrections are permanently acknowledged (with optional ORCID) in [`AUTHORS.md`](../AUTHORS.md) and release notes.
