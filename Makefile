.PHONY: all charts export lean test audit rag clean

PYTHON ?= python

all: charts export lean test audit

charts:
	$(PYTHON) src/v2_charts.py

export:
	$(PYTHON) src/v2_export_all.py

lean:
	cd lean && lake build

test:
	$(PYTHON) -m pytest -v

audit:
	$(PYTHON) scripts/audit_atlas.py --sync-checksums --check-lean

rag:
	$(PYTHON) rag/query.py "turbulence climate sensitivity" --top 5 --hops 1

clean:
	rm -rf .pytest_cache __pycache__ src/__pycache__ src/v2_data/__pycache__ tests/__pycache__ rag/__pycache__
