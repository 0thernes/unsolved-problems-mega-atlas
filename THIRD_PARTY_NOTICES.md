# Third-Party Notices & Attributions

This repository bundles no third-party vendored source code, but builds upon and
interoperates with the following open-source toolchains, libraries, and standards.
All licenses are compatible with this repository's dual **Apache-2.0 (code) / CC-BY-4.0 (data & paper)** license.

| Component | Version / Standard | License | Usage in This Repository |
|---|---|---|---|
| **Lean 4** (`leanprover/lean4`) | `v4.35.0` | Apache-2.0 | Primary proof kernel, `lake`, `leanchecker`, `leanchecker-paranoid`, `leanexport`, `lake comparator` |
| **lean4lean** | Bundled w/ Lean `v4.35.0` | Apache-2.0 | Independent Lean 4 kernel implemented in Lean 4 |
| **nanoda_bin** | Bundled w/ Lean `v4.35.0` | MIT / Apache-2.0 | Independent Rust kernel verifying `.export` terms |
| **con-leche** / **con-ron** | Bundled w/ Lean `v4.35.0` | Apache-2.0 / MIT | Independent external proof checkers (`--verified`) |
| **Python & Standard Library** | `3.10+` (`3.12` tested) | PSF-2.0 | Data loader, exporter, RAG/MCP servers, test & audit scripts |
| **pandas** | `>=2.0` | BSD-3-Clause | Tabular aggregation and cross-tabulation matrices |
| **NumPy** | `>=1.26` | BSD-3-Clause | Numerical array operations |
| **NetworkX** | `>=3.2` | BSD-3-Clause | Biconnectivity, PageRank, betweenness, modularity analytics |
| **Matplotlib** | `>=3.8` | PSF-based | 15 PNG/SVG charts, 5 vector PDF paper figures, social card |
| **Seaborn** | `>=0.13` | BSD-3-Clause | Statistical distribution & heatmap visualization |
| **openpyxl** | `>=3.1` | MIT | 15-sheet XLSX workbook export |
| **xlwt** | `>=1.3` | BSD-3-Clause | 8-sheet legacy BIFF `.xls` export |
| **jsonschema** | `>=4.20` | MIT | Draft 2020-12 JSON Schema validation on all 1,900 records |
| **pytest** | `>=8.0` | MIT | Automated test suite |
| **Hypothesis** | `>=6.100` | MPL-2.0 | Property-based testing (`1,000+` examples/property) |
| **Ruff** | `>=0.15` | MIT | Static lint checks |
| **mypy** | `>=1.10` | MIT | Static type checking |
| **Tectonic** | `>=0.15` | MIT | Self-contained AMS-LaTeX PDF white-paper compiler |
| **SQLite 3 + FTS5** | Python built-in | Public Domain | Deterministic offline Porter-stemmed full-text search index |
| **MLCommons Croissant 1.0** | Spec `1.0` | Apache-2.0 | Machine-readable dataset metadata (`croissant.json`) |
| **RO-Crate 1.1** | Spec `1.1` | Apache-2.0 | Scholarly packaging descriptor (`ro-crate-metadata.json`) |
| **Karpathy AutoResearch** | Pattern reference | MIT | Inspiration for immutable `autoresearch/evaluate.py` + `program.md` |
| **Build Standard for LLMs** | `v1.2.0` | MIT / CC-BY-4.0 | 90-item engineering & verification standard (`docs/build-standard.md`) |

No proprietary fonts, closed-source SDKs, or unattributed third-party assets are included.
