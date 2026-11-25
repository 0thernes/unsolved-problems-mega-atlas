# Task runner for unsolved-problems-mega-atlas (Build Standard v1.2.0, A31 & B01)
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

setup:
    python3 -m pip install -r requirements.txt

test:
    python3 -m pytest -v

lean:
    cd lean && lake build

lint:
    python3 -m ruff check src/ scripts/ rag/ mcp_server/ autoresearch/ tests/ || true
    python3 -m mypy --ignore-missing-imports scripts/ rag/ mcp_server/ || true

reproduce:
    python3 src/v2_loader.py
    python3 scripts/forensic_audit.py
    python3 scripts/audit_atlas.py
    python3 autoresearch/evaluate.py --verify-gates
    python3 scripts/publish_zenodo.py --dry-run
    python3 -m pytest -v
    bash scripts/audit-repo.sh .

audit:
    bash scripts/audit-repo.sh .
