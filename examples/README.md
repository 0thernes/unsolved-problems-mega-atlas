# Runnable Examples (`examples/`)

Every example script in this directory is executed as part of the automated pytest suite (`tests/test_properties_and_differential.py`) and CI workflows.

## 1. Quickstart End-to-End Demo (`quickstart_demo.py`)

Loads all 1,900 problems and the 5,808-edge biconnected graph, runs an offline Hybrid RAG query with 1-hop graph expansion, compares `NT-001` (Riemann Hypothesis) vs. `CS-001` (P vs. NP), and checks differential parity against the 50-digit `Decimal` reference oracle:

```bash
python examples/quickstart_demo.py
```

## 2. Offline RAG CLI Examples

```bash
python rag/query.py "quantum gravity black hole information" --top 5 --hops 1
python rag/query.py --compare ANL-001 FLD-001 --json
python rag/query.py --flag ai-claim-under-audit-nov2026 --top 15
```

## 3. Track B Finite Computational Probe (`LOG-002` Antihydra)

```bash
python research/runs/LOG-002_antihydra_pilot/antihydra_probe.py
```
