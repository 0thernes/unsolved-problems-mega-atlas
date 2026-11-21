# Cryptographic Evidence & Provenance Dossier

**Project:** Unsolved Problems Mega-Atlas (`v2.2.0`)  
**Author / Curator:** Alexander Stephen Donahue (`0thernes LLC`, Spokane, WA, USA)  
**ORCID:** [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648)  
**Repository:** [https://github.com/0thernes/unsolved-problems-mega-atlas](https://github.com/0thernes/unsolved-problems-mega-atlas)  
**Interactive Web Atlas (GitHub Pages):** [https://0thernes.github.io/unsolved-problems-mega-atlas/](https://0thernes.github.io/unsolved-problems-mega-atlas/)  
**Master Research Archive Registration:** `0TH-BUILD-007` in [`0thernes/0thernes-research-archive`](https://github.com/0thernes/0thernes-research-archive)

---

## Verification & Integrity Matrix

| Evidence Layer | Artifact / Command | Status |
|---|---|---|
| **Pure Lean 4.35.0 Invariants** | `cd lean && lake build` (`MegaAtlasProofs/VerifyAxioms.lean`) | **58 theorems verified** (7 files, 817 lines) · 0 warnings · 0 `sorry` · 0 `native_decide` · `[propext, Quot.sound]` or empty |
| **JSON Schema Draft 2020-12** | `schema/problem.schema.json` + `schema/atlas.schema.json` | **1,855 / 1,855 records valid** |
| **FAIR Scholarly Metadata** | `.zenodo.json` · `croissant.json` · `ro-crate-metadata.json` · `docs/DATASHEET.md` | MLCommons Croissant 1.0 + W3C RO-Crate 1.1 + Zenodo ORCID + Gebru Datasheet synced byte-exact |
| **Karpathy AutoResearch Oracle** | `python autoresearch/evaluate.py --verify-gates` (`autoresearch/results.tsv`) | Immutable 5-axis AQS + 25-query Hybrid BM25+Graph RAG benchmark (`96.0% MRR@5`, 23/25 top-1) |
| **MCP Stdio Research Server** | `mcp_server/server.py` (tested end-to-end via JSON-RPC 2.0 in `pytest`) | 7 grounded tools live over SQLite FTS5 + 5,597-edge graph |
| **Automated Test Suite** | `pytest -v` (`tests/test_mega_atlas.py`) | **100% PASS** (schema, scoring, comparator, graph handshaking, parity, RAG, MCP stdio, AutoResearch, FAIR, ORCID, Lean hygiene, SHA-256) |
| **Cryptographic Manifest** | `CHECKSUMS.sha256` (`python scripts/audit_atlas.py --check-lean`) | Byte-exact SHA-256 across all frozen datasets, SQLite FTS5 DB, 24 charts, HTML, PDF, `RANKING.md`, schemas & white paper |
| **Continuous Integration** | `.github/workflows/ci.yml` (2 jobs: Python Audit + Lean 4.35.0 Build) | Automated on every push & PR to `main` |
| **Live Web Publication** | `.github/workflows/pages.yml` (GitHub Pages) | Automated deployment of standalone interactive dashboard & charts |
| **Software Heritage Preservation** | [Save Code Now](https://archive.softwareheritage.org/save/) (manual browser submission required due to Anubis PoW anti-bot gate) | Pending manual user click; never bypassed programmatically |
| **External Peer Review / DOI** | None claimed | Explicitly disclosed as independent solo human + AI-assisted preprint/dataset; external review welcome via [`docs/ACADEMIC_REVIEW.md`](docs/ACADEMIC_REVIEW.md) |

## Dataset Key Statistics (`v2.1.0`)

- **Total Deduplicated Open / Hard Problems:** `1,855` (from `1,860` raw authored entries; `5` cross-field overlaps cleanly merged)
- **Taxonomy:** `8` Macro-Pillars × `28` Superdomains × `1,705` fine-grained subdomains (`88` canonical hub anchors)
- **Connectome:** `5,597` undirected edges · `1` single connected component (`1,855/1,855`) · `34.6%` cross-superdomain (`1,934`) · `17.6%` cross-pillar (`983`) · `11` greedy modularity communities · average degree `6.03`
- **Scoring:** Mean `0thernes CSS` = `57.32 / 100` · Mean `Titan Index` = `7.30 / 10` · Mean Difficulty = `8.14` · Mean Tractability (2050) = `6.78` · Mean Civilizational Impact = `7.19`
- **Epistemic Verification Flags:** `primary-registry-indexed` (`687`), `ai-assisted-editorial-synthesis` (`1,145`), `ai-claim-under-audit-nov2026` (`12`), `disputed-human-claim` (`11`)
- **Historical Span:** `500 BCE` to `2024` (median formulation year `1979`, median age `47` years in `2026`)

## One-Command Independent Reproduction

```bash
git clone https://github.com/0thernes/unsolved-problems-mega-atlas.git
cd unsolved-problems-mega-atlas
pip install -r requirements.txt
pytest -v
python scripts/audit_atlas.py --check-lean
python rag/query.py "turbulence climate sensitivity" --top 5 --hops 1
```
