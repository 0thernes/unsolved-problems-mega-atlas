# Cryptographic Evidence & Provenance Dossier

**Project:** Unsolved Problems Mega-Atlas (`v2.3.0`)  
**Author / Curator:** Alexander Stephen Donahue (`Independent Researcher (0thernes)`, Spokane, WA, USA)  
**ORCID:** [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648)  
**Repository:** [https://github.com/0thernes/unsolved-problems-mega-atlas](https://github.com/0thernes/unsolved-problems-mega-atlas)  
**Interactive Web Atlas (GitHub Pages):** [https://0thernes.github.io/unsolved-problems-mega-atlas/](https://0thernes.github.io/unsolved-problems-mega-atlas/)  
**Master Research Archive Registration:** `0TH-BUILD-007` in [`0thernes/0thernes-research-archive`](https://github.com/0thernes/0thernes-research-archive)

---

## Verification & Integrity Matrix

| Evidence Layer | Artifact / Command | Status |
|---|---|---|
| **Pure Lean 4.35.0 Invariants** | `cd lean && lake build` (`MegaAtlasProofs/VerifyAxioms.lean`) | **72 theorems verified** (8 files, 1,008 lines) · 0 warnings · 0 `sorry` · 0 `native_decide` · 0 `Classical.choice` · `[propext, Quot.sound]` or empty |
| **JSON Schema Draft 2020-12** | `schema/problem.schema.json` + `schema/atlas.schema.json` | **1,900 / 1,900 records valid** across all **48 typed columns** |
| **Forensic Graph & Blindspot Audit** | `python scripts/forensic_audit.py` + `docs/FORENSIC_AUDIT_V2.3.md` | **0 unresolved raw links**, **0 articulation points**, **0 bridge edges** (`nx.is_biconnected(G) == True`), 12 cross-field duplicates merged |
| **FAIR Scholarly & Zenodo Pipeline** | `.zenodo.json` · `croissant.json` · `ro-crate-metadata.json` · `scripts/publish_zenodo.py --dry-run` · `docs/DATASHEET.md` | MLCommons Croissant 1.0 (48 fields) + W3C RO-Crate 1.1 + Zenodo ORCID dry-run validated byte-exact |
| **Karpathy AutoResearch Oracle** | `python autoresearch/evaluate.py --verify-gates` (`autoresearch/results.tsv`) | Immutable 5-axis **`AQS = 97.99`** + 25-query Hybrid BM25+PageRank RAG (**`100.00% MRR@5`**, `25/25` top-1) |
| **Track B Frontier Pilot** | `research/runs/LOG-002_antihydra_pilot/` (`antihydra_probe.py` + `RESULTS.json`) | Reproducible 5,000-step exact big-int Antihydra (`BB(6)`) simulation + 99-seed sweep (strictly non-claimant empirical pilot) |
| **Dual-Framed 9-Tool MCP Server** | `mcp_server/server.py` (tested over NDJSON & `Content-Length:` in `pytest`) | 9 grounded tools live over SQLite FTS5 + 5,808-edge biconnected graph |
| **Automated Test Suite** | `pytest -v` (`tests/test_mega_atlas.py`) | **25/25 PASS** (schema, scoring, layer/gradient invariants, biconnectivity, parity, 100% RAG, dual-framed 9-tool MCP, AutoResearch, Track B, FAIR, Zenodo dry-run, ORCID, 72 Lean thms, SHA-256) |
| **Cryptographic Manifest** | `CHECKSUMS.sha256` (`python scripts/audit_atlas.py --check-lean`) | Byte-exact SHA-256 across all frozen datasets, SQLite FTS5 DB, 30 chart files, HTML, PDF, `RANKING.md`, schemas, FAIR JSONs, forensic/preservation docs & Track B `RESULTS.json` |
| **Continuous Integration** | `.github/workflows/ci.yml` (2 jobs: Python/Forensic/MCP Audit + 72-Theorem Lean 4.35.0 Build) | Automated on every push & PR to `main` |
| **Live Web Publication** | `.github/workflows/pages.yml` (GitHub Pages) | Automated deployment of standalone interactive dashboard, 30 charts & FAIR/LLM manifests |
| **External Archival (Options 1 & 2)** | `docs/PRESERVATION.md` + `scripts/publish_zenodo.py` | Zenodo DOI awaits user `ZENODO_TOKEN`/webhook; Software Heritage SWHID awaits manual browser click due to Anubis PoW gate (never fabricated or bypassed) |
| **External Peer Review / DOI** | None claimed | Explicitly disclosed as independent solo human + AI-assisted preprint/dataset; external review welcome via [`docs/ACADEMIC_REVIEW.md`](docs/ACADEMIC_REVIEW.md) |

## Dataset Key Statistics (`v2.3.0`)

- **Total Deduplicated Open / Hard Problems:** `1,900` (from `1,912` raw authored entries across 11 modules; `12` cross-field overlaps cleanly merged with `0` unresolved raw links)
- **Multi-Layer Taxonomy:** `8` Macro-Pillars × `28` Superdomains × `8` Physical/Formal Substrates × `7` Abstraction Layers (`L0–L6`) × `1,752` fine-grained subdomains (`88` canonical hub anchors)
- **Biconnected Connectome:** `5,808` undirected edges · `1` single connected component (`1,900/1,900`) · `0` articulation points · `0` bridge edges · `35.7%` cross-superdomain (`2,076`) · `18.7%` cross-pillar (`1,084`) · `14` greedy modularity communities · average degree `6.11` (`∑ deg = 11,616`)
- **Scoring & Multi-Layer Means:** `0thernes CSS = 57.33 / 100` · `Titan Index = 7.31 / 10` · Difficulty = `8.13` · Tractability (2050) = `6.81` · Impact = `7.22` · Gradient (`D − T`) = `+1.32` · `CSS − Titan×10` Margin = `-15.76` · Bridge Ratio = `0.131` · Adjacent Pillars = `0.61`
- **Epistemic Verification Flags:** `ai-assisted-editorial-synthesis` (`952`), `primary-registry-indexed` (`925`), `ai-claim-under-audit-nov2026` (`12`), `disputed-human-claim` (`11`)
- **Structural Margin Roles:** `Intra-Pillar Bridge` (`1,108`), `Core Intra-Pillar Specialist` (`485`), `Trans-Pillar Boundary Interface` (`239`), `Apex Multi-Pillar Keystone (3+ Adj)` (`68`)
- **Historical Span:** `500 BCE` to `2026` (median formulation year `1979`, median age `47` years in `2026`)

## One-Command Independent Reproduction

```bash
git clone https://github.com/0thernes/unsolved-problems-mega-atlas.git
cd unsolved-problems-mega-atlas
pip install -r requirements.txt
pytest -v
python scripts/audit_atlas.py --check-lean
python scripts/forensic_audit.py
python autoresearch/evaluate.py --verify-gates
python rag/query.py "turbulence climate sensitivity" --top 5 --hops 1
```
