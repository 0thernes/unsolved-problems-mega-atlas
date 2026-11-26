# SPDX-License-Identifier: Apache-2.0
.PHONY: all charts export fair lean paper test lint typecheck mutate bench audit forensic zenodo-dry-run evaluate rag mcp clean

PYTHON ?= python

all: charts export fair lean paper audit forensic zenodo-dry-run evaluate test lint typecheck mutate

charts:
	$(PYTHON) src/v2_charts.py

export:
	$(PYTHON) src/v2_export_all.py --skip-pdf

fair:
	$(PYTHON) scripts/generate_fair_metadata.py
	$(PYTHON) scripts/generate_llms_full.py

lean:
	cd lean && lake build && lake env lean MegaAtlasProofs/VerifyAxioms.lean
	$(PYTHON) scripts/check_readme_axioms.py

paper:
	$(PYTHON) scripts/build_paper.py
	$(PYTHON) scripts/check_citations.py

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src rag mcp_server reference scripts examples tests

typecheck:
	$(PYTHON) -m mypy src rag mcp_server reference scripts examples --ignore-missing-imports

mutate:
	$(PYTHON) scripts/run_mutation_audit.py

bench:
	$(PYTHON) scripts/benchmark_atlas.py

audit:
	$(PYTHON) scripts/audit_atlas.py --sync-checksums --check-lean

forensic:
	$(PYTHON) scripts/forensic_audit.py

zenodo-dry-run:
	$(PYTHON) scripts/publish_zenodo.py --dry-run

evaluate:
	$(PYTHON) autoresearch/evaluate.py --verify-gates

rag:
	$(PYTHON) rag/query.py "turbulence climate sensitivity" --top 5 --hops 1

mcp:
	$(PYTHON) mcp_server/server.py

clean:
	rm -rf build paper/build .pytest_cache .mypy_cache .ruff_cache __pycache__ src/__pycache__ src/v2_data/__pycache__ tests/__pycache__ rag/__pycache__ autoresearch/__pycache__ mcp_server/__pycache__
