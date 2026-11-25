# Upgrading & Deprecation Guide (`UPGRADING.md`)

## Semantic Versioning Policy

- **MAJOR (`X.0.0`):** Breaking changes to the 48-field JSON Schema (`schema/problem.schema.json`), SQLite table schemas, or MCP tool signatures.
- **MINOR (`2.X.0`):** Additive columns, new problems, new MCP tools, new Lean invariant modules, or new export formats that preserve backward compatibility for existing fields and Problem IDs.
- **PATCH (`2.3.X`):** Governance, verification, CI, metadata, and bug-fix updates leaving all 1,900 Problem IDs, 48 schema columns, and 9 MCP tool signatures intact.

## Upgrading from `v2.3.0` to `v2.3.1`

- **Zero breaking changes** to `outputs/*`, `schema/problem.schema.json`, `rag/query.py`, `mcp_server/server.py`, or `lean/MegaAtlasProofs/`.
- Removed `.github/PULL_REQUEST_TEMPLATE.md` (Build Standard `R4` compliance).
- Replaced unformed-entity `"0thernes LLC"` strings in active governance/metadata files with `Independent Researcher, Spokane, WA, USA` (matching ORCID `0009-0006-8168-9648`).
- Added Build Standard v1.2.0 infrastructure (`repo.yaml`, `justfile`, `CLAIMS.md`, `LIMITATIONS.md`, `REPLICATION.md`, `docs/0THERNES_SOLVED_AUDIT_2026-11-25.md`, `data/MANIFEST.sha256`, cross-platform CI, `release.yml` with `SHA256SUMS` + SLSA attestation, and `tests/test_build_standard_and_properties.py`).

## Deprecation Policy

No existing Problem ID is deleted without being redirected via `EXPLICIT_DUPLICATE_ALIASES` in `src/v2_loader.py`. Deprecated MCP tools or CLI flags will be retained for at least one MINOR version with deprecation notes in `CHANGELOG.md`.
