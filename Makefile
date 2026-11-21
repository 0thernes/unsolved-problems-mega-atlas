.PHONY: all charts export fair lean test audit evaluate rag mcp clean

PYTHON ?= python

all: charts export fair lean audit evaluate test

charts:
	$(PYTHON) src/v2_charts.py

export:
	$(PYTHON) src/v2_export_all.py

fair:
	$(PYTHON) scripts/generate_fair_metadata.py

lean:
	cd lean && lake build

test:
	$(PYTHON) -m pytest -v

audit:
	$(PYTHON) scripts/audit_atlas.py --sync-checksums --check-lean

evaluate:
	$(PYTHON) autoresearch/evaluate.py --verify-gates

rag:
	$(PYTHON) rag/query.py "turbulence climate sensitivity" --top 5 --hops 1

mcp:
	$(PYTHON) mcp_server/server.py

clean:
	rm -rf .pytest_cache __pycache__ src/__pycache__ src/v2_data/__pycache__ tests/__pycache__ rag/__pycache__ autoresearch/__pycache__ mcp_server/__pycache__
