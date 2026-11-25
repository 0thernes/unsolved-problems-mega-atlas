# Limitations, Epistemic Boundaries & Real-vs-Metaphor (`LIMITATIONS.md`)

## 1. What This Atlas Does and Does Not Claim

- **Zero solved-problem claims:** This repository is a **research taxonomy, knowledge graph, and verification infrastructure** — it makes **zero claim** to solve or retire any of the `1,900` open problems (see also [`docs/0THERNES_SOLVED_AUDIT_2026-11-25.md`](docs/0THERNES_SOLVED_AUDIT_2026-11-25.md)).
- **Editorial vs. formal metrics:** The `72` Pure Lean 4.35.0 theorems (`lean/MegaAtlasProofs/`) verify exact **mathematical properties of the scoring, classification, graph-handshaking, and AutoResearch gate functions** — they do **NOT** prove that the subjective rubric inputs (`difficulty_score`, `tractability_2050`, `civilizational_impact`, `interdisciplinarity_index`) are objective physical constants. Those rubric inputs are transparent, falsifiable editorial estimates.
- **No external peer review:** The catalog, white paper (`docs/WHITE_PAPER.md`), and rubric scores have been authored by solo researcher Alexander Stephen Donahue with disclosed AI assistance (see `docs/AI_DISCLOSURE.md` and `docs/DATASHEET.md`) and have not undergone formal journal peer review.
- **12 Nov 2026 AI proof claims remain unretired:** Lean kernel compilation alone does not establish formalization statement fidelity or community consensus; all 12 AI-targeted problems stay open under `verification_flag = "ai-claim-under-audit-nov2026"`.
- **Committed release artifacts > 5 MB (Build Standard `A24` trade-off):** Six generated dataset/monograph files inside `outputs/` (`MegaAtlas_Comprehensive_Report_V2.pdf`, `MegaAtlas_Interactive_Dashboard_V2.html`, `MegaAtlas_Print_Report_V2.html`, `MegaAtlas_Unsolved_Problems_V2.sqlite`, `.json`, `.jsonl`) exceed 5 MB. They are intentionally committed so GitHub Pages, the offline RAG CLI, the 9-tool MCP server, and `pytest` work directly from a clean clone without external LFS or cloud hosting (see [ADR 0002](docs/adr/0002-dual-license-and-committed-atlas-artifacts.md)).

## 2. Real vs. Metaphor

- **"Connectome" / "Keystone Domino Hubs":** Graph-theoretic metaphors for the literal undirected co-dependency graph $G = (V, E)$ with $|V|=1{,}900$ problem nodes and $|E|=5{,}808$ curated mathematical/scientific dependency edges (measured literally by degree, betweenness centrality, PageRank, and cross-pillar edge count).
- **"Titan Index" / "0thernes CSS":** Named deterministic weighted formulas over `[1..10]` editorial integer scores and problem age (capped at 300 years), formally bounded and proved monotonic in `lean/MegaAtlasProofs/Scoring.lean`.
- **"Biconnected":** Used in its strict graph-theoretic sense (`nx.is_biconnected(G) == True`: 1 connected component, 0 articulation points, 0 bridge edges).
- **"AutoResearch":** Refers to the deterministic, offline keep/discard evaluation loop (`autoresearch/evaluate.py` + `results.tsv`) optimizing local RAG retrieval metrics under locked gates — not autonomous theorem proving of open conjectures.
