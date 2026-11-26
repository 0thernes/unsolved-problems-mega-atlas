# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| `2.4.x` (`main`) | Yes |
| `< 2.4.0` | No — upgrade to `2.4.0` (`UPGRADING.md`) |

## Reporting a Vulnerability

If you discover a security vulnerability in the MCP stdio server (`mcp_server/server.py`),
SQLite FTS5 query sanitizer (`rag/query.py`), HTML escaping (`src/v2_export_all.py`), Lean
verification scripts, or GitHub Actions workflows, **please do not file a public issue**.

Report privately via email to **`0_0@0thernes.art`** (Alexander Stephen Donahue, Independent
Researcher, ORCID `0009-0006-8168-9648`) with:
1. A clear description of the vulnerability and affected file/line.
2. Minimal reproduction input or payload.
3. Any suggested mitigation.

You will receive an acknowledgement within 72 hours and a coordinated resolution timeline.

## Threat Model & Hardening Controls

See [`docs/threat-model.md`](docs/threat-model.md) for the complete STRIDE + OWASP LLM
security analysis (parameterized SQLite queries, FTS5 token sanitization, HTML/JSON XSS
escaping, zero hardcoded secrets, zero runtime network calls, and CI secret scanning).
