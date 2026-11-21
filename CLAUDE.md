# CLAUDE.md

See [`AGENTS.md`](AGENTS.md) for the complete AI coding & research agent contract, non-negotiable 0thernes LLC epistemic boundaries, Pure Lean 4.35.0 rules, MCP server usage (`mcp_server/server.py`), and Karpathy-style autonomous research protocol (`autoresearch/program.md`).

Quick verification gate before committing any change:
```bash
cd lean && lake build && cd ..
python scripts/generate_fair_metadata.py
python scripts/audit_atlas.py --sync-checksums --check-lean
python autoresearch/evaluate.py --verify-gates
pytest -v
```
