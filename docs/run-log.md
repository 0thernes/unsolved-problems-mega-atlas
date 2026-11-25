# Verification & Audit Run Log (`docs/run-log.md`)

| Date (UTC) | Version | Scope | Outcome |
|---|---|---|---|
| 2026-11-21 | `v2.3.0` (`c735b9f`) | 1,900-node biconnected connectome, 48 fields, 72 Pure Lean theorems, 100% RAG MRR@5, 9-tool dual-framed MCP | 25/25 pytest PASS; 72/72 Lean PASS; baseline Build Standard v1.2.0 score **40.0% (22/55)**. |
| 2026-11-25 | `v2.3.1` | Build Standard v1.2.0 hardening: removed R4-banned `PULL_REQUEST_TEMPLATE.md`, replaced unformed `0thernes LLC` in active governance/metadata, added `docs/0THERNES_SOLVED_AUDIT_2026-11-25.md`, `repo.yaml`, `CLAIMS.md`, `LIMITATIONS.md`, `REPLICATION.md`, `justfile`, Hypothesis/mutation tests, cross-platform CI, `SHA256SUMS` + SLSA release workflow | Full `pytest` (original 25 + new Build Standard/property/mutation tests) PASS; 72/72 Lean PASS; `audit_atlas.py`, `forensic_audit.py`, `evaluate.py --verify-gates`, `publish_zenodo.py --dry-run` PASS; CI verified green across `ubuntu`, `windows`, `macos`. |
