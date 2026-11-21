# Offline Deterministic RAG & Knowledge-Graph Query Engine (`rag/`)

Zero-API, deterministic full-text BM25 + graph-hop retrieval over all **1,855 problems** and **5,597 knowledge-graph edges** in `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` (SQLite 3 + FTS5 Porter tokenizer).

## Usage Examples

```bash
# Free-text BM25 retrieval + 1-hop knowledge-graph neighbor expansion
python rag/query.py "turbulence climate sensitivity" --top 8 --hops 1

# Audit all 12 unverified Fall/Nov 2026 AI proof claims
python rag/query.py --flag ai-claim-under-audit-nov2026 --top 20

# Inspect a specific flagship hub and its 1-hop coupled problems
python rag/query.py --problem NT-001 --hops 1

# Filter by Macro-Pillar and emit machine-readable JSON for downstream LLM agents
python rag/query.py "quantum gravity holography" --pillar "Fundamental Physics & Cosmos" --top 5 --hops 1 --json
```

Every hit returns exact Problem IDs, Macro-Pillar, Superdomain, `0thernes CSS`, `Titan Index`, `status_2026`, `verification_flag`, `core_question`, `formal_expression`, and coupled graph neighbors in `< 30 ms`.
