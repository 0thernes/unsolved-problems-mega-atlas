# Roadmap

## Completed (`v2.3.1`)
- `1,900` strictly deduplicated problems across `8` Macro-Pillars × `28` Superdomains × `8` Substrates × `7` Abstraction Layers (`48` typed fields, `0` dangling links, biconnected `5,808`-edge graph).
- `72` Pure Lean 4.35.0 formal invariant theorems (`0` Mathlib, `0` `sorry`, strictly `[propext, Quot.sound]` or empty).
- `100.0% MRR@5` offline Hybrid BM25+PageRank RAG CLI, dual-framed 9-tool MCP stdio server, Karpathy AutoResearch harness, and FAIR Croissant 1.0 / RO-Crate 1.1 / Zenodo metadata.
- Build Standard v1.2.0 hardening (cross-platform CI, `SHA256SUMS` + Sigstore SLSA releases, Hypothesis/mutation tests, R4 banned-file removal, honest `0/1,900` archive solved-problem audit).

## Planned
- Periodic quarterly audits of the `12` Fall/Nov 2026 AI proof claims (`verification_flag = "ai-claim-under-audit-nov2026"`) as independent human fidelity reviews conclude.
- Optional Zenodo Versioned DOI minting using `scripts/publish_zenodo.py` once manual review is completed.
- Community-submitted falsification/status updates via `.github/ISSUE_TEMPLATE/status-update-or-falsification.yml`.

## Not Planned
- Claiming automatic retirement of open problems based solely on unreviewed AI preprints or unverified Lean builds.
- Adding hosted cloud API dependencies to the offline RAG CLI or MCP server.
- Removing the standalone committed `outputs/` snapshot required for zero-dependency GitHub Pages and offline replication (see `docs/adr/0002-dual-license-and-committed-atlas-artifacts.md`).
