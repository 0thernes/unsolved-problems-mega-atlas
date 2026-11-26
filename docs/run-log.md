# Experimental & Verification Run Log (`v2.4.0`)

Chronological audit log of quantitative builds, formal verification runs, AutoResearch iterations, mutation audits, and clean-clone replications (Build Standard **B40**).

| Date (UTC) | Run Type | Command / Artifact | Key Metrics & Outcome |
|---|---|---|---|
| 2026-11-20 | `v2.1.0` Baseline | `autoresearch/evaluate.py --log` | `AQS=91.69`, `RAG MRR@5=82.22%` (`19/25`), `1,855` problems, `58` Lean theorems (`baseline`). |
| 2026-11-21 | `v2.2.0` AutoResearch Ratchet | `autoresearch/results.tsv` (`H-001`–`H-004`) | Staged FTS5 + Hybrid Title-Bigram + PageRank re-ranker kept (`H-001`, `H-003`); `H-002` & `H-004` honestly discarded. `AQS -> 96.49`, `MRR@5 -> 94.93%`. |
| 2026-11-21 | `v2.3.0` Forensic Biconnectivity & Multi-Layer Upgrade | `scripts/forensic_audit.py` + `autoresearch/evaluate.py` | Fixed 10 dangling links, eliminated `GEOM-038` articulation point, merged 12 duplicates (`1,900` unique, `5,808` edges, `0` APs), reached `100.0% MRR@5` (`25/25`), `AQS=97.99`, `72` Lean theorems, Track B Antihydra pilot. |
| 2026-11-25 | `v2.4.0` Cycle 1 — 6-Kernel Lean 4.35.0 Palomar & `<5 MB` Hygiene | `lake build` + `VerifyAxioms.lean` + `leanchecker-paranoid` + `con-leche` + `con-ron` + `nanoda_bin` + `src/v2_export_all.py` | Upgraded to `92` Lean 4.35.0 theorems (`12` NonVacuity + `8` Palomar specs; `1,753` decls accepted; axioms `⊆ [propext, Quot.sound]`); shrank Interactive HTML `20.64 MB -> 3.80 MB`; cured legal affiliation (`0` `0thernes LLC` hits); upgraded code license to `Apache-2.0`. |
| 2026-11-25 | `v2.4.0` Cycle 2 — AMS-LaTeX White Paper & Verification Ladder | `scripts/build_paper.py` + `scripts/check_citations.py` + `scripts/run_mutation_audit.py` + `scripts/benchmark_atlas.py` | Compiled 10-page AMS-LaTeX PDF (`0.672 MB`, `0` overfull hboxes, `0` warnings) + clean-room `arxiv_submission.tar.gz` (`0.498 MB`); `12/12` live citations HTTP/DOI 200; 50-digit reference oracle + Hypothesis + `6/6` (100%) mutation kill rate + 10-iteration benchmarks. |
| 2026-11-25 | `v2.4.0` Cycle 3 — 10-Pass Red-Team Audit & Clean Replication | `scripts/Audit-Repo.ps1` + clean-clone replication + GitHub Actions CI | Full details recorded in `HARDENING_LOG.md`, `docs/reviews/2026-11-25-redteam-hardening.md`, and `REPLICATION.md`. |
