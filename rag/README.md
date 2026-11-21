# Offline Deterministic Hybrid RAG & Knowledge-Graph Query Engine (`rag/`)

Zero-API, deterministic **Hybrid BM25 + Contiguous Title Bigram + Unique-Token Coverage + NetworkX PageRank Graph-Authority** retrieval (**`100.00% MRR@5`, `25/25` top-1** on the immutable cross-pillar benchmark) over all **1,900 problems (48 fields)** and **5,808 biconnected knowledge-graph edges** in `outputs/MegaAtlas_Unsolved_Problems_V2.sqlite` (SQLite 3 + FTS5 Porter tokenizer).

## Usage Examples

```bash
# Free-text Hybrid BM25+PageRank retrieval + 1-hop knowledge-graph neighbor expansion
python rag/query.py "turbulence climate sensitivity" --top 8 --hops 1

# Side-by-side comparison with Lean-verified antisymmetric deltas & shared neighbors
python rag/query.py --compare NT-001 CS-001

# Audit all 12 unverified Fall/Nov 2026 AI proof claims
python rag/query.py --flag ai-claim-under-audit-nov2026 --top 20

# Inspect a specific flagship hub and its 1-hop coupled problems
python rag/query.py --problem NT-001 --hops 1

# Filter by Macro-Pillar and emit machine-readable JSON for downstream LLM agents
python rag/query.py "quantum gravity holography" --pillar "Fundamental Physics & Cosmos" --top 5 --hops 1 --json
```

Every hit returns exact Problem IDs, Macro-Pillar, Superdomain, Substrate, Abstraction Layer, `0thernes CSS`, `Titan Index`, Gradient, Margin Role, `status_2026`, `verification_flag`, `core_question`, `formal_expression`, and coupled graph neighbors in `< 30 ms`.
