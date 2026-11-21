# Security, Integrity & Epistemic-Tampering Policy

## Supported Versions

| Version | Supported |
|---|---|
| `2.2.x` (current) | ✅ Yes |
| `2.1.x` | Security/checksum advisories only |
| `< 2.1.0` | ❌ Superseded |

## Scope of Security & Integrity Reports

Because this repository distributes executable research infrastructure (`mcp_server/server.py`, `rag/query.py`, Python exporters, SQLite FTS5 databases, HTML dashboards) AND cryptographically audited scientific artifacts (`CHECKSUMS.sha256`, Pure Lean 4.35.0 proofs), we treat **all** of the following as high-priority issues:

1. **Software / Injection Vulnerabilities:** SQL injection in `rag/query.py` or `mcp_server/server.py`, XSS in `MegaAtlas_Interactive_Dashboard_V2.html`, or unsafe path/command handling in build scripts.
2. **Cryptographic & Checksum Tampering:** Any mismatch between committed files, `CHECKSUMS.sha256`, `croissant.json`, `ro-crate-metadata.json`, or pinned Git submodule commits in `0thernes/0thernes-research-archive` (`0TH-BUILD-007`).
3. **Formal-Proof Axiom Smuggling:** Any attempt to introduce `sorry`, `admit`, `native_decide`, `Lean.ofReduceBool`, or custom `axiom` declarations inside `lean/MegaAtlasProofs/`.
4. **Epistemic / Citation Integrity Attacks:** Fabricated citations, silently retired open problems lacking peer consensus, or unauthorized modifications to the immutable AutoResearch oracle (`autoresearch/evaluate.py`).

## Reporting a Vulnerability or Integrity Defect

Please report security or integrity issues directly to **Alexander Stephen Donahue** (`0_0@0thernes.art`, ORCID `0009-0006-8168-9648`) or via GitHub Private Security Advisories / `.github/ISSUE_TEMPLATE/status-update-or-falsification.yml`. We acknowledge reports within 48 hours and publish transparent post-mortems for any confirmed defect.
