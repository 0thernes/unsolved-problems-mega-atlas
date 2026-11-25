# Replication Protocol (`REPLICATION.md`)

Any independent researcher can verify all `1,900` records, `5,808` graph edges, `72` Pure Lean 4.35.0 theorems, `100% MRR@5` offline RAG benchmark, dual-framed 9-tool MCP server, FAIR metadata, and byte-exact SHA-256 digests from a clean clone.

## 1. Clean-Clone Verification Steps

```bash
git clone https://github.com/0thernes/unsolved-problems-mega-atlas.git
cd unsolved-problems-mega-atlas
python3 -m pip install -r requirements.txt

# 1. Verify master loader, 48-field JSON Schema, biconnected graph & forensic audit
python3 src/v2_loader.py
python3 scripts/forensic_audit.py

# 2. Run full pytest suite (existing 25 tests + Build Standard property/mutation/integrity tests)
python3 -m pytest -v

# 3. Run cryptographic SHA-256 auditor, AutoResearch oracle & Zenodo dry-run
python3 scripts/audit_atlas.py
python3 autoresearch/evaluate.py --verify-gates
python3 scripts/publish_zenodo.py --dry-run

# 4. Verify all 72 Pure Lean 4.35.0 formal invariant theorems (zero Mathlib, ~15s)
cd lean && lake build && cd ..

# 5. Run Build Standard v1.2.0 repo audit
bash scripts/audit-repo.sh .
```

## 2. Full From-Scratch Regeneration

To regenerate all 15 PNG/SVG charts, all 12 export formats, SQLite+FTS5 DB, `RANKING.md`, FAIR JSON-LD manifests, and `CHECKSUMS.sha256` from the modular Python source under `src/v2_data/`:

```bash
make all        # Linux / macOS / WSL
# or:
.\build.ps1     # Windows PowerShell
```

## 3. Replication Log

| Date | Replicator | Environment | Version | Lean (72 Thms) | Pytest + Audits | Notes |
|---|---|---|---|---|---|---|
| 2026-11-21 | Alexander S. Donahue (author) | Windows 11 + Ubuntu CI, Lean 4.35.0, Python 3.12 | `v2.3.0` | PASS (72/72) | PASS (25/25) | Initial V2.3.0 biconnected release. |
| 2026-11-25 | Alexander S. Donahue (author) | Windows 11, Lean 4.35.0, Python 3.13.12 | `v2.3.1` | PASS (72/72) | PASS (all tests + hypothesis/mutation/ruff/mypy) | Build Standard v1.2.0 hardening, R4 remediation, 0/1,900 archive solved-audit. |
| 2026-11-25 | GitHub Actions CI (`ubuntu-latest`, `windows-latest`, `macos-latest`) | Hosted runners, Lean 4.35.0, Python 3.12 | `v2.3.1` | PASS (72/72) | PASS (3 OSes) | Automated cross-platform CI + release `SHA256SUMS` + SLSA attestation. |

*External replications are warmly invited — open an issue with the `replication` label to append your verified run here.*
